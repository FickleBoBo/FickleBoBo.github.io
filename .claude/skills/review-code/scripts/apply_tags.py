"""
확정된 leaf 태그를 드래프트 front matter에 쓴다 — 순수 결정론적, LLM 판단 없음.
leaf 태그를 고르는 일은 `tags.yaml`의 사용법·`boundary_notes`대로 사람/에이전트 몫이고,
이 스크립트는 확정 뒤의 "조상 펼치기 → 정렬 → `tags:` 줄 치환"만 한다(조상을 손으로
펼치다 빠뜨리는 실수를 막기 위해 분리).

사용법:
    python3 apply_tags.py <드래프트 .md 경로> <leaf 태그> [<leaf 태그> ...]

동작:
    1. `tags.yaml`에서 태그 → parents 매핑을 읽고 정합성을 검증한다(중복 정의·정의 안 된
       부모·순환은 에러). `contextual`·`exception`은 이 단계에서 안 씀 — 이미 leaf 목록에
       반영된 것으로 취급.
    2. leaf마다 parents를 재귀로 펼쳐 조상까지 모은다(다중부모면 두 라인 다, 중복 제거).
    3. 최상위 조상(parents가 빈 태그) 이름의 알파벳 오름차순으로 "체인"을 나열하고, 체인
       안은 상위 → 하위 순, 같은 부모 밑 형제는 알파벳순. 예: `bfs`+`bit manipulation`
       → `["bit manipulation", "graph", "bfs"]`. 다중부모 태그(`tree dp`, `aho corasick`)는
       `tags.yaml` parents 배열에서 먼저 나오는 부모의 체인에 속한다(배열 순서가 곧 확정된 분류).
    4. 어휘집에 없는 태그는 즉시 에러(오타 방지). `sql`은 단독으로만 허용한다.
    5. `tags:` 줄을 항상 큰따옴표로 감싼 배열로 치환한다. `tags:` 줄이 없거나 형식이 다르면
       에러. 출력은 `기존 → 신규`를 같이 보여준다.

한 번에 한 포스트만 처리한다(확정 태그가 포스트마다 달라 배치화 이득이 없음).
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
        if name in parents:
            raise ValueError(f"tags.yaml 파싱 실패 — 태그가 중복 정의됨: {name!r}")
        parents[name] = parent_list

    for name, parent_list in parents.items():
        for parent in parent_list:
            if parent not in parents:
                raise ValueError(
                    f"tags.yaml 파싱 실패 — {name!r}의 부모 {parent!r}가 정의되지 않음"
                )

    state = {}  # 1 = 탐색 중, 2 = 완료

    def check_cycle(tag):
        if state.get(tag) == 2:
            return
        if state.get(tag) == 1:
            raise ValueError(f"tags.yaml 파싱 실패 — parents 순환: {tag!r}")
        state[tag] = 1
        for parent in parents[tag]:
            check_cycle(parent)
        state[tag] = 2

    for name in parents:
        check_cycle(name)

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

    old_line = tags_line_re.search(front_matter).group(0).strip()
    quoted = ", ".join(f'"{t}"' for t in final_tags)
    new_front_matter = tags_line_re.sub(f"tags: [{quoted}]", front_matter, count=1)

    draft_path.write_text(new_front_matter + rest, encoding="utf-8")
    return old_line


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

    if "sql" in leaf_tags and len(leaf_tags) > 1:
        print(
            "에러: `sql`은 다른 태그와 병기하지 않는다(SQL 전용 포스트).",
            file=sys.stderr,
        )
        sys.exit(1)

    parents_map = load_tag_parents()
    expanded = expand_tags(leaf_tags, parents_map)
    final_tags = order_tags(expanded, parents_map)

    old_line = apply_to_draft(draft_path, final_tags)

    quoted = ", ".join(f'"{t}"' for t in final_tags)
    print(f"{draft_path}:\n  {old_line}\n  → tags: [{quoted}]")


if __name__ == "__main__":
    main()
