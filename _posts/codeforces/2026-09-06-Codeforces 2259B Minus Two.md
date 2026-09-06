---
title: "[Codeforces] #2259B - Minus Two [C++]"
date: 2026-09-06
categories: [PS, Codeforces]
tags: ["number theory", "math"]
slug: codeforces-2259b
media_subpath: /assets/img/posts/codeforces-2259b/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2259/B)
{: .prompt-info }

---

## 1. 아이디어

수열 `a`에 모든 원소를 동시에 2를 뺀 절댓값으로 바꾸는 연산을 원하는 만큼 적용해서, 한 값의 최대 빈도를 얼마까지 높일 수 있는지 구하는 문제다.

연산을 몇 번 해보면 규칙성을 발견할 수 있는데, 홀수는 `1`로 수렴하게 되고 짝수는 `0`과 `2`를 진동하게 된다는 점이다. 짝수의 경우 4로 나눈 나머지가 0인 경우와 2인 경우가 서로 반대 위상으로 진동한다. 따라서 수열 `a`의 각 수를 4로 나눈 나머지가 홀수인 그룹과 0인 그룹, 2인 그룹 총 3개의 그룹이 연산을 수없이 시행했을 때 같은 값을 갖는 그룹으로 묶을 수 있다. 이를 위해 카운팅 배열을 통해 각 그룹의 개수를 센 후 최댓값을 반환했다.

---

## 2. 복잡도

| 접근 | 시간   | 공간   |
| ---- | ------ | ------ |
| 풀이 | $O(N)$ | $O(1)$ |

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

---
