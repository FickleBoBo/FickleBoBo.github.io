---
title: "[Codeforces] #2266B - Three Piles [C++]"
date: 2026-09-22
categories: [PS, Codeforces]
tags: ["math", "game theory"]
slug: codeforces-2266b
media_subpath: /assets/img/posts/codeforces-2266b/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2266/B)
{: .prompt-info }

---

## 1. 아이디어

Alice가 $a$개, Bob이 $b$개, 가운데 더미에 $c$개의 돌이 있을 때 둘이 번갈아 가운데 더미에서 돌을 가져와 자기 더미에 더하며 Alice는 두 사람의 돌 수 차이를 크게 하고 Bob은 작게 하려는 게임의 최종 차이를 구하는 문제다.

Bob이 매번 0개를 가져가면 Alice가 가져가는 총량 $y$($0 \le y \le c$)에 대해 최종 차이는 $\lvert a + y - b \rvert$이고, 이는 $y$에 대해 볼록해서 양 끝인 $\lvert a - b \rvert$와 $\lvert a + c - b \rvert$ 중 큰 쪽을 넘지 못하므로, Bob이 이 전략으로 차이를 그 큰 쪽 이하로 만들 수 있어 답도 그 이하이다.

반대로 Alice가 첫 턴에 전부 가져가면 Bob이 더 가져갈 돌이 없어 차이가 $\lvert a + c - b \rvert$로 정해지고, $a < b$일 때는 Alice가 계속 0개를 가져가면 Bob이 가져가는 돌은 Bob의 더미만 키워 차이가 $b - a$ 아래로 내려가지 않으므로 $\lvert a - b \rvert$도 보장된다. $a \ge b$이면 $a + c - b \ge \lvert a - b \rvert$라 앞의 것만으로 충분해서, 어느 경우든 답은 $\max(\lvert a + c - b \rvert, \lvert a - b \rvert)$이다.

---

## 2. 코드

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

지문이 64비트 정수형을 쓰라고 요구해 `long long`으로 받았다.

---
