#!/usr/bin/env python3
"""
이미 존재하는 블로그 포스트의 코드 블록을 PS 레포 최신 코드로 갱신한다.
코드만 건드림 — 프로즈(문제/접근/회고 등 사람이 쓴 글)는 절대 건드리지 않음.
`ps` 스킬과 마찬가지로 완전 결정론적, LLM 판단 없음.

**코드 블록 포맷(라벨 없는 순수 fence를 쓰는 이유, `### 풀이 N` 헤딩 구조,
Prettier IAL 버그 등)은 전부 `ps/SKILL.md`에 문서화돼있음 — 여기서 다시 설명
안 함.** 여기 docstring은 사용법 + 코드를 고칠 때 바로 옆 코드만 봐선 안 보이는
것만 남겨둠(SKILL.md와 내용이 겹치면 둘 중 하나가 stale해지기 쉬워서 분리함).

코드를 고칠 때 알아야 할 것 (SKILL.md에 없는, 이 파일 안에서만 유효한 정보):
- front matter의 date/slug만으로 PS 레포 원본 폴더 경로를 재구성함(파일명이 바뀌어도
  영향 없음 — front matter만 신뢰). date="YYYY-MM-DD" + slug="{platform}-{번호}" →
  {PS_REPO}/{YYYY-MM}/src/day_{DD}/{prefix}_{번호}.
- `ps` 스킬의 `clean_code.py`/`resolve_filename.py`를 그대로 import해서 씀(sys.path로
  `ps/scripts`를 직접 끌어옴) — "PS 레포 코드 → 블로그용 코드" 변환 로직이 두 스킬
  사이에서 갈라지면 안 되기 때문. `ps`의 본문 스켈레톤 구조(챕터 번호, 코드 블록
  포맷)가 바뀌면 여기 코드 블록 탐지 로직(`segment_by_approach`/
  `APPROACH_HEADING_RE`)도 같이 손봐야 함. review/publish 스킬까지 생겨서 공유
  로직이 더 늘어나면 이 sys.path 직접 import 방식은 별도 공유 패키지로 빼는 게
  나을 수 있음(아직은 안 함).
- 코드 블록을 헤딩 구간으로 스코핑하는 이유는 `segment_by_approach` docstring 참고.
- 배치 모드(인자 없음)는 `ps`의 `run_batch`/`discover_problem_folders` 패턴을 그대로
  따름: 개별 포스트 실패가 배치 전체를 막지 않고 그 포스트만 에러로 보고, 나머지는
  계속 처리. `DRAFTS_DIR`/`REPO_ROOT`도 새로 정의하지 않고 `resolve_filename`에서
  그대로 가져옴(단일 진실 소스 유지).

동작:
1. 포스트의 front matter에서 date/slug 파싱 → platform/번호/PS 레포 폴더 경로 역산
2. 그 폴더의 현재 소스 파일들을 다시 스캔 + clean_code로 정리
3. 파일명 끝자리 숫자로 접근법 번호를 뽑고, 포스트에서 그 번호에 해당하는
   "### 풀이 N" 구간 안에서 그 언어의 fenced code block을 찾아 내용이 다르면
   최신 코드로 교체(새 접근법/새 언어 추가·삭제는 자동으로 반영 안 하고
   경고만 출력, 사람이 직접 처리)
4. 실제로 바뀐 게 있을 때만 파일을 다시 씀

사용법:
    python3 sync_code.py
        인자 없이 실행 — 배치 모드. `_drafts/{platform}/`(platform ∈ PLATFORM_MAP)
        아래 포스트(.md)를 전부 스캔해서 동기화(publish와 동일한 스코핑). 포스트 하나가
        실패해도(PS 레포에 대응 폴더가 없는 등) 그 포스트만 에러로 보고하고 나머지는
        계속 처리함.

    python3 sync_code.py <포스트 .md 파일 절대경로>
        포스트 하나만 지정해서 동기화. 이 경우엔 실패하면 즉시 예외를 그대로 띄움
        (배치와 달리 콕 집어 지정했으니 조용히 넘어가지 않음).

출력: 파일별로 "갱신함" / "변경 없음" / "코드 블록을 못 찾음(수동 확인 필요)" 보고.
배치 모드는 포스트별로 한 줄 요약("변경 없음") 또는 세부 내역 + 맨 끝에 총계 한 줄.
"""

import os
import re
import sys

_PS_SCRIPTS = os.path.join(os.path.dirname(__file__), "..", "..", "ps", "scripts")
sys.path.insert(0, os.path.abspath(_PS_SCRIPTS))
from clean_code import clean_code, split_approach_suffix
from resolve_filename import (
    DRAFTS_DIR,
    FENCE_LANG,
    LANGUAGE_DISPLAY_ORDER,
    PLATFORM_MAP,
    PS_REPO,
    REPO_ROOT,
    approach_label,
    find_source_files,
    group_by_approach,
)

APPROACH_HEADING_RE = re.compile(r"^### 풀이(?: (\d+))?[^\n]*\n", re.MULTILINE)

REVERSE_PLATFORM_MAP = {v.lower(): k for k, v in PLATFORM_MAP.items()}
REVERSE_FENCE_LANG = {v: k for k, v in FENCE_LANG.items()}


def front_matter_block(post_text):
    m = re.match(r"^---\n(.*?)\n---\n", post_text, re.DOTALL)
    if not m:
        raise ValueError("front matter(--- ~ ---) 블록을 못 찾음")
    return m.group(1)


def read_front_matter(post_text):
    raw = front_matter_block(post_text)

    date_m = re.search(r"^date:\s*(\S+)", raw, re.MULTILINE)
    slug_m = re.search(r"^slug:\s*(\S+)", raw, re.MULTILINE)
    if not date_m or not slug_m:
        raise ValueError("front matter에 date 또는 slug가 없음")
    return date_m.group(1), slug_m.group(1)


def resolve_source_folder(date, slug):
    platform_lower, _, number = slug.partition("-")
    prefix = REVERSE_PLATFORM_MAP.get(platform_lower)
    if not prefix:
        raise ValueError(f"slug의 플랫폼 부분을 못 알아봄: {slug}")

    # slug는 항상 소문자(build_slug)라 Codeforces 인덱스 문자(예: 1553A)의 대문자
    # 정보가 소실됨 — PS 레포 폴더명은 대문자를 쓰므로(cofo_1553A) 여기서 복원.
    # 다른 플랫폼은 번호가 숫자뿐이라 upper()가 무해함.
    if prefix == "cofo":
        number = number.upper()

    year_month = date[:7]
    day = date[8:10]
    day_dir = os.path.join(PS_REPO, year_month, "src", f"day_{day}")
    folder_name = f"{prefix}_{number}"
    folder = os.path.join(day_dir, folder_name)
    if not os.path.isdir(folder):
        raise ValueError(f"PS 레포에 해당 폴더가 없음(경로 재구성 결과): {folder}")
    # macOS(APFS)는 기본적으로 대소문자를 구분 안 해서 os.path.isdir는 재구성한
    # 이름의 대소문자가 실제 폴더명과 달라도(예: cofo_2148A로 재구성했는데 실제
    # 폴더는 cofo_2148a) 통과시켜버림. git은 대소문자를 구분하므로 이 어긋난
    # 경로로 git 명령을 돌리면(예: publish의 has_pending_changes) 대상이 조용히
    # 안 걸려서 "이미 커밋됨"으로 오판 — 실제로 있었던 사고(2026-08-22, Codeforces
    # #2148A: PS 레포 커밋이 스킵됐는데 publish는 성공으로 보고함). 재구성한
    # 이름을 그대로 믿지 않고, 디렉토리 목록에서 대소문자 무시로 매칭한 뒤 실제
    # 엔트리명으로 교체해서 반환 — PS 레포 폴더명에 특정 대소문자 관례를 강제하지
    # 않으면서도 이후 git 명령이 항상 실제 경로를 정확히 가리키게 함.
    actual_name = next(
        (e for e in os.listdir(day_dir) if e.lower() == folder_name.lower()), None
    )
    if actual_name is None:
        raise ValueError(f"PS 레포에 해당 폴더가 없음(경로 재구성 결과): {folder}")
    return os.path.join(day_dir, actual_name)


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
    # ps 쪽 generate_one과 동일한 검증을 여기서도 거침 — 결과는 안 쓰고 접근법 번호
    # 충돌(같은 접근법에 같은 언어 파일이 2개 이상)만 있으면 여기서 ValueError로
    # 막음. 이 검증 없이 진행하면 아래 루프가 by_language를 직접 순회하므로 충돌
    # 시 같은 헤딩 구간을 두 번 건드려 먼저 처리된 파일 내용이 조용히 덮어써짐.
    group_by_approach(by_language)

    body = post_text
    report = []

    for lang in LANGUAGE_DISPLAY_ORDER:
        for fname in by_language.get(lang, []):
            _, approach_num = split_approach_suffix(fname)
            spans = segment_by_approach(
                body
            )  # 교체할 때마다 오프셋이 어긋나므로 매번 재계산
            if approach_num not in spans:
                report.append((fname, "heading_missing", approach_label(approach_num)))
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
    current_pairs = {
        (num, lang)
        for num, slot in group_by_approach(by_language).items()
        for lang in slot
    }
    stale = []
    for num, (start, end) in segment_by_approach(post_text).items():
        for fence_lang in re.findall(r"```([^\s`]+)\n", post_text[start:end]):
            if fence_lang not in REVERSE_FENCE_LANG:
                continue  # Java/C++/Python이 아닌 펜스(예시로 넣은 ```bash 등) — 대상 아님
            lang = REVERSE_FENCE_LANG[fence_lang]
            if (num, lang) not in current_pairs:
                stale.append(f"{lang} 코드({approach_label(num)})")
    return stale


STATUS_LABELS = {
    "updated": "갱신함",
    "unchanged": "변경 없음",
    "not_found": (
        "포스트에서 코드 블록을 못 찾음 — 수동 확인 필요"
        "(코드 블록이 다른 섹션으로 옮겨졌거나 fence 언어 표시가 깨졌을 수 있음)"
    ),
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


def discover_draft_files():
    """`_drafts/{platform}/`(platform ∈ PLATFORM_MAP) 아래 포스트(.md)를 경로순으로
    찾아 반환. `_drafts/` 바로 밑이나 PS 아닌 서브폴더는 안 봄 — `publish`의 배치
    스코핑(`discover_ready_drafts`)과 동일하게, 블로그에 PS 아닌 드래프트가 생겨도
    안 건드리기 위함."""
    paths = []
    for platform_dir in sorted({v.lower() for v in PLATFORM_MAP.values()}):
        dir_path = os.path.join(DRAFTS_DIR, platform_dir)
        if not os.path.isdir(dir_path):
            continue
        for fname in sorted(os.listdir(dir_path)):
            if fname.endswith(".md"):
                paths.append(os.path.join(dir_path, fname))
    return sorted(paths)


def run_batch():
    """`_drafts/`의 모든 포스트를 동기화. 포스트 하나가 실패해도(PS 레포에 대응
    폴더가 없는 등) 그 포스트만 에러로 보고하고 나머지는 계속 처리함(ps의
    run_batch와 동일한 fail-soft 방침) — 변경 없는 포스트는 한 줄로 축약해서
    출력 노이즈를 줄이고, 갱신/수동확인/에러가 있는 포스트만 세부 내역을 보임."""
    paths = discover_draft_files()
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
        f"--- 총 {len(paths)}개 드래프트 중 {updated}개 갱신함, "
        f"{unchanged}개 변경 없음, {attention}개 수동 확인 필요, {errors}개 에러 ---"
    )


def main():
    if len(sys.argv) == 1:
        run_batch()
    elif len(sys.argv) == 2:
        run_single(sys.argv[1])
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
