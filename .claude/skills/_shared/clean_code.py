"""
블로그에 임베드하기 전 코드를 정리한다. 문자열을 받아 문자열을 반환하며 PS 레포 원본은 건드리지 않는다.
정리는 Java에만 있다:
- `package ...;` 줄 제거 — 복붙하면 컴파일이 안 된다.
- 접근법 파일(`Main2.java`)의 클래스명에 파일명 때문에 붙은 번호를 뗀다(`Main2` → `Main`).
  파일명 기준으로 그 클래스만, 단어 경계로 전부 치환한다(생성자명 등이 같이 바뀌어야 함).
"""

import os
import re

from ps_source import split_approach_suffix

PACKAGE_LINE_RE = re.compile(r"^package\s+[\w.]+;\n(?:\n)?", re.MULTILINE)


def clean_code(source, language, filename):
    if language != "Java":
        return source
    source = PACKAGE_LINE_RE.sub("", source, count=1)
    class_name = os.path.splitext(filename)[0]
    canonical = os.path.splitext(split_approach_suffix(filename)[0])[0]
    if canonical != class_name:
        source = re.sub(rf"\b{re.escape(class_name)}\b", canonical, source)
    return source
