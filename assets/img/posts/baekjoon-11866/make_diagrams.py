"""BaekJoon #11866 요세푸스 문제 0의 큐 시뮬레이션 도식(GIF 2개)을 다시 만든다.

같은 폴더(`assets/img/posts/baekjoon-11866/`)에 만든다:
  josephus-{light,dark}.gif   `7 3`을 라운드(앞의 K-1명을 뒤로 돌리고 K번째를 제거)마다 한 프레임으로 따라간다.

한 프레임에 두 줄을 그린다. 위 줄이 "돌리기 전" 큐, 아래 줄이 "돌린 뒤" 큐이고, 둘 사이의 선이
각 사람이 앞에서 뒤로 어디로 옮겨 가는지 보인다. 뒤로 가는 사람(orange)은 굵은 선, 그대로 앞으로
당겨지는 사람은 흐린 선, 돌린 뒤 맨 앞에 와서 제거되는 사람은 blue 선이다. 다음 프레임의 위 줄은
이 프레임의 아래 줄에서 제거된 사람을 뺀 큐다.

입력 선택 이유: 지문 예제(`7 3`, 결과 <3, 6, 2, 7, 5, 1, 4>)다. 독자가 이미 알고 있는 입력이고
  남은 사람이 K-1명 이하가 되는 마지막 두 라운드(한 바퀴 이상 도는 경우)까지 보여 준다.

값은 손으로 적지 않고 풀이와 같은 순서(앞의 K-1명을 꺼내 뒤에 넣고 맨 앞을 제거)로 실행해 얻는다.
마지막에 독립 구현(리스트에서 인덱스 계산으로 삭제)과 포스트의 Python 코드 블록을 실제로 돌린 결과와 같은지 assert로 대조하고,
돌린 뒤 큐가 슬라이스 공식(앞에서 (K-1) mod 길이만큼 잘라 뒤로 붙임)과 같은지도 assert한다.
색은 IMAGE_STYLE.md 역할표대로 제거할 사람=blue(지금 보는 대상), 뒤로 돌릴 사람=orange(대기·후보).
남은 사람이 K-1명 이하이면 돌리는 사람 전부가 orange이고 그중 제거되는 사람만 blue다.

전환 시간·크기·글자·제목/단계/범례/캡션 위치는 `diagram.py` 공용 틀(IMAGE_STYLE.md)을 따른다.
칸 격자가 아니라 노드(반경 24)로 그린 건 7명을 폭 560에 한 줄로 놓기 위해서다.

사용법:
    python3 make_diagrams.py [출력 디렉토리]   # 기본: 이 스크립트가 있는 폴더

diagram.py(팔레트·헬퍼)를 바꾸면 결과가 달라진다. 다시 만들었다면 GIF를 눈으로 확인한 뒤 커밋한다.
"""

import io
import re
import sys
from collections import deque
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve()
REPO = HERE.parents[4]  # assets/img/posts/{slug}/ 기준 레포 루트
sys.path.insert(0, str(REPO / ".claude" / "skills" / "_shared" / "image"))  # diagram.py

from diagram import (
    CANVAS_W,
    HEADER_H,
    MARGIN,
    ROW,
    caption,
    circle,
    emit,
    header,
    legend,
    line,
    svg,
    text,
)

DEFAULT_OUT = HERE.parent
N, K = 7, 3
PITCH = 66  # 노드 중심 간격
R = 24  # 노드 반경(IMAGE_STYLE.md)
X0 = 120  # 첫 노드 중심 x(왼쪽에 줄 이름을 둔다)
TOP_Y = HEADER_H + 36  # 돌리기 전 줄
BOT_Y = TOP_Y + 92  # 돌린 뒤 줄
LABEL_Y = BOT_Y + R + 18
OUT_Y = LABEL_Y + 36
LEGEND_Y = OUT_Y + ROW + 4
CAPTION_Y = LEGEND_Y + ROW + 6
H = CAPTION_Y + 22


def simulate(n, k):
    """풀이와 같은 순서로 실행하며 라운드마다 돌리기 전·후 큐와 제거된 사람을 모은다."""
    q = deque(range(1, n + 1))
    removed = []
    frames = []
    while q:
        before = list(q)
        moved = []
        for _ in range(k - 1):
            moved.append(q[0])
            q.append(q.popleft())
        after = list(q)
        shift = (k - 1) % len(before)
        assert after == before[shift:] + before[:shift]  # 슬라이스 공식과 같다
        target = q.popleft()
        frames.append(
            dict(
                before=before,
                after=after,
                moving=set(moved),
                target=target,
                done=list(removed),
            )
        )
        removed.append(target)
    frames.append(
        dict(
            before=[],
            after=[],
            moving=set(),
            target=None,
            done=list(removed),
            final=True,
        )
    )
    return frames, removed


def reference(n, k):
    """리스트에서 (인덱스 + K - 1) mod 길이 위치를 삭제하는 독립 구현으로 구한다."""
    people = list(range(1, n + 1))
    out, idx = [], 0
    while people:
        idx = (idx + k - 1) % len(people)
        out.append(people.pop(idx))
    return out


def post_solution_result(n, k):
    """포스트의 Python 코드 블록을 실제로 돌려 출력을 얻는다. 포스트가 없으면 None."""
    for d in ("_drafts", "_posts"):
        for p in (REPO / d).glob("*/*BaekJoon 11866 *.md"):
            code = re.search(r"```python\n(.*?)```", p.read_text(), re.S).group(1)
            stdin, buf = sys.stdin, io.StringIO()
            sys.stdin = io.StringIO(f"{n} {k}\n")
            try:
                with redirect_stdout(buf):
                    exec(code, {})
            finally:
                sys.stdin = stdin
            return buf.getvalue().strip()
    return None


def seq_text(nums, final=False):
    return "<" + ", ".join(map(str, nums)) + (">" if final else "")


def make_caption(frame):
    if frame.get("final"):
        return f"완성: 제거된 순서 {seq_text(frame['done'], True)}가 답이다"
    size = len(frame["before"])
    if K - 1 >= size:
        return f"남은 {size}명뿐이라 한 바퀴 이상 돌아 {frame['target']}번이 맨 앞에 와서 제거된다"
    moved = ", ".join(f"{p}번" for p in frame["before"][: K - 1])
    return f"앞의 {K - 1}명({moved})을 뒤로 보내면 {frame['target']}번이 맨 앞에 와서 제거된다"


def node_style(c, frame, person):
    if person == frame["target"]:
        return c["blue_t"], c["blue"], 3.5
    if person in frame["moving"]:
        return c["orange_t"], c["orange"], 3.5
    return c["tint"], c["ink"], 2.5


def arrow(c, x1, y1, x2, y2, color, sw):
    """선과 끝의 작은 화살촉(채운 삼각형)."""
    import math

    dx, dy = x2 - x1, y2 - y1
    d = math.hypot(dx, dy)
    ux, uy = dx / d, dy / d
    bx, by = x2 - ux * 9, y2 - uy * 9
    px, py = -uy * 4.5, ux * 4.5
    head = (
        f'<path d="M{x2:.1f} {y2:.1f} L{bx + px:.1f} {by + py:.1f} '
        f'L{bx - px:.1f} {by - py:.1f} z" fill="{color}"/>'
    )
    return line(x1, y1, bx, by, color, sw) + head


def make_draw(total):
    def draw(c, frame, solid_bg):
        body = header(c, f"N = {N}, K = {K}", frame_step(frame), total)
        before, after = frame["before"], frame["after"]
        if before:
            body += text(
                MARGIN, TOP_Y, "돌리기 전", c["muted"], 13, anchor="start", mono=False
            )
            body += text(
                MARGIN, BOT_Y, "돌린 뒤", c["muted"], 13, anchor="start", mono=False
            )
            # 선을 먼저 그려 노드 아래에 깔고, 뒤로 가는 선이 위에 오도록 흐린 선 → 굵은 선 순서로 그린다
            order = sorted(
                before,
                key=lambda p: (p in frame["moving"], p == frame["target"]),
            )
            for person in order:
                x1 = X0 + before.index(person) * PITCH
                x2 = X0 + after.index(person) * PITCH
                if person == frame["target"]:
                    color, sw = c["blue"], 3
                elif person in frame["moving"]:
                    color, sw = c["orange"], 3
                else:
                    color, sw = c["dim"], 2
                body += arrow(c, x1, TOP_Y + R + 2, x2, BOT_Y - R - 3, color, sw)
            for row_y, row in ((TOP_Y, before), (BOT_Y, after)):
                for slot, person in enumerate(row):
                    x = X0 + slot * PITCH
                    fill, stroke, sw = node_style(c, frame, person)
                    body += circle(x, row_y, R, fill, stroke, sw)
                    body += text(x, row_y, person, c["text"], 15, weight=700)
            last_x = X0 + (len(after) - 1) * PITCH
            body += text(X0, LABEL_Y, "앞", c["muted"], 15, mono=False)
            if len(after) > 1:
                body += text(last_x, LABEL_Y, "뒤", c["muted"], 15, mono=False)
        else:
            body += text(
                CANVAS_W // 2,
                (TOP_Y + BOT_Y) // 2,
                "큐가 비었다",
                c["muted"],
                17,
                mono=False,
            )
        body += text(
            MARGIN, OUT_Y, "제거된 순서", c["muted"], 15, anchor="start", mono=False
        )
        final = frame.get("final", False)
        body += text(
            MARGIN + 104,
            OUT_Y,
            seq_text(frame["done"], final) if frame["done"] else "",
            c["green"] if final else c["text"],
            17,
            anchor="start",
            weight=700,
        )
        body += legend(
            c,
            [
                (c["orange_t"], c["orange"], 3.5, "뒤로 돌릴 사람"),
                (c["blue_t"], c["blue"], 3.5, "제거할 사람"),
            ],
            LEGEND_Y,
            cols=2,
            col_w=190,
        )
        body += caption(
            c,
            CAPTION_Y,
            make_caption(frame),
            c["green"] if final else None,
            700 if final else 500,
        )
        return svg(CANVAS_W, H, body, c, solid_bg)

    return draw


_steps = {}


def frame_step(frame):
    return _steps[id(frame)]


def main(out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    frames, removed = simulate(N, K)
    assert removed == reference(N, K) == [3, 6, 2, 7, 5, 1, 4]
    post = post_solution_result(N, K)
    expected = "<" + ", ".join(map(str, removed)) + ">"
    assert post is None or post == expected, (post, expected)
    print(
        "입력",
        N,
        K,
        "결과",
        expected,
        "(포스트 코드 대조:",
        "생략" if post is None else "일치",
        ")",
    )
    for i, f in enumerate(frames):
        _steps[id(f)] = i
        print(
            i,
            "전",
            f["before"],
            "후",
            f["after"],
            "돌림",
            sorted(f["moving"]),
            "제거",
            f["target"],
            "지금까지",
            f["done"],
        )
    emit(out_dir, "josephus", make_draw(len(frames) - 1), frames, static=False)
    print("→", out_dir)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_OUT)
