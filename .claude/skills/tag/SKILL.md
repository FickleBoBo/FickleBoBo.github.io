---
name: tag
description: PS 포스트에 closed-vocabulary 태그를 부착한다. leaf 태그를 고르면 부모 ancestry가 자동 확장되어 front matter에 기록된다. "/tag 120807 dijkstra" 또는 "/tag 120807"(코드 보고 추천)처럼 호출한다.
---

# /tag — PS 포스트 태그 부착

`tags.md`의 closed vocabulary(15 카테고리 / 135 태그)에서 **leaf(구체) 태그**를 골라 포스트에
부착한다. 부모 ancestry는 `tag.py`가 자동 확장한다(`dijkstra` → `shortest path` + `graph`).
파이프라인상 **`/review` 등급 확인 후** 본인이 이 스킬로 태깅한다.

## 실행

```
python3 .claude/skills/tag/tag.py                       # 인자 없음: _drafts PS 포스트 + 태그 상태 나열
python3 .claude/skills/tag/tag.py <번호> <leaf태그...>   # 부착
python3 .claude/skills/tag/tag.py audit [번호]           # 어휘 정합성 감사
python3 .claude/skills/tag/tag.py vocab                  # 어휘 자체검증
```

- **인자 없음** (`/tag`) → **기본·게으른 경로.** `tag.py`를 인자 없이 실행하면 `_drafts/`의 PS 포스트(방금
  `/review`한 발행 대기분)를 태그 상태와 함께 나열한다. 그중 **미태깅(`[Unlinked]`)인 것만** 각각 코드/아이디어를
  읽어 leaf를 선정하고, 한 번에 제안해 확인받은 뒤 포스트별로 `tag.py <번호> <leaf들>` 부착한다.
  이미 태깅된 건 건너뛴다(멱등). 미태깅이 0개면 붙일 게 없다고 보고한다.
- **leaf 태그가 이미 지정됨** (`/tag 120807 dijkstra sliding window`) → 그대로 `tag.py`로 부착.
- **번호만 주어짐** (`/tag 120807`) → 그 포스트의 코드/아이디어를 읽고 아래 기준으로 leaf 태그를
  **직접 선정**한 뒤, 사용자에게 제안하고 확인받아 `tag.py <번호> <고른 leaf들>`로 부착한다.
- 부착은 `_drafts/` 우선, 없으면 `_posts/`에서 해당 번호를 찾는다.
- 태그 이름에 **공백이 있으면 CLI 인자로 넘길 때 따옴표**로 감싼다(예: `tag.py 120807 "warm up" "two pointers"`).

## leaf 태그 선정 기준 (번호만 주어졌을 때)

`tags.md`가 단일 진실 소스다. 각 태그의 `attach_when`을 실제로 읽고 대조한다.

- **specific leaf만 고른다.** ancestry는 자동 확장되므로 부모(`graph`, `dp` 등)는 적지 않는다.
  예: `dijkstra`만 고르면 `shortest path`, `graph`는 자동으로 붙는다.
- **Future-you 검색가치 테스트**: "이 태그로 검색한 미래의 내가 이 글을 *유용한 결과*로 받아들일까"
  일 때만 부착.
- **strict 정책 태그**(`attach_policy: strict` — stack/queue/deque/sorting/hash set／hash map/
  tree set／tree map 등)는 **문제 해결의 핵심일 때만.** 단순 보조·라이브러리 사용은 노이즈이므로 제외.
- **`technique` 카테고리 자체는 부착 금지** — 자식(two pointers, prefix sum, binary search 등)만.
- **multi-tag 적극**: 여러 기법이 모두 검색가치가 있으면 다 부착(예: `knapsack` + `greedy`).
- **상위 알고리즘이 함의하는 하위 기법은 생략**: 어떤 기법이 다른 명명 알고리즘의 **표준 구성요소**로만
  쓰였다면 별도 부착하지 않는다 — 상위 태그가 이미 그 사실을 함의하므로 자동 중복이 된다.
  예: 크루스칼은 정의상 항상 유니온 파인드로 사이클을 거르므로 `kruskal`에 `union find`를 덧붙이지
  않는다. **그 기법 자체가 독립적으로 풀이의 핵심일 때만** 부착한다(연결성 판별에 쓴 DSU 등).
- **umbrella 단독은 last resort**: 적합한 specific 자식이 있으면 그것을 우선. 자식이 없고 분류
  자체가 핵심일 때만 umbrella(`graph`, `dp`, `math` 등) 단독 부착 가능.
- **trivial 글**(알고리즘 없이 언어 사용법 수준)은 `warm up` 단독.
- **closed vocabulary — 단, 신설은 능동 제안**: `tags.md`에 없는 태그를 임의로 만들어 붙이지는
  않지만, 적합한 leaf가 없을 때 그냥 `ad hoc`/`math`로 근사하고 넘어가지 말고 **먼저 신설 여부를
  검토해 사용자에게 제안**한다. 판단 기준은 "몇 건 쌓였는가"가 아니라 **"이 개념이 이미 이름과
  정의가 표준으로 확립된 재사용 가능한 알고리즘/기법인가"** — dijkstra·kruskal·manacher와 같은
  급이면 근거 글이 1개뿐이어도 즉시 신설을 제안한다(`floyd's cycle detection` 선례, 2026-08-03).
  반대로 이 글에서만 관찰된 귀납적·애드혹 패턴이면 표준 명칭이 없으니 근사 태그로 두고 2~3건
  쌓일 때까지 보류한다(parity 태그 선례). 애매하면 후보 이름·부모 카테고리·근거를 함께 제시하고
  사용자 판단을 받는다(`tags.md` 13. ad hoc 카테고리의 2026-08-03 정정 노트 참고).

### 입력 주의
- 태그 이름의 `／`는 **fullwidth 슬래시(U+FF0F)**다(`hash set／hash map` 등). 일반 `/`로 쓰면
  거부되지만 스크립트가 올바른 후보를 제시하므로, 그대로 다시 실행하면 된다.

## 보고
- 부착 후 `tag.py` 출력(이전 → 이후 태그, 확장 개수)을 그대로 전달.
- 어휘에 없는 태그를 지정하면 `tag.py`가 거부하므로, 그 목록을 전달하고 올바른 태그로 다시 제안.
- 태그 선정이 애매하면 후보와 근거를 제시하고 사용자 판단을 받는다.

## 참고
- `solved_ac` 매핑은 이식하지 않았다(백준/solved.ac 전용, 새 블로그 플랫폼엔 미대응).
- `tags.md`의 note는 2026-08-03에 한 차례 정리했다 — 이 레포에 대응 글이 없는 옛 백준 예시 번호·
  옛 블로그 시절 날짜(`2026-07-17` 등, 이 블로그 시작일 `2026-07-23`보다 이전)·이식하지 않은 도구
  (`tag_migrate`) 참조를 걷어내고, 가능한 곳은 이 블로그의 실제 발행 글로 예시를 바꿨다. 순수 원칙만
  남고 새 예시가 없는 note는 `(옛 블로그에서 확정된 원칙, 계승)`으로 출처를 밝혀뒀다.
