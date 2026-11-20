"""BaekJoon: 제목·원문 모두 문제 페이지 HTML에서 읽는다(2026-11-20 재오픈 확인).

원문은 라이브 페이지가 먼저이고, 페이지를 못 읽을 때(사이트 중단·차단)만 iCloud 크롤링 미러 JSON으로
떨어진다. 미러는 재오픈 이전 스냅샷이라 새 문제·정정된 지문은 라이브만 정확하다.

원문에는 solved.ac 공식 API로 읽은 `- 난이도: ... / 태그: ...` 줄이 `- 확보:` 줄 뒤에 붙는다
(`solvedac.py`, 키 환경변수 필요). 못 읽으면 `미확인` 줄이 붙고 원문 확보는 계속된다.
"""

import html
import json
import os
import re

import solvedac

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


def _div_inner(page, div_id):
    """`<div id=div_id ...>` 안쪽 HTML(중첩 div 균형 맞춤). 없으면 None."""
    m = re.search(rf'<div[^>]*\bid="{div_id}"[^>]*>', page)
    if not m:
        return None
    depth, pos = 1, m.end()
    for t in re.finditer(r"<(/?)div\b", page[pos:]):
        depth += -1 if t.group(1) else 1
        if depth == 0:
            return page[pos : pos + t.start()]
    return None


def _live_statement(number, url):
    page = net.get(url)
    desc = _div_inner(page, "problem_description")
    if desc is None:
        raise ValueError("문제 본문(problem_description)을 못 찾음")
    t = re.search(r"<title>\d+번: (.+?)</title>", page)
    info = re.search(
        r'id="problem-info".*?<tbody><tr><td>(.*?)</td><td>(.*?)</td>', page, re.S
    )
    parts = [f"# {html.unescape(t.group(1)) if t else number}"]
    if info:
        parts.append(
            f"- 시간 제한: {info.group(1).strip()} / 메모리 제한: {info.group(2).strip()}"
        )
    parts.append("- 확보: 백준 문제 페이지 HTML")
    for heading, key in (
        ("문제", "problem_description"),
        ("입력", "problem_input"),
        ("출력", "problem_output"),
        ("제한", "problem_limit"),
        ("힌트", "problem_hint"),
    ):
        body = html_to_text(_div_inner(page, key) or "")
        if body:
            parts += ["", f"## {heading}", body]
    n = 1
    while True:
        i = re.search(rf'<pre[^>]*id="sample-input-{n}"[^>]*>(.*?)</pre>', page, re.S)
        o = re.search(rf'<pre[^>]*id="sample-output-{n}"[^>]*>(.*?)</pre>', page, re.S)
        if not i or not o:
            break
        for label, m in (("입력", i), ("출력", o)):
            parts += [
                "",
                f"## 예제 {label} {n}",
                "```",
                html.unescape(m.group(1)).replace("\r", "").strip("\n"),
                "```",
            ]
        n += 1
    if n == 1:
        raise ValueError("예제를 못 찾음")
    return "\n".join(parts)


def statement(url):
    m = re.search(r"/problem/(\d+)", url)
    if not m:
        raise ValueError(f"URL에서 문제 번호를 못 찾음: {url[:80]}")
    number = m.group(1)
    return _with_difficulty(number, _statement_body(number))


def _with_difficulty(number, text):
    """`- 확보:` 줄 바로 뒤에 solved.ac 난이도·태그 줄을 넣는다(없으면 맨 앞 헤더 뒤)."""
    line = solvedac.difficulty_line(number)
    if "미확인" in line:
        print(f"  ⚠ {line}")
    lines = text.split("\n")
    at = next((i for i, ln in enumerate(lines) if ln.startswith("- 확보:")), 0)
    lines.insert(at + 1, line)
    return "\n".join(lines)


def _statement_body(number):
    try:
        text = _live_statement(number, f"https://www.acmicpc.net/problem/{number}")
        text = text.replace("[이미지: /", "[이미지: https://www.acmicpc.net/")
        # 그림은 서브에이전트가 Read로 열어야 하므로 미러에 로컬 사본이 있으면 경로를 붙인다
        image_dir = os.path.join(MIRROR_DIR, "images", number)
        if "[이미지:" in text and os.path.isdir(image_dir):
            text += (
                "\n\n## 이미지 로컬 사본\n"
                + image_dir
                + "/ : "
                + ", ".join(sorted(os.listdir(image_dir)))
            )
        return text
    except Exception as e:  # 사이트 중단·차단·구조 변경 — 미러로 폴백
        print(f"  (라이브 조회 실패, 미러로 폴백: {e})")
    return _mirror_statement(number)


def _mirror_statement(number):
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
