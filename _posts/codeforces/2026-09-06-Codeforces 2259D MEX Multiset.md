---
title: "[Codeforces] #2259D - MEX Multiset [C++]"
date: 2026-09-06
categories: [PS, Codeforces]
tags: ["ad hoc", "constructive"]
slug: codeforces-2259d
media_subpath: /assets/img/posts/codeforces-2259d/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2259/D)
{: .prompt-info }

---

## 1. 아이디어

원소를 세 멀티셋 $A$, $B$, $C$에 나눠 담아 MEX의 합이 MEX의 최댓값의 두 배 이상이 되게 하는 문제다. `0`이 없는 멀티셋의 MEX는 0이므로 MEX가 0이 아닐 수 있는 멀티셋은 `0`을 가진 것뿐이다. 배열에 `0`이 하나뿐이면 MEX가 0이 아닌 멀티셋도 하나뿐이라 합이 최댓값과 같고, 최댓값이 1 이상이므로 두 배에 못 미쳐 답은 NO이다. `0`이 없으면 어떻게 나누든 MEX가 전부 0이라 조건이 성립한다. `0`이 둘 이상이면 `0` 하나를 $B$에, 나머지 `0`을 $C$에, `0`이 아닌 원소를 $A$에 담으면 MEX가 0, 1, 1이 되어 합 2가 최댓값 1의 두 배와 같아 성립한다.

---

## 2. 코드

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
