---
title: "[Codeforces] #2259D - MEX Multiset [C++]"
date: 2026-09-06
categories: [PS, Codeforces]
tags: ["ad hoc", "constructive"]
slug: codeforces-2259d
media_subpath: /assets/img/posts/codeforces-2259d/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2259/D)
{: .prompt-info }

---

## 1. 아이디어

수열의 각 원소를 세 멀티셋 `A`, `B`, `C` 중 하나에 넣어, 세 MEX의 합이 그중 최댓값의 두 배 이상이 되게 할 수 있는지 판정하고 가능하면 배치를 출력하는 문제다. 해당 문제는 관찰을 통해 해결할 수 있는데 `0`의 개수가 포인트가 된다.

먼저 수열에 `0`이 한 개도 없는 경우는 어떤 집합이든 MEX가 0이 되며, 주어진 수식을 만족한다.

수열에 `0`이 2개 이상인 경우는 한 집합에는 `0`을 하나만 배정하고, 다른 집합에는 나머지 `0`들을 배정하고, 남은 집합에 `0`이 아닌 남은 수들을 배정할 경우 각 집합의 MEX는 1, 1, 0이 된다. 이런 배치는 주어진 수식을 만족한다.

수열에 `0`이 1개만 있는 경우는 `0`을 배정한 집합은 MEX가 1 이상이 되는데 남은 두 집합은 어떻게 배정하든 MEX가 0이 된다. 이 경우에는 어떻게 해도 주어진 수식을 만족하지 않는다.

위 성질을 통해 `0`의 개수를 센 후, 케이스를 나눴다.

---

## 2. 복잡도

| 접근 | 시간   | 공간   |
| ---- | ------ | ------ |
| 풀이 | $O(N)$ | $O(N)$ |

($N$ = 모든 테스트 케이스에 걸친 수열 길이의 총합)

---

## 3. 코드

### 풀이 [C++]

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n;
    cin >> n;

    vector<int> a(n);
    for (int& x : a) cin >> x;

    int cnt0 = count(a.begin(), a.end(), 0);

    if (cnt0 == 1) {
        cout << "NO\n";
        return;
    }

    bool find0 = false;
    string ans;
    cout << "YES\n";
    for (int x : a) {
        if (x > 0) {
            ans += 'A';
        } else if (!find0) {
            ans += 'B';
            find0 = true;
        } else {
            ans += 'C';
        }
    }
    cout << ans << '\n';
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
