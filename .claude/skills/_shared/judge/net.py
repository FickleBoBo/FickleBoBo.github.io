"""저지 사이트 조회용 HTTP GET/POST. 표준 라이브러리만 쓴다."""

import json
import urllib.request

USER_AGENT = "Mozilla/5.0"


def get(url, data=None, headers=None):
    """`data`를 주면 POST. 응답 본문을 UTF-8 문자열로 돌려준다."""
    req = urllib.request.Request(
        url, data=data, headers={"User-Agent": USER_AGENT, **(headers or {})}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def get_json(url):
    return json.loads(get(url))
