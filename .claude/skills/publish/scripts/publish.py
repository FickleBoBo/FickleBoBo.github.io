#!/usr/bin/env python3
"""
_drafts/{platform}/의 "발행 준비 완료"된 PS 포스트를 _posts/{platform}/로 옮기고,
이 블로그 레포 + PS 레포(형제 디렉토리) 양쪽에 각각 커밋한다. push는 안 함 — 로컬
커밋까지만, 실제 배포는 사람이 직접. `ps`/`sync`와 마찬가지로 완전 결정론적,
LLM 판단 없음.

**"발행 준비 완료"의 정확한 판정 기준, 커밋 메시지 포맷, git add 범위 등 설계
이유는 전부 `publish/SKILL.md`에 문서화돼있음 — 여기서 다시 설명 안 함.**

코드를 고칠 때 알아야 할 것 (SKILL.md에 없는, 이 파일 안에서만 유효한 정보):
- `ps`(`resolve_filename.py`)와 `sync`(`sync_code.py`)를 그대로 import해서 씀
  (`read_front_matter`/`resolve_source_folder`/`front_matter_block`/
  `PLATFORM_MAP`/`PS_REPO`/`DRAFTS_DIR`/`POSTS_DIR`/`REPO_ROOT`) — front matter
  파싱 규칙이나 PS 레포 경로 재구성 로직이 세 스킬 사이에서 갈라지면 안 되기 때문.
- PS 레포 폴더 검증(`resolve_source_folder`)을 항상 블로그 레포를 건드리기
  *전에* 먼저 함(`publish_one` 맨 앞) — 실패 시 아무 상태도 안 남기고 깨끗하게
  에러 보고하기 위함. 이 순서를 바꾸면(먼저 옮기고 나중에 검증) 실패했을 때
  파일만 옮겨진 애매한 상태가 남음.
- `os.rename` 이후부터는 실패해도 파일을 원래 자리로 되돌리지 않음(자동 롤백
  없음) — 각 예외 메시지에 "어디까지 진행됐는지"를 명시해서 사람이 정확히 뭘
  마저 처리해야 하는지 알 수 있게 하는 쪽으로 설계함.

사용법:
    python3 publish.py [경로 ...]
        경로를 안 주면 _drafts/{platform}/(platform ∈ PLATFORM_MAP) 전체를 스캔해서
        완료된 것만 각각 독립적으로 발행(전체 배치). 하나 이상 주면 그 드래프트들만
        대상으로 함(사용자가 특정 포스트를 지목했을 때) — 이 경우에도 "완료 판정"은
        똑같이 적용됨(지정했다고 미완료 드래프트를 강제로 발행하지 않음).
"""

import os
import re
import subprocess
import sys

_SKILLS_DIR = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path.insert(0, os.path.abspath(os.path.join(_SKILLS_DIR, "ps", "scripts")))
sys.path.insert(0, os.path.abspath(os.path.join(_SKILLS_DIR, "sync", "scripts")))

from resolve_filename import (
    COMPLEXITY_HEADING,
    DRAFTS_DIR,
    IDEA_HEADING,
    PLATFORM_MAP,
    POSTS_DIR,
    PS_REPO,
    REPO_ROOT,
)
from sync_code import (
    front_matter_block,
    read_front_matter,
    resolve_source_folder,
)

COMMIT_TRAILER = "Co-Authored-By: Claude <noreply@anthropic.com>"


def run_git(repo_dir, args):
    result = subprocess.run(
        ["git", "-C", repo_dir] + args, capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"git {' '.join(args)} 실패({repo_dir}): {result.stderr.strip()}"
        )
    return result.stdout


def has_pending_changes(repo_dir, paths):
    """paths(pathspec 리스트) 중 하나라도 변경사항 있으면 True. 커밋할 실제 범위와
    항상 동일한 인자로 불러야 함 — 일부만 넘기면(예: 에셋 디렉토리 빠짐) 그 경로만
    변경됐을 때 조용히 스킵될 수 있음."""
    return bool(run_git(repo_dir, ["status", "--porcelain", "--"] + paths).strip())


def commit(repo_dir, paths, message):
    """add로 스테이징한 뒤 commit에도 동일한 paths를 pathspec으로 넘김 — commit에
    pathspec이 없으면 그 시점 인덱스 전체가 커밋에 실려서, 이 발행 작업과 무관하게
    이미 staged된 변경사항이 있을 때 조용히 같이 커밋될 수 있음(레포에 다른 작업으로
    이미 add된 파일이 있는 경우). `git commit -- <pathspec>`은 인덱스의 다른 파일은
    안 건드리고 지정한 경로 변경사항만 커밋하므로 이 위험을 원천 차단함."""
    run_git(repo_dir, ["add", "--"] + paths)
    run_git(
        repo_dir,
        ["commit", "-m", f"{message}\n\n{COMMIT_TRAILER}", "--"] + paths,
    )


def yaml_scalar_value(front_matter_text, field):
    """front matter에서 `{field}: ...` 값을 뽑음. YAML은 큰따옴표 없는 스칼라도
    유효해서(`description: 그냥 이렇게`) 따옴표 유무 둘 다 처리 — 사람이 프로즈 채울 때
    따옴표를 안 쓰거나 실수로 지워도 "비어있음"으로 오판하지 않게 하기 위함. 필드
    자체가 없으면 None, 값이 빈 문자열이면 ""을 반환.

    전제: 값은 항상 한 줄(정규식이 그 줄만 읽음) — `ps` 스킬이 생성하는 `description`은
    항상 한 줄 문자열이라 지금까지는 문제없었지만, 사람이 `description: |`처럼 여러 줄
    블록 스칼라로 바꾸면 첫 줄만 읽고 나머지는 조용히 무시됨(YAML 파서 미사용). 이 정도
    엣지케이스에 YAML 라이브러리를 끌어오는 건 이 프로젝트 규모에 과함 — 실제로 발생하면
    그때 재검토."""
    m = re.search(rf"^{field}:\s*(.*)$", front_matter_text, re.MULTILINE)
    if not m:
        return None
    raw = m.group(1).strip()
    if len(raw) >= 2 and raw[0] == raw[-1] == '"':
        return raw[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    if len(raw) >= 2 and raw[0] == raw[-1] == "'":
        return raw[1:-1].replace("''", "'")
    return raw


def extract_title(text):
    title = yaml_scalar_value(front_matter_block(text), "title")
    if title is None:
        raise ValueError("front matter에 title이 없음")
    return title


def description_filled(text):
    desc = yaml_scalar_value(front_matter_block(text), "description")
    return bool(desc and desc.strip())


def section_is_filled(text, heading):
    """`{heading}`(예: `## 1. 아이디어` — "## " 포함한 전체 헤딩 문자열) 다음, 다음
    `## ` 헤딩 전까지 본문에 HTML 주석/구분선(---) 빼고 실제 텍스트가 있는지. ps
    스킬이 생성한 스캐폴드는 이 heading이 항상 존재한다는 전제(핵심 섹션이라 사람이
    통째로 안 지움) — 없으면 스켈레톤이 훼손된 것으로 보고 미완료 취급."""
    pattern = rf"^{re.escape(heading)}\s*\n(.*?)(?=^## |\Z)"
    m = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    if not m:
        return False
    body = re.sub(r"<!--.*?-->", "", m.group(1), flags=re.DOTALL)
    body = "\n".join(line for line in body.splitlines() if line.strip() != "---")
    return bool(body.strip())


def complexity_table_filled(text):
    """`## 2. 복잡도` 표의 모든 데이터 행(헤더/구분줄 제외)에서 시간·공간 셀이 둘 다
    채워졌는지. 행 개수 자체는 검사 안 함(ps가 이미 접근법 수만큼 정확히 만들어둠) —
    있는 행이 다 채워졌는지만 봄."""
    pattern = rf"^{re.escape(COMPLEXITY_HEADING)}\s*\n(.*?)(?=^## |\Z)"
    m = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    if not m:
        return False
    rows = [
        line.strip() for line in m.group(1).splitlines() if line.strip().startswith("|")
    ]
    data_rows = rows[2:]  # 헤더 행 + `|---|---|---|` 구분 행 제외
    if not data_rows:
        return False
    for row in data_rows:
        cells = [c.strip() for c in row.strip("|").split("|")]
        if len(cells) < 3 or not cells[1] or not cells[2]:
            return False
    return True


def is_ready(text):
    """드래프트 하나가 "발행 준비 완료"인지 (bool, 미완료 사유) 반환. 판정 기준
    자체의 설계 이유는 SKILL.md 참고 — 여기선 각 검사만 순서대로 호출."""
    if not description_filled(text):
        return False, "description이 비어있음"
    if not section_is_filled(text, IDEA_HEADING):
        return False, "'1. 아이디어' 섹션이 비어있음"
    if not complexity_table_filled(text):
        return False, "'2. 복잡도' 표가 안 채워짐"
    return True, None


def discover_ready_drafts(explicit_paths=None):
    """explicit_paths가 없으면 _drafts/{platform}/*.md(platform ∈ PLATFORM_MAP)
    전체를 훑고(전체 배치), 있으면 그 경로들만 후보로 씀(사용자가 특정 포스트를
    지목한 모드) — 둘 다 완료 판정 로직은 동일하게 적용. 후보 중 완료 판정된 것만
    (경로, platform_dir, 파일명) 리스트로, 미완료·못 찾음·경로가 이상함은 전부
    (경로, 사유) 리스트로 반환. PLATFORM_MAP에 없는 서브폴더나 _drafts/ 바로 밑
    파일은 애초에 안 봄(전체 배치 모드) — 블로그에 PS 아닌 드래프트가 생겨도 안
    건드리기 위한 스코핑."""
    valid_platforms = {v.lower() for v in PLATFORM_MAP.values()}
    candidates, not_ready = [], []

    if explicit_paths:
        for path in explicit_paths:
            # 사용자가 상대경로를 넘길 수도 있어서, DRAFTS_DIR(절대경로)과 비교하기
            # 전에 항상 절대경로로 정규화함 — 안 그러면 진짜 드래프트도 "경로가
            # 이상함"으로 오판됨(실제로 겪은 버그).
            abs_path = os.path.abspath(path)
            platform_dir = os.path.basename(os.path.dirname(abs_path))
            if not os.path.isfile(abs_path):
                not_ready.append((path, "파일을 찾을 수 없음"))
            elif platform_dir not in valid_platforms or os.path.dirname(
                abs_path
            ) != os.path.join(DRAFTS_DIR, platform_dir):
                not_ready.append(
                    (path, "_drafts/{platform}/ 아래 있는 드래프트가 아님")
                )
            else:
                candidates.append((abs_path, platform_dir, os.path.basename(abs_path)))
    else:
        for platform_dir in sorted(valid_platforms):
            dir_path = os.path.join(DRAFTS_DIR, platform_dir)
            if not os.path.isdir(dir_path):
                continue
            for fname in sorted(os.listdir(dir_path)):
                if fname.endswith(".md"):
                    candidates.append(
                        (os.path.join(dir_path, fname), platform_dir, fname)
                    )

    ready = []
    for path, platform_dir, fname in candidates:
        with open(path, encoding="utf-8") as f:
            text = f.read()
        ok, reason = is_ready(text)
        if ok:
            ready.append((path, platform_dir, fname))
        else:
            not_ready.append((path, reason))
    return ready, not_ready


def publish_one(draft_path, platform_dir, fname):
    """드래프트 하나를 _posts로 옮기고 블로그 레포 + PS 레포에 각각 커밋. (옮긴
    최종 경로, 블로그 실제 커밋 여부, PS 레포 실제 커밋 여부)를 반환. 실패하면
    어디까지 진행됐는지 담긴 예외를 그대로 던짐(호출자가 그대로 보고)."""
    with open(draft_path, encoding="utf-8") as f:
        text = f.read()

    date, slug = read_front_matter(text)
    title = extract_title(text)

    # 블로그 레포를 건드리기 전에 PS 레포 폴더 존재부터 검증 — 여기서 실패하면
    # 아무것도 안 건드린 깨끗한 상태로 에러 보고 가능.
    source_folder = resolve_source_folder(date, slug)

    posts_platform_dir = os.path.join(POSTS_DIR, platform_dir)
    target_path = os.path.join(posts_platform_dir, fname)
    if os.path.exists(target_path):
        raise FileExistsError(f"_posts에 이미 같은 이름의 파일이 있음: {target_path}")

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

    return target_path, blog_committed, ps_committed


def run_batch(explicit_paths=None):
    ready, not_ready = discover_ready_drafts(explicit_paths)

    published, errors = [], []
    for draft_path, platform_dir, fname in ready:
        try:
            published.append(publish_one(draft_path, platform_dir, fname))
        except Exception as e:
            errors.append((draft_path, str(e)))

    for target_path, blog_committed, ps_committed in published:
        blog_note = "블로그 커밋함" if blog_committed else "블로그 이미 커밋된 상태"
        ps_note = "PS 레포 커밋함" if ps_committed else "PS 레포 이미 커밋된 상태"
        print(f"발행함: {target_path} — {blog_note}, {ps_note}")
    for draft_path, msg in errors:
        print(f"에러({draft_path}): {msg}")
    for draft_path, reason in not_ready:
        print(f"미완료라 스킵: {draft_path} — {reason}")
    print(
        f"--- 총 {len(published)}개 발행, {len(not_ready)}개는 미완료라 스킵, "
        f"{len(errors)}개 에러 ---"
    )


def main():
    run_batch(sys.argv[1:] or None)


if __name__ == "__main__":
    main()
