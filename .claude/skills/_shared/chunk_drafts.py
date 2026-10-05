"""
review-code/review-post가 처리할 포스트 목록을 찾아서 청크(서브에이전트 배정
단위)로 나눈다. 순수 결정론적 — LLM 판단 없음. 실제 리뷰는 이 스크립트가 출력한
청크를 받아 각 스킬의 서브에이전트가 수행한다.

사용법:
    python3 chunk_drafts.py [경로 ...]
        경로를 안 주면 _drafts/{platform}/ 전체(전체 배치), 하나 이상 주면 그
        포스트들만(사용자가 지목했을 때). 경로는 `_drafts|_posts/{platform}/*.md`
        (platform ∈ PLATFORM_DIRS)여야 하고, 없는 파일이나 범위 밖 경로가 섞여
        있으면 즉시 에러(종료 코드 1).

출력: "CHUNK N:" 헤더 아래 그 청크의 절대경로들, 마지막에 총계 한 줄.

청크 크기: 포스트 최대 4개 / 총 약 1200줄 중 먼저 도달하는 조건에서 끊는 그리디
패킹. 개수 상한은 한 번에 너무 많이 보면 뒤로 갈수록 대충 보는 경향 때문, 줄수
상한은 긴 포스트 하나가 낀 청크만 유독 무거워지는 걸 막기 위함이다. 숫자는
근거 있는 절대치가 아니라 보수적 시작값. 한 포스트는 쪼개지 않는다(여러
서브에이전트가 나눠 보면 맥락이 끊김).

`review-code`·`review-post`가 공유한다.
"""

import os
import sys

from blog_common import DRAFTS_DIR, PLATFORM_DIRS, POSTS_DIR, list_platform_posts

MAX_DRAFTS_PER_CHUNK = 4
MAX_LINES_PER_CHUNK = 1200


def in_scope(path):
    """`_drafts|_posts/{platform}/` 바로 아래의 .md인지."""
    parent = os.path.dirname(path)
    return (
        path.endswith(".md")
        and os.path.basename(parent) in PLATFORM_DIRS
        and os.path.dirname(parent) in (DRAFTS_DIR, POSTS_DIR)
    )


def discover_all_drafts(explicit_paths=None):
    """explicit_paths가 없으면 `_drafts/{platform}/*.md` 전체, 있으면 그 경로들을
    검증해 절대경로로 반환. 없는 파일이나 범위 밖 경로가 있으면 예외."""
    if not explicit_paths:
        return list_platform_posts(DRAFTS_DIR)

    # 서브에이전트로 그대로 넘어갈 경로라 cwd와 무관하게 절대경로로 정규화.
    abs_paths = [os.path.abspath(p) for p in explicit_paths]
    missing = [p for p in abs_paths if not os.path.isfile(p)]
    if missing:
        raise FileNotFoundError(f"파일을 찾을 수 없음: {', '.join(missing)}")
    outside = [p for p in abs_paths if not in_scope(p)]
    if outside:
        raise ValueError(
            "_drafts|_posts/{platform}/ 아래 .md가 아님(PS 포스트 범위 밖): "
            + ", ".join(outside)
        )
    return abs_paths


def chunk_by_size(paths, max_count=MAX_DRAFTS_PER_CHUNK, max_lines=MAX_LINES_PER_CHUNK):
    """경로들을 순서대로 그리디하게 묶어 청크(경로 리스트)들의 리스트로. 개수가
    max_count에 닿거나 누적 줄수가 max_lines를 넘기 직전에 새 청크를 시작한다.
    파일 하나가 단독으로 max_lines를 넘으면 그 자체로 단독 청크가 된다."""
    chunks = []
    current, current_lines = [], 0
    for path in paths:
        with open(path, encoding="utf-8") as f:
            n_lines = sum(1 for _ in f)
        if current and (
            len(current) >= max_count or current_lines + n_lines > max_lines
        ):
            chunks.append(current)
            current, current_lines = [], 0
        current.append(path)
        current_lines += n_lines
    if current:
        chunks.append(current)
    return chunks


def main():
    try:
        paths = discover_all_drafts(sys.argv[1:] or None)
    except (FileNotFoundError, ValueError) as e:
        print(f"에러: {e}", file=sys.stderr)
        sys.exit(1)
    chunks = chunk_by_size(paths)

    for i, chunk in enumerate(chunks, 1):
        print(f"CHUNK {i}:")
        for path in chunk:
            print(f"  {path}")
    print(f"--- 총 {len(paths)}개 포스트, {len(chunks)}개 청크로 분할 ---")


if __name__ == "__main__":
    main()
