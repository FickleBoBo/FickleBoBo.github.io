"""
`scaffold_post.py YYYY-MM-DD` — PS 레포 한 날짜의 풀이를 포스트 스캐폴드로 만든다(구조는 SKILL.md).

- 본문의 `---`는 뒤 섹션이 자기 앞에 단다(`## 3. 회고` 같은 선택 섹션을 지울 때
  구분선이 같이 지워지도록). 문서 끝의 `---`만 어느 섹션에도 안 딸린다.
- 코드펜스엔 Kramdown IAL을 붙이지 않는다(Prettier가 fence와 IAL 사이에 빈 줄을 끼움).
  IAL은 `prompt-info` 인용문에만 있고 `<!-- prettier-ignore -->`로 보호한다.
"""

import os
import sys

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "_shared"))
)
from clean_code import clean_code
from judge import title_and_url
from post_text import front_matter_block, yaml_dq, yaml_scalar_value
from problem_post import CODE_HEADING, IDEA_HEADING, QUERY_HEADING
from ps_source import (
    FENCE_OF_LANGUAGE,
    LANGUAGE_DISPLAY_ORDER,
    find_source_files,
    group_by_approach,
    is_sql_only,
)
from repo import DRAFTS_DIR, PLATFORM_MAP, POSTS_DIR, PS_REPO, sanitize_filename

BLOG_START_DATE = "2026-08-17"


def parse_folder_name(folder_path):
    """문제 폴더 -> (접두사, 플랫폼명, 번호, slug). 대상 저지가 아니면 ValueError."""
    name = os.path.basename(folder_path)
    if name.lower().endswith("_fail"):
        raise ValueError("실패한 풀이(_fail)")
    prefix, number = name.split("_", 1)
    prefix = prefix.lower()
    if prefix not in PLATFORM_MAP:
        raise ValueError(f"대상 저지 아님(접두사 {prefix})")
    platform = PLATFORM_MAP[prefix]
    if prefix == "cofo":
        number = number.upper()  # 폴더명 케이스가 섞여 있어도 Index는 대문자
    return prefix, platform, number, f"{platform}-{number}".lower()


def build_front_matter(date, platform, number, slug, title, languages):
    brackets = "".join(f"[{lang}]" for lang in languages)
    return "\n".join(
        [
            "---",
            f'title: "{yaml_dq(f"[{platform}] #{number} - {title} {brackets}")}"',
            f"date: {date}",
            f"categories: [PS, {platform}]",
            "tags: []",
            f"slug: {slug}",
            f"media_subpath: /assets/img/posts/{slug}/",
            "math: true",
            "---",
        ]
    )


def approach_label(num, total):
    """접근이 하나면 '풀이', 둘 이상이면 첫 접근도 '풀이 1'."""
    return "풀이" if total <= 1 and num == 1 else f"풀이 {num}"


def build_code_section(folder_path, by_language):
    groups = group_by_approach(by_language)
    heading = QUERY_HEADING if is_sql_only(by_language) else CODE_HEADING
    lines = [heading, ""]
    for i, num in enumerate(sorted(groups)):
        if i > 0:
            lines.extend(["---", ""])
        langs = [lang for lang in LANGUAGE_DISPLAY_ORDER if lang in groups[num]]
        brackets = "".join(f"[{lang}]" for lang in langs)
        lines.extend([f"### {approach_label(num, len(groups))} {brackets}", ""])
        for lang in langs:
            fname = groups[num][lang]
            with open(os.path.join(folder_path, fname), encoding="utf-8") as f:
                code = clean_code(f.read(), lang, fname).rstrip("\n")
            lines.extend([f"```{FENCE_OF_LANGUAGE[lang]}", code, "```", ""])
    return "\n".join(lines).rstrip("\n")


def build_body(problem_url, folder_path, by_language):
    preamble = (
        f"<!-- prettier-ignore -->\n> [문제 링크]({problem_url})\n{{: .prompt-info }}"
    )
    sections = [IDEA_HEADING, build_code_section(folder_path, by_language)]
    return "\n\n".join([preamble] + [f"---\n\n{s}" for s in sections] + ["---"])


def collect_existing_slugs():
    """`_drafts/`·`_posts/` 포스트의 front matter `slug` 전부."""
    slugs = set()
    for base in (DRAFTS_DIR, POSTS_DIR):
        for dirpath, _, filenames in os.walk(base):
            for fname in filenames:
                if fname.endswith(".md"):
                    with open(os.path.join(dirpath, fname), encoding="utf-8") as f:
                        try:
                            slug = yaml_scalar_value(
                                front_matter_block(f.read()), "slug"
                            )
                        except ValueError:  # front matter 없는 .md는 포스트가 아니다
                            continue
                    if slug:
                        slugs.add(slug)
    return slugs


def write_post(date, folder_path, prefix, platform, number, slug):
    by_language = find_source_files(folder_path)
    languages = [lang for lang in LANGUAGE_DISPLAY_ORDER if lang in by_language]
    title, problem_url = title_and_url(prefix, number)

    platform_dir = os.path.join(DRAFTS_DIR, platform.lower())
    os.makedirs(platform_dir, exist_ok=True)
    path = os.path.join(
        platform_dir, f"{date}-{platform} {number} {sanitize_filename(title)}.md"
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(build_front_matter(date, platform, number, slug, title, languages))
        f.write("\n\n" + build_body(problem_url, folder_path, by_language) + "\n")
    return path


def scaffold_day(date):
    if date < BLOG_START_DATE:
        sys.exit(f"블로그 개설일({BLOG_START_DATE}) 이전 날짜: {date}")
    day_dir = os.path.join(PS_REPO, date[:7], "src", f"day_{date[8:]}")
    if not os.path.isdir(day_dir):
        sys.exit(f"PS 레포에 해당 날짜 폴더가 없음: {day_dir}")

    folder_names = sorted(
        n for n in os.listdir(day_dir) if os.path.isdir(os.path.join(day_dir, n))
    )

    existing_slugs = collect_existing_slugs()
    created = skipped = errors = 0
    for name in folder_names:
        folder_path = os.path.join(day_dir, name)
        try:
            prefix, platform, number, slug = parse_folder_name(folder_path)
            if slug in existing_slugs:
                print(f"스킵(이미 있음): {name} — slug={slug}")
                skipped += 1
                continue
            path = write_post(date, folder_path, prefix, platform, number, slug)
            print(f"생성함: {path}")
            created += 1
        except Exception as e:
            print(f"에러({name}): {type(e).__name__}: {e}")
            errors += 1
    print(f"--- {created}개 생성, {skipped}개 스킵, {errors}개 에러 ---")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("사용법: scaffold_post.py YYYY-MM-DD")
    scaffold_day(sys.argv[1])
