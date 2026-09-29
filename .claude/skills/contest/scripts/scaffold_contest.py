#!/usr/bin/env python3
"""
Codeforces 대회 ID(또는 URL)를 받아서, 이 블로그의 대회 후기 포스트 파일명 +
front matter + 본문 스켈레톤을 결정론적으로 생성한다. LLM 판단 없음 — CF API 응답
파싱 / 페널티 계산(고정 공식) / 등급 색 룩업 / 파일 스캔 / 문자열 치환만 함.

`ps` 스킬과 평행 구조: 스크립트가 확정 가능한 것(front matter·대회 개요·결과 표·
풀이 과정 스탯 표)을 전부 채우고, 문제별 서술·라이브 코드·총평·수동 뉘앙스는
사람이 채운다.

**후기 포스트의 '양식'(섹션 구성·표 컬럼·어휘)은 `contest/SKILL.md`가 정본,
설계 근거 전체는 프로젝트 메모리 `contest-recap-post-format.md`.** 여기 docstring은
사용법 + 코드를 고칠 때 바로 옆 코드만 봐선 안 보이는 '왜'만 남겨둔다.

코드를 고칠 때 알아야 할 것:

- **파이프라인 밖 장르.** 이 스크립트는 `_drafts/contest/`에만 쓴다. 이 폴더는
  `publish.py`/`sync_code.py`의 `PLATFORM_MAP`(programmers/leetcode/codeforces)에
  없어서 두 스킬이 통째로 무시한다 — 의도된 안전장치. 발행은 같은 스킬의
  `publish_contest.py`가 담당(`_drafts/contest/` → `_posts/contest/` 이동 + 두
  레포 커밋).

- **`build_body`의 "---" 구분선**은 `ps`의 `resolve_filename.py`와 똑같이 항상
  "뒤 섹션이 자기 앞에 다는 것"으로 소유한다(섹션 사이 접착제 아님). `## 3. 풀이
  과정` 안의 각 `### {index}` 서브섹션도 하나의 '섹션'으로 취급해 자기 앞에 "---"를
  단다. 맨 끝 "---"는 어느 섹션에도 안 딸린 문서 끝 마커.

- **페널티는 어느 API에도 없다** — 반드시 계산한다(`compute_penalty`). CF Div 3는
  ICPC 방식: 해결한 문제마다 `floor(AC분) + 10 * (AC 이전 오답 중 passedTestCount>=1)`.
  ⚠ 샘플/1번 테스트도 못 넘긴 오답(`passedTestCount == 0`)·컴파일 에러는 페널티
  미포함. 이거 안 걸러서 1119를 198로 계산했다가 실제 188과 틀린 적 있음.

- **순위·레이팅 소스 불일치** — CF가 자기 페이지끼리도 다르다(`/ratings` 5272 vs
  프로필 5419 vs `/standings` 6240). 결정: `contest.ratingChanges` API 기준
  (= `/ratings` 페이지, rated 성적의 캐노니컬 뷰). 순위·레이팅·rated 참가자 수
  전부 여기서. 페널티는 계산값이고 순위·레이팅은 롤백 타이밍에 따라 흔들리므로
  발행 전 `/contest/{id}/standings` 페이지에서 눈으로 대조하는 게 좋다(스크립트는
  스탯만 넣고 경고 주석은 안 박는다 — 사용자가 주석 없는 골격을 원함).

- **첫 대회 레이팅**: `ratingChanges.oldRating == 0`은 센티넬이고 CF `/ratings`
  페이지는 `100 → new`(+`new-100`)로 표시한다. 계정당 한 번뿐. 2번째 대회부터
  `oldRating`이 CF 표시와 정확히 일치.

- **CF API는 익명 GET이면 브라우저 UA도 불필요**(지문 조회와 다름 — 그쪽은 UA
  필요, 프로젝트 메모리 `ps-problem-statement-fetch` 참고). 단
  `contest.standings?contestId=`는 파라미터를 하나라도 더 붙이면 FAILED
  ("no extra parameters") — bare로만 호출. 응답이 크다(수 MB, 행 ~11000에서 잘리지만
  JSON 자체는 유효하고 우리가 쓰는 `result.contest`/`result.problems`는 앞부분이라 안전).

- **등급 색**(`RANK_TIERS`)은 2026-09-07 CF `community.css` 실측. legendary
  grandmaster(3000+)의 "첫 글자 검정"은 v1 미구현(이 핸들이 도달할 일이 수년간 없음).

사용법:
    python3 scaffold_contest.py <대회 ID 또는 URL> [--force | --card-only]

    예:
        python3 scaffold_contest.py 2259
        python3 scaffold_contest.py https://codeforces.com/contest/2259

    핸들은 이 파일 상수(HANDLE). 같은 이름 파일이 `_drafts/contest/`에 이미 있으면
    거부(사람이 채운 서술·라이브 코드 보호) — 재생성은 --force.

    스켈레톤과 함께 프리뷰 카드(`assets/img/posts/{slug}/preview.png`)를 렌더하고
    front matter에 `image:`를 넣는다(렌더러는 `render_card.py`). Chrome이 없으면 카드만
    생략하고 계속. `--card-only`는 이미 있는 후기(드래프트·발행본)의 카드만 (재)생성하고
    front matter에 image가 없으면 넣는다 — 서술·코드는 안 건드림.

    성공하면 stdout엔 쓴 파일의 절대경로만. stderr엔 페널티·순위 요약(눈 대조용).
"""

import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

_SKILLS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_SKILLS_DIR, "ps", "scripts"))

# REPO_ROOT/sanitize_filename/yaml_dq는 ps 스킬(resolve_filename.py) 걸 그대로
# 가져다 씀 — 파일명 이스케이프 표·YAML 이스케이프 로직이 두 스킬에서 갈라지면
# 안 되기 때문(publish_contest.py가 REPO_ROOT를 같은 방식으로 가져다 쓰는 것과
# 동일 패턴).
from render_card import ChromeNotFound, render_card
from resolve_filename import REPO_ROOT, sanitize_filename, yaml_dq

# ── 상수 ──────────────────────────────────────────────────────────────────────

HANDLE = "FickleBoBo"

KST = timezone(timedelta(hours=9))

CONTEST_DRAFTS_DIR = os.path.join(REPO_ROOT, "_drafts", "contest")
# 정제된 개별 문제 풀이 포스트가 사는 곳. AC·업솔빙 서브섹션은 실재 여부와 무관하게
# 팁 링크를 달지만(어차피 나중에 만들 것이므로), 미해결 서브섹션은 이 디렉터리에
# 파일이 실재할 때만 예외적으로 단다(_drafts/는 안 봄, 아직 미발행이므로).
CODEFORCES_POSTS_DIR = os.path.join(REPO_ROOT, "_posts", "codeforces")

CF_API = "https://codeforces.com/api"

CARD_NAME = (
    "preview.png"  # assets/img/posts/{slug}/ 아래. front matter image.path가 가리킴
)

# (하한 레이팅, 등급명, hex) — rating >= 하한인 마지막 튜플이 그 등급.
# 2026-09-07 CF community.css 실측.
RANK_TIERS = [
    (0, "newbie", "#808080"),
    (1200, "pupil", "#008000"),
    (1400, "specialist", "#03A89E"),
    (1600, "expert", "#0000FF"),
    (1900, "candidate master", "#AA00AA"),
    (2100, "master", "#FF8C00"),
    (2300, "international master", "#FF8C00"),
    (2400, "grandmaster", "#FF0000"),
    (2600, "international grandmaster", "#FF0000"),
    (3000, "legendary grandmaster", "#FF0000"),
]


# ── CF API ────────────────────────────────────────────────────────────────────


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8")


def cf_get(method, **params):
    """CF API 호출 → result 반환. status != OK면 예외."""
    qs = "&".join(f"{k}={v}" for k, v in params.items())
    url = f"{CF_API}/{method}?{qs}" if qs else f"{CF_API}/{method}"
    data = json.loads(fetch(url))
    if data.get("status") != "OK":
        raise RuntimeError(f"CF API {method} 실패: {data.get('comment', data)}")
    return data["result"]


def parse_contest_id(arg):
    """'2259' / URL / '.../contest/2259/...' 어느 꼴이든 대회 ID(정수)만 뽑는다."""
    m = re.search(r"(\d+)", arg)
    if not m:
        raise ValueError(f"대회 ID를 못 읽음: {arg!r}")
    return int(m.group(1))


# ── 데이터 수집 ───────────────────────────────────────────────────────────────


def load_contest(contest_id):
    """contest.standings(bare)에서 대회 메타 + 문제 목록.
    ⚠ contestId 외 파라미터를 붙이면 FAILED — bare로만."""
    result = cf_get("contest.standings", contestId=contest_id)
    contest = result["contest"]
    problems = [{"index": p["index"], "name": p["name"]} for p in result["problems"]]
    if not problems:
        raise RuntimeError(
            f"대회 {contest_id}에 문제가 없음 — 대회가 아직 시작 안 됐을 수 있음"
        )
    return contest, problems


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


# ── 문제별 성적 계산 ──────────────────────────────────────────────────────────


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
        in_contest = [
            s
            for s in subs
            if s["author"]["participantType"] == "CONTESTANT"
            and s["relativeTimeSeconds"] <= duration_seconds
        ]
        in_contest.sort(key=lambda s: s["relativeTimeSeconds"])

        ac = next((s for s in in_contest if s["verdict"] == "OK"), None)

        if ac:
            ac_rel = ac["relativeTimeSeconds"]
            # AC 이전 오답 중 passedTestCount >= 1 인 것만 페널티(+10씩).
            # 샘플/1번 테스트도 못 넘긴 오답·컴파일 에러(passed==0)는 제외.
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
            continue

        solved_anywhere = any(s["verdict"] == "OK" for s in subs)
        if solved_anywhere:
            by_index[idx] = {"result": "업솔빙"}
        elif subs:
            by_index[idx] = {"result": "미해결"}
        else:
            by_index[idx] = {"result": "미시도"}
    return by_index


def compute_penalty(by_index):
    return sum(v["problem_penalty"] for v in by_index.values() if v["result"] == "AC")


# ── 포맷 헬퍼 ─────────────────────────────────────────────────────────────────


def fmt_mmss(rel_seconds):
    """relativeTimeSeconds -> 'MM:SS' (분은 60 넘어갈 수 있음: 104:54)."""
    return f"{rel_seconds // 60}:{rel_seconds % 60:02d}"


def fmt_index_set(indices):
    """['A','B','C','D'] -> 'A–D', 연속 아니면 'A, C, E'. 한 개면 그대로."""
    if not indices:
        return None
    if len(indices) == 1:
        return indices[0]
    if all(len(x) == 1 and x.isalpha() for x in indices):
        codes = [ord(x) for x in indices]
        if codes == list(range(codes[0], codes[0] + len(codes))):
            return f"{indices[0]}–{indices[-1]}"  # en dash
    return ", ".join(indices)


def rank_of(rating):
    name, hex_ = RANK_TIERS[0][1], RANK_TIERS[0][2]
    for lo, n, h in RANK_TIERS:
        if rating >= lo:
            name, hex_ = n, h
    return name, hex_


def rating_span(rating):
    name, hex_ = rank_of(rating)
    return f'<span style="color:{hex_}">{name}</span>'


def signed(n):
    return f"+{n}" if n >= 0 else str(n)


def has_solution_post(contest_id, index):
    """_posts/codeforces/에 slug == codeforces-{cid}{index} 인 포스트가 실재하는가."""
    if not os.path.isdir(CODEFORCES_POSTS_DIR):
        return False
    want = f"codeforces-{contest_id}{index}".lower()
    for fname in os.listdir(CODEFORCES_POSTS_DIR):
        if not fname.endswith(".md"):
            continue
        with open(os.path.join(CODEFORCES_POSTS_DIR, fname), encoding="utf-8") as f:
            text = f.read()
        fm = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        if fm and re.search(
            rf"^slug:\s*{re.escape(want)}\s*$", fm.group(1), re.MULTILINE
        ):
            return True
    return False


# ── 프리뷰 카드 ───────────────────────────────────────────────────────────────


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
    solved = sum(1 for v in by_index.values() if v["result"] == "AC")
    data = {
        "name": contest["name"],
        "date": f"{start_kst:%Y.%m.%d}",
        "solved": solved,
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
        old = mine["oldRating"] or 100
        data["delta"] = mine["newRating"] - old
    return data


def make_card(data, assets_dir):
    """카드 PNG 생성. 성공하면 경로, Chrome 없음/렌더 실패면 None(경고만 — 스캐폴드는 계속)."""
    out = os.path.join(assets_dir, CARD_NAME)
    try:
        render_card(data, out)
    except ChromeNotFound as e:
        print(f"  ⚠ 프리뷰 카드 생략: {e}", file=sys.stderr)
        return None
    except Exception as e:  # subprocess 실패·타임아웃 등
        print(f"  ⚠ 프리뷰 카드 렌더 실패: {e}", file=sys.stderr)
        return None
    return out


def find_post_by_slug(slug):
    """_drafts/contest/ → _posts/contest/ 순으로 front matter slug가 일치하는 후기 파일."""
    for d in (CONTEST_DRAFTS_DIR, os.path.join(REPO_ROOT, "_posts", "contest")):
        if not os.path.isdir(d):
            continue
        for fname in sorted(os.listdir(d)):
            if not fname.endswith(".md"):
                continue
            path = os.path.join(d, fname)
            with open(path, encoding="utf-8") as f:
                text = f.read()
            fm = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
            if fm and re.search(
                rf"^slug:\s*{re.escape(slug)}\s*$", fm.group(1), re.MULTILINE
            ):
                return path
    return None


def ensure_image_front_matter(post_path):
    """front matter에 image 블록이 없으면 media_subpath 줄 뒤에 넣는다. 넣었으면 True."""
    with open(post_path, encoding="utf-8") as f:
        text = f.read()
    fm = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not fm or re.search(r"^image:", fm.group(1), re.MULTILINE):
        return False
    block = "\n".join(image_front_matter())
    new_fm = re.sub(
        r"^(media_subpath:.*)$",
        lambda m: f"{m.group(1)}\n{block}",
        fm.group(1),
        count=1,
        flags=re.MULTILINE,
    )
    if new_fm == fm.group(1):
        return False
    with open(post_path, "w", encoding="utf-8") as f:
        f.write(f"---\n{new_fm}\n---\n" + text[fm.end() :])
    return True


def card_only(contest_id):
    """기존 후기(드래프트·발행본)의 프리뷰 카드만 (재)생성하고 front matter에 image를 보장.
    서술·코드는 안 건드림 — 과거 후기 소급·디자인 변경 후 재생성용."""
    contest, problems = load_contest(contest_id)
    rank_count, mine = load_rating_change(contest_id)
    submissions = load_submissions(contest_id)
    start_kst = datetime.fromtimestamp(
        contest["startTimeSeconds"], tz=timezone.utc
    ).astimezone(KST)
    by_index = classify_problems(problems, submissions, contest["durationSeconds"])
    penalty = compute_penalty(by_index)

    slug = f"codeforces-{contest_id}"
    post = find_post_by_slug(slug)
    if not post:
        raise FileNotFoundError(
            f"slug {slug} 후기를 _drafts/contest·_posts/contest에서 못 찾음"
        )
    assets_dir = os.path.join(REPO_ROOT, "assets", "img", "posts", slug)
    data = build_card_data(
        contest, start_kst, problems, by_index, penalty, rank_count, mine
    )
    out = make_card(data, assets_dir)
    if not out:
        raise RuntimeError("카드 생성 실패")
    added = ensure_image_front_matter(post)
    print(
        f"[contest] 카드 생성: {out}  front matter image: {'추가' if added else '이미 있음'}",
        file=sys.stderr,
    )
    return post


# ── 본문 조립 ─────────────────────────────────────────────────────────────────


def image_front_matter():
    """Chirpy 프리뷰 이미지 블록. path는 media_subpath 기준 상대경로.
    ⚠ `alt`는 넣지 않는다 — Chirpy(post.html)가 alt를 이미지 밑 눈에 보이는 캡션으로
    출력해서, 카드 안 제목과 같은 글이 한 번 더 나온다."""
    return ["image:", f"  path: {CARD_NAME}"]


def build_front_matter(contest, start_kst, slug, tags, has_card=False):
    tag_list = ", ".join(f'"{t}"' for t in tags)
    lines = [
        "---",
        f'title: "{yaml_dq(contest["name"])} 후기"',
        f"date: {start_kst:%Y-%m-%d}",
        "categories: [Contest]",
        f"tags: [{tag_list}]",
        f"slug: {slug}",
        f"media_subpath: /assets/img/posts/{slug}/",
        *(image_front_matter() if has_card else []),
        "math: true",
        "mermaid: false",
        "---",
    ]
    return "\n".join(lines)


def build_overview(contest, problems, start_kst, participation):
    first, last = problems[0]["index"], problems[-1]["index"]
    rows = [
        ("대회", contest["name"]),
        ("일시", f"{start_kst:%Y-%m-%d %H:%M} KST"),
        ("배정 시간", f"{contest['durationSeconds'] // 60}분"),
        ("문제 수", f"{len(problems)} ({first}–{last})"),
        ("참가 형태", participation),
    ]
    body = ["## 1. 대회 개요", "", "| 항목 | 내용 |", "| --- | --- |"]
    body += [f"| {k} | {v} |" for k, v in rows]
    return "\n".join(body)


def build_result(by_index, problems, total_problems, penalty, rank_count, mine):
    in_ac = [p["index"] for p in problems if by_index[p["index"]]["result"] == "AC"]
    post_ac = [
        p["index"] for p in problems if by_index[p["index"]]["result"] == "업솔빙"
    ]

    if in_ac:
        solved = f"대회 중 {fmt_index_set(in_ac)} ({len(in_ac)}/{total_problems})"
    else:
        solved = f"대회 중 없음 (0/{total_problems})"
    if post_ac:
        solved += f", 이후 {fmt_index_set(post_ac)} 업솔빙"

    if mine:
        rank = mine["rank"]
        pct = round(rank / rank_count * 100, 1) if rank_count else 0
        rank_cell = f"{rank} / {rank_count}위 · 상위 {pct}%"

        old, new = mine["oldRating"], mine["newRating"]
        if old == 0:  # 첫 대회 센티넬 — CF /ratings 페이지는 100 → new 로 표시
            rating_cell = (
                f"100 → {new} ({signed(new - 100)}, 첫 대회) · {rating_span(new)}"
            )
        else:
            rating_cell = f"{old} → {new} ({signed(new - old)}) · {rating_span(new)}"
    else:
        rank_cell = "<!-- ratingChanges 미반영 — 확정 후 수동 -->"
        rating_cell = "<!-- ratingChanges 미반영 — 확정 후 수동 -->"

    rows = [
        ("푼 문제", solved),
        ("페널티", f"{penalty}분"),
        ("순위", rank_cell),
        ("레이팅", rating_cell),
    ]
    body = ["## 2. 결과", "", "| 항목 | 내용 |", "| --- | --- |"]
    body += [f"| {k} | {v} |" for k, v in rows]
    body += ["", "![레이팅 그래프](rating-graph.png)"]
    return "\n".join(body)


def build_progress_table(by_index, problems, contest_id):
    body = [
        "## 3. 풀이 과정",
        "",
        "| 문제 | 결과 | 제출 시각 | WA |",
        "| --- | --- | --- | --- |",
    ]
    for p in problems:
        idx, name = p["index"], p["name"]
        info = by_index[idx]
        link = f"[{idx}. {name}](https://codeforces.com/problemset/problem/{contest_id}/{idx})"
        if info["result"] == "AC":
            when = fmt_mmss(info["ac_rel"])
            wa = str(info["penalty_wrong"])
        else:
            when = wa = "—"
        body.append(f"| {link} | {info['result']} | {when} | {wa} |")
    return "\n".join(body)


def build_problem_subsection(by_index, p, contest_id):
    idx, name = p["index"], p["name"]
    result = by_index[idx]["result"]
    head = f"### {idx}. {name}"

    if result == "미시도":
        return f"{head}\n\n대회 중 미시도."

    parts = [
        head,
        "",
        "```c++",
        "// 라이브 코드",
        "```",
    ]
    # AC·업솔빙은 어차피 나중에 풀이 포스트를 만들 것이므로 실재 여부를 안 따지고
    # 무조건 링크를 단다(대회 직후엔 아직 _drafts/에도 없는 게 정상). 미해결은
    # 포스트가 생길 보장이 없으니 실재할 때만(has_solution_post) 예외적으로 단다.
    if result in ("AC", "업솔빙") or has_solution_post(contest_id, idx):
        num = f"{contest_id}{idx}"  # 텍스트: 대문자 인덱스
        post_slug = f"codeforces-{contest_id}{idx}".lower()  # URL 슬러그: 소문자
        parts += [
            "",
            "<!-- prettier-ignore -->",
            f"> 풀이 → [[Codeforces] #{num} - {name}](/posts/{post_slug}/)",
            "{: .prompt-tip }",
        ]
    return "\n".join(parts)


def build_summary_section():
    return "## 총평"


def build_body(
    contest,
    contest_id,
    problems,
    by_index,
    start_kst,
    participation,
    penalty,
    rank_count,
    mine,
):
    preamble = "\n".join(
        [
            "<!-- prettier-ignore -->",
            f"> [대회 링크](https://codeforces.com/contest/{contest_id})",
            "{: .prompt-info }",
        ]
    )

    sections = [
        build_overview(contest, problems, start_kst, participation),
        build_result(by_index, problems, len(problems), penalty, rank_count, mine),
        build_progress_table(by_index, problems, contest_id),
    ]
    sections += [build_problem_subsection(by_index, p, contest_id) for p in problems]
    sections.append(build_summary_section())

    # 구분선 소유권: 각 섹션이 자기 앞의 "---"를 소유. 맨 끝 "---"는 문서 끝 마커(독립).
    return "\n\n".join([preamble] + [f"---\n\n{s}" for s in sections] + ["---"])


# ── 엔트리포인트 ──────────────────────────────────────────────────────────────


def determine_participation(mine, submissions):
    """rated 응시 여부(`mine`, load_rating_change의 반환값)와 제출 로그로 참가 형태
    문자열을 판정한다. rated 성적이 있으면 확정 공식 참가고, 없으면 제출 로그의
    participantType으로 오픈/가상 참가를 구분한다 — 셋 다 아니면(제출이 전혀 없거나
    참관만 함) rated 성적 없는 기본값으로 공식 참가 처리."""
    if mine:
        return "공식 (rated)"
    if any(s["author"]["participantType"] == "CONTESTANT" for s in submissions):
        return "오픈 (공식 시간, unrated)"
    if any(s["author"]["participantType"] == "VIRTUAL" for s in submissions):
        return "가상 (virtual, unrated)"
    return "공식 (rated)"


def determine_div_tags(contest_name):
    """대회명에서 디비전 태그를 뽑는다. "(Div. N)" 또는 Educational 라운드의
    "(Rated for Div. N)" 정확 매칭만 — 둘 다 디비전이 명확한 단일 값이라 안전.
    "(Div. 1 + Div. 2)"류 통합 라운드·Global/Hello 등 비표준 라운드명은 매칭 안 되므로
    태그 없이 두고 사람이 추가."""
    tags = ["codeforces"]
    m = re.search(r"\((?:Rated for )?Div\.\s*(\d+)\)", contest_name)
    if m:
        tags.append(f"div {m.group(1)}")
    return tags


def scaffold(contest_id, force):
    contest, problems = load_contest(contest_id)
    rank_count, mine = load_rating_change(contest_id)
    submissions = load_submissions(contest_id)

    start_kst = datetime.fromtimestamp(
        contest["startTimeSeconds"], tz=timezone.utc
    ).astimezone(KST)

    by_index = classify_problems(problems, submissions, contest["durationSeconds"])
    penalty = compute_penalty(by_index)

    participation = determine_participation(mine, submissions)
    tags = determine_div_tags(contest["name"])

    slug = f"codeforces-{contest_id}"
    filename = f"{start_kst:%Y-%m-%d}-{sanitize_filename(contest['name'])}.md"
    target = os.path.join(CONTEST_DRAFTS_DIR, filename)

    if os.path.exists(target) and not force:
        raise FileExistsError(
            f"이미 파일이 있음(사람이 서술·라이브 코드를 채웠을 수 있어 임의로 덮어쓰지 않음): "
            f"{target}\n다시 생성하려면 --force."
        )

    # 레이팅 그래프는 매 후기 100% 들어가므로(`## 2. 결과` 표 아래 `rating-graph.png`
    # 참조가 build_result에서 무조건 박힘) 스캐폴드 시점에 자리를 미리 만들어둔다 —
    # 사람이 DevTools 스크린샷을 이 폴더에 바로 떨어뜨릴 수 있게. 이미 있으면(재생성
    # 시 기존 스크린샷) 손대지 않음.
    assets_dir = os.path.join(REPO_ROOT, "assets", "img", "posts", slug)
    os.makedirs(assets_dir, exist_ok=True)

    # 카드는 부가 기능 — 데이터 조회(user.rating API)·렌더 어느 쪽이 실패해도 스켈레톤은
    # 살린다(--card-only는 명시 요청이라 예외를 그대로 올림).
    card = None
    try:
        card_data = build_card_data(
            contest, start_kst, problems, by_index, penalty, rank_count, mine
        )
    except Exception as e:
        print(f"  ⚠ 프리뷰 카드 생략(레이팅 이력 조회 실패): {e}", file=sys.stderr)
    else:
        card = make_card(card_data, assets_dir)

    front_matter = build_front_matter(
        contest, start_kst, slug, tags, has_card=bool(card)
    )
    body = build_body(
        contest,
        contest_id,
        problems,
        by_index,
        start_kst,
        participation,
        penalty,
        rank_count,
        mine,
    )

    os.makedirs(CONTEST_DRAFTS_DIR, exist_ok=True)
    with open(target, "w", encoding="utf-8") as f:
        f.write(front_matter)
        f.write("\n\n")
        f.write(body)
        f.write("\n")

    # stderr 요약 — 눈 대조용(순위·레이팅은 CF 페이지끼리도 다르므로).
    ac = [i for i, v in by_index.items() if v["result"] == "AC"]
    up = [i for i, v in by_index.items() if v["result"] == "업솔빙"]
    print(f"[contest] {contest['name']} (id {contest_id})", file=sys.stderr)
    print(
        f"  대회 중 AC: {', '.join(ac) or '없음'} / 업솔빙: {', '.join(up) or '없음'}",
        file=sys.stderr,
    )
    print(f"  페널티(계산): {penalty}분", file=sys.stderr)
    if mine:
        old = mine["oldRating"]
        old_disp = 100 if old == 0 else old
        print(
            f"  순위: {mine['rank']} / {rank_count}  레이팅: {old_disp} → {mine['newRating']}"
            f"{' (첫 대회)' if old == 0 else ''}",
            file=sys.stderr,
        )
    else:
        print(
            "  ratingChanges에 핸들 없음 — 순위·레이팅 placeholder로 남김",
            file=sys.stderr,
        )
    print(
        f"  ⚠ 발행 전 /contest/{contest_id}/standings 페이지에서 페널티·순위 눈 대조",
        file=sys.stderr,
    )
    print(f"  레이팅 그래프 자리: {assets_dir}/rating-graph.png", file=sys.stderr)
    if card:
        print(f"  프리뷰 카드: {card}", file=sys.stderr)

    return target


def main():
    argv = sys.argv[1:]
    force = "--force" in argv
    only_card = "--card-only" in argv
    positional = [a for a in argv if a not in ("--force", "--card-only")]
    if len(positional) != 1:
        print(__doc__)
        sys.exit(1)

    contest_id = parse_contest_id(positional[0])
    target = card_only(contest_id) if only_card else scaffold(contest_id, force)
    print(target)


if __name__ == "__main__":
    main()
