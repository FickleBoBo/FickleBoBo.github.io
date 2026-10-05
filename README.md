# BoBo World

[![Build and Deploy](https://github.com/FickleBoBo/FickleBoBo.github.io/actions/workflows/pages-deploy.yml/badge.svg)][deploy]&nbsp;
[![GitHub license](https://img.shields.io/github/license/FickleBoBo/FickleBoBo.github.io.svg?color=blue)][mit]

> Back to Basics

개인 블로그 [ficklebobo.dev][site]의 소스 저장소. [Chirpy][chirpy] Jekyll 테마 기반이며, 알고리즘 문제 풀이(PS)를 비롯한 개발 기록을 담는다. 문제 풀이 원본 코드는 별도 저장소 [PS][ps]에 있고, 이 블로그의 PS 포스트는 그 코드를 옮겨 와 설명을 붙인 것이다.

## 구성

- **PS**: Programmers, LeetCode, Codeforces, BaekJoon 문제 풀이. 아이디어, 복잡도, 언어별 코드(Java, C++, Python)로 이루어진 고정 구조다.
- **Contest**: Codeforces 대회 후기. 성적·순위·레이팅 변동과 문제별 풀이를 담는다.

## PS 자동화 파이프라인

`.claude/skills/`에 PS 레포의 풀이를 블로그 포스트로 옮기는 [Claude Code][claude-code] 스킬을 두었다. 반복 작업(파일명 결정, front matter, 코드 블록 동기화, 커밋)은 스크립트가 맡고, 판단이 필요한 부분(아이디어·복잡도 초안, 코드 리뷰, 태그 후보)만 LLM이 맡는다.

```text
ps → sync → review-code → (태그 확정) → sync → review-post → publish
```

| 스킬          | 역할                                                                                    |
| ------------- | --------------------------------------------------------------------------------------- |
| `ps`          | PS 레포 풀이 폴더 → 포스트 스캐폴드(파일명, front matter, 코드 섹션) 생성               |
| `sync`        | PS 레포 코드 변경을 포스트 코드 블록에 재동기화. `--posts`로 발행본 전체도 점검         |
| `review-code` | 포스트에 임베드된 코드를 정확성·최선 접근 기준으로 리뷰하고 태그 후보 제안              |
| `review-post` | 포스트 완성도(설명·복잡도·컨벤션)를 리뷰하고 빈 필드를 채움. 기계 검증은 `lint_post.py` |
| `publish`     | 완료 게이트를 통과한 드래프트 하나를 `_posts/`로 옮기고 블로그·PS 레포 양쪽에 커밋      |
| `contest`     | 대회 후기(별도 장르)의 스캐폴드 생성과 발행. 위 파이프라인 밖에서 동작                  |

스킬이 공유하는 경로 상수·front matter 파서·커밋 헬퍼·문제 원문 조회·청크 분할은 `.claude/skills/_shared/`에 있다. 포스트 문체와 표기 규칙의 정본은 [`STYLE.md`](.claude/skills/review-post/STYLE.md), 태그 어휘의 정본은 [`tags.yaml`](.claude/skills/review-code/tags.yaml)이다. 각 스킬의 동작은 해당 `SKILL.md`에 자기완결적으로 적혀 있다.

## 저장소 구조

```text
_posts/          발행된 포스트 (programmers, leetcode, codeforces, baekjoon, contest)
_drafts/         작성 중인 포스트
_tabs/           About, Archives, Categories, Tags 페이지
.claude/skills/  PS 자동화 스킬과 스크립트
.claude/agents/  리뷰 서브에이전트 정의 (code-reviewer, post-reviewer)
CLAUDE.md        Claude Code 작업 지침 (워크플로우, 커밋 규칙)
```

## 로컬 실행

```bash
bundle install
bundle exec jekyll serve -l          # http://127.0.0.1:4000
bundle exec jekyll serve -l --drafts # 초안 포함
```

## License

This work is published under [MIT][mit] License.

[site]: https://ficklebobo.dev
[ps]: https://github.com/FickleBoBo/PS
[chirpy]: https://github.com/cotes2020/jekyll-theme-chirpy/
[claude-code]: https://claude.com/claude-code
[mit]: https://github.com/FickleBoBo/FickleBoBo.github.io/blob/main/LICENSE
[deploy]: https://github.com/FickleBoBo/FickleBoBo.github.io/actions/workflows/pages-deploy.yml
