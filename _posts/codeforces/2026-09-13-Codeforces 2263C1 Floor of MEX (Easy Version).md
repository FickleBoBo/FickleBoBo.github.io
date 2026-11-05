---
title: "[Codeforces] #2263C1 - Floor of MEX (Easy Version) [C++]"
date: 2026-09-13
categories: [PS, Codeforces]
tags: ["constructive", "difference array"]
slug: codeforces-2263c1
media_subpath: /assets/img/posts/codeforces-2263c1/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2263/C1)
{: .prompt-info }

---

## 1. 아이디어

집합 $S$와 양의 정수 $x$에 대해 $f(S, x)$는 $S$의 원소를 $x$로 나눈 몫들의 MEX다. 숨겨진 부분집합 $A \subseteq \lbrace 0, 1, \ldots, n - 1 \rbrace$로 $a_k = f(A, k)$ ($1 \le k \le n$)를 만든 배열 $a$만 주어질 때, 같은 배열을 만드는 부분집합 $B$를 하나 구하는 문제다.

$f(B, k) = a_k$는 두 조건으로 풀어 쓸 수 있다. $B$의 원소를 $k$로 나눈 몫에 $0, 1, \ldots, a_k - 1$이 모두 나와야 하고, $a_k$는 나오지 않아야 한다. 몫이 $a_k$인 수는 구간 $[k \cdot a_k, k \cdot (a_k + 1))$의 수이므로 뒤 조건은 $B$가 이 구간의 수를 하나도 갖지 않는다는 뜻이다. 이 구간을 금지 구간이라 하면 $k = 1, \ldots, n$마다 금지 구간이 하나씩 생긴다.

$\lbrace 0, 1, \ldots, n - 1 \rbrace$에서 어떤 금지 구간에도 걸리지 않는 수 전부를 $B$로 하면 뒤 조건은 만족한다. 지문이 어떤 $A$로 만든 배열만 주므로 $A$도 $a_k$인 몫을 만들지 않아 금지 구간을 전부 피하고 있고, 따라서 $A \subseteq B$다. $A$에서 이미 나오던 몫 $0, 1, \ldots, a_k - 1$은 수가 더해져도 그대로 나오므로 앞 조건도 유지되어, 모든 $k$에서 $f(B, k) = a_k$다.

금지 구간은 길이가 $k$라 하나씩 표시하면 $O(n^2)$까지 커질 수 있어 차분 배열로 $O(n)$에 표시한다.

---

## 2. 코드

### 풀이 [C++]

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n;
    cin >> n;

    vector<int> diff(n + 1);
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;

        diff[min(n, (i + 1) * x)]++;
        diff[min(n, (i + 1) * (x + 1))]--;
    }

    for (int i = 1; i <= n; i++) {
        diff[i] += diff[i - 1];
    }

    int cnt = count(diff.begin(), diff.end() - 1, 0);
    cout << cnt << '\n';
    if (cnt) {
        for (int i = 0; i < n; i++) {
            if (diff[i] == 0) cout << i << ' ';
        }
        cout << '\n';
    }
}

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);

    int t;
    cin >> t;
    while (t--) solve();
}
```

금지 구간의 끝 `(i + 1) * (x + 1)`은 입력 범위만 보면 `int`를 넘을 듯하지만, 지문이 보장하는 배열에서는 `x`가 몫 집합의 MEX라 `(n - 1) / (i + 1) + 1`을 넘지 못한다. 그래서 `(i + 1) * (x + 1)`은 `(n - 1) + 2 * (i + 1)`을 넘지 못해 `n`의 3배 미만이므로 `int`로 충분했다. 배열 크기를 넘는 끝은 `std::min(n, ...)`으로 `n`에 맞췄다.

`diff`는 길이를 `n + 1`로 잡아 인덱스 `n`을 넘친 구간을 버리는 칸으로 썼고, 그래서 `std::count`는 `diff.end() - 1`까지만 세었다.

---
