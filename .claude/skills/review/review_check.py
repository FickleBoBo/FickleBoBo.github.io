#!/usr/bin/env python3
"""
Mechanical pre-check + chunk planning for /review.

Deterministically flags leftover-skeleton problems in PS drafts (empty 아이디어,
unfilled 복잡도 table, missing sections, TODO title/link) and prints a chunk plan
for the Sonnet review agents. It does NOT judge content — that's the LLM's job
(see SKILL.md).

The `fill` subcommand writes complexity values the reviewer worked out into the
skeleton table. The reviewer decides the values; every mechanical concern (which
rows are blank, whether the count lines up, ordering, refusing to touch published
posts or already-filled tables) is settled here rather than in prose — same split
as tag.py, where the LLM picks the tags and the script does the writing.

Usage:
    python3 review_check.py                # all drafts in _drafts/
    python3 review_check.py 120807         # this problem (drafts first, then posts)
    python3 review_check.py 120807 1929
    python3 review_check.py fill 120809 "O(N)" "O(1)"
    python3 review_check.py fill 12900 "O(N)" "O(N)" "O(N)" "O(1)"   # 접근 2개, 순서대로
"""

import re
import sys
from pathlib import Path

HOME = Path.home()
BLOG_DIR = HOME / "Desktop" / "GITHUB" / "FickleBoBo.github.io"
DRAFTS_DIR = BLOG_DIR / "_drafts"
POSTS_DIR = BLOG_DIR / "_posts"
PS_DIRS = {'programmers', 'leetcode', 'codeforces'}

# A chunk closes at whichever comes first. A single post is never split.
CHUNK_MAX_POSTS = 5
CHUNK_MAX_CHARS = 12000


# ── Target discovery ───────────────────────────
def is_ps(path, root):
    return path.relative_to(root).parts[0] in PS_DIRS


def filename_number(path):
    """The problem-number field of a PS filename, or None."""
    m = re.match(r"\d{4}-\d{2}-\d{2}-.+? (\S+) .+\.md", path.name)
    return m.group(1) if m else None


def find_targets(numbers):
    if numbers:
        targets = []
        for num in numbers:
            found = None
            for root in (DRAFTS_DIR, POSTS_DIR):
                for p in root.rglob("*.md"):
                    # Match the parsed number field, not a substring in the title.
                    if is_ps(p, root) and filename_number(p) == num:
                        found = p
                        break
                if found:
                    break
            if found:
                targets.append(found)
            else:
                print(f"[경고] {num}번 포스트를 찾을 수 없습니다.")
        return targets
    return sorted(p for p in DRAFTS_DIR.rglob("*.md") if is_ps(p, DRAFTS_DIR))


# ── Parsing ────────────────────────────────────
def split_front_matter(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    return (m.group(1), m.group(2)) if m else (None, text)


def sections(body):
    """Split body on '## N. title' headers -> {title: content}."""
    parts = re.split(r"^##\s+\d+\.\s+(.+?)\s*$", body, flags=re.MULTILINE)
    result = {}
    for i in range(1, len(parts), 2):
        title = parts[i].strip()
        result[title] = parts[i + 1] if i + 1 < len(parts) else ""
    return result


# ── Mechanical checks ──────────────────────────
def check(text):
    fm, body = split_front_matter(text)
    issues = []
    if fm is None:
        issues.append("front matter 없음")
        fm = ""

    tm = re.search(r'^title:\s*"?(.+?)"?\s*$', fm, re.MULTILINE)
    if tm and 'TODO' in tm.group(1):
        issues.append("제목 TODO 미기입")
    if re.search(r'\[문제 링크\]\(\s*TODO\s*\)', body):
        issues.append("문제 링크 TODO")

    secs = sections(body)
    for req in ('아이디어', '복잡도', '코드'):
        if req not in secs:
            issues.append(f"'{req}' 섹션 없음")

    # 아이디어 body empty (strip horizontal rules / whitespace)
    if '아이디어' in secs:
        idea = re.sub(r'^-{3,}\s*$', '', secs['아이디어'], flags=re.MULTILINE).strip()
        if not idea:
            issues.append("아이디어 비어있음")

    # 복잡도: any all-blank table data row = unfilled skeleton
    if '복잡도' in secs and _has_blank_table_row(secs['복잡도']):
        issues.append("복잡도 표 미기입")

    # 코드: fenced blocks present, each with a language tag and non-empty body
    if '코드' in secs:
        if '```' not in secs['코드']:
            issues.append("코드블록 없음")
        else:
            if _has_untagged_fence(secs['코드']):
                issues.append("언어 태그 없는 코드블록")
            if _has_empty_code_block(secs['코드']):
                issues.append("빈 코드블록")

    issues += _callout_issues(body)

    return issues


def _callout_issues(body):
    """Chirpy prompt callouts and their Prettier guard.

    A callout is a blockquote closed by a kramdown IAL:

        <!-- prettier-ignore -->
        > 본문
        {: .prompt-tip }

    Prettier treats the IAL line as a lazy continuation of the blockquote and
    rewrites it to `> {: .prompt-tip }`, which makes kramdown attach the class to
    the inner <p> instead of the <blockquote>. The theme selector is
    blockquote[class^='prompt-'], so the styling silently disappears — no error,
    no visible marker in the diff beyond one added '> '. The only reliable guard
    is the prettier-ignore comment, so a missing one is reported before it fires.
    """
    issues = []
    lines = body.split('\n')
    broken = unguarded = 0

    for i, ln in enumerate(lines):
        if re.match(r'^>\s*\{:\s*\.prompt-\w+\s*\}\s*$', ln):
            broken += 1
        elif re.match(r'^\{:\s*\.prompt-\w+\s*\}\s*$', ln):
            # Walk back past the blockquote this IAL closes.
            j = i - 1
            while j >= 0 and lines[j].startswith('>'):
                j -= 1
            if j < 0 or lines[j].strip() != '<!-- prettier-ignore -->':
                unguarded += 1

    if broken:
        issues.append(
            f"콜아웃 깨짐 {broken}건 — '> {{: .prompt-... }}' 형태. "
            "'>' 를 지우고 앞줄에 <!-- prettier-ignore --> 추가"
        )
    if unguarded:
        issues.append(
            f"콜아웃 prettier-ignore 누락 {unguarded}건 — 다음 저장 때 깨짐"
        )
    return issues


def _has_blank_table_row(section):
    for line in section.splitlines():
        s = line.strip()
        if not s.startswith('|'):
            continue
        cells = [c.strip() for c in s.strip('|').split('|')]
        if not ''.join(cells):  # header/separator rows are never blank
            return True
    return False


def _has_untagged_fence(section):
    in_block = False
    for line in section.splitlines():
        s = line.strip()
        if s.startswith('```'):
            if not in_block and not s[3:].strip():
                return True
            in_block = not in_block
    return False


def _has_empty_code_block(section):
    """A tagged fence whose body is blank — e.g. an empty source file got embedded."""
    in_block, body = False, []
    for line in section.splitlines():
        if line.strip().startswith('```'):
            if in_block and not ''.join(body).strip():
                return True
            in_block, body = not in_block, []
        elif in_block:
            body.append(line)
    return False


# ── fill: write complexity values into the skeleton table ──
def _blank_row_indices(lines):
    """Line indices of blank data rows inside the 복잡도 section, in file order.

    Working on whole-file line indices (rather than the section text) is what
    makes the write unambiguous: with several approaches every blank row is the
    byte-identical string '|  |  |', so nothing but position can tell them apart.
    """
    idxs, in_sec = [], False
    for i, line in enumerate(lines):
        m = re.match(r'^##\s+\d+\.\s+(.+?)\s*$', line)
        if m:
            in_sec = m.group(1).strip() == '복잡도'
            continue
        if not in_sec:
            continue
        s = line.strip()
        if not s.startswith('|'):
            continue
        cells = [c.strip() for c in s.strip('|').split('|')]
        if not ''.join(cells):  # header/separator rows always have content
            idxs.append(i)
    return idxs


def _as_math(value):
    """'O(N)' / '$O(N)$' -> '$O(N)$'. The published tables all use $…$."""
    v = value.strip()
    if v.startswith('$') and v.endswith('$') and len(v) > 1:
        return v
    return f'${v}$'


def find_draft(number):
    """fill only ever touches _drafts/ — see cmd_fill."""
    for p in sorted(DRAFTS_DIR.rglob("*.md")):
        if is_ps(p, DRAFTS_DIR) and filename_number(p) == number:
            return p
    return None


def cmd_fill(args):
    if len(args) < 3:
        print("사용법: review_check.py fill <번호> <시간> <공간> [<시간> <공간> ...]")
        return 2
    number, values = args[0], args[1:]

    if len(values) % 2:
        print(f"거부: 값이 {len(values)}개 — 시간·공간을 쌍으로 넘겨야 합니다.")
        return 1
    pairs = list(zip(values[::2], values[1::2]))

    path = find_draft(number)
    if path is None:
        # Published posts are deliberately out of reach: fill is for skeletons.
        if any(is_ps(p, POSTS_DIR) and filename_number(p) == number
               for p in POSTS_DIR.rglob("*.md")):
            print(f"거부: {number}번은 이미 _posts/에 발행된 글입니다. "
                  "발행본 수정은 이 명령의 범위 밖입니다.")
        else:
            print(f"거부: _drafts/에서 {number}번 초안을 찾을 수 없습니다.")
        return 1

    lines = path.read_text(encoding='utf-8').split('\n')
    idxs = _blank_row_indices(lines)

    if not idxs:
        print(f"거부: {path.name} — 복잡도 표에 빈 행이 없습니다. "
              "(이미 채워졌거나 표가 없음. 채워진 값은 덮어쓰지 않습니다.)")
        return 1
    if len(idxs) != len(pairs):
        print(f"거부: 빈 행 {len(idxs)}개인데 값은 {len(pairs)}쌍입니다. "
              "접근(풀이) 수만큼 순서대로 넘기십시오.")
        return 1

    for i, (t, s) in zip(idxs, pairs):
        lines[i] = f"| {_as_math(t)} | {_as_math(s)} |"
    path.write_text('\n'.join(lines), encoding='utf-8')

    print(f"채움: {path.relative_to(BLOG_DIR)}")
    for n, (t, s) in enumerate(pairs, 1):
        label = f"풀이 {n}" if len(pairs) > 1 else "복잡도"
        print(f"  {label}: 시간 {_as_math(t)} / 공간 {_as_math(s)}")

    remaining = check(path.read_text(encoding='utf-8'))
    if any('복잡도' in it for it in remaining):
        print("  ⚠ 기록 후에도 '복잡도 표 미기입'이 남아 있습니다 — 확인 필요.")
        return 1
    print("  ✓ 복잡도 미기입 해소")
    if remaining:
        print("  (남은 다른 이슈: " + ", ".join(remaining) + ")")
    return 0


# ── Chunk planning ─────────────────────────────
def plan_chunks(file_info):
    chunks, cur, cur_chars = [], [], 0
    for path, n in file_info:
        if cur and (len(cur) >= CHUNK_MAX_POSTS or cur_chars + n > CHUNK_MAX_CHARS):
            chunks.append(cur)
            cur, cur_chars = [], 0
        cur.append((path, n))
        cur_chars += n
    if cur:
        chunks.append(cur)
    return chunks


# ── Main ───────────────────────────────────────
def main():
    args = sys.argv[1:]
    if args and args[0] == 'fill':
        return cmd_fill(args[1:])

    targets = find_targets(args)
    if not targets:
        print("검사할 포스트가 없습니다.")
        return 0

    print("=== 기계 검사 ===")
    file_info = []
    for path in targets:
        text = path.read_text(encoding='utf-8')
        issues = check(text)
        print(f"\n[{path.name}]")
        print(f"  {path.relative_to(BLOG_DIR)}")
        if issues:
            for it in issues:
                print(f"  ⚠ {it}")
        else:
            print("  ✓ 기계 검사 통과")
        file_info.append((path, len(text)))

    chunks = plan_chunks(file_info)
    print(f"\n=== 청크 계획 ({len(targets)}개 포스트 → {len(chunks)}개 청크) ===")
    for i, ch in enumerate(chunks, 1):
        total = sum(n for _, n in ch)
        print(f"\n청크 {i} ({len(ch)}개, {total:,}자):")
        for path, _ in ch:
            print(f"  {path}")  # absolute path — pass to the Sonnet agent
    return 0


if __name__ == "__main__":
    sys.exit(main())
