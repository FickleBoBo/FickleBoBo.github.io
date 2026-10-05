"""
PS 레포 문제 폴더 경로를 받아서, 이 블로그의 포스트 파일명 + front matter +
본문 스켈레톤을 결정론적으로 생성한다. LLM 판단 없음 — 정규식/API 응답 파싱/
파일 스캔/문자열 치환만 함.

**섹션 구성·챕터 번호 같은 스켈레톤 '구조'는 `ps/SKILL.md`가 정본.** 여기 docstring은
사용법 + 코드를 고칠 때 바로 옆 코드만 봐선 안 보이는 '왜'(구분선 소유권, IAL 회피
등 — 아래 "코드를 고칠 때 알아야 할 것")만 남겨둠. 겹쳐 쓰면 둘 중 하나가 stale해져서
분리함.

지원 플랫폼: Programmers/LeetCode/Codeforces/BOJ(`PLATFORM_MAP`). SWEA는
`UNSUPPORTED_PLATFORMS`로 보류 중 — 이유는 SKILL.md 참고. 컷오프
(`SCOPE_START_DATE`) 이전 폴더는 전부 무시.

이 파일은 포스트 본문·front matter 생성과 배치/CLI만 맡는다. 나머지는 분리돼 있음:
네트워크 제목 조회는 `problem_lookup.py`, PS 레포 폴더 읽기·언어 매핑·접근법 그룹핑은
`ps_source.py`(`sync`도 같이 씀), 코드 문자열 정리는 `clean_code.py`.

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
- 섹션 헤딩 상수(`IDEA_HEADING`/`COMPLEXITY_HEADING`)는 `ps_source.py`에 있다(`publish`의
  완료 판정과 공유).

사용법·동작은 `ps/SKILL.md`의 `## 실행`이 정본.
"""

import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "_shared"))
)
from blog_common import (
    DRAFTS_DIR,
    PLATFORM_MAP,
    POSTS_DIR,
    PS_REPO,
    front_matter_block,
    sanitize_filename,
    yaml_dq,
    yaml_scalar_value,
)
from clean_code import clean_code
from problem_lookup import get_title_and_url
from ps_source import (
    COMPLEXITY_HEADING,
    FENCE_LANG,
    IDEA_HEADING,
    LANGUAGE_DISPLAY_ORDER,
    SQL_ONLY_LANGUAGES,
    approach_label,
    discover_problem_folders,
    find_source_files,
    group_by_approach,
    is_fail_folder,
    parse_folder,
)

# 이 날짜 이전 풀이는 블로그 파이프라인의 대상이 아님(블로그 개설일 2026-08-17과는
# 무관 — 개설일 이전이어도 이 날짜 이후는 전 스킬의 대상).
SCOPE_START_DATE = "2025-12-01"


# 제목 자동조회가 아직 구현 안 된(또는 원천 서비스 문제로 막힌) 플랫폼
UNSUPPORTED_PLATFORMS = {"swea"}


def check_cutoff(date):
    if date < SCOPE_START_DATE:
        raise ValueError(
            f"대상 시작일({SCOPE_START_DATE}) 이전 풀이({date})는 대상이 아님 "
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


def build_filename(date, platform, number, title):
    return f"{date}-{platform} {number} {sanitize_filename(title)}.md"


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
        f"slug: {slug}",
        f"media_subpath: {media_subpath}",
        "math: true",
        "mermaid: false",
        "---",
    ]
    return "\n".join(lines)


def build_complexity_section(by_language):
    """접근법별 시간/공간 표. 행 구조(몇 개 접근이 있는지, 라벨이 뭔지)는
    코드 섹션과 동일하게 group_by_approach로 결정론적으로 뽑고, 셀 값(Big-O)만
    사람이 채움. 표로 다 담기 애매한 부연설명은 표 아래 프로즈로 따로 씀."""
    groups = group_by_approach(by_language)
    lines = [COMPLEXITY_HEADING, "", "| 접근 | 시간 | 공간 |", "|---|---|---|"]
    for num in sorted(groups):
        lines.append(f"| {approach_label(num, len(groups))} | | |")
    return "\n".join(lines)


def build_code_section(folder_path, by_language, heading_num=3, heading_text="코드"):
    """heading_num: 이 섹션의 챕터 번호. SQL 전용 포스트는 앞의 `## 2. 복잡도`가
    통째로 빠지므로 코드 섹션이 2번으로 한 칸 당겨짐(build_body에서 결정).
    heading_text: SQL 전용 포스트는 "코드" 대신 "쿼리"(언어가 MySQL 하나뿐이라
    "코드"보다 정확한 지칭) — build_body에서 결정."""
    groups = group_by_approach(by_language)
    nums = sorted(groups)
    lines = [f"## {heading_num}. {heading_text}", ""]
    for i, num in enumerate(nums):
        if i > 0:
            lines.extend(["---", ""])
        label = approach_label(num, len(nums))
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

    # 회고/참고는 기본 스캐폴드에 넣지 않음 — 실제로 쓸 내용이 있을 때만 사람이
    # "## 회고"/"## 참고" 헤딩을 직접 추가. 빈 헤딩을 미리 깔면 대부분 그대로 방치되는
    # 보일러플레이트가 됨.

    # 복잡도(Big-O) 섹션은 SQL 전용 포스트에서 통째로 뺌 — 이 문제 성격에 안 맞는
    # 형식이라. publish.py의 완료 판정도 같은 SQL_ONLY_LANGUAGES 조건으로 이 섹션
    # 부재를 예외 처리해야 함.
    is_sql_only = set(by_language) == SQL_ONLY_LANGUAGES

    # 구분선 소유권 규칙은 모듈 docstring 참고(여기서 반복 안 함).
    trailing_sections = [IDEA_HEADING]
    if not is_sql_only:
        trailing_sections.append(build_complexity_section(by_language))
    code_heading_num = 2 if is_sql_only else 3
    code_heading_text = "쿼리" if is_sql_only else "코드"
    trailing_sections.append(
        build_code_section(
            folder_path,
            by_language,
            heading_num=code_heading_num,
            heading_text=code_heading_text,
        )
    )
    # 맨 끝에도 "---"를 하나 더 둠 — 이건 어느 섹션에도 안 딸린, 문서 끝을 표시하는
    # 독립적인 구분선이라 회고/참고를 지워도 영향 안 받음(항상 마지막에 남음).
    return "\n\n".join(
        [preamble] + [f"---\n\n{s}" for s in trailing_sections] + ["---"]
    )


def generate_one(folder_path, existing_slugs=None):
    """PS 레포 문제 폴더 하나를 스캐폴드 파일로 생성. 실제로 쓴 파일의 절대경로를 반환.
    같은 slug의 드래프트/포스트가 이미 있으면 거부(사람이 채운 프로즈 보호 + 발행분 중복
    방지) — 덮어쓰기 옵션은 없고, 다시 만들려면 기존 파일을 지우고 돌린다. 배치는
    스캔해 둔 existing_slugs를 넘겨 재스캔을 피한다.
    실패하면 예외를 그대로 던짐(호출자가 단일 모드인지 배치 모드인지에 따라 다르게 처리)."""
    date, prefix, number = parse_folder(folder_path)
    check_cutoff(date)
    if is_fail_folder(folder_path):
        raise ValueError(f"`_fail` 폴더는 대상이 아님(실패한 풀이): {folder_path}")
    platform = get_platform(prefix)
    if prefix == "cofo":
        # PS 레포 폴더명 케이스가 들쭉날쭉함(cofo_2148a vs cofo_2148A) — Codeforces
        # 공식 표기(contestId+Index)는 Index가 대문자라 title/filename/slug 전부
        # 대문자로 통일. get_title_url_codeforces(problem_lookup.py)는 이미
        # index.upper()로 API를 매칭하니 입력 케이스가 뭐든 상관없이 안전.
        number = number.upper()
    slug = build_slug(platform, number)
    if slug in (collect_existing_slugs() if existing_slugs is None else existing_slugs):
        raise FileExistsError(
            f"이미 같은 slug({slug})의 포스트/드래프트가 있음 — 덮어쓰지 않음. "
            "다시 만들려면 기존 파일을 지운 뒤 실행할 것."
        )
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
    if os.path.exists(target_path):
        raise FileExistsError(f"이미 파일이 있음(덮어쓰지 않음): {target_path}")

    os.makedirs(platform_dir, exist_ok=True)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(front_matter)
        f.write("\n\n")
        f.write(body)
        f.write("\n")

    return target_path


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
                # front matter 블록 안에서만 찾음 — 본문(회고 등)에 우연히 "slug: ..."로
                # 시작하는 줄이 있어도(인용/예시) 안 낚이게.
                try:
                    slug = yaml_scalar_value(front_matter_block(text), "slug")
                except ValueError:
                    continue
                if slug:
                    slugs.add(slug)
    return slugs


def run_batch():
    """PS_REPO 전체를 스캔해서, 대상 시작일(SCOPE_START_DATE) 이후 존재하는 풀이 중
    아직 이 블로그에 포스트/드래프트가 없는 것 전부를 스캐폴드로 생성. 개별 폴더의 실패는
    그 폴더만 에러로 보고하고 나머지는 계속 진행(단일 모드처럼 즉시 죽지 않음 — 배치라서
    한 문제 때문에 전체가 막히면 안 됨). 이미 있는 파일은 절대 덮어쓰지 않음.

    같은 (플랫폼, 번호)가 서로 다른 day 폴더에 중복으로 존재하는 경우가 많음(같은 문제를
    다른 날 다시 푼 것). **가장 최근 날짜 폴더를 채택**하고 나머지는 제외한다
    (최신 풀이가 더 낫다는 전제).
    어느 폴더를 골랐는지는 "중복" 줄로 보고. 이미 같은 slug의 드래프트/포스트가 있으면 그게
    덮어쓰이지 않는다(위 existing_slugs 스킵이 먼저) — 즉 더 오래된 풀이로 이미 만든
    포스트를 최신 폴더로 갈아끼우진 않음(그건 `sync`의 몫)."""
    folders = discover_problem_folders(PS_REPO)
    existing_slugs = collect_existing_slugs()

    # 1차: 컷오프 통과 + 지원 플랫폼 + 아직 없는 슬러그인 후보만 슬러그별로 묶음.
    candidates_by_slug = {}
    skipped_existing, skipped_unsupported, skipped_fail = [], [], []
    for folder_path in folders:
        date, prefix, number = parse_folder(folder_path)
        if date < SCOPE_START_DATE:
            continue
        if is_fail_folder(folder_path):
            skipped_fail.append(folder_path)
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

    created, errors, duplicates = [], [], []
    for slug, folder_paths in candidates_by_slug.items():
        chosen = max(folder_paths, key=lambda fp: parse_folder(fp)[0])
        if len(folder_paths) > 1:
            duplicates.append(
                (slug, chosen, [fp for fp in folder_paths if fp != chosen])
            )
        try:
            created.append(generate_one(chosen, existing_slugs))
        except Exception as e:
            errors.append((chosen, str(e)))

    for path in created:
        print(f"생성함: {path}")
    for folder_path, msg in errors:
        print(f"에러({folder_path}): {msg}")
    for slug, chosen, dropped in duplicates:
        print(
            f"중복(slug={slug}): 가장 최근 폴더 채택 — {chosen} "
            f"(제외: {', '.join(dropped)})"
        )
    print(
        f"--- 총 {len(created)}개 생성, {len(skipped_existing)}개는 이미 있어서 스킵, "
        f"{len(skipped_unsupported)}개는 미지원 플랫폼(SWEA)이라 스킵, "
        f"{len(skipped_fail)}개는 `_fail` 폴더라 스킵, "
        f"{len(duplicates)}개는 같은 문제 중복이라 최근 폴더만 채택, {len(errors)}개 에러 ---"
    )


def main():
    argv = sys.argv[1:]
    if not argv:
        run_batch()
        return

    if len(argv) != 1:
        print(__doc__)
        sys.exit(1)

    print(generate_one(argv[0]))


if __name__ == "__main__":
    main()
