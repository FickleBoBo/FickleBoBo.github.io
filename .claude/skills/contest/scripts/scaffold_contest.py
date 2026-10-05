"""
Codeforces 대회 ID(또는 URL)를 받아 대회 후기 드래프트(`_drafts/contest/`)를 생성한다.
LLM 판단 없음 — CF 조회·계산·문자열 조립만. `ps` 스킬과 평행 구조: 스크립트가 확정 가능한
것(front matter·대회 개요·결과 표·풀이 과정 표)을 전부 채우고, 문제별 서술·라이브 코드·
총평·수동 뉘앙스는 사람이 채운다.

역할별 모듈(이 파일은 오케스트레이션·CLI만):
- `cf_contest.py` — CF API 조회, 문제별 성적·페널티 계산
- `recap_body.py` — front matter·본문 조립(순수 함수)
- `render_card.py` — 프리뷰 카드 PNG 렌더(헤드리스 Chrome)
- `contest_common.py` — 경로 상수, slug로 후기 찾기

**후기 '양식'은 `contest/SKILL.md`가 정본, 설계 근거는 프로젝트 메모리
`contest-recap-post-format.md`.** 이 스크립트는 `_drafts/contest/`에만 쓴다 — 그 폴더는
`blog_common.PLATFORM_DIRS`에 없어서 `sync`·`review-*`·`publish`가 통째로 무시한다(의도된
안전장치). 발행은 `publish_contest.py`.

사용법:
    python3 scaffold_contest.py <대회 ID 또는 URL> [--force | --card-only]

    같은 이름 파일이 `_drafts/contest/`에 이미 있으면 거부(사람이 채운 서술·라이브 코드
    보호) — 재생성은 --force. 스켈레톤과 함께 프리뷰 카드를 렌더하고 front matter에
    `image:`를 넣는다(Chrome이 없으면 카드만 생략하고 계속). `--card-only`는 이미 있는
    후기(드래프트·발행본)의 카드만 (재)생성하고 image가 없으면 넣는다 — 서술·코드는 안 건드림.

    성공하면 stdout엔 쓴 파일의 절대경로만. stderr엔 페널티·순위 요약(눈 대조용).
"""

import os
import re
import sys
from datetime import datetime, timedelta, timezone

from blog_common import (  # contest_common 뒤(sys.path)
    REPO_ROOT,
    front_matter_block,
    sanitize_filename,
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
from recap_body import (
    build_body,
    build_front_matter,
    determine_div_tags,
    image_front_matter,
)
from render_card import ChromeNotFound, render_card

KST = timezone(timedelta(hours=9))


def load_all(contest_id):
    """스캐폴드·카드 재생성이 공유하는 조회·계산 묶음."""
    contest, problems = load_contest(contest_id)
    rank_count, mine = load_rating_change(contest_id)
    submissions = load_submissions(contest_id)
    start_kst = datetime.fromtimestamp(
        contest["startTimeSeconds"], tz=timezone.utc
    ).astimezone(KST)
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


def card_data_of(d):
    return build_card_data(
        d["contest"],
        d["start_kst"],
        d["problems"],
        d["by_index"],
        d["penalty"],
        d["rank_count"],
        d["mine"],
    )


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
    d = load_all(contest_id)
    assets_dir = os.path.join(REPO_ROOT, "assets", "img", "posts", slug)
    out = make_card(card_data_of(d), assets_dir)
    if not out:
        raise RuntimeError("카드 생성 실패")
    added = ensure_image_front_matter(posts[0])
    print(
        f"[contest] 카드 생성: {out}  front matter image: {'추가' if added else '이미 있음'}",
        file=sys.stderr,
    )
    return posts[0]


def print_summary(contest_id, d, assets_dir, card):
    """stderr 요약 — 눈 대조용(순위·레이팅은 CF 페이지끼리도 다르므로)."""
    by_index, mine = d["by_index"], d["mine"]
    ac = [i for i, v in by_index.items() if v["result"] == "AC"]
    up = [i for i, v in by_index.items() if v["result"] == "업솔빙"]
    out = lambda msg: print(msg, file=sys.stderr)
    out(f"[contest] {d['contest']['name']} (id {contest_id})")
    out(f"  대회 중 AC: {', '.join(ac) or '없음'} / 업솔빙: {', '.join(up) or '없음'}")
    out(f"  페널티(계산): {d['penalty']}분")
    if mine:
        old = mine["oldRating"]
        out(
            f"  순위: {mine['rank']} / {d['rank_count']}  레이팅: {old or 100} → {mine['newRating']}"
            f"{' (첫 대회)' if old == 0 else ''}"
        )
    else:
        out("  ratingChanges에 핸들 없음 — 순위·레이팅 placeholder로 남김")
    out(f"  ⚠ 발행 전 /contest/{contest_id}/standings 페이지에서 페널티·순위 눈 대조")
    out(f"  레이팅 그래프 자리: {assets_dir}/rating-graph.png")
    if card:
        out(f"  프리뷰 카드: {card}")


def scaffold(contest_id, force):
    d = load_all(contest_id)
    contest, start_kst = d["contest"], d["start_kst"]

    slug = f"codeforces-{contest_id}"
    filename = f"{start_kst:%Y-%m-%d}-{sanitize_filename(contest['name'])}.md"
    target = os.path.join(CONTEST_DRAFTS_DIR, filename)
    if os.path.exists(target) and not force:
        raise FileExistsError(
            f"이미 파일이 있음(사람이 서술·라이브 코드를 채웠을 수 있어 임의로 덮어쓰지 않음): "
            f"{target}\n다시 생성하려면 --force."
        )

    # 레이팅 그래프는 매 후기 100% 들어가므로(`## 2. 결과` 아래 `rating-graph.png` 참조가
    # 무조건 박힘) 자리를 미리 만들어 둔다 — DevTools 스크린샷을 바로 떨어뜨릴 수 있게.
    # 이미 있으면(재생성 시 기존 스크린샷) 손대지 않음.
    assets_dir = os.path.join(REPO_ROOT, "assets", "img", "posts", slug)
    os.makedirs(assets_dir, exist_ok=True)

    # 카드는 부가 기능 — 데이터 조회(user.rating API)·렌더 어느 쪽이 실패해도 스켈레톤은
    # 살린다(--card-only는 명시 요청이라 예외를 그대로 올림).
    card = None
    try:
        card_data = card_data_of(d)
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
        d["problems"],
        d["by_index"],
        start_kst,
        determine_participation(d["mine"], d["submissions"]),
        d["penalty"],
        d["rank_count"],
        d["mine"],
    )

    os.makedirs(CONTEST_DRAFTS_DIR, exist_ok=True)
    with open(target, "w", encoding="utf-8") as f:
        f.write(f"{front_matter}\n\n{body}\n")

    print_summary(contest_id, d, assets_dir, card)
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
