---
title: "[Codeforces] #2275B - Did Not Go to Print [C++]"
date: 2026-10-11
categories: [PS, Codeforces]
tags: ["data structure", "stack"]
slug: codeforces-2275b
media_subpath: /assets/img/posts/codeforces-2275b/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2275/B)
{: .prompt-info }

---

## 1. 아이디어

각 문서 `i`에 대해 명령 `1`은 문서를 메모리 맨 위에 쌓고, `2`는 메모리가 비어 있지 않으면 맨 위 문서를 출력하고 비어 있으면 문서 `i`를 출력하며, `3`은 문서 `i`를 바로 출력한다. 모든 명령이 끝난 뒤 출력되지 않은 문서를 모두 찾는 문제다.

`3`은 문서 `i`가 항상 출력되므로 볼 필요가 없고, `2`는 메모리가 비어 있지 않으면 자기 문서 `i`는 출력되지 않으면서 맨 위 문서 하나를 출력한다. 따라서 명령을 그대로 스택으로 재현하면, 메모리가 비어 있지 않을 때 `2`를 받은 문서 `i`와 끝까지 스택에 남은 문서가 출력되지 않은 문서다.

---

## 2. 복잡도

| 접근 | 시간   | 공간   |
| ---- | ------ | ------ |
| 풀이 | $O(N)$ | $O(N)$ |

($N$ = 모든 테스트 케이스에 걸친 `n`의 총합)

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
