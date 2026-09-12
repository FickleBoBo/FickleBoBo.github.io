---
title: "[Codeforces] #2259A - Moo Language School [C++]"
date: 2026-09-06
categories: [PS, Codeforces]
tags: ["warm up"]
slug: codeforces-2259a
media_subpath: /assets/img/posts/codeforces-2259a/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2259/A)
{: .prompt-info }

---

## 1. 아이디어

`n`개의 칸이 `k`칸씩 묶여 여러 농장을 이루고, 농장마다 학교를 최소 하나는 지어야 한다. 이진 문자열 `s`에서 `1`인 칸은 Nhoj의 땅이라 거기 학교를 지으면 비용이 들고, Nhoj의 땅에 짓는 횟수를 최소화하는 문제다. `k`칸씩 묶인 각 농장에 대해 John의 땅인 `0`이 하나라도 있으면 그 칸에 바로 학교를 지으면 되고, `0`이 하나도 없으면 Nhoj의 땅에 학교를 어쩔 수 없이 짓고 카운팅을 하면 된다.

---

## 2. 복잡도

| 접근 | 시간            | 공간   |
| ---- | --------------- | ------ |
| 풀이 | $O(T \times N)$ | $O(N)$ |

($T$ = 테스트 케이스 수, $N$ = `s`의 길이)

---

## 3. 코드

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
        bool ok = false;
        for (int j = i; j < i + k; j++) {
            if (s[j] == '0') ok = true;
        }

        if (!ok) cnt++;
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
