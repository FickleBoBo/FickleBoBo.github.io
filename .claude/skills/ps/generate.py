#!/usr/bin/env python3
"""
Generate PS blog post skeletons from the Algorithm solution repo.

Usage:
    python3 generate.py [<YYYY-MM-DD|YYYY-MM>] [problem_numbers...] [--review]
    python3 generate.py                           # no date → every solution on/
                                                  #   after the blog restart that
                                                  #   isn't posted yet (lazy path)
    python3 generate.py 2026-07-24               # one day
    python3 generate.py 2026-07                   # whole month
    python3 generate.py 2026-07 120802 120803     # month, only these numbers
    python3 generate.py 2026-07-24 --review       # include a 리뷰 section

Anything that already has a draft (_drafts/) or a published post (_posts/) is
skipped, so re-running is safe and only fills in what's missing. Existence is
matched on the problem number across every date — one post per problem, since
the slug carries no date — with one exception: a draft still titled TODO (a
title fetch that failed earlier) gets retried and renamed in place.

Sections: 아이디어 / 복잡도 / 코드  (+ 리뷰 only with --review).
Solutions are grouped by approach (Main / Main2 / ...); languages within one
approach share a 풀이 header and one complexity table. With multiple approaches
both 복잡도 and 코드 split into 풀이 1, 풀이 2, ... with matching numbers.

Reads solutions from  ~/Desktop/GITHUB/Algorithm/{YYYY-MM}/src/day_{N}/{platform}_{number}/
Writes skeletons to   ~/Desktop/GITHUB/FickleBoBo.github.io/_drafts/{platform_dir}/

Platforms: prms / leet / cofo   (BOJ and SWEA intentionally not supported — see NOTE below)
Only solutions dated on/after 2026-07-24 are processed.
"""

import json
import re
import sys
import urllib.request
from pathlib import Path

# ── Paths ──────────────────────────────────────
HOME = Path.home()
ALGO_DIR = HOME / "Desktop" / "GITHUB" / "Algorithm"
BLOG_DIR = HOME / "Desktop" / "GITHUB" / "FickleBoBo.github.io"
DRAFTS_DIR = BLOG_DIR / "_drafts"
POSTS_DIR = BLOG_DIR / "_posts"

# Only generate for solutions dated on/after the blog restart.
CUTOFF_DATE = "2026-07-24"

# NOTE: BaekJoon(boj) is intentionally omitted — the online judge has been down
# since 2026-04-28 (no submissions possible), so no new BOJ solutions land here.
# Re-add when BOJ reopens: restore the 'boj' platform config, its title fetcher
# (read from the local crawl mirror at
#  ~/Library/Mobile Documents/com~apple~CloudDocs/baekjoon-crawling/data/problems/{num}.json,
#  since solved.ac is Cloudflare-blocked), and the boj branch in get_problem_link.

# ── Platform / language config ─────────────────
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
        'title_format': '[Codeforces] #{num} - {title}',
    },
}

LANG_ORDER = [
    {'ext': '.java', 'name': 'Java', 'block': 'java'},
    {'ext': '.cpp', 'name': 'C++', 'block': 'c++'},
    {'ext': '.py', 'name': 'Python', 'block': 'python'},
]

CODE_FILE_PREFIXES = ['Main', 'Solution']

FILENAME_SANITIZE = {
    '/': '／', '?': '？', ':': '：', '*': '＊',
    '"': '＂', '<': '＜', '>': '＞', '|': '｜', '\\': '＼',
}


# ── HTTP helpers ───────────────────────────────
def api_get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode('utf-8'))


def api_post(url, data):
    body = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(url, data=body, headers={
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0',
    })
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode('utf-8'))


def url_get_text(url):
    req = urllib.request.Request(url, headers={
        'User-Agent': (
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/120.0.0.0 Safari/537.36'
        ),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'ko-KR,ko;q=0.9,en;q=0.8',
    })
    with urllib.request.urlopen(req, timeout=10) as resp:
        return resp.read().decode('utf-8')


# ── Title fetchers ─────────────────────────────
def fetch_title_prms(number):
    html = url_get_text(
        f"https://school.programmers.co.kr/learn/courses/30/lessons/{number}"
    )
    m = re.search(r'<title>코딩테스트 연습 - (.+?) \| 프로그래머스', html)
    if not m:
        m = re.search(r'<title>(.+?) \| 프로그래머스', html)
    return (m.group(1) if m else None), None


def fetch_title_leet(number):
    # Directory names use the user-facing problem number, which is LeetCode's
    # `questionFrontendId` — NOT the internal `questionId` (they diverge past the
    # early classic problems). Match on frontendId.
    data = api_post("https://leetcode.com/graphql", {
        "query": (
            "query q($categorySlug:String,$limit:Int,$skip:Int,"
            "$filters:QuestionListFilterInput)"
            "{problemsetQuestionList:questionList("
            "categorySlug:$categorySlug limit:$limit skip:$skip "
            "filters:$filters){data{questionFrontendId title titleSlug}}}"
        ),
        "variables": {
            "categorySlug": "",
            "skip": 0,
            "limit": 1,
            "filters": {"searchKeywords": str(number)},
        },
    })
    questions = data['data']['problemsetQuestionList']['data']
    if questions and questions[0]['questionFrontendId'] == str(number):
        return questions[0]['title'], questions[0]['titleSlug']
    return None, None


def fetch_title_cf(number):
    m = re.match(r'(\d+)([A-Za-z]\d?)', str(number))
    if not m:
        return None, None
    contest_id, index = m.group(1), m.group(2).upper()
    data = api_get(
        f"https://codeforces.com/api/contest.standings?"
        f"contestId={contest_id}&from=1&count=1"
    )
    for p in data['result']['problems']:
        if p['index'] == index:
            return p['name'], None
    return None, None


FETCHERS = {
    'prms': fetch_title_prms,
    'leet': fetch_title_leet,
    'cofo': fetch_title_cf,
}


def fetch_title(platform, number):
    try:
        return FETCHERS[platform](number)
    except Exception as e:
        print(f"  [ERROR] Title fetch failed: {e}")
        return None, None


# ── Problem link ───────────────────────────────
def get_problem_link(platform, number, slug=None):
    if platform == 'prms':
        return f"https://school.programmers.co.kr/learn/courses/30/lessons/{number}"
    if platform == 'leet':
        return f"https://leetcode.com/problems/{slug}/" if slug else "TODO"
    if platform == 'cofo':
        m = re.match(r'(\d+)([A-Za-z]\d?)', str(number))
        if m:
            return (
                f"https://codeforces.com/problemset/problem/"
                f"{m.group(1)}/{m.group(2).upper()}"
            )
    return "TODO"


# ── Code reading ───────────────────────────────
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
    # Find which prefix is used (Main or Solution)
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


# ── Post generation ────────────────────────────
def sanitize(name):
    for c, r in FILENAME_SANITIZE.items():
        name = name.replace(c, r)
    return name


def _group_tags(group):
    """'[Java][C++]' for the languages present in one approach group."""
    names = []
    for lang, _ in group:
        if lang['name'] not in names:
            names.append(lang['name'])
    return ''.join(f'[{n}]' for n in names)


def _complexity_table():
    return ['| 시간복잡도 | 공간복잡도 |', '| :-: | :-: |', '|  |  |']


def retitle_draft(path, platform, number, title, link):
    """Fill a real title into a draft that was written with a TODO placeholder.

    Only the front matter title line, a TODO problem link, and the filename are
    touched — the body (아이디어/복잡도 the user may already have written) is
    left exactly as it is.
    """
    plat = PLATFORMS[platform]
    text = path.read_text(encoding='utf-8')

    lines = text.split('\n')
    for i, ln in enumerate(lines):
        if ln.startswith('title: "') and '- TODO' in ln:
            # Every title_format ends in '- {title}', so replacing the first
            # '- TODO' keeps the trailing [Java][C++] language tags intact.
            lines[i] = ln.replace('- TODO', '- ' + title.replace('"', '\\"'), 1)
            break
    text = '\n'.join(lines)
    text = text.replace('[문제 링크](TODO)', f'[문제 링크]({link})')

    date_part = path.name[:10]  # YYYY-MM-DD — keep the draft's original date
    new_path = path.with_name(
        f"{date_part}-{plat['name_ko']} {number} {sanitize(title)}.md"
    )
    new_path.write_text(text, encoding='utf-8')
    if new_path != path:
        path.unlink()
    return new_path


def generate_post(date_str, platform, number, title, groups, link, include_review=False):
    plat = PLATFORMS[platform]

    # Title language tag = union of languages across all approaches (LANG_ORDER).
    seen = []
    for group in groups:
        for lang, _ in group:
            if lang['name'] not in seen:
                seen.append(lang['name'])
    lang_tags = ''.join(f'[{name}]' for name in seen)
    post_title = plat['title_format'].format(num=number, title=title)
    slug = f"{plat['slug_prefix']}-{number}".lower()
    # Escape quotes so a title containing " doesn't break the YAML front matter.
    fm_title = f'{post_title} {lang_tags}'.replace('"', '\\"')

    # One approach → flat sections; multiple approaches → split per 풀이 N,
    # so 복잡도 and 코드 stay parallel and numbering means the same thing.
    multi = len(groups) > 1

    # Section numbers are assigned dynamically so the (optional) 리뷰 section
    # keeps a consistent trailing number.
    sec = iter(range(1, 99))

    lines = [
        '---',
        f'title: "{fm_title}"',
        f'slug: {slug}',
        f'date: {date_str}',
        f"categories: [PS, {plat['category']}]",
        'tags: [Unlinked]',
        'toc: true',
        'math: true',
        '---',
        '',
        f'[문제 링크]({link})',
        '',
        '---',
        '',
        f'## {next(sec)}. 아이디어',
        '',
        '',
        '',
        '---',
        '',
        f'## {next(sec)}. 복잡도',
        '',
    ]

    # 복잡도: one table per approach (labeled 풀이 N when there are several).
    if multi:
        for i, _group in enumerate(groups, 1):
            lines.append(f'### {i}. 풀이')
            lines.append('')
            lines += _complexity_table()
            lines.append('')
    else:
        lines += _complexity_table()
        lines.append('')

    # 코드: languages of one approach grouped under a single 풀이 header.
    lines += ['---', '', f'## {next(sec)}. 코드', '']
    for i, group in enumerate(groups, 1):
        num = f'{i}. ' if multi else ''
        lines.append(f'### {num}풀이 {_group_tags(group)}')
        lines.append('')
        for lang, code in group:
            lines.append(f'```{lang["block"]}')
            lines.append(code)
            lines.append('```')
            lines.append('')

    if include_review:
        lines += ['---', '', f'## {next(sec)}. 리뷰', '', '없음.', '', '---', '']
    else:
        lines += ['---', '']

    return '\n'.join(lines)


# ── Main ───────────────────────────────────────
def process_day(year, month, day, filter_numbers, include_review=False):
    # ASSUMPTION: a source dir named `day_N` maps to calendar day N of that month,
    # so the post date is {year}-{month}-{N}. This is load-bearing in month mode
    # (the date comes only from the dir number). If day_N ever becomes a
    # "study day N" counter instead of a calendar day, month-mode dates break.
    date_str = f"{year}-{month:02d}-{day:02d}"

    if date_str < CUTOFF_DATE:
        print(f"[SKIP] {date_str} < cutoff {CUTOFF_DATE}")
        return 0, 0

    day_dir = ALGO_DIR / f"{year}-{month:02d}" / "src" / f"day_{day:02d}"
    if not day_dir.exists():
        print(f"Error: Not found: {day_dir}")
        return 0, 0

    # Scan problem directories
    problems = []
    for entry in sorted(day_dir.iterdir()):
        if not entry.is_dir():
            continue
        name_lower = entry.name.lower()
        for prefix in PLATFORMS:
            if name_lower.startswith(f'{prefix}_'):
                number = entry.name[len(prefix) + 1:]
                if filter_numbers and number not in filter_numbers:
                    continue
                problems.append((prefix, number, entry))
                break
        else:
            if not filter_numbers:
                print(f"  [SKIP] {entry.name}")

    if not problems:
        print(f"No problems found in {day_dir}")
        return 0, 0

    print(f"Found {len(problems)} problem(s) in {day_dir}\n")

    generated = []
    retitled = []
    for platform, number, problem_dir in problems:
        plat = PLATFORMS[platform]
        print(f"[{plat['name_ko']} {number}]")

        # Match on the number across every date, not just this one: the slug is
        # date-independent (programmers-120583), so a second draft for a problem
        # re-solved on a later day would collide on URL. One post per problem.
        # Globbing the number (not the title) also means a hand-edited title
        # still counts as existing.
        draft_dir = DRAFTS_DIR / plat['post_dir']
        post_subdir = POSTS_DIR / plat['post_dir']
        exist_glob = f"*-{plat['name_ko']} {number} *.md"
        drafts = sorted(draft_dir.glob(exist_glob))
        existing = drafts + sorted(post_subdir.glob(exist_glob))
        # A draft left with a TODO title (transient title-fetch failure) is not
        # "done" — it gets a retry instead of being skipped forever.
        todo_drafts = [p for p in drafts if p.stem.endswith(f" {number} TODO")]
        if existing and not todo_drafts:
            print("  SKIP (already exists)")
            continue

        # Fetch title
        title, extra = fetch_title(platform, number)

        if todo_drafts:
            if not title:
                print("  SKIP (title still TODO — fetch failed again)")
                continue
            link = get_problem_link(platform, number, slug=extra)
            for p in todo_drafts:
                new_path = retitle_draft(p, platform, number, title, link)
                print(f"  Retitled TODO -> {title}: "
                      f"_drafts/{plat['post_dir']}/{new_path.name}")
            retitled.append(todo_drafts[0])
            continue

        if not title:
            title = "TODO"
            print("  Title: TODO (manual input needed)")
        else:
            print(f"  Title: {title}")

        # Read code (grouped by approach)
        groups = read_codes(problem_dir)
        if not groups:
            print("  No code files found. Skipping.")
            continue
        lang_names = []
        for g in groups:
            for lang, _ in g:
                if lang['name'] not in lang_names:
                    lang_names.append(lang['name'])
        print(f"  Approaches: {len(groups)}, Languages: {', '.join(lang_names)}")

        # Generate
        link = get_problem_link(platform, number, slug=extra)
        content = generate_post(date_str, platform, number, title, groups, link,
                                include_review=include_review)

        draft_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{date_str}-{plat['name_ko']} {number} {sanitize(title)}.md"
        draft_path = draft_dir / filename

        draft_path.write_text(content, encoding='utf-8')
        print(f"  Created: _drafts/{plat['post_dir']}/{filename}")
        generated.append(draft_path)

    return len(generated), len(retitled)


def all_day_targets():
    """(year, month, day) for every day_N dir on/after CUTOFF, across all months.

    Used by the no-argument path: sweep the whole Algorithm repo since the blog
    restart and let process_day skip anything that already has a draft/post.
    """
    cutoff_month = CUTOFF_DATE[:7]  # 'YYYY-MM'
    targets = []
    for month_dir in sorted(ALGO_DIR.iterdir()):
        if not month_dir.is_dir() or not re.match(r'\d{4}-\d{2}$', month_dir.name):
            continue
        if month_dir.name < cutoff_month:
            continue
        src = month_dir / "src"
        if not src.exists():
            continue
        year, month = int(month_dir.name[:4]), int(month_dir.name[5:7])
        for d in sorted(src.iterdir()):
            if d.is_dir() and d.name.startswith("day_"):
                try:
                    day_num = int(d.name[len("day_"):])
                except ValueError:
                    continue
                # Day-level cutoff here too, so the cutoff month's pre-restart
                # days (e.g. 07-14/07-15) never enter the sweep in the first place.
                if f"{year}-{month:02d}-{day_num:02d}" < CUTOFF_DATE:
                    continue
                targets.append((year, month, day_num))
    return targets


def main():
    # Separate the --review flag from positional args.
    args = [a for a in sys.argv[1:] if a != '--review']
    include_review = '--review' in sys.argv[1:]

    if not args:
        # Lazy path (the common one): no date → sweep every solution on/after the
        # blog restart and generate a skeleton for any that isn't posted yet.
        filter_numbers = None
        day_targets = all_day_targets()
        if not day_targets:
            print(f"No day_* directories on/after {CUTOFF_DATE} in {ALGO_DIR}.")
            sys.exit(0)
    else:
        date_str = args[0]
        filter_numbers = set(args[1:]) if len(args) >= 2 else None

        parts = date_str.split('-')
        try:
            if len(parts) == 3:
                year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
                day_targets = [(year, month, day)]
            elif len(parts) == 2:
                year, month = int(parts[0]), int(parts[1])
                month_dir = ALGO_DIR / f"{year}-{month:02d}" / "src"
                if not month_dir.exists():
                    print(f"Error: Not found: {month_dir}")
                    sys.exit(1)
                day_targets = []
                for d in sorted(month_dir.iterdir()):
                    if d.is_dir() and d.name.startswith("day_"):
                        try:
                            day_num = int(d.name[len("day_"):])
                        except ValueError:
                            continue
                        day_targets.append((year, month, day_num))
                if not day_targets:
                    print(f"No day_* directories in {month_dir}")
                    sys.exit(0)
            else:
                raise ValueError
        except ValueError:
            print(f"Error: Invalid date '{date_str}'. Use YYYY-MM-DD or YYYY-MM.")
            sys.exit(1)

    total = 0
    total_retitled = 0
    for year, month, day in day_targets:
        made, fixed = process_day(year, month, day, filter_numbers, include_review)
        total += made
        total_retitled += fixed

    summary = f"\nDone. Generated {total} post(s)."
    if total_retitled:
        summary += f" Retitled {total_retitled} TODO draft(s)."
    print(summary)


if __name__ == '__main__':
    main()
