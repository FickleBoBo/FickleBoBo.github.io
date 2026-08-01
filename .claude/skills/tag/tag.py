#!/usr/bin/env python3
"""
Tag engine for PS posts — closed-vocabulary tagging with auto-companion ancestry.

Usage:
    python3 tag.py                                        # list _drafts PS posts + tag state
    python3 tag.py <number> <leaf-tag> [<leaf-tag> ...]   # apply tags to a post
    python3 tag.py audit [<number>]                       # audit posts against the vocab
    python3 tag.py vocab                                  # self-check tags.md only

Leaf tags are the *specific* tags you choose; the parent chain is auto-expanded
(dijkstra -> shortest path -> graph) and written flat into the post's front
matter. Only tags defined in tags.md are allowed; the audit flags the rest.
Tag names with a fullwidth slash (e.g. "hash set／hash map") must be typed with
that character (U+FF0F), not a plain '/'.
"""

import re
import sys
from pathlib import Path

HOME = Path.home()
BLOG_DIR = HOME / "Desktop" / "github" / "FickleBoBo.github.io"
DRAFTS_DIR = BLOG_DIR / "_drafts"
POSTS_DIR = BLOG_DIR / "_posts"
PS_DIRS = {'programmers', 'leetcode', 'codeforces'}
TAGS_FILE = Path(__file__).parent / "tags.md"
UNLINKED = "Unlinked"


# ── Vocabulary ─────────────────────────────────
def parse_tags_md(path=TAGS_FILE):
    """Parse tags.md into {tag: {parent, attach_when, attach_policy, auto_companion, note}}."""
    tags, cur, fields = {}, None, {}
    for raw in path.read_text(encoding='utf-8').splitlines():
        line = raw.rstrip()
        m = re.match(r'^\[([^\]]+)\]\s*$', line)
        if m:
            if cur is not None:
                tags[cur] = fields
            cur = m.group(1).strip()
            fields = {'parent': None, 'attach_when': None, 'attach_policy': None,
                      'auto_companion': True, 'note': None}
            continue
        if line == '' and cur is not None:
            tags[cur] = fields
            cur, fields = None, {}
            continue
        if cur is not None:
            fm = re.match(r'^(\w+):\s*(.*)$', line)
            if fm:
                k, v = fm.group(1).strip(), fm.group(2).strip()
                if k == 'auto_companion':
                    fields['auto_companion'] = v.lower() != 'false'
                elif k in fields:
                    fields[k] = v or None
    if cur is not None:
        tags[cur] = fields
    return tags


def compute_ancestry(tag, tags):
    """Ancestor chain (immediate parent -> root), excluding the tag itself."""
    chain, cur, seen = [], tags.get(tag, {}).get('parent'), set()
    while cur and cur not in seen:
        seen.add(cur)
        chain.append(cur)
        cur = tags.get(cur, {}).get('parent')
    return chain


def _depth(tag, tags):
    d, cur, seen = 0, tags.get(tag, {}).get('parent'), set()
    while cur and cur not in seen:
        seen.add(cur)
        d += 1
        cur = tags.get(cur, {}).get('parent')
    return d


def expand_with_ancestry(leaves, tags):
    """Expand leaf tags to include full ancestry (respecting auto_companion=false).
    Sorted root-first. Unknown tags are kept as-is so the audit can flag them."""
    result = set()
    for tag in leaves:
        result.add(tag)
        if tag in tags:
            for anc in compute_ancestry(tag, tags):
                if tags.get(anc, {}).get('auto_companion', True):
                    result.add(anc)
    return sorted(result, key=lambda t: (_depth(t, tags), t))


# ── Post front matter ──────────────────────────
def read_post_tags(path):
    m = re.match(r'^---\n(.*?)\n---', path.read_text(encoding='utf-8'), re.DOTALL)
    if not m:
        return None
    tm = re.search(r'^tags:\s*\[(.*?)\]\s*$', m.group(1), re.MULTILINE)
    if not tm:
        return []
    inner = tm.group(1).strip()
    return [t.strip() for t in inner.split(',')] if inner else []


def write_post_tags(path, new_tags):
    text = path.read_text(encoding='utf-8')
    fm_m = re.match(r'^(---\n.*?\n---)(.*)$', text, re.DOTALL)
    if not fm_m:
        raise ValueError(f"front matter 없음: {path.name}")
    fm, rest = fm_m.group(1), fm_m.group(2)
    tags_str = 'tags: [' + ', '.join(new_tags) + ']'
    new_fm, n = re.subn(r'(?m)^tags:\s*\[.*?\]\s*$', tags_str, fm, count=1)
    if n == 0:
        raise ValueError(f"tags 필드 없음: {path.name}")
    path.write_text(new_fm + rest, encoding='utf-8')


def filename_number(path):
    m = re.match(r"\d{4}-\d{2}-\d{2}-.+? (\S+) .+\.md", path.name)
    return m.group(1) if m else None


def find_post(number):
    for root in (DRAFTS_DIR, POSTS_DIR):
        for p in root.rglob("*.md"):
            if p.relative_to(root).parts[0] in PS_DIRS and filename_number(p) == number:
                return p
    return None


def find_all_posts():
    posts = []
    for root in (DRAFTS_DIR, POSTS_DIR):
        if root.exists():
            posts += [p for p in root.rglob("*.md")
                      if p.relative_to(root).parts[0] in PS_DIRS]
    return sorted(posts)


def find_draft_posts():
    """PS posts under _drafts — the publish-pending (just-reviewed) set."""
    if not DRAFTS_DIR.exists():
        return []
    return sorted(p for p in DRAFTS_DIR.rglob("*.md")
                  if p.relative_to(DRAFTS_DIR).parts[0] in PS_DIRS)


# ── Audit ──────────────────────────────────────
def audit_vocab(tags):
    issues = []
    for name, f in tags.items():
        parent = f.get('parent')
        if parent and parent not in tags:
            issues.append(f"[{name}] parent '{parent}' 미정의")
        if not f.get('attach_when'):
            issues.append(f"[{name}] attach_when 없음")
        if name != name.lower():
            issues.append(f"[{name}] 소문자 아님")
        if '  ' in name:
            issues.append(f"[{name}] 이중 공백")
    for name in tags:  # cycle detection
        seen, cur = set(), name
        while cur:
            if cur in seen:
                issues.append(f"[{name}] 사이클 ({cur})")
                break
            seen.add(cur)
            cur = tags.get(cur, {}).get('parent')
    return issues


def audit_post(path, tags):
    found = []
    post_tags = read_post_tags(path)
    if post_tags is None:
        return [f"front matter 없음"]
    if not post_tags:
        return ["tags 비어있음"]
    if post_tags == [UNLINKED]:
        return None  # sentinel — not yet tagged
    for t in post_tags:
        if t not in tags:
            found.append(f"미정의 태그 '{t}'")
    known = [t for t in post_tags if t in tags]
    expected = set()
    for t in known:
        expected.add(t)
        for anc in compute_ancestry(t, tags):
            if tags.get(anc, {}).get('auto_companion', True):
                expected.add(anc)
    for miss in sorted(expected - set(post_tags)):
        found.append(f"조상 태그 누락 '{miss}'")
    for t in known:
        if not tags.get(t, {}).get('auto_companion', True):
            found.append(f"'{t}'는 부착 금지(auto_companion=false)")
    return found


# ── Commands ───────────────────────────────────
def cmd_apply(number, leaves):
    tags = parse_tags_md()
    unknown = [t for t in leaves if t not in tags]
    if unknown:
        print("Error: 어휘에 없는 태그 — tags.md에 정의된 것만 사용:")
        for t in unknown:
            print(f"  '{t}'")
        sys.exit(1)
    post = find_post(number)
    if not post:
        print(f"Error: {number}번 포스트를 찾을 수 없습니다.")
        sys.exit(1)
    before = read_post_tags(post)
    expanded = expand_with_ancestry(leaves, tags)
    write_post_tags(post, expanded)
    print(f"[{post.relative_to(BLOG_DIR)}]")
    print(f"  이전: [{', '.join(before)}]")
    print(f"  이후: [{', '.join(expanded)}]")
    print(f"  (leaf {len(leaves)}개 → ancestry 확장 {len(expanded)}개)")


def cmd_audit(number):
    tags = parse_tags_md()
    vissues = audit_vocab(tags)
    if vissues:
        print(f"[vocab] {len(vissues)}개 문제 — tags.md 먼저 고칠 것:")
        for i in vissues:
            print(f"  - {i}")
        sys.exit(1)
    posts = [find_post(number)] if number else find_all_posts()
    posts = [p for p in posts if p]
    checked = unlinked = total = 0
    for p in posts:
        checked += 1
        issues = audit_post(p, tags)
        if issues is None:
            unlinked += 1
            continue
        if issues:
            total += len(issues)
            print(f"[{p.name}]")
            for i in issues:
                print(f"  ⚠ {i}")
    print(f"\n검사 {checked}개 (미태깅 {unlinked}개), 문제 {total}건")
    sys.exit(0 if total == 0 else 1)


def cmd_list():
    """No-arg: list _drafts PS posts with tag state, for the LLM to tag each."""
    tags = parse_tags_md()
    posts = find_draft_posts()
    if not posts:
        print("_drafts에 PS 포스트가 없습니다.")
        return
    untagged = 0
    print(f"=== _drafts PS 포스트 {len(posts)}개 (인자 없음 → 태깅 대상) ===\n")
    for p in posts:
        cur = read_post_tags(p)
        num = filename_number(p)
        is_untagged = cur == [UNLINKED]
        untagged += is_untagged
        state = "미태깅" if is_untagged else f"이미 태깅됨 [{', '.join(cur)}]"
        print(f"[{num}] {state}")
        print(f"  {p}")
    print(f"\n미태깅 {untagged}개 / 전체 {len(posts)}개. "
          f"미태깅 포스트를 각각 읽고 leaf 선정 → 부착한다(이미 태깅된 건 건너뜀).")


def cmd_vocab():
    tags = parse_tags_md()
    attachable = sum(1 for f in tags.values() if f.get('auto_companion', True))
    print(f"어휘 {len(tags)}개 로드 ({attachable} attachable + {len(tags)-attachable} auto_companion=false)")
    issues = audit_vocab(tags)
    if issues:
        print(f"\n[vocab] {len(issues)}개 문제:")
        for i in issues:
            print(f"  - {i}")
        sys.exit(1)
    print("✓ 어휘 자체검증 통과.")


def main():
    args = sys.argv[1:]
    if not args:
        cmd_list()
        sys.exit(0)
    if args[0] == 'vocab':
        cmd_vocab()
    elif args[0] == 'audit':
        cmd_audit(args[1] if len(args) > 1 else None)
    else:
        number, leaves = args[0], args[1:]
        if not leaves:
            print("Error: leaf 태그를 하나 이상 지정하세요. (예: tag.py 120807 dijkstra)")
            sys.exit(1)
        cmd_apply(number, leaves)


if __name__ == "__main__":
    main()
