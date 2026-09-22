#!/usr/bin/env python3
"""
review-code의 "태그 후보 추천"이 끝나고 사람이 최종 leaf 태그를 확정한 뒤,
그 태그를 드래프트 front matter에 실제로 써넣는 단계 — 순수 결정론적. LLM 판단
없음.

배경: leaf 태그 선정("이 개념이 이 문제의 핵심 난이도인가")은 tags.yaml 0번
규칙대로 여전히 사람/에이전트 해석 영역이라 이 스크립트가 하지 않는다(자동화
불가 — 문제 도메인 이해가 필요함). 하지만 leaf 태그가 확정된 뒤 "parents를
재귀적으로 펼쳐서 조상까지 다 붙인다"(tags.yaml 2·3번)는 순수 트리 lookup이라
해석 여지가 전혀 없는데, 이 단계를 에이전트가 손으로(Edit) 하다가 조상을
빠뜨리는 실수가 실제로 발생함(2026-09-13, number theory 확정하고 parents인
math를 "핵심 난이도 바를 또 넘어야 한다"며 잘못 제외 — 5번 규칙 예시에
브루트포스+수론+math 병기가 정확히 반례로 박혀 있었는데 놓침). 그래서 이
"확정된 leaf 태그 → 조상 펼치기 → front matter 치환"만 스크립트로 분리했다.

사용법:
    python3 apply_tags.py <드래프트 .md 경로> <leaf 태그> [<leaf 태그> ...]

동작:
    1. tags.yaml을 파싱해 태그 → parents 매핑을 만든다(contextual/exception은
       이 단계에서 안 씀 — 그것도 사람 판단 영역이라 이미 leaf 태그 목록에
       반영된 걸로 취급).
    2. 입력 leaf 태그마다 parents를 재귀적으로 펼쳐 조상까지 다 모은다
       (다중부모면 두 라인 다, 중복 제거).
    3. 최종 나열 순서(2026-09-13 확정, 사용자 지정): 태그 집합을 "체인"으로
       묶는다 — 각 체인은 어떤 최상위 조상(parents가 빈 태그)에서 시작해 그
       조상을 가진 하위 태그로 내려가는 한 줄기. 체인끼리는 그 **최상위
       조상 이름의 알파벳 오름차순**으로 나열하고, 체인 내부는 항상 상위 →
       하위 순으로 쓴다. 예: `bfs`+`bit manipulation` 추천 → `bfs`의 조상은
       `graph`(최상위), `bit manipulation`은 조상 없어 자기 자신이 최상위 →
       최상위끼리 정렬하면 `bit manipulation` < `graph` → 최종
       `["bit manipulation", "graph", "bfs"]`. 한 조상 밑에 형제 태그가
       여럿이면(같은 부모를 공유하는 하위 태그가 동시에 뽑힌 경우) 그
       형제끼리도 알파벳 오름차순.

       다중부모(`tree dp`의 `tree`+`dynamic programming`, `aho corasick`의
       `string`+`trie`)처럼 한 태그가 두 체인에 걸치면, tags.yaml에 적힌
       parents 순서상 먼저 나오는 조상을 그 태그가 속할 "주 체인"으로 삼는다.
       이건 임의 타이브레이크가 아니라 이미 확정된 분류를 그대로 따르는
       것 — 프로젝트 메모리 `ps-tag-taxonomy`의 확정 트리 다이어그램이
       `tree dp`를 `tree` 섹션 밑에, `aho corasick`을 `string` 섹션 밑에
       "본가"로 이미 그려뒀고, `tags.yaml`의 parents 배열 순서가 그 결정을
       그대로 반영한다(예: `tree dp: { parents: [tree, dynamic programming] }`
       — `tree`가 먼저). 부모 이름 알파벳순으로 바꾸면 오히려 `tree`와
       `tree dp`가 떨어져 나와(→ `dynamic programming` 밑으로 감) 기존
       분류와 어긋나므로 채택 안 함(2026-09-13 확정).
    4. 어휘집에 없는 태그가 입력되면 즉시 에러(오타 방지, 조용히 넘어가지 않음).
    5. 드래프트 front matter의 `tags:` 줄을 전부 큰따옴표로 감싼 배열로
       치환한다(tags.yaml 6번 — 아포스트로피 유무 안 따지고 항상 큰따옴표).
       `tags:` 줄이 front matter 안에 없거나 형식이 예상과 다르면 에러.

이 스크립트가 하지 않는 것:
    - leaf 태그가 이 문제에 적절한지 판단(그건 review-code 체크 항목 몫).
    - contextual 태그를 자동으로 끼워 넣는 것(예: trie→string) — 그것도 문제
      성격 판단이라 사람이 필요하다고 정하면 leaf 태그 인자에 직접 넣어서 준다.
    - 여러 드래프트 배치 처리 — 한 번에 하나. 확정 태그는 드래프트마다 다르므로
      배치화해봐야 인자 목록만 늘어날 뿐 이득이 없다.
"""

import re
import sys
from pathlib import Path

TAGS_YAML = Path(__file__).parent.parent / "tags.yaml"

# tags.yaml의 태그 정의 줄만 매칭. 이름은 큰따옴표로 감싸져 있거나(아포스트로피
# 포함 태그) 그냥 소문자+공백+하이픈+숫자 조합. `# 다중부모` 같은 줄 끝 주석은
# 무시.
_LINE_RE = re.compile(
    r'^\s*(?:"([^"]+)"|([a-z0-9][a-z0-9 \'\-]*?)):\s*'
    r"\{\s*parents:\s*\[([^\]]*)\]"
)


def load_tag_parents():
    """tags.yaml을 파싱해 {태그명: [parents]} 딕셔너리를 만든다."""
    parents = {}
    in_tags_block = False
    for raw_line in TAGS_YAML.read_text(encoding="utf-8").splitlines():
        stripped = raw_line.strip()
        if stripped == "tags:":
            in_tags_block = True
            continue
        if stripped == "boundary_notes:":
            break
        if not in_tags_block:
            continue
        if not stripped or stripped.startswith("#"):
            continue

        m = _LINE_RE.match(raw_line)
        if not m:
            # 여기서 조용히 넘어가지 않음 — tags.yaml의 태그 정의는 전부 이 정규식이
            # 매칭하는 한 줄짜리 flow 스타일이라, 형식이 바뀌어 일부 줄만 매칭 안 되면
            # 해당 태그가 parents_map에서 조용히 빠지고, 그 태그가 실제로 쓰일 때만
            # (leaf 또는 누군가의 parent로) 뒤늦게 "오타 확인" 에러로 잘못 드러난다.
            # 파싱 시점에 바로 잡아서 원인을 명확히 한다.
            raise ValueError(
                f"tags.yaml 파싱 실패 — 'tags:' 블록의 이 줄이 태그 정의 패턴과 "
                f"안 맞음: {raw_line!r}\n형식이 바뀌었으면 이 파일의 _LINE_RE도 "
                "같이 고칠 것."
            )

        name = m.group(1) if m.group(1) is not None else m.group(2)
        parents_raw = m.group(3).strip()
        parent_list = (
            [p.strip() for p in parents_raw.split(",") if p.strip()]
            if parents_raw
            else []
        )
        parents[name] = parent_list

    return parents


def expand_tags(leaf_tags, parents_map):
    """leaf 태그 목록을 순서 유지하며 조상까지 재귀적으로 펼친다(중복 제거)."""
    result = []

    def add(tag):
        if tag not in parents_map:
            print(
                f"에러: '{tag}'는 tags.yaml 어휘집에 없는 태그다(오타 확인).",
                file=sys.stderr,
            )
            sys.exit(1)
        if tag not in result:
            result.append(tag)
            for parent in parents_map[tag]:
                add(parent)

    for leaf in leaf_tags:
        add(leaf)

    return result


def order_tags(tag_set_list, parents_map):
    """확정된(중복 제거된) 태그 목록을, 최상위 조상 알파벳순 체인 묶음으로
    재배열한다(위 docstring 3번). 입력 순서는 안 씀 — 순수하게 tags.yaml
    구조 + 알파벳순으로만 정해짐."""
    tag_set = set(tag_set_list)

    # 각 태그의 "주 체인 부모" — parents 중 tags.yaml에 적힌 순서상 먼저
    # 나오면서 이 태그 집합에도 포함된 것. 없으면 그 태그가 체인의 최상위.
    primary_parent = {}
    for tag in tag_set_list:
        primary_parent[tag] = next((p for p in parents_map[tag] if p in tag_set), None)

    children = {}
    roots = []
    for tag in tag_set_list:
        parent = primary_parent[tag]
        if parent is None:
            roots.append(tag)
        else:
            children.setdefault(parent, []).append(tag)

    ordered = []

    def visit(tag):
        ordered.append(tag)
        for child in sorted(children.get(tag, [])):
            visit(child)

    for root in sorted(set(roots)):
        visit(root)

    return ordered


def apply_to_draft(draft_path: Path, final_tags):
    text = draft_path.read_text(encoding="utf-8")

    if not text.startswith("---"):
        print(f"에러: front matter가 없는 파일이다: {draft_path}", file=sys.stderr)
        sys.exit(1)

    end = text.find("\n---", 3)
    if end == -1:
        print(
            f"에러: front matter 종료 구분선을 못 찾음: {draft_path}", file=sys.stderr
        )
        sys.exit(1)

    front_matter = text[:end]
    rest = text[end:]

    tags_line_re = re.compile(r"^tags:\s*\[.*\]\s*$", re.MULTILINE)
    if not tags_line_re.search(front_matter):
        print(
            f"에러: front matter 안에서 `tags: [...]` 줄을 못 찾음: {draft_path}",
            file=sys.stderr,
        )
        sys.exit(1)

    quoted = ", ".join(f'"{t}"' for t in final_tags)
    new_front_matter = tags_line_re.sub(f"tags: [{quoted}]", front_matter, count=1)

    draft_path.write_text(new_front_matter + rest, encoding="utf-8")


def main():
    if len(sys.argv) < 3:
        print(
            "사용법: python3 apply_tags.py <드래프트 .md 경로> <leaf 태그> [<leaf 태그> ...]",
            file=sys.stderr,
        )
        sys.exit(1)

    draft_path = Path(sys.argv[1]).resolve()
    leaf_tags = sys.argv[2:]

    if not draft_path.is_file():
        print(f"에러: 파일이 없다: {draft_path}", file=sys.stderr)
        sys.exit(1)

    parents_map = load_tag_parents()
    expanded = expand_tags(leaf_tags, parents_map)
    final_tags = order_tags(expanded, parents_map)

    apply_to_draft(draft_path, final_tags)

    quoted = ", ".join(f'"{t}"' for t in final_tags)
    print(f"{draft_path}: tags: [{quoted}]")


if __name__ == "__main__":
    main()
