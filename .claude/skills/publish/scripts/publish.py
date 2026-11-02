"""
`publish.py <드래프트.md>` — `_drafts/{platform}/`의 PS 포스트 하나를 검사하고, 결함이 없으면
`_posts/{platform}/`로 옮겨 블로그 레포 + PS 레포(형제 디렉토리)에 각각 커밋한다. push는 안 함(동작은 SKILL.md).

결함 검사(`blocking_defects`)는 파일 이동 전에 끝내고, 결함은 첫 번째에서 멈추지 않고 전부 모아 한 번에
보고한다. `os.rename` 이후엔 자동 롤백이 없다. 종료 코드: 발행하면 0, 막히거나 에러면 1.
"""

import os
import sys

_SKILLS_DIR = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path.insert(0, os.path.abspath(os.path.join(_SKILLS_DIR, "_shared")))

from git_ops import move_and_commit
from lint import lint, split_issues
from post_text import (
    extract_title,
    front_matter_block,
    read_front_matter,
    read_tags,
)
from problem_post import idea_is_filled
from ps_source import resolve_source_folder
from repo import DRAFTS_DIR, PLATFORM_DIRS, POSTS_DIR
from sync_text import sync_text


def format_issues(issues):
    return "\n".join(f"  {no}줄 [{rule}] {msg}" for no, rule, msg in issues)


def blocking_defects(draft_path, text):
    """(발행을 막는 결함 목록, 표기 이슈 목록). 표기 이슈는 알리기만 한다."""
    defects = []

    if not read_tags(front_matter_block(text)):
        defects.append("tags가 비어 있음")
    if not idea_is_filled(text):
        defects.append("'1. 아이디어' 섹션이 비어 있음")

    structure, notation = split_issues(lint(draft_path, strict=True))
    if structure:
        defects.append("구조 위반:\n" + format_issues(structure))

    try:
        source_folder = resolve_source_folder(*read_front_matter(text))
    except ValueError as e:
        defects.append(f"PS 소스 폴더: {e}")
    else:
        new_text, updated, warnings = sync_text(text, source_folder)
        if new_text != text:
            defects.append(
                f"포스트 코드가 PS 레포와 다름(`sync` 후 다시 발행): {', '.join(updated) or '공백 차이'}"
            )
        defects += [f"코드 대응 불일치: {w}" for w in warnings]

    return defects, notation


def publish_post(draft_path):
    """드래프트 하나를 검사하고 발행한다. 결함이 있으면 아무것도 안 건드리고 ValueError."""
    draft_path = os.path.abspath(draft_path)
    platform_dir = os.path.basename(os.path.dirname(draft_path))
    if os.path.dirname(draft_path) != os.path.join(DRAFTS_DIR, platform_dir) or (
        platform_dir not in PLATFORM_DIRS
    ):
        raise ValueError("_drafts/{platform}/ 아래 있는 드래프트가 아님")

    with open(draft_path, encoding="utf-8") as f:
        text = f.read()
    target_path = os.path.join(POSTS_DIR, platform_dir, os.path.basename(draft_path))

    defects, notation = blocking_defects(draft_path, text)
    if os.path.exists(target_path):
        defects.append(f"_posts에 이미 같은 이름의 파일이 있음: {target_path}")
    if defects:
        raise ValueError("발행 막힘:\n" + "\n".join(f"- {d}" for d in defects))

    date, slug = read_front_matter(text)
    blog_pending, ps_pending = move_and_commit(
        draft_path,
        target_path,
        slug,
        [resolve_source_folder(date, slug)],
        f"feat: {extract_title(text)}",
    )

    blog_note = "블로그 커밋함" if blog_pending else "블로그 이미 커밋된 상태"
    ps_note = "PS 레포 커밋함" if ps_pending else "PS 레포 이미 커밋된 상태"
    result = f"발행함: {target_path} — {blog_note}, {ps_note}"
    if notation:  # 표기 이슈는 발행을 막지 않고 알리기만 한다
        result += f"\n표기 참고 {len(notation)}건(발행엔 영향 없음):\n" + format_issues(
            notation
        )
    return result


def main():
    if len(sys.argv) != 2:
        sys.exit("사용법: publish.py <드래프트 .md 경로> (한 번에 하나)")
    try:
        print(publish_post(sys.argv[1]))
    except Exception as e:  # 막힘이든 이동 뒤 실패든 사유를 보고하고 종료 코드 1
        print(f"에러({sys.argv[1]}): {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
