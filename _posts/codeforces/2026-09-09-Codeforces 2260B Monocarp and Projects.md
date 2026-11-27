---
title: "[Codeforces] #2260B - Monocarp and Projects [C++]"
date: 2026-09-09
categories: [PS, Codeforces]
tags: ["math", "number theory"]
slug: codeforces-2260b
media_subpath: /assets/img/posts/codeforces-2260b/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2260/B)
{: .prompt-info }

---

## 1. 아이디어

달 $i$($0 \le i < k$)에 직원이 $x + i$명, 프로젝트가 $y + i$개일 때 Monocarp가 직접 하는 프로젝트 수는 프로젝트 수를 직원 수로 나눈 나머지이므로 $k$달 동안의 나머지 합을 구하는 문제이고, $k$가 $10^{12}$까지라 달마다 계산할 수는 없다.

프로젝트는 직원보다 항상 $d = y - x$개 많으므로 $(y + i) \bmod (x + i)$는 $d \bmod (x + i)$와 같고, 직원 수 $x + i$가 $d$보다 커지면 이 값은 $d$ 그대로다.

$x + i \le d$인 달은 많아야 $y$개이고 $y$의 합이 $10^6$ 이하라 하나씩 더해도 충분하며, 그 뒤 남은 달은 전부 $d$씩이라 $d \cdot (k - i)$로 한 번에 더한다.

---

## 2. 코드

### 풀이 [C++]

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    long long x, y, k;
    cin >> x >> y >> k;

    long long diff = y - x;
    long long sum = 0;

    long long i = 0;
    for (; i < k && x + i <= diff; i++) {
        sum += diff % (x + i);
    }
    sum += diff * (k - i);

    cout << sum << '\n';
}

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);

    int t;
    cin >> t;
    while (t--) solve();
}
```

`diff * (k - i)`가 $10^{18}$에 가까워질 수 있어 `int`로는 넘치므로 모든 변수를 `long long`으로 받았다.

---
