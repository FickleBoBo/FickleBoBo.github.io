"""
`sync_code.py <포스트.md 또는 폴더>` — 포스트의 코드 블록을 PS 레포 최신 코드로 갱신한다(동작은 SKILL.md).
코드 펜스 안만 바꾸고 프로즈는 건드리지 않는다. 결정론적, LLM 판단 없음.
"""

import os
import re
import sys

_SKILLS_DIR = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path.insert(0, os.path.abspath(os.path.join(_SKILLS_DIR, "ps", "scripts")))
sys.path.insert(0, os.path.abspath(os.path.join(_SKILLS_DIR, "_shared")))
from blog_common import read_front_matter, resolve_source_folder, section_span
from clean_code import clean_code
from ps_source import LANG_OF_FENCE, find_source_files, group_by_approach

APPROACH_HEADING_RE = re.compile(r"^### 풀이(?: (\d+))?", re.MULTILINE)
# 줄 시작에 고정해 빈 코드 블록이 뒤 블록을 삼키지 않게 한다. 본문은 끝 줄바꿈까지 포함.
FENCE_RE = re.compile(r"^```(\S+)\n(.*?)^```[ \t]*$", re.DOTALL | re.MULTILINE)
# 아이디어 섹션의 설명용 펜스는 건드리지 않는다. 번호는 신(`## 2.`)·구(`## 3.`) 모두 받는다.
CODE_SECTION_HEADING = r"## \d+\. (?:코드|쿼리)"


def approach_at(headings, pos):
    """pos가 속한 `### 풀이 N` 구간의 N. 첫 풀이 헤딩 앞이면 None."""
    num = None
    for start, n in headings:
        if start > pos:
            break
        num = n
    return num


def sync_text(text, folder):
    """(새 본문, 갱신한 파일명 리스트, 알림 리스트). 접근법 구간 안의 언어별 첫 펜스를 같은 번호의 소스로 교체."""
    span = section_span(text, CODE_SECTION_HEADING)
    if not span:
        return text, [], ["코드 섹션(`## N. 코드`/`## N. 쿼리`)을 못 찾음"]
    start, end = span
    sources = group_by_approach(find_source_files(folder))
    body = text[start:end]
    headings = [
        (m.start(), int(m.group(1) or 1)) for m in APPROACH_HEADING_RE.finditer(body)
    ]
    seen = set()
    updated = []
    warnings = []

    def replace(m):
        lang = LANG_OF_FENCE.get(m.group(1))
        num = approach_at(headings, m.start())
        if lang is None or num is None or (num, lang) in seen:
            # 소스 언어가 아닌 펜스(```bash 등)·풀이 구간 밖·같은 구간의 둘째 펜스는 대상 아님
            return m.group(0)
        seen.add((num, lang))
        fname = sources.get(num, {}).get(lang)
        if fname is None:
            warnings.append(f"{lang} 코드(풀이 {num}): 포스트엔 있는데 PS 레포엔 없음")
            return m.group(0)
        with open(os.path.join(folder, fname), encoding="utf-8") as f:
            code = clean_code(f.read(), lang, fname).rstrip("\n")
        if code != m.group(2).rstrip("\n"):
            updated.append(fname)
        return f"```{m.group(1)}\n{code}\n```"

    new_text = text[:start] + FENCE_RE.sub(replace, body) + text[end:]
    for num, files in sources.items():
        for lang, fname in files.items():
            if (num, lang) not in seen:
                warnings.append(f"{fname}: 포스트에 코드 블록이 없음")
    return new_text, updated, warnings


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
