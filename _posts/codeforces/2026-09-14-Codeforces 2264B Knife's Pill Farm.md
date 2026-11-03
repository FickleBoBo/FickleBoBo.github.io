---
title: "[Codeforces] #2264B - Knife's Pill Farm [C++]"
date: 2026-09-14
categories: [PS, Codeforces]
tags: ["data structure", "priority queue", "greedy", "math"]
slug: codeforces-2264b
media_subpath: /assets/img/posts/codeforces-2264b/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2264/B)
{: .prompt-info }

---

## 1. 아이디어

배열 $a$의 길이가 $m$인 부분수열 $b$를 골라 점수 $\sum_{i=1}^{m} i \cdot (b_i - b_{i-1})$을 최대로 만드는 문제다. 이를 $b_i$별로 묶으면 $b_0 = 0$이므로 $b_m$의 계수는 $m$이고 $1 \le i < m$인 $b_i$의 계수는 $i - (i + 1) = -1$이라, 점수는 $m \cdot b_m - (b_1 + \cdots + b_{m-1})$이다. 마지막으로 고르는 원소 $a_j$를 정하면 그 앞에서 $m - 1$개를 합이 가장 작게 고르면 되고 점수에는 합만 들어가 순서는 상관없으므로 $a_j$ 앞의 가장 작은 $m - 1$개를 쓰며, 이를 고를 수 있도록 $a_j$ 앞에 원소가 $m - 1$개 이상 있는 $j$만 후보가 된다. $j$를 오른쪽으로 옮기며 앞쪽의 가장 작은 $m - 1$개를 최대 힙으로 유지하면 새 원소가 힙의 최댓값보다 작을 때만 교체하면 되고, 이렇게 모든 $j$를 $O(n \log m)$에 훑는다.

---

## 2. 코드

### 풀이 [C++]

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n, m;
    cin >> n >> m;

    vector<int> a(n);
    for (int& x : a) cin >> x;

    priority_queue<int> pq;
    long long sum = 0;
    for (int i = 0; i < m - 1; i++) {
        pq.push(a[i]);
        sum += a[i];
    }

    long long ans = LLONG_MIN;
    for (int i = m - 1; i < n; i++) {
        ans = max(ans, 1LL * m * a[i] - sum);

        if (!pq.empty() && pq.top() > a[i]) {
            sum -= pq.top();
            pq.pop();
            sum += a[i];
            pq.push(a[i]);
        }
    }

    cout << ans << '\n';
}

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);

    int t;
    cin >> t;
    while (t--) solve();
}
```

`m * a[i]`가 약 $2 \cdot 10^{12}$까지 커져 `1LL`을 곱해 `long long`으로 계산했고, `m`이 1이면 힙이 비어 있어 `pq.empty()`를 먼저 확인했다.

---
