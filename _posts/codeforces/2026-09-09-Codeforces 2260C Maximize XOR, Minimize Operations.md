---
title: "[Codeforces] #2260C - Maximize XOR, Minimize Operations [C++]"
date: 2026-09-09
categories: [PS, Codeforces]
tags: ["bit manipulation", "greedy"]
slug: codeforces-2260c
media_subpath: /assets/img/posts/codeforces-2260c/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2260/C)
{: .prompt-info }

---

## 1. 아이디어

`x`를 1 줄이고 `y`를 1 늘리는 연산을 몇 번이든 반복해 XOR을 최대화하고, 그중 연산 횟수가 최소인 경우를 찾아야 한다. 한쪽에서 줄어든 만큼 다른 쪽에 그대로 더해지므로 두 값의 합은 연산 전후로 항상 같다(`sum = x + y`). 합이 고정된 두 수의 XOR은 두 수가 겹치는 비트가 없을 때 최대가 되고 그 값은 `sum` 자신인데, 이 상태는 한쪽 값이 `sum`의 켜진 비트 중 일부만 고른 부분집합(서브마스크)일 때 성립한다. `0`은 항상 그런 서브마스크이고 연산이 도달 가능한 범위(`0`부터 `x`까지)에도 항상 포함되므로, 최댓값 `sum`은 어떤 입력에서도 달성 가능하다. 남은 문제는 그 서브마스크 중 `x` 이하이면서 가장 큰 값을 고르는 것인데, 클수록 거기까지 줄이는 연산 횟수가 줄어든다. 이는 `sum`의 비트를 높은 자리부터 훑으며 그 비트가 켜져 있고 지금까지 고른 값에 더해도 여전히 `x`를 넘지 않을 때만 채택하는 그리디로 구성할 수 있고, 최소 연산 횟수는 그렇게 고른 값을 `x`에서 뺀 만큼이다.

---

## 2. 복잡도

| 접근 | 시간   | 공간   |
| ---- | ------ | ------ |
| 풀이 | $O(T)$ | $O(1)$ |

($T$ = 테스트 케이스 수. 비트 탐색은 `x`, `y`의 크기와 무관하게 항상 30회 고정이라 케이스당 상수 시간)

---

## 3. 코드

### 풀이 [C++]

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    int x, y;
    cin >> x >> y;

    int sum = x + y;
    int res = 0;
    for (int b = 29; b >= 0; b--) {
        if ((sum & (1 << b)) && (res | (1 << b)) <= x) {
            res |= 1 << b;
        }
    }

    cout << sum << ' ' << x - res << '\n';
}

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);

    int t;
    cin >> t;
    while (t--) solve();
}
```

---
