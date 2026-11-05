---
title: "[Codeforces] #2148A - Sublime Sequence [C++]"
date: 2026-11-05
categories: [PS, Codeforces]
tags: ["math"]
slug: codeforces-2148a
media_subpath: /assets/img/posts/codeforces-2148a/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2148/A)
{: .prompt-info }

---

## 1. 아이디어

$x$와 $-x$를 $x$부터 번갈아 놓은 길이 $n$의 수열의 합을 구하는 문제로, 이웃한 $x$와 $-x$는 합이 0이므로 앞에서부터 두 항씩 묶으면 $n$이 짝수일 때 전부 상쇄되어 합이 0이고, $n$이 홀수일 때는 묶고 남은 마지막 항 $x$ 하나가 합이 된다.

---

## 2. 코드

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
