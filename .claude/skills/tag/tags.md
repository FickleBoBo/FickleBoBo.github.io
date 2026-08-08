# PS Blog Tag Vocabulary — Single Source of Truth

이 파일은 PS 블로그(`FickleBoBo.github.io`) 태그 시스템의 단일 진실 소스다.
15 카테고리 + 135 태그의 closed vocabulary를 정의한다.

## 운영 원칙

- **Frontmatter 형식**: 옵션 A (flat full ancestry). 글의 `tags` 필드에 ancestry 전체가 명시적으로 들어감
- **Auto-companion**: 자식 태그를 달면 부모 chain 전체가 자동 부착됨 (예: `dijkstra` → `shortest path` + `graph`)
- **부착 기준 (Future-you 검색 가치 테스트)**: "X로 검색한 미래의 자신이 이 글을 *유용한 결과*로 받아들일 것이다" 일 때만 부착
- **Strict 정책**: `attach_policy: strict` 표시된 태그는 *문제 해결의 핵심이 해당 자료구조/기법일 때만* 부착. 단순 보조/라이브러리 사용은 노이즈이므로 부착 금지
- **Closed vocabulary**: 이 파일에 정의되지 않은 태그는 사용 금지. `tag.py audit`에서 검출
- **`technique` 카테고리는 auto-companion 예외**: 자식 부착해도 `technique` 태그 자체는 부착 안 함
- **Umbrella 단독 부착 허용**: 모든 umbrella 카테고리(data structure, graph, dp, string, math, geometry, game theory + 하위 umbrella)는 자식이 적합하지 않으나 분류 자체가 명확한 경우 단독 부착 가능. 단, specific 자식이 있으면 그것을 우선 (umbrella 단독은 last resort)

## Schema

각 태그는 다음 필드를 가짐:

```
[tag-name]                  태그 헤더 (대괄호로 감쌈)
parent: ...                 부모 태그 (root 카테고리는 생략)
attach_when: ...            부착 기준 (한 줄, 필수)
attach_policy: strict       (선택) 강화 부착 정책
auto_companion: false       (선택) auto-companion 예외 (technique만)
note: ...                   (선택) 추가 노트 (cross-reference, disambiguation 등)
```

빈 줄이 태그 정의의 종료를 의미한다.

---

# Tag Definitions

## 1. data structure (16)

[data structure]
attach_when: 자식 자료구조 태그 부착 시 auto-companion. 또는 자식이 적합하지 않으나 자료구조 분류가 풀이의 핵심인 경우 단독 부착 가능.

[stack]
parent: data structure
attach_when: 스택 자료구조 활용이 풀이의 핵심
attach_policy: strict

[queue]
parent: data structure
attach_when: 큐 자료구조 활용이 풀이의 핵심 (단순 BFS 보조 X)
attach_policy: strict

[deque]
parent: data structure
attach_when: 덱 자료구조 활용이 풀이의 핵심 (단순 슬라이딩 윈도우 보조 X)
attach_policy: strict

[priority queue]
parent: data structure
attach_when: 우선순위 큐 사용이 풀이의 핵심

[segment tree]
parent: data structure
attach_when: 세그먼트 트리 자체 또는 변형 사용

[lazy propagation]
parent: segment tree
attach_when: 구간 업데이트 + lazy 전파 사용

[merge sort tree]
parent: segment tree
attach_when: 머지 소트 트리 사용

[2d segment tree]
parent: segment tree
attach_when: 2차원 세그먼트 트리 사용

[persistent segment tree]
parent: segment tree
attach_when: 퍼시스턴트 세그먼트 트리 사용

[fenwick tree]
parent: data structure
attach_when: 펜윅 트리(BIT) 사용

[2d fenwick tree]
parent: fenwick tree
attach_when: 2차원 펜윅 트리 사용

[sparse table]
parent: data structure
attach_when: 희소 테이블 사용 (RMQ, LCA 보조 등)

[hash set／hash map]
parent: data structure
attach_when: 해시 자료구조 선택이 문제 해결의 핵심 (단순 카운팅/룩업 보조 X)
attach_policy: strict

[tree set／tree map]
parent: data structure
attach_when: 정렬된 set/map 자료구조 선택이 문제 해결의 핵심
attach_policy: strict

[trie]
parent: data structure
attach_when: 트라이 사용 (string 또는 XOR trie 등)
note: string에 한정되지 않는 광범위 자료구조라 data structure에 분류

## 2. graph (32)

[graph]
attach_when: 자식 그래프 태그 부착 시 auto-companion. 또는 자식이 적합하지 않으나 그래프 분류가 풀이의 핵심인 경우 단독 부착 가능.

[bfs]
parent: graph
attach_when: BFS 탐색이 풀이의 핵심
note: 무가중치 그래프에서 BFS로 최소 이동 횟수를 구하는 것은 `shortest path`로 치지 않는다. `bfs` 단독으로 둘 것 (옛 블로그에서 확정된 원칙, 계승)

[dfs]
parent: graph
attach_when: DFS 탐색이 풀이의 핵심

[flood fill]
parent: graph
attach_when: 플러드 필 패턴 (그리드 영역 채우기/세기)

[topological sort]
parent: graph
attach_when: 위상 정렬 사용

[union find]
parent: graph
attach_when: DSU가 그 자체로 풀이의 핵심 기법일 때(연결성 판별 등). 크루스칼처럼 다른 명명 알고리즘의 표준 구현 요소로만 쓰이면 부착하지 않는다(kruskal 태그가 이미 그 사실을 함의).
note: kruskal/MST의 구현 수단으로 쓰인 경우는 kruskal 태그로 충분 — 별도 부착 금지.

[2-sat]
parent: graph
attach_when: 2-SAT 환원/풀이

[articulation]
parent: graph
attach_when: 단절점 또는 단절선 검출

[bipartite matching]
parent: graph
attach_when: 이분 매칭 (DFS 기반 augmenting path)

[hopcroft karp]
parent: bipartite matching
attach_when: 호프크로프트–카프 알고리즘 (BFS+DFS 매칭)

[eulerian path]
parent: graph
attach_when: 오일러 경로/회로 (모든 간선 1회 방문)
note: tree의 euler tour와는 완전히 다른 개념

[floyd's cycle detection]
parent: graph
attach_when: 플로이드의 토끼와 거북이(느린/빠른 포인터)로 함수형 그래프(각 정점이 간선 하나만 갖는 구조)에서 사이클 검출
note: 2026-08-03 신설, 근거 글 1개(LeetCode 202 Happy Number). 배열/문자열을 훑는 technique의 `two pointers`와는 다른 개념 — 혼동 방지 위해 별도 태그

[tree]
parent: graph
attach_when: 자식 트리 알고리즘 부착 시 auto-companion. 또는 자식이 적합하지 않으나 트리 분류가 풀이의 핵심인 경우 단독 부착 가능.

[lca]
parent: tree
attach_when: 최소 공통 조상 (sparse table/euler tour 등)

[euler tour]
parent: tree
attach_when: 트리 DFS 진입/탈출 시퀀스 (subtree → range)
note: graph의 eulerian path와는 완전히 다른 개념. 트리 특화 기법

[hld]
parent: tree
attach_when: heavy-light decomposition (트리 경로 쿼리)

[centroid decomposition]
parent: tree
attach_when: 센트로이드 분할 (트리 분할정복)

[shortest path]
parent: graph
attach_when: 가중치 그래프의 최단경로. 자식 알고리즘(dijkstra/bellman ford/floyd warshall/0-1 bfs) 부착 시 auto-companion. 또는 자식이 적합하지 않으나 최단경로 분류가 풀이의 핵심인 경우 단독 부착 가능.
note: 무가중치 BFS 거리는 제외 — `bfs` 단독으로 둔다. 붙이면 `bfs`와 검색 결과가 거의 겹쳐 구분값이 사라짐 (옛 블로그에서 확정된 원칙, 계승)

[dijkstra]
parent: shortest path
attach_when: 다익스트라 알고리즘 (양수 가중치 단일 시작점)

[bellman ford]
parent: shortest path
attach_when: 벨만-포드 (음수 가중치 또는 음수 사이클 검출)

[floyd warshall]
parent: shortest path
attach_when: 플로이드-워셜 (모든 쌍 최단경로)

[0-1 bfs]
parent: shortest path
attach_when: 0-1 가중치 BFS (deque 활용)

[mst]
parent: graph
attach_when: 자식 MST 알고리즘 부착 시 auto-companion. 또는 자식이 적합하지 않으나 MST 분류가 풀이의 핵심인 경우 단독 부착 가능.

[kruskal]
parent: mst
attach_when: 크루스칼 알고리즘 (간선 정렬 + union find)

[prim]
parent: mst
attach_when: 프림 알고리즘 (정점 기반 priority queue)

[scc]
parent: graph
attach_when: 자식 SCC 알고리즘 부착 시 auto-companion. 또는 자식이 적합하지 않으나 SCC 분류가 풀이의 핵심인 경우 단독 부착 가능.

[tarjan]
parent: scc
attach_when: 타잔 SCC 알고리즘 (low-link)

[kosaraju]
parent: scc
attach_when: 코사라주 SCC 알고리즘 (두 번 DFS)

[network flow]
parent: graph
attach_when: 자식 플로우 알고리즘 부착 시 auto-companion. 또는 자식이 적합하지 않으나 네트워크 플로우 분류가 풀이의 핵심인 경우 단독 부착 가능.

[max flow]
parent: network flow
attach_when: 최대 유량 (Ford-Fulkerson 계열)

[dinic]
parent: max flow
attach_when: 디닉 알고리즘 (level graph + blocking flow)

[min cost max flow]
parent: network flow
attach_when: 최소 비용 최대 유량 (SSP 등)

## 3. dp (14)

[dp]
attach_when: 자식 DP 태그 부착 시 auto-companion. 또는 자식이 적합하지 않으나 DP 분류가 풀이의 핵심인 경우 단독 부착 가능.

[knapsack]
parent: dp
attach_when: 배낭 문제 (0-1, unbounded, bounded 통합)

[lis]
parent: dp
attach_when: 가장 긴 증가하는 부분 수열 (DP 또는 이분탐색 변형)

[lcs]
parent: dp
attach_when: 가장 긴 공통 부분 수열

[bitmask dp]
parent: dp
attach_when: 비트마스크로 상태 압축한 DP
note: 일반 비트 조작은 technique의 bit manipulation. 분리

[tree dp]
parent: dp
attach_when: 트리 위에서 DP (서브트리 합/카운트 등)
note: 본질이 DP라 dp 카테고리 (graph/tree umbrella가 아님). 트리 문제 검색 시 cross-reference

[digit dp]
parent: dp
attach_when: 자릿수 DP (수의 자릿수를 상태로)

[interval dp]
parent: dp
attach_when: 구간 DP (행렬 곱셈 순서, 파일 합치기 등)

[profile dp]
parent: dp
attach_when: 프로파일 DP / broken profile DP (행 단위 비트 상태 압축)
note: bitmask dp의 변형이지만 dp 직속 flat (digit/interval dp와 같은 격)

[dp optimization]
parent: dp
attach_when: 자식 DP 최적화 기법 부착 시 auto-companion. 또는 자식이 적합하지 않으나 DP 최적화 분류가 풀이의 핵심인 경우 단독 부착 가능.

[convex hull trick]
parent: dp optimization
attach_when: CHT (선형 함수 envelope으로 DP 최적화)

[divide and conquer optimization]
parent: dp optimization
attach_when: 분할 정복 DP 최적화 (monge condition)

[knuth optimization]
parent: dp optimization
attach_when: 크누스 DP 최적화 (interval DP O(n^3) → O(n^2))

[sos dp]
parent: dp optimization
attach_when: sum over subsets DP (부분집합 합 O(2^n * n))

## 4. string (9)

[string]
attach_when: 자식 문자열 태그 부착 시 auto-companion. 또는 자식이 적합하지 않으나 문자열의 성질·구조·조작 자체가 풀이의 핵심인 경우 단독 부착 가능.
note: dp 상태값이 문자열이면 부착(예: 상태를 문자열로 관리하고 전이가 문자열 연결, 비교가 길이→사전순인 DP). 숫자를 문자열로 **표현만** 하는 경우(진법 변환, 큰 수 덧셈, 팩토리얼처럼 출력 형식이 문자열일 뿐인 경우)는 제외 — `[math]` 단독. 판별법: dp/알고리즘이 문자열 위에서 도는가, 아니면 입출력 표현일 뿐인가 (옛 블로그에서 확정된 원칙, 계승)

[palindrome]
parent: string
attach_when: 회문 성질이 풀이의 핵심인 문제 (s == reverse(s) 비교, 양 끝 두 포인터 대칭, 회문 분할 등). manacher 같은 specific 알고리즘이 있으면 그것도 함께 부착.
note: 관습적으로는 `구현`/`문자열`에 묻히지만, 이 시스템은 problem type으로서 독립 태그로 뺀다

[manacher]
parent: palindrome
attach_when: 마나허 알고리즘 (선형 시간 팰린드롬)

[anagram]
parent: string
attach_when: 애너그램 판별이 풀이의 핵심인 문제 (문자 빈도 비교, 정렬 후 비교 등)
note: palindrome과 같은 이유로 problem type 단독 태그

[kmp]
parent: string
attach_when: KMP 패턴 매칭

[string hashing]
parent: string
attach_when: 문자열 해싱 (라빈-카프 등 포함)

[z algorithm]
parent: string
attach_when: Z 함수 / Z 알고리즘

[aho corasick]
parent: string
attach_when: 아호-코라식 다중 패턴 매칭

[suffix array]
parent: string
attach_when: 접미사 배열 (LCP 포함)

## 5. math (24)

[math]
attach_when: 자식 수학 태그 부착 시 auto-companion. 또는 자식이 적합하지 않으나 수학 분류가 풀이의 핵심인 경우 단독 부착 가능.

[binary exponentiation]
parent: math
attach_when: 이진 거듭제곱 (modular exp, matrix exp 등)
note: cross-cutting 기법이라 math 직속 flat (subfield 강제 X)

[number theory]
parent: math
attach_when: 자식 정수론 태그 부착 시 auto-companion. 또는 자식이 적합하지 않으나 정수론 분류가 풀이의 핵심인 경우 단독 부착 가능.

[sieve of eratosthenes]
parent: number theory
attach_when: 에라토스테네스의 체
note: 체 계열은 flat sibling으로 확장 (linear sieve, segmented sieve 등). `sieve` umbrella를 두지 않음

[prime factorization]
parent: number theory
attach_when: 소인수분해

[euclidean algorithm]
parent: number theory
attach_when: 유클리드 호제법 (gcd)
note: `euclidean` 단독은 euclidean distance/geometry로 읽히므로 `algorithm`을 명시. 표준 명칭도 "Euclidean algorithm"

[extended euclidean algorithm]
parent: number theory
attach_when: 확장 유클리드 (gcd 계수)

[modular inverse]
parent: number theory
attach_when: 모듈러 역원 (페르마/확장 유클리드/CRT 활용)

[fermat's little theorem]
parent: number theory
attach_when: 페르마의 소정리 활용

[crt]
parent: number theory
attach_when: 중국인의 나머지 정리

[euler's totient]
parent: number theory
attach_when: 오일러 피 함수

[mobius function]
parent: number theory
attach_when: 뫼비우스 함수 / 뫼비우스 반전

[miller rabin]
parent: number theory
attach_when: 밀러-라빈 소수 판정 (큰 수)

[pollard rho]
parent: number theory
attach_when: 폴라드 로 인수분해 (큰 수)

[combinatorics]
parent: math
attach_when: 자식 조합론 태그 부착 시 auto-companion. 또는 자식이 적합하지 않으나 조합론 분류가 풀이의 핵심인 경우 단독 부착 가능.

[binomial coefficient]
parent: combinatorics
attach_when: 이항 계수 (파스칼/팩토리얼/모듈러)

[lucas' theorem]
parent: combinatorics
attach_when: 뤼카 정리 (소수 모듈러 이항 계수)

[inclusion exclusion]
parent: combinatorics
attach_when: 포함-배제 원리

[catalan numbers]
parent: combinatorics
attach_when: 카탈란 수 (괄호 매칭, 이진 트리 카운트 등)

[linear algebra]
parent: math
attach_when: 자식 선형대수 태그 부착 시 auto-companion. 또는 자식이 적합하지 않으나 선형대수 분류가 풀이의 핵심인 경우 단독 부착 가능.

[matrix exponentiation]
parent: linear algebra
attach_when: 행렬 거듭제곱 (선형 점화식 등)

[gauss elimination]
parent: linear algebra
attach_when: 가우스 소거법 (연립방정식, rank, determinant)

[polynomial]
parent: math
attach_when: 자식 다항식 태그 부착 시 auto-companion. 또는 자식이 적합하지 않으나 다항식 분류가 풀이의 핵심인 경우 단독 부착 가능.

[fft]
parent: polynomial
attach_when: 고속 푸리에 변환 (다항식/큰 수 곱셈)

## 6. geometry (11)

[geometry]
attach_when: 자식 기하 태그 부착 시 auto-companion. 또는 자식이 적합하지 않으나 기하 분류가 풀이의 핵심인 경우 단독 부착 가능.

[ccw]
parent: geometry
attach_when: CCW (세 점 방향성 외적)

[convex hull]
parent: geometry
attach_when: 볼록 껍질 (Graham/Andrew)

[polygon area]
parent: geometry
attach_when: 다각형 넓이 (Shoelace formula)

[point in polygon]
parent: geometry
attach_when: 점 다각형 내부 판정 (ray casting / winding)

[segment intersection]
parent: geometry
attach_when: 두 선분 교차 판정/교차점 (CCW 4회)

[closest pair of points]
parent: geometry
attach_when: 가장 가까운 두 점 (분할정복/sweep)

[rotating calipers]
parent: geometry
attach_when: 회전하는 캘리퍼스 (지름/너비 등)

[pick's theorem]
parent: geometry
attach_when: 픽의 정리 (격자 다각형 넓이)

[pythagorean theorem]
parent: geometry
attach_when: 피타고라스 정리 활용 (직각삼각형 변 관계, 두 점 거리, 대각선 길이 등)

[polar sort]
parent: geometry
attach_when: 각도 정렬 (CCW 비교 또는 atan2)

## 7. greedy (1)

[greedy]
attach_when: 그리디 알고리즘이 풀이의 핵심

## 8. technique (자식 20, technique 자체는 부착 X)

[technique]
attach_when: (카테고리 only — 태그로 부착하지 않음)
auto_companion: false
note: catch-all 카테고리. 자식 부착해도 technique 자체는 부착 안 됨

[sorting]
parent: technique
attach_when: 정렬이 문제 해결의 핵심 (greedy + 정렬, 좌표 정렬 후 sweeping 등). 단순 입력 정렬 X
attach_policy: strict
note: 비교 기반 호출(Collections.sort 등)에 한정되지 않는다 — 빈도를 인덱스로 써서 실제 순서(랭킹)를 만들어내는 버킷/카운팅 정렬도 "정렬이 핵심"이면 부착 대상(LeetCode 347 버킷 정렬 접근, 2026-08-08). 반대로 카운팅/집계만 하고 순서를 만들어내지 않는 경우(존재 확인·합계 비교용, 예: LeetCode 242 Valid Anagram의 카운팅 배열 접근)는 정렬 자체가 발생하지 않았으므로 부착 대상 아님 — 이쪽은 애초에 sorting/hash set／hash map 어느 쪽도 강제로 붙이지 않는다.
note: bucket sort 등 정렬 알고리즘별 개별 leaf 신설은 2026-08-08 논의에서 보류 — sorting 하나로 퉁치기엔 비교 기반과 인덱스 기반이 메커니즘상 다르다는 문제 제기는 있었으나, 지금은 sorting으로 근사하고 정렬 계열 근거 글이 몇 건 더 쌓이면 sieve 계열(위 참고)처럼 flat sibling 분리를 재검토한다.

[divide and conquer]
parent: technique
attach_when: 분할정복 패턴

[two pointers]
parent: technique
attach_when: 투 포인터 기법

[sliding window]
parent: technique
attach_when: 슬라이딩 윈도우 기법

[monotonic stack]
parent: technique
attach_when: 단조 스택 활용 (next greater 등)

[monotonic queue]
parent: technique
attach_when: 단조 큐 활용 (sliding window max 등)

[prefix sum]
parent: technique
attach_when: 누적합 활용

[2d prefix sum]
parent: technique
attach_when: 2차원 누적합 활용

[difference array]
parent: technique
attach_when: 차분 배열 (range update + point query)

[bit manipulation]
parent: technique
attach_when: 비트 연산 자체의 성질(XOR 자기상쇄, 시프트, 개별 비트 조작 등)을 이용한 기법. 부분집합을 비트로 표현해 순회/상태 압축하는 쓰임은 아님(DP면 bitmask dp, 아니어도 상태 압축 성격이면 검토 필요)
note: bitmask dp는 별도 (dp 카테고리)

[coordinate compression]
parent: technique
attach_when: 좌표 압축

[meet in the middle]
parent: technique
attach_when: 중간에서 만나기 (절반 분할 + 결합)

[binary search]
parent: technique
attach_when: 이분 탐색 (정렬된 배열 검색)

[parametric search]
parent: technique
attach_when: 매개변수 탐색 (결정 문제로 환원 후 이분탐색)

[ternary search]
parent: technique
attach_when: 삼분 탐색 (볼록/오목 함수 최적화)

[backtracking]
parent: technique
attach_when: 백트래킹 (가지치기 + DFS-like 탐색)

[offline queries]
parent: technique
attach_when: 쿼리 정렬/재배치 (오프라인 처리)

[sweeping]
parent: technique
attach_when: 스위핑 (line sweep, event-based)

[sqrt decomposition]
parent: technique
attach_when: 평방 분할 (블록 단위 처리)

[mo's algorithm]
parent: technique
attach_when: Mo's algorithm (오프라인 쿼리 + sqrt decomposition)

## 9. game theory (2)

[game theory]
attach_when: 게임 이론이 풀이의 핵심 (Nim, 최적 게임 등)

[sprague grundy]
parent: game theory
attach_when: 스프라그-그런디 정리 (그런디 수 계산)

## 10. implementation (1)

[implementation]
attach_when: 코드 구현 자체가 복잡한 문제 (엣지 케이스, 상태 관리, parsing 등)
note: **구현이 본체인 문제에만** 부착. 그리디·dp 등 알고리즘적 통찰이 본체면 제외(엣지 케이스가 있어도 그 알고리즘이 실질이면 알고리즘 태그가 우선). 기준선은 알고리즘 없이 규칙을 코드로 옮기는 문제 — 이 블로그에서는 118666 성격 유형 검사하기가 첫 사례. 엣지 케이스 유무로 붙이기 시작하면 거의 모든 문제에 붙어 검색 가치가 사라짐 (옛 블로그에서 확정된 원칙, 계승)

## 11. simulation (1)

[simulation]
attach_when: 주어진 시나리오/규칙을 그대로 따라가는 문제

## 12. brute force (1)

[brute force]
attach_when: 모든 가능한 경우 시도 (가지치기 없는 완전 탐색)
note: backtracking(technique)과 구분 — backtracking은 가지치기 + DFS-like

## 13. ad hoc (1)

[ad hoc]
attach_when: 특정 알고리즘 없이 case-by-case 추론
note: **단순히 답이 짝/홀 등 조건에 따라 갈리는 것만으로는 `ad hoc`을 함께 붙이지 않는다.** 그 분기가 수학적 도출 과정의 자연스러운 결과(예: 텔레스코핑 합에서 홀수 항 하나가 남는 것)라면 `math` 단독으로 충분하다 — 2026-08-03 정정. 2148A(Sublime Sequence, 짝/홀에 따라 0 또는 x)가 처음엔 이 반대 예시로 잘못 인용됐다가, "이 분기 자체가 흔한 패턴이라 붙이면 `ad hoc`이 `math`의 동의어가 된다"는 지적으로 `math` 단독으로 정정됨. `ad hoc`을 **함께** 붙이는 건 공식 하나로 안 끝나고, 문제 고유의 여러 케이스를 서로 다른 논거로 따로 따져야 하는 경우로 한정한다(아직 이 블로그에 확정 사례 없음).
note: **홀짝/parity라는 이름의 태그는 아직 어휘에 없음** — 이분 색칠처럼 각 case가 별도 증명을 요구하는 **구조적** 홀짝 논증이 나오면 지금은 `ad hoc`이 대신 받는다(위 note의 "단순 분기"와는 다른 경우). 신설 여부는 아래 2026-08-03 정정 노트 기준(개수가 아니라 표준 개념 여부)을 따를 것.
note: **"글 1개 = 신설 보류"는 일률 규칙이 아니다 (2026-08-03 정정).** parity가 보류된 진짜 이유는 *그 개념 자체가 사후에 귀납적으로 뽑아낸 애드혹 패턴*이라 재현성이 불확실했기 때문이지, 단순히 글이 1개였기 때문이 아니다. 반대로 이름과 정의가 이미 표준으로 확립된 알고리즘(dijkstra/kruskal/manacher와 같은 급 — 예: `floyd's cycle detection`, graph 산하 2026-08-03 신설)은 **글 1개로도 즉시 신설 가능**하다. 판단 기준은 "몇 건 쌓였는가"가 아니라 "이 태그가 재사용 가능한 표준 개념인가, 아니면 이 글에서만 관찰된 귀납적 패턴인가".

## 14. constructive (1)

[constructive]
attach_when: 답을 step-by-step 구성 (예시 만들기)

## 15. warm up (1)

[warm up]
attach_when: PS 추론이나 알고리즘 없이 프로그래밍 언어 사용법(입출력, 기초 자료형, 사칙연산, 문자열 인덱싱, 단순 출력 등) 연습 수준의 문제
note: 난이도 표시에 가까운 outlier 카테고리. 다른 algorithm 태그가 매칭되지 않는 trivial 글에만 부착. 다른 태그와 배타는 강제하지 않으나 단독 사용이 자연스러움.
