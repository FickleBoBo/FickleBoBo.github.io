"""
대회 후기 스크립트(`scaffold_contest.py`·`publish_contest.py`)가 같이 쓰는 경로 상수와
slug로 후기 파일을 찾는 헬퍼, PS 레포의 `live_{contestId}{index}` 폴더 탐색.
진입점이 `_shared`를 `sys.path`에 넣은 뒤 import된다.
"""

import os
import re

from post_text import front_matter_block, yaml_scalar_value
from repo import DRAFTS_DIR, POSTS_DIR, PS_REPO

CONTEST_DRAFTS_DIR = os.path.join(DRAFTS_DIR, "contest")
CONTEST_POSTS_DIR = os.path.join(POSTS_DIR, "contest")
# 대회 중 쓴 코드 파일명(Codeforces는 C++만). 폴더에 이 파일이 없으면 라이브 코드가 없는 것으로 본다.
LIVE_CODE_FILE = "Main.cpp"

# 정제된 개별 문제 풀이 포스트가 사는 곳(후기의 `풀이 →` 링크 실재 확인용).
CODEFORCES_POSTS_DIR = os.path.join(POSTS_DIR, "codeforces")

# assets/img/posts/{slug}/ 아래 프리뷰 카드 파일명. front matter image.path가 가리킴.
CARD_NAME = "preview.png"


def parse_contest_id(arg):
    """'2259' / URL / '.../contest/2259/...' 어느 꼴이든 대회 ID(정수)만 뽑는다."""
    m = re.search(r"(\d+)", arg)
    if not m:
        raise ValueError(f"대회 ID를 못 읽음: {arg!r}")
    return int(m.group(1))


def find_posts_by_slug(slug, dirs):
    """`dirs`(앞에서부터) 안의 .md 중 front matter slug가 일치하는 파일 경로 전부."""
    found = []
    for d in dirs:
        if not os.path.isdir(d):
            continue
        for fname in sorted(os.listdir(d)):
            if not fname.endswith(".md"):
                continue
            path = os.path.join(d, fname)
            with open(path, encoding="utf-8") as f:
                text = f.read()
            try:
                value = yaml_scalar_value(front_matter_block(text), "slug")
            except ValueError:  # front matter 없는 파일
                continue
            if value == slug:
                found.append(path)
    return found


def _live_folder_re(contest_id):
    """live_{contestId}{index}[...] — index는 알파벳 한 글자로 시작(live_22590 같은 다른 대회 오매칭 방지).
    index 대소문자는 구분하지 않는다(PS 폴더는 소문자, CF 문제 index는 대문자)."""
    return re.compile(
        rf"^live_{re.escape(str(contest_id))}([A-Za-z]\w*)$", re.IGNORECASE
    )


def discover_live_folders(contest_id):
    """PS 레포에서 그 대회의 live_{contestId}{index} 폴더 전부(경로순).
    패턴은 실제 관측된 레이아웃만 매칭하므로 폴더 구조가 바뀌면 손볼 것."""
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


def load_live_code(contest_id):
    """{문제 index(대문자): 코드 문자열}. `live_{contestId}{index}/Main.cpp`를 읽기만 한다.
    PS 레포나 폴더·파일이 없으면 그 문제는 빠진다(빈 dict). 같은 index가 둘이면 먼저 찾은 쪽."""
    try:
        folders = discover_live_folders(contest_id)
    except ValueError:
        return {}
    pat = _live_folder_re(contest_id)
    codes = {}
    for folder in folders:
        index = pat.match(os.path.basename(folder)).group(1).upper()
        path = os.path.join(folder, LIVE_CODE_FILE)
        if index in codes or not os.path.isfile(path):
            continue
        with open(path, encoding="utf-8") as f:
            codes[index] = f.read().rstrip("\n")
    return codes
