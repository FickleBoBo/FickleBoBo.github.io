---
title: "[Codeforces] #2148A - Sublime Sequence [C++]"
date: 2026-08-22
categories: [PS, Codeforces]
tags: ["warm up"]
slug: codeforces-2148a
media_subpath: /assets/img/posts/codeforces-2148a/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2148/A)
{: .prompt-info }

---

## 1. 아이디어

$x$로 시작하며 $x$와 $-x$가 번갈아 등장하는 길이 $n$짜리 수열의 합을 구하는 문제다. 인접한 두 항의 합이 $(x) + (-x) = 0$이 된다는 점에서 $n$이 홀수면 마지막 항을 제외한 나머지 항의 합이 0이 되어 모든 항의 합이 $x$가 되고, 짝수면 모든 항의 합이 $0$이 된다.

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
    int x, n;
    cin >> x >> n;
    cout << (n % 2 ? x : 0) << '\n';
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
