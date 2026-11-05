---
title: "[Codeforces] #2266D - Falling Concrete [C++]"
date: 2026-09-22
categories: [PS, Codeforces]
tags: ["ad hoc", "sorting"]
slug: codeforces-2266d
media_subpath: /assets/img/posts/codeforces-2266d/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2266/D)
{: .prompt-info }

---

## 1. 아이디어

$j$번째 도로 구역을 앞쪽 위치 $i$로 옮기면 그 구역은 높이가 $j - i$ 줄고 지나친 구역은 높이가 1씩 오르는 연산을 반복해, 높이가 같은 연속 구간의 최대 길이를 구하는 문제다.

$b_k = a_k - k$로 두면 위치 $i$로 옮겨진 구역의 $b$는 $a_j - (j - i) - i = a_j - j$로 그대로이고, 지나친 구역은 위치가 1 늘고 높이가 1 올라 역시 $b$가 그대로이다. 곧 연산은 $b$의 값을 바꾸지 않고 원소 하나를 앞쪽 원하는 위치에 끼워 넣을 뿐이고, 앞에서부터 원하는 원소를 차례로 끌어오면 $b$를 어떤 순서로든 재배열할 수 있다.

이웃한 두 구역의 높이가 같다는 것은 $b$가 오른쪽으로 갈수록 정확히 1 작아진다는 뜻이므로, 높이가 같은 연속 구간은 $b$ 값이 1씩 줄어드는 수열이라 값이 모두 다르다. 따라서 $b$의 서로 다른 값 중 연속한 정수로 이어지는 가장 긴 묶음의 크기가 답이고, 그 묶음은 $b$를 큰 값부터 이웃하게 재배열하면 높이가 모두 같아진다.

---

## 2. 코드

### 풀이 [C++]

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n;
    cin >> n;

    vector<int> b(n);
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        b[i] = x - (i + 1);
    }

    sort(b.begin(), b.end());
    b.erase(unique(b.begin(), b.end()), b.end());

    int ans = 1, len = 1;
    for (int i = 1; i < b.size(); i++) {
        len = (b[i] == b[i - 1] + 1) ? len + 1 : 1;
        ans = max(ans, len);
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
