"""Programmers: 제목·원문 모두 문제 페이지 HTML(서버 렌더링)에서 읽는다."""

import html
import re

from . import net
from .html_text import html_to_text

PREFIX = "prms"
PLATFORM = "Programmers"
HOST = "programmers.co.kr"


def _page_url(number):
    return f"https://school.programmers.co.kr/learn/courses/30/lessons/{number}"


def title_and_url(number):
    url = _page_url(number)
    m = re.search(
        r"<title>코딩테스트 연습 - (.+?) \| 프로그래머스 스쿨</title>", net.get(url)
    )
    if not m:
        raise ValueError(
            f"Programmers {number}번 title 패턴 불일치 — 사이트 구조 변경?"
        )
    return html.unescape(m.group(1)), url


def statement(url):
    page = net.get(url)
    m = re.search(r'property="og:title"[^>]*content="([^"]*)"', page)
    if not m:
        raise ValueError(f"og:title을 못 찾음: {page[:80]}")
    title = m.group(1).replace("코딩테스트 연습 - ", "")
    body = html_to_text(page, capture_class="markdown")
    if not body:
        raise ValueError("문제 본문 영역(markdown)을 못 찾음")
    return "\n".join([f"# {title}", "- 확보: 프로그래머스 문제 페이지 HTML", "", body])
