"""
태그 규칙: front matter `tags:`의 형식·정합성. 어휘·정규 순서는 `tag_vocab`을 그대로 쓴다.
태그 판정(어떤 태그가 맞는가)은 보지 않는다.
"""

from post_text import read_tags, yaml_scalar_value
from ps_source import is_sql_only
from tag_vocab import canonical_tags, load_tag_parents

from .structure import trailing_langs


def tag_issues(fm, layout, published):
    """어휘/조상 누락, 중복, 정규 순서, `sql` 단독·제목 일치, 단일 접근 포스트의 `warm up` 병기,
    발행본(`published`)의 빈 태그. 다중 접근 여부는 `layout`의 풀이 헤딩 수로 본다."""
    tags = read_tags(fm)
    if tags is None:
        return []
    issues = []
    if not tags:
        if published:
            issues.append((1, "태그", "발행본인데 태그가 비어 있음"))
        return issues

    parents = load_tag_parents()
    unknown = [t for t in tags if t not in parents]
    for t in unknown:
        issues.append((1, "태그", f"어휘집에 없는 태그: {t!r}"))
    for t in tags:
        for p in parents.get(t, []):
            if p not in tags:
                issues.append((1, "태그", f"{t!r}의 조상 {p!r}가 빠짐"))
    if len(set(tags)) != len(tags):
        issues.append((1, "태그", "중복된 태그"))

    title_langs = trailing_langs(yaml_scalar_value(fm, "title") or "")
    sql_only = bool(title_langs) and is_sql_only(title_langs)
    if "sql" in tags and len(tags) > 1:
        issues.append((1, "태그", "`sql`은 다른 태그와 병기하지 않음"))
    elif ("sql" in tags) != sql_only:
        issues.append((1, "태그", "`sql` 태그와 제목의 `[MySQL]` 단독 표기가 어긋남"))

    if "warm up" in tags and len(tags) > 1 and len(layout.approaches) == 1:
        issues.append(
            (1, "태그", "`warm up`은 단일 접근 포스트에서 다른 태그와 병기하지 않음")
        )

    if not unknown and len(set(tags)) == len(tags):
        canonical = canonical_tags(tags)
        if canonical != tags:
            issues.append((1, "태그", f"태그 순서가 정규 순서와 다름 → {canonical}"))
    return issues
