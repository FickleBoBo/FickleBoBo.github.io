"""
표기 규칙: 어투, 확정 가능한 맞춤법, 용어, 수식 표기. 보고만 하고 `publish`는 막지 않는다.

기계적으로 확정되는 것만 둔다. 정규식이라 한계가 있다 — `수식 뒤 조사`는 지시어 "이"(`$N$ 이 값은`)를
오탐할 수 있고, 천 단위 콤마는 연도 표기(19xx·20xx)를 예외로 두므로 2000·2048 같은 값은 못 잡는다.
일반 맞춤법, 평문·백틱·수식 선택, "왜"가 있는 아이디어, 코드-설명 정합성은 `STYLE.md` + 서브에이전트
몫이다. 이 린터가 조용하다고 해서 컨벤션이 통과라는 뜻이 아니다 — 잡히는 것만 잡는다.

검사 대상은 프로즈다. 펜스 코드 블록, 인라인 코드(백틱), 헤딩, 인용(`>`) 줄은 제외하고, 표 행에는
수식 규칙(`MATH_RULES`)만 적용한다.
"""

import re

from post_text import classify_fences

INLINE_CODE_RE = re.compile(r"(`+)(.+?)\1")
MATH_RE = re.compile(r"\$([^$\n]+)\$")

# 받침이 ㄴ·ㄹ인 음절(`될거`·`본거`의 `될`·`본`). `게`는 `길게` 같은 부사형이 있어 제외
_NR_FINAL = "".join(
    chr(c) for c in range(0xAC00, 0xD7A4) if (c - 0xAC00) % 28 in (4, 8)
)

# (규칙 이름, 정규식, 설명) — 프로즈(코드·수식 제거 후)에 적용
PROSE_RULES = [
    # 어투: 다체(~이다/~한다)로 고정. 이탈하는 종결어미만 본다
    (
        "합니다체",
        re.compile(r"(합니다|입니다|습니다|됩니다|십시오|[합입습됩]니까)(?![가-힣])"),
        "합니다체 금지 — 다체(~이다/~한다)로",
    ),
    (
        "해요체",
        re.compile(
            r"(?:[아어여해와봐돼]요|이에요|예요|네요|군요|까요|세요|죠|지요|게요|거든요|는데요|합시다)(?![가-힣])"
        ),
        "해요체 금지 — 다체(~이다/~한다)로",
    ),
    # 맞춤법: 오류가 확정되는 고정 패턴만. 일반 맞춤법은 리뷰어(STYLE.md 체크리스트) 몫
    ("안 되다", re.compile(r"안되|안돼"), "`안 되다`는 띄운다(`안되다`는 별도 뜻)"),
    ("필요 없다", re.compile(r"필요없"), "`필요 없다`는 띄운다"),
    ("둘 다", re.compile(r"둘다"), "`둘 다`는 띄운다"),
    (
        "의존명사",
        re.compile(
            rf"(?<=[는은])(게|거|걸)(?![가-힣])|(?<=[{_NR_FINAL}])(?<![근선])(?:거(?=[다야죠라])|(거|걸)(?![가-힣]))"
        ),
        "관형사형 어미 뒤 `것` 축약형은 띄운다(`하는게`→`하는 게`)",
    ),
    # 용어집: 표기가 갈리는 외래어를 한쪽(관용형)으로 고정. 새 용어는 한 줄씩 추가한다
    (
        "용어",
        re.compile(r"(오버|언더)플로(?!우)"),
        "`오버플로우`/`언더플로우`로 표기",
    ),
    ("용어", re.compile(r"패널티"), "`페널티`로 표기"),
]

# 수식($...$) 뒤 조사·단위는 붙여 쓴다(`$N$ 이`→`$N$이`) — 수식을 남긴 채(인라인 코드만 제거) 적용.
# 조사는 뒤에 한글이 이어지면 다른 단어(`이`+`미지`)일 수 있어 단독일 때만, 단위는 `개의`·`개라서`·
# `층짜리`처럼 조사·접미가 붙은 꼴까지 잡는다(`단계`·`번호`·`분포`는 단위가 아니라 제외)
_MATH_PARTICLES = r"의|와|과|에서|에|을|를|까지|부터|보다|마다|로|으로|은|는|이|가|라고|라는|이며|이므로|이라|이다|이고|일|인|만|도"
_MATH_UNITS = r"개|명|층|칸|번|단|배|회"
# 조사가 겹친 꼴·서술격 활용형(`이라서`·`이면`·`까지의`)과 단위 뒤 조사(`킬로그램을`)는 위 단독 조사
# 규칙의 `(?![가-힣])`에 막혀 놓치므로 따로 나열한다. 뒤에 한글이 더 이어지면 다른 단어라 제외
_MATH_COMPOUNDS = (
    r"이라서|이라면|이면|이어서|이어도|이지만|이든"
    r"|까지의|까지는|까지도|부터는|에서의|에서는|에는|에도|로는|으로는"
    r"|킬로그램[을를이가은는의과와]"
)
MATH_PARTICLE_RE = re.compile(
    rf"\$ (?:(?:{_MATH_PARTICLES}|킬로그램|번째|{_MATH_COMPOUNDS})(?![가-힣])"
    rf"|(?:{_MATH_UNITS})(?=(?:의|라서|로|가|를|은|는|이|짜리|째|씩)|(?![가-힣])))"
)

# 수식($...$) 안에만 적용. kramdown이 마크다운을 먼저 처리한 뒤 MathJax가 수식을 렌더하므로
# `*`는 한 단락에 둘이면 `<em>`이 되고, `\{`·`\|`·`\\`는 역슬래시가 먹힌다(실측). 이스케이프가
# 필요 없는 `\ast`·`\lbrace`·`\vert`가 안전하다.
MATH_RULES = [
    ("frac", re.compile(r"\\frac(?![a-z])"), "`\\frac` 금지 — `\\dfrac` 또는 슬래시"),
    (
        "수식 깨짐",
        re.compile(r"\*"),
        "수식 안 `*`는 kramdown이 강조로 읽을 수 있음 — `\\ast` 또는 `\\times`",
    ),
    (
        "수식 깨짐",
        re.compile(r"(?<!\\)\\[{}]"),
        "`\\{` `\\}`는 역슬래시가 사라짐 — `\\lbrace` `\\rbrace`",
    ),
    (
        "수식 깨짐",
        re.compile(r"\\\|"),
        "`\\|`는 역슬래시가 사라짐 — `\\Vert` 또는 `\\vert`",
    ),
    (
        "수식 깨짐",
        re.compile(r"\\\\"),
        "`\\\\`는 역슬래시가 줄어듦 — 수식 줄바꿈은 쓰지 않는다",
    ),
    # 연도(19xx·20xx)는 원래 콤마를 안 쓰는 표기라 예외
    (
        "천 단위 콤마",
        re.compile(
            r"(?<![\d},.^_])(?<!_\{)(?<!\^\{)(?!(?:19|20)\d\d(?!\d))\d{4,}(?!\d)"
        ),
        "1,000 이상 숫자는 `{,}`로 콤마(`10{,}000`)",
    ),
    (
        "천 단위 콤마",
        re.compile(r"(?<![\d{},.^_\[(])\d{1,3}(?:,\d{3})+(?!\d)"),
        "1,000 이상 숫자는 `{,}`로 콤마(`10{,}000`) — 평문 콤마 `10,000`은 MathJax가 여백을 넣는다",
    ),
    (
        "연산자 공백",
        re.compile(r"(?<![\\{^_])[A-Za-z0-9)]/[A-Za-z0-9(\\]"),
        "나눗셈 `/` 양쪽에 공백(`N / 2`)",
    ),
]

# 이항 `+` `-` 공백 — 위·아래첨자 안(`a_{n-1}`)과 `\text{}` 안은 붙여 쓰므로 먼저 지우고 검사
SCRIPT_RE = re.compile(r"[_^]\{[^{}]*\}|\\text\{[^}]*\}")
# `\text{km/h}`의 슬래시는 단위 표기라 `연산자 공백` 대상 아님
TEXT_RE = re.compile(r"\\text\{[^}]*\}")
SIGN_RE = re.compile(r"[A-Za-z0-9)\]}][+\-][A-Za-z0-9(\\]")


def _strip_inline(line):
    """인라인 코드를 같은 길이 공백으로 지운다(열 위치 보존)."""
    return INLINE_CODE_RE.sub(lambda m: " " * len(m.group(0)), line)


def _prose_lines(body):
    """(줄 번호, 줄, 표 행 여부) 생성. 펜스 코드·헤딩·인용·Liquid 태그 줄 제외."""
    kinds, _ = classify_fences([line for _, line in body])
    for (no, line), kind in zip(body, kinds):
        if kind != "text":
            continue
        s = line.lstrip()
        if not s or s[0] in "#>" or s.startswith("{:") or s.startswith("<!--"):
            continue
        yield no, line, s[0] == "|"


def _text_issues(no, plain, plain_no_math):
    issues = []
    if "—" in plain_no_math:
        issues.append((no, "em-dash", "em-dash 금지 — 마침표로 끊거나 다른 문장부호로"))
    if MATH_PARTICLE_RE.search(plain):
        issues.append(
            (no, "수식 뒤 조사", "수식 뒤 조사·단위는 붙인다(`$N$ 이`→`$N$이`)")
        )
    for name, pat, msg in PROSE_RULES:
        if pat.search(plain_no_math):
            issues.append((no, name, msg))
    return issues


def _math_issues(no, expr, is_table):
    issues = []
    if is_table and re.search(r"(?<!\\)\|", expr):
        issues.append(
            (no, "수식 깨짐", f"표 셀 안 수식의 `|`는 열이 갈라짐 — `\\vert`: ${expr}$")
        )
    for name, pat, msg in MATH_RULES:
        target = TEXT_RE.sub("", expr) if name == "연산자 공백" else expr
        if pat.search(target):
            issues.append((no, name, f"{msg}: ${expr}$"))
    if SIGN_RE.search(SCRIPT_RE.sub("", expr)):
        issues.append((no, "연산자 공백", f"이항 `+` `-` 양쪽에 공백: ${expr}$"))
    return issues


def prose_issues(body):
    """`body`는 (줄 번호, 줄) 리스트."""
    issues = []
    for no, line, is_table in _prose_lines(body):
        plain = _strip_inline(line)
        plain_no_math = MATH_RE.sub(lambda m: " " * len(m.group(0)), plain)
        if not is_table:
            issues += _text_issues(no, plain, plain_no_math)
        for m in MATH_RE.finditer(plain):
            issues += _math_issues(no, m.group(1), is_table)
    return issues
