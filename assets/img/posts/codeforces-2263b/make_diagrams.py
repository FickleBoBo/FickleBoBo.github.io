"""Codeforces #2263B Min Matrices 포스트의 구성 도식(정적 SVG)을 다시 만든다.

같은 폴더(`assets/img/posts/codeforces-2263b/`)에 만든다:
  construction-{light,dark}.svg   n = 5, k = 7(m = 3): 최솟값을 맡은 칸의 배치와 서로 다른 최솟값의 개수.

입력 선택: n - m = 2라서 "대각선 m번째 칸의 행 오른쪽"과 "마지막 열 아래"가 각각 두 칸씩 보이고, 겹침 칸도
세 칸이라 세 종류의 칸(겹침·열 최솟값·행 최솟값)이 모두 드러나는 가장 작은 입력이다.

값은 손으로 적지 않는다. 풀이 코드와 같은 구성으로 행렬을 만든 뒤 실제 행·열 최솟값을 계산해
칸의 역할을 정하고, 아래에 적는 최솟값 집합과 서로 다른 값의 개수도 그 계산에서 가져온다.
색은 IMAGE_STYLE.md 역할표대로 겹침=green(꽉 찬 초록), 열 최솟값=purple, 행 최솟값=yellow이고
칸 안 라벨(`행·열`/`열`/`행`)을 같이 쓴다.

사용법:
    python3 make_diagrams.py [출력 디렉토리]   # 기본: 이 스크립트가 있는 폴더
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve()
REPO = HERE.parents[4]  # assets/img/posts/{slug}/ 기준 레포 루트
sys.path.insert(0, str(REPO / ".claude" / "skills" / "_shared" / "image"))  # diagram.py

from diagram import (
    CANVAS_W,
    CELL_H,
    CELL_W,
    FS_CELL,
    LEGEND_ROW,
    ROW,
    caption,
    cell_xy,
    emit,
    grid_bottom,
    header,
    legend,
    rect,
    svg,
    text,
)

DEFAULT_OUT = HERE.parent
LABEL = {"both": "행·열", "col": "열", "row": "행"}


def build_matrix(n, k):
    """풀이 코드(C++)와 같은 구성."""
    m = 2 * n - k
    a = [[0] * n for _ in range(n)]
    num = 1
    for i in range(m):
        a[i][i] = num
        num += 1
    for i in range(m, n):
        a[m - 1][i] = num
        num += 1
    for i in range(m, n):
        a[i][n - 1] = num
        num += 1
    for i in range(n):
        for j in range(n):
            if a[i][j] == 0:
                a[i][j] = num
                num += 1
    return a, m


def minima(a):
    """실제 행·열 최솟값: 칸 집합과 값 목록, 칸별 역할."""
    n = len(a)
    row_cells = {(i, a[i].index(min(a[i]))) for i in range(n)}
    col_cells = set()
    for j in range(n):
        col = [a[i][j] for i in range(n)]
        col_cells.add((col.index(min(col)), j))
    role = {}
    for i in range(n):
        for j in range(n):
            r, c = (i, j) in row_cells, (i, j) in col_cells
            role[(i, j)] = "both" if r and c else "col" if c else "row" if r else ""
    row_vals = sorted(a[i][j] for i, j in row_cells)
    col_vals = sorted(a[i][j] for i, j in col_cells)
    return role, row_vals, col_vals


def style(c, r):
    """역할별 (채움, 윤곽, 윤곽 굵기, 글자색)."""
    if r == "both":
        return c["green"], c["green"], 3, c["on_color"]
    if r == "col":
        return c["purple_t"], c["purple"], 2.5, c["text"]
    if r == "row":
        return c["yellow_t"], c["yellow"], 2.5, c["text"]
    return c["cell"], c["dim"], 1.5, c["muted"]


def make_draw(a, role, row_vals, col_vals, n, k, m):
    legend_y = grid_bottom(n) + ROW
    sum_y = legend_y + LEGEND_ROW + ROW
    H = sum_y + 2 * LEGEND_ROW + 22

    def join(v):
        return ", ".join(map(str, v))

    def draw(c, _frame, solid_bg):
        body = header(c, f"n = {n}, k = {k}  (겹침 m = {m})")
        for i in range(n):
            for j in range(n):
                x, y = cell_xy(i, j, n)
                r = role[(i, j)]
                fill, stroke, sw, tc = style(c, r)
                body += rect(x, y, CELL_W, CELL_H, fill, stroke, sw)
                cx, cy = x + CELL_W / 2, y + CELL_H / 2
                if r:
                    body += text(cx, cy - 9, a[i][j], tc, FS_CELL, weight=700)
                    body += text(cx, cy + 16, LABEL[r], tc, 15, mono=False, weight=600)
                else:
                    body += text(cx, cy, a[i][j], tc, FS_CELL)
        items = [
            ("both", "행과 열의 최솟값을 함께 맡는 칸"),
            ("col", "열의 최솟값만 맡는 칸"),
            ("row", "행의 최솟값만 맡는 칸"),
            ("", "더 큰 수로 채운 칸"),
        ]
        body += legend(
            c,
            [(*style(c, r)[:3], label) for r, label in items],
            legend_y,
            cols=2,
            col_w=262,
        )
        distinct = sorted(set(row_vals) | set(col_vals))
        body += caption(c, sum_y, f"행 최솟값: {join(row_vals)}")
        body += caption(c, sum_y + LEGEND_ROW, f"열 최솟값: {join(col_vals)}")
        body += caption(
            c,
            sum_y + 2 * LEGEND_ROW,
            f"합치면 서로 다른 값이 {len(distinct)}개 = k",
            c["green"],
            700,
        )
        return svg(CANVAS_W, H, body, c, solid_bg)

    return draw


def main(out_dir, n=5, k=7):
    a, m = build_matrix(n, k)
    role, row_vals, col_vals = minima(a)
    # 검증: 순열, 서로 다른 최솟값 k개, 겹침 m칸, 열·행 최솟값만 맡는 칸 n - m칸씩
    assert sorted(v for row in a for v in row) == list(range(1, n * n + 1))
    f = {min(r) for r in a} | {min(a[i][j] for i in range(n)) for j in range(n)}
    assert len(f) == k == len(set(row_vals) | set(col_vals)), (len(f), k)
    cnt = {r: sum(1 for v in role.values() if v == r) for r in ("both", "col", "row")}
    assert cnt == {"both": m, "col": n - m, "row": n - m}, cnt
    for r in a:
        print(r)
    print(
        "겹침",
        sorted(a[i][j] for (i, j), v in role.items() if v == "both"),
        "열",
        sorted(a[i][j] for (i, j), v in role.items() if v == "col"),
        "행",
        sorted(a[i][j] for (i, j), v in role.items() if v == "row"),
        "나머지 최솟값",
        min(a[i][j] for (i, j), v in role.items() if v == ""),
    )
    print("행 최솟값", row_vals, "열 최솟값", col_vals, "서로 다른 값", len(f))
    emit(
        out_dir,
        "construction",
        make_draw(a, role, row_vals, col_vals, n, k, m),
        [None],
        gif=False,
    )
    print("→", out_dir)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_OUT)
