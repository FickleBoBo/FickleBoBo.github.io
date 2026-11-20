---
title: "[Codeforces] #2277A - Subset Selecting [C++]"
date: 2026-11-19
categories: [PS, Codeforces]
tags: ["greedy"]
slug: codeforces-2277a
media_subpath: /assets/img/posts/codeforces-2277a/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2277/A)
{: .prompt-info }

---

## 1. 아이디어

원소 중 일부를 골라 $k$개 이상씩 묶었을 때 각 묶음의 최댓값들로 이루어진 집합의 MEX를 최대로 만드는 문제다. MEX를 $x$ 이상으로 만들려면 0부터 $x - 1$까지의 모든 값 $v$마다 최댓값이 $v$인 묶음이 하나씩 필요하다. 최댓값이 $v$인 묶음은 값이 $v$인 원소를 하나 이상 포함하고 나머지는 $v$ 이하의 아무 원소로 채우면 되므로, 값이 작을수록 쓸 수 있는 원소가 제한되어 $v$가 작은 묶음부터 차례로 만든다. 묶음에 $k$개보다 많이 담으면 뒤 묶음이 쓸 원소만 줄어드니 묶음마다 $k$개만 쓴다.

값이 $v$ 미만인 원소 중 앞 묶음에 쓰고 남은 것은 최댓값이 $v$인 묶음의 빈자리를 어느 것이든 채울 수 있으므로 어느 묶음에 썼는지는 상관없이 남은 개수만 세면 된다. 따라서 값이 $v$인 원소가 하나라도 있고 그 개수와 남은 원소 수의 합이 $k$ 이상이면 그 묶음을 만들 수 있고, 이 묶음에 $k$개를 쓰고 남은 원소는 다음 $v$로 넘어간다. $v$를 0부터 올리며 이 조건이 처음 깨지는 $v$가 답이다. 어떻게 묶어도 최댓값이 0부터 $v$까지인 $v + 1$개의 묶음은 각각 값이 $v$ 이하인 원소를 $k$개 이상 가지므로, 값이 $v$ 이하인 원소 중 묶음에 쓰이지 않고 남는 수는 이 방법보다 많을 수 없고, 따라서 조건이 깨지면 다른 방법으로도 그 묶음을 만들 수 없다.

---

## 2. 코드

### 풀이 [C++]

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n, k;
    cin >> n >> k;

    vector<int> cnt(1 + n);
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        cnt[x]++;
    }

    int left = 0;
    for (int i = 0; i <= n; i++) {
        if (cnt[i] == 0 || left + cnt[i] < k) {
            cout << i << '\n';
            return;
        }

        left += cnt[i] - k;
    }
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
