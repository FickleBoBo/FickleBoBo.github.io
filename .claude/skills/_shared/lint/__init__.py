"""
포스트(`_drafts/` 또는 `_posts/`의 .md)에서 기계적으로 판정되는 규칙 위반을 잡는 결정적 린터. LLM 판단 없음.
`review-post` 오케스트레이터가 서브에이전트 dispatch 전에 돌려 결과를 리포트에 합치고, `publish`가
발행 전에 돌린다. 명령줄 진입점은 `_shared/lint_post.py`.

이슈는 `(줄 번호, 규칙 이름, 설명)`이고 구조(`publish`가 막음)와 표기(보고만)로 나뉜다. 두 종류의 규칙
목록과 근거는 `STYLE.md`가 정본이다. 규칙을 바꾸면 거기도 같이 바꾼다.

- `structure`: 구조 규칙(front matter·제목·섹션·풀이 헤딩·코드 블록)
- `tags`: 태그 규칙
- `prose`: 표기 규칙(어투·맞춤법·용어·수식)

코드를 고칠 때 알아야 할 것:
- 규칙을 추가하면 먼저 시험 입력으로 오탐이 없는지 본다. 발행본의 진짜 위반은 사용자 글이라 이
  린터가 고치지 않고 리포트만 한다(`review-post`와 같은 원칙).
- `lint(path, strict=True)`는 `publish`용이다. 드래프트에서 허용하는 `### 풀이 N [언어]`
  (이름 붙이기 전) 형태도 이슈로 본다.
"""

import os

from post_text import front_matter_block

from .prose import prose_issues
from .structure import (
    approach_issues,
    front_matter_issues,
    layout_issues,
    scan_layout,
)
from .tags import tag_issues

# 구조 이슈의 규칙 이름. 이 밖의 이슈는 표기 이슈(보고만)다
STRUCTURE_RULES = {"front matter", "제목", "섹션", "풀이 헤딩", "코드 블록", "태그"}


def split_issues(issues):
    """(구조 이슈, 표기 이슈)."""
    structure = [i for i in issues if i[1] in STRUCTURE_RULES]
    return structure, [i for i in issues if i[1] not in STRUCTURE_RULES]


def lint(path, strict=False):
    path = os.path.abspath(path)
    with open(path, encoding="utf-8") as f:
        text = f.read()

    try:
        fm = front_matter_block(text)
    except ValueError as e:
        return [(1, "front matter", str(e))]
    fm_lines = fm.count("\n") + 3  # '---' + 본문 + '---'
    body = [(i + fm_lines + 1, ln) for i, ln in enumerate(text.split("\n")[fm_lines:])]

    fm_issues, title_langs = front_matter_issues(fm)
    layout = scan_layout(body)
    return [
        *tag_issues(fm, layout, published=f"{os.sep}_posts{os.sep}" in path),
        *approach_issues(
            layout, allow_scaffold=not strict and f"{os.sep}_drafts{os.sep}" in path
        ),
        *fm_issues,
        *layout_issues(layout, title_langs),
        *prose_issues(body),
    ]
