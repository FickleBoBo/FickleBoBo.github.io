---
title: "[Codeforces] #2266A - Good Contest [C++]"
date: 2026-09-22
categories: [PS, Codeforces]
tags: ["warm up"]
slug: codeforces-2266a
media_subpath: /assets/img/posts/codeforces-2266a/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2266/A)
{: .prompt-info }

---

## 1. 아이디어

`n`명의 참가자와 세 문제가 있고, 각 문제를 푼 참가자 수가 `a1`, `a2`, `a3`로 주어질 때 세 문제를 모두 풀지 못한 약한 참가자 수의 최솟값을 구하는 문제다. 세 문제를 모두 풀지 못한 약한 참가자의 수는 전체 참가자 수에서 세 문제를 모두 푼 참가자 수의 최댓값을 빼는 것으로도 구할 수 있는데, 세 문제를 모두 푼 참가자 수의 최댓값은 `a1`, `a2`, `a3`의 교집합의 최댓값과 같고 이는 세 값의 최솟값이 된다.

---

## 2. 복잡도

| 접근 | 시간   | 공간   |
| ---- | ------ | ------ |
| 풀이 | $O(T)$ | $O(1)$ |

($T$ = 테스트 케이스 수)

---

## 3. 코드

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
