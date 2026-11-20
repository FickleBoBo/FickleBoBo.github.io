"""solved.ac 공식 API(v4)에서 백준 문제의 난이도·태그를 읽는다. 표준 라이브러리만 쓴다.

`review-code`·`review-post`의 서브에이전트가 "의도된 해"를 지문 제약만으로 추측하지 않도록, 백준 원문
파일에 난이도 한 줄을 덧붙이는 데 쓴다(`judge/baekjoon.py`). 정본은 공식 명세
(https://backstage.solved.ac/api/v4/openapi)다.

- 인증: 모든 요청에 앱의 `x-client-id`·`x-client-secret` 헤더가 필요하다. 값은 환경변수
  `SOLVEDAC_CLIENT_ID`·`SOLVEDAC_CLIENT_SECRET`에서만 읽고 레포·로그·출력에 남기지 않는다.
- 문제 조회: `GET https://solved.ac/api/v4/problems/{백준 번호}`(요청당 1유닛, 호출자당 600유닛 버킷을
  초당 2유닛씩 충전, 초과하면 429 + `Retry-After`). 백준 문제는 `problemId`가 백준 번호와 같다
  (응답 `judgeIds`로 대조한다).
- 실패(키 없음·네트워크·429·형식 변경)는 예외를 던지지 않고 `미확인` 한 줄로 돌려준다 — 난이도는
  보조 정보라 원문 확보를 막지 않는다. 호출자는 그 줄로 미확인임을 알린다.
- v3(`/api/v3/*`)는 2026-11-17 공지로 지원이 종료됐다. v4 태그 키는 v3와 다르다(`arbitrary_precision` → `big`).
"""

import json
import os
import urllib.error
import urllib.request

API = "https://solved.ac/api/v4/problems/{}"
TIERS = ("Bronze", "Silver", "Gold", "Platinum", "Diamond", "Ruby")
ROMAN = ("V", "IV", "III", "II", "I")


def tier_name(level):
    """solved.ac 레벨(0~30) → `Bronze V` 형식. 0은 Unrated, 범위 밖은 `레벨 N`."""
    if level == 0:
        return "Unrated"
    if not isinstance(level, int) or not 1 <= level <= 30:
        return f"레벨 {level}"
    return f"{TIERS[(level - 1) // 5]} {ROMAN[(level - 1) % 5]}"


def fetch(number):
    """백준 번호의 solved.ac 문제 JSON. 실패하면 예외."""
    cid = os.environ.get("SOLVEDAC_CLIENT_ID")
    secret = os.environ.get("SOLVEDAC_CLIENT_SECRET")
    if not cid or not secret:
        raise RuntimeError("SOLVEDAC_CLIENT_ID/SECRET 환경변수 없음")
    req = urllib.request.Request(
        API.format(number),
        headers={
            "x-client-id": cid,
            "x-client-secret": secret,
            "User-Agent": "Mozilla/5.0",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError(
            f"HTTP {e.code}"
        ) from None  # 본문·헤더는 키가 섞일 수 있어 버린다
    if not any(
        j.get("ojId") == "boj" and j.get("problemId") == str(number)
        for j in data.get("judgeIds", [])
    ):
        raise RuntimeError("응답의 judgeIds가 백준 번호와 안 맞음")
    return data


def difficulty_line(number):
    """원문 파일에 덧붙일 한 줄(`- 난이도: ...`). 실패해도 예외 없이 `미확인` 줄을 돌려준다."""
    try:
        d = fetch(number)
        level = d["level"]
        tags = ", ".join(t["key"] for t in d.get("tags", [])) or "없음"
        return (
            f"- 난이도: {tier_name(level)} (solved.ac 레벨 {level}) / 태그: {tags}"
            " (solved.ac 공식 API)"
        )
    except Exception as e:
        return f"- 난이도: 미확인 (solved.ac 조회 실패: {e})"
