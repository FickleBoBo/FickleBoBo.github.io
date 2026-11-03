---
title: "[Codeforces] #2130B - Pathless [C++]"
date: 2026-10-01
categories: [PS, Codeforces]
tags: ["constructive", "math"]
slug: codeforces-2130b
media_subpath: /assets/img/posts/codeforces-2130b/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2130/B)
{: .prompt-info }

---

## 1. 아이디어

Bob이 `0`, `1`, `2`로 된 배열을 재배열해 Alice가 1번 칸에서 $n$번 칸까지 이웃한 칸으로만 걸어 합이 정확히 $s$가 되는 경로를 못 찾게 만들 수 있는지 판정하고, 가능하면 그 배열을 출력하는 문제다. 경로의 합은 시작 칸의 값 $a_1$에서 출발해 이웃한 두 칸 사이를 오른쪽으로 건널 때는 오른쪽 칸의 값을, 왼쪽으로 건널 때는 왼쪽 칸의 값을 더한 것이다. 1번 칸에서 $n$번 칸으로 가려면 각 이웃 쌍 $(e, e + 1)$을 오른쪽으로 건너는 횟수가 왼쪽으로 건너는 횟수보다 정확히 하나 많아 모든 쌍을 홀수 번 건너고, 모든 쌍을 정확히 한 번씩만 건너는 직진 경로의 합이 배열 전체의 합 $T$이다. 이웃 쌍마다 독립적으로 두 번 더 건너는 왕복을 끼워 넣을 수 있고 이 왕복은 오른쪽 건넘에서 오른쪽 칸을, 왼쪽 건넘에서 왼쪽 칸을 더해 $a_e + a_{e+1}$만큼 합을 늘리므로, 이웃 쌍 $e$를 왕복하는 횟수를 $c_e \ge 0$이라 하면 가능한 합은 정확히 $T + \sum_{e=1}^{n-1} c_e \cdot (a_e + a_{e+1})$이다.

그래서 $s < T$이면 어떻게 늘어놓아도 막을 수 있고 $s = T$이면 곧장 걷는 경로를 막을 수 없으며, $s > T$이면 이웃한 두 값의 합으로 $s - T$를 만들 수 있는지가 관건이다. 합이 1인 이웃(`0`과 `1`)이 있으면 어떤 $s - T$도 만들 수 있다. 없으면 지문이 `0`, `1`, `2`가 모두 있음을 보장하므로 `0`이 이어진 덩어리 바깥에 이웃이 있고 그것은 `1`일 수 없어 `2`이며, `1`이 이어진 덩어리 바깥의 이웃도 마찬가지로 `2`라 합 2와 3이 반드시 생기고, 2와 3의 조합으로 2 이상은 모두 만들 수 있어 $s - T \ge 2$는 어떤 배열로도 막지 못한다. 그러니 $s > T$에서 막을 수 있는 경우는 $s - T = 1$ 하나뿐이고, `0`, `2`, `1` 순으로 모아 놓으면 이웃한 두 값의 합이 0+0, 0+2, 2+2, 2+1, 1+1 곧 0, 2, 3, 4뿐이라 1을 만들 수 없어 막힌다. 따라서 $s < T$이거나 $s = T + 1$일 때만 Bob이 막을 수 있다.

---

## 2. 코드

### 풀이 [C++]

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n, s;
    cin >> n >> s;

    vector<int> cnt(3);
    while (n--) {
        int x;
        cin >> x;
        cnt[x]++;
    }

    int sum = cnt[1] + cnt[2] * 2;
    if (sum > s || sum == s - 1) {
        while (cnt[0]--) cout << 0 << ' ';
        while (cnt[2]--) cout << 2 << ' ';
        while (cnt[1]--) cout << 1 << ' ';
        cout << '\n';
    } else {
        cout << -1 << '\n';
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

---
