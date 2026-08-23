#!/usr/bin/env python3
"""
PS 레포의 코드를 블로그에 임베드하기 전 결정론적으로 정리하는 공유 유틸.
`ps`(최초 임베드)와 `sync`(재동기화) 스킬이 동일하게 불러써서 중복을 없앤다.
PS 레포 원본 파일은 절대 건드리지 않음 — 항상 문자열을 받아서 문자열을 반환.

정리 내용(자바만 해당, 지금까지 확인된 실제 문제 기준 — 다른 언어는 아직 손볼 이유가
없어서 그대로 통과시킴):
- `package ...;` 선언 줄(+ 뒤따르는 빈 줄) 제거 — PS 레포 내부 폴더 구조가 그대로
  노출되는 데다, 그대로 두면 남이 복붙했을 때 컴파일이 안 됨
- 번호 붙은 클래스명(`Solution2`, `Main3` 등) 정규화 — 같은 폴더에 여러 접근이
  있을 때 자바 파일명 제약(퍼블릭 클래스명 = 파일명, 폴더 내 중복 불가) 때문에
  어쩔 수 없이 붙는 번호인데, 블로그에 그대로 노출하면 지저분하고 "복붙하면
  그대로 채점 통과"라는 목적에도 안 맞음. 클래스 선언줄만 바꾸면 생성자명이
  안 맞아서 컴파일이 깨지므로, 파일 전체에서 해당 식별자를 단어 경계 기준으로
  일괄 치환함.

`split_approach_suffix`는 파일명 끝자리 숫자 = 접근법(같은 문제를 푼 다른 방식)
번호라는 컨벤션을 다루는 공유 유틸. ps가 파일들을 "풀이"/"풀이 N" 헤딩으로
그룹핑할 때, sync가 포스트의 어느 헤딩 구간을 갱신할지 찾을 때 둘 다 이 규칙을
똑같이 써야 해서 여기(공유 모듈)에 둠.
"""

import os
import re

PACKAGE_LINE_RE = re.compile(r"^package\s+[\w.]+;\n(?:\n)?", re.MULTILINE)
CLASS_NAME_RE = re.compile(r"\bclass\s+(\w+)")
TRAILING_DIGITS_RE = re.compile(r"^(.+?)(\d+)$")


def strip_trailing_digits(name: str) -> str:
    """끝자리 숫자를 뗀 이름. 숫자가 없으면 원본 그대로."""
    m = TRAILING_DIGITS_RE.match(name)
    return m.group(1) if m else name


def split_approach_suffix(filename: str):
    """파일명(확장자 포함)에서 끝자리 숫자를 접근법 번호로 분리한다.
    예: "Solution2.cpp" -> ("Solution.cpp", 2), "Solution.cpp" -> ("Solution.cpp", 1).
    반환: (번호 뗀 정규 파일명, 접근법 번호 — 숫자 없으면 1)"""
    base, ext = os.path.splitext(filename)
    canonical_base = strip_trailing_digits(base)
    if canonical_base == base:
        return filename, 1
    m = TRAILING_DIGITS_RE.match(base)
    return f"{canonical_base}{ext}", int(m.group(2))


def clean_java(source: str) -> str:
    source = PACKAGE_LINE_RE.sub("", source, count=1)

    # "첫 번째로 나오는 class"가 아니라 "이름 끝에 숫자가 붙은 class"를 찾음 — 접근법이
    # 여러 개일 때 번호가 붙는 대상은 항상 이거고(Java 파일명 제약 때문에 어쩔 수 없이
    # 붙는 번호), public 여부와 무관함(PS 레포에 "class Solution2"처럼 public 없이
    # 번호만 붙는 경우가 실제로 흔함). 앞에 헬퍼 클래스(Pair/Node 등, 번호 없음)가
    # 먼저 선언돼있어도 그쪽은 strip해도 이름이 안 바뀌니 건너뛰고 넘어감.
    for m in CLASS_NAME_RE.finditer(source):
        original = m.group(1)
        canonical = strip_trailing_digits(original)
        if canonical != original:
            source = re.sub(rf"\b{re.escape(original)}\b", canonical, source)
            break

    return source


def clean_code(source: str, language: str) -> str:
    """language는 EXT_TO_LANGUAGE(resolve_filename.py)의 표시명("Java"/"C++"/"Python")."""
    if language == "Java":
        return clean_java(source)
    # C++/Python은 지금까지 실제로 문제된 케이스가 없어서 그대로 통과.
    # (패키지 개념이 없고, 번호 붙은 클래스명 충돌도 관찰된 적 없음 — 나중에
    # 실제 사례 생기면 그때 확장)
    return source
