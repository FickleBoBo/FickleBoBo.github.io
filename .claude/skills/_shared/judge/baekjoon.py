"""BaekJoon: 문제 제목·URL은 문제 페이지 `<title>`에서, 원문은 iCloud 크롤링 미러 JSON에서 읽는다."""

import html
import json
import os
import re

from . import net
from .html_text import html_to_text

PREFIX = "boj"
PLATFORM = "BaekJoon"
HOST = "acmicpc.net"

MIRROR_DIR = os.path.expanduser(
    "~/Library/Mobile Documents/com~apple~CloudDocs/baekjoon-crawling/data"
)


def title_and_url(number):
    url = f"https://www.acmicpc.net/problem/{number}"
    m = re.search(r"<title>\d+번: (.+?)</title>", net.get(url))
    if not m:
        raise ValueError(f"BaekJoon {number}번 title 패턴 불일치 — 사이트 구조 변경?")
    return html.unescape(m.group(1)), url


def statement(url):
    m = re.search(r"/problem/(\d+)", url)
    if not m:
        raise ValueError(f"URL에서 문제 번호를 못 찾음: {url[:80]}")
    number = m.group(1)
    with open(
        os.path.join(MIRROR_DIR, "problems", f"{number}.json"), encoding="utf-8"
    ) as f:
        d = json.load(f)
    info = d.get("info", {})
    parts = [
        f"# {d.get('title')}",
        f"- 시간 제한: {info.get('time_limit')} / 메모리 제한: {info.get('memory_limit')}",
        f"- 확보: iCloud 크롤링 미러(crawled_at {d.get('crawled_at')})",
    ]
    for heading, key in (
        ("문제", "description"),
        ("입력", "input"),
        ("출력", "output"),
        ("제한", "limit"),
        ("힌트", "hint"),
    ):
        body = html_to_text(d.get(key) or "")
        if body:
            parts += ["", f"## {heading}", body]
    for s in d.get("samples", []):
        n = s.get("number")
        parts += [
            "",
            f"## 예제 입력 {n}",
            "```",
            s.get("input", "").rstrip("\n"),
            "```",
            f"## 예제 출력 {n}",
            "```",
            s.get("output", "").rstrip("\n"),
            "```",
        ]
    image_dir = os.path.join(MIRROR_DIR, "images", number)
    if os.path.isdir(image_dir):
        parts += [
            "",
            "## 이미지 로컬 사본",
            image_dir + "/ : " + ", ".join(sorted(os.listdir(image_dir))),
        ]
    return "\n".join(parts)
