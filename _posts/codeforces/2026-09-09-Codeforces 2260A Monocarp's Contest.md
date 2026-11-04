---
title: "[Codeforces] #2260A - Monocarp's Contest [C++]"
date: 2026-09-09
categories: [PS, Codeforces]
tags: ["ad hoc"]
slug: codeforces-2260a
media_subpath: /assets/img/posts/codeforces-2260a/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2260/A)
{: .prompt-info }

---

## 1. 아이디어

문제 둘을 맞바꾸는 연산으로 맨 앞과 맨 뒤 문제를 쉬운 문제(`0`)로 만드는 최소 횟수를 구하는 문제다. 맨 앞과 맨 뒤 중 어려운 문제(`1`)의 개수를 `need`라 하면, 한 번의 교환은 두 위치만 바꾸는데 맨 앞과 맨 뒤끼리 바꿔서는 어려운 문제가 줄지 않으므로 한 번에 끝의 어려운 문제를 최대 하나만 해결할 수 있어 `need`번이 하한이다. 어려운 끝을 가운데의 쉬운 문제와 바꾸면 정확히 하나 줄어드므로 가운데에 쉬운 문제가 `need`개 이상이면 `need`번이 답이다. 모자라면 전체에 쉬운 문제가 둘 미만이라 양 끝을 쉬운 문제로 채울 수 없어 불가능하다.

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
