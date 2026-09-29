---
name: contest
description: Codeforces 대회 후기 포스트 장르(`Contest` 카테고리)를 다루는 스킬. `scaffold_contest.py`는 대회 ID/URL로 CF API를 조회해 후기 스켈레톤(파일명 + front matter + 대회 개요·결과·풀이 과정 표)을 결정론적으로 생성하고, `publish_contest.py`는 완성된 후기를 `_posts/contest/`로 옮겨 블로그·PS 레포에 커밋한다. "이번 대회 후기 스켈레톤 만들어줘", "대회 후기 발행해줘", "contest 스킬 돌려줘" 같은 요청에 사용. LLM 판단 없이 스크립트가 CF API 조회·페널티 계산·파일 스캔·git 커밋만 함.
---

# contest — 대회 후기 포스트 생성·발행

**스코프**: 스켈레톤 생성은 파일명 + front matter + `## 1. 대회 개요` + `## 2. 결과` + `## 3. 풀이 과정`의 스탯 표까지 완전 자동 — 문제별 서술·라이브 코드·총평·수동 뉘앙스(`미완 · 업솔빙` 등)는 사람이 채운다(`ps` 스킬과 평행 구조). 발행은 `_drafts/contest/` → `_posts/contest/` 이동 + 블로그·PS 레포 커밋까지.

**파이프라인 밖 장르.** `ps`/`sync`/`review-code`/`review-post`/`publish`는 전부 문제 포스트 구조(`## 1. 아이디어` + `## 2. 복잡도`)를 전제한다 — 후기엔 안 맞는다. `_drafts/contest/`는 `publish.py`/`sync_code.py`의 `PLATFORM_MAP`(programmers/leetcode/codeforces)에 없어서 두 스킬이 통째로 무시한다(의도된 안전장치). 발행은 이 스킬의 `publish_contest.py`가 담당(아래 "발행").

스크립트 3개:

- `scaffold_contest.py` — CF API에서 후기 스켈레톤 + 프리뷰 카드 생성 (아래 "스캐폴드 생성")
- `render_card.py` — 프리뷰 카드(PNG) 렌더러. 데이터를 받아 HTML → 헤드리스 Chrome 스크린샷. 스캐폴드가 호출하는 헬퍼(직접 실행은 디버그용). 디자인 '양식'과 미래 변수 대응(Y축 동적 범위·점 개수·레이팅 하락·unrated 등)의 '왜'는 이 파일 docstring
- `publish_contest.py` — 완성된 후기를 `_posts/contest/`로 옮기고 두 레포에 커밋 (아래 "발행")

양식·규칙의 설계 근거 전체(순위/레이팅 소스 불일치, 등급 색 실측, CF API 함정, 나중으로 미룬 것들)는 프로젝트 메모리 `contest-recap-post-format.md`. 스켈레톤 '구조'를 바꿀 때 알아야 할 '왜'(구분선 소유권, 페널티 계산 규칙 등)는 `scripts/scaffold_contest.py` docstring. 여기 SKILL.md는 사용법 + 무엇이 채워지는지만.

## 스캐폴드 생성

```
python3 <이 스킬의 base directory>/scripts/scaffold_contest.py <대회 ID 또는 URL> [--force | --card-only]
```

예:

```
python3 .claude/skills/contest/scripts/scaffold_contest.py 2259
python3 .claude/skills/contest/scripts/scaffold_contest.py https://codeforces.com/contest/2259
```

- 배치 모드 없음 — 대회는 한 번에 하나씩, 대회 끝나고 실행한다.
- 핸들은 스크립트 상수(`HANDLE = "FickleBoBo"`). 인자로 안 받는다.
- `_drafts/contest/{파일명}`이 이미 있으면 거부(사람이 채운 서술·라이브 코드 보호). 재생성은 `--force`.
- `assets/img/posts/{slug}/` 폴더도 같이 만든다(레이팅 그래프 스크린샷 자리 — 매 후기 100% 쓰이므로). 여기에 **프리뷰 카드 `preview.png`**(2400×1260)도 렌더하고 front matter에 `image:`를 넣는다. 로컬 Chrome 필요(`CHROME_BIN`으로 경로 지정 가능) — 없으면 카드만 생략하고 나머지는 정상 진행(경고 출력).
- `--card-only`: 이미 있는 후기(`_drafts/contest`·`_posts/contest`, slug로 탐색)의 카드만 (재)생성하고 front matter에 `image:`가 없으면 넣는다. 서술·코드는 안 건드림. 과거 후기 소급·카드 디자인 변경 후 재생성용 — `--force`와 달리 덮어써도 안전.
- 성공 시 stdout엔 쓴 파일의 절대경로만. **stderr**엔 페널티·순위·레이팅 요약 + 그래프 저장 경로(눈 대조·안내용).
- 필수 인자(대회 ID/URL)가 없으면 평문으로 요청하고 기다린다 — `AskUserQuestion` 같은 선택지 UI로 후보를 골라주지 않는다(`ps`와 동일).

## CF API 조회 (contestId + 핸들, 전부 익명 GET)

브라우저 UA 불필요. 스크립트가 세 번 호출:

| 엔드포인트                                                                  | 쓰는 값                                                                                                   |
| --------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| `contest.standings?contestId={id}` (⚠ bare로만 — 파라미터 더 붙이면 FAILED) | `result.contest`(대회명·시작 시각·배정 시간·type), `result.problems`(index·name)                          |
| `contest.ratingChanges?contestId={id}`                                      | rated 순위, oldRating, newRating(핸들별). 배열 길이 = rated 참가자 수                                     |
| `contest.status?contestId={id}&handle={h}`                                  | 제출 전부: `problem.index`, `verdict`, `relativeTimeSeconds`, `passedTestCount`, `author.participantType` |

대회 직후 실행해 `ratingChanges`가 아직 비어 있으면 순위·레이팅 행을 placeholder(HTML 주석)로 남기고 crash하지 않는다 — 확정 후 사람이 그 행만 채우거나 `--force`로 재생성.

프리뷰 카드는 이 시점에 rated 성적 없이(순위 칩·델타 없음) 그려진다 — 확정 후 `--card-only`로 카드만 다시 만든다. 카드 데이터 조회(`user.rating`)·렌더가 실패해도 스켈레톤은 정상 생성되고(카드·`image:`만 빠짐, stderr 경고) 나중에 `--card-only`로 채운다.

## 무엇이 채워지는가

| 자리                           | 채워지는 방식                                                                                                                                                                                                                                                                                                              |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 파일명                         | `{대회 시작일 KST}-{CF 대회명 그대로}.md`. 금지 문자만 유니코드 치환(괄호·마침표는 그대로)                                                                                                                                                                                                                                 |
| front matter `title`           | `"{대회명 그대로} 후기"` — 브래킷 접두어·정규화 없음(Educational·Global 등 어떤 대회명이든 안 깨짐)                                                                                                                                                                                                                        |
| front matter `date`            | 대회 **시작일**(KST). 후기 쓰는 날 아님                                                                                                                                                                                                                                                                                    |
| front matter `categories`      | 항상 `[Contest]` — 평평한 최상위(PS 아래 아님, 플랫폼 2단 아님. 이유는 메모리)                                                                                                                                                                                                                                             |
| front matter `tags`            | `["codeforces"]` + 대회명이 정확히 `(Div. N)` 또는 `(Rated for Div. N)` 꼴이면 `"div N"` 추가. `(Div. 1 + Div. 2)` 통합 라운드·Global/Hello 등은 태그 없이 두고 사람이 추가                                                                                                                                                |
| front matter `slug`            | `codeforces-{contestId}` (개별 문제 포스트 `codeforces-{contestId}{index}`와 접두어로 묶임)                                                                                                                                                                                                                                |
| front matter `image`           | `path: preview.png`(media_subpath 기준) — Chirpy 프리뷰(og:image 겸용). `alt`는 일부러 안 넣음: Chirpy가 이미지 밑에 눈에 보이는 캡션으로 출력함. 카드는 대회명·날짜·solved·penalty·순위(rated만)·레이팅 이력 그래프(이 대회 이전 참가분 + 이번 대회, 델타 라벨)                                                           |
| `math` / `mermaid`             | `true` / `false` 고정                                                                                                                                                                                                                                                                                                      |
| 상단 prompt-info               | `> [대회 링크](https://codeforces.com/contest/{id})`                                                                                                                                                                                                                                                                       |
| `## 1. 대회 개요` 표           | 대회명 / 일시(KST) / 배정 시간 / 문제 수 / 참가 형태 — 전부 자동                                                                                                                                                                                                                                                           |
| `## 2. 결과` 표                | 푼 문제(대회 중 AC 범위 + 업솔빙) / 페널티(**계산값** — 아래) / 순위(`ratingChanges` 기준) / 레이팅(등급 색 span 포함). 표 밑에 `![레이팅 그래프](rating-graph.png)`                                                                                                                                                       |
| `## 3. 풀이 과정` 표           | 문제(CF 링크) / 결과(`AC`·`업솔빙`·`미해결`·`미시도`) / 제출 시각(`MM:SS`) / WA(페널티 카운트되는 오답 수). 전부 자동                                                                                                                                                                                                      |
| `### {index}. {name}` 서브섹션 | 문제 전부(A~). 빈 `c++` 펜스 + `> 풀이 → [[Codeforces] #… ](…)` 팁 링크. AC·업솔빙은 풀이 포스트 실재 여부와 무관하게 무조건 단다(어차피 나중에 만들 것이므로 — 발행 시점엔 아직 링크가 죽어 있을 수 있음). 미해결만 `_posts/codeforces/`에 그 포스트가 실재할 때만 예외적으로 단다. 미시도 문제는 `대회 중 미시도.` 한 줄 |
| `## 총평`                      | 헤딩만(내용은 사람이)                                                                                                                                                                                                                                                                                                      |

## 페널티 계산 (Div 3, ICPC 방식) — API에 없어서 스크립트가 계산

대회 중 **해결한** 문제마다 `floor(AC분) + 10 * (AC 이전 오답 중 passedTestCount >= 1 인 것)` 을 합산.

- ⚠ 샘플/1번 테스트도 못 넘긴 오답(`passedTestCount == 0`)·컴파일 에러는 **페널티 미포함**. `## 3` 표의 WA 열과 페널티가 이 규칙으로 일관된다.
- 순위·레이팅은 CF가 자기 페이지끼리도 다르다(`ratingChanges` API 기준으로 고정) → **발행 전 `/contest/{id}/standings` 페이지에서 눈으로 대조** (스크립트는 스탯만 넣고 경고 주석은 안 박음).

## 사람이 스켈레톤 생성 뒤 하는 일

1. 각 `### {index}` 서브섹션에 대회 중 흐름 서술 + 라이브/WIP 코드 붙여넣기(PS 레포에 있지만 `sync`가 contest 포스트를 안 본다 — 손으로). 컴파일 안 되는 미완 코드도 그대로.
2. 필요하면 `## 3` 표·결과 라벨의 수동 뉘앙스 조정(`업솔빙` → `미완 · 업솔빙` 등).
3. `## 총평` 작성.
4. 레이팅 그래프 이미지: Chrome DevTools → 그래프 노드 선택 → `Cmd+Shift+P` → "Capture node screenshot" → `assets/img/posts/{slug}/rating-graph.png`(폴더는 스캐폴드 단계에서 이미 만들어져 있음 — stderr에 경로 출력됨). 첫 대회는 점 1개라 가치 낮음(줄 지워도 됨).
5. 발행 전 `/contest/{id}/standings`에서 페널티·순위 눈 대조.
6. 발행: `publish_contest.py` 실행 (아래).

## 발행

```
python3 <이 스킬의 base directory>/scripts/publish_contest.py <후기 .md 경로 또는 대회 ID/URL>
```

`publish` 스킬(PS 포스트 발행)의 "옮긴 뒤 레포별로 각각 커밋" 흐름을 그대로 따른다:

1. `_drafts/contest/{파일}` → `_posts/contest/{파일}` 이동
2. **블로그 레포 커밋**: 포스트 + (있으면) `assets/img/posts/{slug}/` → `feat: [Contest] {CF API 대회명} 후기`
3. **PS 레포 커밋**: 그 대회의 `live_{contestId}*` 폴더 전부(대회날 `day_XX`에 문제별로 생김) → 같은 메시지
4. push 안 함 — 로컬 커밋까지만

- **완료 게이트 없음.** 이 스크립트를 콕 집어 실행 = 발행 준비됐다는 뜻(`publish`와 달리 `## 총평` 채워졌는지 등을 검사하지 않음 — 후기는 사람이 판단). 배치 모드도 없음.
- **`live_` 폴더를 하나도 못 찾으면** 아무것도 안 옮기고 에러(대회 ID 오타이거나 이미 수동 처리한 경우). PS 레포 검증을 블로그 레포 건드리기 전에 하는 건 `publish.py`와 같은 이유.
- 이미 커밋된 상태면 그 레포 커밋은 스킵("이미 커밋된 상태"로 보고, 에러 아님).
- 트레일러는 `Co-Authored-By: Claude <noreply@anthropic.com>`(모델명 없음) — `publish` 산출물과 동일, 정적 스크립트라 커밋 시점 모델 버전을 모름.

## 규칙

- PS 레포 소스 파일 내용은 건드리지 않는다(`scaffold`는 읽지도 않고, `publish_contest`는 `live_` 폴더를 커밋만 함 — 코드 정리 안 함).
- 결과 보고 시 판단을 얹지 않는다 — stderr 요약·stdout 경로를 "괜찮아 보인다" 없이 그대로 전달. 페널티·순위 대조는 사람 몫.
- 스킬 정의 변경 커밋: `<type>: [Claude Skill] contest - <요약>`, 트레일러 `Co-Authored-By: Claude {현재 모델명} <noreply@anthropic.com>` 한 줄만.
