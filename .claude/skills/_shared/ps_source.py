"""
PS 레포 문제 폴더를 읽는 쪽. 폴더가 `{YYYY-MM}/src/day_{DD}/{접두사}_{번호}/`
규칙과 소스 파일 네이밍을 항상 지킨다고 가정하고 검증 없이 읽는다.
접근법 = 파일명 끝자리 숫자(`Main.java`/`Main.cpp`는 1, `Main2.*`는 2).
포스트의 `date`/`slug`로 그 폴더를 찾는 것(`resolve_source_folder`)도 여기다.
"""

import os
import re

from repo import PREFIX_OF_PLATFORM, PS_REPO

LANGUAGE_DISPLAY_ORDER = ["Java", "C++", "Python", "MySQL"]
LANGUAGE_OF_EXT = {".java": "Java", ".cpp": "C++", ".py": "Python", ".sql": "MySQL"}
# MySQL의 코드펜스가 sql인 이유: 이 레포의 Rouge(4.7.0)엔 mysql 렉서가 없다.
FENCE_OF_LANGUAGE = {"Java": "java", "C++": "c++", "Python": "python", "MySQL": "sql"}
LANGUAGE_OF_FENCE = {v: k for k, v in FENCE_OF_LANGUAGE.items()}

SQL_ONLY_LANGUAGES = {"MySQL"}

_TRAILING_DIGITS_RE = re.compile(r"^(.+?)(\d+)$")


def is_sql_only(languages):
    """언어 목록이 SQL 전용(MySQL뿐)인지 — 이런 포스트는 코드 섹션이 `## 2. 쿼리`다."""
    return set(languages) == SQL_ONLY_LANGUAGES


def split_approach_suffix(filename):
    """`Solution2.cpp` -> ("Solution.cpp", 2), `Solution.cpp` -> ("Solution.cpp", 1)."""
    base, ext = os.path.splitext(filename)
    m = _TRAILING_DIGITS_RE.match(base)
    if not m:
        return filename, 1
    return f"{m.group(1)}{ext}", int(m.group(2))


def find_source_files(folder_path):
    """{언어: [파일명, ...]} — 확장자로 판별한 폴더 안 소스 파일, 파일명 정렬."""
    by_language = {}
    for entry in sorted(os.listdir(folder_path)):
        lang = LANGUAGE_OF_EXT.get(os.path.splitext(entry)[1].lower())
        if lang:
            by_language.setdefault(lang, []).append(entry)
    return by_language


def group_by_approach(by_language):
    """{언어: [파일명]} -> {접근법 번호: {언어: 파일명}}."""
    groups = {}
    for lang, files in by_language.items():
        for fname in files:
            groups.setdefault(split_approach_suffix(fname)[1], {})[lang] = fname
    return groups


def resolve_source_folder(date, slug):
    """포스트 front matter의 date/slug로 PS 레포 원본 폴더의 실제 경로를 역산하고
    존재를 검증한다. 대소문자는 재구성한 이름을 믿지 않고 실제 디렉토리 엔트리명으로
    교체한다 — macOS(APFS)는 대소문자를 구분하지 않아 `os.path.isdir`가 틀린 대소문자도
    통과시키지만 git은 구분해서, 어긋난 경로로 git을 돌리면 대상이 조용히 안 걸린다."""
    platform_lower, _, number = slug.partition("-")
    prefix = PREFIX_OF_PLATFORM.get(platform_lower)
    if not prefix:
        raise ValueError(f"slug의 플랫폼 부분을 못 알아봄: {slug}")

    # slug는 항상 소문자라 Codeforces 인덱스 문자(예: 1553A)의 대문자가 사라진다.
    # PS 레포 폴더명은 대문자를 쓰므로 여기서 복원. 다른 플랫폼은 번호가 숫자뿐이라 무해.
    if prefix == "cofo":
        number = number.upper()

    day_dir = os.path.join(PS_REPO, date[:7], "src", f"day_{date[8:10]}")
    folder_name = f"{prefix}_{number}"
    entries = os.listdir(day_dir) if os.path.isdir(day_dir) else []
    actual_name = next((e for e in entries if e.lower() == folder_name.lower()), None)
    if actual_name is None:
        raise ValueError(
            f"PS 레포에 해당 폴더가 없음(경로 재구성 결과): {os.path.join(day_dir, folder_name)}"
        )
    return os.path.join(day_dir, actual_name)
