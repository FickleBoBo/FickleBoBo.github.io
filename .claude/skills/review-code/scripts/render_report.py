"""
`review-code` 서브에이전트의 JSON 보고를 검증해 표로 렌더링한다. 인용이 포스트에 글자 그대로 있는지
(`grep -F`에 해당)와 건수 집계는 결정적이라 오케스트레이터 대신 여기서 한다.

사용법:
    render_report.py <보고 파일> [...]

보고 파일은 서브에이전트가 낸 텍스트 그대로다(```json 펜스 한 블록, 형식은 `.claude/agents/code-reviewer.md` `## 출력 형식`).
인용이 포스트에 없는 지적은 폐기하고 포스트별 건수를 보고한다. 형식이 틀리면 사유만 내고 종료 코드 1
(아무것도 렌더링하지 않는다).
"""

import os
import sys

_SKILLS_DIR = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path.insert(0, os.path.abspath(os.path.join(_SKILLS_DIR, "_shared")))

from post_text import classify_fences, section_span
from problem_post import CODE_SECTION_PATTERN
from report_io import cell, collect, exit_on_errors

KINDS = ("정석 여부", "버그/정확성", "언어 관용", "접근 제안", "불필요 요소", "일관성")
VERDICTS = ("정석", "비정석", "불확실")


def filter_quotes(findings, post_text):
    """`quote`가 포스트에 글자 그대로 없는 지적을 걷어낸다. (남은 지적, 폐기 건수)."""
    kept = [f for f in findings if not f.get("quote") or f["quote"] in post_text]
    return kept, len(findings) - len(kept)


def finding_error(f):
    """지적 하나의 형식이 틀리면 사유 문자열, 맞으면 None."""
    if not isinstance(f, dict) or f.get("kind") not in KINDS:
        return f"kind는 {'|'.join(KINDS)} 중 하나"
    if not isinstance(f.get("where"), str) or not f["where"]:
        return "where가 비어 있음"
    if not isinstance(f.get("text"), str):
        return "text가 문자열이 아님"
    if "quote" in f and not isinstance(f["quote"], str):
        return "quote가 문자열이 아님"
    if f["kind"] == "정석 여부":
        if f.get("verdict") not in VERDICTS:
            return f"정석 여부의 verdict는 {'|'.join(VERDICTS)} 중 하나"
        if f["verdict"] != "정석" and not f["text"]:
            return "정석이 아니거나 불확실하면 text(더 일반적인 해·사유)가 필요"
    elif not f["text"]:
        return "text가 비어 있음"
    return None


def entry_errors(entry):
    if not isinstance(entry, dict) or not os.path.isfile(str(entry.get("post"))):
        return ["post가 없거나 존재하지 않는 경로"]
    if entry.get("source") not in ("확인", "미확인"):
        return ["source는 확인|미확인"]
    findings = entry.get("findings")
    if not isinstance(findings, list):
        return ["findings가 배열이 아님"]
    errors = [
        f"findings[{i}]: {e}" for i, f in enumerate(findings) if (e := finding_error(f))
    ]
    with open(entry["post"], encoding="utf-8") as f:
        expected = expected_approaches(f.read())
    rows = [
        f.get("where")
        for f in findings
        if isinstance(f, dict) and f.get("kind") == "정석 여부"
    ]
    if sorted(map(str, rows)) != sorted(expected):
        errors.append(
            f"정석 여부 행의 where는 접근마다 하나씩 {expected}여야 함(지금: {rows})"
        )
    return errors


def expected_approaches(text):
    """코드 섹션의 `### 풀이` 헤딩 수로 정한 접근 이름: 하나면 `풀이`, 여럿이면 `풀이 N`."""
    span = section_span(text, CODE_SECTION_PATTERN)
    lines = text[span[0] : span[1]].split("\n") if span else []
    kinds, _ = classify_fences(lines)
    n = sum(
        1 for ln, k in zip(lines, kinds) if k == "text" and ln.startswith("### 풀이")
    )
    return ["풀이"] if n == 1 else [f"풀이 {i}" for i in range(1, n + 1)]


def is_issue(f):
    return not (f["kind"] == "정석 여부" and f["verdict"] == "정석")


def render(entry):
    """포스트 하나를 출력하고 (이름, 이슈 건수, 정석 여부 요약)을 돌려준다."""
    with open(entry["post"], encoding="utf-8") as f:
        post_text = f.read()
    kept, dropped = filter_quotes(entry["findings"], post_text)
    issues = sum(1 for f in kept if is_issue(f))
    name = os.path.splitext(os.path.basename(entry["post"]))[0]

    print(f"### {name}")
    if entry["source"] == "미확인":
        print("원문 미확인")
    if not issues:
        print("이상없음")
    if dropped:
        print(f"인용 불일치로 폐기 {dropped}건")
    print("\n| 구분 | 위치 | 내용 |\n| --- | --- | --- |")
    for f in kept:
        if f["kind"] == "정석 여부":
            body = f["verdict"] + (f" — {f['text']}" if f["text"] else "")
        else:
            body = f["text"]
        if f.get("quote"):
            body += f" — `{f['quote']}`"
        print(f"| {cell(f['kind'])} | {cell(f['where'])} | {cell(body)} |")
    print()

    verdicts = [(f["where"], f["verdict"]) for f in kept if f["kind"] == "정석 여부"]
    if verdicts and all(v == "정석" for _, v in verdicts):
        summary = "정석"
    else:
        summary = "; ".join(f"{w}: {v}" for w, v in verdicts if v != "정석") or "—"
    return name, issues, summary


def main():
    if len(sys.argv) < 2:
        sys.exit("사용법: render_report.py <보고 파일> [...]")
    entries, errors = collect(sys.argv[1:], entry_errors)
    exit_on_errors(errors)

    rows = [render(e) for e in entries]
    print("| 포스트 | 결과 | 정석 여부 |\n| --- | --- | --- |")
    for name, issues, summary in rows:
        print(
            f"| {cell(name)} | {'이슈 %d건' % issues if issues else '이상없음'} | {cell(summary)} |"
        )


if __name__ == "__main__":
    main()
