---
title: "[Codeforces] #2264A - Rumb Needs a Hand [C++]"
date: 2026-09-14
categories: [PS, Codeforces]
tags: ["ad hoc"]
slug: codeforces-2264a
media_subpath: /assets/img/posts/codeforces-2264a/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2264/A)
{: .prompt-info }

---

## 1. 아이디어

순열 $p$에서 인덱스 $i_1 < i_2 < \cdots < i_m$을 골라 $i_j$의 원소를 $i_{m - j + 1}$로 보내는(고른 위치의 값을 거꾸로 뒤집는) 연산을 정확히 한 번 해서 오름차순으로 정렬할 수 있는지 묻는 문제다. 고르지 않은 위치의 값은 그대로다.

정렬되려면 제자리에 있지 않은 원소는 모두 골라야 한다. 고르지 않으면 그 위치의 값이 바뀌지 않기 때문이다. 반대로 제자리에 있는 원소는 고를 이유가 없다. 고른 인덱스들의 가운데가 아니면 그 값이 거울 위치로 옮겨져 제자리를 잃고, 가운데면 움직이지 않아 고르나 마나다.

제자리에 있지 않은 위치를 앞에서부터 $s_1 < s_2 < \cdots < s_r$이라 하자. 나머지 위치는 모두 제자리의 값이 차지하고 있으므로 이 위치들에 놓인 값의 집합도 $\lbrace s_1, \ldots, s_r \rbrace$이다. 이 위치들을 고르면 $s_j$의 값이 $s_{r - j + 1}$로 옮겨지므로, 정렬되려면 $s_j$에 있는 값이 $s_{r - j + 1}$이어야 한다. 위치는 $s_1 < \cdots < s_r$로 커지는데 그 위치의 값은 $s_r, \ldots, s_1$로 작아지므로, 제자리에 있지 않은 원소의 값이 앞에서부터 내림차순이면 된다.

제자리에 있지 않은 원소가 없을 때는 원소 하나를 골라 아무것도 바꾸지 않으면 되니 이 경우도 가능하다.

---

## 2. 코드

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
