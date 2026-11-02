"""
`review-post` 서브에이전트의 JSON 보고를 검증해 포스트별 결과와 예비 등급을 렌더링한다. 기계적으로
정해지는 일을 오케스트레이터 대신 여기서 한다: 단위 누락 검사, 인용 검증, 린터 실행과 심각도 매핑, 건수
집계, 등급 환산(S 제외), 포스트 사이 문장 중복.

사용법:
    render_report.py <보고 파일> [...]

보고 파일은 서브에이전트가 낸 텍스트 그대로다(```json 펜스 한 블록, 형식은 `.claude/agents/post-reviewer.md`
`## 출력 형식`). 형식이 틀리거나 단위가 빠졌으면 사유만 내고 종료 코드 1(아무것도 렌더링하지 않는다).
등급 기준은 SKILL.md `## 등급 환산`이다.
"""

import os
import re
import sys

_SKILLS_DIR = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path.insert(0, os.path.abspath(os.path.join(_SKILLS_DIR, "_shared")))

from lint import STRUCTURE_RULES, lint
from problem_post import idea_is_filled
from repo import DRAFTS_DIR, POSTS_DIR, list_platform_posts
from report_io import cell, collect, exit_on_errors
from units import ROLES, extract_units

CATEGORIES = ("코드-설명", "제약", "표기", "맞춤법", "구조")
GRADED = ("로직", "경미")  # 코드-설명·제약만 서브에이전트가 심각도를 고른다
AXES = ("논증 엄밀성", "추론 명확성", "통찰 공백", "문장력")
MIN_DUPLICATE_CHARS = 15


def is_text(v):
    return isinstance(v, str) and bool(v.strip())


FIXED_SEVERITY = {"표기": "표기", "맞춤법": "표기", "구조": "경미"}


def severity(f):
    """분류에서 정해지는 심각도. 코드-설명·제약만 보고된 값을 쓴다."""
    return FIXED_SEVERITY.get(f["category"]) or f["severity"]


def finding_error(f, ids):
    if not isinstance(f, dict) or f.get("category") not in CATEGORIES:
        return f"category는 {'|'.join(CATEGORIES)} 중 하나"
    if f.get("unit") not in ids:
        return f"unit이 이 포스트의 단위 번호가 아님: {f.get('unit')!r}"
    if not is_text(f.get("basis")):
        return "basis가 비어 있음"
    if "fragment" in f and not is_text(f["fragment"]):
        return "fragment는 비지 않은 문자열이어야 함(생략 가능)"
    if f["category"] in ("코드-설명", "제약") and f.get("severity") not in GRADED:
        return f"{f['category']}의 severity는 {'|'.join(GRADED)} 중 하나"
    if f["category"] in ("표기", "맞춤법") and not is_text(f.get("rule")):
        return "표기·맞춤법은 rule(위반한 STYLE.md 규칙 이름)이 필요"
    return None


def observation_error(o, ids):
    if not isinstance(o, dict) or o.get("axis") not in AXES:
        return f"axis는 {'|'.join(AXES)} 중 하나"
    if not is_text(o.get("text")):
        return "text가 비어 있음"
    if "unit" in o and o["unit"] not in ids:
        return f"unit이 이 포스트의 단위 번호가 아님: {o['unit']!r}"
    return None


def diagram_error(d, ids):
    if is_text(d):
        return None
    if isinstance(d, list) and 1 <= len(d) <= 2:
        for c in d:
            if (
                not isinstance(c, dict)
                or c.get("unit") not in ids
                or not all(is_text(c.get(k)) for k in ("show", "format", "input"))
            ):
                return "후보는 {unit, show, format, input}(unit은 단위 번호)"
        return None
    return "diagram은 해당 없음 사유(문자열) 또는 후보 1~2개 배열"


def units_error(reported, units):
    if not isinstance(reported, dict):
        return "units가 객체가 아님"
    expected = {no for no, _, _ in units}
    problems = []
    if missing := sorted(expected - reported.keys()):
        problems.append(f"빠진 단위: {', '.join(missing)}")
    if extra := sorted(reported.keys() - expected):
        problems.append(f"없는 단위: {', '.join(extra)}")
    bad = [
        f"{no}={role!r}"
        for no, role in reported.items()
        if no in expected and role not in ROLES[no[0]]
    ]
    if bad:
        problems.append(
            f"역할 오류 {', '.join(bad)} (I: {'|'.join(ROLES['I'])} / "
            f"C: {'|'.join(ROLES['C'])} / R: {'|'.join(ROLES['R'])})"
        )
    return "; ".join(problems) or None


def entry_errors(entry, text, units):
    """검증할 수 있는 게 없으면(아이디어가 비어 있음) 빈 목록."""
    if entry.get("source") not in ("확인", "미확인"):
        return ["source는 확인|미확인"]
    if not idea_is_filled(text):
        return []
    ids = {no for no, _, _ in units}
    errors = []
    if e := units_error(entry.get("units"), units):
        errors.append(f"units: {e}")
    for key, check in (
        ("findings", finding_error),
        ("observations", observation_error),
    ):
        items = entry.get(key)
        if not isinstance(items, list):
            errors.append(f"{key}가 배열이 아님")
            continue
        errors += [
            f"{key}[{i}]: {e}" for i, x in enumerate(items) if (e := check(x, ids))
        ]
    if (e := diagram_error(entry.get("diagram"), ids)) is not None:
        errors.append(f"diagram: {e}")
    if entry.get("s_candidate") is not None and entry["s_candidate"] not in ids:
        errors.append("s_candidate는 단위 번호 또는 null")
    return errors


def normalized(s):
    return re.sub(r"\s+", "", s)


def duplicate_index():
    """정규화한 문장 → [(포스트 경로, 단위 번호)]. `_drafts`와 `_posts` 전체."""
    index = {}
    for path in list_platform_posts(DRAFTS_DIR) + list_platform_posts(POSTS_DIR):
        with open(path, encoding="utf-8") as f:
            for no, _, body in extract_units(f.read()):
                key = normalized(body)
                if len(key) >= MIN_DUPLICATE_CHARS:
                    index.setdefault(key, []).append((path, no))
    return index


def short(s, n=60):
    return s if len(s) <= n else s[:n] + "…"


def grade(logic, minor, notation_kinds):
    if logic or notation_kinds >= 3:
        return "C"
    return "B" if minor or notation_kinds else "A"


def render(entry, text, units, index):
    """포스트 하나를 출력하고 (이름, 로직, 경미, 표기 종, 예비 등급)을 돌려준다."""
    path = entry["post"]
    name = os.path.splitext(os.path.basename(path))[0]
    print(f"### {name}")
    if entry["source"] == "미확인":
        print("원문 미확인 — S 불가")
    if not idea_is_filled(text):
        print("아이디어 비어 있음 — 작성 필요(평가 불가)\n")
        return name, 0, 0, 0, "평가 불가"

    by_id = {no: (where, body) for no, where, body in units}
    kept, dropped = [], 0
    for f in entry["findings"]:
        if f.get("fragment") and f["fragment"] not in by_id[f["unit"]][1]:
            dropped += 1
        else:
            kept.append(f)

    issues = sorted(lint(path))
    minor_lint = [i for i in issues if i[1] in STRUCTURE_RULES and i[1] != "태그"]
    notation_lint = [i for i in issues if i[1] not in STRUCTURE_RULES]

    logic = sum(1 for f in kept if severity(f) == "로직")
    minor = sum(1 for f in kept if severity(f) == "경미") + len(minor_lint)
    kinds = {("보고", f["rule"]) for f in kept if severity(f) == "표기"} | {
        ("린터", i[1]) for i in notation_lint
    }
    result = grade(logic, minor, len(kinds))

    if issues:
        print("린터:")
        for no, rule, msg in issues:
            print(
                f"  {no}줄 [{rule}] {msg}" + (" (등급 제외)" if rule == "태그" else "")
            )
    if kept:
        print(
            "\n| 단위 | 분류 | 심각도 | 인용 | 근거 |\n| --- | --- | --- | --- | --- |"
        )
        for f in kept:
            quote = f.get("fragment") or short(by_id[f["unit"]][1])
            basis = f["basis"] + (f" (규칙: {f['rule']})" if f.get("rule") else "")
            print(
                f"| {f['unit']} | {f['category']} | {severity(f)} | {cell(quote)} | {cell(basis)} |"
            )
    else:
        print("\n지적 없음")
    print(
        f"\n**건수**: 로직 {logic} / 경미 {minor} / 표기 {len(kinds)}종"
        + (f" · 인용 불일치로 폐기 {dropped}건" if dropped else "")
    )
    print(f"\n**예비 등급: {result}** (S는 오케스트레이터가 판단)")
    if entry.get("s_candidate"):
        print(f"S 후보: {entry['s_candidate']} — {by_id[entry['s_candidate']][1]}")

    purposeless = [no for no, role in entry["units"].items() if role == "없음"]
    if purposeless:
        print("\n**목적 없다고 보고된 단위**(읽고 판단):")
        for no in purposeless:
            print(f"- {no}: {short(by_id[no][1], 90)}")
    copies = []
    for no, _, body in units:
        for other, other_no in index.get(normalized(body), []):
            if other != path:
                copies.append(f"- {no} = {os.path.basename(other)} {other_no}")
    if copies:
        print("\n**다른 포스트와 같은 문장**:\n" + "\n".join(copies))

    if entry["observations"]:
        print("\n> **심화 관찰** (등급 무관, 반영은 선택)")
        for o in entry["observations"]:
            where = f" ({o['unit']})" if o.get("unit") else ""
            print(f"> - **{o['axis']}**{where}: {o['text']}")
    else:
        print("\n심화 관찰: 특이사항 없음")
    d = entry["diagram"]
    if isinstance(d, str):
        print(f"\n**도식 후보**: {d}")
    else:
        print("\n> **도식 후보** (등급 무관, 제작은 승인 후)")
        for c in d:
            print(f"> - {c['unit']} — {c['show']}, {c['format']}, 입력 {c['input']}")
    print()
    return name, logic, minor, len(kinds), result


def load_post(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    return text, extract_units(text)


def check(entry):
    if not isinstance(entry, dict) or not os.path.isfile(str(entry.get("post"))):
        return ["post가 없거나 존재하지 않는 경로"]
    name = os.path.basename(entry["post"])
    return [f"{name}: {e}" for e in entry_errors(entry, *load_post(entry["post"]))]


def main():
    if len(sys.argv) < 2:
        sys.exit("사용법: render_report.py <보고 파일> [...]")
    entries, errors = collect(sys.argv[1:], check)
    exit_on_errors(errors)

    index = duplicate_index()
    rows = [render(e, *load_post(e["post"]), index) for e in entries]
    print(
        "| 드래프트 | 로직 | 경미 | 표기 종 | 예비 등급 |\n| --- | --- | --- | --- | --- |"
    )
    for name, logic, minor, kinds, result in rows:
        print(f"| {cell(name)} | {logic} | {minor} | {kinds} | {result} |")


if __name__ == "__main__":
    main()
