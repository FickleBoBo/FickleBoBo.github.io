"""LeetCode: 문제 제목·URL과 원문 모두 GraphQL에서 읽는다."""

import functools
import json
import re
import urllib.error

from . import net
from .html_text import html_to_text

PREFIX = "leet"
PLATFORM = "LeetCode"
HOST = "leetcode.com"

_GRAPHQL_QUERY = (
    "query q($t:String!){question(titleSlug:$t){title difficulty content hints}}"
)

_PAGE = 50
_LIST_QUERY = (
    "query p($l:Int,$s:Int,$f:QuestionListFilterInput){"
    'questionList(categorySlug:"",limit:$l,skip:$s,filters:$f)'
    "{total:totalNum data{id:questionFrontendId title titleSlug}}}"
)


def _graphql(query, variables):
    payload = json.dumps({"query": query, "variables": variables}).encode()
    return json.loads(
        net.get(
            "https://leetcode.com/graphql",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
    )


def _find(number):
    """번호 검색 결과(제목 등에 숫자가 섞여 여러 개일 수 있음)에서 번호가 정확히 같은 문제를 찾는다."""
    skip = 0
    while True:
        page = _graphql(
            _LIST_QUERY,
            {"l": _PAGE, "s": skip, "f": {"searchKeywords": number}},
        )["data"]["questionList"]
        for q in page["data"]:
            if q["id"] == number:
                return q
        skip += _PAGE
        if skip >= page["total"]:
            return None


@functools.cache
def title_and_url(number):
    # /api/problems/all/은 Cloudflare 챌린지로 403이 반복돼 쓰지 않는다. 원문과 같은 GraphQL로 읽는다.
    try:
        q = _find(number)
    except urllib.error.HTTPError as e:
        raise RuntimeError(
            f"LeetCode 제목 조회 실패(HTTP {e.code}). Cloudflare 차단이면 우회하지 말고 "
            "사용자 Chrome(claude-in-chrome)에서 조회한다(ps/SKILL.md)."
        ) from e
    if not q:
        raise ValueError(f"LeetCode {number}번을 못 찾음")
    return q["title"], f"https://leetcode.com/problems/{q['titleSlug']}/"


def statement(url):
    m = re.search(r"/problems/([^/]+)", url)
    if not m:
        raise ValueError(f"URL에서 문제 slug를 못 찾음: {url[:80]}")
    slug = m.group(1)
    resp = _graphql(_GRAPHQL_QUERY, {"t": slug})
    q = resp["data"]["question"]
    if not q or not q.get("content"):
        raise ValueError(f"문제를 못 찾았거나 본문이 비어 있음(유료 문제 가능): {slug}")
    parts = [
        f"# {q['title']}",
        f"- 난이도: {q['difficulty']}",
        "- 확보: LeetCode GraphQL",
        "",
        html_to_text(q["content"]),
    ]
    for i, h in enumerate(q.get("hints") or [], 1):
        parts += ["", f"## 힌트 {i}", html_to_text(h)]
    return "\n".join(parts)
