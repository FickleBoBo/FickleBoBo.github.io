"""LeetCode #202 Happy Number 포스트의 플로이드 사이클 탐지 도식(GIF 4개)을 다시 만든다.

같은 폴더(`assets/img/posts/leetcode-202/`)의 도식을 만든다:
  floyd-happy-{light,dark}.gif    n = 19(지문 예제 1): slow와 fast가 4번째 반복에 1에서 만난다.
  floyd-unhappy-{light,dark}.gif  n = 2(지문 예제 2): 7번째 반복에 사이클 안의 42에서 만난다.

값은 손으로 적지 않고 풀이와 같은 step·Floyd 로직을 실행해 얻는다. 풀이 코드(`slow = n,
fast = step(n)`)와 같게 fast를 한 칸 앞서 출발시킨다. 색은 IMAGE_STYLE.md 역할표대로
slow=blue, fast=red, 만남=green.

사용법:
    python3 make_diagrams.py [출력 디렉토리]   # 기본: 이 스크립트가 있는 폴더

크기·글자·제목/단계/캡션 위치·전환 속도는 `diagram.py` 공용 틀(IMAGE_STYLE.md)을 따른다. 본문은 GIF만 쓰므로
`emit(..., static=False)`로 SVG는 만들지 않는다. diagram.py를 바꾸면 결과가 달라지니 다시 만든 GIF는 눈으로 확인한 뒤 커밋한다.
"""

import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
REPO = HERE.parents[4]  # assets/img/posts/{slug}/ 기준 레포 루트
sys.path.insert(0, str(REPO / ".claude" / "skills" / "_shared" / "image"))  # diagram.py

from diagram import CANVAS_W, caption, circle, emit, header, line, svg, text

DEFAULT_OUT = HERE.parent
R_NODE = 24


def step(x):
    return sum(int(d) ** 2 for d in str(x))


def floyd_frames(n):
    """풀이 코드와 같은 진행: slow = n, fast = step(n)에서 시작해 만날 때까지 (slow, fast)를 모은다."""
    s, f = n, step(n)
    frames = [(s, f)]
    while s != f:
        s, f = step(s), step(step(f))
        frames.append((s, f))
    return frames


def head(ex, ey, ux, uy, color, size=9):
    bx, by = ex - ux * size, ey - uy * size
    nx, ny = -uy, ux
    return (
        f'<path d="M{ex:.1f} {ey:.1f} L{bx + nx * size * 0.5:.1f} {by + ny * size * 0.5:.1f} '
        f'L{bx - nx * size * 0.5:.1f} {by - ny * size * 0.5:.1f} z" fill="{color}"/>'
    )


def arrow(p, q, color, sw=1.5, r=R_NODE):
    (x1, y1), (x2, y2) = p, q
    d = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / d, (y2 - y1) / d
    sx, sy = x1 + ux * (r + 2), y1 + uy * (r + 2)
    ex, ey = x2 - ux * (r + 4), y2 - uy * (r + 4)
    return line(sx, sy, ex, ey, color, sw) + head(ex, ey, ux, uy, color)


def node(c, pos, val, role):
    x, y = pos
    if role == "meet":
        fill, stroke, sw = c["green_t"], c["green"], 3
    elif role == "slow":
        fill, stroke, sw = c["blue_t"], c["blue"], 3
    elif role == "fast":
        fill, stroke, sw = c["red_t"], c["red"], 3
    else:
        fill, stroke, sw = c["cell"], c["ink"], 2.5
    return circle(x, y, R_NODE, fill, stroke, sw) + text(
        x, y, val, c["text"], 15, weight=600
    )


def tag(c, pos, direction, label, color):
    x, y = pos
    dx, dy = direction
    dist = R_NODE + 14 + 22 * abs(dx)
    return text(x + dx * dist, y + dy * dist, label, color, 14, weight=700)


def make_draw(seq, positions, outward, edges, loops, n, total, verdict):
    W, H = positions["_size"]

    def draw(c, frame, solid_bg):
        k, (s, f) = frame
        body = ""
        for a, b in edges:
            body += arrow(positions[a], positions[b], c["line"])
        for v in loops:  # 1의 자기 반복 화살표
            x, y = positions[v]
            sx, sy = x - 10, y - 23
            ex, ey = x + 8, y - 27
            body += (
                f'<path d="M{sx} {sy} C{x - 34} {y - 74} {x + 34} {y - 74} {ex} {ey}" fill="none" '
                f'stroke="{c["line"]}" stroke-width="1.5" stroke-linecap="round"/>'
            )
            ux, uy = ex - (x + 34), ey - (y - 74)
            d = math.hypot(ux, uy)
            body += head(ex, ey + 1, ux / d, uy / d, c["line"])
        meet = s == f
        for v in seq:
            role = (
                "meet"
                if (meet and v == s)
                else ("slow" if v == s else ("fast" if v == f else ""))
            )
            body += node(c, positions[v], v, role)
        if meet:
            body += tag(c, positions[s], outward[s], "slow = fast", c["green"])
        else:
            body += tag(c, positions[s], outward[s], "slow", c["blue"])
            body += tag(c, positions[f], outward[f], "fast", c["red"])
        body += header(c, f"n = {n}", k, total)
        if k == 0:
            body += caption(c, H - 22, "시작: slow는 n, fast는 step(n)에서 출발한다")
        elif meet:
            body += caption(
                c, H - 22, f"{k}번째 반복에 만난다. {verdict}", c["green"], 700
            )
        else:
            body += caption(
                c, H - 22, f"{k}번째 반복: slow는 한 칸, fast는 두 칸 이동한다"
            )
        return svg(W, H, body, c, solid_bg)

    return draw


def build_unhappy(n=2):
    """꼬리 하나(2) + 8칸 사이클. 사이클은 고리 모양으로 배치한다."""
    frames = floyd_frames(n)
    seen, x = [], n
    while x not in seen:
        seen.append(x)
        x = step(x)
    tail, ring = seen[: seen.index(x)], seen[seen.index(x) :]
    assert tail == [2] and len(ring) == 8, (tail, ring)
    W, H = CANVAS_W, 400
    cx, cy, R = 375, 205, 112
    pos, out = {"_size": (W, H)}, {}
    for i, v in enumerate(ring):
        th = math.pi + i * math.pi / 4  # 왼쪽에서 시작해 시계 방향
        pos[v] = (cx + R * math.cos(th), cy + R * math.sin(th))
        out[v] = (math.cos(th), math.sin(th))
    out[ring[0]] = (-0.7, -0.7)  # 꼬리 간선과 라벨이 겹치지 않게
    pos[tail[0]] = (cx - R - 175, cy)
    out[tail[0]] = (0, 1)
    edges = [(tail[0], ring[0])] + [(ring[i], ring[(i + 1) % 8]) for i in range(8)]
    meet = frames[-1][0]
    assert step(n) == 4 and meet != 1
    draw = make_draw(
        tail + ring,
        pos,
        out,
        edges,
        [],
        n,
        len(frames) - 1,
        f"만난 값 {meet} ≠ 1: 행복하지 않음",
    )
    return draw, list(enumerate(frames))


def build_happy(n=19):
    """꼬리 4개를 한 줄로, 마지막 1에 자기 반복 화살표."""
    frames = floyd_frames(n)
    seq, x = [], n
    while x not in seq:
        seq.append(x)
        x = step(x)
    assert seq[-1] == 1 and x == 1
    W, H = CANVAS_W, 224
    pos, out = {"_size": (W, H)}, {}
    for i, v in enumerate(seq):
        pos[v] = (42 + i * 110, 125)
        out[v] = (0, 1)
    edges = [(seq[i], seq[i + 1]) for i in range(len(seq) - 1)]
    assert frames[-1][0] == 1
    draw = make_draw(
        seq, pos, out, edges, [1], n, len(frames) - 1, "만난 값 1: 행복한 수"
    )
    return draw, list(enumerate(frames))


def main(out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for name, (draw, frames) in {
        "floyd-unhappy": build_unhappy(),
        "floyd-happy": build_happy(),
    }.items():
        print(name, [f for _, f in frames])
        emit(out_dir, name, draw, frames, static=False)
    print("→", out_dir)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_OUT)
