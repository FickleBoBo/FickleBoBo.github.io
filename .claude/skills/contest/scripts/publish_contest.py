"""
대회 후기 드래프트 하나(`_drafts/contest/{파일}.md`)를 `_posts/contest/`로 옮기고, 이 블로그
레포 + PS 레포(형제 디렉토리) 양쪽에 각각 커밋한다. push는 안 함. `publish` 스킬과 같은
"옮긴 뒤 레포별로 각각 커밋" 흐름이고, 후기 장르라 갈라지는 부분만 다르다:

- **완료 게이트가 다르다.** 후기엔 `## 1. 아이디어`·복잡도 표가 없다. 대신 스캐폴드가 남기는
  미완 표식(라이브 코드 자리·ratingChanges 자리·레이팅 그래프 이미지)과 `## 총평`이 채워졌는지
  검사한다(`not_ready_reason`). 서술의 질은 사람 몫이라 검사 안 함.
- **PS 레포 소스가 1:N.** `publish`는 slug로 폴더 하나를 찾지만, 후기는 그 대회의 라이브 코드
  폴더 여러 개(`live_{contestId}{index}` — 대회날 `day_XX`에 문제별로)에 대응한다. 전부 같은
  메시지로 커밋한다.
- **커밋 메시지**: `feat: [Contest] {CF API 대회명} 후기`(블로그·PS 레포 동일). 대회명은 포스트
  `title`에서 그대로(front matter가 `"{대회명} 후기"`). 트레일러는 `commit`이 붙이는
  `Co-Authored-By: Claude <noreply@anthropic.com>`(모델명 없음 — 정적 스크립트라 커밋 시점
  모델 버전을 모름, 블로그 CLAUDE.md "트레일러 모델명 규칙").

코드를 고칠 때 알아야 할 것:
- PS 레포 쪽(`live_` 폴더) 검증을 블로그 레포를 건드리기 *전에* 한다 — `publish.py`와 같은
  이유. `live_` 폴더를 하나도 못 찾으면 아무것도 안 옮기고 에러.
- `os.rename` 이후부턴 실패해도 파일을 원래 자리로 안 되돌림 — 예외 메시지에 어디까지
  진행됐는지 명시.
- `live_` 패턴은 실제 관측된 레이아웃(`live_2259a`~`live_2259e`, 문제별)만 매칭한다
  (`_live_folder_re`). 대회 하나에 폴더 하나로 바뀌면 그 함수도 손볼 것.

사용법:
    python3 publish_contest.py <후기 .md 경로 또는 대회 ID/URL>
종료 코드: 발행하면 0, 미완료·에러면 1, 인자 오류면 2.
"""

import os
import re
import sys

from blog_common import (
    PS_REPO,
    REPO_ROOT,
    commit,
    extract_title,
    has_pending_changes,
    read_front_matter,
)
from contest_common import (
    CONTEST_DRAFTS_DIR,
    CONTEST_POSTS_DIR,
    find_posts_by_slug,
    parse_contest_id,
)
from recap_body import LIVE_CODE_PLACEHOLDER, RATING_PLACEHOLDER


def _live_folder_re(contest_id):
    """live_{contestId}{index}[...] — index는 알파벳 한 글자로 시작(live_22590 같은 다른 대회 오매칭 방지)."""
    return re.compile(rf"^live_{re.escape(contest_id)}[A-Za-z]\w*$")


def resolve_draft(arg):
    """후기 .md 경로 또는 대회 ID/URL → _drafts/contest/{파일} 절대경로."""
    abs_path = os.path.abspath(arg)
    if os.path.isfile(abs_path):
        if os.path.dirname(abs_path) != CONTEST_DRAFTS_DIR:
            raise ValueError(f"_drafts/contest/ 아래 있는 드래프트가 아님: {abs_path}")
        return abs_path

    # 경로처럼 생겼는데 파일이 없으면 경로 오타 — 아래 숫자 추출이 경로 속 날짜("2026") 등을
    # 대회 ID로 오인하지 않게 여기서 명확히 실패한다.
    if "/" in arg or arg.endswith(".md"):
        raise ValueError(f"후기 드래프트 파일을 찾을 수 없음: {abs_path}")

    slug = f"codeforces-{parse_contest_id(arg)}"
    matches = find_posts_by_slug(slug, [CONTEST_DRAFTS_DIR])
    if not matches:
        raise ValueError(f"_drafts/contest/에 slug={slug} 후기가 없음")
    if len(matches) > 1:
        raise ValueError(f"slug={slug} 후기가 여러 개: {matches}")
    return matches[0]


def discover_live_folders(contest_id):
    """PS 레포에서 그 대회의 live_{contestId}{index} 폴더 전부(경로순)."""
    if not os.path.isdir(PS_REPO):
        raise ValueError(f"PS 레포가 없음: {PS_REPO}")
    pat = _live_folder_re(contest_id)
    found = []
    for year_month in sorted(os.listdir(PS_REPO)):
        src = os.path.join(PS_REPO, year_month, "src")
        if not os.path.isdir(src):
            continue
        for day in sorted(os.listdir(src)):
            day_dir = os.path.join(src, day)
            if not os.path.isdir(day_dir):
                continue
            for entry in sorted(os.listdir(day_dir)):
                full = os.path.join(day_dir, entry)
                if pat.match(entry) and os.path.isdir(full):
                    found.append(full)
    return found


def not_ready_reason(text, slug):
    """발행 준비가 안 됐으면 사유 문자열, 됐으면 None."""
    if LIVE_CODE_PLACEHOLDER in text:
        return f"라이브 코드 자리(`{LIVE_CODE_PLACEHOLDER}`)가 남아 있음"
    if RATING_PLACEHOLDER in text:
        return "순위·레이팅 placeholder(ratingChanges 미반영)가 남아 있음"
    if "](rating-graph.png)" in text and not os.path.isfile(
        os.path.join(REPO_ROOT, "assets", "img", "posts", slug, "rating-graph.png")
    ):
        return "rating-graph.png가 없음(캡처해 넣거나 본문의 이미지 줄을 지울 것)"
    m = re.search(r"^## 총평\s*\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
    body = re.sub(r"<!--.*?-->", "", m.group(1) if m else "", flags=re.DOTALL)
    if not "\n".join(l for l in body.splitlines() if l.strip() != "---").strip():
        return "'## 총평'이 비어 있음"
    return None


def publish_one(draft_path):
    """후기 하나를 검증하고 발행한다. 미완료면 아무것도 안 건드리고 ValueError."""
    with open(draft_path, encoding="utf-8") as f:
        text = f.read()

    _date, slug = read_front_matter(text)
    if not slug.startswith("codeforces-"):
        raise ValueError(f"후기 slug 형식이 예상과 다름(codeforces-{{id}}): {slug}")
    contest_id = slug[len("codeforces-") :]

    reason = not_ready_reason(text, slug)
    if reason:
        raise ValueError(f"미완료 — {reason}")

    message = f"feat: [Contest] {extract_title(text)}"

    # 블로그 레포를 건드리기 전에 PS 레포 쪽부터 검증.
    live_folders = discover_live_folders(contest_id)
    if not live_folders:
        raise ValueError(
            f"PS 레포에서 live_{contest_id}* 폴더를 못 찾음 — 대회 ID를 확인하거나, "
            "이미 수동으로 처리했으면 `git mv`로 직접 옮길 것"
        )

    target_path = os.path.join(CONTEST_POSTS_DIR, os.path.basename(draft_path))
    if os.path.exists(target_path):
        raise ValueError(
            f"_posts/contest/에 이미 같은 이름의 파일이 있음: {target_path}"
        )

    os.makedirs(CONTEST_POSTS_DIR, exist_ok=True)
    os.rename(draft_path, target_path)  # 이 시점부턴 실패해도 파일은 이미 옮겨진 상태

    asset_dir = os.path.join(REPO_ROOT, "assets", "img", "posts", slug)
    blog_paths = [target_path] + ([asset_dir] if os.path.isdir(asset_dir) else [])

    try:
        blog_committed = has_pending_changes(REPO_ROOT, blog_paths)
        if blog_committed:
            commit(REPO_ROOT, blog_paths, message)
    except Exception as e:
        raise RuntimeError(
            f"파일은 이미 {target_path}로 이동됐지만 블로그 커밋 실패: {e} "
            "— 수동으로 git add/commit 필요"
        )

    try:
        ps_committed = has_pending_changes(PS_REPO, live_folders)
        if ps_committed:
            commit(PS_REPO, live_folders, message)
    except Exception as e:
        raise RuntimeError(
            f"블로그는 이미 커밋됨({target_path}), 하지만 PS 레포 커밋 실패: {e} "
            f"— PS 레포({', '.join(live_folders)})는 직접 확인 필요"
        )

    blog_note = "블로그 커밋함" if blog_committed else "블로그 이미 커밋된 상태"
    ps_note = (
        f"PS 레포 커밋함({len(live_folders)}개 live 폴더)"
        if ps_committed
        else "PS 레포 이미 커밋된 상태"
    )
    return f"발행함: {target_path} — {blog_note}, {ps_note}"


def main():
    if len(sys.argv) != 2:
        print(
            "사용법: python3 publish_contest.py <후기 .md 경로 또는 대회 ID/URL>",
            file=sys.stderr,
        )
        sys.exit(2)
    try:
        print(publish_one(resolve_draft(sys.argv[1])))
    except Exception as e:
        print(f"에러({sys.argv[1]}): {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
