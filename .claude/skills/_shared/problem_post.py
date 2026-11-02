"""
문제 포스트(`## 1. 아이디어` + `## 2. 코드`)의 구조 규약: 섹션 헤딩과 아이디어 작성 여부.
"""

import re

from post_text import section_span

# 문제 포스트의 본문 섹션 헤딩 — 스캐폴드가 만들고 린터·`publish`가 그대로 찾는다.
IDEA_HEADING = "## 1. 아이디어"
CODE_HEADING = "## 2. 코드"
QUERY_HEADING = "## 2. 쿼리"
# 코드 섹션 헤딩 패턴. 번호는 신(`## 2.`)·구(`## 3.`) 모두 받는다.
CODE_SECTION_PATTERN = r"## \d+\. (?:코드|쿼리)"


def idea_is_filled(text):
    """아이디어 섹션에 HTML 주석·구분선(---)을 뺀 실제 텍스트가 있는지. 헤딩이 없어도 미완료.
    `publish`의 완료 게이트이자 `tag`가 태그를 판정하기 전 전제다."""
    span = section_span(text, re.escape(IDEA_HEADING))
    if not span:
        return False
    body = text[span[0] : span[1]].split("\n", 1)[1]
    body = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL)
    return any(line.strip() not in ("", "---") for line in body.splitlines())
