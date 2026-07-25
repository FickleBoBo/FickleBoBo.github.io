#!/usr/bin/env python3
"""
Publish a PS draft: move _drafts/ -> _posts/ and commit to both repos.

Usage:
    python3 publish.py                 # publish every draft in _drafts/ (one commit each)
    python3 publish.py 120807          # publish only this problem
    python3 publish.py 120807 1929     # publish these problems

For each problem it:
  1. finds the draft in _drafts/{platform}/ by problem number,
  2. commits the matching source dir in the Algorithm repo,
  3. moves the draft to _posts/{platform}/,
  4. commits the moved post in the Blog repo (rolls the move back on failure).

Never pushes. This mirrors what /ps produced, so it depends on that filename
and front-matter shape. Run only when explicitly invoked — see SKILL.md.
"""

import re
import shutil
import subprocess
import sys
from pathlib import Path

# ── Paths ──────────────────────────────────────
HOME = Path.home()
ALGO_DIR = HOME / "Desktop" / "GITHUB" / "Algorithm"
BLOG_DIR = HOME / "Desktop" / "GITHUB" / "FickleBoBo.github.io"
DRAFTS_DIR = BLOG_DIR / "_drafts"
POSTS_DIR = BLOG_DIR / "_posts"

# ── Platform config ────────────────────────────
# Korean platform name (as it appears in the filename) -> source-dir prefix.
# Only the platforms /ps supports. Add '백준': 'boj' / 'SWEA': 'swea' if reopened.
PLATFORM_MAP = {
    '프로그래머스': 'prms',
    '리트코드': 'leet',
    '코드포스': 'cofo',
}
# Blog post directories, used to skip non-PS drafts during a bulk publish.
PS_DIRS = {'programmers', 'leetcode', 'codeforces'}

# ── Claude trailer ─────────────────────────────
# This repo is exempt from the "leave no Claude trace" rule, so blog commits
# carry the trailer. Model-agnostic on purpose: the script doesn't know which
# model invoked it. Flip ALGO_TRAILER to False to keep it off the Algorithm repo.
CLAUDE_TRAILER = "Co-Authored-By: Claude <noreply@anthropic.com>"
BLOG_TRAILER = True
ALGO_TRAILER = True


# ── Filename / front matter parsing ────────────
def parse_filename(path):
    """'2026-07-24-프로그래머스 120807 숫자 비교하기.md' -> parts, or None."""
    m = re.match(r"(\d{4}-\d{2}-\d{2})-(.+?) (\S+) (.+)\.md", path.name)
    if not m:
        return None
    date_str, platform_ko, number = m.group(1), m.group(2), m.group(3)
    prefix = PLATFORM_MAP.get(platform_ko)
    if not prefix:
        return None
    y, mo, d = date_str.split("-")
    return {
        'date': date_str,
        'platform_ko': platform_ko,
        'prefix': prefix,
        'number': number,
        'year_month': f"{y}-{mo}",
        'day': int(d),
    }


def extract_frontmatter(path, key):
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = re.match(rf'^{key}:\s*"?(.+?)"?\s*$', line)
            if m:
                return m.group(1)
    return None


# ── Assets (images) ────────────────────────────
def assets_paths(slug):
    """Draft staging dir and published dir — parallels _drafts/ <-> _posts/."""
    return BLOG_DIR / "assets" / slug, BLOG_DIR / "assets" / "posts" / slug


def move_assets(slug):
    """Move assets/{slug}/ -> assets/posts/{slug}/ alongside the post move.

    Publishing only the post while leaving images behind would half-move the
    reboot and leave the published post pointing at a path that hasn't moved.
    Moves entry-by-entry (pub may already hold earlier-published images) and
    records exactly what moved so a rollback touches only those.
    Returns (moved_names, files_to_stage).
    """
    if not slug:
        return [], []
    staged, pub = assets_paths(slug)
    moved_names = []
    if staged.is_dir():
        pub.mkdir(parents=True, exist_ok=True)
        for f in list(staged.iterdir()):
            shutil.move(str(f), str(pub / f.name))
            moved_names.append(f.name)
        staged.rmdir()
        print(f"  이미지 이동: assets/{slug}/ → assets/posts/{slug}/")
    if not pub.is_dir():
        return moved_names, []
    # Stage both: the published dir (additions) and the old staging path, so a
    # previously-tracked staging dir has its deletion staged too.
    return moved_names, [str(pub.relative_to(BLOG_DIR)), str(staged.relative_to(BLOG_DIR))]


def unmove_assets(slug, moved_names):
    """Roll back move_assets — return ONLY the files this run moved, so
    images published in an earlier run stay put in assets/posts/{slug}/."""
    if not moved_names:
        return
    staged, pub = assets_paths(slug)
    staged.mkdir(parents=True, exist_ok=True)
    for name in moved_names:
        src = pub / name
        if src.exists():
            shutil.move(str(src), str(staged / name))
    if pub.is_dir() and not any(pub.iterdir()):
        pub.rmdir()
    print(f"  (롤백: assets/posts/{slug}/ → assets/{slug}/)")


# ── Draft discovery ────────────────────────────
def is_ps_draft(path):
    return path.relative_to(DRAFTS_DIR).parts[0] in PS_DIRS


def find_draft(number):
    # Match the parsed number field, not a " {number} " substring — a bare
    # number inside the title text (e.g. "205 ... 1 line") would collide.
    matches = []
    for p in DRAFTS_DIR.rglob("*.md"):
        if not is_ps_draft(p):
            continue
        parsed = parse_filename(p)
        if parsed and parsed['number'] == number:
            matches.append(p)
    if not matches:
        print(f"Error: _drafts/에서 {number}번 포스트를 찾을 수 없습니다.")
        sys.exit(1)
    if len(matches) > 1:
        print("Error: 여러 개 매칭됨:")
        for m in matches:
            print(f"  {m.relative_to(BLOG_DIR)}")
        sys.exit(1)
    return matches[0]


def find_all_draft_numbers():
    numbers = []
    for path in sorted(DRAFTS_DIR.rglob("*.md")):
        if not is_ps_draft(path):
            continue
        parsed = parse_filename(path)
        if parsed:
            numbers.append(parsed['number'])
        else:
            print(f"[경고] 파일명 파싱 실패, 건너뜀: {path.name}")
    return numbers


# ── Git ────────────────────────────────────────
def git_commit(repo_dir, files_to_add, message, add_trailer):
    """Stage exactly `files_to_add` and commit. Returns True if a commit was made."""
    subprocess.run(["git", "reset"], cwd=repo_dir,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for f in files_to_add:
        subprocess.run(["git", "add", str(f)], cwd=repo_dir,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    staged = subprocess.run(["git", "diff", "--cached", "--stat"],
                            cwd=repo_dir, capture_output=True, text=True)
    if not staged.stdout.strip():
        print("  (커밋할 변경사항 없음, 건너뜀)")
        return False
    print("  " + staged.stdout.strip().replace("\n", "\n  "))
    msg = f"{message}\n\n{CLAUDE_TRAILER}" if add_trailer else message
    result = subprocess.run(["git", "commit", "-m", msg],
                            cwd=repo_dir, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr.strip()}")
        sys.exit(1)
    print(f"  {result.stdout.strip().splitlines()[0]}")
    return True


# ── Publish one problem ────────────────────────
def publish_one(number):
    draft = find_draft(number)
    print(f"[1] 드래프트: {draft.relative_to(BLOG_DIR)}")

    parsed = parse_filename(draft)
    if not parsed:
        print(f"Error: 파일명 파싱 실패: {draft.name}")
        sys.exit(1)

    title = extract_frontmatter(draft, "title")
    if not title:
        print("Error: title 추출 실패")
        sys.exit(1)
    commit_msg = f"feat: {title}"
    print(f"[2] 커밋 메시지: {commit_msg}")

    # Algorithm repo (before the move — nothing to roll back if it fails).
    algo_rel = f"{parsed['year_month']}/src/day_{parsed['day']:02d}/{parsed['prefix']}_{parsed['number']}"
    algo_committed = False
    if not (ALGO_DIR / algo_rel).exists():
        print(f"[3] Algorithm 경로 없음, 건너뜀: {algo_rel}")
    else:
        print("[3] Algorithm 레포 커밋")
        algo_committed = git_commit(ALGO_DIR, [algo_rel], commit_msg, ALGO_TRAILER)

    # Move draft -> posts, mirroring the platform subdir it already lives in.
    post_dir = POSTS_DIR / draft.parent.name
    post_dir.mkdir(parents=True, exist_ok=True)
    post = post_dir / draft.name
    shutil.move(str(draft), str(post))
    print(f"[4] 이동: _drafts/ → {post.relative_to(BLOG_DIR)}")

    # Move images alongside the post (assets/{slug}/ -> assets/posts/{slug}/).
    slug = extract_frontmatter(post, "slug")
    moved_names, assets_files = move_assets(slug)

    # Blog repo (roll post + assets + the Algorithm commit back if it fails).
    print("[5] Blog 레포 커밋")
    blog_files = [str(post.relative_to(BLOG_DIR)), str(draft.relative_to(BLOG_DIR))]
    blog_files.extend(assets_files)
    try:
        blog_committed = git_commit(BLOG_DIR, blog_files, commit_msg, BLOG_TRAILER)
    except SystemExit:
        draft.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(post), str(draft))
        print(f"  (롤백: {draft.relative_to(BLOG_DIR)}로 복원)")
        if moved_names:
            unmove_assets(slug, moved_names)
        if algo_committed:
            subprocess.run(["git", "reset", "--soft", "HEAD~1"], cwd=ALGO_DIR,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("  (롤백: Algorithm 커밋 취소 — git reset --soft HEAD~1)")
        raise

    print("완료.\n")
    return {'number': number, 'title': title,
            'algo': algo_committed, 'blog': blog_committed}


def main():
    numbers = sys.argv[1:] or find_all_draft_numbers()
    if not numbers:
        print("_drafts/에 발행할 포스트가 없습니다.")
        sys.exit(0)
    if len(sys.argv) < 2:
        print(f"_drafts/ 전체 발행: {len(numbers)}개 문제\n")

    results = []
    for i, number in enumerate(numbers, 1):
        if len(numbers) > 1:
            print(f"{'='*50}\n[{i}/{len(numbers)}] 문제 {number}\n{'='*50}")
        results.append(publish_one(number))

    # Summary table
    print(f"{'='*50}\n결과")
    print("| # | 문제 | Algorithm | Blog |")
    print("| :-: | :-- | :-: | :-: |")
    for i, r in enumerate(results, 1):
        algo = "✅" if r['algo'] else "-"
        blog = "✅" if r['blog'] else "-"
        print(f"| {i} | {r['number']} {r['title']} | {algo} | {blog} |")


if __name__ == "__main__":
    main()
