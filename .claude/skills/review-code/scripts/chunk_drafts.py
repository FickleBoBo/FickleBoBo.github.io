#!/usr/bin/env python3
"""
review-code/review-post가 처리할 드래프트 목록을 찾아서 청크(서브에이전트 배정
단위)로 나눈다. 순수 결정론적 — discovery/필터링/그룹핑엔 LLM 판단이 전혀 없음.
실제 리뷰(코드 정확성 판단, 프로즈 품질 평가 등)는 이 스크립트가 출력한 청크를
받아 review-code/review-post 스킬(서브에이전트)이 수행함 — 이 파일은 그 앞단계만.

**청크 크기 기준: 드래프트 최대 4개 / 총 줄수 약 1200줄 중 먼저 도달하는
조건에서 그룹을 끊는 그리디 패킹. 개수 상한은 LLM이 한 번에 너무 많은 항목을
보면 뒤로 갈수록 대충 보는 경향 때문, 줄수 상한은 긴 드래프트 하나가 낀 그룹만
유독 무거워지는 걸 막기 위함. 숫자는 근거 있는 절대치가 아니라 보수적 시작값.
`--mode code`/`--mode post`는 지금은 동작이 동일(둘 다 필터 없이 전체 대상) —
review-post가 예전엔 '2. 접근' 비어있는 드래프트를 스킵했었는데, 이제 비어있으면
review-post가 직접 채우는 게 정상 동작이라 필터 자체를 없앰. 모드 구분은 향후
다시 갈릴 가능성을 열어두려고 인터페이스만 유지.**

코드를 고칠 때 알아야 할 것:
- `resolve_filename.py`(`ps`)의 `PLATFORM_MAP`/`DRAFTS_DIR`를 그대로
  import해서 씀 — 드래프트 스캔 범위가 다른 스킬과 갈라지면 안 되기 때문.
- 이 스크립트는 review-code 스킬 소유지만 review-post도 `--mode post`로 그대로
  가져다 씀(파일 복제 안 함) — sync가 ps의 스크립트를, publish가 sync/ps의
  스크립트를 그대로 가져다 쓰는 것과 같은 패턴.

사용법:
    python3 chunk_drafts.py --mode code [경로 ...]
    python3 chunk_drafts.py --mode post [경로 ...]
        경로를 안 주면 _drafts/{platform}/ 전체가 대상(전체 배치), 하나 이상 주면
        그 드래프트들만 대상(사용자가 특정 포스트를 지목했을 때 — 존재하지 않는
        경로가 섞여 있으면 즉시 에러). 두 모드 다 필터 없이 그대로 청크로 나눔.

출력: "CHUNK N:" 헤더 아래 그 청크에 속한 드래프트 절대경로들, 마지막에 총계 한 줄.
"""

import os
import sys

_SKILLS_DIR = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path.insert(0, os.path.abspath(os.path.join(_SKILLS_DIR, "ps", "scripts")))

from resolve_filename import DRAFTS_DIR, PLATFORM_MAP

MAX_DRAFTS_PER_CHUNK = 4
MAX_LINES_PER_CHUNK = 1200


def discover_all_drafts(explicit_paths=None):
    """explicit_paths가 없으면 _drafts/{platform}/*.md(platform ∈ PLATFORM_MAP)
    전체를 절대경로 리스트로 반환(전체 배치). 있으면 그 경로들을 존재 검증만 하고
    그대로 반환(사용자가 지목한 특정 드래프트만 대상으로 하는 모드) — 존재하지
    않는 경로가 하나라도 있으면 즉시 예외."""
    if explicit_paths:
        # 절대경로로 정규화 — 서브에이전트로 그대로 넘어갈 경로라 cwd가 달라져도
        # 안전하게 하려는 목적.
        abs_paths = [os.path.abspath(p) for p in explicit_paths]
        missing = [p for p in abs_paths if not os.path.isfile(p)]
        if missing:
            raise FileNotFoundError(f"파일을 찾을 수 없음: {', '.join(missing)}")
        return abs_paths

    paths = []
    for platform_dir in sorted({v.lower() for v in PLATFORM_MAP.values()}):
        dir_path = os.path.join(DRAFTS_DIR, platform_dir)
        if not os.path.isdir(dir_path):
            continue
        for fname in sorted(os.listdir(dir_path)):
            if fname.endswith(".md"):
                paths.append(os.path.join(dir_path, fname))
    return paths


def chunk_by_size(paths, max_count=MAX_DRAFTS_PER_CHUNK, max_lines=MAX_LINES_PER_CHUNK):
    """드래프트 경로들을 순서대로 그리디하게 묶어서 청크(경로 리스트)들의 리스트로.
    누적 줄수가 max_lines를 넘기기 직전, 또는 개수가 max_count에 도달하면 새 청크를
    시작. 파일 하나가 단독으로 max_lines를 넘어도 그 자체로 단독 청크가 됨(더
    잘게 쪼개지 않음 — 한 드래프트를 여러 서브에이전트가 나눠 보는 건 오히려
    맥락이 끊겨서 안 함)."""
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
    if (
        len(sys.argv) < 3
        or sys.argv[1] != "--mode"
        or sys.argv[2] not in ("code", "post")
    ):
        print(__doc__)
        sys.exit(1)
    explicit_paths = sys.argv[3:] or None

    paths = discover_all_drafts(explicit_paths)
    chunks = chunk_by_size(paths)

    for i, chunk in enumerate(chunks, 1):
        print(f"CHUNK {i}:")
        for path in chunk:
            print(f"  {path}")
    print(f"--- 총 {len(paths)}개 드래프트, {len(chunks)}개 청크로 분할 ---")


if __name__ == "__main__":
    main()
