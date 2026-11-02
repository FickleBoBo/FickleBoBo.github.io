"""
포스트 본문의 코드 펜스를 PS 레포 소스로 교체하는 순수 변환(`sync_text`). 파일 입출력은 호출하는 쪽 몫.
"""

import os
import re

from clean_code import clean_code
from post_text import section_span
from problem_post import CODE_SECTION_PATTERN
from ps_source import LANGUAGE_OF_FENCE, find_source_files, group_by_approach

APPROACH_HEADING_RE = re.compile(r"^### 풀이(?: (\d+))?", re.MULTILINE)
# 줄 시작에 고정해 빈 코드 블록이 뒤 블록을 삼키지 않게 한다. 본문은 끝 줄바꿈까지 포함.
FENCE_RE = re.compile(r"^```(\S+)\n(.*?)^```[ \t]*$", re.DOTALL | re.MULTILINE)


def _approach_at(headings, pos):
    """pos가 속한 `### 풀이 N` 구간의 N. 첫 풀이 헤딩 앞이면 None."""
    num = None
    for start, n in headings:
        if start > pos:
            break
        num = n
    return num


def sync_text(text, folder):
    """(새 본문, 갱신한 파일명 리스트, 알림 리스트). 접근법 구간 안의 언어별 첫 펜스를 같은 번호의 소스로 교체."""
    span = section_span(text, CODE_SECTION_PATTERN)
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
        lang = LANGUAGE_OF_FENCE.get(m.group(1))
        num = _approach_at(headings, m.start())
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
