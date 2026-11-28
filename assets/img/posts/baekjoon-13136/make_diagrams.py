"""BaekJoon #13136 Do Not Touch Anything의 구역 분할·대표 좌석 도식(정적 SVG)을 다시 만든다.

같은 폴더(`assets/img/posts/baekjoon-13136/`)에 만든다:
  cctv-{light,dark}.svg   `R = 7, C = 9, N = 3`에서 N칸씩 끊은 9개 구역(이만큼이면 충분)과 1행·1열부터
                          N칸 간격으로 고른 좌석 9개(한 대가 둘을 함께 못 찍어 이만큼은 필요)를 겹쳐 보인다.

입력 선택 이유: 지문 예제(`7 9 3`, 출력 9)다. 행이 N으로 나누어떨어지지 않아 잘린 구역이 생기는 경우까지
한 그림에 나온다. 파란 점선은 구역과 어긋난 자리에 놓은 CCTV 한 대의 예이며, 그래도 대표 좌석은 하나만 든다(어느 위치든 많아야 하나다).

값은 손으로 적지 않는다. 구역이 모든 좌석을 한 번씩 덮는지, 구역마다 대표 좌석이 하나인지, 가능한 모든
위치의 N×N 창이 대표 좌석을 하나보다 많이 담지 못하는지, 개수가 포스트의 Python 코드 블록 출력과 같은지
assert로 대조한다.
색은 IMAGE_STYLE.md 역할표대로 대표 좌석=green(조건을 만족한 칸), 예로 놓은 CCTV=blue(지금 보는 대상)다.

칸 크기를 격자 기본(92)이 아니라 40으로 줄인 건 9열을 폭 560 안에 놓기 위해서다.

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

from diagram import (
    CANVAS_W,
    FS_LEGEND,
    HEADER_H,
    LEGEND_ROW,
    MARGIN,
    ROW,
    caption,
    emit,
    header,
    legend,
    rect,
    svg,
    text,
)

DEFAULT_OUT = HERE.parent
R, C, N = 7, 9, 3
CS, GAP = 40, 6  # 칸 크기·간격
X0 = (CANVAS_W - (C * CS + (C - 1) * GAP)) // 2  # 격자 왼쪽 x
Y0 = HEADER_H + 22  # 격자 위 y(열 번호 자리를 남긴다)
SAMPLE = (3, 3)  # 예로 놓는 CCTV의 왼쪽 위 좌석(1부터)


def post_solution_result(r, c, n):
    """포스트의 Python 코드 블록을 실제로 돌린 출력. 포스트가 없으면 None."""
    for d in ("_drafts", "_posts"):
        for path in (REPO / d).glob("*/*BaekJoon 13136 *.md"):
            code = re.search(r"```python\n(.*?)```", path.read_text(), re.DOTALL)
            stdin, buf = sys.stdin, io.StringIO()
            sys.stdin = io.StringIO(f"{r} {c} {n}\n")
            try:
                with redirect_stdout(buf):
                    exec(code.group(1), {})
            finally:
                sys.stdin = stdin
            return int(buf.getvalue())
    return None


def window(top, left, n):
    return {(top + i, left + j) for i in range(n) for j in range(n)}


def build_frame():
    seats = {(i, j) for i in range(1, R + 1) for j in range(1, C + 1)}
    blocks = [
        window(i, j, N) & seats for i in range(1, R + 1, N) for j in range(1, C + 1, N)
    ]
    reps = {(i, j) for i in range(1, R + 1, N) for j in range(1, C + 1, N)}
    assert set().union(*blocks) == seats  # 구역이 모든 좌석을 덮는다
    assert sum(len(b) for b in blocks) == len(seats)  # 겹치지 않는다
    assert all(len(b & reps) == 1 for b in blocks)
    # 격자 밖으로 걸치는 위치까지 모든 N×N 창은 대표 좌석을 최대 하나만 담는다
    assert all(
        len(window(i, j, N) & reps) <= 1
        for i in range(2 - N, R + 1)
        for j in range(2 - N, C + 1)
    )
    total = len(blocks)
    assert total == len(reps) == ((R + N - 1) // N) * ((C + N - 1) // N)
    sol = post_solution_result(R, C, N)
    assert sol is None or sol == total
    assert len(window(*SAMPLE, N) & reps) == 1
    return {"blocks": blocks, "reps": reps, "total": total}


def box(seats):
    """좌석 묶음을 감싸는 화면 사각형 (x, y, w, h)."""
    rows = [i for i, _ in seats]
    cols = [j for _, j in seats]
    x = X0 + (min(cols) - 1) * (CS + GAP)
    y = Y0 + (min(rows) - 1) * (CS + GAP)
    w = (max(cols) - min(cols) + 1) * (CS + GAP) - GAP
    h = (max(rows) - min(rows) + 1) * (CS + GAP) - GAP
    return x, y, w, h


def draw(c, frame, solid_bg):
    out = header(c, f"R = {R}, C = {C}, N = {N}")
    for j in range(1, C + 1):
        x = X0 + (j - 1) * (CS + GAP) + CS / 2
        out += text(x, Y0 - 14, j, c["muted"], 13)
    for i in range(1, R + 1):
        y = Y0 + (i - 1) * (CS + GAP) + CS / 2
        out += text(X0 - 16, y, i, c["muted"], 13)
        for j in range(1, C + 1):
            x = X0 + (j - 1) * (CS + GAP)
            yy = Y0 + (i - 1) * (CS + GAP)
            if (i, j) in frame["reps"]:
                out += rect(x, yy, CS, CS, c["green_t"], c["green"], 2.5, rx=6)
            else:
                out += rect(x, yy, CS, CS, c["cell"], c["dim"], 1.5, rx=6)
    for k, block in enumerate(frame["blocks"], 1):  # 구역 둘레와 번호
        x, y, w, h = box(block)
        out += rect(x - 3, y - 3, w + 6, h + 6, "none", c["ink"], 2, rx=3)
        rep = min(block & frame["reps"])
        rx, ry, _, _ = box({rep})
        out += text(rx + CS / 2, ry + CS / 2, k, c["green"], 15, weight=700)
    x, y, w, h = box(window(*SAMPLE, N))
    out += (
        f'<rect x="{x - 1}" y="{y - 1}" width="{w + 2}" height="{h + 2}" rx="7" '
        f'fill="none" stroke="{c["blue"]}" stroke-width="3" stroke-dasharray="8 5"/>'
    )

    bottom = Y0 + R * (CS + GAP) - GAP
    legend_y = bottom + ROW
    out += legend(
        c,
        [
            (c["cell"], c["ink"], 2, "구역(한 대)"),
            (c["green_t"], c["green"], 2.5, f"{N}칸 간격 좌석"),
        ],
        legend_y,
    )
    # 임의 위치의 한 대는 그림과 같은 점선 상자라 legend()를 쓰지 않고 셋째 열에 직접 그린다
    lx = MARGIN + 2 * 170
    out += (
        f'<rect x="{lx}" y="{legend_y - 9}" width="18" height="18" rx="4" '
        f'fill="none" stroke="{c["blue"]}" stroke-width="2.5" stroke-dasharray="5 3"/>'
    )
    out += text(
        lx + 26,
        legend_y,
        "임의 위치의 한 대",
        c["text"],
        FS_LEGEND,
        anchor="start",
        mono=False,
    )
    cap1_y = legend_y + LEGEND_ROW + 6
    cap2_y = cap1_y + 28
    total = frame["total"]
    out += caption(
        c,
        cap1_y,
        "구역마다 한 대면 모두 덮이고, 한 대에 드는 초록 좌석은 많아야 하나다",
    )
    out += caption(
        c,
        cap2_y,
        f"답: ⌈{R} / {N}⌉ × ⌈{C} / {N}⌉ = {total}대",
        color=c["green"],
        weight=700,
    )
    return svg(CANVAS_W, cap2_y + 22, out, c, solid_bg)


def alt_text(frame):
    total = frame["total"]
    return (
        f"R = {R}, C = {C}, N = {N}의 좌석을 {total}개 구역으로 나누고, 1행·1열부터 {N}칸 간격인 좌석 "
        f"{total}개는 어디에 놓은 CCTV든 많아야 하나만 담아 답이 {total}대임을 보이는 도식"
    )


if __name__ == "__main__":
    out_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUT
    frame = build_frame()
    emit(out_dir, "cctv", draw, [frame], gif=False)
    print("alt:", alt_text(frame))
    print("total:", frame["total"], "reps:", sorted(frame["reps"]))
