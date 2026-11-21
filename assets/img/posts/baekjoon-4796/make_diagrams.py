"""BaekJoon #4796 캠핑의 주기 배치 도식(정적 SVG 2개)을 다시 만든다.

같은 폴더(`assets/img/posts/baekjoon-4796/`)에 만든다:
  camping-{light,dark}.svg   `L = 5, P = 8, V = 17`에서 휴가 17일을 P일 주기로 나눠, 주기마다 앞 L일만
                              쓸 수 있고 마지막에 남은 V mod P일이 min(V mod P, L)일만큼 채워지는 모습.

아이디어의 핵심 성질("어느 연속한 P일에도 쓸 수 있는 날이 정확히 L일")이 한 줄에 한 주기씩 놓여
줄마다 5일로 같다는 것이 보이게 하고, 마지막 줄(남은 날)만 짧아서 min이 걸리는 자리를 보여 준다.

입력 선택 이유: 지문 예제 2(`5 8 17`, 출력 11)다. 독자가 이미 아는 입력이고, 완전한 주기 2번과
남은 1일이 모두 있어 몫 항과 나머지 항(min)이 한 그림에 나온다. 남은 1일이 L보다 작아 min이 나머지를
그대로 고르는 경우다(남은 날이 L 이상이면 L로 잘리는 경우는 본문 식이 다룬다).

값은 손으로 적지 않는다. 날짜별로 "주기 안 위치가 L 미만이면 쓸 수 있다"를 직접 세어 얻고, 독립 구현(휴가
시작 위치를 모두 시도하는 브루트포스)과 포스트의 Python 코드 블록을 실제로 돌린 결과와 같은지 assert로 대조한다.
색은 IMAGE_STYLE.md 역할표대로 쓸 수 있는 날=green(확정·정답), 쓸 수 없는 날=dim(제외·미사용)이다.

전환 시간·크기·글자·제목/캡션 위치는 `diagram.py` 공용 틀(IMAGE_STYLE.md)을 따른다.
칸 폭을 격자 기본(92)이 아니라 46으로 줄인 건 한 줄에 P = 8칸을 폭 560 안에 놓기 위해서다.

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
L, P, V = 5, 8, 17
CW, CH, GAP = 46, 40, 6  # 칸 폭·높이·간격(한 줄에 P칸이 폭 560 안에 들어가는 값)
X0 = MARGIN  # 첫 칸 왼쪽 x
ROW_GAP = 8  # 줄 사이 간격


def usable_days(l, p, v):
    """날짜(1부터)별로 주기 안 위치가 L 미만이면 쓸 수 있다고 직접 센다."""
    return [(d, (d - 1) % p < l) for d in range(1, v + 1)]


def reference(l, p, v):
    """독립 구현: 휴가 시작 위치를 모두 시도해 쓸 수 있는 날의 최댓값을 구한다."""
    best = 0
    for start in range(p):
        best = max(best, sum(1 for d in range(v) if (d + start) % p < l))
    return best


def post_solution_result(l, p, v):
    """포스트의 Python 코드 블록을 실제로 돌려 `Case 1: N` 의 N을 얻는다. 포스트가 없으면 None."""
    for d in ("_drafts", "_posts"):
        for path in (REPO / d).glob("*/*BaekJoon 4796 *.md"):
            code = re.search(r"```python\n(.*?)```", path.read_text(), re.S).group(1)
            stdin, buf = sys.stdin, io.StringIO()
            sys.stdin = io.StringIO(f"{l} {p} {v}\n0 0 0\n")
            try:
                with redirect_stdout(buf):
                    exec(code, {})
            finally:
                sys.stdin = stdin
            return int(buf.getvalue().strip().split(": ")[1])
    return None


def build_frame():
    days = usable_days(L, P, V)
    rows = [days[i : i + P] for i in range(0, len(days), P)]
    per_row = [sum(1 for _, ok in r if ok) for r in rows]
    total = sum(per_row)
    full, rem = divmod(V, P)
    formula = full * L + min(rem, L)
    assert total == formula == reference(L, P, V)  # 세어 얻은 값 = 공식 = 브루트포스
    sol = post_solution_result(L, P, V)
    assert sol is None or sol == total  # 포스트 코드의 출력과 같다
    assert per_row[:full] == [L] * full  # 완전한 주기는 줄마다 정확히 L일
    assert per_row[full] == min(rem, L)  # 마지막 줄은 min(V mod P, L)일
    return dict(rows=rows, per_row=per_row, total=total, full=full, rem=rem)


def draw(c, frame, solid_bg):
    rows, per_row = frame["rows"], frame["per_row"]
    out = header(c, f"L = {L}, P = {P}, V = {V}")
    right_x = X0 + P * (CW + GAP) + 6  # 줄 오른쪽 일수 라벨 시작 x
    for i, row in enumerate(rows):
        y = HEADER_H + i * (CH + ROW_GAP)
        for j, (day, ok) in enumerate(row):
            x = X0 + j * (CW + GAP)
            if ok:
                out += rect(x, y, CW, CH, c["green_t"], c["green"], 2.5)
                out += text(x + CW / 2, y + CH / 2, day, c["green"], 15, weight=700)
            else:
                out += rect(x, y, CW, CH, c["cell"], c["dim"], 1.5)
                out += text(x + CW / 2, y + CH / 2, day, c["muted"], 15)
        label = f"{per_row[i]}일"
        out += text(
            right_x,
            y + CH / 2,
            label,
            c["green"] if per_row[i] else c["muted"],
            15,
            anchor="start",
            mono=False,
            weight=700,
        )
    bottom = HEADER_H + len(rows) * CH + (len(rows) - 1) * ROW_GAP
    legend_y = bottom + ROW
    out += legend(
        c,
        [
            (c["green_t"], c["green"], 2.5, "쓸 수 있는 날"),
            (c["cell"], c["dim"], 1.5, "쓸 수 없는 날"),
        ],
        legend_y,
        cols=2,
        col_w=170,
    )
    cap1_y = legend_y + LEGEND_ROW + 6
    cap2_y = cap1_y + 28
    out += caption(
        c,
        cap1_y,
        f"{P}일마다 앞 {L}일만 쓸 수 있고, 남은 {frame['rem']}일은 {L}일 이내라 모두 쓴다",
    )
    parts = " + ".join(str(n) for n in per_row)
    out += caption(
        c,
        cap2_y,
        f"답: {parts} = {frame['total']}일",
        color=c["green"],
        weight=700,
    )
    return svg(560, cap2_y + 22, out, c, solid_bg)


def alt_text(frame):
    parts = " + ".join(str(n) for n in frame["per_row"])
    return (
        f"L = {L}, P = {P}, V = {V}에서 휴가 {V}일을 {P}일씩 나눠 줄마다 앞 {L}일만 쓸 수 있는 날로 "
        f"표시하고 남은 {frame['rem']}일을 더해 {parts} = {frame['total']}일을 얻는 도식"
    )


if __name__ == "__main__":
    out_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUT
    frame = build_frame()
    emit(out_dir, "camping", draw, [frame], gif=False)
    print("alt:", alt_text(frame))
    print("total:", frame["total"], "per_row:", frame["per_row"])
