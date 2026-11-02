"""
`apply_tags.py <드래프트 .md> <leaf 태그> [<leaf 태그> ...]` — 확정된 leaf 태그를 드래프트 front matter의
`tags:` 줄에 쓴다. 결정론적이고 LLM 판단 없음.

leaf를 고르는 일은 `RULES.md`대로 에이전트 몫이고, 이 스크립트는 확정 뒤의 "조상 펼치기 → 정규 순서
정렬 → `tags:` 줄 치환"만 한다(조상을 손으로 펼치다 빠뜨리는 실수 방지). 펼치기·정렬 규칙은
`_shared/tag_vocab.py`의 `canonical_tags`다. 어휘집에 없는 태그와, 판정 근거인 `## 1. 아이디어`가 비어
있는 드래프트는 거부한다. 종료 코드: 적용하면 0, 거부되거나 에러면 1.
"""

import json
import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "_shared"))
)

from post_text import front_matter_block, read_tags, replace_tags
from problem_post import idea_is_filled
from tag_vocab import canonical_tags


def apply_tags(draft_path, leaf_tags):
    """`tags:` 줄을 바꿔 쓰고 `기존 → 신규` 한 줄을 돌려준다."""
    with open(draft_path, encoding="utf-8") as f:
        text = f.read()
    if not idea_is_filled(text):
        raise ValueError(
            "`## 1. 아이디어`가 비어 있다. 태그 판정은 아이디어의 핵심 관찰에 기대므로 먼저 작성한다."
        )
    final_tags = canonical_tags(leaf_tags)
    old_tags = read_tags(front_matter_block(text))
    new_text = replace_tags(text, final_tags)
    with open(draft_path, "w", encoding="utf-8") as f:
        f.write(new_text)
    old, new = (json.dumps(t, ensure_ascii=False) for t in (old_tags, final_tags))
    return f"{draft_path}:\n  tags: {old} → {new}"


def main():
    if len(sys.argv) < 3:
        sys.exit(
            "사용법: apply_tags.py <드래프트 .md 경로> <leaf 태그> [<leaf 태그> ...]"
        )
    try:
        print(apply_tags(os.path.abspath(sys.argv[1]), sys.argv[2:]))
    except (OSError, ValueError) as e:
        print(f"에러({sys.argv[1]}): {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
