"""
`_drafts/{platform}/`의 PS 포스트 하나를 `_posts/{platform}/`로 옮기고 블로그 레포 + PS
레포(형제 디렉토리) 양쪽에 각각 커밋한다. push는 안 함. 완전 결정론적, LLM 판단 없음.
여러 개를 발행하려면 포스트마다 한 번씩 실행한다.

발행 준비 판정 기준·커밋 메시지·실패 처리는 `publish/SKILL.md`에 있다 — 여기서 반복 안 함.

코드를 고칠 때 알아야 할 것 (SKILL.md에 없는 정보):
- 레포 상수·front matter 파서·git 헬퍼·PS 폴더 역산(`resolve_source_folder`)은
  `_shared/blog_common.py`, 완료 판정에 쓰는 섹션 헤딩·SQL 전용 상수는 `ps/scripts/ps_source.py`에서 import.
- PS 레포 폴더 검증(`resolve_source_folder`)은 항상 블로그 레포를 건드리기 *전에* 한다 —
  실패 시 아무 상태도 안 남기려는 것. 순서를 바꾸면 파일만 옮겨진 애매한 상태가 남는다.
- `os.rename` 이후엔 자동 롤백이 없다(이유·케이스별 대응은 SKILL.md "실패 처리").

사용법:
    python3 publish.py <_drafts/{platform}/ 아래 드래프트 .md 경로>
종료 코드: 발행하면 0, 미완료·에러면 1, 인자 오류면 2.
"""

import os
import re
import sys

_SKILLS_DIR = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path.insert(0, os.path.abspath(os.path.join(_SKILLS_DIR, "_shared")))
sys.path.insert(0, os.path.abspath(os.path.join(_SKILLS_DIR, "ps", "scripts")))

from blog_common import (
    DRAFTS_DIR,
    PLATFORM_DIRS,
    POSTS_DIR,
    PS_REPO,
    REPO_ROOT,
    commit,
    extract_title,
    front_matter_block,
    has_pending_changes,
    read_front_matter,
    resolve_source_folder,
)
from ps_source import COMPLEXITY_HEADING, IDEA_HEADING, SQL_ONLY_LANGUAGES


def _section_body(text, heading):
    """`heading`("## " 포함 전체 헤딩) 다음부터 다음 `## ` 헤딩 전까지의 본문. 없으면 None."""
    m = re.search(
        rf"^{re.escape(heading)}\s*\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL
    )
    return m.group(1) if m else None


def section_is_filled(text, heading):
    """섹션 본문에 HTML 주석·구분선(---)을 뺀 실제 텍스트가 있는지. 헤딩이 없으면 스켈레톤이
    훼손된 것으로 보고 미완료."""
    body = _section_body(text, heading)
    if body is None:
        return False
    body = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL)
    body = "\n".join(line for line in body.splitlines() if line.strip() != "---")
    return bool(body.strip())


def is_sql_only_title(title):
    """title 끝의 언어 브래킷 집합이 `SQL_ONLY_LANGUAGES`와 같은지. `## 2. 복잡도` 헤딩
    부재로 판정하지 않는 이유는 SKILL.md "완료 판정" 참고."""
    m = re.search(r"((?:\[[^\[\]]*\])+)\s*$", title)
    if not m:
        return False
    return set(re.findall(r"\[([^\[\]]*)\]", m.group(1))) == SQL_ONLY_LANGUAGES


def complexity_table_filled(text):
    """`## 2. 복잡도` 표의 모든 데이터 행에서 시간·공간 셀이 둘 다 채워졌는지(행 수는
    검사 안 함 — `ps`가 접근법 수만큼 만든다)."""
    body = _section_body(text, COMPLEXITY_HEADING)
    if body is None:
        return False
    rows = [line.strip() for line in body.splitlines() if line.strip().startswith("|")]
    data_rows = rows[2:]  # 헤더 행 + 구분 행 제외
    if not data_rows:
        return False
    for row in data_rows:
        cells = [c.strip() for c in row.strip("|").split("|")]
        if len(cells) < 3 or not cells[1] or not cells[2]:
            return False
    return True


def front_matter_value(text, key):
    m = re.search(rf"^{key}:\s*(.*)$", front_matter_block(text), re.MULTILINE)
    return m.group(1).strip() if m else None


def not_ready_reason(text, platform_dir):
    """발행 준비가 안 됐으면 사유 문자열, 됐으면 None."""
    m = re.match(
        r"\[\s*PS\s*,\s*([^\],\s]+)\s*\]$", front_matter_value(text, "categories") or ""
    )
    if not m or m.group(1).lower() != platform_dir:
        return (
            f"categories({front_matter_value(text, 'categories')})가 폴더({platform_dir})와 "
            "안 맞음 — 올바른 _drafts/{platform}/로 옮긴 뒤 발행"
        )
    if not re.fullmatch(r"\[\s*\S.*\]", front_matter_value(text, "tags") or ""):
        return "tags가 비어 있음"
    if not section_is_filled(text, IDEA_HEADING):
        return "'1. 아이디어' 섹션이 비어 있음"
    if not is_sql_only_title(extract_title(text)) and not complexity_table_filled(text):
        return "'2. 복잡도' 표가 안 채워짐"
    return None


def publish_post(draft_path):
    """드래프트 하나를 검증하고 발행한다. 미완료면 아무것도 안 건드리고 ValueError."""
    draft_path = os.path.abspath(draft_path)
    platform_dir = os.path.basename(os.path.dirname(draft_path))
    if not os.path.isfile(draft_path):
        raise ValueError("파일을 찾을 수 없음")
    if platform_dir not in PLATFORM_DIRS or os.path.dirname(draft_path) != os.path.join(
        DRAFTS_DIR, platform_dir
    ):
        raise ValueError("_drafts/{platform}/ 아래 있는 드래프트가 아님")

    with open(draft_path, encoding="utf-8") as f:
        text = f.read()
    reason = not_ready_reason(text, platform_dir)
    if reason:
        raise ValueError(f"미완료 — {reason}")

    date, slug = read_front_matter(text)
    title = extract_title(text)

    # 블로그 레포를 건드리기 전에 PS 폴더 존재부터 검증.
    source_folder = resolve_source_folder(date, slug)

    posts_platform_dir = os.path.join(POSTS_DIR, platform_dir)
    target_path = os.path.join(posts_platform_dir, os.path.basename(draft_path))
    if os.path.exists(target_path):
        raise ValueError(f"_posts에 이미 같은 이름의 파일이 있음: {target_path}")

    os.makedirs(posts_platform_dir, exist_ok=True)
    os.rename(draft_path, target_path)  # 이 시점부턴 실패해도 파일은 이미 옮겨진 상태

    asset_dir = os.path.join(REPO_ROOT, "assets", "img", "posts", slug)
    blog_paths = [target_path] + ([asset_dir] if os.path.isdir(asset_dir) else [])

    try:
        blog_committed = has_pending_changes(REPO_ROOT, blog_paths)
        if blog_committed:
            commit(REPO_ROOT, blog_paths, f"feat: {title}")
    except Exception as e:
        raise RuntimeError(
            f"파일은 이미 {target_path}로 이동됐지만 블로그 커밋 실패: {e} "
            "— 수동으로 git add/commit 필요"
        )

    try:
        ps_committed = has_pending_changes(PS_REPO, [source_folder])
        if ps_committed:
            commit(PS_REPO, [source_folder], f"feat: {title}")
    except Exception as e:
        raise RuntimeError(
            f"블로그는 이미 커밋됨({target_path}), 하지만 PS 레포 커밋 실패: {e} "
            f"— PS 레포({source_folder})는 직접 확인 필요"
        )

    blog_note = "블로그 커밋함" if blog_committed else "블로그 이미 커밋된 상태"
    ps_note = "PS 레포 커밋함" if ps_committed else "PS 레포 이미 커밋된 상태"
    return f"발행함: {target_path} — {blog_note}, {ps_note}"


def main():
    if len(sys.argv) != 2:
        print(
            "사용법: python3 publish.py <드래프트 .md 경로> (한 번에 하나)",
            file=sys.stderr,
        )
        sys.exit(2)
    try:
        print(publish_post(sys.argv[1]))
    except Exception as e:
        print(f"에러({sys.argv[1]}): {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
