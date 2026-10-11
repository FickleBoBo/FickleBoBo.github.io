---
title: "[Codeforces] #2275D - Precision Alignment [C++]"
date: 2026-10-11
categories: [PS, Codeforces]
tags: ["ad hoc", "binary search", "parametric search"]
slug: codeforces-2275d
media_subpath: /assets/img/posts/codeforces-2275d/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2275/D)
{: .prompt-info }

---

## 1. 아이디어

각 실험실의 세 값의 합 $a_i + b_i + c_i$ 중 최솟값 $S$를, 조정을 최대 `k`번 해서 최대로 만드는 문제다.

조정 한 번은 합을 최대 1만 바꾸므로 목표 $S$가 정해지면 합이 $S$ 미만인 실험실마다 필요한 조정 횟수를 더해 `k` 이하인지 확인하면 되고, $S$가 커질수록 필요한 횟수가 늘기만 하므로 $S$를 매개변수 이분 탐색으로 구했다. 실험실 하나에 필요한 횟수는 $S$까지 올릴 양에 막힌 상태를 벗어나는 비용을 더한 값인데, $a_i \le b_i \le c_i$이면 세 조정이 모두 합을 줄이거나 그대로 두는 막힌 상태이고 여기서 벗어나려면 $b_i$를 $a_i$ 아래로 내리거나 $c_i$를 $b_i$ 아래로 내려 이웃한 두 값의 순서를 뒤집어야 한다. 한 번에 1씩만 바뀌므로 가까운 쪽의 간격 $d = \min(b_i - a_i, c_i - b_i)$에 대해 $d + 1$번이 들고 그동안 합이 $d + 1$ 줄지만, 뒤집힌 뒤에는 한 값이 계속 올라 조정마다 합이 1씩 늘어나므로 줄어든 만큼을 되찾는 데 $d + 1$번이 더 들어 벗어나는 비용은 $2(d + 1)$이다. 막힌 상태가 아니면 이 비용이 없고 세 값이 모두 같으면 어떤 조정도 값을 바꾸지 못해 합을 올릴 수 없으므로, 결국 실험실마다 이 비용을 계산해 이분 탐색으로 최대 $S$를 찾으면 된다.

---

## 2. 복잡도

| 접근 | 시간          | 공간   |
| ---- | ------------- | ------ |
| 풀이 | $O(N \log K)$ | $O(N)$ |

($N$ = 모든 테스트 케이스에 걸친 `n`의 총합, $K$ = 케이스당 `k`의 최댓값)

---

## 3. 코드

### 풀이 [C++]

```c++
#include <bits/stdc++.h>
using namespace std;

const long long INF = 1'000'000'000'000'000'000;

long long upper_bound_param(int n, long long k, vector<long long>& sum, vector<long long>& cost) {
    long long lo = *min_element(sum.begin(), sum.end());
    long long hi = lo + k + 1;
    while (lo < hi) {
        long long mid = lo + (hi - lo) / 2;

        long long need = 0;
        for (int i = 0; i < n && need <= k; i++) {
            if (sum[i] < mid) need += cost[i] + (mid - sum[i]);
        }

        if (need <= k) {
            lo = mid + 1;
        } else {
            hi = mid;
        }
    }

    return lo;
}

void solve() {
    int n;
    long long k;
    cin >> n >> k;

    vector<long long> sum(n), cost(n);
    for (int i = 0; i < n; i++) {
        long long a, b, c;
        cin >> a >> b >> c;

        sum[i] = a + b + c;
        if (a == b && b == c) {
            cost[i] = INF;
        } else if (a <= b && b <= c) {
            cost[i] = 2 * (min(b - a, c - b) + 1);
        }
    }

    cout << upper_bound_param(n, k, sum, cost) - 1 << '\n';
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
