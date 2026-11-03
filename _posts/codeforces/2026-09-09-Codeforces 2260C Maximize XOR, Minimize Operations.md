---
title: "[Codeforces] #2260C - Maximize XOR, Minimize Operations [C++]"
date: 2026-09-09
categories: [PS, Codeforces]
tags: ["bit manipulation", "greedy"]
slug: codeforces-2260c
media_subpath: /assets/img/posts/codeforces-2260c/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2260/C)
{: .prompt-info }

---

## 1. 아이디어

연산은 $x$를 1 줄이고 $y$를 1 늘리므로 합 $s = x + y$가 연산 횟수와 무관하게 일정하고, 이 일정한 합 아래에서 $x \oplus y$를 최대로 만들고 그중 연산 횟수가 가장 적은 것을 찾는 문제다. 연산을 $t$번 한 뒤의 두 수를 $a = x - t$, $b = y + t$라 하면 $a + b = s$는 $a \oplus b$에 두 수가 공통으로 켜진 비트 값의 두 배를 더한 값이므로 $a \oplus b$는 $s$ 이하이고, 공통으로 켜진 비트가 없을 때만 $s$와 같다. $t = x$로 $a = 0$을 만들면 이 조건을 만족하므로 최댓값은 항상 $x + y$이다. 겹치는 비트가 없으면 덧셈에서 올림이 생기지 않아 $a$와 $b$가 $s$의 켜진 비트를 나눠 가진 꼴이고, 반대로 $s$의 서브마스크, 곧 $s$의 켜진 비트 일부로만 만든 $a$는 $b = s - a$와 겹치지 않으므로, 연산 횟수 $t = x - a$는 0 이상이니 $a$는 $x$ 이하여야 하고, $t$를 최소로 하려면 $s$의 서브마스크 중 그 조건을 만족하는 가장 큰 $a$를 찾으면 된다. 높은 비트 하나가 그보다 낮은 비트를 전부 합친 값보다 크므로, 높은 비트부터 지금까지 고른 값에 더해도 $x$를 넘지 않을 때만 고르는 탐욕으로 구한다.

---

## 2. 코드

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

`x`, `y`가 $2^{29}$ 미만이라 합은 $2^{30}$ 미만이므로 29번 비트까지 켜질 수 있어 29번 비트부터 훑었다.

---
