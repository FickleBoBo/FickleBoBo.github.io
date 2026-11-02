"""
포스트의 기계적 규칙 위반을 잡는 결정적 린터의 명령줄 진입점(규칙은 `lint/` 패키지).

사용법:
    python3 lint_post.py <포스트.md> [<포스트.md> ...]
    python3 lint_post.py --all            # _drafts/·_posts/의 {platform} 폴더 전체(PS 포스트만)

출력: 이슈마다 `경로:줄: [규칙] 설명`. 종료 코드: 0 이슈 없음, 1 이슈 있음, 2 파일을 못 읽음.
"""

import sys

from lint import lint
from repo import DRAFTS_DIR, POSTS_DIR, list_platform_posts


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(2)
    paths = (
        list_platform_posts(DRAFTS_DIR) + list_platform_posts(POSTS_DIR)
        if args == ["--all"]
        else args
    )

    total = unreadable = 0
    for path in paths:
        try:
            found = sorted(lint(path))
        except (
            OSError,
            ValueError,
        ) as e:  # ValueError: 인코딩 오류, tags.yaml 파싱 오류
            print(f"{path}: 읽기 실패({getattr(e, 'strerror', None) or e})")
            unreadable += 1
            continue
        for no, rule, msg in found:
            print(f"{path}:{no}: [{rule}] {msg}")
            total += 1
    print(f"-- {len(paths)}개 파일, 이슈 {total}건", file=sys.stderr)
    sys.exit(2 if unreadable else 1 if total else 0)


if __name__ == "__main__":
    main()
