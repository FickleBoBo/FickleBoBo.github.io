---
title: "[Codeforces] #2263C1 - Floor of MEX (Easy Version) [C++]"
date: 2026-09-13
categories: [PS, Codeforces]
tags: ["constructive", "difference array"]
slug: codeforces-2263c1
media_subpath: /assets/img/posts/codeforces-2263c1/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2263/C1)
{: .prompt-info }

---

## 1. 아이디어

주어진 배열 $a$가 $f(B, k) = a_k$를 만족하려면 각 $k$마다 두 조건이 필요한데, 몫이 $a_k$가 되는 구간 $[k \cdot a_k, k \cdot (a_k + 1))$에는 $B$의 원소가 하나도 없어야 하고, 그보다 작은 몫 0부터 $a_k - 1$까지 각각에 해당하는 구간에는 $B$의 원소가 적어도 하나씩 있어야 한다. 배제 조건은 $k$마다 어느 자리를 빼야 하는지가 배열 $a$로 그대로 정해져 있어 어떤 $B$를 고르든 공통으로 피해야 하지만, 포함 조건은 원소가 많을수록 오히려 만족하기 쉬워지므로, 모든 $k$에 대한 배제 구간을 전부 합쳐 그 합집합만 빼고 나머지를 통째로 $B$에 넣는 게 항상 안전하다. 실제 정답이 존재한다면 그 정답은 이 최대 후보의 부분집합일 수밖에 없어서 최대 후보가 원소를 더 갖고 있어도 포함 조건이 깨질 일이 없고, 배제 조건은 애초에 정의상 지켜지기 때문이다. 이 배제 구간들의 합집합은 차분 배열로 표시해 한 번의 누적합으로 계산하면 된다.

---

## 2. 복잡도

| 접근 | 시간   | 공간   |
| ---- | ------ | ------ |
| 풀이 | $O(N)$ | $O(N)$ |

($N$ = 모든 테스트 케이스에 걸친 `n`의 총합)

---

## 3. 코드

### 풀이 [C++]

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n;
    cin >> n;

    vector<int> diff(n + 1);
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;

        diff[min(n, (i + 1) * x)]++;
        diff[min(n, (i + 1) * (x + 1))]--;
    }

    for (int i = 1; i <= n; i++) {
        diff[i] += diff[i - 1];
    }

    int cnt = count(diff.begin(), diff.end() - 1, 0);
    cout << cnt << '\n';
    if (cnt) {
        for (int i = 0; i < n; i++) {
            if (diff[i] == 0) cout << i << ' ';
        }
        cout << '\n';
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
