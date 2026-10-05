"""
Programmers/LeetCode/Codeforces/BOJ 문제 번호로 (제목, 문제 URL)을 조회하는 함수들.
스캐폴드 생성(`generate_one`)에서만 씀 — 제목 조회는 그 시점에만 필요하고, 이후
파이프라인 단계는 이미 만들어진 드래프트 파일만 다룬다.

`scaffold_post.py`에서 이 함수들만 분리한 이유: 나머지(파일명/front matter/본문
빌더)는 순수 문자열 조작인데 이쪽만 유일하게 네트워크 I/O가 섞여 있어서 관심사가
갈림.
"""

import functools
import json
import os
import re
import urllib.request


def fetch(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read().decode("utf-8")


def get_title_and_url(prefix, number):
    """(제목, 문제 URL) 튜플을 반환. URL은 본문의 prompt-info 박스에 그대로 씀."""
    if prefix == "prms":
        return get_title_url_programmers(number)
    if prefix == "leet":
        return get_title_url_leetcode(number)
    if prefix == "cofo":
        return get_title_url_codeforces(number)
    if prefix == "boj":
        return get_title_url_boj(number)
    raise NotImplementedError(f"{prefix} 제목 조회 미구현")


def get_title_url_programmers(number):
    url = f"https://school.programmers.co.kr/learn/courses/30/lessons/{number}"
    html = fetch(url)
    m = re.search(r"<title>코딩테스트 연습 - (.+?) \| 프로그래머스 스쿨</title>", html)
    if not m:
        raise ValueError(
            f"Programmers {number}번 title 태그 패턴이 안 맞음 — 사이트 구조가 바뀌었을 수 있음"
        )
    return m.group(1), url


@functools.lru_cache(maxsize=1)
def _fetch_leetcode_problems():
    # 레거시 엔드포인트 — 언젠가 죽을 수 있음. 죽으면 GraphQL questionList 쪽으로 교체 필요.
    # 응답이 꽤 큰 전체 문제 목록이라 프로세스당 한 번만 받아오게 캐시함 — 안 그러면
    # 배치 모드에서 LeetCode 문제가 여러 개일 때 같은 목록을 문제 수만큼 중복 다운로드함.
    body = fetch("https://leetcode.com/api/problems/all/")
    return json.loads(body)["stat_status_pairs"]


def get_title_url_leetcode(number):
    for item in _fetch_leetcode_problems():
        if str(item["stat"]["frontend_question_id"]) == str(number):
            title = item["stat"]["question__title"]
            slug = item["stat"]["question__title_slug"]
            return title, f"https://leetcode.com/problems/{slug}/"
    raise ValueError(f"LeetCode {number}번을 목록에서 못 찾음")


@functools.lru_cache(maxsize=1)
def _fetch_codeforces_problems():
    # problemset 전체를 받는 큰 응답이라 프로세스당 한 번만 캐시 — 배치 모드에서
    # Codeforces 문제가 여러 개일 때 같은 목록을 중복 다운로드하지 않게
    # (_fetch_leetcode_problems와 동일한 이유).
    body = fetch("https://codeforces.com/api/problemset.problems")
    return json.loads(body)["result"]["problems"]


@functools.cache
def _fetch_codeforces_contest_problems(contest_id):
    # Div1+Div2 통합 대회는 공유 문제가 problemset.problems엔 한쪽 contestId로만
    # 정본화되어 있음(실측: 2263 C1/C2가 problemset.problems엔 없고 2262 A1/A2로만
    # 등록됨) — 이럴 때 그 대회 응시 시점 문제 목록(contest.standings)으로
    # 재조회한다. /problemset/problem/{contest_id}/{index} 링크는 이 경우에도
    # 살아있음.
    body = fetch(f"https://codeforces.com/api/contest.standings?contestId={contest_id}")
    return json.loads(body)["result"]["problems"]


def get_title_url_codeforces(number):
    # 폴더명 형식: "{contestId}{Index}"(예: 1553A)
    m = re.match(r"(\d+)([A-Za-z]\d*)$", number)
    if not m:
        raise ValueError(f"Codeforces 번호 형식이 예상과 다름(예: 1553A): {number}")
    contest_id, index = m.groups()
    index = index.upper()
    url = f"https://codeforces.com/problemset/problem/{contest_id}/{index}"
    for p in _fetch_codeforces_problems():
        if str(p["contestId"]) == contest_id and p["index"] == index:
            return p["name"], url
    for p in _fetch_codeforces_contest_problems(contest_id):
        if p["index"] == index:
            return p["name"], url
    raise ValueError(f"Codeforces {number}번을 목록에서 못 찾음")


# 백준(acmicpc.net)은 2026-04-28부로 서비스가 내려가 있어 온라인 조회가 불가 — iCloud에 있는
# 크롤링 미러(문제당 JSON, `title`·`url` 키)에서 읽는다. URL은 미러가 가진 원본 그대로
# (`https://www.acmicpc.net/problem/{번호}`)라 기존 백준 포스트의 링크 형식과 같다.
BOJ_MIRROR_DIR = os.path.expanduser(
    "~/Library/Mobile Documents/com~apple~CloudDocs/baekjoon-crawling/data/problems"
)


def get_title_url_boj(number):
    path = os.path.join(BOJ_MIRROR_DIR, f"{number}.json")
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        raise ValueError(f"BOJ {number}번이 크롤링 미러에 없음: {path}")
    return data["title"], data["url"]
