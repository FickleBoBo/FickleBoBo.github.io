---
title: "[Codeforces] #2264A - Rumb Needs a Hand [C++]"
date: 2026-09-14
categories: [PS, Codeforces]
tags: ["ad hoc"]
slug: codeforces-2264a
media_subpath: /assets/img/posts/codeforces-2264a/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2264/A)
{: .prompt-info }

---

## 1. 아이디어

임의의 인덱스들을 골라 해당 자리의 값들만 순서를 뒤집어 원본 수열에 반영했을 때 수열이 오름차순이 되는지 판정하는 문제다. 이미 제자리에 위치한 원소들은 굳이 선택할 필요 없고 제자리에 위치하지 않은 원소들만 고르면 되며, 이때 고른 수들이 내림차순으로 배치되어 있어야 뒤집은 결과가 오름차순이 되며 배치 후에도 적절한 위치로 삽입된다. 따라서 제자리에 위치하지 않은 수들만 뽑아서 순서대로 저장한 후 해당 배열이 내림차순인지 판단했다.

---

## 2. 복잡도

| 접근 | 시간            | 공간   |
| ---- | --------------- | ------ |
| 풀이 | $O(T \times N)$ | $O(N)$ |

($T$ = 테스트 케이스 수, $N$ = 케이스당 `n`의 최댓값)

---

## 3. 코드

### 풀이 [C++]

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n;
    cin >> n;

    vector<int> v;
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        if (x != i + 1) v.push_back(x);
    }

    bool flag = true;
    for (int i = 1; i < v.size(); i++) {
        if (v[i - 1] < v[i]) flag = false;
    }

    cout << (flag ? "YES\n" : "NO\n");
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
