---
title: "[Codeforces] #2148A - Sublime Sequence [C++]"
date: 2026-08-22
categories: [PS, Codeforces]
tags: ["warm up"]
description: "x, -x, x, -x, … 순으로 길이 n인 수열을 만든 뒤 전체 원소의 합을 구하는 워밍업 문제."
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

수열은 홀수 번째 항이 $X$, 짝수 번째 항이 $-X$로 채워진다. 인접한 두 항 $X$와 $-X$를 더하면 0이 되므로, 항을 앞에서부터 둘씩 묶으면 각 묶음의 합이 0이다. 따라서 $N$이 짝수면 모든 항이 짝을 이뤄 전체 합이 0이고, $N$이 홀수면 마지막 한 항 $X$만 짝 없이 남아 전체 합이 $X$다. 수열을 실제로 구성할 필요 없이 $N$의 홀짝만으로 답이 정해진다.

---

## 2. 복잡도

| 접근 | 시간   | 공간   |
| ---- | ------ | ------ |
| 풀이 | $O(1)$ | $O(1)$ |

---

## 3. 코드

### 풀이 [C++]

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    int x, n;
    cin >> x >> n;

    if (n % 2) {
        cout << x << '\n';
    } else {
        cout << 0 << '\n';
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
