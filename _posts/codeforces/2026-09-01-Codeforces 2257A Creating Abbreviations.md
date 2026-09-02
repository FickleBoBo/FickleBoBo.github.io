---
title: "[Codeforces] #2257A - Creating Abbreviations [C++]"
date: 2026-09-01
categories: [PS, Codeforces]
tags: ["string"]
slug: codeforces-2257a
media_subpath: /assets/img/posts/codeforces-2257a/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2257/A)
{: .prompt-info }

---

## 1. 아이디어

약어가 만들어질 수 있는지는 그 약어의 모든 글자가 초기 단어들의 첫 글자 집합 안에 있는지로 결정되는데, 새로 만든 약어를 집합에 다시 넣어도 이 판정이 달라지지 않는다는 점이 핵심이다. 약어가 이후에 다른 약어의 재료로 쓰일 때 기여하는 건 자기 첫 글자 하나뿐이고, 그 첫 글자는 약어를 이루는 수열 맨 앞 단어의 첫 글자인데 그 단어가 다시 초기 단어이거나 약어이므로 계속 거슬러 올라가면 결국 초기 단어의 첫 글자에 닿는다. 따라서 쓸 수 있는 첫 글자는 처음 주어진 것들에서 늘어나지 않는다.

반대로 어떤 문자열의 모든 글자가 이 집합 안에 있으면 각 글자마다 그 글자로 시작하는 초기 단어를 순서대로 골라 뽑는 것으로 항상 약어로 만들 수 있고, 같은 단어를 여러 번 써도 되며 약어 길이가 1 이상이라 뽑을 게 없는 경우도 없다. 약어를 하나 만드는 게 쓸 수 있는 글자 집합을 건드리지 않으니 주어진 약어들을 어떤 순서로 처리하든 상관없고, 결국 초기 단어들의 첫 글자만 모아 두고 각 약어의 글자가 전부 거기 들어 있는지 확인하면 된다.

---

## 2. 복잡도

| 접근 | 시간       | 공간   |
| ---- | ---------- | ------ |
| 풀이 | $O(N + M)$ | $O(1)$ |

($N$ = 전체 테스트 케이스에 걸친 초기 단어 길이의 총합, $M$ = 전체 약어 길이의 총합)

---

## 3. 코드

### 풀이 [C++]

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n, m;
    cin >> n >> m;

    vector<bool> seen(26);
    while (n--) {
        string s;
        cin >> s;
        seen[s[0] - 'a'] = true;
    }

    bool ok = true;
    while (m--) {
        string s;
        cin >> s;

        for (char c : s) {
            if (!seen[c - 'A']) ok = false;
        }
    }

    cout << (ok ? "YES" : "NO") << '\n';
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
