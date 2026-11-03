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

$\lbrace 0, 1, \ldots, n - 1 \rbrace$의 어떤 부분집합 $A$의 원소를 $k$로 나눈 몫들의 MEX를 $a_k$로 하여 만든 배열 $a$가 주어질 때, 같은 배열을 만드는 부분집합 $B$를 하나 구하는 문제다. $f(B, k) = a_k$는 $B$의 원소를 $k$로 나눈 몫 중 $a_k$ 미만은 모두 나오고 $a_k$는 나오지 않는다는 뜻이고, 나오지 않으려면 $B$가 구간 $[k \cdot a_k, k \cdot (a_k + 1))$의 수를 하나도 갖지 않아야 한다. 이 금지 구간을 모든 $k$에 대해 모으면 $B$가 피해야 할 수가 정해지는데, 지문이 어떤 $A$로 만든 배열만 주므로 그 $A$는 금지 구간을 전부 피하면서 필요한 몫을 모두 만들고 있다. 그래서 $\lbrace 0, 1, \ldots, n - 1 \rbrace$에서 금지 구간에 걸리지 않는 수를 전부 담은 집합을 $B$로 하면 $A$를 포함하므로 필요한 몫이 그대로 나오고, 더해진 수는 어느 $k$에서도 $a_k$인 몫을 만들지 못하므로 $f(B, k) = a_k$가 유지된다. 금지 구간은 길이가 $k$라 하나씩 표시하면 $O(n^2)$까지 커질 수 있어 차분 배열로 $O(n)$에 표시한다.

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

금지 구간의 끝 `(i + 1) * (x + 1)`은 입력 범위만 보면 `int`를 넘을 듯하지만, `x`가 몫 집합의 MEX라 `(n - 1) / (i + 1) + 1`을 넘지 못하고 그래서 `(i + 1) * (x + 1)`이 `(n - 1) + 2 * (i + 1)`을 넘지 못하므로, `n`의 3배 미만이어서 `int`로 충분했다. 배열 크기를 넘는 끝은 `std::min(n, ...)`으로 `n`에 맞췄다. `diff`는 길이를 `n + 1`로 잡아 인덱스 `n`을 넘친 구간을 버리는 칸으로 썼고, 그래서 `std::count`는 `diff.end() - 1`까지만 세었다.

---
