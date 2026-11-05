# 태그 판정 기준

어휘집([`tags.yaml`](../_shared/tags.yaml))에서 어떤 태그를 붙일지 정하는 기준이다. 절차는 [`SKILL.md`](SKILL.md).

용도: 태그로 관련 문제를 찾아보고, 한 분야의 문제들에서 어떤 테크닉이 쓰이는지 탐색한다. 그래서 태그로 모은 문제 목록이 그 태그의 이름값을 해야 한다(기술적으로 걸린다고 다 붙이지 않는다).

## 판정 원칙

접근(`### 풀이`/`### 풀이 N`)마다 적용한다.

1. 이 문제를 "이런 문제"라고 소개할 때 그 태그가 자연스럽게 나오고, 그 태그의 문제 목록에 들어 있어도 어색하지 않으면 붙인다. 도메인(string, geometry), 기법(dijkstra), 성격(constructive)을 가르지 않고 같은 원칙으로 판정하며, 여러 태그가 함께 붙어도 된다. 덧셈을 했다고 math, 코드를 썼다고 implementation을 붙이지 않는다.
2. 가장 구체적인 태그를 고른다. 이름이 비슷하다고 고르지 않는다 — 코드가 그 알고리즘/자료구조를 실제로 구현·사용할 때만(특히 고급 알고리즘).
3. 조상은 고르지 않는다. leaf만 고르면 `apply_tags.py`가 parents를 재귀로 따라 조상 태그를 전부 붙인다(예: `lazy propagation` → `segment tree`, `data structure`). parents가 2개인 태그(`# 다중부모`)는 두 라인을 각각 따라간다. 하위만 골라도 상위 모음 페이지에 모이게 하는 의도된 정책이다. `contextual`이 있는 태그(trie, lcs)는 구조적 부모가 아니라 판단 기준이다 — 문자열 문제에서 trie를 쓰거나 문자열에 대한 lcs(수열 lcs는 해당 없음)면 string도 같이 붙일지 판단한다.
4. 자료구조 태그(stack, queue, deque, priority queue, hash set/map, tree set/map 등)는 그 자료구조가 풀이의 핵심일 때만 붙인다. 이미 고른 알고리즘 태그가 그 자료구조를 암묵적으로 포함하면 붙이지 않는다(bfs→queue, dijkstra→priority queue, kruskal→union find). 단 그 자료구조 자체가 풀이의 핵심이면(예: 가중치 DSU, 롤백) 붙인다.
5. warm up은 한 접근을 위 판정으로 판정했을 때 아무 태그도 안 남은 경우에만 그 접근에 붙는 마지막 라벨이고, 한 접근 안에서는 다른 태그와 병기하지 않는다. 태그 최소 1개 정책 때문에 존재한다.
6. 접근이 여럿이면 접근마다 warm up까지 포함해 판정을 끝낸 뒤, 그 결과의 합집합이 포스트 태그다. 한 접근이 warm up이고 다른 접근이 태그를 가지면 둘이 병기된다(단일 접근 포스트는 5번 그대로).
7. `interactive`는 문제 형식 태그라 위 판정과 독립이다 — 인터랙티브 문제면 다른 태그와 함께 붙인다.
8. SQL 전용 포스트(언어 브래킷이 [MySQL] 하나뿐): `sql` 하나만 달고 끝낸다. 다른 태그와 병기하지 않고 위 판정도 거치지 않는다.

## 경계가 애매한 태그 쌍

판정 원칙만으로 안 갈릴 때 아래 기준으로 판단한다.

### string, warm up

string은 문제가 문자열의 내용(글자·부분문자열·패턴·순서)을 들여다보거나 바꾸는 문제일 때 붙인다. 풀이가 내장함수 한 줄이어도 붙이고, 그러면 warm up은 뺀다. 판별 질문은 "문자열 가공 부분을 빼도 풀이가 성립하는가" — 성립하면 문자열이 숫자·기호를 담는 입력 형식일 뿐이라 string이 아니다. (a) 필터·탐색·매칭·슬라이스·뒤집기·재배열·파싱·카운트·split·글자별 변환(대소문자·치환·시프트)은 string이다. (b) 문자열 출력만(echo, 이어붙여 출력, n번 반복)이면 string이 아니다. (c) 문자열↔숫자 통째 변환만 하고 핵심이 그 숫자의 비교·연산이면 string이 아니다(자릿수 분해도 같다). (d) 문자를 하나씩 보며 stack 등에 넣거나 비교만 하는 단순 순회(괄호 짝 맞추기)는 string이 아니라 stack 등만 붙인다.

### math, implementation, warm up

- math는 지문에 없는 식·성질을 풀이에서 직접 떠올려야 할 때(공식 유도, 규칙성 발견) 붙인다. 지문이 판정 기준·공식을 그대로 주고 남은 작업이 기계적 적용이면 붙이지 않고(예: "9로 나눈 나머지는 각 자리 숫자 합의 나머지, 이 사실을 이용하여"), 사칙연산·나머지를 쓴 것만으로도 붙이지 않는다. 하위 분야(number theory, combinatorics 등)에 맞으면 그 하위 태그를 고르고 math는 조상으로 붙는다. 지문이 기준은 주되 방법은 안 알려주면(유한소수 판별 — 분모 소인수가 2·5뿐이라는 기준만 주고 기약분수화는 안 알려줌) 풀이가 가져온 기법(euclidean algorithm 등)과 그 조상을 단다.
- implementation은 아이디어는 분명한데 코드로 옮겨 풀어내는 것 자체가 작업의 대부분일 때(규칙이 긴 시뮬레이션, 복잡한 상태·분기·엣지케이스, 큰 수 직접 연산) 붙이며 다른 태그와 병기할 수 있다.
- warm up은 위 어느 것도 안 붙고 지문을 그대로 옮기면 끝나는 문제(입출력, 단순 조건·반복, 내장 함수 호출)에만 붙인다.

### greedy, dynamic programming, constructive, ad hoc

greedy는 매 단계 국소 최선을 고르고 그것이 전체 최적이 되는 근거(교환 논증 등)가 성립하는 접근일 때(정렬·우선순위 큐 기반 포함). 코드 구조만으로 안 가려지면 포스트의 아이디어 서술이 있는 경우 그 근거까지 보고 판단한다. dynamic programming은 부분문제 점화식(표/메모)이 있을 때 — prefix max를 한 번 스캔하는 정도는 dp가 아니다. constructive는 조건을 만족하는 답(배열·문자열 등)을 직접 만들어내고 그 구성의 정당성이 핵심일 때. 구성에 쓴 기법이 정당성이 아니라 구현 수단일 뿐이면(예: 금지구간을 표시하는 difference array) 그 기법과 병기한다. ad hoc은 그 문제에서만 통하는 비자명한 통찰(불변량, 구조 발견, 증명이 필요한 성질)이 풀이의 본체일 때 — 단순한 카운팅·조건 확인·케이스 분기이거나 정형 기법이 뼈대면 붙이지 않는다. constructive와 ad hoc은 한 문제에 둘 다 붙을 수 있다.

### brute force, warm up

brute force는 "다 해봐도 된다"는 판단이나 탐색 공간 설계가 풀이의 핵심일 때. 지문이 시키는 대로 훑으며 계산·세기만 하면(이중 루프여도) warm up. 반복문 전수 탐색은 brute force. dfs/bfs가 붙으면 brute force는 중복이라 뺀다.

### dfs, backtracking

dfs는 그래프·트리를 깊이 우선으로 순회하는 경우(visited 유무 무관)이거나, 재귀로 선택을 갈라 상태 공간(결정 트리)을 탐색해 경우의 수·도달 여부를 구하는 경우(타겟 넘버처럼 부분 해를 따로 쌓지 않고 값을 인자로 넘기는 것)다. 판별 질문은 "노드(상태)와 간선(선택)을 말할 수 있고 그것을 깊이 우선으로 훑는 게 풀이의 핵심인가". backtracking은 재귀로 부분 해(배열·visited 등)를 한 칸씩 쌓다가 돌아오며 취소하거나 가지치기하는 경우 — 명시적 undo 없이 `sel[depth]`를 덮어써 다음 선택으로 대체하는 구조도 해당한다(N과 M 시리즈, N-Queen, 스도쿠). 그래서 부분 해를 쌓고 되돌리거나 가지치기하면 dfs가 아니라 backtracking이고, 값을 인자로 넘기며 경우를 세는 재귀 탐색은 backtracking이 아니라 dfs다. 재귀가 구현 수단일 뿐인 분할 정복·단순 재귀 계산·메모이제이션 점화식은 dfs가 아니다(각각 divide and conquer, 태그 없음, dynamic programming).

### bfs, flood fill, shortest path

bfs는 큐로 레벨 순회하는 경우 — 큐로 절차를 흉내 내는 시뮬레이션(프린터 등)은 bfs가 아니다. 격자 최단거리는 bfs만 붙이고, 가중치가 있어 최단경로 알고리즘(dijkstra 등)을 쓸 때만 shortest path 계열. flood fill은 격자에서 연결 영역의 개수·크기를 구하거나 영역을 칠하는 문제일 때만 bfs/dfs와 병기한다(시작 칸에서 도달한 칸 수를 세는 것 포함). 거리·시간·도달 여부가 목적이거나, 격자가 아닌 일반 그래프, 외부 공기 판별 같은 보조 판정이면 붙이지 않는다.

### tree, graph

tree는 graph의 자식이 아닌 독립 태그다. 입력이 트리여도 단순 순회(bfs/dfs)면 graph 계열, 조상·서브트리·트리 성질을 쓰면 tree 계열. 풀이의 주된 작업이 어느 쪽이냐로 가르고, 둘 다면 둘 다 붙인다.

### two pointers, sliding window

두 태그는 병렬이다(한쪽이 다른 쪽의 부모가 아님). two pointers는 정렬된/단조성 있는 배열에서 두 포인터가 각자 독립적으로(또는 반대 방향으로) 이동하며 조건을 좁혀 가는 경우. sliding window는 "연속된 구간"을 유지한 채 한쪽 끝을 늘리고 반대쪽을 줄이며 조건을 만족하는 구간을 찾는 경우. 구현이 비슷해도 무엇을 유지하는지로 구분한다. 누적합 배열로 구간합을 질의하면 prefix sum이다.

### two pointers, floyd's cycle detection

floyd's cycle detection(토끼와 거북이)은 배열 인덱싱이 아니라 값에서 다음 값을 정하는 함수 f(x)로 정의된 암묵적 연결 리스트/그래프 위에서 서로 다른 속도(1스텝/2스텝)의 두 포인터가 사이클에서 만난다는 성질로 사이클 여부·시작점을 찾는 기법이다. "두 포인터"라는 표면적 유사성과 무관하게 함수형 시퀀스 위에서 동작하는지가 구분 기준.

### sorting, greedy

sorting은 문제가 정렬 자체를 요구하거나(정렬 기준 설계 포함) 정렬이 풀이의 전제/아이디어 (정렬 후 인접 비교, sort+greedy, sort+two pointers)일 때. 출력 순서를 맞추려는 부수적 정렬은 태그하지 않는다.

### hash set/map, tree set/map, string hashing

LeetCode의 자료구조 설계 문제(LRU 캐시 등)는 data structure와 핵심 구조 태그만 붙인다. hash set/map은 해시 기반 set/map(HashSet/HashMap, unordered_map, dict/set)을 아우르고, 조회·카운트·존재 판정이 풀이의 핵심일 때 붙인다. tree set/map은 정렬된 set/map(TreeSet/TreeMap, std::set/map, PBDS)에서 순서 질의(lower_bound, floor/ceiling, 최솟값·최댓값 삭제)가 핵심일 때 — 단순 정렬·중복 제거 용도면 아니다. string hashing은 롤링 해시로 문자열을 비교하는 경우이고 set에 해시를 모으는 것만으론 hash set/map을 추가하지 않는다.

### bit manipulation, bitmask, bitmask dp

bit manipulation은 XOR/AND/시프트 등 비트 자체의 성질을 이용하는 트릭(비트 개수 세기, XOR 소거, 2의 거듭제곱 판정). bitmask는 부분집합을 정수 하나로 인코딩해 다루는 표현 방식 그 자체로, bit manipulation이 조상으로 자동 붙는다. bitmask dp는 그 bitmask를 DP 상태로 쓰는 경우 — dynamic programming과 bitmask(와 그 조상)가 함께 붙는다.

### game theory, sprague grundy, dynamic programming

game theory는 두 사람이 번갈아 두는 게임의 승패·필승 전략을 다루는 문제 전반이다. 일반 님의 XOR 판정(Bouton 정리)과 님으로 환원되는 문제(님블 등)는 game theory만 붙인다. sprague grundy는 그런디 수를 mex로 직접 구하고 독립된 게임들의 그런디 수를 XOR로 합쳐 판정할 때(이동 규칙이 님과 달라 그런디 수를 계산해야 하는 경우)만 붙이며, 미제르 님은 붙이지 않는다. 승패를 작은 상태부터 점화식으로 채우면(돌 게임 3·4) dynamic programming을 함께, 홀짝·주기 규칙으로 바로 판정되면 game theory만 붙인다.

### divide and conquer, divide and conquer optimization

divide and conquer optimization은 DP 점화식의 최적 분할점 단조성을 이용하는 최적화(dp optimization 자식)다. 일반 분할 정복·병합 정렬형 풀이는 divide and conquer.

### geometry, pythagorean theorem, warm up

geometry는 좌표/도형에 대한 판정·계산(거리, 넓이, 방향, 삼각형 성립 판정, 겹침)이면 풀이가 사소해도 붙이고 warm up은 뺀다. 격자 이동·2차원 배열 조작은 geometry가 아니다. pythagorean theorem은 피타고라스 관계(두 점 사이 거리 공식·빗변 길이·직각 판정 포함)가 풀이의 핵심 단계일 때 geometry와 함께 붙인다. 거리 계산이 다른 알고리즘의 부속 단계일 뿐이면 붙이지 않는다.
