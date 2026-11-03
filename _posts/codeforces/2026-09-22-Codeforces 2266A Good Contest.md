---
title: "[Codeforces] #2266A - Good Contest [C++]"
date: 2026-09-22
categories: [PS, Codeforces]
tags: ["warm up"]
slug: codeforces-2266a
media_subpath: /assets/img/posts/codeforces-2266a/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2266/A)
{: .prompt-info }

---

## 1. 아이디어

세 문제의 풀이 인원이 주어질 때 세 문제를 모두 풀지 못한 참가자 수의 최솟값을 구하는 문제다. 세 문제를 모두 푼 참가자는 어느 문제의 풀이 인원보다도 많을 수 없어 $\min(a_1, a_2, a_3)$명 이하이고, 문제 $i$를 1번부터 $a_i$번 참가자가 풀었다고 하면 1번부터 $\min(a_1, a_2, a_3)$번 참가자가 세 문제를 모두 풀어 이 값을 달성할 수 있으므로, 답은 $n - \min(a_1, a_2, a_3)$이다.

---

## 2. 코드

### 풀이 [C++]

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n, a1, a2, a3;
    cin >> n >> a1 >> a2 >> a3;
    cout << n - min({a1, a2, a3}) << '\n';
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
