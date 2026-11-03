---
title: "[Codeforces] #2275C - Unrequited Love [C++]"
date: 2026-10-11
categories: [PS, Codeforces]
tags: ["data structure", "hash set/map", "math", "combinatorics"]
slug: codeforces-2275c
media_subpath: /assets/img/posts/codeforces-2275c/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2275/C)
{: .prompt-info }

---

## 1. 아이디어

건반 $n$개에서 $x$, $x + 2$, $x + 4$번 건반을 한꺼번에 누르는 삼화음 두 개를 골라, 건반을 공유하지 않으면서 가치가 같은 쌍의 수를 세는 문제다. 시작 위치 $x$인 삼화음의 가치를 $b_x = a_x + a_{x+2} - a_{x+4}$라 하면, 시작 위치가 $x < y$인 두 삼화음이 건반을 공유하는 경우는 $y - x$가 2나 4일 때뿐이다(차이가 홀수이면 건반의 홀짝이 달라 겹치지 않고, 6 이상이면 두 번째 삼화음의 첫 건반 $y$가 $x + 4$보다 크다). 그래서 $b$ 값이 같은 위치 쌍을 전부 센 뒤 $b_x = b_{x+2}$인 쌍과 $b_x = b_{x+4}$인 쌍을 빼면 된다. $n \le 2 \cdot 10^5$이라 삼화음 쌍을 하나씩 비교하면 $O(n^2)$이어서 느리므로 값이 같은 쌍은 값별 개수 $v$로 $v(v - 1) / 2$개씩 모아 세고, 뺄 쌍은 위치 차이가 2와 4인 경우만 직접 훑는다.

---

## 2. 코드

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

같은 가치의 삼화음이 모두 몰리면 쌍의 수가 $2 \cdot 10^{10}$ 가까이 되어 `int`로는 넘치므로 `cnt`의 값과 `ans`를 `long long`으로 두었다.

---
