"""
태그 어휘집(`tags.yaml`) 로더와 정규 태그 배열 — `tag`의 `apply_tags.py`와 `lint/tags.py`가 공유한다.
어휘·조상·정규 순서를 한 곳에서 정의해 부착(apply_tags)과 검사(lint)가 어긋나지 않게 한다.
오류는 `ValueError`로 올린다(호출하는 쪽이 종료 방식을 정한다).
"""

import functools
import re
from pathlib import Path

TAGS_YAML = Path(__file__).with_name("tags.yaml")

# tags.yaml의 한 줄짜리 flow 스타일 정의만 매칭. 이름은 큰따옴표(아포스트로피·숫자 시작 태그)
# 또는 소문자+공백+하이픈 조합이고, 줄 끝 `# 다중부모` 같은 주석은 무시한다.
_LINE_RE = re.compile(
    r'^\s*(?:"([^"]+)"|([a-z0-9][a-z0-9 \'\-]*?)):\s*'
    r"\{\s*parents:\s*\[([^\]]*)\]"
)


@functools.cache
def load_tag_parents():
    """tags.yaml을 파싱해 {태그명: [parents]}를 만든다(첫 호출만 읽고, 반환값은 수정하지 않는다).
    형식이 어긋나면 조용히 넘기지 않고 에러."""
    parents = {}
    for raw_line in TAGS_YAML.read_text(encoding="utf-8").splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#") or stripped == "tags:":
            continue
        m = _LINE_RE.match(raw_line)
        if not m:
            raise ValueError(
                f"tags.yaml 파싱 실패 — 태그 정의 패턴과 안 맞는 줄: {raw_line!r}"
                "\n형식이 바뀌었으면 이 파일의 _LINE_RE도 같이 고칠 것."
            )
        name = m.group(1) or m.group(2)
        if name in parents:
            raise ValueError(f"tags.yaml 파싱 실패 — 태그가 중복 정의됨: {name!r}")
        parents[name] = [p.strip() for p in m.group(3).split(",") if p.strip()]

    for name, parent_list in parents.items():
        for parent in parent_list:
            if parent not in parents:
                raise ValueError(
                    f"tags.yaml 파싱 실패 — {name!r}의 부모 {parent!r}가 정의되지 않음"
                )
    return parents


def _expand(leaf_tags, parents_map):
    """leaf 태그를 조상까지 재귀로 펼친다(중복 제거)."""
    result = []

    def add(tag):
        if tag not in parents_map:
            raise ValueError(f"'{tag}'는 tags.yaml 어휘집에 없는 태그다(오타 확인).")
        if tag not in result:
            result.append(tag)
            for parent in parents_map[tag]:
                add(parent)

    for leaf in leaf_tags:
        add(leaf)
    return result


def _order(tags, parents_map):
    """태그 집합을 최상위 조상 알파벳순 체인으로 재배열한다(입력 순서는 안 씀)."""
    tag_set = set(tags)
    children = {}
    roots = []
    for tag in tags:
        # 주 체인 부모: parents 목록에서 먼저 나오면서 이 집합에 포함된 것
        parent = next((p for p in parents_map[tag] if p in tag_set), None)
        if parent is None:
            roots.append(tag)
        else:
            children.setdefault(parent, []).append(tag)

    ordered = []

    def visit(tag):
        ordered.append(tag)
        for child in sorted(children.get(tag, [])):
            visit(child)

    for root in sorted(roots):
        visit(root)
    return ordered


def canonical_tags(leaf_tags):
    """leaf 태그를 조상까지 펼쳐 정규 순서로 정렬한 `tags:` 배열. 어휘집에 없는 태그는 ValueError.
    정규 순서는 최상위 조상 알파벳순 체인이고 체인 안은 상위 → 하위, 같은 부모 밑 형제는 알파벳순이다
    (`bfs`+`bit manipulation` → `bit manipulation, graph, bfs`). 다중부모 태그(`tree dp`,
    `aho corasick`)는 parents 목록에서 먼저 나오는 부모의 체인에 속한다."""
    parents_map = load_tag_parents()
    return _order(_expand(leaf_tags, parents_map), parents_map)
