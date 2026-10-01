---
title: "[Codeforces] #2130B - Pathless [C++]"
date: 2026-10-01
categories: [PS, Codeforces]
tags: ["constructive"]
slug: codeforces-2130b
media_subpath: /assets/img/posts/codeforces-2130b/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2130/B)
{: .prompt-info }

---

## 1. 아이디어

`0`, `1`, `2`로 이루어진 배열을 재배치해서, 인덱스 1에서 `n`까지 한 칸씩 좌우로 움직이며 방문한 값의 합이 정확히 `s`가 되는 경로를 Alice가 못 찾게 만들 수 있는지 판정하는 문제다. 곧장 가는 경로의 합 `sum`(배열 전체의 합)이 가능한 최소이고, 다른 경로는 이웃한 두 칸을 왕복할 때마다 그 두 값의 합이 더해질 뿐이라 가능한 합은 `sum`에 이웃한 쌍의 합들을 몇 번이든 더한 값이다.

그래서 `s < sum`이면 어떻게 놓아도 Alice가 맞출 수 없고, `s = sum`이면 곧장 가는 경로로 항상 맞출 수 있다. `s > sum`이면 더해야 할 값 $d = s - \text{sum}$이 관건이다. $d = 1$은 합이 1인 이웃 쌍, 곧 `0`과 `1`이 붙어 있어야만 만들 수 있으므로, `0`을 앞에 모으고 그다음 `2`, 마지막에 `1`을 모으면 이웃 합이 0, 2, 3, 4뿐이라 막을 수 있다. 반면 $d \ge 2$는 어떻게 놓아도 막을 수 없다. `0`과 `1`이 붙어 있으면 $d = 1$ 자체가 가능해 모든 $d$를 만들 수 있고, 붙어 있지 않으면 `0`과 `1` 사이에 반드시 `2`가 끼어 합 2인 쌍(`0`과 `2`)과 합 3인 쌍(`2`와 `1`)이 모두 존재하는데, 2와 3을 몇 번이든 더하면 2 이상의 모든 정수가 나온다. 따라서 `s < sum`이거나 `s = sum + 1`일 때만 위 배치를 출력하고 나머지는 -1이다.

---

## 2. 복잡도

| 접근 | 시간   | 공간   |
| ---- | ------ | ------ |
| 풀이 | $O(N)$ | $O(1)$ |

($N$ = 전체 테스트 케이스에 걸친 배열 길이의 총합)

---

## 3. 코드

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
