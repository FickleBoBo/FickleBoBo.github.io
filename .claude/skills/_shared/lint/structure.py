"""
구조 규칙: front matter 필수 키, 제목 형식·언어 브라켓 순서, 섹션 헤딩, `### 풀이` 헤딩 형식, 코드 블록
언어(풀이 헤딩 브라켓·제목과의 일치), 펜스 짝. `publish`가 이 규칙 위반이 있으면 막는다.
"""

import re
from dataclasses import dataclass, field

from post_text import classify_fences, yaml_scalar_value
from problem_post import CODE_HEADING, IDEA_HEADING, QUERY_HEADING
from ps_source import LANGUAGE_DISPLAY_ORDER, LANGUAGE_OF_FENCE, is_sql_only

REQUIRED_KEYS = ("title", "date", "categories", "tags", "slug")
TITLE_RE = re.compile(r"^\[[^\[\]]+\] #\S+ - .+? (?P<langs>(?:\[[^\[\]]+\])+)$")
TRAILING_LANGS_RE = re.compile(r" ((?:\[[^\[\]]+\])+)$")
LEGACY_SECTION_RE = re.compile(r"^## (?:\d+\. 복잡도|3\. (?:코드|쿼리))$")

# `### 풀이` 헤딩 형식(STYLE.md "다중 접근 — 접근 이름")
_LANGS = r" (\[[^\]]+\])+"
SINGLE_HEADING_RE = re.compile(rf"^### 풀이{_LANGS}$")
MULTI_HEADING_RE = re.compile(rf"^### 풀이 (\d+): (\S.*?){_LANGS}$")
# ps 스캐폴드 직후(이름 전)
SCAFFOLD_HEADING_RE = re.compile(rf"^### 풀이 (\d+){_LANGS}$")


def bracket_langs(s):
    return re.findall(r"\[([^\[\]]+)\]", s)


def trailing_langs(s):
    """문자열 끝의 `[언어][언어]...` 브라켓 목록. 없으면 []."""
    m = TRAILING_LANGS_RE.search(s.rstrip())
    return bracket_langs(m.group(1)) if m else []


@dataclass
class Approach:
    no: int  # 헤딩 줄 번호
    heading: str
    fences: list = field(default_factory=list)  # 이 풀이 구간의 코드 펜스 언어 태그

    @property
    def langs(self):
        return trailing_langs(self.heading)


@dataclass
class Layout:
    """본문 순회 한 번으로 모은 섹션·풀이·펜스 정보."""

    sections: list  # (줄 번호, `## ` 헤딩)
    approaches: list  # Approach
    stray_fences: list  # `### 풀이` 헤딩 앞의 코드 블록 줄 번호
    unclosed: int | None  # 닫히지 않은 펜스의 줄 번호


def scan_layout(body):
    """`body`는 (줄 번호, 줄) 리스트. 코드 섹션 안의 `### 풀이` 헤딩만 풀이로 본다(아이디어 속
    `### 풀이 아이디어` 같은 줄은 대상 아님)."""
    kinds, unclosed = classify_fences([line for _, line in body])
    layout = Layout([], [], [], body[unclosed][0] if unclosed is not None else None)
    in_code = False
    for (no, line), kind in zip(body, kinds):
        if kind == "open":
            if in_code:
                info = line.strip().lstrip("`~").strip().split(" ")[0]
                if layout.approaches:
                    layout.approaches[-1].fences.append(info)
                else:
                    layout.stray_fences.append(no)
        elif kind != "text":
            continue
        elif line.startswith("## "):
            layout.sections.append((no, line.rstrip()))
            in_code = line.rstrip() in (CODE_HEADING, QUERY_HEADING)
        elif in_code and line.startswith("### 풀이"):
            layout.approaches.append(Approach(no, line.rstrip()))
    return layout


def front_matter_issues(fm):
    """필수 키와 제목. 제목에서 읽은 언어 목록도 돌려준다: (이슈, 제목 언어)."""
    issues = []
    for key in REQUIRED_KEYS:
        if yaml_scalar_value(fm, key) is None:
            issues.append((1, "front matter", f"필수 키가 없음: {key}"))

    title = yaml_scalar_value(fm, "title") or ""
    if not title:
        return issues, []
    m = TITLE_RE.match(title)
    if not m:
        issues.append(
            (1, "제목", f"`[플랫폼] #번호 - 제목 [언어]...` 형식이 아님: {title}")
        )
        return issues, []
    langs = bracket_langs(m.group("langs"))
    rank = [
        LANGUAGE_DISPLAY_ORDER.index(lang)
        for lang in langs
        if lang in LANGUAGE_DISPLAY_ORDER
    ]
    if len(rank) != len(langs) or len(set(langs)) != len(langs):
        issues.append((1, "제목", f"언어 브라켓이 알 수 없거나 중복: {langs}"))
    elif rank != sorted(rank):
        issues.append(
            (1, "제목", f"언어 브라켓 순서는 {LANGUAGE_DISPLAY_ORDER} 고정: {langs}")
        )
    return issues, langs


def approach_issues(layout, allow_scaffold=False):
    """`### 풀이` 헤딩 형식: 단일은 `### 풀이 [langs]`, 다중은 `### 풀이 N: 이름 [langs]`
    (번호 1부터 연속). 이름을 붙이기 전(review-post 전)의 `### 풀이 N [langs]`는 `allow_scaffold`일
    때만 허용한다."""
    heads = layout.approaches
    issues = []
    if len(heads) == 1:
        a = heads[0]
        if not SINGLE_HEADING_RE.match(a.heading):
            issues.append(
                (
                    a.no,
                    "풀이 헤딩",
                    f"접근이 하나면 `### 풀이 [언어]...` 형식: {a.heading}",
                )
            )
    elif len(heads) >= 2:
        nums = []
        for a in heads:
            if m := MULTI_HEADING_RE.match(a.heading):
                nums.append(int(m.group(1)))
            elif allow_scaffold and (sm := SCAFFOLD_HEADING_RE.match(a.heading)):
                nums.append(int(sm.group(1)))
            else:
                issues.append(
                    (
                        a.no,
                        "풀이 헤딩",
                        f"다중 접근은 `### 풀이 N: 이름 [언어]...` 형식: {a.heading}",
                    )
                )
        if len(nums) == len(heads) and nums != list(range(1, len(nums) + 1)):
            issues.append(
                (heads[0].no, "풀이 헤딩", f"풀이 번호가 1부터 연속이 아님: {nums}")
            )
    return issues


def layout_issues(layout, title_langs):
    """섹션 헤딩, 코드 블록 언어, 펜스 짝, 제목 브라켓과 풀이 브라켓의 일치."""
    issues = []
    for no in layout.stray_fences:
        issues.append((no, "코드 블록", "`### 풀이` 헤딩 앞에 코드 블록이 있음"))
    if layout.unclosed is not None:
        issues.append((layout.unclosed, "코드 블록", "코드 펜스가 닫히지 않음"))

    names = [h for _, h in layout.sections]
    for no, h in layout.sections:
        if LEGACY_SECTION_RE.match(h):
            issues.append(
                (no, "섹션", f"구형 섹션 헤딩(복잡도·`## 3. 코드`)은 쓰지 않음: {h}")
            )
    expected_code = QUERY_HEADING if is_sql_only(title_langs) else CODE_HEADING
    if IDEA_HEADING not in names:
        issues.append((1, "섹션", f"`{IDEA_HEADING}` 헤딩이 없음"))
    if expected_code not in names:
        issues.append(
            (1, "섹션", f"`{expected_code}` 헤딩이 없음(SQL 전용만 `{QUERY_HEADING}`)")
        )
    elif IDEA_HEADING in names and names.index(IDEA_HEADING) > names.index(
        expected_code
    ):
        issues.append((1, "섹션", "아이디어 섹션이 코드 섹션보다 뒤에 있음"))

    if expected_code in names and not layout.approaches:
        issues.append((1, "풀이 헤딩", "코드 섹션에 `### 풀이` 헤딩이 없음"))
    union = set()
    for a in layout.approaches:
        fence_langs = [LANGUAGE_OF_FENCE[f] for f in a.fences if f in LANGUAGE_OF_FENCE]
        if a.langs != fence_langs:
            issues.append(
                (
                    a.no,
                    "코드 블록",
                    f"풀이 헤딩 브라켓 {a.langs}과 코드 블록 언어 {fence_langs}가 다름",
                )
            )
        union.update(a.langs)
    if title_langs and layout.approaches and union != set(title_langs):
        issues.append(
            (
                1,
                "제목",
                f"제목 언어 브라켓 {title_langs}과 풀이 헤딩 브라켓 {sorted(union)}이 다름",
            )
        )
    return issues
