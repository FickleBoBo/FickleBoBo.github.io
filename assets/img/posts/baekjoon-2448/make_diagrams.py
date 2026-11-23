"""BaekJoon #2448 별 찍기 - 11의 분할 구조 도식(GIF 2개)을 다시 만든다.

같은 폴더(`assets/img/posts/baekjoon-2448/`)에 만든다:
  triangle-{light,dark}.gif   `N = 12`의 삼각형이 크기 6 삼각형 세 개로, 다시 크기 3 삼각형 아홉 개로 나뉘고
                               크기 3에서 별 8개를 직접 찍는 4프레임 흐름.

아이디어의 핵심 성질("크기 N 삼각형 = 크기 N / 2 삼각형 세 개, 위 하나는 열 +N / 2, 아래 둘은 열 +0과 +N, 크기 3이
기저")이 한 프레임에 한 사건씩 보이게 한다: 전체 -> 크기 6 분할(오프셋 표시) -> 크기 3 분할 -> 기저 모양.

입력 선택 이유: `12`다. N = 3 x 2^2라 반으로 나누면 12 -> 6 -> 3으로 기저에 닿고, 분할이 두 번 일어나는 가장 작은
입력이다. 지문 예제(`24`)는 폭 2N = 48칸을 캔버스 폭 560에 넣느라 칸이 11px까지 줄어 별이 뭉개져서 쓰지 않았다.
폭 24칸이면 칸을 22px로 키울 수 있다(격자 기본 92가 아님).

값은 손으로 적지 않는다. 포스트의 재귀(`dfs`)를 그대로 옮겨 별 칸을 얻고, 분할 상자의 (행, 열) 오프셋도 같은
호출 규칙으로 계산한다. 기저 삼각형의 줄별 별 개수(1, 2, 5)와 별 8개, 세 호출의 별 칸 합 = 전체, 만든 격자 = 포스트의
Python 코드 블록을 N = 12로 돌린 출력을 assert로 대조한다.

색은 IMAGE_STYLE.md 역할표대로 쓴다: 별은 옅은 회색 채움과 먹색 윤곽(기본), 마지막 프레임의 기저 삼각형만 지금 보는
대상 blue, 나머지 별은 dim. 전환 시간·크기·글자·제목/단계/캡션 위치는 `diagram.py` 공용 틀을 따른다.

사용법:
    python3 make_diagrams.py [출력 디렉토리]   # 기본: 이 스크립트가 있는 폴더

diagram.py(팔레트·헬퍼)를 바꾸면 결과가 달라진다. 다시 만들었다면 GIF를 눈으로 확인한 뒤 커밋한다.
"""

import io
import re
import sys
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve()
REPO = HERE.parents[4]  # assets/img/posts/{slug}/ 기준 레포 루트
sys.path.insert(0, str(REPO / ".claude" / "skills" / "_shared" / "image"))  # diagram.py

from diagram import HEADER_H, MARGIN, caption, emit, header, rect, svg, text

DEFAULT_OUT = HERE.parent
N = 12
CELL = 22  # 한 칸 크기(폭 2N = 24칸이 폭 560 안에 들어가는 값)
STAR = CELL - 2  # 별 사각형 크기(칸 사이 2px 간격)
X0 = MARGIN
FS_LABEL = 15  # 칸 안 보조 라벨(산세리프 15)
NAMES = ["위", "왼쪽 아래", "오른쪽 아래"]


def stars(sr, sc, n, acc):
    """포스트의 재귀를 그대로 옮겨 별이 놓이는 (행, 열) 칸을 acc에 모은다."""
    if n == 3:
        acc.update(
            {
                (sr, sc + 2),
                (sr + 1, sc + 1),
                (sr + 1, sc + 3),
                (sr + 2, sc),
                (sr + 2, sc + 1),
                (sr + 2, sc + 2),
                (sr + 2, sc + 3),
                (sr + 2, sc + 4),
            }
        )
        return
    stars(sr, sc + n // 2, n // 2, acc)
    stars(sr + n // 2, sc, n // 2, acc)
    stars(sr + n // 2, sc + n, n // 2, acc)


def split_boxes(sr, sc, n, depth, out):
    """같은 호출 규칙으로 depth번 나눈 삼각형의 (행 오프셋, 열 오프셋, 크기)를 out에 모은다."""
    if depth == 0:
        out.append((sr, sc, n))
        return
    h = n // 2
    split_boxes(sr, sc + h, h, depth - 1, out)
    split_boxes(sr + h, sc, h, depth - 1, out)
    split_boxes(sr + h, sc + n, h, depth - 1, out)


def post_solution_lines(n):
    """포스트의 Python 코드 블록을 실제로 돌려 출력 줄을 얻는다. 포스트가 없으면 None."""
    for d in ("_drafts", "_posts"):
        for path in (REPO / d).glob("*/*BaekJoon 2448 *.md"):
            code = re.search(r"```python\n(.*?)```", path.read_text(), re.S).group(1)
            stdin, buf = sys.stdin, io.StringIO()
            sys.stdin = io.StringIO(f"{n}\n")
            try:
                with redirect_stdout(buf):
                    exec(code, {})
            finally:
                sys.stdin = stdin
            return buf.getvalue().split("\n")[:-1]
    return None


def build_frames():
    full = set()
    stars(0, 0, N, full)
    grid = ["".join("*" if (r, c) in full else " " for c in range(2 * N)) for r in range(N)]
    sol = post_solution_lines(N)
    assert sol is None or sol == grid  # 포스트 코드의 출력과 줄 단위로 같다

    half = N // 2
    lvl1, lvl2 = [], []
    split_boxes(0, 0, N, 1, lvl1)
    split_boxes(0, 0, N, 2, lvl2)
    assert lvl1 == [(0, half, half), (half, 0, half), (half, N, half)]  # (+0, +6), (+6, +0), (+6, +12)
    assert len(lvl2) == 9 and all(size == 3 for _, _, size in lvl2)
    union = set()
    for sr, sc, size in lvl2:  # 크기 3 아홉 개의 별 칸 합 = 전체, 서로 겹치지 않는다
        acc = set()
        stars(sr, sc, size, acc)
        assert all(sr <= r < sr + size and sc <= c < sc + 2 * size - 1 for r, c in acc)
        assert not (union & acc)
        union |= acc
    assert union == full
    base = lvl2[0]  # 맨 위 삼각형의 맨 위 크기 3
    base_stars = {(r, c) for r, c in full if base[0] <= r < base[0] + 3 and base[1] <= c < base[1] + 5}
    assert len(base_stars) == 8
    assert [sum(1 for r, _ in base_stars if r == base[0] + k) for k in range(3)] == [1, 2, 5]

    texts = [
        f"크기 {N} 삼각형 하나를 찍는다",
        f"크기 {N}은 크기 {half} 삼각형 세 개로 나뉜다. 괄호는 (행, 열) 오프셋",
        f"크기 {half}도 같은 배치로 크기 3 삼각형 세 개로 나뉜다",
        "크기 3은 더 나누지 않고 별 8개(1 + 2 + 5)를 직접 찍는다",
    ]
    return [
        dict(step=k, caption=texts[k], full=full, lvl1=lvl1, lvl2=lvl2, base=base, base_stars=base_stars)
        for k in range(4)
    ]


def tri_box(c, sr, sc, size, stroke, sw):
    x, y = X0 + sc * CELL, HEADER_H + sr * CELL
    # 삼각형 밑변은 2 * size - 1칸이라 상자 폭을 그만큼만 잡아 옆 상자와 겹치지 않게 한다
    return rect(x - 1.5, y - 1, (2 * size - 1) * CELL + 3, size * CELL + 1, "none", stroke, sw, 4)


def draw(c, frame, solid_bg):
    k = frame["step"]
    out = header(c, f"N = {N}", k, 3)
    for r, col in sorted(frame["full"]):
        x, y = X0 + col * CELL, HEADER_H + r * CELL
        if k == 3 and (r, col) in frame["base_stars"]:
            out += rect(x, y, STAR, STAR, c["blue_t"], c["blue"], 2.5, 3)
        elif k == 3:
            out += rect(x, y, STAR, STAR, c["cell"], c["dim"], 1.5, 3)
        else:
            out += rect(x, y, STAR, STAR, c["tint"], c["ink"], 2, 3)
    if k == 1:
        for (sr, sc, size), name in zip(frame["lvl1"], NAMES):
            out += tri_box(c, sr, sc, size, c["line"], 1.5)
            x, y = X0 + sc * CELL, HEADER_H + sr * CELL
            out += text(x + 8, y + 18, name, c["text"], FS_LABEL, anchor="start", mono=False, weight=700)
            out += text(x + 8, y + 38, f"(+{sr}, +{sc})", c["muted"], FS_LABEL, anchor="start", mono=False)
    if k >= 2:
        for sr, sc, size in frame["lvl2"]:
            is_base = k == 3 and (sr, sc, size) == frame["base"]
            out += tri_box(c, sr, sc, size, c["blue"] if is_base else c["line"], 2.5 if is_base else 1.5)
    cap_y = HEADER_H + N * CELL + 26
    last = k == 3
    out += caption(c, cap_y, frame["caption"], color=c["green"] if last else None, weight=700 if last else 500)
    return svg(560, cap_y + 22, out, c, solid_bg)


def alt_text():
    half = N // 2
    return (
        f"N = {N}의 별 삼각형이 크기 {half} 삼각형 세 개로, 다시 크기 3 삼각형 아홉 개로 나뉘고 "
        "크기 3에서 1줄 1개, 2줄 2개, 3줄 5개의 별 8개를 직접 찍는 4단계 도식"
    )


if __name__ == "__main__":
    out_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_OUT
    frames = build_frames()
    emit(out_dir, "triangle", draw, frames, static=False)
    print("alt:", alt_text())
    print("frames:", len(frames), "stars:", len(frames[0]["full"]))
