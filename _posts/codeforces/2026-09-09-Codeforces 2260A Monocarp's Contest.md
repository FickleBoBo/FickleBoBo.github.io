---
title: "[Codeforces] #2260A - Monocarp's Contest [C++]"
date: 2026-09-09
categories: [PS, Codeforces]
tags: ["warm up"]
slug: codeforces-2260a
media_subpath: /assets/img/posts/codeforces-2260a/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2260/A)
{: .prompt-info }

---

## 1. 아이디어

`n`개의 문제들이 주어지며 각 문제는 쉬우면 `0`, 어려우면 `1`로 표현된다. 이때 두 문제의 위치를 변경할 수 있을 때 첫 번째 문제와 마지막 문제에 쉬운 문제를 두기 위한 최소 연산 횟수를 구해야 한다. 첫 번째 문제와 마지막 문제가 쉬운 문제인지 어려운 문제인지를 구하고 그 사이 문제들 중 쉬운 문제의 수를 구해 조건 분기로 해결했는데, 첫 번째 문제와 마지막 문제의 합이 어려운 문제의 수가 되며 이 값이 중간에 위치한 쉬운 문제들 보다 많으면 어떻게 스왑해도 불가능하며, 적거나 같은 경우 해당 수만큼 스왑하면 된다.

---

## 2. 복잡도

| 접근 | 시간            | 공간   |
| ---- | --------------- | ------ |
| 풀이 | $O(T \times N)$ | $O(N)$ |

($T$ = 테스트 케이스 수, $N$ = 케이스당 `n`의 최댓값)

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

    int need = a.front() + a.back();
    int cnt0 = count(a.begin() + 1, a.end() - 1, 0);

    cout << (cnt0 >= need ? need : -1) << '\n';
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
