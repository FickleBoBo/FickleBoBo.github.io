---
title: "[Codeforces] #2244A - Iskander and Drawings [C++]"
date: 2026-09-04
categories: [PS, Codeforces]
tags: ["string"]
slug: codeforces-2244a
media_subpath: /assets/img/posts/codeforces-2244a/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2244/A)
{: .prompt-info }

---

## 1. 아이디어

`#`이 이어진 줄들 중 다 지우는 데 가장 오래 걸리는 줄의 시간을 구하는 문제다. 한 줄은 초마다 양 끝에서 1센티미터씩, 곧 2센티미터씩 줄다가 길이가 1이나 2가 되면 다음 1초에 다 지워지므로 길이 $L$이 짝수면 $L / 2$초, 홀수면 $(L + 1) / 2$초가 걸려 $\lceil L / 2 \rceil$초이고, 이 시간은 $L$이 길어져도 줄어들지 않으므로 `#`이 이어지는 길이를 세어 가장 긴 줄의 시간을 답으로 한다.

---

## 2. 코드

### 풀이 [C++]

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n;
    string s;
    cin >> n >> s;

    int mx = 0, cnt = 0;
    for (char c : s) {
        if (c == '#') {
            cnt++;
        } else {
            cnt = 0;
        }

        mx = max(mx, (cnt + 1) / 2);
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
