"""
대회 후기의 front matter + 본문 스켈레톤 조립 — 순수 함수(네트워크·파일 I/O 없음).
데이터 수집은 `cf_contest.py`, 파일 쓰기는 `scaffold_contest.py`.

**후기 '양식'(섹션 구성·표 컬럼·어휘)은 `contest/SKILL.md`가 정본, 설계 근거 전체는
프로젝트 메모리 `contest-recap-post-format.md`.** 여기엔 옆 코드만 봐선 안 보이는 '왜'만:

- **"---" 구분선 소유권**: `ps`의 `scaffold_post.py`와 똑같이 항상 "뒤 섹션이 자기 앞에
  다는 것"(섹션 사이 접착제 아님). `## 3. 풀이 과정` 안의 각 `### {index}` 서브섹션도
  하나의 섹션으로 취급해 자기 앞에 단다. 맨 끝 "---"는 어느 섹션에도 안 딸린 문서 끝 마커.
- **등급 색**(`RANK_TIERS`)은 2026-09-07 CF `community.css` 실측. legendary grandmaster
  (3000+)의 "첫 글자 검정"은 미구현(이 핸들이 도달할 일이 수년간 없음).
- **스켈레톤이 남기는 미완 표식**(`LIVE_CODE_PLACEHOLDER`·`RATING_PLACEHOLDER`)은
  `publish_contest.py`의 완료 게이트가 그대로 검사한다 — 문구를 바꾸면 게이트도 같은 상수를 쓴다.
"""

import re

from blog_common import (
    yaml_dq,  # contest_common이 먼저 import돼 sys.path에 _shared가 들어간 뒤여야 함
)
from contest_common import CARD_NAME, CODEFORCES_POSTS_DIR, find_posts_by_slug

LIVE_CODE_PLACEHOLDER = "// 라이브 코드"
RATING_PLACEHOLDER = "<!-- ratingChanges 미반영 — 확정 후 수동 -->"

# (하한 레이팅, 등급명, hex) — rating >= 하한인 마지막 튜플이 그 등급.
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


# ── 포맷 헬퍼 ─────────────────────────────────────────────────────────────────


def fmt_mmss(rel_seconds):
    """relativeTimeSeconds -> 'MM:SS' (분은 60 넘어갈 수 있음: 104:54)."""
    return f"{rel_seconds // 60}:{rel_seconds % 60:02d}"


def fmt_index_set(indices):
    """['A','B','C','D'] -> 'A–D', 연속 아니면 'A, C, E'. 한 개면 그대로."""
    if len(indices) == 1:
        return indices[0]
    if all(len(x) == 1 and x.isalpha() for x in indices):
        codes = [ord(x) for x in indices]
        if codes == list(range(codes[0], codes[0] + len(codes))):
            return f"{indices[0]}–{indices[-1]}"  # en dash
    return ", ".join(indices)


def rating_span(rating):
    _, name, hex_ = [t for t in RANK_TIERS if rating >= t[0]][-1]
    return f'<span style="color:{hex_}">{name}</span>'


def signed(n):
    return f"+{n}" if n >= 0 else str(n)


def determine_div_tags(contest_name):
    """대회명에서 디비전 태그를 뽑는다. "(Div. N)" 또는 Educational 라운드의
    "(Rated for Div. N)" 정확 매칭만. "(Div. 1 + Div. 2)"류 통합 라운드·Global/Hello 등
    비표준 라운드명은 매칭 안 되므로 태그 없이 두고 사람이 추가."""
    tags = ["codeforces"]
    m = re.search(r"\((?:Rated for )?Div\.\s*(\d+)\)", contest_name)
    if m:
        tags.append(f"div {m.group(1)}")
    return tags


def has_solution_post(contest_id, index):
    """_posts/codeforces/에 slug == codeforces-{cid}{index} 인 포스트가 실재하는가."""
    slug = f"codeforces-{contest_id}{index}".lower()
    return bool(find_posts_by_slug(slug, [CODEFORCES_POSTS_DIR]))


# ── front matter ──────────────────────────────────────────────────────────────


def image_front_matter():
    """Chirpy 프리뷰 이미지 블록. path는 media_subpath 기준 상대경로.
    ⚠ `alt`는 넣지 않는다 — Chirpy(post.html)가 alt를 이미지 밑 눈에 보이는 캡션으로
    출력해서, 카드 안 제목과 같은 글이 한 번 더 나온다."""
    return ["image:", f"  path: {CARD_NAME}"]


def build_front_matter(contest, start_kst, slug, tags, has_card=False):
    tag_list = ", ".join(f'"{t}"' for t in tags)
    title = yaml_dq(contest["name"])
    lines = [
        "---",
        f'title: "{title} 후기"',
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


# ── 본문 ──────────────────────────────────────────────────────────────────────


def _table(title, rows):
    return "\n".join(
        [title, "", "| 항목 | 내용 |", "| --- | --- |"]
        + [f"| {k} | {v} |" for k, v in rows]
    )


def build_overview(contest, problems, start_kst, participation):
    first, last = problems[0]["index"], problems[-1]["index"]
    return _table(
        "## 1. 대회 개요",
        [
            ("대회", contest["name"]),
            ("일시", f"{start_kst:%Y-%m-%d %H:%M} KST"),
            ("배정 시간", f"{contest['durationSeconds'] // 60}분"),
            ("문제 수", f"{len(problems)} ({first}–{last})"),
            ("참가 형태", participation),
        ],
    )


def build_result(by_index, problems, penalty, rank_count, mine):
    in_ac = [p["index"] for p in problems if by_index[p["index"]]["result"] == "AC"]
    post_ac = [
        p["index"] for p in problems if by_index[p["index"]]["result"] == "업솔빙"
    ]

    if in_ac:
        solved = f"대회 중 {fmt_index_set(in_ac)} ({len(in_ac)}/{len(problems)})"
    else:
        solved = f"대회 중 없음 (0/{len(problems)})"
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
        rank_cell = rating_cell = RATING_PLACEHOLDER

    table = _table(
        "## 2. 결과",
        [
            ("푼 문제", solved),
            ("페널티", f"{penalty}분"),
            ("순위", rank_cell),
            ("레이팅", rating_cell),
        ],
    )
    return f"{table}\n\n![레이팅 그래프](rating-graph.png)"


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
            when, wa = fmt_mmss(info["ac_rel"]), str(info["penalty_wrong"])
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

    parts = [head, "", "```c++", LIVE_CODE_PLACEHOLDER, "```"]
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
        build_result(by_index, problems, penalty, rank_count, mine),
        build_progress_table(by_index, problems, contest_id),
        *[build_problem_subsection(by_index, p, contest_id) for p in problems],
        "## 총평",
    ]
    return "\n\n".join([preamble] + [f"---\n\n{s}" for s in sections] + ["---"])
