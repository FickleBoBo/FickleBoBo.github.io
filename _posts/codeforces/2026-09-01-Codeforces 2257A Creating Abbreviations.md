---
title: "[Codeforces] #2257A - Creating Abbreviations [C++]"
date: 2026-09-01
categories: [PS, Codeforces]
tags: ["ad hoc", "string"]
slug: codeforces-2257a
media_subpath: /assets/img/posts/codeforces-2257a/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2257/A)
{: .prompt-info }

---

## 1. 아이디어

처음 단어들로 약어를 차례로 만들어 갈 때 주어진 약어가 전부 나올 수 있는지 묻는 문제인데, 약어의 첫 글자는 그 약어를 이루는 첫 단어의 첫 글자이므로 약어를 단어로 쓰더라도 새로운 첫 글자는 생기지 않는다. 그래서 쓸 수 있는 단어의 첫 글자는 언제나 처음 단어들의 첫 글자 집합에 들어 있고(처음 단어는 소문자, 약어는 대문자라 대문자로 바꿔 맞춘다), 약어를 이루는 글자가 전부 그 집합에 있으면 글자마다 그 글자로 시작하는 처음 단어를 골라(같은 단어를 여러 번 써도 된다) 약어를 만들 수 있어 순서와 상관없이 가능하다. 반대로 집합에 없는 글자가 하나라도 있는 약어는 어떤 순서로도 만들 수 없다.

---

## 2. 코드

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

    bool flag = true;
    while (m--) {
        string s;
        cin >> s;

        for (char c : s) {
            if (!seen[c - 'A']) flag = false;
        }
    }

    cout << (flag ? "YES" : "NO") << '\n';
}

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);

    int t;
    cin >> t;
    while (t--) solve();
}
```

한 약어에서 만들 수 없음이 드러나도 남은 약어를 끝까지 읽어야 다음 테스트 케이스의 입력이 밀리지 않으므로, 바로 반환하지 않고 `flag`에 기록했다.

---
