# BoBo World

[![Build and Deploy](https://github.com/FickleBoBo/FickleBoBo.github.io/actions/workflows/pages-deploy.yml/badge.svg)][deploy]&nbsp;
[![GitHub license](https://img.shields.io/github/license/FickleBoBo/FickleBoBo.github.io.svg?color=blue)][mit]

> Back to Basics

개인 블로그 [ficklebobo.dev][site]의 소스 저장소. [Chirpy][chirpy] Jekyll 테마 기반이며, 알고리즘 문제 풀이(PS)를 비롯한 개발 기록을 담는다.

## PS 자동화 파이프라인

`.claude/skills/`에 별도 PS 레포의 문제 풀이를 이 블로그 포스트로 옮기는 자동화 스킬 5종을 구현해뒀다 — 문제 풀이 폴더를 스캔해 포스트 스캐폴드를 생성하고(`ps`), 원본 코드 변경을 재동기화하고(`sync`), 코드/포스트 완성도를 각각 리뷰하고(`review-code`/`review-post`), 완료된 포스트를 발행(`publish`)까지 자동 처리한다.

| 스킬          | 역할                                                                         |
| ------------- | ---------------------------------------------------------------------------- |
| `ps`          | PS 레포 문제 풀이 폴더 → 포스트 스캐폴드(파일명/front matter/코드 섹션) 생성 |
| `sync`        | PS 레포 코드 변경사항을 기존 포스트 코드 블록에 재동기화                     |
| `review-code` | 포스트에 임베드된 코드를 정확성·최선접근·컨벤션 기준으로 리뷰                |
| `review-post` | 포스트 완성도(설명·복잡도·컨벤션)를 리뷰하고 빈 필드를 채움                  |
| `publish`     | 완료된 드래프트를 발행하고 블로그/PS 레포 양쪽에 커밋                        |

## License

This work is published under [MIT][mit] License.

[site]: https://ficklebobo.dev
[chirpy]: https://github.com/cotes2020/jekyll-theme-chirpy/
[mit]: https://github.com/FickleBoBo/FickleBoBo.github.io/blob/main/LICENSE
[deploy]: https://github.com/FickleBoBo/FickleBoBo.github.io/actions/workflows/pages-deploy.yml
