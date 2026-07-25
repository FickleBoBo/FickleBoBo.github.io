#!/usr/bin/env python3
"""
Mechanical pre-check + chunk planning for /review.

Deterministically flags leftover-skeleton problems in PS drafts (empty 아이디어,
unfilled 복잡도 table, missing sections, TODO title/link) and prints a chunk plan
for the Sonnet review agents. It does NOT judge content — that's the LLM's job
(see SKILL.md).

Usage:
    python3 review_check.py                # all drafts in _drafts/
    python3 review_check.py 120807         # this problem (drafts first, then posts)
    python3 review_check.py 120807 1929
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
    targets = find_targets(sys.argv[1:])
    if not targets:
        print("검사할 포스트가 없습니다.")
        return

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


if __name__ == "__main__":
    main()
