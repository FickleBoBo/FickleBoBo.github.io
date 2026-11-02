"""LeetCode: 문제 제목·URL은 전체 목록 API에서, 원문은 GraphQL에서 읽는다."""

import functools
import json
import re

from . import net
from .html_text import html_to_text

PREFIX = "leet"
PLATFORM = "LeetCode"
HOST = "leetcode.com"

_GRAPHQL_QUERY = (
    "query q($t:String!){question(titleSlug:$t){title difficulty content hints}}"
)


@functools.cache
def _problems():
    # 전체 목록 응답이 커서 프로세스당 한 번만 받는다.
    return net.get_json("https://leetcode.com/api/problems/all/")["stat_status_pairs"]


def title_and_url(number):
    for item in _problems():
        stat = item["stat"]
        if str(stat["frontend_question_id"]) == number:
            slug = stat["question__title_slug"]
            return stat["question__title"], f"https://leetcode.com/problems/{slug}/"
    raise ValueError(f"LeetCode {number}번을 목록에서 못 찾음")


def statement(url):
    m = re.search(r"/problems/([^/]+)", url)
    if not m:
        raise ValueError(f"URL에서 문제 slug를 못 찾음: {url[:80]}")
    slug = m.group(1)
    payload = json.dumps({"query": _GRAPHQL_QUERY, "variables": {"t": slug}}).encode()
    resp = json.loads(
        net.get(
            "https://leetcode.com/graphql",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
    )
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
