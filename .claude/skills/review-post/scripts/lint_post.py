"""
포스트(`_drafts/` 또는 `_posts/`의 .md)에서 정규식으로 판정되는 `STYLE.md` 규칙 위반을
잡는 결정적 린터. LLM 판단 없음 — `review-post` 오케스트레이터가 서브에이전트
dispatch 전에 돌려 결과를 리포트에 합친다.

여기엔 **오탐이 거의 없는 규칙만** 둔다(발행본 전체에 돌려 확인). 맥락 판단이 필요한
것(평문·백틱·수식 선택, "왜"가 있는 아이디어, 코드-설명 정합성, 의존명사 띄어쓰기
전반)은 계속 `STYLE.md` + 서브에이전트 몫이다. 이 린터가 조용하다고 해서 컨벤션이
통과라는 뜻이 아니다 — 잡히는 것만 잡는다.

검사 대상은 프로즈뿐이다. front matter, 펜스 코드 블록, 인라인 코드(백틱), 표 행,
헤딩, 인용(`>`) 줄은 규칙별로 제외한다.

사용법:
    python3 lint_post.py <포스트.md> [<포스트.md> ...]
    python3 lint_post.py --all            # _drafts/ + _posts/ 전체

출력: 이슈마다 `경로:줄: [규칙] 설명`. 이슈가 하나라도 있으면 종료 코드 1.

코드를 고칠 때 알아야 할 것:
- 규칙을 추가하면 **먼저 `--all`로 발행본에 돌려** 오탐이 없는지 본다. 발행본의 진짜
  위반은 사용자 글이라 이 스크립트가 고치지 않고 리포트만 한다(`review-post`와 같은 원칙).
- `### 풀이` 헤딩 형식 검사는 프로즈가 아니라 구조 검사라 `lint()`가 따로 부른다(`approach_issues`).
- 태그 어휘는 `review-code/scripts/apply_tags.py`의 `load_tag_parents`를 그대로 쓴다.
"""

import os
import re
import sys

_SKILLS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(_SKILLS_DIR, "_shared"))
sys.path.insert(0, os.path.join(_SKILLS_DIR, "review-code", "scripts"))

from apply_tags import load_tag_parents
from blog_common import DRAFTS_DIR, POSTS_DIR, front_matter_block

# tags.yaml 어휘집엔 없지만 SQL 포스트가 관행적으로 쓰는 태그(문서화 안 된 관행)
UNLISTED_OK = {"sql"}

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

# (규칙 이름, 정규식, 설명) — 프로즈(코드·수식 제거 후)에 적용
PROSE_RULES = [
    (
        "합니다체",
        re.compile(r"(합니다|입니다|습니다|됩니다|십시오)(?![가-힣])"),
        "합니다체 금지 — 다체(~이다/~한다)로",
    ),
    ("해주다", re.compile(r"해\s?(주|줬|줘)"), "`해주다`/`해줬다` 계열 금지"),
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
        re.compile(r"(?<=[는은])(게|거|걸)(?![가-힣])"),
        "관형사형 어미 뒤 `것` 축약형은 띄운다(`하는게`→`하는 게`)",
    ),
]

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
        "연산자 공백",
        re.compile(r"(?<![\\\w{^_])[A-Za-z0-9)]/[A-Za-z0-9(\\]"),
        "나눗셈 `/` 양쪽에 공백(`N / 2`)",
    ),
]


def strip_inline(line):
    """인라인 코드를 같은 길이 공백으로 지운다(열 위치 보존)."""
    return INLINE_CODE_RE.sub(lambda m: " " * len(m.group(0)), line)


def prose_lines(body_lines):
    """(줄 번호, 프로즈 줄) 생성. 펜스 코드·표·헤딩·인용·Liquid 태그 줄 제외."""
    in_fence = False
    for no, line in body_lines:
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        s = line.lstrip()
        if not s or s[0] in "|#>" or s.startswith("{:") or s.startswith("<!--"):
            continue
        yield no, line


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


def lint(path):
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
    m = re.search(r"^tags:\s*\[(.*)\]\s*$", fm, re.MULTILINE)
    # 대회 후기는 PS 태그 어휘를 안 쓰는 별도 장르
    if m and f"{os.sep}contest{os.sep}" not in path:
        tags = [t.strip().strip('"') for t in m.group(1).split(",") if t.strip()]
        parents = load_tag_parents()
        for t in tags:
            if t in UNLISTED_OK:
                continue
            if t not in parents:
                issues.append((1, "태그", f"어휘집에 없는 태그: {t!r}"))
                continue
            for p in parents[t]:
                if p not in tags:
                    issues.append((1, "태그", f"{t!r}의 조상 {p!r}가 빠짐"))

    issues += approach_issues(path, body, text)

    for no, line in prose_lines(body):
        plain = strip_inline(line)
        maths = [mm.group(1) for mm in MATH_RE.finditer(plain)]
        plain_no_math = MATH_RE.sub(lambda mm: " " * len(mm.group(0)), plain)

        if "—" in plain_no_math:
            issues.append(
                (
                    no,
                    "em-dash",
                    "문장 뒤 부연절 em-dash 금지 — 마침표로 끊어 다음 문장으로",
                )
            )
        for name, pat, msg in PROSE_RULES:
            if pat.search(plain_no_math):
                issues.append((no, name, msg))
        for expr in maths:
            for name, pat, msg in MATH_RULES:
                if pat.search(expr):
                    issues.append((no, name, f"{msg}: ${expr}$"))

    return issues


def collect_all():
    paths = []
    for root in (DRAFTS_DIR, POSTS_DIR):
        for d, _, files in os.walk(root):
            for f in files:
                if f.endswith(".md"):
                    paths.append(os.path.join(d, f))
    return sorted(paths)


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    paths = collect_all() if args == ["--all"] else args

    total = 0
    for path in paths:
        for no, rule, msg in sorted(lint(path)):
            print(f"{path}:{no}: [{rule}] {msg}")
            total += 1
    print(f"-- {len(paths)}개 파일, 이슈 {total}건", file=sys.stderr)
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
