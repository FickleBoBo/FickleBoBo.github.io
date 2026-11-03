---
title: "[Codeforces] #2259E - Treasure Map Destruction (Constructive Version) [C++]"
date: 2026-09-06
categories: [PS, Codeforces]
tags: ["constructive", "difference array"]
slug: codeforces-2259e
media_subpath: /assets/img/posts/codeforces-2259e/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2259/E)
{: .prompt-info }

---

## 1. 아이디어

섬마다 가장 가까운 보물섬까지의 거리를 적은 지도가 일부 `-1`로 지워졌을 때, 남은 거리와 모순이 없는 보물 배치를 하나 찾는 문제다. 거리 $b_i > 0$이 적힌 섬 $i$는 $i$에서 거리가 $b_i$ 미만인 구간 $[i - b_i + 1, i + b_i - 1]$(이하 금지 구간)에 보물이 없어야 하고 정확히 $b_i$만큼 떨어진 $i - b_i$ 또는 $i + b_i$(섬 범위 밖이면 제외) 중 한 곳에는 보물이 있어야 하며, $b_i = 0$이면 $i$ 자체에 보물이 있어야 한다. 보물이 없어야 한다는 조건은 보물을 줄이는 쪽이고 있어야 한다는 조건은 늘리는 쪽이므로, 어떤 섬의 금지 구간에도 걸리지 않는 섬 전부에 보물을 놓은 배치가 없어야 한다는 조건을 지키는 배치 중 가장 많다. 유효한 배치는 모두 이 배치의 부분집합이고 이 배치에서도 있어야 한다는 조건은 그대로 유지되므로 이 배치 하나만 검사하면 된다. $b_i = 0$인데 금지 구간에 걸린 섬이 있거나 $b_i > 0$인데 $i - b_i$와 $i + b_i$ 모두 보물이 없는 섬이 있으면 유효한 배치가 없는 것이다. 지워지지 않은 거리가 있으면 그 섬에 대한 검사가 보물의 존재를 요구하고 전부 지워졌으면 모든 섬이 보물이라, 어느 쪽이든 이 배치에는 보물이 적어도 한 곳 있다. $n \le 2 \cdot 10^5$이라 금지 구간을 하나씩 칠하면 $O(n^2)$이 되므로 차분 배열로 구간을 한꺼번에 표시한다.

---

## 2. 코드

### 풀이 [C++]

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n;
    cin >> n;

    vector<int> b(n);
    for (int& x : b) cin >> x;

    vector<int> diff(n + 1);
    for (int i = 0; i < n; i++) {
        if (b[i] > 0) {
            diff[max(i - b[i] + 1, 0)]++;
            diff[min(i + b[i], n)]--;
        }
    }
    for (int i = 1; i <= n; i++) {
        diff[i] += diff[i - 1];
    }

    string ans(n, '0');
    for (int i = 0; i < n; i++) {
        if (diff[i] == 0) ans[i] = '1';
    }

    for (int i = 0; i < n; i++) {
        if (b[i] == 0 && ans[i] == '0') {
            cout << -1 << '\n';
            return;
        }
    }

    for (int i = 0; i < n; i++) {
        if (b[i] <= 0) continue;
        int l = i - b[i], r = i + b[i];
        if (!((l >= 0 && ans[l] == '1') || (r < n && ans[r] == '1'))) {
            cout << -1 << '\n';
            return;
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
