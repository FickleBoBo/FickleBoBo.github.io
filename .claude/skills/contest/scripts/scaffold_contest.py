"""
Codeforces 대회 ID(또는 URL)로 대회 후기 드래프트(`_drafts/contest/`)와 프리뷰 카드를 생성한다.
LLM 판단 없음 — CF 조회·계산·문자열 조립만이고, 이 파일은 오케스트레이션·CLI다. 양식과 동작은
`contest/SKILL.md`가 정본. `_drafts/contest/`는 `repo.PLATFORM_DIRS`에 없어서 `sync`·`review-*`·
`publish`가 통째로 무시한다(의도된 안전장치).

사용법:
    python3 scaffold_contest.py <대회 ID 또는 URL> [--force | --card-only]

성공하면 stdout엔 쓴 파일의 절대경로만, stderr엔 페널티·순위 요약(눈 대조용)을 낸다.
"""

import os
import re
import sys
from datetime import UTC, datetime, timedelta, timezone

# 아래 import(contest_common·cf_contest 포함)가 `_shared`를 찾도록 먼저 sys.path에 넣는다.
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "_shared"))
)

from cf_contest import (
    build_card_data,
    classify_problems,
    compute_penalty,
    determine_participation,
    load_contest,
    load_rating_change,
    load_submissions,
)
from contest_common import (
    CARD_NAME,
    CONTEST_DRAFTS_DIR,
    CONTEST_POSTS_DIR,
    find_posts_by_slug,
    parse_contest_id,
)
from post_text import front_matter_block
from recap_body import (
    build_body,
    build_front_matter,
    determine_div_tags,
    image_front_matter,
)
from render_card import render_card
from repo import REPO_ROOT, sanitize_filename

KST = timezone(timedelta(hours=9))


def fetch_contest_data(contest_id):
    """스캐폴드·카드 재생성이 공유하는 조회·계산 묶음."""
    contest, problems = load_contest(contest_id)
    rank_count, mine = load_rating_change(contest_id)
    submissions = load_submissions(contest_id)
    start_kst = datetime.fromtimestamp(contest["startTimeSeconds"], tz=UTC).astimezone(
        KST
    )
    by_index = classify_problems(problems, submissions, contest["durationSeconds"])
    return {
        "contest": contest,
        "problems": problems,
        "rank_count": rank_count,
        "mine": mine,
        "submissions": submissions,
        "start_kst": start_kst,
        "by_index": by_index,
        "penalty": compute_penalty(by_index),
    }


def card_data_from(data):
    return build_card_data(
        data["contest"],
        data["start_kst"],
        data["problems"],
        data["by_index"],
        data["penalty"],
        data["rank_count"],
        data["mine"],
    )


def make_card(card_data, assets_dir):
    """카드 PNG 생성. 성공하면 경로, Chrome 없음/렌더 실패면 None(경고만 — 스캐폴드는 계속)."""
    out = os.path.join(assets_dir, CARD_NAME)
    try:
        render_card(card_data, out)
    except Exception as e:  # Chrome 없음, subprocess 실패·타임아웃 등
        print(f"  ⚠ 프리뷰 카드 생략: {e}", file=sys.stderr)
        return None
    return out


def ensure_image_front_matter(post_path):
    """front matter에 image 블록이 없으면 media_subpath 줄 뒤에 넣는다. 넣었으면 True."""
    with open(post_path, encoding="utf-8") as f:
        text = f.read()
    fm = front_matter_block(text)
    if re.search(r"^image:", fm, re.MULTILINE):
        return False
    block = "\n".join(image_front_matter())
    new_fm = re.sub(
        r"^(media_subpath:.*)$",
        lambda m: f"{m.group(1)}\n{block}",
        fm,
        count=1,
        flags=re.MULTILINE,
    )
    if new_fm == fm:
        return False
    with open(post_path, "w", encoding="utf-8") as f:
        f.write(text.replace(fm, new_fm, 1))
    return True


def card_only(contest_id):
    """기존 후기(드래프트·발행본)의 프리뷰 카드만 (재)생성하고 front matter에 image를 보장."""
    slug = f"codeforces-{contest_id}"
    posts = find_posts_by_slug(slug, [CONTEST_DRAFTS_DIR, CONTEST_POSTS_DIR])
    if not posts:
        raise FileNotFoundError(
            f"slug {slug} 후기를 _drafts/contest·_posts/contest에서 못 찾음"
        )
    data = fetch_contest_data(contest_id)
    assets_dir = os.path.join(REPO_ROOT, "assets", "img", "posts", slug)
    out = make_card(card_data_from(data), assets_dir)
    if not out:
        raise RuntimeError("카드 생성 실패")
    added = ensure_image_front_matter(posts[0])
    print(
        f"[contest] 카드 생성: {out}  front matter image: {'추가' if added else '이미 있음'}",
        file=sys.stderr,
    )
    return posts[0]


def print_summary(contest_id, data, assets_dir, card):
    """stderr 요약 — 눈 대조용(순위·레이팅은 CF 페이지끼리도 다르므로)."""
    by_index, mine = data["by_index"], data["mine"]
    ac = [i for i, v in by_index.items() if v["result"] == "AC"]
    up = [i for i, v in by_index.items() if v["result"] == "업솔빙"]

    def out(msg):
        print(msg, file=sys.stderr)

    out(f"[contest] {data['contest']['name']} (id {contest_id})")
    out(f"  대회 중 AC: {', '.join(ac) or '없음'} / 업솔빙: {', '.join(up) or '없음'}")
    out(f"  페널티(계산): {data['penalty']}분")
    if mine:
        old = mine["oldRating"]
        out(
            f"  순위: {mine['rank']} / {data['rank_count']}  레이팅: {old or 100} → {mine['newRating']}"
            f"{' (첫 대회)' if old == 0 else ''}"
        )
    else:
        out("  ratingChanges에 핸들 없음 — 순위·레이팅 placeholder로 남김")
    out(f"  ⚠ 발행 전 /contest/{contest_id}/standings 페이지에서 페널티·순위 눈 대조")
    out(f"  레이팅 그래프 자리: {assets_dir}/rating-graph.png")
    if card:
        out(f"  프리뷰 카드: {card}")


def scaffold(contest_id, force):
    data = fetch_contest_data(contest_id)
    contest, start_kst = data["contest"], data["start_kst"]

    slug = f"codeforces-{contest_id}"
    filename = f"{start_kst:%Y-%m-%d}-{sanitize_filename(contest['name'])}.md"
    target = os.path.join(CONTEST_DRAFTS_DIR, filename)
    if os.path.exists(target) and not force:
        raise FileExistsError(
            f"이미 파일이 있음(사람이 서술·라이브 코드를 채웠을 수 있어 임의로 덮어쓰지 않음): "
            f"{target}\n다시 생성하려면 --force."
        )

    # 본문이 항상 rating-graph.png를 참조하므로 스크린샷을 떨어뜨릴 폴더를 미리 만든다.
    assets_dir = os.path.join(REPO_ROOT, "assets", "img", "posts", slug)
    os.makedirs(assets_dir, exist_ok=True)

    # 카드는 부가 기능 — 조회·렌더가 실패해도 스켈레톤은 살린다(--card-only는 예외를 그대로 올림).
    card = None
    try:
        card_data = card_data_from(data)
    except Exception as e:
        print(f"  ⚠ 프리뷰 카드 생략(레이팅 이력 조회 실패): {e}", file=sys.stderr)
    else:
        card = make_card(card_data, assets_dir)

    front_matter = build_front_matter(
        contest,
        start_kst,
        slug,
        determine_div_tags(contest["name"]),
        has_card=bool(card),
    )
    body = build_body(
        contest,
        contest_id,
        data["problems"],
        data["by_index"],
        start_kst,
        determine_participation(data["mine"], data["submissions"]),
        data["penalty"],
        data["rank_count"],
        data["mine"],
    )

    os.makedirs(CONTEST_DRAFTS_DIR, exist_ok=True)
    with open(target, "w", encoding="utf-8") as f:
        f.write(f"{front_matter}\n\n{body}\n")

    print_summary(contest_id, data, assets_dir, card)
    return target


def main():
    argv = sys.argv[1:]
    force = "--force" in argv
    only_card = "--card-only" in argv
    positional = [a for a in argv if a not in ("--force", "--card-only")]
    if len(positional) != 1:
        print(__doc__, file=sys.stderr)
        sys.exit(2)

    contest_id = parse_contest_id(positional[0])
    print(card_only(contest_id) if only_card else scaffold(contest_id, force))


if __name__ == "__main__":
    main()
