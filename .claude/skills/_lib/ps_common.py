#!/usr/bin/env python3
"""Shared PS-post infra for the ps and sync skills.

Platform registry, source-file grouping (Main/Main2/... by language), and the
Java package/class rewrite used when embedding PS repo source into a post.
generate.py and sync.py both read PS repo solutions the same way, so this is
the single source of truth for "what counts as a platform" and "how to read
one problem's code" — see memory:sync-skill for the duplication this replaces.

Not a skill itself (no SKILL.md) — sibling skill scripts reach it via
sys.path, the same pattern review_check.py already uses to import sync.py.
"""

import re
from pathlib import Path

# ── Paths ──────────────────────────────────────
HOME = Path.home()
ALGO_DIR = HOME / "Desktop" / "github" / "PS"
BLOG_DIR = HOME / "Desktop" / "github" / "FickleBoBo.github.io"
DRAFTS_DIR = BLOG_DIR / "_drafts"
POSTS_DIR = BLOG_DIR / "_posts"

# ── Platform registry ───────────────────────────
# Single source of truth: PLATFORM_MAP and PS_DIRS are both derived from this,
# so adding a platform (e.g. BOJ on reopen) only means editing this dict.
#
# title_format's '번' suffix rule: it attaches to a number, so it's used
# wherever the problem is identified by one (BOJ 1000번 / LeetCode 704번 /
# Programmers 154540번 — the last is really a lesson id the site never
# displays, but Korean PS writing has settled on referring to it that way).
# Codeforces is the exception: '2148A' is contest id + slot letter, not a
# number, so it takes no suffix — and no '#' either, which Codeforces uses
# for round numbers rather than problems.
PLATFORMS = {
    'prms': {
        'name_ko': '프로그래머스',
        'post_dir': 'programmers',
        'slug_prefix': 'programmers',
        'category': 'Programmers',
        'title_format': '[Programmers] {num}번 - {title}',
    },
    'leet': {
        'name_ko': '리트코드',
        'post_dir': 'leetcode',
        'slug_prefix': 'leetcode',
        'category': 'LeetCode',
        'title_format': '[LeetCode] {num}번 - {title}',
    },
    'cofo': {
        'name_ko': '코드포스',
        'post_dir': 'codeforces',
        'slug_prefix': 'codeforces',
        'category': 'Codeforces',
        'title_format': '[Codeforces] {num} - {title}',
    },
}
# NOTE: BaekJoon(boj) is intentionally omitted — the online judge has been
# down since 2026-04-28 (no submissions possible), so no new BOJ solutions
# land here. Re-add when BOJ reopens: restore a 'boj' entry above, its title
# fetcher in generate.py (read from the local crawl mirror at
#  ~/Library/Mobile Documents/com~apple~CloudDocs/baekjoon-crawling/data/problems/{num}.json,
#  since solved.ac is Cloudflare-blocked), and the boj branch in
#  generate.py's get_problem_link.

PLATFORM_MAP = {p['name_ko']: prefix for prefix, p in PLATFORMS.items()}
PS_DIRS = {p['post_dir'] for p in PLATFORMS.values()}

# ── Language / source file config ───────────────
LANG_ORDER = [
    {'ext': '.java', 'name': 'Java', 'block': 'java'},
    {'ext': '.cpp', 'name': 'C++', 'block': 'c++'},
    {'ext': '.py', 'name': 'Python', 'block': 'python'},
]
EXT_TO_LANG = {l['ext']: l for l in LANG_ORDER}
BLOCK_TO_LANG = {l['block']: l for l in LANG_ORDER}
CODE_FILE_PREFIXES = ['Main', 'Solution']


def process_java(code):
    code = re.sub(r'package\s+[\w.]+;\s*\n*', '', code)
    code = re.sub(r'(class\s+)(Main|Solution)\d+', r'\1\2', code)
    return code.strip()


def read_codes(problem_dir):
    """Return solutions grouped by approach.

    Each suffix group (Main / Main2 / ...) is one approach; the languages
    within it share the same algorithm (and thus complexity).
    Returns [[(lang, code), ...], ...] — one inner list per approach.
    """
    prefix = None
    for p in CODE_FILE_PREFIXES:
        if any((problem_dir / f"{p}{lang['ext']}").exists() for lang in LANG_ORDER):
            prefix = p
            break
    if not prefix:
        return []
    # Approaches in order: Main (''), Main2 ('2'), Main3 ('3'), ...
    suffixes = ['']
    n = 2
    while True:
        if any((problem_dir / f"{prefix}{n}{lang['ext']}").exists() for lang in LANG_ORDER):
            suffixes.append(str(n))
            n += 1
        else:
            break
    groups = []
    for suffix in suffixes:
        group = []
        for lang in LANG_ORDER:
            fp = problem_dir / f"{prefix}{suffix}{lang['ext']}"
            if fp.exists():
                code = fp.read_text(encoding='utf-8')
                code = process_java(code) if lang['ext'] == '.java' else code.strip()
                group.append((lang, code))
        if group:
            groups.append(group)
    return groups


def group_tags(group):
    """'[Java][C++]' for the languages present in one approach group."""
    names = []
    for lang, _ in group:
        if lang['name'] not in names:
            names.append(lang['name'])
    return ''.join(f'[{n}]' for n in names)
