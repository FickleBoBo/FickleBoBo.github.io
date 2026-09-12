---
title: "[Codeforces] #2260B - Monocarp and Projects [C++]"
date: 2026-09-09
categories: [PS, Codeforces]
tags: ["brute force", "math", "number theory"]
slug: codeforces-2260b
media_subpath: /assets/img/posts/codeforces-2260b/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2260/B)
{: .prompt-info }

---

## 1. 아이디어

각 달마다 직원 수와 프로젝트 수가 함께 1씩 늘어나는 `k`개월 동안 Monocarp가 직접 처리하는 프로젝트 수의 총합을 구해야 한다. `i`번째 달엔 직원이 `x + i`명, 프로젝트가 `y + i`개이므로 그 달 Monocarp가 처리하는 양은 `y + i`를 `x + i`로 나눈 나머지다. `d = y - x`는 매달 그대로 유지되는 값이라, 이 나머지는 `d`를 `x + i`로 나눈 나머지와 같다(나누는 수 자신을 더해도 나머지는 바뀌지 않으므로). 그리고 `x + i`가 `d`를 넘어서는 순간부터는 그 나머지가 `d` 그대로 굳어지므로, 실제로 나눗셈이 필요한 구간은 `x + i`가 `d` 이하인 최대 `d - x + 1`번뿐이고 그 뒤 남은 달들은 `d`를 그대로 더하면 된다.

---

## 2. 복잡도

| 접근 | 시간   | 공간   |
| ---- | ------ | ------ |
| 풀이 | $O(Y)$ | $O(1)$ |

($Y$ = 모든 테스트 케이스에 걸친 `y`의 총합)

---

## 3. 코드

### 풀이 [C++]

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    long long x, y, k;
    cin >> x >> y >> k;

    long long d = y - x;
    long long sum = 0;

    long long i = 0;
    for (; i < k && x + i <= d; i++) {
        sum += d % (x + i);
    }
    sum += d * (k - i);

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

---
