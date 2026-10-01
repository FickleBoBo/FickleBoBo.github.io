"""
스킬 스크립트들이 공유하는 레포 상수 + 순수 헬퍼. 스킬이 아니다(SKILL.md 없음) —
`ps`/`sync`/`publish`/`review-code`/`contest` 스크립트가 `sys.path`로 이 디렉토리를
끌어와 `from blog_common import ...`로 쓴다.

여기엔 **어느 한 스킬의 도메인에도 안 속하는 것만** 둔다: 레포 경로 상수, PS 플랫폼
접두사 맵, front matter 읽기, git 커밋 헬퍼. 스캐폴드 본문 생성·코드 블록 동기화·
완료 판정처럼 한 스킬의 동작에 묶인 로직은 그 스킬에 남긴다(`sync`가 `ps`의
`clean_code`를 쓰는 식의 도메인 재사용은 계속 스킬 간 직접 import).

여기로 모은 이유(2026-10-02): `resolve_filename.py`(`ps`)에 공용 상수가, `sync_code.py`에
front matter 파서가, `publish.py`에 git 헬퍼가 얹혀 있어 `contest → publish → sync → ps`
식으로 스킬이 서로의 스크립트를 연쇄 import하고 있었다. 정의만 이 파일로 옮겼고 동작은
그대로다. 기존 모듈(`resolve_filename`/`sync_code`/`publish`)도 이 이름들을 import해서
들고 있어 옛 경로로 가져다 써도 깨지지 않는다.

코드를 고칠 때 알아야 할 것:
- `PS_REPO`는 이 컴퓨터/사용자 전용으로 하드코딩된 유일한 값 — 다른 환경에서 쓰려면
  여기만 고치면 된다. 나머지 경로는 전부 `__file__` 기준 상대경로.
- `commit()`은 `git commit -- <pathspec>`으로 지정한 경로만 커밋한다(인덱스에 이미
  staged된 무관한 변경이 같이 실리는 걸 막기 위함) — `has_pending_changes()`는 커밋할
  실제 범위와 항상 같은 인자로 불러야 한다.
- 트레일러에 모델명이 없는 이유(정적 스크립트라 커밋 시점 모델 버전을 모름)는
  레포 `CLAUDE.md`의 "트레일러 모델명 규칙".
"""

import os
import re
import subprocess

# 이 파일(.claude/skills/_shared/blog_common.py) 기준 이 블로그 레포 루트
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
DRAFTS_DIR = os.path.join(REPO_ROOT, "_drafts")
POSTS_DIR = os.path.join(REPO_ROOT, "_posts")

# PS 레포(형제 디렉토리) 루트
PS_REPO = "/Users/mwzz6/Desktop/github/PS"

PLATFORM_MAP = {
    "prms": "Programmers",
    "leet": "LeetCode",
    "boj": "BaekJoon",
    "cofo": "Codeforces",
    "swea": "SWEA",
}

COMMIT_TRAILER = "Co-Authored-By: Claude <noreply@anthropic.com>"


def front_matter_block(post_text):
    m = re.match(r"^---\n(.*?)\n---\n", post_text, re.DOTALL)
    if not m:
        raise ValueError("front matter(--- ~ ---) 블록을 못 찾음")
    return m.group(1)


def read_front_matter(post_text):
    raw = front_matter_block(post_text)

    date_m = re.search(r"^date:\s*(\S+)", raw, re.MULTILINE)
    slug_m = re.search(r"^slug:\s*(\S+)", raw, re.MULTILINE)
    if not date_m or not slug_m:
        raise ValueError("front matter에 date 또는 slug가 없음")
    return date_m.group(1), slug_m.group(1)


def yaml_scalar_value(front_matter_text, field):
    """front matter에서 `{field}: ...` 값을 뽑음. YAML은 큰따옴표 없는 스칼라도
    유효해서(`title: 그냥 이렇게`) 따옴표 유무 둘 다 처리한다. 필드 자체가 없으면
    None, 값이 빈 문자열이면 ""을 반환.

    전제: 값은 항상 한 줄(정규식이 그 줄만 읽음) — `ps` 스킬이 생성하는 필드는 전부
    한 줄 스칼라라 지금까지는 문제없었지만, 사람이 `title: |`처럼 여러 줄 블록
    스칼라로 바꾸면 첫 줄만 읽고 나머지는 조용히 무시됨(YAML 파서 미사용). 이 정도
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
