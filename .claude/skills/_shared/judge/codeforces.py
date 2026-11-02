"""
Codeforces: 제목·URL은 공개 API에서 읽는다. 문제 페이지는 직접 조회가 막혀 있어(403) 원문은 직접
받지 않는다(`statement`가 없다). TinyFish 등으로 받은 텍스트를 `check_statement`로 검사해 저장한다.
"""

import functools
import re

from . import net

PREFIX = "cofo"
PLATFORM = "Codeforces"
HOST = "codeforces.com"

statement = None  # 직접 조회 불가

_REQUIRED = ["time limit per test", "memory limit per test", "Input", "Output"]
_REQUIRED_ANY = ["Example", "Examples"]


@functools.cache
def _problemset():
    return net.get_json("https://codeforces.com/api/problemset.problems")["result"][
        "problems"
    ]


@functools.cache
def _contest_problems(contest_id):
    # Div1+Div2 통합 대회의 공유 문제는 problemset.problems에 한쪽 contestId로만 있어서
    # (예: 2263 C1/C2는 2262 A1/A2로만 등록) 그 대회의 문제 목록으로 다시 찾는다.
    url = f"https://codeforces.com/api/contest.standings?contestId={contest_id}"
    return net.get_json(url)["result"]["problems"]


def problem_name(contest_id, index):
    for p in _problemset():
        if str(p["contestId"]) == contest_id and p["index"] == index:
            return p["name"]
    for p in _contest_problems(contest_id):
        if p["index"] == index:
            return p["name"]
    raise ValueError(f"Codeforces {contest_id}{index}번을 목록에서 못 찾음")


def title_and_url(number):
    """number는 `{contestId}{Index}`(Index 대문자, 예: 1553A, 2263C1)."""
    m = re.fullmatch(r"(\d+)([A-Z]\d*)", number)
    if not m:
        raise ValueError(f"Codeforces 번호 형식 불일치(예: 1553A, 2263C1): {number}")
    contest_id, index = m.groups()
    url = f"https://codeforces.com/problemset/problem/{contest_id}/{index}"
    return problem_name(contest_id, index), url


def ids_of_url(url):
    m = re.search(r"/problemset/problem/(\d+)/(\w+)", url) or re.search(
        r"/contest/(\d+)/problem/(\w+)", url
    )
    if not m:
        raise ValueError(f"URL에서 문제 번호를 못 찾음: {url[:80]}")
    return m.group(1), m.group(2)


def check_statement(url, text):
    """TinyFish 등으로 받은 지문의 완전성 검사: 필수 구간과 API 제목 대조. 문제 목록을 돌려준다
    (비면 통과). API 대조 수단이 없다고 저장을 막지는 않는다(경고만)."""
    problems = [f"필수 구간 누락: {w}" for w in _REQUIRED if w not in text]
    if not any(w in text for w in _REQUIRED_ANY):
        problems.append("필수 구간 누락: Example")
    contest_id, index = ids_of_url(url)
    try:
        name = problem_name(contest_id, index)
        if f"{index}. {name}" not in text.splitlines()[0]:
            problems.append(f"제목 불일치: 기대 '{index}. {name}'")
    except Exception as e:
        print(f"경고: Codeforces API 제목 대조 실패({e})")
    return problems
