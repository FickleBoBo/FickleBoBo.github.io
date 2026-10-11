---
title: "[Codeforces] #2275C - Unrequited Love [C++]"
date: 2026-10-11
categories: [PS, Codeforces]
tags: ["data structure", "hash table", "math", "combinatorics"]
slug: codeforces-2275c
media_subpath: /assets/img/posts/codeforces-2275c/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2275/C)
{: .prompt-info }

---

## 1. 아이디어

건반 $x$, $x + 2$, $x + 4$를 동시에 눌러 $a_x + a_{x + 2} - a_{x + 4}$만큼의 값을 얻는 삼화음 중, 건반이 겹치지 않으면서 값이 같은 두 삼화음을 고르는 경우의 수를 세는 문제다.

시작 위치 `i`인 삼화음의 값을 `b[i] = a[i] + a[i + 2] - a[i + 4]`라 하면, 삼화음이 쓰는 건반은 시작 위치와 홀짝이 같아 시작 위치의 차가 홀수이면 겹칠 수 없고, 차가 6 이상이어도 건반의 범위가 떨어져 있으므로 겹치는 경우는 차가 2 또는 4일 때뿐이다. 따라서 `b`에서 값이 같은 모든 쌍의 수를 구한 뒤, 차가 2인 쌍과 4인 쌍은 서로 다른 쌍이므로 각각 값이 같은 쌍을 한 번씩 빼면 된다. 값이 같은 쌍은 값별 개수 $v$를 해시맵으로 세어 $v(v - 1) / 2$를 더했다.

---

## 2. 복잡도

| 접근 | 시간   | 공간   |
| ---- | ------ | ------ |
| 풀이 | $O(N)$ | $O(N)$ |

($N$ = 모든 테스트 케이스에 걸친 `n`의 총합)

---

## 3. 코드

### 풀이 [C++]

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n;
    cin >> n;

    vector<int> a(n);
    for (int& x : a) cin >> x;

    int m = n - 4;
    vector<int> b(m);
    for (int i = 0; i < m; i++) b[i] = a[i] + a[i + 2] - a[i + 4];

    unordered_map<int, long long> cnt;
    for (int x : b) cnt[x]++;

    long long ans = 0;
    for (auto [_, v] : cnt) ans += v * (v - 1) / 2;
    for (int i = 0; i + 2 < m; i++) ans -= b[i] == b[i + 2];
    for (int i = 0; i + 4 < m; i++) ans -= b[i] == b[i + 4];

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
