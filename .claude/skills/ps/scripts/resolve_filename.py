#!/usr/bin/env python3
"""
PS 레포 문제 폴더 경로를 받아서, 이 블로그의 포스트 파일명 + front matter +
본문 스켈레톤을 결정론적으로 생성한다. LLM 판단 없음 — 정규식/API 응답 파싱/
파일 스캔/문자열 치환만 함.

**본문 스켈레톤 구조와 그 설계 이유(챕터 번호, 구분선 소유권, 문제/접근 역할
분담, 코드 라벨을 안 쓰는 이유 등)는 전부 `ps/SKILL.md`에 문서화돼있음 —
여기서 다시 설명 안 함.** 여기 docstring은 사용법 + 코드를 고칠 때 바로 옆
코드만 봐선 안 보이는 것만 남겨둠(SKILL.md와 내용이 겹치면 둘 중 하나가 stale
해지기 쉬워서 분리함).

지원 플랫폼: Programmers/LeetCode/Codeforces(`PLATFORM_MAP`). BOJ/SWEA는
`UNSUPPORTED_PLATFORMS`로 보류 중 — 이유는 SKILL.md 참고. 컷오프
(`BLOG_CREATION_DATE`) 이전 폴더는 전부 무시.

코드를 고칠 때 알아야 할 것 (SKILL.md에 없는, 이 파일 안에서만 유효한 정보):
- `build_body`의 "---" 구분선은 항상 **뒤 섹션이 자기 앞에 다는 것**으로 소유
  (섹션 사이 접착제가 아님) — 회고/참고 같은 선택 섹션을 통째로 지울 때 그
  섹션이 든 구분선까지 같이 지워지게 하려는 설계. 이 소유권 방향을 바꾸면
  섹션 삭제 시 구분선이 붕 뜨거나 중복될 수 있음.
- 코드펜스엔 `{: file="..." }` 같은 Kramdown IAL을 아예 안 붙임 — Chirpy가
  라벨 없어도 헤더바를 자동 생성해주고, IAL을 붙이면 Prettier가 fence와 IAL
  사이에 빈 줄을 끼워넣는 버그가 있어서(재현 확인함) 아예 안 쓰는 쪽으로
  피함. 지금 IAL이 남은 곳은 blockquote(prompt-info)뿐이고 거긴
  `<!-- prettier-ignore -->` 하나로 안전하게 보호됨. 코드펜스에 IAL을 다시
  붙이는 방향으로 바꾸면 이 문제가 재발함.
- `sync` 스킬(`../../sync/scripts/sync_code.py`)이 이 파일의 `PLATFORM_MAP`/
  `FENCE_LANG`/`PS_REPO`/`group_by_approach`/`approach_label`을 그대로
  import해서 씀 — 여기서 이름을 바꾸거나 동작을 바꾸면 sync도 같이 깨짐.

사용법:
    python3 resolve_filename.py
        인자 없이 실행 — 배치 모드. PS_REPO 전체를 스캔해서 블로그 개설일
        (BLOG_CREATION_DATE) 이후 존재하는 풀이 중 이 블로그에 아직 포스트/드래프트가
        없는 것 전부를 스캐폴드로 생성. 이미 있는 건 절대 안 건드림(--force 없음),
        개별 폴더가 실패해도(네트워크/파싱 에러 등) 그 폴더만 보고하고 나머지는 계속함.

    python3 resolve_filename.py <PS레포 문제 폴더 경로> [--force]
        폴더 하나만 지정해서 처리 — 특정 문제를 다시 만들고 싶을 때(스켈레톤 구조가
        바뀌어서 재생성하는 등) 씀.
        예: python3 resolve_filename.py /Users/mwzz6/Desktop/github/PS/2026-08/src/day_14/prms_258705

동작: 이 레포의 _drafts/{platform}/ 밑에 파일을 실제로 씀. platform 디렉토리명은
소문자(예: programmers, leetcode, codeforces). _posts/가 아니라 _drafts/에 두는
이유: 사람이 문제/접근/회고 등을 다 채워서 "발행 준비 완료"로 판단하기 전까진
아직 초안이라, publish 단계(별도 스킬)에서 _posts/로 옮기기 전까지는 사이트에
노출되면 안 됨.
두 모드 다 이미 같은 이름의 파일이 있으면 기본적으로 거부(사람이 이미 프로즈를
채워넣었을 수 있어서 임의로 덮어쓰지 않음) — 단일 폴더 모드에서만 --force로
의도적으로 다시 생성 가능(배치 모드는 --force 자체를 안 받음, 위 참고).
"""

import functools
import json
import os
import re
import sys
import urllib.request

from clean_code import clean_code, split_approach_suffix

BLOG_CREATION_DATE = "2026-08-17"

# 이 스크립트(.claude/skills/ps/scripts/resolve_filename.py) 기준 이 블로그 레포 루트
REPO_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")
)
DRAFTS_DIR = os.path.join(REPO_ROOT, "_drafts")
POSTS_DIR = os.path.join(REPO_ROOT, "_posts")

# PS 레포(형제 디렉토리) 루트 — 인자 없이 실행하는 배치 스캔의 대상.
# sync 스킬도 이 값을 그대로 가져다 씀(중복 정의 안 함).
# ⚠️ 이 스크립트에서 유일하게 이 컴퓨터/사용자 전용으로 하드코딩된 값 — 다른 환경에서
# 이 레포를 쓰려면(경로/사용자명이 다르면) 여기만 고치면 됨. 나머지는 전부 __file__
# 기준 상대경로라 레포를 어디로 옮겨도 그대로 동작함.
PS_REPO = "/Users/mwzz6/Desktop/github/PS"

PLATFORM_MAP = {
    "prms": "Programmers",
    "leet": "LeetCode",
    "boj": "BaekJoon",
    "cofo": "Codeforces",
    "swea": "SWEA",
}

# 언어 브라켓 표시 순서 및 확장자 매핑
LANGUAGE_DISPLAY_ORDER = ["Java", "C++", "Python"]
EXT_TO_LANGUAGE = {
    ".java": "Java",
    ".cpp": "C++",
    ".py": "Python",
}
FENCE_LANG = {
    "Java": "java",
    "C++": "c++",
    "Python": "python",
}

# 본문 섹션 헤딩 — publish 스킬의 완료 판정(`publish.py`)이 이 문자열을 그대로
# 찾아서 씀. 여기서 챕터 번호/제목을 바꾸면 publish의 완료 판정도 반드시 같이
# 확인해야 함(안 바꿔도 조용히 "미완료"로만 fail-closed 되긴 하지만, 원인
# 추적이 헷갈릴 수 있음).
IDEA_HEADING = "## 1. 아이디어"
COMPLEXITY_HEADING = "## 2. 복잡도"

# 제목 자동조회가 아직 구현 안 된(또는 원천 서비스 문제로 막힌) 플랫폼
UNSUPPORTED_PLATFORMS = {"boj", "swea"}

# 파일명 금지 문자 -> 육안 구별 어려운 유니코드 대체
# 출처: laggner.info "Replacing Forbidden File System Characters with Unicode Alternatives"
# 주의: 이 치환은 파일명에만 적용. front matter의 title/description은 원문 그대로 씀.
FILENAME_ESCAPES = {
    "/": "⁄",  # FRACTION SLASH
    ":": "∶",  # RATIO
    "?": "？",  # FULLWIDTH QUESTION MARK
    "*": "⁎",  # LOW ASTERISK
    '"': "＂",  # FULLWIDTH QUOTATION MARK
    "<": "‹",  # SINGLE LEFT-POINTING ANGLE QUOTATION MARK
    ">": "›",  # SINGLE RIGHT-POINTING ANGLE QUOTATION MARK
    "\\": "∖",  # SET MINUS
    "|": "｜",  # FULLWIDTH VERTICAL LINE
}


def fetch(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read().decode("utf-8")


def parse_folder(path):
    """PS 레포 경로에서 {year}-{month}/day_{DD}/{prefix}_{번호} 추출"""
    m = re.search(
        r"(\d{4}-\d{2})/src/day_(\d{2})/([a-zA-Z]+)_(.+?)/?$", path.rstrip("/")
    )
    if not m:
        raise ValueError(
            "경로 패턴을 못 읽음(기대 형식: {year}-{month}/src/day_{DD}/{prefix}_{번호}): "
            + path
        )
    year_month, day, prefix, number = m.groups()
    date = f"{year_month}-{day}"
    return date, prefix.lower(), number


def check_cutoff(date):
    if date < BLOG_CREATION_DATE:
        raise ValueError(
            f"블로그 개설일({BLOG_CREATION_DATE}) 이전 풀이({date})는 대상이 아님 "
            "— 존재하지 않는 것으로 취급"
        )


def get_platform(prefix):
    if prefix not in PLATFORM_MAP:
        raise ValueError(f"알 수 없는 플랫폼 접두사: {prefix}")
    if prefix in UNSUPPORTED_PLATFORMS:
        raise NotImplementedError(
            f"{PLATFORM_MAP[prefix]}는 아직 제목 자동조회 미구현(보류 상태) — 수동 처리 필요"
        )
    return PLATFORM_MAP[prefix]


def get_title_and_url(prefix, number):
    """(제목, 문제 URL) 튜플을 반환. URL은 본문의 prompt-info 박스에 그대로 씀."""
    if prefix == "prms":
        return get_title_url_programmers(number)
    if prefix == "leet":
        return get_title_url_leetcode(number)
    if prefix == "cofo":
        return get_title_url_codeforces(number)
    raise NotImplementedError(f"{prefix} 제목 조회 미구현")


def get_title_url_programmers(number):
    url = f"https://school.programmers.co.kr/learn/courses/30/lessons/{number}"
    html = fetch(url)
    m = re.search(r"<title>코딩테스트 연습 - (.+?) \| 프로그래머스 스쿨</title>", html)
    if not m:
        raise ValueError(
            f"Programmers {number}번 title 태그 패턴이 안 맞음 — 사이트 구조가 바뀌었을 수 있음"
        )
    return m.group(1), url


@functools.lru_cache(maxsize=1)
def _fetch_leetcode_problems():
    # 레거시 엔드포인트 — 언젠가 죽을 수 있음. 죽으면 GraphQL questionList 쪽으로 교체 필요.
    # 응답이 꽤 큰 전체 문제 목록이라 프로세스당 한 번만 받아오게 캐시함 — 안 그러면
    # 배치 모드에서 LeetCode 문제가 여러 개일 때 같은 목록을 문제 수만큼 중복 다운로드함.
    body = fetch("https://leetcode.com/api/problems/all/")
    return json.loads(body)["stat_status_pairs"]


def get_title_url_leetcode(number):
    for item in _fetch_leetcode_problems():
        if str(item["stat"]["frontend_question_id"]) == str(number):
            title = item["stat"]["question__title"]
            slug = item["stat"]["question__title_slug"]
            return title, f"https://leetcode.com/problems/{slug}/"
    raise ValueError(f"LeetCode {number}번을 목록에서 못 찾음")


@functools.lru_cache(maxsize=1)
def _fetch_codeforces_problems():
    # problemset 전체를 받는 큰 응답이라 프로세스당 한 번만 캐시 — 배치 모드에서
    # Codeforces 문제가 여러 개일 때 같은 목록을 중복 다운로드하지 않게
    # (_fetch_leetcode_problems와 동일한 이유).
    body = fetch("https://codeforces.com/api/problemset.problems")
    return json.loads(body)["result"]["problems"]


def get_title_url_codeforces(number):
    # 폴더명 형식이 "{contestId}{Index}"(예: 1553A)라고 가정함 — 실제 사용 사례로 검증된 적 없음.
    m = re.match(r"(\d+)([A-Za-z]\d*)$", number)
    if not m:
        raise ValueError(f"Codeforces 번호 형식이 예상과 다름(예: 1553A): {number}")
    contest_id, index = m.groups()
    for p in _fetch_codeforces_problems():
        if str(p["contestId"]) == contest_id and p["index"] == index.upper():
            url = f"https://codeforces.com/problemset/problem/{contest_id}/{index.upper()}"
            return p["name"], url
    raise ValueError(f"Codeforces {number}번을 목록에서 못 찾음")


def find_source_files(folder_path):
    """폴더 안 파일을 확장자 기준으로 언어별로 묶어서 반환: {언어: [파일명, ...]} (정렬됨).
    Solution.java / Solution2.java처럼 같은 언어에 여러 접근이 있으면 전부 모아둠."""
    try:
        entries = sorted(os.listdir(folder_path))
    except FileNotFoundError:
        raise ValueError(f"폴더가 실제로 존재하지 않음: {folder_path}")

    by_language = {}
    for entry in entries:
        ext = os.path.splitext(entry)[1].lower()
        lang = EXT_TO_LANGUAGE.get(ext)
        if lang:
            by_language.setdefault(lang, []).append(entry)
    return by_language


def sanitize_filename(title):
    for bad, good in FILENAME_ESCAPES.items():
        title = title.replace(bad, good)
    return title


def build_filename(date, platform, number, title):
    return f"{date}-{platform} {number} {sanitize_filename(title)}.md"


def yaml_dq(s):
    """YAML 큰따옴표 문자열 안에 안전하게 넣기 위한 이스케이프."""
    return s.replace("\\", "\\\\").replace('"', '\\"')


def build_slug(platform, number):
    return f"{platform}-{number}".lower()


def build_media_subpath(slug):
    return f"/assets/img/posts/{slug}/"


def build_title(platform, number, title, languages):
    lang_suffix = f" {''.join(f'[{lang}]' for lang in languages)}" if languages else ""
    raw = f"[{platform}] #{number} - {title}{lang_suffix}"
    return f'"{yaml_dq(raw)}"'


def build_front_matter(date, platform, number, title, languages):
    slug = build_slug(platform, number)
    media_subpath = build_media_subpath(slug)
    lines = [
        "---",
        f"title: {build_title(platform, number, title, languages)}",
        f"date: {date}",
        f"categories: [PS, {platform}]",
        "tags: []",
        'description: ""',
        f"slug: {slug}",
        f"media_subpath: {media_subpath}",
        "math: true",
        "mermaid: false",
        "---",
    ]
    return "\n".join(lines)


def group_by_approach(by_language):
    """{언어: [파일명, ...]} -> {접근법 번호: {언어: 파일명}}.
    파일명 끝자리 숫자(split_approach_suffix)를 접근법 번호로 씀 — 예를 들어
    Main.java/Main.cpp는 접근법 1, Main2.java/Main2.cpp는 접근법 2로 묶임."""
    groups = {}
    for lang, files in by_language.items():
        for fname in files:
            _, num = split_approach_suffix(fname)
            slot = groups.setdefault(num, {})
            if lang in slot:
                raise ValueError(
                    f"접근법 {num}번에 {lang} 파일이 2개 이상 매칭됨: "
                    f"{slot[lang]}, {fname} — 파일명 끝자리 숫자가 겹치는 것으로 보임"
                )
            slot[lang] = fname
    return groups


def approach_label(num):
    return "풀이" if num == 1 else f"풀이 {num}"


def build_complexity_section(by_language):
    """접근법별 시간/공간 표. 행 구조(몇 개 접근이 있는지, 라벨이 뭔지)는
    코드 섹션과 동일하게 group_by_approach로 결정론적으로 뽑고, 셀 값(Big-O)만
    사람이 채움. 표로 다 담기 애매한 부연설명은 표 아래 프로즈로 따로 씀."""
    groups = group_by_approach(by_language)
    lines = [COMPLEXITY_HEADING, "", "| 접근 | 시간 | 공간 |", "|---|---|---|"]
    for num in sorted(groups):
        lines.append(f"| {approach_label(num)} | | |")
    return "\n".join(lines)


def build_code_section(folder_path, by_language):
    groups = group_by_approach(by_language)
    nums = sorted(groups)
    lines = ["## 3. 코드", ""]
    for i, num in enumerate(nums):
        if i > 0:
            lines.extend(["---", ""])
        label = approach_label(num)
        langs_present = [lang for lang in LANGUAGE_DISPLAY_ORDER if lang in groups[num]]
        brackets = "".join(f"[{lang}]" for lang in langs_present)
        lines.append(f"### {label} {brackets}")
        lines.append("")
        for lang in langs_present:
            fname = groups[num][lang]
            fence = FENCE_LANG.get(lang, lang.lower())
            with open(os.path.join(folder_path, fname), encoding="utf-8") as f:
                raw = f.read()
            cleaned = clean_code(raw, lang).rstrip("\n")
            lines.append(f"```{fence}")
            lines.append(cleaned)
            lines.append("```")
            lines.append("")
    return "\n".join(lines).rstrip("\n")


def build_body(problem_url, folder_path, by_language):
    preamble = "\n".join(
        [
            "<!-- prettier-ignore -->",
            f"> [문제 링크]({problem_url})",
            "{: .prompt-info }",
        ]
    )

    idea_section = IDEA_HEADING

    # 회고/참고는 기본 스캐폴드에 넣지 않음(2026-08-27 확정) — 실제로 쓸 내용이 있을 때만
    # 사람이 "## 회고"/"## 참고" 헤딩을 직접 추가. 빈 헤딩만 미리 깔아두면 안 쓰는 경우가
    # 대부분이라 대부분의 포스트에서 그대로 방치되는 보일러플레이트가 됨.

    # 구분선 소유권 규칙은 모듈 docstring 참고(여기서 반복 안 함).
    trailing_sections = [
        idea_section,
        build_complexity_section(by_language),
        build_code_section(folder_path, by_language),
    ]
    # 맨 끝에도 "---"를 하나 더 둠 — 이건 어느 섹션에도 안 딸린, 문서 끝을 표시하는
    # 독립적인 구분선이라 회고/참고를 지워도 영향 안 받음(항상 마지막에 남음).
    return "\n\n".join(
        [preamble] + [f"---\n\n{s}" for s in trailing_sections] + ["---"]
    )


def generate_one(folder_path, force):
    """PS 레포 문제 폴더 하나를 스캐폴드 파일로 생성. 실제로 쓴 파일의 절대경로를 반환.
    실패하면 예외를 그대로 던짐(호출자가 단일 모드인지 배치 모드인지에 따라 다르게 처리)."""
    date, prefix, number = parse_folder(folder_path)
    check_cutoff(date)
    platform = get_platform(prefix)
    if prefix == "cofo":
        # PS 레포 폴더명 케이스가 들쭉날쭉함(cofo_2148a vs cofo_2148A) — Codeforces
        # 공식 표기(contestId+Index)는 Index가 대문자라 title/filename/slug 전부
        # 대문자로 통일. get_title_url_codeforces는 이미 index.upper()로 API를
        # 매칭하니 입력 케이스가 뭐든 상관없이 안전.
        number = number.upper()
    title, problem_url = get_title_and_url(prefix, number)
    by_language = find_source_files(folder_path)
    languages = [lang for lang in LANGUAGE_DISPLAY_ORDER if lang in by_language]
    if not languages:
        raise ValueError(f"코드 파일을 하나도 못 찾음 — 언어 감지 불가: {folder_path}")

    filename = build_filename(date, platform, number, title)
    front_matter = build_front_matter(date, platform, number, title, languages)
    body = build_body(problem_url, folder_path, by_language)

    platform_dir = os.path.join(DRAFTS_DIR, platform.lower())
    target_path = os.path.join(platform_dir, filename)
    if os.path.exists(target_path) and not force:
        raise FileExistsError(
            f"이미 파일이 있음(사람이 프로즈를 채워넣었을 수 있어서 임의로 덮어쓰지 않음): "
            f"{target_path}\n다시 생성하려면 --force를 붙일 것."
        )

    os.makedirs(platform_dir, exist_ok=True)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(front_matter)
        f.write("\n\n")
        f.write(body)
        f.write("\n")

    return target_path


def discover_problem_folders(ps_repo_root):
    """PS_REPO 전체를 훑어서 `{YYYY-MM}/src/day_{DD}/{prefix}_{번호}` 패턴의 문제
    폴더를 전부 찾아 경로순(=날짜순)으로 정렬해 반환. 이 패턴 자체가 "문제 폴더"의
    정의라, 안 맞는 건 애초에 대상이 아닌 걸로 보고 조용히 건너뜀(에러 아님) —
    예: PS_REPO 안의 `out/production/...` 빌드 산출물 디렉토리."""
    if not os.path.isdir(ps_repo_root):
        raise ValueError(f"PS 레포가 없음: {ps_repo_root}")

    folders = []
    for year_month in sorted(os.listdir(ps_repo_root)):
        if not re.match(r"^\d{4}-\d{2}$", year_month):
            continue
        src_dir = os.path.join(ps_repo_root, year_month, "src")
        if not os.path.isdir(src_dir):
            continue
        for day_dir in sorted(os.listdir(src_dir)):
            if not re.match(r"^day_\d{2}$", day_dir):
                continue
            day_path = os.path.join(src_dir, day_dir)
            if not os.path.isdir(day_path):
                continue
            for problem_dir in sorted(os.listdir(day_path)):
                problem_path = os.path.join(day_path, problem_dir)
                if os.path.isdir(problem_path) and re.match(
                    r"^[a-zA-Z]+_.+$", problem_dir
                ):
                    folders.append(problem_path)
    return folders


def collect_existing_slugs():
    """이 블로그의 _drafts/**/*.md + _posts/*.md front matter에서 slug 값을 전부 모음.
    배치 스캔에서 "이미 포스트/드래프트가 있는 문제"를 건너뛰는 기준으로 씀 — slug는
    {platform}-{번호}로 결정론적이라, 파일명(사람이 고칠 수도 있는 title 기반)보다
    안정적인 식별자."""
    slugs = set()
    for base in (DRAFTS_DIR, POSTS_DIR):
        if not os.path.isdir(base):
            continue
        for dirpath, _, filenames in os.walk(base):
            for fname in filenames:
                if not fname.endswith(".md"):
                    continue
                with open(os.path.join(dirpath, fname), encoding="utf-8") as f:
                    text = f.read()
                # front matter(--- ~ ---) 블록 안에서만 찾음 — 본문(회고 등)에 우연히
                # "slug: ..."로 시작하는 줄이 있어도(인용/예시) 안 낚이게.
                fm = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
                if not fm:
                    continue
                m = re.search(r"^slug:\s*(\S+)", fm.group(1), re.MULTILINE)
                if m:
                    slugs.add(m.group(1))
    return slugs


def run_batch():
    """PS_REPO 전체를 스캔해서, 블로그 개설일(BLOG_CREATION_DATE) 이후 존재하는 풀이 중
    아직 이 블로그에 포스트/드래프트가 없는 것 전부를 스캐폴드로 생성. 개별 폴더의 실패는
    그 폴더만 에러로 보고하고 나머지는 계속 진행(단일 모드처럼 즉시 죽지 않음 — 배치라서
    한 문제 때문에 전체가 막히면 안 됨). 이미 있는 파일은 절대 덮어쓰지 않음(--force 없음).

    같은 (플랫폼, 번호)가 서로 다른 day 폴더에 중복으로 존재하는 경우가 실제 PS 레포에
    있었음(재풀이/폴더 재정리 흔적으로 추정 — 과거 레거시 네이밍 시절 얘기고, 블로그
    개설 이후로는 같은 문제를 두 번 풀 일이 없을 거라고 함). 그래도 혹시 생기면: 어느
    폴더가 "진짜"인지 스크립트가 판단할 근거가 없으므로 **둘 다 스캐폴드를 만들지 않고
    충돌로만 보고** — 사람이 직접 보고 정리하게 함(예전엔 먼저 발견된 쪽만 조용히
    생성했었는데, 그러면 어느 게 만들어졌는지 매번 확인해야 해서 이쪽으로 바꿈)."""
    folders = discover_problem_folders(PS_REPO)
    existing_slugs = collect_existing_slugs()

    # 1차: 컷오프 통과 + 지원 플랫폼 + 아직 없는 슬러그인 후보만 슬러그별로 묶음.
    candidates_by_slug = {}
    skipped_existing, skipped_unsupported = [], []
    for folder_path in folders:
        date, prefix, number = parse_folder(folder_path)
        if date < BLOG_CREATION_DATE:
            continue
        if prefix not in PLATFORM_MAP:
            continue  # 플랫폼 접두사를 못 알아보는 폴더 — 문제 폴더가 아닐 가능성이 높음
        slug = build_slug(PLATFORM_MAP[prefix], number)
        if slug in existing_slugs:
            skipped_existing.append(folder_path)
            continue
        if prefix in UNSUPPORTED_PLATFORMS:
            skipped_unsupported.append(folder_path)
            continue
        candidates_by_slug.setdefault(slug, []).append(folder_path)

    created, errors, conflicts = [], [], []
    for slug, folder_paths in candidates_by_slug.items():
        if len(folder_paths) > 1:
            conflicts.append((slug, folder_paths))
            continue
        try:
            created.append(generate_one(folder_paths[0], force=False))
        except Exception as e:
            errors.append((folder_paths[0], str(e)))

    for path in created:
        print(f"생성함: {path}")
    for folder_path, msg in errors:
        print(f"에러({folder_path}): {msg}")
    for slug, folder_paths in conflicts:
        print(
            f"충돌(slug={slug}): 같은 문제가 여러 폴더에 있음 — {', '.join(folder_paths)} "
            "— 스캐폴드 안 만듦, 직접 확인 필요"
        )
    print(
        f"--- 총 {len(created)}개 생성, {len(skipped_existing)}개는 이미 있어서 스킵, "
        f"{len(skipped_unsupported)}개는 미지원 플랫폼(BOJ/SWEA)이라 스킵, "
        f"{len(conflicts)}개는 중복 충돌이라 스킵, {len(errors)}개 에러 ---"
    )


def main():
    argv = sys.argv[1:]
    force = "--force" in argv
    positional = [a for a in argv if a != "--force"]

    if not positional:
        if force:
            raise ValueError(
                "인자 없이 실행하는 배치 모드에선 --force를 안 씀 — 이미 있는 포스트/"
                "드래프트는 항상 보존됨. 특정 폴더 하나만 강제로 다시 만들려면 그 폴더"
                "경로를 직접 넘길 것."
            )
        run_batch()
        return

    if len(positional) != 1:
        print(__doc__)
        sys.exit(1)

    target_path = generate_one(positional[0], force)
    print(target_path)


if __name__ == "__main__":
    main()
