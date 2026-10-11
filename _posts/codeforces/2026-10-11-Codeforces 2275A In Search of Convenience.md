---
title: "[Codeforces] #2275A - In Search of Convenience [C++]"
date: 2026-10-11
categories: [PS, Codeforces]
tags: ["constructive", "geometry"]
slug: codeforces-2275a
media_subpath: /assets/img/posts/codeforces-2275a/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2275/A)
{: .prompt-info }

---

## 1. 아이디어

라우터 $(x_0, y_0)$에서 정확히 거리 $R$만큼 떨어진 정수 좌표를 아무거나 하나 구하는 문제다. $x$ 좌표는 같고 $y$ 좌표만 $R$ 차이 나는 $(x_0, y_0 + R)$은 거리가 정확히 $R$이면서 정수 좌표이므로 항상 조건을 만족한다.

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
    int x, y, r;
    cin >> x >> y >> r;
    cout << x << ' ' << y + r << '\n';
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
