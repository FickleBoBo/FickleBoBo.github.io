"""
이미 존재하는 블로그 포스트의 코드 블록을 PS 레포 최신 코드로 갱신한다.
코드만 건드림 — 프로즈는 건드리지 않음. 완전 결정론적, LLM 판단 없음.

사용법·동작·출력은 `sync/SKILL.md`가 정본. 코드 블록 포맷의 '왜'는 `ps/SKILL.md`와
`scaffold_post.py` docstring에 있다. `ps`의 본문 스켈레톤(챕터 번호, 코드 블록
포맷)이 바뀌면 여기 코드 블록 탐지(`segment_by_approach`/`APPROACH_HEADING_RE`)도
같이 손봐야 한다.
"""

import os
import re
import sys

_SKILLS_DIR = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path.insert(0, os.path.abspath(os.path.join(_SKILLS_DIR, "ps", "scripts")))
sys.path.insert(0, os.path.abspath(os.path.join(_SKILLS_DIR, "_shared")))
from blog_common import (
    DRAFTS_DIR,
    PLATFORM_DIRS,
    POSTS_DIR,
    REPO_ROOT,
    list_platform_posts,
    read_front_matter,
    resolve_source_folder,
)
from clean_code import clean_code, split_approach_suffix
from ps_source import (
    FENCE_LANG,
    LANGUAGE_DISPLAY_ORDER,
    approach_label,
    find_source_files,
    group_by_approach,
)

APPROACH_HEADING_RE = re.compile(r"^### 풀이(?: (\d+))?[^\n]*\n", re.MULTILINE)

REVERSE_FENCE_LANG = {v: k for k, v in FENCE_LANG.items()}


def segment_by_approach(text):
    """ "### 풀이"/"### 풀이 N" 헤딩 기준으로 구간을 나눠서 {접근법 번호: (시작, 끝)}을
    반환. 같은 언어 fence가 접근법마다 반복될 수 있어서(예: 접근법 1의 ```java와
    접근법 2의 ```java), 코드 블록을 찾을 때 이 구간으로 먼저 스코핑해야 엉뚱한
    접근법의 블록을 잘못 건드리지 않음."""
    matches = list(APPROACH_HEADING_RE.finditer(text))
    spans = {}
    for i, m in enumerate(matches):
        num = int(m.group(1)) if m.group(1) else 1
        if num in spans:
            raise ValueError(f"포스트에 '풀이 {num}' 헤딩이 중복됨 — 수동 확인 필요")
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        spans[num] = (start, end)
    return spans


def replace_code_block(body, fence_lang, new_content, start, end):
    pattern = re.compile(
        r"(```" + re.escape(fence_lang) + r"\n)(.*?)(\n```\n?)", re.DOTALL
    )
    m = pattern.search(body, pos=start, endpos=end)
    if not m:
        return body, "not_found"
    old_content = m.group(2)
    if old_content == new_content:
        return body, "unchanged"
    new_body = (
        body[: m.start()] + m.group(1) + new_content + m.group(3) + body[m.end() :]
    )
    return new_body, "updated"


def sync_files(post_text, folder, by_language):
    """포스트 본문을 PS 레포 최신 코드로 갱신. (최종 body, 파일별 결과 리스트)를 반환.
    결과 리스트 항목: (파일명, status, extra) — status는
    "updated"/"unchanged"/"not_found"/"heading_missing"."""
    # group_by_approach는 같은 접근법에 같은 언어 파일이 2개 이상이면 ValueError를
    # 던진다. 이 호출 없이 아래 루프가 by_language를 직접 순회하면 충돌 시 같은
    # 헤딩 구간을 두 번 건드려 먼저 처리된 내용이 조용히 덮어써진다.
    total_approaches = len(group_by_approach(by_language))

    body = post_text
    report = []

    for lang in LANGUAGE_DISPLAY_ORDER:
        for fname in by_language.get(lang, []):
            _, approach_num = split_approach_suffix(fname)
            # 교체할 때마다 오프셋이 어긋나므로 매번 재계산
            spans = segment_by_approach(body)
            if approach_num not in spans:
                report.append(
                    (
                        fname,
                        "heading_missing",
                        approach_label(approach_num, total_approaches),
                    )
                )
                continue
            start, end = spans[approach_num]
            with open(os.path.join(folder, fname), encoding="utf-8") as f:
                raw = f.read()
            cleaned = clean_code(raw, lang).rstrip("\n")
            fence = FENCE_LANG.get(lang, lang.lower())
            body, status = replace_code_block(body, fence, cleaned, start, end)
            report.append((fname, status, None))

    return body, report


def find_stale_blocks(post_text, by_language):
    """PS 레포엔 더 이상 없는데 포스트엔 남아있는 (접근법, 언어) 코드 블록을 찾아
    "{언어} 코드({풀이 라벨})" 문자열 리스트로 반환. sync 시작 시점의 헤딩 구간
    (post_text 원본)을 기준으로 함 — 원본 언어-접근법 매칭 스냅샷."""
    groups = group_by_approach(by_language)
    total_approaches = len(groups)
    current_pairs = {(num, lang) for num, slot in groups.items() for lang in slot}
    stale = []
    for num, (start, end) in segment_by_approach(post_text).items():
        for fence_lang in re.findall(r"```([^\s`]+)\n", post_text[start:end]):
            if fence_lang not in REVERSE_FENCE_LANG:
                continue  # Java/C++/Python이 아닌 펜스(예시로 넣은 ```bash 등) — 대상 아님
            lang = REVERSE_FENCE_LANG[fence_lang]
            if (num, lang) not in current_pairs:
                stale.append(f"{lang} 코드({approach_label(num, total_approaches)})")
    return stale


STATUS_LABELS = {
    "updated": "갱신함",
    "unchanged": "변경 없음",
    # 원인 설명은 SKILL.md `## 출력`이 담당 — 여기서 다시 안 풂(중복 시 어긋날 여지).
    "not_found": "포스트에서 코드 블록을 못 찾음 — 수동 확인 필요",
}


def process_post(post_path):
    """포스트 파일 하나를 동기화(바뀐 게 있으면 실제로 다시 씀).
    (report 줄 문자열 리스트, has_update, needs_attention)을 반환.
    실패하면 예외를 그대로 던짐 — 단일 모드는 그대로 죽고, 배치 모드는 호출자가
    잡아서 그 포스트만 에러로 보고하고 계속 진행함."""
    with open(post_path, encoding="utf-8") as f:
        post_text = f.read()

    date, slug = read_front_matter(post_text)
    folder = resolve_source_folder(date, slug)
    by_language = find_source_files(folder)

    body, report = sync_files(post_text, folder, by_language)

    if body != post_text:
        with open(post_path, "w", encoding="utf-8") as f:
            f.write(body)

    lines = []
    has_update = False
    needs_attention = False
    for fname, status, extra in report:
        if status == "heading_missing":
            lines.append(
                f"{fname}: 포스트에 '{extra}' 섹션 자체가 없음 — 새 접근법으로 보임, 직접 섹션 추가해야 함"
            )
            needs_attention = True
        else:
            lines.append(f"{fname}: {STATUS_LABELS[status]}")
            if status == "updated":
                has_update = True
            elif status == "not_found":
                needs_attention = True

    for stale in find_stale_blocks(post_text, by_language):
        lines.append(
            f"{stale}: 포스트엔 있는데 PS 레포 폴더엔 더 이상 없음 — 수동 확인 필요"
        )
        needs_attention = True

    return lines, has_update, needs_attention


def run_single(post_path):
    lines, _, _ = process_post(post_path)
    for line in lines:
        print(line)


def run_batch(base_dir, label, platform=None):
    """`base_dir/{platform}/`(`_drafts` 또는 `_posts`)의 포스트를 동기화. platform이
    None이면 전체 플랫폼. 포스트 하나가 실패해도 그 포스트만 에러로 보고하고 계속
    처리한다(fail-soft). 변경 없는 포스트는 한 줄로 축약하고, 갱신/수동확인/에러만
    세부 내역을 보인다."""
    paths = list_platform_posts(base_dir, platform)
    updated = unchanged = attention = errors = 0

    for path in paths:
        rel = os.path.relpath(path, REPO_ROOT)
        try:
            lines, has_update, needs_attention = process_post(path)
        except Exception as e:
            print(f"에러({rel}): {e}")
            errors += 1
            continue

        if has_update:
            updated += 1
        elif needs_attention:
            attention += 1
        else:
            unchanged += 1

        if has_update or needs_attention:
            for line in lines:
                print(f"{rel} — {line}")
        else:
            print(f"{rel}: 변경 없음")

    print(
        f"--- 총 {len(paths)}개 {label}{f'({platform})' if platform else ''} 중 {updated}개 갱신함, "
        f"{unchanged}개 변경 없음, {attention}개 수동 확인 필요, {errors}개 에러 ---"
    )


USAGE = "사용법: sync_code.py [--posts] [platform] | sync_code.py <포스트 .md 경로>"


def main():
    args = sys.argv[1:]
    posts = args[:1] == ["--posts"]
    if posts:
        args = args[1:]
    base_dir, label = (POSTS_DIR, "발행") if posts else (DRAFTS_DIR, "드래프트")
    if not args:
        run_batch(base_dir, label)
    elif len(args) == 1 and args[0] in PLATFORM_DIRS:
        run_batch(base_dir, label, args[0])
    elif len(args) == 1 and not posts and args[0].endswith(".md"):
        run_single(args[0])
    else:
        print(USAGE)
        sys.exit(1)


if __name__ == "__main__":
    main()
