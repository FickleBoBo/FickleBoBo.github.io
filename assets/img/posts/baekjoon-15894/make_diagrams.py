"""BaekJoon #15894 수학은 체육과목 입니다의 둘레 투영 도식(정적 SVG)을 다시 만든다.

같은 폴더(`assets/img/posts/baekjoon-15894/`)에 만든다:
  perimeter-{light,dark}.svg   `n = 3` 계단 도형에서 위·왼쪽·오른쪽을 향한 변 조각을 각 방향으로 옮기면
                               겹치거나 비는 곳 없이 길이 n을 채우고, 아랫변까지 더해 4n이 되는 모습.

입력 선택 이유: 지문 예제 2(`3`, 출력 12)다. 예제 1(n = 1)은 정사각형 하나라 옮겨 볼 것이 없다.

모양은 지문 그림대로 위에서부터 1, 2, ..., n개를 가운데에 맞춰 쌓은 것이다. 좌표는 반 칸 단위 정수로
두고 바깥에 드러난 변을 직접 계산하며, 방향별 조각이 길이 n을 정확히 한 번씩 덮는지, 둘레 합이 4n이고
포스트의 Python 코드 블록 출력과 같은지 assert로 대조한다.
색은 IMAGE_STYLE.md 역할표대로 가로 변(열 방향 길이)=purple, 세로 변(행 방향 길이)=yellow다.

사용법:
    python3 make_diagrams.py [출력 디렉토리]   # 기본: 이 스크립트가 있는 폴더

diagram.py(팔레트·헬퍼)를 바꾸면 결과가 달라진다. 다시 만들었다면 SVG를 눈으로 확인한 뒤 커밋한다.
"""

import io
import re
import sys
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve()
REPO = HERE.parents[4]  # assets/img/posts/{slug}/ 기준 레포 루트
sys.path.insert(0, str(REPO / ".claude" / "skills" / "_shared" / "image"))  # diagram.py

from diagram import CANVAS_W, HEADER_H, caption, emit, header, line, rect, svg, text

DEFAULT_OUT = HERE.parent
N = 3
S = 72  # 한 변이 1인 정사각형의 화면 길이
OFF = 46  # 도형과 옮긴 선분 사이 간격
FX = (CANVAS_W - N * S) // 2  # 도형 왼쪽 x
FY = HEADER_H + OFF + 26  # 도형 위 y


def squares(n):
    """(왼쪽 x, 위 y)를 반 칸 단위로 준다. 위에서 r번째 줄(0부터)은 r + 1개이고 가운데에 맞춘다."""
    return [(n - 1 - r + 2 * k, 2 * r) for r in range(n) for k in range(r + 1)]


def exposed(n):
    """바깥에 드러난 변 조각을 방향별로 준다. 값은 (투영 축의 시작 반 칸, 변이 있는 위치)."""
    cells = {(x + dx, y + dy) for x, y in squares(n) for dx in (0, 1) for dy in (0, 1)}
    sides = {"top": [], "bottom": [], "left": [], "right": []}
    for x, y in sorted(cells):
        if (x, y - 1) not in cells:
            sides["top"].append((x, y))
        if (x, y + 1) not in cells:
            sides["bottom"].append((x, y + 1))
        if (x - 1, y) not in cells:
            sides["left"].append((y, x))
        if (x + 1, y) not in cells:
            sides["right"].append((y, x + 1))
    return sides


def post_solution_result(n):
    """포스트의 Python 코드 블록을 실제로 돌린 출력. 포스트가 없으면 None."""
    for d in ("_drafts", "_posts"):
        for path in (REPO / d).glob("*/*BaekJoon 15894 *.md"):
            code = re.search(r"```python\n(.*?)```", path.read_text(), re.S).group(1)
            stdin, buf = sys.stdin, io.StringIO()
            sys.stdin = io.StringIO(f"{n}\n")
            try:
                with redirect_stdout(buf):
                    exec(code, {})
            finally:
                sys.stdin = stdin
            return int(buf.getvalue())
    return None


def build_frame():
    sides = exposed(N)
    lengths = {}
    for name, segs in sides.items():
        starts = sorted(a for a, _ in segs)
        assert starts == list(range(2 * N))  # 길이 N을 겹침·빈틈 없이 한 번씩
        lengths[name] = len(segs) / 2
    total = sum(lengths.values())
    assert total == 4 * N
    sol = post_solution_result(N)
    assert sol is None or sol == total
    return dict(sides=sides, lengths=lengths, total=int(total))


def runs(segs):
    """같은 위치에서 이어지는 반 칸 조각을 (시작, 끝, 위치) 선분 하나로 합친다."""
    out = []
    for a, p in sorted(segs, key=lambda s: (s[1], s[0])):
        if out and out[-1][2] == p and out[-1][1] == a:
            out[-1][1] = a + 1
        else:
            out.append([a, a + 1, p])
    return out


def dashed(x1, y1, x2, y2, color):
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
        f'stroke-width="1.2" stroke-dasharray="3 5"/>'
    )


def draw(c, frame, solid_bg):
    h = S / 2
    out = header(c, f"n = {N}")

    def px(v):
        return FX + v * h

    def py(v):
        return FY + v * h

    for x, y in squares(N):  # 쌓은 정사각형
        out += rect(px(x), py(y), S, S, c["tint"], c["dim"], 1.5, rx=0)

    top_y, left_x, right_x = FY - OFF, FX - OFF, FX + N * S + OFF
    guides = {}  # 같은 좌표의 안내선은 가장 긴 것 하나만 긋는다
    solid = ""
    for name, segs in frame["sides"].items():
        horizontal = name in ("top", "bottom")
        color = c["purple"] if horizontal else c["yellow"]
        for a, b, p in runs(segs):
            if horizontal:
                x1, x2, y = px(a), px(b), py(p)
                solid += line(x1, y, x2, y, color, 4)
                if name == "top":
                    for x in (x1, x2):
                        key = ("v", x)
                        guides[key] = max(guides.get(key, y), y)
                    solid += line(x1 + 6, top_y, x2 - 6, top_y, color, 6)
            else:
                y1, y2, x = py(a), py(b), px(p)
                solid += line(x, y1, x, y2, color, 4)
                tx = left_x if name == "left" else right_x
                for y in (y1, y2):
                    key = (name, y)
                    far = max if name == "left" else min
                    guides[key] = far(guides.get(key, x), x)
                solid += line(tx, y1 + 6, tx, y2 - 6, color, 6)
    for (kind, at), end in guides.items():
        if kind == "v":
            out += dashed(at, top_y, at, end, c["muted"])
        else:
            out += dashed(
                left_x if kind == "left" else right_x, at, end, at, c["muted"]
            )
    out += solid

    n = {k: int(v) for k, v in frame["lengths"].items()}
    mid_x, mid_y, bottom = FX + N * S / 2, FY + N * S / 2, FY + N * S
    out += text(
        mid_x, top_y - 20, f"위 {n['top']}", c["purple"], 15, mono=False, weight=700
    )
    out += text(
        mid_x,
        bottom + 22,
        f"아래 {n['bottom']}",
        c["purple"],
        15,
        mono=False,
        weight=700,
    )
    out += text(
        left_x - 14,
        mid_y,
        f"왼쪽 {n['left']}",
        c["yellow"],
        15,
        anchor="end",
        mono=False,
        weight=700,
    )
    out += text(
        right_x + 14,
        mid_y,
        f"오른쪽 {n['right']}",
        c["yellow"],
        15,
        anchor="start",
        mono=False,
        weight=700,
    )
    cap_y = bottom + 62
    parts = " + ".join(str(n[k]) for k in ("top", "bottom", "left", "right"))
    out += caption(
        c,
        cap_y,
        f"둘레: {parts} = 4 × {N} = {frame['total']}",
        color=c["green"],
        weight=700,
    )
    return svg(CANVAS_W, cap_y + 22, out, c, solid_bg)


def alt_text(frame):
    return (
        f"n = {N}인 계단 도형에서 위·왼쪽·오른쪽을 향한 변 조각을 각 방향으로 옮기면 겹치거나 비는 곳 없이 "
        f"길이 {N}을 채우고, 아랫변까지 더해 둘레가 4 × {N} = {frame['total']}가 되는 도식"
    )


if __name__ == "__main__":
    out_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUT
    frame = build_frame()
    emit(out_dir, "perimeter", draw, [frame], gif=False)
    print("alt:", alt_text(frame))
    print("total:", frame["total"], "lengths:", frame["lengths"])
