"""
포스트 본문 텍스트 다루기: front matter 필드(읽기, `tags` 쓰기, YAML 문자열 이스케이프), 코드 펜스 분류, `## ` 섹션 범위.
문자열을 받아 문자열·값을 돌려주는 순수 함수만 둔다(파일 입출력은 호출하는 쪽 몫).
"""

import json
import re


def yaml_dq(s):
    """YAML 큰따옴표 문자열 안에 안전하게 넣기 위한 이스케이프."""
    return s.replace("\\", "\\\\").replace('"', '\\"')


def front_matter_block(post_text):
    m = re.match(r"^---\n(.*?)\n---\n", post_text, re.DOTALL)
    if not m:
        raise ValueError("front matter(--- ~ ---) 블록을 못 찾음")
    return m.group(1)


def yaml_scalar_value(front_matter_text, field):
    """front matter에서 `{field}: ...` 값을 뽑는다. 따옴표 없는 스칼라(`title: 그냥 이렇게`)도 유효한
    YAML이라 따옴표 유무 둘 다 처리한다. 필드가 없으면 None, 값이 비면 ""을 돌려준다.

    값은 한 줄이라고 전제한다(정규식이 그 줄만 읽는다). `title: |` 같은 여러 줄 블록 스칼라는 첫 줄만
    읽고 나머지는 조용히 무시한다."""
    m = re.search(rf"^{field}:[ \t]*(.*)$", front_matter_text, re.MULTILINE)
    if not m:
        return None
    raw = m.group(1).strip()
    if len(raw) >= 2 and raw[0] == raw[-1] == '"':
        return raw[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    if len(raw) >= 2 and raw[0] == raw[-1] == "'":
        return raw[1:-1].replace("''", "'")
    return raw


# `tags: [...]` 배열. 80자를 넘으면 Prettier가 여러 줄로 나누므로 줄바꿈을 허용한다.
_TAGS_RE = re.compile(r"^tags:\s*\[([^\]]*)\][ \t]*$", re.MULTILINE)
_PRINT_WIDTH = 80  # Prettier 기본값


def read_tags(front_matter_text):
    """front matter의 `tags: ["a", "b"]` 배열(한 줄·여러 줄)을 리스트로. 그 형태가 없으면 None."""
    m = _TAGS_RE.search(front_matter_text)
    if not m:
        return None
    return [t.strip().strip('"') for t in m.group(1).split(",") if t.strip()]


def _format_tags(tags):
    """Prettier가 두는 모양 그대로: 한 줄, 안 되면 다음 줄에 배열, 그것도 넘으면 태그마다 한 줄."""
    array = json.dumps(tags, ensure_ascii=False)
    if len(f"tags: {array}") <= _PRINT_WIDTH:
        return f"tags: {array}"
    if len(f"  {array}") <= _PRINT_WIDTH:
        return f"tags:\n  {array}"
    items = "".join(f"    {json.dumps(t, ensure_ascii=False)},\n" for t in tags)
    return f"tags:\n  [\n{items}  ]"


def replace_tags(post_text, tags):
    """`tags` 항목만 새 배열로 바꾼 본문. front matter에 `tags: [...]`가 없으면 ValueError."""
    m = _TAGS_RE.search(front_matter_block(post_text))
    if not m:
        raise ValueError("front matter 안에서 `tags: [...]`를 못 찾음")
    start = len("---\n") + m.start()  # front_matter_block은 여는 `---\n` 뒤부터다
    return post_text[:start] + _format_tags(tags) + post_text[start + len(m.group(0)) :]


def read_front_matter(post_text):
    """(date, slug). 둘 중 하나라도 없으면 ValueError."""
    raw = front_matter_block(post_text)
    date = yaml_scalar_value(raw, "date")
    slug = yaml_scalar_value(raw, "slug")
    if not date or not slug:
        raise ValueError("front matter에 date 또는 slug가 없음")
    return date, slug


def extract_title(post_text):
    title = yaml_scalar_value(front_matter_block(post_text), "title")
    if title is None:
        raise ValueError("front matter에 title이 없음")
    return title


_FENCE_LINE_RE = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")


def classify_fences(lines):
    """줄마다 `text`(펜스 밖)·`open`(여는 펜스)·`code`(펜스 안)·`close`(닫는 펜스)를 매긴 리스트와,
    끝까지 안 닫힌 펜스의 줄 인덱스(없으면 None)를 돌려준다. 닫는 펜스는 여는 것과 같은 문자에
    같거나 긴 길이이고 뒤에 아무것도 없는 줄이다(CommonMark) — 4중 백틱 안의 3중 백틱은 코드다.
    한 줄에서 열고 닫는 ```` ```x``` ````은 펜스가 아니다."""
    kinds = []
    opener = None  # (문자, 길이, 줄 인덱스)
    for i, line in enumerate(lines):
        m = _FENCE_LINE_RE.match(line)
        if opener is None:
            if m and not (m.group(1)[0] == "`" and "`" in m.group(2)):
                opener = (m.group(1)[0], len(m.group(1)), i)
                kinds.append("open")
            else:
                kinds.append("text")
        elif (
            m
            and m.group(1)[0] == opener[0]
            and len(m.group(1)) >= opener[1]
            and not m.group(2).strip()
        ):
            opener = None
            kinds.append("close")
        else:
            kinds.append("code")
    return kinds, (opener[2] if opener else None)


def section_span(text, heading_pattern):
    """`heading_pattern`(정규식, 줄 전체와 매칭)에 맞는 `## ` 헤딩부터 다음 `## ` 헤딩 앞까지의
    (시작, 끝) 문자 오프셋. 헤딩이 없으면 None. 코드 펜스 안의 `## ` 줄(코드 주석 등)은 경계로
    보지 않는다."""
    lines = text.split("\n")
    kinds, _ = classify_fences(lines)
    offset = 0
    start = None
    for line, kind in zip(lines, kinds):
        if kind == "text":
            if start is None:
                if re.fullmatch(heading_pattern, line.rstrip()):
                    start = offset
            elif line.startswith("## "):
                return start, offset
        offset += len(line) + 1
    return None if start is None else (start, len(text))
