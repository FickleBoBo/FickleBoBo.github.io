"""
`sync_code.py <포스트.md 또는 폴더>` — 포스트의 코드 블록을 PS 레포 최신 코드로 갱신한다(동작은 SKILL.md).
코드 펜스 안만 바꾸고 프로즈는 건드리지 않는다. 결정론적, LLM 판단 없음.
"""

import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "_shared"))
)
from post_text import read_front_matter
from ps_source import resolve_source_folder
from sync_text import sync_text


def sync_file(path):
    """(갱신한 파일명 리스트, 알림 리스트). 바뀐 게 있을 때만 파일을 다시 쓴다."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    folder = resolve_source_folder(*read_front_matter(text))
    new_text, updated, warnings = sync_text(text, folder)
    if new_text != text:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_text)
    return updated, warnings


def collect_paths(target):
    """포스트 하나면 그 경로, 폴더면 하위 `.md` 전부(정렬)."""
    if not os.path.isdir(target):
        return [target]
    return sorted(
        os.path.join(d, n)
        for d, _, ns in os.walk(target)
        for n in ns
        if n.endswith(".md")
    )


def main():
    if len(sys.argv) != 2:
        sys.exit("사용법: sync_code.py <포스트 .md 또는 폴더>")
    target = sys.argv[1]
    base = target if os.path.isdir(target) else os.path.dirname(target)
    paths = collect_paths(target)

    counts = {"갱신함": 0, "변경 없음": 0, "확인 필요": 0, "에러": 0}
    for path in paths:
        try:
            updated, warnings = sync_file(path)
        except Exception as e:  # 포스트 하나의 실패는 그 포스트만 보고하고 계속한다
            lines, kind = [f"에러: {type(e).__name__}: {e}"], "에러"
        else:
            lines = [f"{n}: 갱신함" for n in updated] + warnings
            kind = "확인 필요" if warnings else "갱신함" if updated else "변경 없음"
        counts[kind] += 1
        for line in lines or ["변경 없음"]:
            print(f"{os.path.relpath(path, base)} — {line}")
    print(
        f"--- 총 {len(paths)}개 중 "
        + ", ".join(f"{k} {v}개" for k, v in counts.items())
        + " ---"
    )
    sys.exit(1 if counts["에러"] else 0)


if __name__ == "__main__":
    main()
