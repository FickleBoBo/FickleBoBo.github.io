"""LeetCode #73 Set Matrix Zeroes 풀이 2(첫 행·열 재사용)의 진행 도식(GIF 2개)을 다시 만든다.

같은 폴더(`assets/img/posts/leetcode-73/`)에 만든다:
  first-rowcol-{light,dark}.gif   4×5 행렬을 풀이 2의 열한 단계로 따라간다.

입력 선택 이유: 지문 예제는 첫 행·열 재사용의 요점을 다 보여 주지 못해 직접 골랐다.
  [[1,1,1,0,1],
   [1,0,1,1,1],
   [1,1,1,1,1],
   [1,1,0,1,1]]
  - 첫 행의 (0,3)에 원래 0이 있다 → 첫 행에 0이 있었다는 사실을 먼저 기억해야 하는 이유.
  - 안쪽 칸 (1,1)·(3,2) 두 곳의 0이 서로 다른 행·열에 표시를 남긴다.
  - 첫 열에는 0이 없다 → 마지막에 첫 열은 그대로, 첫 행만 전체가 0이 된다.

값은 손으로 적지 않고 풀이 2와 같은 순서로 실행해 얻는다. 마지막에 독립 구현과 포스트의
Python 코드 블록(풀이 2)을 실제로 돌린 결과와 같은지 assert로 대조한다.
색은 IMAGE_STYLE.md 역할표대로 읽는 칸=blue, 표시 칸=orange, 0이 된 칸=green.
표시를 끝낸 뒤 첫 행·첫 열을 훑으며 0을 발견하면 그 열·행을 0으로 바꾸는 순서로 그린다
(포스트 코드는 안쪽 칸마다 표시를 확인하지만 같은 결과다. 무작위 입력으로 같음을 확인했다).
정보를 줄이려고 행·열 번호와 원래 있던 0의 별도 표시는 두지 않았다.

전환 시간: 프레임마다 FRAME_MS, 마지막 프레임 LAST_MS(IMAGE_STYLE.md 기본 1초·2.2초보다 느리게).
`diagram.emit`은 마지막 프레임 시간을 못 바꾸므로 `raster`·`save_gif`를 직접 쓴다.

사용법:
    python3 make_diagrams.py [출력 디렉토리]   # 기본: 이 스크립트가 있는 폴더

diagram.py(팔레트·헬퍼)를 바꾸면 결과가 달라진다. 다시 만들었다면 GIF를 눈으로 확인한 뒤 커밋한다.
"""

import copy
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
REPO = HERE.parents[4]  # assets/img/posts/{slug}/ 기준 레포 루트
sys.path.insert(0, str(REPO / ".claude" / "skills" / "_shared" / "image"))  # diagram.py

from diagram import THEMES, raster, rect, save_gif, svg, text

DEFAULT_OUT = HERE.parent
MATRIX = [
    [1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1],
    [1, 1, 1, 1, 1],
    [1, 1, 0, 1, 1],
]
FRAME_MS, LAST_MS = 2000, 3500
CELL_W, CELL_H, GAP = 92, 60, 8
X0, Y0 = 34, 52
W = 2 * X0 + 5 * CELL_W + 4 * GAP
GRID_BOTTOM = Y0 + 4 * CELL_H + 3 * GAP
FLAG_Y = GRID_BOTTOM + 36
LEGEND_Y = FLAG_Y + 36
CAPTION_Y = LEGEND_Y + 40
H = CAPTION_Y + 22


def solve_with_snapshots(matrix):
    """풀이 2와 같은 순서로 실행하며 단계마다 (격자, 역할 표시)를 모은다."""
    m = copy.deepcopy(matrix)
    R, C = len(m), len(m[0])
    assert (
        m[0][0] != 0
    )  # 모서리 칸은 첫 행·열 양쪽 표시를 겸해 도식이 복잡해지므로 피한다
    first_row_has_0 = any(m[0][j] == 0 for j in range(C))
    first_col_has_0 = any(m[i][0] == 0 for i in range(R))

    def markers(g):  # 첫 행·열(모서리 제외)의 0 칸이 표시로 쓰인다
        return {(0, j) for j in range(1, C) if g[0][j] == 0} | {
            (i, 0) for i in range(1, R) if g[i][0] == 0
        }

    frames = []

    def snap(**kw):
        base = dict(
            read=set(), mark=set(), new=set(), fr=None, fc=None, outline=None, note=None
        )
        base.update(kw, grid=copy.deepcopy(m), step=len(frames))
        frames.append(base)

    snap(caption="처음 행렬")

    first_zero_cells = {(0, j) for j in range(C) if m[0][j] == 0} | {
        (i, 0) for i in range(R) if m[i][0] == 0
    }
    snap(
        read=first_zero_cells,
        fr=first_row_has_0,
        fc=first_col_has_0,
        caption="첫 행·첫 열에 0이 있는지 먼저 기억한다",
    )

    # 안쪽 칸을 순서대로 훑으며 0을 발견할 때마다 한 프레임
    found = 0
    for i in range(1, R):
        for j in range(1, C):
            if m[i][j] == 0:
                m[i][0] = 0
                m[0][j] = 0
                found += 1
                snap(
                    read={(i, j)},
                    mark=markers(m),
                    fr=first_row_has_0,
                    fc=first_col_has_0,
                    caption="안쪽 칸을 훑다 0을 발견해 첫 열·첫 행에 표시한다"
                    if found == 1
                    else "또 0을 발견해 같은 방식으로 표시한다",
                )

    # 표시가 끝나면 첫 행을 훑고, 0을 발견하면 그 열의 안쪽 칸을 전부 0으로 바꾼다
    new = set()
    found = 0
    for j in range(1, C):
        if m[0][j] == 0:
            col_new = {(i, j) for i in range(1, R) if m[i][j] != 0}
            assert (
                col_new
            )  # 이 입력은 표시된 열마다 바뀌는 칸이 있어 열마다 한 프레임이 된다
            for i, _ in col_new:
                m[i][j] = 0
            new |= col_new
            found += 1
            snap(
                read={(0, j)},
                mark=markers(m),
                new=set(new),
                fr=first_row_has_0,
                fc=first_col_has_0,
                outline=("row", 0),
                caption="첫 행을 훑다 0을 발견해 그 열의 안쪽 칸을 모두 0으로 바꾼다"
                if found == 1
                else "또 0을 발견해 그 열의 안쪽 칸을 모두 0으로 바꾼다",
            )

    # 이어서 첫 열을 훑고, 0을 발견하면 그 행의 안쪽 칸을 전부 0으로 바꾼다
    found = 0
    for i in range(1, R):
        if m[i][0] == 0:
            row_new = {(i, j) for j in range(1, C) if m[i][j] != 0}
            assert row_new  # 열 때와 같은 이유로 행마다 한 프레임이 된다
            for _, j in row_new:
                m[i][j] = 0
            new |= row_new
            found += 1
            snap(
                read={(i, 0)},
                mark=markers(m),
                new=set(new),
                fr=first_row_has_0,
                fc=first_col_has_0,
                outline=("col", 0),
                caption="이어서 첫 열을 훑다 0을 발견해 그 행의 안쪽 칸을 모두 0으로 바꾼다"
                if found == 1
                else "또 0을 발견해 그 행의 안쪽 칸을 모두 0으로 바꾼다",
            )

    # 마지막에 기억한 값대로 첫 열, 첫 행 순서로 처리한다. 판정은 기억한 값 옆에 보인다
    before = copy.deepcopy(m)
    if first_col_has_0:
        for i in range(R):
            m[i][0] = 0
    new |= {(i, 0) for i in range(R) if m[i][0] == 0 and before[i][0] != 0}
    snap(
        mark=markers(before),
        new=set(new),
        fr=first_row_has_0,
        fc=first_col_has_0,
        outline=("col", 0),
        note="fc",
        caption="기억한 값 확인: 첫 열은 원래 0이 있었으니 전부 0으로 바꾼다"
        if first_col_has_0
        else "기억한 값 확인: 첫 열은 원래 0이 없었으니 그대로 둔다",
    )
    before = copy.deepcopy(m)
    if first_row_has_0:
        for j in range(C):
            m[0][j] = 0
    new |= {(0, j) for j in range(C) if m[0][j] == 0 and before[0][j] != 0}
    snap(
        mark=markers(before),
        new=set(new),
        fr=first_row_has_0,
        fc=first_col_has_0,
        outline=("row", 0),
        note="fr",
        caption="기억한 값 확인: 첫 행은 원래 0이 있었으니 전부 0으로 바꾼다"
        if first_row_has_0
        else "기억한 값 확인: 첫 행은 원래 0이 없었으니 그대로 둔다",
    )
    snap(
        final=True,
        fr=first_row_has_0,
        fc=first_col_has_0,
        caption="완성: 0이 있던 행과 열이 모두 0이 되었다",
    )
    return frames, m


def reference(matrix):
    R, C = len(matrix), len(matrix[0])
    rows = {i for i in range(R) for j in range(C) if matrix[i][j] == 0}
    cols = {j for i in range(R) for j in range(C) if matrix[i][j] == 0}
    return [
        [0 if (i in rows or j in cols) else matrix[i][j] for j in range(C)]
        for i in range(R)
    ]


def post_solution_result(matrix):
    """포스트의 Python 코드 블록(풀이 2)을 실제로 돌려 결과를 얻는다. 포스트가 없으면 None."""
    for d in ("_drafts", "_posts"):
        for p in (REPO / d).glob("*/*LeetCode 73 Set Matrix Zeroes.md"):
            sec = re.split(r"^### 풀이 2.*$", p.read_text(), flags=re.M)[1]
            code = re.search(r"```python\n(.*?)```", sec, re.S).group(1)
            ns = {}
            exec(code, ns)
            m = copy.deepcopy(matrix)
            ns["Solution"]().setZeroes(m)
            return m
    return None


def cell_xy(i, j):
    return X0 + j * (CELL_W + GAP), Y0 + i * (CELL_H + GAP)


def cell_style(c, frame, i, j):
    pos = (i, j)
    if pos in frame["read"]:
        return c["blue_t"], c["blue"], 3
    if pos in frame["mark"]:
        return c["orange_t"], c["orange"], 3
    if pos in frame["new"]:
        return c["green_t"], c["green"], 3
    if frame.get("final") and frame["grid"][i][j] == 0:
        return c["green_t"], c["green"], 3
    return c["cell"], c["line"], 1.5


def make_draw(total):
    R, C = len(MATRIX), len(MATRIX[0])

    def draw(c, frame, solid_bg):
        body = text(
            16,
            24,
            f"{frame['step']} / {total}단계" if frame["step"] else "시작",
            c["text"],
            17,
            anchor="start",
            mono=False,
            weight=700,
        )
        for i in range(R):
            for j in range(C):
                x, y = cell_xy(i, j)
                fill, stroke, sw = cell_style(c, frame, i, j)
                body += rect(x, y, CELL_W, CELL_H, fill, stroke, sw)
                v = frame["grid"][i][j]
                body += text(
                    x + CELL_W / 2,
                    y + CELL_H / 2,
                    v,
                    c["text"],
                    24,
                    weight=700 if v == 0 else 500,
                )
        if frame["outline"]:  # 지금 훑거나 처리하는 행·열을 윤곽선으로 보인다
            kind, k = frame["outline"]
            gw = C * CELL_W + (C - 1) * GAP
            gh = R * CELL_H + (R - 1) * GAP
            if kind == "row":
                _, y = cell_xy(k, 0)
                body += rect(
                    X0 - 7, y - 7, gw + 14, CELL_H + 14, "none", c["ink"], 2.5, 12
                )
            else:
                x, _ = cell_xy(0, k)
                body += rect(
                    x - 7, Y0 - 7, CELL_W + 14, gh + 14, "none", c["ink"], 2.5, 12
                )
        # 기억한 값(첫 행·열에 원래 0이 있었는지). 기억하기 전 프레임에는 그리지 않는다
        flags = [
            ("fr", "첫 행에 0", frame["fr"], X0),
            ("fc", "첫 열에 0", frame["fc"], X0 + 290),
        ]
        for key, label, flag, x in flags:
            if flag is None:
                continue
            body += text(x, FLAG_Y, label, c["muted"], 15, anchor="start", mono=False)
            body += text(
                x + 92,
                FLAG_Y,
                "True" if flag else "False",
                c["blue"] if flag else c["muted"],
                17,
                anchor="start",
                weight=700,
            )
            if frame["note"] == key:  # 마지막 처리 단계: 기억한 값에 따른 판정
                body += text(
                    x + 152,
                    FLAG_Y,
                    "→ 전부 0으로" if flag else "→ 그대로",
                    c["green"] if flag else c["muted"],
                    15,
                    anchor="start",
                    mono=False,
                    weight=700,
                )
        # 범례
        legend = [
            (c["blue_t"], c["blue"], 3, "읽는 칸"),
            (c["orange_t"], c["orange"], 3, "표시 칸"),
            (c["green_t"], c["green"], 3, "0이 된 칸"),
        ]
        for k, (fill, stroke, sw, label) in enumerate(legend):
            x = X0 + k * 150
            body += rect(x, LEGEND_Y - 9, 18, 18, fill, stroke, sw, rx=3)
            body += text(
                x + 28, LEGEND_Y, label, c["text"], 15, anchor="start", mono=False
            )
        body += text(
            16,
            CAPTION_Y,
            frame["caption"],
            c["text"],
            16,
            anchor="start",
            mono=False,
        )
        return svg(W, H, body, c, solid_bg)

    return draw


def main(out_dir):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    frames, final = solve_with_snapshots(MATRIX)
    assert final == reference(MATRIX)
    post = post_solution_result(MATRIX)
    assert post is None or post == final, (post, final)
    print("입력", MATRIX)
    print("결과", final, "(포스트 코드 대조:", "생략" if post is None else "일치", ")")
    for f in frames:
        print(
            f["step"],
            f["grid"],
            "fr",
            f["fr"],
            "fc",
            f["fc"],
            "read",
            sorted(f["read"]),
            "mark",
            sorted(f["mark"]),
            "new",
            sorted(f["new"]),
        )
    draw = make_draw(len(frames) - 1)
    for mode, c in THEMES.items():
        images = [raster(draw(c, f, True)) for f in frames]
        save_gif(
            images,
            out_dir / f"first-rowcol-{mode}.gif",
            ms=FRAME_MS,
            last_ms=LAST_MS,
        )
    print("→", out_dir)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_OUT)
