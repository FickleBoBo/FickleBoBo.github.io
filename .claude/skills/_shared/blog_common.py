"""
스킬 스크립트들이 공유하는 레포 상수 + 순수 헬퍼. 스킬이 아니다(SKILL.md 없음) —
각 스킬 스크립트가 `sys.path`로 이 디렉토리를 끌어와 `from blog_common import ...`로
쓴다.

여기엔 **어느 한 스킬의 도메인에도 안 속하는 것만** 둔다: 레포 경로 상수, PS 플랫폼
접두사 맵과 플랫폼 폴더 스캔, 파일명·YAML 문자열 이스케이프, front matter 읽기, PS 레포 폴더 역산,
git 커밋 헬퍼. 스캐폴드 본문 생성, 코드 블록 동기화, 완료 판정처럼 한 스킬의 동작에
묶인 로직은 그 스킬에 남긴다(`sync`가 `ps`의 `clean_code`를 쓰는 식의 도메인 재사용은
계속 스킬 간 직접 import).

코드를 고칠 때 알아야 할 것:
- 모든 경로는 `__file__` 기준 상대경로다. `PS_REPO`도 이 블로그 레포의 형제 디렉토리
  `PS/`로 잡는다(다른 위치에 두려면 여기만 고친다).
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
PS_REPO = os.path.abspath(os.path.join(REPO_ROOT, "..", "PS"))

PLATFORM_MAP = {
    "prms": "Programmers",
    "leet": "LeetCode",
    "boj": "BaekJoon",
    "cofo": "Codeforces",
    "swea": "SWEA",
}

REVERSE_PLATFORM_MAP = {v.lower(): k for k, v in PLATFORM_MAP.items()}

# `_drafts/`·`_posts/` 아래 PS 플랫폼 서브폴더 이름. 스킬의 스캔 범위는 이것으로 한정
# 한다(PS가 아닌 폴더·양식의 포스트는 자동으로 범위 밖).
PLATFORM_DIRS = sorted(REVERSE_PLATFORM_MAP)

COMMIT_TRAILER = "Co-Authored-By: Claude <noreply@anthropic.com>"


# 파일명 금지 문자 -> 육안 구별 어려운 유니코드 대체
# 출처: laggner.info "Replacing Forbidden File System Characters with Unicode Alternatives"
# 주의: 이 치환은 파일명에만 적용. front matter의 title은 원문 그대로 씀.
FILENAME_ESCAPES = {
    "/": "⁄",  # FRACTION SLASH
    ":": "∶",  # RATIO
    "?": "？",  # FULLWIDTH QUESTION MARK
    "*": "⁎",  # LOW ASTERISK
    '"': "＂",  # FULLWIDTH QUOTATION MARK
    "<": "‹",  # SINGLE LEFT-POINTING ANGLE QUOTATION MARK
    ">": "›",  # SINGLE RIGHT-POINTING ANGLE QUOTATION MARK
    "\\": "∖",  # SET MINUS
    "|": "｜",  # FULLWIDTH VERTICAL LINE
}


def sanitize_filename(title):
    for bad, good in FILENAME_ESCAPES.items():
        title = title.replace(bad, good)
    return title


def yaml_dq(s):
    """YAML 큰따옴표 문자열 안에 안전하게 넣기 위한 이스케이프."""
    return s.replace("\\", "\\\\").replace('"', '\\"')


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


def resolve_source_folder(date, slug):
    """포스트 front matter의 date/slug로 PS 레포 원본 폴더의 실제 경로를 역산하고
    존재를 검증한다. 대소문자는 재구성한 이름을 믿지 않고 실제 디렉토리 엔트리명으로
    교체한다 — macOS(APFS)가 대소문자를 구분 안 해 `os.path.isdir`가 틀린 대소문자도
    통과시키는데 git은 구분해서, 어긋난 경로로 git을 돌리면 대상이 조용히 안 걸린다
    (실사고: Codeforces #2148A에서 PS 레포 커밋이 스킵됐는데 publish는 성공 보고)."""
    platform_lower, _, number = slug.partition("-")
    prefix = REVERSE_PLATFORM_MAP.get(platform_lower)
    if not prefix:
        raise ValueError(f"slug의 플랫폼 부분을 못 알아봄: {slug}")

    # slug는 항상 소문자라 Codeforces 인덱스 문자(예: 1553A)의 대문자 정보가 소실됨 —
    # PS 레포 폴더명은 대문자를 쓰므로 여기서 복원. 다른 플랫폼은 번호가 숫자뿐이라 무해.
    if prefix == "cofo":
        number = number.upper()

    day_dir = os.path.join(PS_REPO, date[:7], "src", f"day_{date[8:10]}")
    folder_name = f"{prefix}_{number}"
    folder = os.path.join(day_dir, folder_name)
    if not os.path.isdir(folder):
        raise ValueError(f"PS 레포에 해당 폴더가 없음(경로 재구성 결과): {folder}")
    actual_name = next(
        (e for e in os.listdir(day_dir) if e.lower() == folder_name.lower()), None
    )
    if actual_name is None:
        raise ValueError(f"PS 레포에 해당 폴더가 없음(경로 재구성 결과): {folder}")
    return os.path.join(day_dir, actual_name)


def list_platform_posts(base_dir, platform=None):
    """`base_dir/{platform}/*.md` 경로를 정렬해 반환. platform이 None이면
    `PLATFORM_DIRS` 전체, 아니면 그 플랫폼 하나(소문자). 폴더가 없으면 건너뜀."""
    paths = []
    for platform_dir in [platform] if platform else PLATFORM_DIRS:
        dir_path = os.path.join(base_dir, platform_dir)
        if not os.path.isdir(dir_path):
            continue
        for fname in sorted(os.listdir(dir_path)):
            if fname.endswith(".md"):
                paths.append(os.path.join(dir_path, fname))
    return paths


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
