---
name: contest
description: Codeforces 대회 후기 포스트 장르(`Contest` 카테고리)를 다루는 스킬. `scaffold_contest.py`는 대회 ID/URL로 CF API를 조회해 후기 스켈레톤(파일명 + front matter + 대회 개요·결과·풀이 과정 표)을 결정론적으로 생성하고, `publish_contest.py`는 완성된 후기를 `_posts/contest/`로 옮겨 블로그·PS 레포에 커밋한다. "이번 대회 후기 스켈레톤 만들어줘", "대회 후기 발행해줘", "contest 스킬 돌려줘" 같은 요청에 사용. LLM 판단 없이 스크립트가 CF API 조회·페널티 계산·파일 스캔·git 커밋만 함.
---

# contest — 대회 후기 포스트 생성·발행

스캐폴드는 파일명·front matter·`## 1. 대회 개요`·`## 2. 결과`·`## 3. 풀이 과정` 표·프리뷰 카드까지 자동이고, 문제별 서술·라이브 코드·총평·수동 뉘앙스(`미완 · 업솔빙` 등)는 사람이 채운다. 발행은 `_drafts/contest/` → `_posts/contest/` 이동 + 블로그·PS 레포 커밋까지.

**PS 파이프라인 밖 장르.** `ps`·`sync`·`review-*`·`publish`는 문제 포스트 구조(`## 1. 아이디어` + `## 2. 코드`)를 전제하는데 후기엔 안 맞는다. `_drafts/contest/`는 `repo.PLATFORM_DIRS`에 없어서 이 스킬들이 통째로 무시한다(의도된 안전장치).

스크립트(`scripts/`) — 진입점 2개 + 역할별 모듈:

- `scaffold_contest.py` — **진입점.** 후기 스켈레톤 + 프리뷰 카드 생성
- `publish_contest.py` — **진입점.** 완료 게이트 검사 후 `_posts/contest/`로 옮기고 두 레포에 커밋
- `cf_contest.py` — CF API 조회, 문제별 성적·페널티 계산(네트워크는 여기만). API 함정과 페널티 계산 규칙의 '왜'는 이 파일 docstring
- `recap_body.py` — front matter·본문 조립(순수 함수). 구분선 소유권·등급 색의 '왜'는 이 파일 docstring
- `render_card.py` — 프리뷰 카드(PNG) 렌더러(HTML → 헤드리스 Chrome). 디자인 양식의 '왜'는 이 파일 docstring
- `contest_common.py` — 경로 상수, slug로 후기 찾기(내부 모듈)

## 스캐폴드 생성

```
python3 ${CLAUDE_SKILL_DIR}/scripts/scaffold_contest.py <대회 ID 또는 URL> [--force | --card-only]
```

- 대회는 한 번에 하나씩, 대회 끝나고 실행한다. 대회 ID/URL이 없으면 평문으로 요청한다(선택지 UI 금지).
- 핸들은 `cf_contest.py`의 `HANDLE`이고 인자로 안 받는다.
- `_drafts/contest/{파일명}`이 이미 있으면 거부(사람이 채운 서술·라이브 코드 보호). 재생성은 `--force`.
- `assets/img/posts/{slug}/` 폴더도 같이 만든다(레이팅 그래프 스크린샷 자리). 여기에 프리뷰 카드 `preview.png`(2400×1260)를 렌더하고 front matter에 `image:`를 넣는다. 로컬 Chrome이 필요하고(`CHROME_BIN`으로 경로 지정 가능) 없거나 렌더가 실패하면 카드만 빠진다(stderr 경고).
- `--card-only`: 이미 있는 후기(`_drafts/contest`·`_posts/contest`, slug로 탐색)의 카드만 (재)생성하고 `image:`가 없으면 넣는다. 서술·코드는 안 건드려서 `--force`와 달리 덮어써도 안전하다. 순위·레이팅 확정 뒤 카드 갱신, 과거 후기 소급, 디자인 변경 후 재생성에 쓴다.
- 대회 직후 `ratingChanges`가 비어 있으면 순위·레이팅 행을 placeholder(HTML 주석)로 남기고 `description`에서도 뺀다. 확정 후 그 행과 `description`만 채우거나 `--force`로 재생성하고, 카드는 `--card-only`로 다시 만든다.
- 성공하면 stdout엔 쓴 파일의 절대경로만. stderr엔 페널티·순위·레이팅 요약과 그래프 저장 경로(눈 대조용).

## 채워지는 것 (양식 정본은 `recap_body.py`)

- 파일명 `{대회 시작일 KST}-{CF 대회명 그대로}.md`, `title` `"{대회명} 후기"`, `date` 대회 시작일(KST), `categories` `[Contest]`, `slug` `codeforces-{contestId}`.
- `tags`: `["codeforces"]` + 대회명이 정확히 `(Div. N)`·`(Rated for Div. N)` 꼴이면 `"div N"`. 통합 라운드(`Div. 1 + Div. 2`)·Global 등은 사람이 추가.
- `description`: `대회 중 {푼 수}/{문제 수}문제 해결 · {순위}위 · 레이팅 {이전} → {이후} ({변동})`. 검색·공유용 요약이자 Chirpy가 제목 밑에 보여 주는 부제다(없으면 `<meta description>`이 본문 첫 줄 "대회 링크"가 된다). 순위·레이팅이 미확정이면 앞부분만 들어가니, 확정 뒤 `## 2. 결과`를 채울 때 같이 맞춘다.
- 본문: `## 1. 대회 개요` 표, `## 2. 결과` 표(푼 문제·페널티·순위·레이팅)와 `rating-graph.png` 참조, `## 3. 풀이 과정` 표(문제·결과·제출 시각·WA), 문제마다 `### {index}. {name}` 서브섹션(빈 `c++` 펜스, AC·업솔빙·실재하는 미해결엔 `풀이 →` 링크), 헤딩만 있는 `## 총평`.
- 결과 라벨은 `AC`·`업솔빙`·`미해결`·`미시도`. 미시도 문제는 `대회 중 미시도.` 한 줄.
- 페널티는 API에 없어서 스크립트가 계산한다(ICPC 방식, 규칙은 `cf_contest.py` docstring). 순위·레이팅은 `contest.ratingChanges` 기준인데 CF가 페이지끼리도 값이 다르므로 발행 전 `/contest/{id}/standings`와 눈으로 대조한다.

## 사람이 스켈레톤 생성 뒤 하는 일

1. 각 `### {index}` 서브섹션에 대회 중 흐름 서술 + 라이브/WIP 코드를 붙여넣는다(`sync`가 후기를 안 보므로 손으로). 컴파일 안 되는 미완 코드도 그대로.
2. 필요하면 `## 3` 표·결과 라벨의 수동 뉘앙스를 조정한다.
3. `## 총평`을 쓴다.
4. 레이팅 그래프: Chrome DevTools → 그래프 노드 선택 → `Cmd+Shift+P` → "Capture node screenshot" → `assets/img/posts/{slug}/rating-graph.png`. 첫 대회는 점이 1개라 가치가 낮으니 이미지 줄을 지워도 된다.
5. 발행 전 `/contest/{id}/standings`에서 페널티·순위를 대조한다.
6. `publish_contest.py`로 발행한다.

## 발행

```
python3 ${CLAUDE_SKILL_DIR}/scripts/publish_contest.py <후기 .md 경로 또는 대회 ID/URL>
```

한 번에 후기 하나. `publish` 스킬과 같은 "옮긴 뒤 레포별로 각각 커밋" 흐름이다.

1. **완료 게이트** — 하나라도 걸리면 아무것도 안 건드리고 사유와 함께 에러(종료 코드 1). 서술의 질은 사람 몫이라 보지 않고 스캐폴드가 남긴 미완 표식만 본다: 라이브 코드 자리(`// 라이브 코드`) 잔존, 순위·레이팅 placeholder 잔존, 참조한 `rating-graph.png` 부재, `## 총평` 비어 있음.
2. `_drafts/contest/{파일}` → `_posts/contest/{파일}` 이동.
3. 블로그 레포 커밋: 포스트 + (있으면) `assets/img/posts/{slug}/` → `feat: [Contest] {CF API 대회명} 후기`.
4. PS 레포 커밋: 그 대회의 `live_{contestId}{index}` 폴더 전부(대회날 `day_XX`에 문제별로 생김) → 같은 메시지.
5. push는 안 한다.

- `live_` 폴더를 하나도 못 찾으면 아무것도 안 옮기고 에러(대회 ID 오타이거나 이미 수동 처리한 경우). PS 레포 검증을 블로그 레포를 건드리기 전에 하는 이유는 `publish`와 같다.
- 이미 커밋된 상태면 그 레포 커밋은 스킵한다("이미 커밋된 상태"로 보고, 에러 아님).
- 트레일러는 `Co-Authored-By: Claude <noreply@anthropic.com>`(모델명 없음 — 정적 스크립트라 커밋 시점 모델 버전을 모른다).

## 규칙

- PS 레포 소스 파일 내용은 건드리지 않는다(`scaffold`는 읽지도 않고, `publish_contest`는 `live_` 폴더를 커밋만 한다).
- 결과 보고 시 판단을 얹지 않는다 — stderr 요약·stdout 경로를 그대로 전달하고 페널티·순위 대조는 사람 몫이다.
- 스킬 정의 변경 커밋: `<type>: [Claude Skill] contest - <요약>`.
