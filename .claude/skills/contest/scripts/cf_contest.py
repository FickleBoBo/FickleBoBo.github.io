"""
Codeforces API 조회와 문제별 성적 계산 — 이 스킬에서 네트워크를 쓰는 유일한 모듈.
후기 본문 조립은 `recap_body.py`, 파일 쓰기는 `scaffold_contest.py`.

코드를 고칠 때 알아야 할 것:

- **CF API는 익명 GET이면 브라우저 UA도 불필요**(지문 조회와 다름 — 프로젝트 메모리
  `ps-problem-statement-fetch` 참고). 단 `contest.standings?contestId=`는 파라미터를
  하나라도 더 붙이면 FAILED("no extra parameters") — bare로만 호출. 응답이 크다(수 MB,
  행 ~11000에서 잘리지만 JSON 자체는 유효하고 우리가 쓰는 `result.contest`/`result.problems`는
  앞부분이라 안전).
- **페널티는 어느 API에도 없다** — 반드시 계산한다. CF Div 3는 ICPC 방식: 해결한 문제마다
  `floor(AC분) + 10 * (AC 이전 오답 중 passedTestCount>=1)`. ⚠ 샘플/1번 테스트도 못 넘긴
  오답(`passedTestCount == 0`)·컴파일 에러는 페널티 미포함. 이거 안 걸러서 1119를 198로
  계산했다가 실제 188과 틀린 적 있음.
- **순위·레이팅 소스 불일치** — CF가 자기 페이지끼리도 다르다(`/ratings` 5272 vs 프로필
  5419 vs `/standings` 6240). 결정: `contest.ratingChanges` API 기준(= `/ratings` 페이지,
  rated 성적의 캐노니컬 뷰). 순위·레이팅·rated 참가자 수 전부 여기서. 페널티는 계산값이고
  순위·레이팅은 롤백 타이밍에 따라 흔들리므로 발행 전 `/contest/{id}/standings`에서 눈으로
  대조한다(스크립트는 스탯만 넣고 경고 주석은 안 박는다 — 사용자가 주석 없는 골격을 원함).
- **첫 대회 레이팅**: `ratingChanges.oldRating == 0`은 센티넬이고 CF `/ratings` 페이지는
  `100 → new`(+`new-100`)로 표시한다. 계정당 한 번뿐. 2번째 대회부터 `oldRating`이 CF
  표시와 정확히 일치.
"""

import json
import urllib.request

HANDLE = "FickleBoBo"
CF_API = "https://codeforces.com/api"


def cf_get(method, **params):
    """CF API 호출 → result 반환. status != OK면 예외."""
    qs = "&".join(f"{k}={v}" for k, v in params.items())
    url = f"{CF_API}/{method}?{qs}" if qs else f"{CF_API}/{method}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    if data.get("status") != "OK":
        raise RuntimeError(f"CF API {method} 실패: {data.get('comment', data)}")
    return data["result"]


def load_contest(contest_id):
    """contest.standings(bare)에서 대회 메타 + 문제 목록."""
    result = cf_get("contest.standings", contestId=contest_id)
    problems = [{"index": p["index"], "name": p["name"]} for p in result["problems"]]
    if not problems:
        raise RuntimeError(
            f"대회 {contest_id}에 문제가 없음 — 대회가 아직 시작 안 됐을 수 있음"
        )
    return result["contest"], problems


def load_rating_change(contest_id):
    """(rated 참가자 수, 내 항목 또는 None).
    대회 직후엔 ratingChanges가 아직 비어 있을 수 있음 → (0, None)."""
    result = cf_get("contest.ratingChanges", contestId=contest_id)
    mine = next((r for r in result if r["handle"].lower() == HANDLE.lower()), None)
    return len(result), mine


def load_submissions(contest_id):
    """내 제출 전부(생성 시각 오름차순)."""
    result = cf_get("contest.status", contestId=contest_id, handle=HANDLE)
    return sorted(result, key=lambda s: s["creationTimeSeconds"])


def classify_problems(problems, submissions, duration_seconds):
    """문제 index -> {
        result: 'AC' | '업솔빙' | '미해결' | '미시도',
        ac_rel: 대회 중 AC의 relativeTimeSeconds (AC일 때만),
        penalty_wrong: 페널티에 카운트되는 오답 수 (AC일 때만),
        problem_penalty: 이 문제가 총 페널티에 더하는 값 (AC일 때만),
    }
    """
    by_index = {}
    for p in problems:
        idx = p["index"]
        subs = [s for s in submissions if s["problem"]["index"] == idx]

        # 대회 중 = 공식 참가(CONTESTANT) + 대회 시간 내.
        in_contest = sorted(
            (
                s
                for s in subs
                if s["author"]["participantType"] == "CONTESTANT"
                and s["relativeTimeSeconds"] <= duration_seconds
            ),
            key=lambda s: s["relativeTimeSeconds"],
        )
        ac = next((s for s in in_contest if s["verdict"] == "OK"), None)

        if ac:
            ac_rel = ac["relativeTimeSeconds"]
            wrong = sum(
                1
                for s in in_contest
                if s["relativeTimeSeconds"] < ac_rel
                and s["verdict"] != "OK"
                and s.get("passedTestCount", 0) >= 1
            )
            by_index[idx] = {
                "result": "AC",
                "ac_rel": ac_rel,
                "penalty_wrong": wrong,
                "problem_penalty": ac_rel // 60 + 10 * wrong,
            }
        elif any(s["verdict"] == "OK" for s in subs):
            by_index[idx] = {"result": "업솔빙"}
        elif subs:
            by_index[idx] = {"result": "미해결"}
        else:
            by_index[idx] = {"result": "미시도"}
    return by_index


def compute_penalty(by_index):
    return sum(v["problem_penalty"] for v in by_index.values() if v["result"] == "AC")


def determine_participation(mine, submissions):
    """rated 성적(`mine`)과 제출 로그의 participantType으로 참가 형태 문자열을 정한다.
    셋 다 아니면(제출이 전혀 없거나 참관만 함) 공식 참가 기본값."""
    if mine:
        return "공식 (rated)"
    if any(s["author"]["participantType"] == "CONTESTANT" for s in submissions):
        return "오픈 (공식 시간, unrated)"
    if any(s["author"]["participantType"] == "VIRTUAL" for s in submissions):
        return "가상 (virtual, unrated)"
    return "공식 (rated)"


def load_rating_points(contest, mine):
    """카드 그래프용 레이팅 이력(시작값 포함). 이 대회 '이전' 참가분 + (rated면) 이 대회.
    ratingUpdateTimeSeconds < 대회 시작 시각인 항목이 이전 대회 — 재생성(과거 대회
    소급) 때도 그 시점 그래프가 나온다. oldRating==0(첫 대회 센티넬)은 CF 표시대로 100."""
    hist = cf_get("user.rating", handle=HANDLE)
    prior = [
        r for r in hist if r["ratingUpdateTimeSeconds"] < contest["startTimeSeconds"]
    ]
    entries = prior + ([mine] if mine else [])
    if not entries:
        return []
    first = entries[0]["oldRating"] or 100
    return [first] + [e["newRating"] for e in entries]


def build_card_data(contest, start_kst, problems, by_index, penalty, rank_count, mine):
    """`render_card.render_card`가 받는 dict. 레이팅 이력 조회(user.rating)가 포함돼 네트워크를 탄다."""
    data = {
        "name": contest["name"],
        "date": f"{start_kst:%Y.%m.%d}",
        "solved": sum(1 for v in by_index.values() if v["result"] == "AC"),
        "total": len(problems),
        "penalty": penalty,
        "rank": None,
        "rank_count": rank_count,
        "pct": None,
        "ratings": load_rating_points(contest, mine),
        "delta": None,
    }
    if mine:
        data["rank"] = mine["rank"]
        data["pct"] = round(mine["rank"] / rank_count * 100, 1) if rank_count else 0
        data["delta"] = mine["newRating"] - (mine["oldRating"] or 100)
    return data
