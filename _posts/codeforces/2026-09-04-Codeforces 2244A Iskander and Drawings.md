---
title: "[Codeforces] #2244A - Iskander and Drawings [C++]"
date: 2026-09-04
categories: [PS, Codeforces]
tags: ["string"]
slug: codeforces-2244a
media_subpath: /assets/img/posts/codeforces-2244a/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2244/A)
{: .prompt-info }

---

## 1. 아이디어

`#`과 `*`로 이루어진 문자열이 주어지고 `*`은 빈 공간, `#`는 선을 의미한다. 각 문자열에 대해 선을 지우는 데 가장 오래 걸리는 시간을 구하는 문제로 각 선은 좌우에서 매초 1센티미터씩 지울 수 있다. 따라서 주어진 문자열에서 연속된 `#`으로 이루어진 가장 긴 선을 찾아 길이를 구한 후 이를 2로 올림 나눗셈을 한 값이 해당 문자열에서 가장 긴 선을 지우는 데 걸리는 시간이 된다.

---

## 2. 복잡도

| 접근 | 시간   | 공간   |
| ---- | ------ | ------ |
| 풀이 | $O(N)$ | $O(1)$ |

($N$ = 모든 테스트 케이스에 걸친 문자열 길이의 총합. `stringstream` 버퍼는 문자열 길이에 비례하지만 그 길이가 10 이하라 상수)

---

## 3. 코드

### 풀이 [C++]

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n;
    string s;
    cin >> n >> s;

    stringstream ss(s);
    string token;
    int mx = 0;
    while (getline(ss, token, '*')) {
        mx = max(mx, ((int)token.size() + 1) / 2);
    }

    cout << mx << '\n';
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
