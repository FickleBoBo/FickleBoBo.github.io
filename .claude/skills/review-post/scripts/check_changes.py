"""
스냅샷 대비 드래프트 변경이 허용 범위 안인지 검사한다.

사용법: check_changes.py <스냅샷 디렉토리> <드래프트 .md 경로> [...]
(스냅샷은 파일명을 유지한 채 복사해 둔 사본 — `review-post/SKILL.md` 참고.)

허용 범위 = 비어 있던 자리를 채우는 변경. 스냅샷에서 지워지거나 바뀐 줄이
아래에 해당하지 않으면(사람이 쓴 프로즈·코드·채워진 표 값) 위반으로 보고하고
종료 코드 1을 돌려준다. 추가된 줄은 제한하지 않는다 — 채움은 빈 자리에 줄이
늘어나는 변경이라서.

지워지거나 바뀌어도 되는 줄:
- 빈 줄
- 빈 셀이 있는 표 행 (복잡도 빈 셀 채움)
- 이름 없는 `### 풀이 [N] [언어]...` 헤딩 (접근 이름 붙이기)
- `math:`/`mermaid:`/`description:` front matter 줄
- 표 행의 첫 칸만 바뀐 경우 (복잡도 표 "접근" 열 이름 붙이기)
"""

import difflib
import os
import re
import sys

UNNAMED_HEADING_RE = re.compile(r"### 풀이(?: \d+)?(?: ?\[[^\]]+\])*")
FRONT_MATTER_RE = re.compile(r"(math|mermaid|description):")


def cells(line):
    s = line.strip()
    if not (s.startswith("|") and s.endswith("|")):
        return None
    return [c.strip() for c in s[1:-1].split("|")]


def removable(line):
    s = line.strip()
    if not s:
        return True
    row = cells(line)
    if row is not None and "" in row:
        return True
    if UNNAMED_HEADING_RE.fullmatch(s):
        return True
    return bool(FRONT_MATTER_RE.match(s))


def first_cell_only(old, new):
    a, b = cells(old), cells(new)
    return a is not None and b is not None and len(a) == len(b) and a[1:] == b[1:]


def violations(old_lines, new_lines):
    found = []
    matcher = difflib.SequenceMatcher(None, old_lines, new_lines, autojunk=False)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag not in ("replace", "delete"):
            continue
        paired = tag == "replace" and (i2 - i1) == (j2 - j1)
        for k in range(i1, i2):
            if removable(old_lines[k]):
                continue
            if paired and first_cell_only(old_lines[k], new_lines[j1 + k - i1]):
                continue
            found.append((k + 1, old_lines[k]))
    return found


def main():
    if len(sys.argv) < 3:
        print("사용법: check_changes.py <스냅샷 디렉토리> <드래프트 .md 경로> [...]")
        sys.exit(2)
    snap_dir, paths = sys.argv[1], sys.argv[2:]
    bad = 0
    for path in paths:
        snap = os.path.join(snap_dir, os.path.basename(path))
        if not os.path.isfile(snap):
            print(f"{path}: 스냅샷 없음({snap})")
            sys.exit(2)
        with open(snap, encoding="utf-8") as f:
            old_lines = f.read().split("\n")
        with open(path, encoding="utf-8") as f:
            new_lines = f.read().split("\n")
        found = violations(old_lines, new_lines)
        if not found:
            print(f"{path}: 허용 범위 안")
            continue
        bad += 1
        for lineno, text in found:
            print(
                f"{path}:{lineno} — 허용 범위 밖에서 지워지거나 바뀐 줄: {text.strip()[:70]}"
            )
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
