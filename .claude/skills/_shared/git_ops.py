"""
블로그·PS 레포 git 작업: 지정한 경로만 커밋하는 헬퍼와, 드래프트를 옮겨 두 레포에 같은 메시지로 커밋하는
`move_and_commit`.

`commit()`은 `git commit -- <pathspec>`으로 지정한 경로만 커밋한다(인덱스에 이미 staged된 무관한
변경이 같이 실리는 걸 막기 위함). `has_pending_changes()`는 커밋할 실제 범위와 항상 같은 인자로
불러야 한다. 트레일러에 모델명이 없는 이유(정적 스크립트라 커밋 시점 모델 버전을 모름)는 레포
`CLAUDE.md`의 "트레일러 모델명 규칙".
"""

import os
import subprocess

from repo import PS_REPO, REPO_ROOT

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
    """paths(pathspec 리스트) 중 하나라도 변경사항 있으면 True. 일부만 넘기면(예: 에셋 디렉토리
    빠짐) 그 경로만 변경됐을 때 조용히 스킵될 수 있다."""
    return bool(run_git(repo_dir, ["status", "--porcelain", "--"] + paths).strip())


def commit(repo_dir, paths, message):
    """paths를 add한 뒤 commit에도 같은 paths를 pathspec으로 넘긴다 — pathspec이 없으면 그 시점
    인덱스 전체가 커밋에 실려, 무관하게 이미 staged된 변경이 조용히 같이 커밋될 수 있다."""
    run_git(repo_dir, ["add", "--"] + paths)
    run_git(
        repo_dir,
        ["commit", "-m", f"{message}\n\n{COMMIT_TRAILER}", "--"] + paths,
    )


def move_and_commit(draft_path, target_path, slug, ps_paths, message):
    """드래프트를 target_path로 옮기고 블로그 레포(포스트+이미지 폴더)와 PS 레포(ps_paths)에 같은
    메시지로 커밋한다. `(블로그 커밋함, PS 커밋함)` 반환(이미 커밋된 상태면 False). 이동 뒤 실패는
    자동 롤백 없이 RuntimeError로 현 상태를 알린다. 호출하는 쪽이 이동 전에 검증을 끝내야 한다."""
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    os.rename(draft_path, target_path)  # 이 시점부턴 실패해도 파일은 이미 옮겨진 상태

    asset_dir = os.path.join(REPO_ROOT, "assets", "img", "posts", slug)
    blog_paths = [target_path] + ([asset_dir] if os.path.isdir(asset_dir) else [])
    try:
        blog_pending = has_pending_changes(REPO_ROOT, blog_paths)
        if blog_pending:
            commit(REPO_ROOT, blog_paths, message)
    except Exception as e:
        raise RuntimeError(
            f"파일은 이미 {target_path}로 이동됐지만 블로그 커밋 실패: {e} "
            "— 수동으로 git add/commit 필요"
        ) from e
    try:
        ps_pending = has_pending_changes(PS_REPO, ps_paths)
        if ps_pending:
            commit(PS_REPO, ps_paths, message)
    except Exception as e:
        raise RuntimeError(
            f"블로그는 이미 커밋됨({target_path}), 하지만 PS 레포 커밋 실패: {e} "
            f"— PS 레포({', '.join(ps_paths)})는 직접 확인 필요"
        ) from e
    return blog_pending, ps_pending
