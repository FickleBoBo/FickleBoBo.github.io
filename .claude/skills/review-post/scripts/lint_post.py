"""
포스트(`_drafts/` 또는 `_posts/`의 .md)에서 정규식으로 판정되는 `STYLE.md` 규칙 위반을
잡는 결정적 린터. LLM 판단 없음 — `review-post` 오케스트레이터가 서브에이전트
dispatch 전에 돌려 결과를 리포트에 합친다.

여기엔 **오탐이 적은 규칙만** 둔다(발행본 전체에 돌려 확인). 정규식이라 한계가 있다 —
`수식 뒤 조사`는 지시어 "이"(`$N$ 이 값은`)를 오탐할 수 있고, 천 단위 콤마는 연도 표기
(19xx·20xx)를 예외로 두므로 2000·2048 같은 값은 못 잡는다. 맥락 판단이 필요한
것(평문·백틱·수식 선택, "왜"가 있는 아이디어, 코드-설명 정합성, 의존명사 띄어쓰기
전반)은 계속 `STYLE.md` + 서브에이전트 몫이다. 이 린터가 조용하다고 해서 컨벤션이
통과라는 뜻이 아니다 — 잡히는 것만 잡는다.

검사 대상은 프로즈다. front matter, 펜스 코드 블록, 인라인 코드(백틱), 헤딩, 인용(`>`)
줄은 제외하고, 표 행에는 수식 규칙(`MATH_RULES`)만 적용한다.

사용법:
    python3 lint_post.py <포스트.md> [<포스트.md> ...]
    python3 lint_post.py --all            # _drafts/·_posts/의 {platform} 폴더 전체(PS 포스트만)

출력: 이슈마다 `경로:줄: [규칙] 설명`. 종료 코드: 0 이슈 없음, 1 이슈 있음, 2 파일을 못 읽음.

코드를 고칠 때 알아야 할 것:
- 규칙을 추가하면 **먼저 `--all`로 발행본에 돌려** 오탐이 없는지 본다. 발행본의 진짜
  위반은 사용자 글이라 이 스크립트가 고치지 않고 리포트만 한다(`review-post`와 같은 원칙).
- `### 풀이` 헤딩 형식 검사는 프로즈가 아니라 구조 검사라 `lint()`가 따로 부른다(`approach_issues`).
- 태그 어휘·정규 순서는 `review-code/scripts/apply_tags.py`의 `load_tag_parents`·`order_tags`를
  그대로 쓴다(`tag_issues`). 태그 판정(어떤 태그가 맞는가)은 안 보고 형식·정합성만 검사한다.
"""

import os
import re
import sys

_SKILLS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_SKILLS_DIR, "_shared"))
sys.path.insert(0, os.path.join(_SKILLS_DIR, "review-code", "scripts"))

from apply_tags import expand_tags, load_tag_parents, order_tags
from blog_common import DRAFTS_DIR, POSTS_DIR, front_matter_block, list_platform_posts

# `### 풀이` 헤딩 형식(STYLE.md "다중 접근 — 접근 이름")
_LANGS = r" (\[[^\]]+\])+"
SINGLE_HEADING_RE = re.compile(rf"^### 풀이{_LANGS}$")
MULTI_HEADING_RE = re.compile(rf"^### 풀이 (\d+): (\S.*?){_LANGS}$")
SCAFFOLD_HEADING_RE = re.compile(
    rf"^### 풀이 (\d+){_LANGS}$"
)  # ps 스캐폴드 직후(이름 전)

FENCE_RE = re.compile(r"^\s*(```|~~~)")
INLINE_CODE_RE = re.compile(r"(`+)(.+?)\1")
MATH_RE = re.compile(r"\$([^$\n]+)\$")

# 받침이 ㄴ·ㄹ인 음절(`될거`·`본거`의 `될`·`본`). `게`는 `길게` 같은 부사형이 있어 제외
_NR_FINAL = "".join(
    chr(c) for c in range(0xAC00, 0xD7A4) if (c - 0xAC00) % 28 in (4, 8)
)

# (규칙 이름, 정규식, 설명) — 프로즈(코드·수식 제거 후)에 적용
PROSE_RULES = [
    (
        "합니다체",
        re.compile(r"(합니다|입니다|습니다|됩니다|십시오)(?![가-힣])"),
        "합니다체 금지 — 다체(~이다/~한다)로",
    ),
    (
        "해주다",
        re.compile(
            r"해(?:주(?!어(?:진|지|졌))|줬|줘|준)"
            r"|해\s(?:주(?:다|는|면|고|며|니|도|지|기|자|세|신|시|었|겠|어(?!진|지|졌)|(?![가-힣]))|줬|줘|준)"
        ),
        "`해주다`/`해줬다` 계열 금지",
    ),
    (
        "오버플로우",
        re.compile(r"(오버|언더)플로(?!우)"),
        "`오버플로우`/`언더플로우`로 표기",
    ),
    ("안 되다", re.compile(r"안되"), "`안 되다`는 띄운다(`안되다`는 별도 뜻)"),
    ("필요 없다", re.compile(r"필요없"), "`필요 없다`는 띄운다"),
    ("둘 다", re.compile(r"둘다"), "`둘 다`는 띄운다"),
    ("어휘", re.compile(r"패널티|뭉탱이"), "`페널티`/`뭉텅이`로 표기"),
    (
        "의존명사",
        re.compile(
            rf"(?<=[는은])(게|거|걸)(?![가-힣])|(?<=[{_NR_FINAL}])(?:거(?=[다야죠라])|(거|걸)(?![가-힣]))"
        ),
        "관형사형 어미 뒤 `것` 축약형은 띄운다(`하는게`→`하는 게`)",
    ),
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

# 수식($...$) 안에만 적용
MATH_RULES = [
    ("frac", re.compile(r"\\frac(?![a-z])"), "`\\frac` 금지 — `\\dfrac` 또는 슬래시"),
    (
        "곱셈 결합",
        re.compile(r"O\([^$]*\\cdot(?![a-z])"),
        "복잡도 `O(...)`의 변수곱에 `\\cdot` 금지 — `\\times`",
    ),
    # 연도(19xx·20xx)는 원래 콤마를 안 쓰는 표기라 예외
    (
        "천 단위 콤마",
        re.compile(r"(?<![\d{},.^_])(?!(?:19|20)\d\d(?!\d))\d{4,}(?![\d}])"),
        "1,000 이상 숫자는 `{,}`로 콤마(`10{,}000`)",
    ),
    (
        "천 단위 콤마",
        re.compile(r"(?<![\d{},.^_])\d{1,3}(?:,\d{3})+(?!\d)"),
        "1,000 이상 숫자는 `{,}`로 콤마(`10{,}000`) — 평문 콤마 `10,000`은 KaTeX가 여백을 넣는다",
    ),
    (
        "연산자 공백",
        re.compile(r"(?<![\\{^_])[A-Za-z0-9)]/[A-Za-z0-9(\\]"),
        "나눗셈 `/` 양쪽에 공백(`N / 2`)",
    ),
]

# 이항 `+` `-` 공백 — 위·아래첨자 안(`a_{n-1}`)과 `\text{}` 안은 붙여 쓰므로 먼저 지우고 검사
SCRIPT_RE = re.compile(r"[_^]\{[^{}]*\}|\\text\{[^}]*\}")
SIGN_RE = re.compile(r"[A-Za-z0-9)\]}][+\-][A-Za-z0-9(\\]")


def strip_inline(line):
    """인라인 코드를 같은 길이 공백으로 지운다(열 위치 보존)."""
    return INLINE_CODE_RE.sub(lambda m: " " * len(m.group(0)), line)


def prose_lines(body_lines):
    """(줄 번호, 줄, 표 행 여부) 생성. 펜스 코드·헤딩·인용·Liquid 태그 줄 제외."""
    in_fence = False
    for no, line in body_lines:
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        s = line.lstrip()
        if not s or s[0] in "#>" or s.startswith("{:") or s.startswith("<!--"):
            continue
        yield no, line, s[0] == "|"


def approach_issues(path, body, text):
    """`### 풀이` 헤딩 형식: 단일은 `### 풀이 [langs]`, 다중은 `### 풀이 N: 이름 [langs]`
    (번호 1부터 연속, 이름은 복잡도 표 "접근" 열과 일치). `_drafts/`는 review-post가
    이름을 붙이기 전이라 `### 풀이 N [langs]`도 허용한다."""
    in_fence = False
    heads = []
    for no, line in body:
        if FENCE_RE.match(line):
            in_fence = not in_fence
        elif not in_fence and line.startswith("### 풀이"):
            heads.append((no, line.rstrip()))
    is_draft = f"{os.sep}_drafts{os.sep}" in path
    issues = []
    if len(heads) == 1:
        no, line = heads[0]
        if not SINGLE_HEADING_RE.match(line):
            issues.append(
                (no, "풀이 헤딩", f"접근이 하나면 `### 풀이 [언어]...` 형식: {line}")
            )
    elif len(heads) >= 2:
        nums, names = [], []
        for no, line in heads:
            m = MULTI_HEADING_RE.match(line)
            if m:
                nums.append(int(m.group(1)))
                names.append(m.group(2))
            elif is_draft and (sm := SCAFFOLD_HEADING_RE.match(line)):
                nums.append(int(sm.group(1)))
            else:
                issues.append(
                    (
                        no,
                        "풀이 헤딩",
                        f"다중 접근은 `### 풀이 N: 이름 [언어]...` 형식: {line}",
                    )
                )
        if nums and nums != list(range(1, len(nums) + 1)) and len(nums) == len(heads):
            issues.append(
                (heads[0][0], "풀이 헤딩", f"풀이 번호가 1부터 연속이 아님: {nums}")
            )
        for name in names:
            if not re.search(rf"^\|\s*{re.escape(name)}\s*\|", text, re.MULTILINE):
                issues.append(
                    (
                        heads[0][0],
                        "풀이 헤딩",
                        f"복잡도 표 `접근` 열에 이름이 없음: {name}",
                    )
                )
    return issues


def tag_issues(path, fm, text):
    """front matter `tags:`의 형식·정합성. 어휘/조상 누락, 중복, 정규 순서, `sql` 단독·제목
    일치, 단일 접근 `warm up` 병기, 발행본의 빈 태그."""
    m = re.search(r"^tags:\s*\[(.*)\]\s*$", fm, re.MULTILINE)
    if not m:
        return []
    issues = []
    tags = [t.strip().strip('"') for t in m.group(1).split(",") if t.strip()]
    if not tags:
        if os.sep + "_posts" + os.sep in path:
            issues.append((1, "태그", "발행본인데 태그가 비어 있음"))
        return issues

    parents = load_tag_parents()
    unknown = [t for t in tags if t not in parents]
    for t in unknown:
        issues.append((1, "태그", f"어휘집에 없는 태그: {t!r}"))
    for t in tags:
        for p in parents.get(t, []):
            if p not in tags:
                issues.append((1, "태그", f"{t!r}의 조상 {p!r}가 빠짐"))
    if len(set(tags)) != len(tags):
        issues.append((1, "태그", "중복된 태그"))

    title = re.search(r"^title:\s*(.*)$", fm, re.MULTILINE)
    sql_only = bool(
        title and re.search(r'(?<![\]\[])\[MySQL\]\s*"?\s*$', title.group(1))
    )
    if "sql" in tags and len(tags) > 1:
        issues.append((1, "태그", "`sql`은 다른 태그와 병기하지 않음"))
    elif ("sql" in tags) != sql_only:
        issues.append((1, "태그", "`sql` 태그와 제목의 `[MySQL]` 단독 표기가 어긋남"))

    if "warm up" in tags and len(tags) > 1:
        if len(re.findall(r"^### 풀이", text, re.MULTILINE)) < 2:
            issues.append((1, "태그", "단일 접근인데 `warm up`을 다른 태그와 병기함"))

    if not unknown and len(set(tags)) == len(tags):
        canonical = order_tags(expand_tags(tags, parents), parents)
        if canonical != tags:
            issues.append((1, "태그", f"태그 순서가 정규 순서와 다름 → {canonical}"))
    return issues


# 복잡도 변수 설명 줄에서 서술형 명사 + 코드 변수(`수의 개수 `n``)는 쓰지 않는다 — ``입력값 `n` ``.
# 대상 표기는 STYLE.md "변수 설명 프로즈 포맷"의 고정 표를 따른다
VAR_NOUN_RE = re.compile(
    r"\$[A-Z]\$ = (?!입력값 )[가-힣][가-힣 ]* `[A-Za-z_]\w*`(?=[,.)])"
)
VAR_T_INPUT_RE = re.compile(r"\$T\$ = 입력값")


def _cell_vars(expr):
    """복잡도 셀 수식에서 변수 문자(대문자). `O(`의 O와 `\\log` 같은 명령은 제외."""
    expr = re.sub(r"\\[A-Za-z]+", "", expr).replace("O(", "(")
    return set(re.findall(r"[A-Z]", expr))


def complexity_issues(body):
    """`## 2. 복잡도` 절의 일관성 검사: 표에 쓴 변수가 변수 설명 줄에 정의돼 있는지, 대상 표기가
    고정 포맷인지, 출력 버퍼 주석이 없는지. 정의만 하고 표에 안 쓴 변수는 안 본다(언어별 소수파
    주석·설명 문장 속 변수 같은 정당한 경우가 있다)."""
    sec, on = [], False
    for no, line in body:
        if line.startswith("## 2. 복잡도"):
            on = True
            continue
        if on and (line.startswith("## ") or line.strip() == "---"):
            break
        if on:
            sec.append((no, line))
    if not sec:
        return []

    issues = []
    used, defined, first_row = set(), set(), None
    for no, line in sec:
        s = line.strip()
        if "StringBuilder" in s or "출력 버퍼" in s:
            issues.append(
                (
                    no,
                    "복잡도 출력 버퍼",
                    "출력 버퍼는 공간에 세지 않는다 — `StringBuilder` 주석 삭제",
                )
            )
        if s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if cells[0] == "접근" or set(s) <= set("|-: "):
                continue
            first_row = first_row or no
            for c in cells[1:]:
                for expr in MATH_RE.findall(c):
                    used |= _cell_vars(expr)
        elif s.startswith("("):
            defined |= set(re.findall(r"\$([A-Z])\$ =", s))
            if VAR_NOUN_RE.search(s):
                issues.append(
                    (
                        no,
                        "복잡도 변수 표기",
                        "입력 스칼라는 ``입력값 `n` ``으로 쓴다(서술형 명사 + 코드 변수 금지)",
                    )
                )
            if VAR_T_INPUT_RE.search(s):
                issues.append(
                    (
                        no,
                        "복잡도 변수 표기",
                        "`$T$`는 `테스트 케이스 수`로 쓴다(`입력값 `t`` 금지)",
                    )
                )
    for v in sorted(used - defined):
        issues.append(
            (
                first_row or sec[0][0],
                "복잡도 변수 설명",
                f"표에 쓴 `${v}$`의 정의가 표 아래 변수 설명에 없음",
            )
        )
    return issues


def lint(path):
    path = os.path.abspath(path)
    with open(path, encoding="utf-8") as f:
        text = f.read()
    issues = []

    try:
        fm = front_matter_block(text)
    except ValueError as e:
        return [(1, "front matter", str(e))]
    fm_lines = fm.count("\n") + 3  # '---' + 본문 + '---'
    body = [(i + fm_lines + 1, ln) for i, ln in enumerate(text.split("\n")[fm_lines:])]

    # front matter
    if re.search(r"^description:", fm, re.MULTILINE):
        issues.append((1, "description", "폐기된 `description:` 필드 — 삭제"))
    issues += tag_issues(path, fm, text)

    issues += approach_issues(path, body, text)
    issues += complexity_issues(body)

    for no, line, is_table in prose_lines(body):
        plain = strip_inline(line)
        maths = [mm.group(1) for mm in MATH_RE.finditer(plain)]
        plain_no_math = MATH_RE.sub(lambda mm: " " * len(mm.group(0)), plain)

        if not is_table:
            issues += prose_issues(no, plain, plain_no_math)
        for expr in maths:
            for name, pat, msg in MATH_RULES:
                if pat.search(expr):
                    issues.append((no, name, f"{msg}: ${expr}$"))
            if SIGN_RE.search(SCRIPT_RE.sub("", expr)):
                issues.append(
                    (no, "연산자 공백", f"이항 `+` `-` 양쪽에 공백: ${expr}$")
                )

    return issues


def prose_issues(no, plain, plain_no_math):
    issues = []
    if "—" in plain_no_math:
        issues.append(
            (no, "em-dash", "문장 뒤 부연절 em-dash 금지 — 마침표로 끊어 다음 문장으로")
        )
    if MATH_PARTICLE_RE.search(plain):
        issues.append(
            (no, "수식 뒤 조사", "수식 뒤 조사·단위는 붙인다(`$N$ 이`→`$N$이`)")
        )
    for name, pat, msg in PROSE_RULES:
        if pat.search(plain_no_math):
            issues.append((no, name, msg))
    return issues


def collect_all():
    return list_platform_posts(DRAFTS_DIR) + list_platform_posts(POSTS_DIR)


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(2)
    paths = collect_all() if args == ["--all"] else args

    total = unreadable = 0
    for path in paths:
        try:
            found = sorted(lint(path))
        except OSError as e:
            print(f"{path}: 읽기 실패({e.strerror})")
            unreadable += 1
            continue
        for no, rule, msg in found:
            print(f"{path}:{no}: [{rule}] {msg}")
            total += 1
    print(f"-- {len(paths)}개 파일, 이슈 {total}건", file=sys.stderr)
    sys.exit(2 if unreadable else 1 if total else 0)


if __name__ == "__main__":
    main()
