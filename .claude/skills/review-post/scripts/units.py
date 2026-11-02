"""
`review-post`가 평가할 프로즈 단위를 뽑는다: 아이디어 문장(`I`), 코드 섹션의 블록 설명 문단(`C`), 회고
문장(`R`). 서브에이전트는 단위마다 역할을 보고하고 `render_report.py`가 빠진 단위를 잡는다(검토 누락
방지). 두 스크립트가 같은 `extract_units`를 쓰므로 번호가 어긋나지 않는다.

사용법:
    units.py <출력 디렉토리> <포스트 .md 경로> [...]
        <디렉토리>/{slug}.txt에 `번호<TAB>위치<TAB>본문`을 한 줄씩 쓴다.
"""

import os
import re
import sys
from collections import Counter

_SKILLS_DIR = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path.insert(0, os.path.abspath(os.path.join(_SKILLS_DIR, "_shared")))

from post_text import classify_fences, read_front_matter
from problem_post import CODE_SECTION_PATTERN, IDEA_HEADING, RETRO_SECTION_PATTERN

SECTION_LABEL = {"I": "아이디어", "C": "—", "R": "회고"}
# 단위 종류별로 서브에이전트가 매길 수 있는 역할. `없음`은 어느 질문에도 답하지 못하는 단위다
ROLES = {
    "I": ("왜 옳은가", "놓치기 쉬운 조건", "맥락", "없음"),
    "C": ("함정", "지름길", "없음"),
    "R": ("사건", "없음"),
}

# 문장 경계로 보지 않을 구간: 수식, 인라인 코드, 링크 주소
_SPAN_RE = re.compile(r"\$\$.+?\$\$|\$[^$\n]+\$|`[^`\n]+`|\]\([^)\n]*\)", re.DOTALL)
_SENTENCE_END_RE = re.compile(r"[.!?](?=\s|$)")
_ABBREVIATION_RE = re.compile(r"(?:e\.g|i\.e|vs)\.$")
_LIST_MARK_RE = re.compile(r"^(?:[-*]|\d+\.)\s+")
_NON_PROSE_RE = re.compile(r"^(?:!\[.*|\{:.*\})$")  # 이미지, kramdown 속성 줄


def split_sentences(paragraph):
    masked = _SPAN_RE.sub(lambda m: "\0" * len(m.group()), paragraph)
    sentences, start = [], 0
    for m in _SENTENCE_END_RE.finditer(masked):
        if _ABBREVIATION_RE.search(masked[: m.end()]):
            continue
        sentences.append(paragraph[start : m.end()].strip())
        start = m.end()
    sentences.append(paragraph[start:].strip())
    return [s for s in sentences if s]


def _paragraphs(text):
    """(섹션 종류 `I`/`C`/`R`, 풀이 헤딩, 문단). 코드 펜스·HTML 주석·헤딩·구분선·빈 줄이 문단을 끊는다."""
    lines = text.split("\n")
    kinds, _ = classify_fences(lines)
    found, para = [], []
    section = scope = None
    in_comment = False

    def flush():
        if para and section:
            found.append((section, scope, " ".join(para)))
        para.clear()

    for line, kind in zip(lines, kinds):
        s = line.strip()
        if kind != "text":
            flush()
        elif in_comment:
            in_comment = "-->" not in s
        elif s.startswith("<!--"):
            flush()
            in_comment = "-->" not in s
        elif line.startswith("## "):
            flush()
            scope = None
            if s == IDEA_HEADING:
                section = "I"
            elif re.fullmatch(CODE_SECTION_PATTERN, s):
                section = "C"
            elif re.fullmatch(RETRO_SECTION_PATTERN, s):
                section = "R"
            else:
                section = None
        elif line.startswith("### "):
            flush()
            scope = s[4:]
        elif s in ("", "---") or _NON_PROSE_RE.match(s):
            flush()
        else:
            para.append(_LIST_MARK_RE.sub("", s))
    flush()
    return found


def extract_units(text):
    """[(번호, 위치, 본문)]. 번호는 `I1`, `C2`, `R1`처럼 종류별로 1부터."""
    counts = Counter()
    units = []
    for section, scope, para in _paragraphs(text):
        for piece in [para] if section == "C" else split_sentences(para):
            counts[section] += 1
            units.append(
                (f"{section}{counts[section]}", scope or SECTION_LABEL[section], piece)
            )
    return units


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    out_dir = sys.argv[1]
    os.makedirs(out_dir, exist_ok=True)
    failed = 0
    for path in map(os.path.abspath, sys.argv[2:]):
        try:
            with open(path, encoding="utf-8") as f:
                text = f.read()
            _, slug = read_front_matter(text)
        except (OSError, ValueError) as e:
            print(f"에러({path}): {e}")
            failed += 1
            continue
        units = extract_units(text)
        out_path = os.path.join(out_dir, f"{slug}.txt")
        with open(out_path, "w", encoding="utf-8") as f:
            f.writelines(f"{no}\t{where}\t{body}\n" for no, where, body in units)
        counts = Counter(no[0] for no, _, _ in units)
        print(
            f"{out_path} (아이디어 {counts['I']}문장, 코드 설명 {counts['C']}문단, "
            f"회고 {counts['R']}문장)"
        )
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
