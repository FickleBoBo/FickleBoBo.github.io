"""
레포 배치: 블로그·PS 레포 경로 상수, PS 플랫폼 접두사 맵(저지 목록에서 파생), 포스트 파일 탐색·파일명 규칙.
모든 경로는 `__file__` 기준 상대경로다. `PS_REPO`는 이 블로그 레포의 형제 디렉토리 `PS/`로 잡는다
(다른 위치에 두려면 여기만 고친다).
"""

import os

from judge import JUDGES

# 이 파일(.claude/skills/_shared/repo.py) 기준 이 블로그 레포 루트
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
DRAFTS_DIR = os.path.join(REPO_ROOT, "_drafts")
POSTS_DIR = os.path.join(REPO_ROOT, "_posts")

# PS 레포(형제 디렉토리) 루트
PS_REPO = os.path.abspath(os.path.join(REPO_ROOT, "..", "PS"))

# 접두사 → 플랫폼 표기. 지원하는 저지 목록은 `judge`가 정본이다
PLATFORM_MAP = {j.PREFIX: j.PLATFORM for j in JUDGES}

PREFIX_OF_PLATFORM = {v.lower(): k for k, v in PLATFORM_MAP.items()}

# `_drafts/`·`_posts/` 아래 PS 플랫폼 서브폴더 이름. 스킬의 스캔 범위는 이것으로 한정
# 한다(PS가 아닌 폴더·양식의 포스트는 자동으로 범위 밖).
PLATFORM_DIRS = sorted(PREFIX_OF_PLATFORM)

# 파일명 금지 문자 -> 육안 구별 어려운 유니코드 대체
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


def list_platform_posts(base_dir):
    """`base_dir/{platform}/*.md` 경로를 `PLATFORM_DIRS` 전체에 대해 정렬해 반환. 폴더가 없으면 건너뜀."""
    paths = []
    for platform_dir in PLATFORM_DIRS:
        dir_path = os.path.join(base_dir, platform_dir)
        if not os.path.isdir(dir_path):
            continue
        for fname in sorted(os.listdir(dir_path)):
            if fname.endswith(".md"):
                paths.append(os.path.join(dir_path, fname))
    return paths
