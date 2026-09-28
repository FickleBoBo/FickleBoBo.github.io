---
title: "[Codeforces] #2266B - Three Piles [C++]"
date: 2026-09-22
categories: [PS, Codeforces]
tags: ["math", "game theory"]
slug: codeforces-2266b
media_subpath: /assets/img/posts/codeforces-2266b/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2266/B)
{: .prompt-info }

---

## 1. 아이디어

Alice와 Bob이 각각 파일을 하나씩 가지고 있고 더미 파일도 하나 존재하는 상황이다. Alice와 Bob의 파일의 크기 차이를 Alice는 최대로, Bob은 최소로 하려고 할 때 최적의 플레이 이후 결과를 구해야 한다. Alice의 파일 크기를 `a`, Bob의 파일 크기를 `b`, 더미 파일의 크기를 `c`라고 할 때 `a >= b`, `a < b`로 케이스를 나눌 수 있다.

`a >= b`의 경우 Alice가 먼저 시작하므로 항상 더미 파일 전체를 가져오는 게 Alice한테는 유리하고 Bob한테는 불리해서 최적이다. `a < b`의 경우 Alice가 더미 파일을 가져가는 게 유리하면 전부 가져가는 게 Alice한테는 유리하고 Bob한테는 불리하므로 최적이다. `a < b`에서 Alice가 더미 파일을 가져가는 게 불리하면 Alice는 안 가져가는 게 최적의 선택이고 Bob 역시 안 가져가는 게 최적의 선택이므로 둘 다 더미 파일을 가져가지 않은 채 끝난다.

따라서 Alice는 가져가는 게 유리한 순간 전부 가져가고 아닌 경우 둘 다 가져가지 않게 되는 게 각 플레이어의 최적 전략이 된다.

---

## 2. 복잡도

| 접근 | 시간   | 공간   |
| ---- | ------ | ------ |
| 풀이 | $O(T)$ | $O(1)$ |

($T$ = 테스트 케이스 수)

---

## 3. 코드

### 풀이 [C++]

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    long long a, b, c;
    cin >> a >> b >> c;
    cout << max(abs(a + c - b), abs(a - b)) << '\n';
}

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);

    int t;
    cin >> t;
    while (t--) solve();
}
```

Alice가 가져가는 게 유리해서 전부 가져가는 경우는 `abs(a + c - b)`가 되며, 둘 다 가져가지 않는 경우는 `abs(a - b)`가 된다. 둘 중 최댓값이 첫 턴에 Alice의 두 가지 선택 중 최적인 값이 된다.

---
