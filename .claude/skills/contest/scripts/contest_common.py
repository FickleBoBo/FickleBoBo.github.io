"""
대회 후기 스크립트(`scaffold_contest.py`·`publish_contest.py`)가 같이 쓰는 경로 상수와
slug로 후기 파일을 찾는 헬퍼. 스킬이 아니라 이 스킬의 내부 모듈(SKILL.md 없음).
"""

import os
import re
import sys

_SKILLS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_SKILLS_DIR, "_shared"))

from blog_common import DRAFTS_DIR, POSTS_DIR, front_matter_block, yaml_scalar_value

CONTEST_DRAFTS_DIR = os.path.join(DRAFTS_DIR, "contest")
CONTEST_POSTS_DIR = os.path.join(POSTS_DIR, "contest")
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
