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

처음 단어 $n$개로 시작해 약어를 하나씩 만들어 갈 때, 주어진 약어 $m$개를 어떤 순서로든 전부 만들 수 있는지 묻는 문제다. 약어는 단어열의 첫 글자들로 이루어지므로, 처음 단어들의 첫 글자 집합이 곧 약어에 쓸 수 있는 글자의 전부인지가 핵심이다.

약어를 이루는 글자는 항상 이 집합 안에 있다. 처음 단어로 만든 약어의 글자는 처음 단어의 첫 글자이고, 이미 만든 약어를 단어로 쓰더라도 그 첫 글자는 약어를 만든 단어의 첫 글자라 새로운 글자는 생기지 않기 때문이다. 처음 단어는 소문자, 약어는 대문자이므로 대문자로 바꿔 비교한다.

반대로 약어의 글자가 전부 이 집합에 있으면 만들 수 있다. 글자마다 그 글자로 시작하는 처음 단어를 골라 이어 붙이면 되고(같은 단어를 여러 번 써도 된다), 다른 약어를 거치지 않으므로 만드는 순서와도 상관이 없다. 집합에 없는 글자가 하나라도 있는 약어는 어떤 순서로도 만들 수 없다.

따라서 모든 약어의 모든 글자가 집합에 들어 있으면 `YES`, 아니면 `NO`이다.

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
