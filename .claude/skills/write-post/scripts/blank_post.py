"""
`blank_post.py <출력 디렉토리> <포스트 .md 경로> [...]` — 이미 채워진 포스트를 백지에서 다시 쓰기 위한
사본을 만든다. 쓰는 쪽이 기존 글에 끌리지 않도록 `{디렉토리}/{slug}.md`에 아이디어 본문, 접근 이름,
블록 설명, 회고 섹션을 빼고, 원본의 아이디어가 채워져 있는지(`채워짐`/`비어 있음`)를 함께 알린다.
front matter·문제 링크·섹션과 풀이 헤딩·코드 블록은 그대로다.
원본은 건드리지 않는다.
"""

import os
import re
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "_shared"))
)
from post_text import classify_fences, read_front_matter
from problem_post import (
    CODE_SECTION_PATTERN,
    IDEA_HEADING,
    RETRO_SECTION_PATTERN,
    idea_is_filled,
)

_APPROACH_NAME_RE = re.compile(r"^(### 풀이(?: \d+)?):[^\[]*?( ?\[)")


def blank_text(text):
    lines = text.split("\n")
    kinds, _ = classify_fences(lines)
    kept = []
    section = None  # "idea" | "code" | "retro" | None(front matter·머리말·그 밖의 섹션)
    for line, kind in zip(lines, kinds):
        if kind != "text":
            if section != "retro":
                kept.append(line)
            continue
        if line.startswith("## "):
            heading = line.rstrip()
            if heading == IDEA_HEADING:
                section = "idea"
            elif re.fullmatch(CODE_SECTION_PATTERN, heading):
                section = "code"
            elif re.fullmatch(RETRO_SECTION_PATTERN, heading):
                section = "retro"
            else:
                section = None
            if section != "retro":
                kept.append(line)
        elif section is None:
            kept.append(line)
        elif section == "code" and line.startswith("### "):
            kept.append(_APPROACH_NAME_RE.sub(r"\1 [", line, count=1))
        elif section != "retro" and line.strip() in ("", "---"):
            kept.append(line)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(kept)).rstrip("\n") + "\n"


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    out_dir = sys.argv[1]
    os.makedirs(out_dir, exist_ok=True)
    failed = 0
    for path in map(os.path.abspath, sys.argv[2:]):
        try:
            with open(path, encoding="utf-8") as f:
                text = f.read()
            _, slug = read_front_matter(text)
        except (OSError, ValueError) as e:
            print(f"에러({path}): {e}")
            failed += 1
            continue
        out_path = os.path.join(out_dir, f"{slug}.md")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(blank_text(text))
        mode = "채워짐" if idea_is_filled(text) else "비어 있음"
        print(f"{mode}: {path} -> {out_path}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
