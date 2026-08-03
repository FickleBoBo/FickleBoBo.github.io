#!/usr/bin/env python3
"""
Sync PS blog post code blocks with the PS repo source.

Detects drift between a `_drafts/` post's code fences and the PS repo's
current source for that problem, and (only in `apply`) writes the update.
Two kinds of drift:
  - an existing 풀이's code changed (bug fix, refactor, etc.)
  - a new 풀이 was added in the PS repo (e.g. Solution2.java showed up)
    that the draft doesn't have a section for yet

Usage:
    python3 sync.py                    # diff every _drafts/ PS post (no writes)
    python3 sync.py 154538             # diff just this problem
    python3 sync.py apply              # apply drift found in every _drafts/ PS post
    python3 sync.py apply 154538       # apply just this problem

_posts/ (published) is out of scope, same boundary as fill/vars in
../review/review_check.py.

Approach matching is positional and header-text-agnostic: the user is free to
rename "### 1. 풀이" to "### 1. bfs", "### 2. dp", etc. This script only ever
writes code copied verbatim from the PS repo — never content it authors
itself, which is why it's allowed to touch code fences at all (see
../../memory note on PS code being the user's own territory: sync doesn't
generate solutions, it re-syncs a copy of one that already exists). The Nth
`###` block under 코드 is matched to the Nth approach group in the PS repo
(Main/Main2/... or Solution/Solution2/..., grouped by ../_lib/ps_common.py's
read_codes(), shared with generate.py), in file order. Language within an
approach matches by the fence's language tag, not position.

A brand new approach (PS repo has more groups than the draft) gets a new
### N. 풀이 section + a matching empty 복잡도 table, mirroring generate.py's
own multi-approach template. Going from one approach to several also
retrofits the existing (unnumbered) 코드/복잡도 blocks to "1. ..." so the
whole post's numbering stays consistent — the same shape generate.py would
have produced had all approaches existed from the start. Any custom label
the user already gave approach 1 (e.g. renamed "풀이" to "bfs") is preserved;
only the "N. " prefix is added.
"""

import difflib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_lib"))
from ps_common import (  # noqa: E402 — sibling _lib dir, must follow sys.path insert above
    ALGO_DIR, BLOG_DIR, DRAFTS_DIR, PLATFORM_MAP, PS_DIRS,
    LANG_ORDER, EXT_TO_LANG, BLOCK_TO_LANG, read_codes, group_tags,
)


# ── Filename parsing (same regex as ../publish/publish.py) ──
def parse_filename(path):
    m = re.match(r"(\d{4}-\d{2}-\d{2})-(.+?) (\S+) (.+)\.md", path.name)
    if not m:
        return None
    date_str, platform_ko, number = m.group(1), m.group(2), m.group(3)
    prefix = PLATFORM_MAP.get(platform_ko)
    if not prefix:
        return None
    y, mo, d = date_str.split("-")
    return {
        'date': date_str, 'platform_ko': platform_ko, 'prefix': prefix,
        'number': number, 'year_month': f"{y}-{mo}", 'day': int(d),
    }


def is_ps_draft(path):
    return path.relative_to(DRAFTS_DIR).parts[0] in PS_DIRS


def find_drafts(number):
    return [p for p in sorted(DRAFTS_DIR.rglob("*.md"))
            if is_ps_draft(p) and (parsed := parse_filename(p)) and parsed['number'] == number]


def all_draft_numbers():
    numbers = []
    for p in sorted(DRAFTS_DIR.rglob("*.md")):
        if is_ps_draft(p):
            parsed = parse_filename(p)
            if parsed:
                numbers.append(parsed['number'])
    return numbers


# ── PS repo reading (grouping logic lives in ps_common.read_codes) ──
def resolve_problem_dir(parsed):
    return (ALGO_DIR / parsed['year_month'] / "src" / f"day_{parsed['day']:02d}"
            / f"{parsed['prefix']}_{parsed['number']}")


# ── Draft section/approach parsing ─────────────
def find_section(lines, title):
    """[start, end) body line range for '## N. {title}'. end may run past the
    trailing '---' divider into EOF when 코드 is the last section — callers
    that insert content locate the true content boundary themselves rather
    than trusting `end` as an insertion point."""
    start = None
    for i, line in enumerate(lines):
        if re.match(r'^##\s+\d+\.\s+', line):
            if start is not None:
                return start, i
            if re.match(rf'^##\s+\d+\.\s+{re.escape(title)}\s*$', line):
                start = i + 1
    if start is None:
        return None
    return start, len(lines)


def find_h3_blocks(lines, start, end):
    """[(header_idx, body_start, body_end), ...] within [start, end)."""
    h3_idxs = [i for i in range(start, end) if re.match(r'^###\s+', lines[i])]
    blocks = []
    for j, hi in enumerate(h3_idxs):
        body_start = hi + 1
        body_end = h3_idxs[j + 1] if j + 1 < len(h3_idxs) else end
        blocks.append((hi, body_start, body_end))
    return blocks


def find_fences(lines, start, end):
    """[{'lang', 'code_start', 'code_end'}, ...] within [start, end).

    code_end is the index of the closing '```' line itself (not included in
    the code body) so callers can locate "right after this fence" as
    code_end + 1 without re-deriving it.
    """
    fences = []
    i = start
    while i < end:
        m = re.match(r'^```(\S+)\s*$', lines[i])
        if m:
            j = i + 1
            while j < end and lines[j].strip() != '```':
                j += 1
            fences.append({'lang': m.group(1), 'code_start': i + 1, 'code_end': j})
            i = j + 1
        else:
            i += 1
    return fences


def strip_tags(header_text):
    """'풀이 [Java][C++]' -> '풀이'. '1. bfs [Java]' -> '1. bfs'."""
    return re.sub(r'(\s*\[[^\[\]]+\])+\s*$', '', header_text).strip()


def strip_number(label):
    """'1. bfs' -> 'bfs'. 'bfs' -> 'bfs' (no leading number to begin with)."""
    m = re.match(r'^\d+\.\s*(.*)$', label)
    return m.group(1) if m else label


def parse_code_approaches(lines, code_bounds):
    start, end = code_bounds
    approaches = []
    for header_idx, body_start, body_end in find_h3_blocks(lines, start, end):
        header_text = re.sub(r'^###\s+', '', lines[header_idx])
        label = strip_number(strip_tags(header_text))
        by_ext = {}
        for f in find_fences(lines, body_start, body_end):
            lang = BLOCK_TO_LANG.get(f['lang'])
            if lang:
                by_ext[lang['ext']] = f
        approaches.append({'header_idx': header_idx, 'label': label, 'fences': by_ext})
    return approaches


def complexity_h3_indices(lines, complexity_bounds):
    start, end = complexity_bounds
    return [i for i in range(start, end) if re.match(r'^###\s+', lines[i])]


def last_content_line(lines, start, end, prefixes):
    """Highest line index in [start, end) whose stripped text starts with any
    of `prefixes` — used to find "end of real content" while ignoring the
    trailing blank-line-then-'---' padding find_section's `end` includes."""
    idxs = [i for i in range(start, end) if lines[i].strip().startswith(prefixes)]
    return max(idxs) if idxs else None


# ── Drift detection ─────────────────────────────
def compute_drift(path):
    """Returns a drift dict, or None (with a message already printed) if this
    post can't be safely analyzed."""
    parsed = parse_filename(path)
    if not parsed:
        print(f"[경고] 파일명 파싱 실패: {path.name}")
        return None

    problem_dir = resolve_problem_dir(parsed)
    if not problem_dir.exists():
        print(f"[경고] {parsed['number']} — PS 레포 경로 없음: "
              f"{problem_dir.relative_to(ALGO_DIR)} (이동됐거나 _fail/_ignore로 바뀜)")
        return None

    ps_groups = read_codes(problem_dir)
    if not ps_groups:
        print(f"[경고] {parsed['number']} — PS 레포에 코드 파일 없음: {problem_dir}")
        return None

    lines = path.read_text(encoding='utf-8').split('\n')
    code_bounds = find_section(lines, '코드')
    complexity_bounds = find_section(lines, '복잡도')
    if not code_bounds or not complexity_bounds:
        print(f"[경고] {parsed['number']} — 코드/복잡도 섹션을 찾을 수 없음")
        return None

    draft_approaches = parse_code_approaches(lines, code_bounds)
    if not draft_approaches:
        print(f"[경고] {parsed['number']} — 코드 섹션에서 풀이를 찾을 수 없음")
        return None
    complexity_h3 = complexity_h3_indices(lines, complexity_bounds)

    n_code = len(draft_approaches)
    n_complexity = len(complexity_h3) if complexity_h3 else 1
    if n_code != n_complexity:
        print(f"[경고] {parsed['number']} — 코드 풀이 {n_code}개 vs 복잡도 표 {n_complexity}개, "
              f"구조가 어긋나 건너뜀 (수동 확인 필요)")
        return None
    if len(draft_approaches) == 1 and complexity_h3:
        print(f"[경고] {parsed['number']} — 코드 풀이는 1개인데 복잡도는 이미 번호형입니다, "
              f"건너뜀 (수동 확인 필요)")
        return None

    changes, missing_lang, dropped, dropped_lang = [], [], [], []
    for idx, approach in enumerate(draft_approaches):
        if idx >= len(ps_groups):
            dropped.append(idx + 1)
            continue
        ps_by_ext = {lang['ext']: code for lang, code in ps_groups[idx]}
        for ext, fence in approach['fences'].items():
            new_code = ps_by_ext.get(ext)
            if new_code is None:
                continue
            old_code = '\n'.join(lines[fence['code_start']:fence['code_end']])
            if old_code.strip() != new_code.strip():
                changes.append({'approach_idx': idx, 'label': approach['label'],
                                 'lang': EXT_TO_LANG[ext], 'fence': fence,
                                 'old': old_code, 'new': new_code})
        # Both directions, reported in LANG_ORDER so output is deterministic.
        extra_langs = set(ps_by_ext) - set(approach['fences'])
        if extra_langs:
            missing_lang.append((idx + 1, approach['label'],
                                  [l['name'] for l in LANG_ORDER if l['ext'] in extra_langs]))
        # The draft has a language the PS repo no longer does: that fence is
        # stale forever and no diff would ever surface it, so warn explicitly.
        gone_langs = set(approach['fences']) - set(ps_by_ext)
        if gone_langs:
            dropped_lang.append((idx + 1, approach['label'],
                                  [l['name'] for l in LANG_ORDER if l['ext'] in gone_langs]))

    new_approaches = ps_groups[len(draft_approaches):]
    if new_approaches:
        # apply_drift anchors new sections to the last code fence and the last
        # 복잡도 table row. Without either, it would die on max()/next()/None+1,
        # so drop the insert (keeping any code changes) and tell the user.
        has_fence = any(a['fences'] for a in draft_approaches)
        has_table_row = any(lines[i].strip().startswith('|')
                            for i in range(complexity_bounds[0], complexity_bounds[1]))
        if not has_fence or not has_table_row:
            print(f"[경고] {parsed['number']} — 새 풀이 {len(new_approaches)}개의 삽입 지점을 "
                  f"찾을 수 없어(코드펜스/복잡도 표 없음) 신설을 건너뜁니다 (수동 확인 필요)")
            new_approaches = []

    return {
        'path': path, 'parsed': parsed, 'lines': lines,
        'code_bounds': code_bounds, 'complexity_bounds': complexity_bounds,
        'complexity_h3': complexity_h3, 'draft_approaches': draft_approaches,
        'ps_groups': ps_groups, 'changes': changes, 'new_approaches': new_approaches,
        'missing_lang': missing_lang, 'dropped': dropped, 'dropped_lang': dropped_lang,
    }


# ── Report ───────────────────────────────────────
def label_of(drift, idx0, label):
    n = len(drift['draft_approaches'])
    tag = f"풀이 {idx0 + 1}" if n > 1 else "풀이"
    if label and label != '풀이':
        tag += f" ({label})"
    return tag


def print_diff_report(drift):
    p = drift['parsed']
    print(f"\n[{p['number']}] {p['platform_ko']} {p['number']}")

    if not any([drift['changes'], drift['new_approaches'], drift['missing_lang'],
                drift['dropped'], drift['dropped_lang']]):
        print("  변경 없음")
        return

    for ch in drift['changes']:
        print(f"  {label_of(drift, ch['approach_idx'], ch['label'])} "
              f"[{ch['lang']['name']}]: 변경됨")
        diff = difflib.unified_diff(ch['old'].splitlines(), ch['new'].splitlines(),
                                     lineterm='')
        for d in diff:
            if d.startswith(('---', '+++', '@@')):
                continue
            print(f"    {d}")

    base = len(drift['draft_approaches'])
    for offset, group in enumerate(drift['new_approaches']):
        langs = ', '.join(l['name'] for l, _ in group)
        print(f"  풀이 {base + offset + 1}: PS 레포에 새로 추가됨 ({langs}) — apply 시 섹션 신설")

    for idx1, label, langs in drift['missing_lang']:
        tag = f"풀이 {idx1}" + (f" ({label})" if label != '풀이' else '')
        print(f"  {tag}: PS 레포에 있는 언어 {', '.join(langs)}가 드래프트엔 없음 — 수동 추가 필요")

    for idx1, label, langs in drift['dropped_lang']:
        tag = f"풀이 {idx1}" + (f" ({label})" if label != '풀이' else '')
        print(f"  {tag}: 드래프트의 {', '.join(langs)} 코드가 PS 레포에서 사라짐 "
              f"— 그 코드블록은 갱신되지 않습니다 (자동 삭제 안 함, 수동 확인 필요)")

    for idx1 in drift['dropped']:
        print(f"  풀이 {idx1}: PS 레포에서 소스가 사라짐 — 수동 확인 필요 (자동 삭제 안 함)")


# ── Apply ────────────────────────────────────────
def apply_drift(drift):
    lines = list(drift['lines'])
    edits = []  # (start, end, new_lines), applied bottom-up

    for ch in drift['changes']:
        edits.append((ch['fence']['code_start'], ch['fence']['code_end'], ch['new'].split('\n')))

    n_new = len(drift['new_approaches'])
    if n_new:
        draft_approaches = drift['draft_approaches']
        going_multi = len(draft_approaches) == 1 and not drift['complexity_h3']
        start_idx = len(draft_approaches) + 1

        if going_multi:
            hdr_idx = draft_approaches[0]['header_idx']
            hdr_text = re.sub(r'^###\s+', '', lines[hdr_idx])
            edits.append((hdr_idx, hdr_idx + 1, [f"### 1. {hdr_text}"]))

            comp_start, comp_end = drift['complexity_bounds']
            t_start = next(i for i in range(comp_start, comp_end)
                            if lines[i].strip().startswith('|'))
            t_last = last_content_line(lines, comp_start, comp_end, ('|', '>'))
            label1 = draft_approaches[0]['label'] or '풀이'
            edits.append((t_start, t_last + 1,
                          [f"### 1. {label1}", ''] + lines[t_start:t_last + 1]))

        # New 코드 sections — right after the last existing fence.
        code_insert_at = max(f['code_end'] for a in draft_approaches
                              for f in a['fences'].values()) + 1
        code_lines = []
        for offset, group in enumerate(drift['new_approaches']):
            i = start_idx + offset
            code_lines += ['', f"### {i}. 풀이 {group_tags(group)}", '']
            for j, (lang, code) in enumerate(group):
                code_lines.append(f"```{lang['block']}")
                code_lines.extend(code.split('\n'))
                code_lines.append('```')
                if j != len(group) - 1:
                    code_lines.append('')
        edits.append((code_insert_at, code_insert_at, code_lines))

        # New 복잡도 tables — right after the last existing table/note line.
        comp_start, comp_end = drift['complexity_bounds']
        comp_insert_at = last_content_line(lines, comp_start, comp_end, ('|', '>')) + 1
        comp_lines = []
        for offset in range(n_new):
            i = start_idx + offset
            comp_lines += ['', f"### {i}. 풀이", '',
                            '| 시간복잡도 | 공간복잡도 |', '| :-: | :-: |', '|  |  |']
        edits.append((comp_insert_at, comp_insert_at, comp_lines))

    edits.sort(key=lambda e: e[0], reverse=True)
    for start, end, new_lines in edits:
        lines[start:end] = new_lines

    drift['path'].write_text('\n'.join(lines), encoding='utf-8')


def print_apply_report(drift):
    p = drift['parsed']
    print(f"\n[{p['number']}] {p['platform_ko']} {p['number']} — 적용")
    for ch in drift['changes']:
        print(f"  {label_of(drift, ch['approach_idx'], ch['label'])} [{ch['lang']['name']}] 갱신")
    base = len(drift['draft_approaches'])
    for offset, group in enumerate(drift['new_approaches']):
        langs = ', '.join(l['name'] for l, _ in group)
        print(f"  풀이 {base + offset + 1} 신설 ({langs}) + 빈 복잡도 표")
    print(f"  기록: {drift['path'].relative_to(BLOG_DIR)}")


# ── Main ─────────────────────────────────────────
def main():
    args = sys.argv[1:]
    do_apply = bool(args) and args[0] == 'apply'
    if do_apply:
        args = args[1:]

    numbers = args or all_draft_numbers()
    if not numbers:
        print("_drafts/에 PS 포스트가 없습니다.")
        return 0

    mode = "적용" if do_apply else "동기화 검사"
    print(f"=== 코드 {mode} ===")

    any_drift = False
    for number in numbers:
        drafts = find_drafts(number)
        if not drafts:
            print(f"\n[경고] {number} — _drafts/에서 찾을 수 없음")
            continue
        if len(drafts) > 1:
            print(f"\n[경고] {number} — 여러 개 매칭됨, 건너뜀:")
            for d in drafts:
                print(f"  {d.relative_to(BLOG_DIR)}")
            continue

        drift = compute_drift(drafts[0])
        if drift is None:
            continue

        has_drift = bool(drift['changes'] or drift['new_approaches'])
        any_drift = any_drift or has_drift

        if do_apply:
            if has_drift:
                apply_drift(drift)
                print_apply_report(drift)
            else:
                print(f"\n[{drift['parsed']['number']}] 변경 없음 — 건너뜀")
            if drift['missing_lang'] or drift['dropped'] or drift['dropped_lang']:
                print("  (수동 확인 필요 항목이 있습니다 — 위 diff 모드로 다시 확인하세요)")
        else:
            print_diff_report(drift)

    if not do_apply and any_drift:
        print("\n반영하려면: python3 sync.py apply [<번호>...]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
