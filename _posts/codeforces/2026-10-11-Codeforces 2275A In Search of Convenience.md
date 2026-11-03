---
title: "[Codeforces] #2275A - In Search of Convenience [C++]"
date: 2026-10-11
categories: [PS, Codeforces]
tags: ["constructive", "geometry"]
slug: codeforces-2275a
media_subpath: /assets/img/posts/codeforces-2275a/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2275/A)
{: .prompt-info }

---

## 1. 아이디어

라우터에서 정확히 $R$만큼 떨어진 격자점 하나를 찾는 문제다. 한 축으로만 $R$ 떨어진 점은 거리가 정확히 $R$이므로, 제곱의 합이 $R^2$이 되는 두 정수를 찾을 필요 없이 $(x_0, y_0 + R)$을 출력하면 된다.

---

## 2. 코드

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
