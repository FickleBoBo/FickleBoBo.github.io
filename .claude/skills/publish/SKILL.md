---
name: publish
description: PS 드래프트를 발행한다 — _drafts/ 아래 포스트를 _posts/로 옮기고, PS 레포(풀이 소스)와 Blog 레포(포스트)에 각각 커밋한다. "/publish" 또는 "/publish 120807"처럼 호출한다.
---

# /publish — PS 포스트 발행

`/ps`로 만든 `_drafts/{플랫폼}/` 초안을 검토·작성 완료한 뒤, `_posts/`로 옮기고
PS 레포와 Blog 레포에 커밋한다.

**⚠️ 임의 실행 금지.** 이 스킬은 사용자가 직접 `/publish`를 호출하거나 "발행/커밋해"라고
명시적으로 지시할 때만 실행한다. 리뷰 통과·작업 완료 같은 상황에서 알아서 커밋하지 않는다.

## 실행

```
python3 .claude/skills/publish/publish.py $ARGUMENTS
```

- 인자: `[문제번호...]`
  - `/publish` — `_drafts/`의 모든 PS 초안을 문제별로 개별 커밋
  - `/publish 120807` — 해당 문제만
  - `/publish 120807 1929` — 여러 개
- 문제별로 수행하는 일:
  1. `_drafts/{플랫폼}/`에서 번호로 초안을 찾고 파일명/front matter를 파싱
  2. **PS 레포** 커밋 — `{YYYY-MM}/src/day_{DD}/{prefix}_{번호}` (풀이 소스)
  3. 초안을 `_posts/{플랫폼}/`으로 이동 (이미지 있으면 `assets/{slug}/` → `assets/posts/{slug}/` 동반 이동)
  4. **Blog 레포** 커밋 — 이동된 포스트 + 삭제된 초안 (+ 이미지)
- 커밋 메시지: `feat: {포스트 title}`. 양쪽 레포 모두 Claude 트레일러 부착
  (스크립트 상단 `BLOG_TRAILER` / `ALGO_TRAILER` 상수로 개별 제어).
- **push는 하지 않는다.** 커밋까지만.
- Blog 레포 커밋 실패 시 이동을 롤백(초안·이미지 원위치)한다.

## 보고

스크립트 출력의 결과표(문제별 PS / Blog 커밋 여부)를 사용자에게 그대로 전달한다.
초안을 못 찾거나 여러 개 매칭되면 스크립트가 멈추므로, 그 메시지를 전달하고 번호를 명확히 하도록 요청한다.

## 범위 밖: 이미 발행된 글 수정

`/publish`는 `_drafts/`만 다룬다. **이미 `_posts/`에 있는 글을 고치는 건 전부 수동**이며,
`/sync`·`review_check.py fill`도 발행본을 거부한다(`vars`만 예외로 허용).

- **커밋 메시지를 `feat: {title}` 그대로 쓰지 말 것** — 기존 발행 커밋과 글자 그대로 같아져
  git log에서 구분이 안 된다. 무엇을 했는지 적는다:
  `feat: [Programmers] 43105번 포스트에 0-패딩 근거 추가`. 트레일러는 발행과 동일하게 유지.
- **산문 보강**(설명 추가·정정)은 순수 Edit으로 끝난다.
- **풀이 추가**(PS 레포에 `Solution2`가 생긴 경우)는 `generate.py`와 **동일한 Java 변환을 손으로**
  적용해야 한다 — `package ...;` 제거 + `class Solution2` → `class Solution`. 복잡도 표도 수동.
