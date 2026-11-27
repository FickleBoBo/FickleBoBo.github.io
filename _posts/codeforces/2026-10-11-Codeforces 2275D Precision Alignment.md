---
title: "[Codeforces] #2275D - Precision Alignment [C++]"
date: 2026-10-11
categories: [PS, Codeforces]
tags: ["binary search", "parametric search"]
slug: codeforces-2275d
media_subpath: /assets/img/posts/codeforces-2275d/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2275/D)
{: .prompt-info }

---

## 1. 아이디어

실험실마다 합 $a_i + b_i + c_i$가 있고, 연산을 최대 $k$번 해서 합의 최솟값 $S$를 최대로 만드는 문제다.

연산 하나는 값 하나를 1만 바꾸므로 합이 1을 넘게 늘지 않고, 실험실끼리 서로 영향을 주지 않는다. 그래서 $S$를 정하면 합이 $S$ 미만인 실험실마다 합을 $S$까지 올리는 최소 연산 횟수를 구해 더하고, 그 합이 $k$ 이하인지로 가능 여부가 갈린다. $S$가 클수록 필요한 횟수가 늘어 이 판정이 단조이므로, 이분 탐색으로 최대 $S$를 구한다. 남은 일은 실험실 하나의 합을 $d$ 올리는 최소 비용이다.

$a_i > b_i$이면 $c_i$가, $b_i > c_i$이면 $a_i$가 연산마다 1씩 올라 연산을 해도 이 조건이 그대로 유지되므로, 합을 $d$ 올리는 데 $d$번이 든다.

이 두 경우가 아니면 $a_i \le b_i \le c_i$이고, 세 연산이 더하는 값이 모두 0 이하라 어떤 연산도 합을 늘리지 못한다. 세 값이 모두 같으면 값이 아예 바뀌지 않아 합을 올릴 수 없다.

그렇지 않으면 합을 깎더라도 $b_i < a_i$이거나 $c_i < b_i$인 상태로 먼저 빠져나와야 한다. 앞의 것은 $b_i$를 $b_i - a_i + 1$번, 뒤의 것은 $c_i$를 $c_i - b_i + 1$번 내려야 만들어진다. $b_i$를 내리는 연산은 $c_i - b_i$를 키우고 $c_i$를 내리는 연산은 $b_i - a_i$를 건드리지 않으며, $a_i$를 내리는 연산은 어느 쪽도 돕지 않아 둘은 서로 도와주지 않으므로 적은 쪽인 $m = \min(b_i - a_i, c_i - b_i) + 1$번이 최소이다($a_i = b_i$이면 $c_i$는 내려가지 않지만 이때 $m = 1$이라 $b_i$ 쪽이 최소이다).

내릴 때마다 합이 정확히 1씩 깎이고 합을 안 바꾸는 연산은 쓸 이유가 없으므로, 깎인 합을 되찾는 데 다시 $m$번이 들어 $2m$번 뒤에야 원래 합이 되고 그다음부터 연산마다 1씩 오른다. 따라서 합을 $d$ 올리는 비용은 $d$에 $2m$을 더한 값이다.

---

## 2. 코드

### 풀이 [C++]

```c++
#include <bits/stdc++.h>
using namespace std;

const long long INF = 1'000'000'000'000'000'000;

long long upperBound(int n, long long k, vector<long long>& sum, vector<long long>& cost) {
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

    cout << upperBound(n, k, sum, cost) - 1 << '\n';
}

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);

    int t;
    cin >> t;
    while (t--) solve();
}
```

`cost`는 0으로 시작해 `a > b`이거나 `b > c`인 실험실은 시작 비용이 없고, 값이 모두 같은 실험실은 $10^{18}$로 두되 `need`가 `k`를 넘는 즉시 반복을 멈춰 `long long`이 넘치지 않게 했다. 탐색은 가능한 마지막 $S$의 다음 값에서 끝나므로 출력에서 1을 뺐다.

---
