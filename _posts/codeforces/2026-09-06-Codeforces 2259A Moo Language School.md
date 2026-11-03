---
title: "[Codeforces] #2259A - Moo Language School [C++]"
date: 2026-09-06
categories: [PS, Codeforces]
tags: ["warm up"]
slug: codeforces-2259a
media_subpath: /assets/img/posts/codeforces-2259a/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2259/A)
{: .prompt-info }

---

## 1. 아이디어

$k$칸씩 묶인 농장마다 학교를 하나 이상 지어야 하고 그중 Farmer Nhoj의 땅에 짓는 횟수를 최소로 하는 문제다. 농장끼리는 칸을 공유하지 않아 서로 독립이고 학교를 더 짓는다고 횟수가 줄지 않으므로 농장마다 하나씩만 짓는다. Farmer Nhoj의 땅이 아닌 칸(`0`)이 농장에 하나라도 있으면 거기에 지어 횟수를 늘리지 않을 수 있으니, 칸이 전부 Farmer Nhoj의 땅(`1`)인 농장에서만 어쩔 수 없이 횟수가 한 번씩 늘어 답은 그런 농장의 수가 된다.

---

## 2. 코드

### 풀이 [C++]

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n, k;
    string s;
    cin >> n >> k >> s;

    int cnt = 0;
    for (int i = 0; i < n; i += k) {
        bool flag = false;
        for (int j = i; j < i + k; j++) {
            if (s[j] == '0') flag = true;
        }

        if (!flag) cnt++;
    }

    cout << cnt << '\n';
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
