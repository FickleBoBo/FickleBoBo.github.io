---
title: "[Codeforces] #2275B - Did Not Go to Print [C++]"
date: 2026-10-11
categories: [PS, Codeforces]
tags: ["data structure", "stack"]
slug: codeforces-2275b
media_subpath: /assets/img/posts/codeforces-2275b/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2275/B)
{: .prompt-info }

---

## 1. 아이디어

명령 문자열이 주어질 때 인쇄되지 않은 문서의 번호를 구하는 문제다. `1`은 문서 $i$를 스택에 올리고, `2`는 스택이 비어 있지 않으면 맨 위 문서를 인쇄하고 비어 있으면 문서 $i$를 인쇄하며, `3`은 문서 $i$를 인쇄하므로 스택을 시뮬레이션하면 된다. 문서 $i$가 인쇄되지 않는 경우는 두 가지로, 끝까지 스택에서 꺼내지 못한 문서와 스택의 맨 위 문서를 인쇄한 `2` 명령 자신의 문서 $i$이다.

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

    stack<int> st;
    vector<bool> chk(1 + n);
    for (int i = 1; i <= n; i++) {
        int c = s[i - 1] - '0';
        if (c == 1) {
            st.push(i);
        } else if (c == 2) {
            if (!st.empty()) {
                st.pop();
                chk[i] = true;
            }
        }
    }

    while (!st.empty()) {
        chk[st.top()] = true;
        st.pop();
    }

    cout << count(chk.begin(), chk.end(), true) << '\n';
    for (int i = 1; i <= n; i++) {
        if (chk[i]) cout << i << ' ';
    }
    cout << '\n';
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
