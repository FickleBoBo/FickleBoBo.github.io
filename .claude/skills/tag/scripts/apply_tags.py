"""
확정된 leaf 태그를 드래프트 front matter에 쓴다 — 결정론적, LLM 판단 없음.
leaf를 고르는 일은 `tags.yaml`의 판정 원칙·`boundary_notes`대로 에이전트 몫이고, 이 스크립트는
확정 뒤의 "조상 펼치기 → 정렬 → `tags:` 줄 치환"만 한다(조상을 손으로 펼치다 빠뜨리는 실수 방지).

사용법: python3 apply_tags.py <드래프트 .md 경로> <leaf 태그> [<leaf 태그> ...]

1. `_shared/tag_vocab.py`가 `tags.yaml`에서 태그 → parents 매핑을 읽고 검증한다(중복 정의·정의 안 된 부모·순환은 에러).
   `contextual`·`exception`은 안 씀 — 이미 leaf 목록에 반영된 것으로 취급.
2. leaf마다 parents를 재귀로 펼쳐 조상까지 모은다(중복 제거). 어휘집에 없는 태그는 에러(오타 방지).
3. 최상위 조상 이름의 알파벳순으로 체인을 나열한다. 체인 안은 상위 → 하위, 같은 부모 밑 형제는
   알파벳순. 예: `bfs`+`bit manipulation` → `["bit manipulation", "graph", "bfs"]`. 다중부모
   태그(`tree dp`, `aho corasick`)는 parents 배열에서 먼저 나오는 부모의 체인에 속한다.
4. `tags:` 줄을 큰따옴표 배열로 치환하고 `기존 → 신규`를 출력한다. `sql`은 단독으로만 허용.
   아이디어 섹션이 비어 있으면 거부한다(판정 근거가 아이디어에 있다).
"""

import re
import sys
from pathlib import Path

_SKILLS_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_SKILLS_DIR / "_shared"))
from post_text import front_matter_block
from problem_post import idea_is_filled
from tag_vocab import expand_tags, load_tag_parents, order_tags

_TAGS_LINE_RE = re.compile(r"^tags:[ \t]*\[.*\][ \t]*$", re.MULTILINE)


def die(msg):
    print(f"에러: {msg}", file=sys.stderr)
    sys.exit(1)


def apply_to_draft(draft_path, final_tags):
    """front matter의 `tags:` 줄을 치환하고 (기존 줄, 새 줄)을 돌려준다."""
    text = draft_path.read_text(encoding="utf-8")
    try:
        front_matter = front_matter_block(text)
    except ValueError as e:
        die(f"{e}: {draft_path}")
    m = _TAGS_LINE_RE.search(front_matter)
    if not m:
        die(f"front matter 안에서 `tags: [...]` 줄을 못 찾음: {draft_path}")
    new_line = "tags: [" + ", ".join(f'"{t}"' for t in final_tags) + "]"
    # front_matter_block은 여는 `---\n` 뒤부터 반환한다
    start = len("---\n") + m.start()
    draft_path.write_text(
        text[:start] + new_line + text[start + len(m.group(0)) :], encoding="utf-8"
    )
    return m.group(0).strip(), new_line


def main():
    if len(sys.argv) < 3:
        die("사용법: apply_tags.py <드래프트 .md 경로> <leaf 태그> [<leaf 태그> ...]")
    draft_path = Path(sys.argv[1]).resolve()
    leaf_tags = sys.argv[2:]
    if not draft_path.is_file():
        die(f"파일이 없다: {draft_path}")
    if "sql" in leaf_tags and len(leaf_tags) > 1:
        die("`sql`은 다른 태그와 병기하지 않는다(SQL 전용 포스트).")

    if not idea_is_filled(draft_path.read_text(encoding="utf-8")):
        die(
            "`## 1. 아이디어`가 비어 있다. 태그 판정은 아이디어의 핵심 관찰에 기대므로 먼저 작성한다."
        )

    try:
        parents_map = load_tag_parents()
        final_tags = order_tags(expand_tags(leaf_tags, parents_map), parents_map)
    except ValueError as e:
        die(str(e))
    old_line, new_line = apply_to_draft(draft_path, final_tags)
    print(f"{draft_path}:\n  {old_line}\n  → {new_line}")


if __name__ == "__main__":
    main()
