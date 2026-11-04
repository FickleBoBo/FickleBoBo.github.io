---
title: "[Codeforces] #2259B - Minus Two [C++]"
date: 2026-09-06
categories: [PS, Codeforces]
tags: ["math", "number theory"]
slug: codeforces-2259b
media_subpath: /assets/img/posts/codeforces-2259b/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2259/B)
{: .prompt-info }

---

## 1. 아이디어

배열의 모든 원소에 $\lvert a_i - 2 \rvert$를 동시에, 몇 번이든 반복해서 적용할 수 있을 때 같은 값을 가진 원소를 가장 많이 만드는 문제다. 연산은 홀짝을 바꾸지 않으므로 홀수와 짝수는 절대 같아지지 않고, 홀수는 2씩 줄다가 $a_i = 1$에서 $\lvert 1 - 2 \rvert = 1$로 멈추기 때문에 연산을 충분히 하면 전부 같은 값으로 모인다. 짝수는 결국 `0`과 `2`를 오가게 되는데, 짝수에서 $\lvert a_i - 2 \rvert$는 $a_i \ge 2$이든 $a_i = 0$이든 4로 나눈 나머지를 0에서 2로, 2에서 0으로 바꾸므로 모든 짝수 원소의 나머지가 매 연산마다 함께 맞바뀐다. 따라서 4로 나눈 나머지가 같은 짝수끼리는 연산 뒤에도 나머지가 계속 같아 충분히 연산하면 같은 값이 되는 반면 나머지가 다른 짝수끼리는 계속 달라 같아질 수 없다. 결국 홀수 전체, 4로 나눈 나머지가 0인 원소, 나머지가 2인 원소 중 가장 큰 묶음의 크기가 답이다.

---

## 2. 코드

### 풀이 [C++]

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n;
    cin >> n;

    vector<int> cnt(4);
    while (n--) {
        int x;
        cin >> x;
        cnt[x % 4]++;
    }

    cout << max({cnt[1] + cnt[3], cnt[0], cnt[2]}) << '\n';
}

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);

    int t;
    cin >> t;
    while (t--) solve();
}
```

`std::max`는 중괄호로 묶은 값 목록도 받아서 세 묶음의 크기 중 최댓값을 한 번에 구했다.

---
