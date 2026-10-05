"""
PS 레포 풀이 폴더를 읽는 쪽 — 폴더 경로 파싱, 전체 탐색, 언어별 파일 수집, 접근법
그룹핑, 언어 표시·코드펜스 매핑. 포스트 본문을 만드는 쪽(`scaffold_post.py`)과
이미 만들어진 포스트의 코드를 갱신하는 쪽(`sync`)이 같은 규칙을 써야 해서 공유한다.

접근법 = 파일명 끝자리 숫자(`clean_code.split_approach_suffix`): `Main.java`/`Main.cpp`는
접근법 1, `Main2.java`/`Main2.cpp`는 접근법 2. 헤딩 라벨(`approach_label`)도 이 규칙의
일부라 `ps`(생성)와 `sync`(경고 메시지)가 어긋나면 안 된다.
"""

import os
import re

from clean_code import split_approach_suffix

# 언어 브라켓 표시 순서 및 확장자 매핑
# MySQL(프로그래머스 SQL 문제)은 항상 폴더에 Solution.sql 하나뿐 —
# Java/C++/Python과 동시 존재하지 않음(PS 레포 ps-new-problem 스킬 규칙).
LANGUAGE_DISPLAY_ORDER = ["Java", "C++", "Python", "MySQL"]
EXT_TO_LANGUAGE = {
    ".java": "Java",
    ".cpp": "C++",
    ".py": "Python",
    ".sql": "MySQL",
}
FENCE_LANG = {
    "Java": "java",
    "C++": "c++",
    "Python": "python",
    # 표시명은 MySQL이지만 실제 코드펜스는 "sql" — 이 레포에 설치된 Rouge(4.7.0)엔
    # mysql 전용 렉서가 없고 sql/plsql만 있음(확인함). ```mysql로 쓰면 하이라이팅
    # 없이 렌더링됨.
    "MySQL": "sql",
}

# 언어 구성이 이 집합과 일치하면 "SQL 전용 포스트"(복잡도 섹션 없음). `publish`의
# 완료 판정도 이 값을 import해 title 언어 브래킷과 대조한다(값은 여기 하나뿐).
SQL_ONLY_LANGUAGES = {"MySQL"}

# 본문 섹션 헤딩 — 스캐폴드(`scaffold_post.py`)가 만들고 `publish`의 완료 판정이 이
# 문자열을 그대로 찾는다. 챕터 번호·제목을 바꾸면 소비자 import문도 같이 확인할 것.
IDEA_HEADING = "## 1. 아이디어"
COMPLEXITY_HEADING = "## 2. 복잡도"


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


def is_fail_folder(path):
    """폴더명이 `_fail`로 끝나면 실패한 풀이 — PS 대상이 아님(대소문자 무시)."""
    return os.path.basename(path.rstrip("/")).lower().endswith("_fail")


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


def approach_label(num, total):
    """접근법 헤딩 라벨 — ps(스캐폴드 생성)와 sync(경고 메시지)가 같은 규칙을 써야
    헤딩 라벨이 서로 어긋나지 않는다. 접근이 2개 이상이면 첫 접근도 '풀이 1'로 번호를
    붙이고(STYLE.md '다중 접근 — 접근 이름'), 하나뿐이면 번호 없이 '풀이'.
    total(group_by_approach로 센 전체 접근 수)은 필수 — sync도 이 값을 넘긴다."""
    if total <= 1 and num == 1:
        return "풀이"
    return f"풀이 {num}"


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
