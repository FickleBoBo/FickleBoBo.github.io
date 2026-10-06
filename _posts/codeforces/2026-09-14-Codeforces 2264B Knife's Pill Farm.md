---
title: "[Codeforces] #2264B - Knife's Pill Farm [C++]"
date: 2026-09-14
categories: [PS, Codeforces]
tags: ["data structure", "priority queue", "greedy", "math"]
slug: codeforces-2264b
media_subpath: /assets/img/posts/codeforces-2264b/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2264/B)
{: .prompt-info }

---

## 1. 아이디어

길이 $m$인 부분수열 $b$를 골라 점수 $\sum\limits_{i=1}^{m} i \cdot (b_i - b_{i-1})$을 최대화하는 문제인데, 이 식을 전개해서 정리하면 $m \cdot b_m - \sum\limits_{i=1}^{m-1} b_i$만 남는다. 즉 마지막으로 고른 값만 계수 $m$으로 크게 기여하고 나머지 $m - 1$개는 위치와 무관하게 그냥 값의 합만 빼는 형태이므로, 어떤 원소를 마지막으로 정하든 그 앞에서 고를 나머지 $m - 1$개는 순서 조건이 자동으로 지켜지니 그냥 가장 작은 값들로 고르는 게 항상 최선이다.

그래서 왼쪽부터 훑으면서 지금까지 본 것 중 가장 작은 $m - 1$개의 합을 유지해두고, 매 위치를 마지막 원소 후보로 삼아 그 값을 $m$배한 값에서 유지해둔 합을 뺀 점수로 답을 갱신하면 된다. 이 가장 작은 $m - 1$개의 원소는 크기 $m - 1$짜리 최대 힙으로 유지하면, 새 값이 힙의 최댓값보다 작을 때만 교체하는 식으로 효율적으로 관리할 수 있다.

---

## 2. 복잡도

| 접근 | 시간          | 공간   |
| ---- | ------------- | ------ |
| 풀이 | $O(N \log M)$ | $O(N)$ |

($N$ = 모든 테스트 케이스에 걸친 `n`의 총합, $M$ = 케이스당 `m`의 최댓값)

---

## 3. 코드

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

---
