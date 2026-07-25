---
name: publish
description: PS 드래프트를 발행한다 — _drafts/ 아래 포스트를 _posts/로 옮기고, Algorithm 레포(풀이 소스)와 Blog 레포(포스트)에 각각 커밋한다. "/publish" 또는 "/publish 120807"처럼 호출한다.
---

# /publish — PS 포스트 발행

`/ps`로 만든 `_drafts/{플랫폼}/` 초안을 검토·작성 완료한 뒤, `_posts/`로 옮기고
Algorithm 레포와 Blog 레포에 커밋한다.

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
  2. **Algorithm 레포** 커밋 — `{YYYY-MM}/src/day_{DD}/{prefix}_{번호}` (풀이 소스)
  3. 초안을 `_posts/{플랫폼}/`으로 이동 (이미지 있으면 `assets/{slug}/` → `assets/posts/{slug}/` 동반 이동)
  4. **Blog 레포** 커밋 — 이동된 포스트 + 삭제된 초안 (+ 이미지)
- 커밋 메시지: `feat: {포스트 title}`. 양쪽 레포 모두 Claude 트레일러 부착
  (스크립트 상단 `BLOG_TRAILER` / `ALGO_TRAILER` 상수로 개별 제어).
- **push는 하지 않는다.** 커밋까지만.
- Blog 레포 커밋 실패 시 이동을 롤백(초안·이미지 원위치)한다.

## 보고

스크립트 출력의 결과표(문제별 Algorithm / Blog 커밋 여부)를 사용자에게 그대로 전달한다.
초안을 못 찾거나 여러 개 매칭되면 스크립트가 멈추므로, 그 메시지를 전달하고 번호를 명확히 하도록 요청한다.
