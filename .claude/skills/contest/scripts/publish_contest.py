"""
대회 후기 드래프트 하나(`_drafts/contest/{파일}.md`)를 `_posts/contest/`로 옮기고,
이 블로그 레포 + PS 레포(형제 디렉토리) 양쪽에 각각 커밋한다. push는 안 함 — 로컬
커밋까지만. `publish` 스킬(PS 포스트 발행)의 "옮긴 뒤 레포별로 각각 커밋" 흐름을
그대로 따르되, 대회 후기 장르에 맞게 갈라지는 부분만 다르다:

- **완료 게이트 없음.** `publish`는 `## 1. 아이디어`·`## 2. 복잡도`가 채워졌는지
  검사하지만, 후기엔 그런 구조가 없고 "됐다" 판단은 사람 몫이다. 이 스크립트를
  콕 집어 실행한 것 = 발행 준비됐다는 뜻(배치 모드 없음, 한 번에 하나).
- **PS 레포 소스가 1:N.** `publish`는 slug로 PS 레포 폴더 하나를 찾지만, 후기는
  그 대회의 라이브 코드 폴더 여러 개(`live_{contestId}{index}` — 대회날
  `day_XX`에 문제별로)에 대응한다. 그 폴더들을 전부 같은 메시지로 커밋한다.
- **커밋 메시지**: `feat: [Contest] {CF API 대회명} 후기` (블로그·PS 레포 동일).
  대회명은 포스트 `title`에서 그대로 온다(front matter가 `"{대회명} 후기"`).

커밋·front matter 헬퍼(`commit`/`has_pending_changes`/`extract_title`/`yaml_scalar_value`/
`read_front_matter`/`front_matter_block`)는 `publish`와 같은 `_shared/blog_common.py`에서
import해서 두 스킬 사이에서 커밋·파싱 방식이 갈라지지 않게 한다. 커밋 트레일러도 `commit`이 붙이는
`Co-Authored-By: Claude <noreply@anthropic.com>`(모델명 없음) 그대로 — 커밋 주체가
정적 스크립트라 커밋 시점에 모델 버전을 모름(블로그 CLAUDE.md "트레일러 모델명 규칙").
후기를 Claude가 손으로 커밋하는 경우(발행 후 손수정)만 모델명을 넣는다.

코드를 고칠 때 알아야 할 것:
- **PS 레포 쪽(`live_` 폴더) 검증을 블로그 레포를 건드리기 *전에* 한다**
  (`publish_one` 맨 앞) — `publish.py`와 같은 이유. `live_` 폴더를 하나도 못 찾으면
  아무것도 안 옮기고 에러 보고(대회 ID 오타이거나 이미 수동 처리한 경우).
- `os.rename` 이후부턴 실패해도 파일을 원래 자리로 안 되돌림 — 예외 메시지에
  "어디까지 진행됐는지" 명시.
- `live_` 폴더 패턴은 실제 관측된 레이아웃(`live_2259a`~`live_2259e`, 문제별)만
  매칭한다(`_live_folder_re`). 나중에 `live_2259/`(대회 하나에 폴더 하나, 문제는
  하위)로 바꾸면 그 함수도 같이 손봐야 함.

사용법:
    python3 publish_contest.py <후기 .md 경로 또는 대회 ID/URL>

    예:
        python3 publish_contest.py "_drafts/contest/2026-09-05-Codeforces Round 1119 (Div. 3).md"
        python3 publish_contest.py 2259
"""

import os
import re
import sys

_SKILLS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_SKILLS_DIR, "_shared"))

from blog_common import (
    DRAFTS_DIR,
    POSTS_DIR,
    PS_REPO,
    REPO_ROOT,
    commit,
    extract_title,
    front_matter_block,
    has_pending_changes,
    read_front_matter,
    yaml_scalar_value,
)

CONTEST_DRAFTS_DIR = os.path.join(DRAFTS_DIR, "contest")
CONTEST_POSTS_DIR = os.path.join(POSTS_DIR, "contest")


# 대회날 day_XX에 문제별로 생기는 라이브 코드 폴더: live_{contestId}{index}[...]
# (index는 알파벳 한 글자로 시작 — live_22590 같은 다른 대회 오매칭 방지)
def _live_folder_re(contest_id):
    return re.compile(rf"^live_{re.escape(contest_id)}[A-Za-z]\w*$")


def resolve_draft(arg):
    """후기 .md 경로 또는 대회 ID/URL → _drafts/contest/{파일} 절대경로."""
    abs_path = os.path.abspath(arg)
    if os.path.isfile(abs_path):
        if os.path.dirname(abs_path) != CONTEST_DRAFTS_DIR:
            raise ValueError(f"_drafts/contest/ 아래 있는 드래프트가 아님: {abs_path}")
        return abs_path

    # 경로처럼 생겼는데(슬래시 포함 or .md로 끝남) 파일이 없으면 — 경로 오타로 보고
    # 명확히 실패한다. 안 그러면 아래 숫자 추출이 경로 속 날짜("2026") 등을 잡아
    # 엉뚱한 대회 ID로 헤맴.
    if "/" in arg or arg.endswith(".md"):
        raise ValueError(f"후기 드래프트 파일을 찾을 수 없음: {abs_path}")

    m = re.search(r"(\d+)", arg)
    if not m:
        raise ValueError(f"후기 드래프트 경로도 대회 ID도 아님: {arg!r}")
    want_slug = f"codeforces-{m.group(1)}"

    if not os.path.isdir(CONTEST_DRAFTS_DIR):
        raise ValueError(f"{CONTEST_DRAFTS_DIR}가 없음 — 스캐폴드부터 생성할 것")
    matches = []
    for fname in sorted(os.listdir(CONTEST_DRAFTS_DIR)):
        if not fname.endswith(".md"):
            continue
        with open(os.path.join(CONTEST_DRAFTS_DIR, fname), encoding="utf-8") as f:
            slug = yaml_scalar_value(front_matter_block(f.read()), "slug")
        if slug == want_slug:
            matches.append(fname)
    if not matches:
        raise ValueError(f"_drafts/contest/에 slug={want_slug} 후기가 없음")
    if len(matches) > 1:
        raise ValueError(f"slug={want_slug} 후기가 여러 개: {matches}")
    return os.path.join(CONTEST_DRAFTS_DIR, matches[0])


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


def publish_one(draft_path):
    """후기 하나를 _posts/contest/로 옮기고 블로그 + PS 레포에 각각 커밋.
    (옮긴 경로, 블로그 커밋 여부, PS 커밋 여부)를 반환. 실패하면 어디까지
    진행됐는지 담은 예외를 그대로 던짐."""
    with open(draft_path, encoding="utf-8") as f:
        text = f.read()

    _date, slug = read_front_matter(text)
    if not slug.startswith("codeforces-"):
        raise ValueError(f"후기 slug 형식이 예상과 다름(codeforces-{{id}}): {slug}")
    contest_id = slug[len("codeforces-") :]
    title = extract_title(text)  # "Codeforces Round 1119 (Div. 3) 후기"
    message = f"feat: [Contest] {title}"

    # 블로그 레포를 건드리기 전에 PS 레포 쪽부터 검증 (publish.py와 같은 이유).
    live_folders = discover_live_folders(contest_id)
    if not live_folders:
        raise ValueError(
            f"PS 레포에서 live_{contest_id}* 폴더를 못 찾음 — 대회 ID를 확인하거나, "
            "이미 수동으로 처리했으면 `git mv`로 직접 옮길 것"
        )

    fname = os.path.basename(draft_path)
    target_path = os.path.join(CONTEST_POSTS_DIR, fname)
    if os.path.exists(target_path):
        raise FileExistsError(
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

    return target_path, blog_committed, ps_committed, live_folders


def main():
    argv = sys.argv[1:]
    if len(argv) != 1:
        print(__doc__)
        sys.exit(1)

    draft_path = resolve_draft(argv[0])
    target_path, blog_committed, ps_committed, live_folders = publish_one(draft_path)

    blog_note = (
        "블로그 커밋함" if blog_committed else "블로그 변경 없음(이미 커밋된 상태)"
    )
    ps_note = (
        f"PS 레포 커밋함 ({len(live_folders)}개 live 폴더)"
        if ps_committed
        else "PS 레포 이미 커밋된 상태"
    )
    print(f"발행함: {target_path} — {blog_note}, {ps_note}")


if __name__ == "__main__":
    main()
