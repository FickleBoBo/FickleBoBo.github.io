---
title: "[Codeforces] #2263B - Min Matrices [C++]"
date: 2026-09-13
categories: [PS, Codeforces]
tags: ["constructive"]
slug: codeforces-2263b
media_subpath: /assets/img/posts/codeforces-2263b/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2263/B)
{: .prompt-info }

---

## 1. 아이디어

$n \times n$ 행렬에 1부터 $n^2$까지의 수를 하나씩 채워 넣어 행 최솟값과 열 최솟값을 모은 집합 $f(A)$의 크기가 정확히 $k$가 되게 만들어야 하는 문제인데, 먼저 $k$의 가능 범위부터 좁혀야 한다. 행 최솟값 $n$개는 서로 다른 칸의 값이라 항상 서로 다르므로 $f(A)$는 최소 $n$개는 가져야 하고, 반대로 전체에서 가장 작은 수는 자기 행과 열의 최솟값을 동시에 차지할 수밖에 없어 아무리 벌어져도 행 최솟값 $n$개와 열 최솟값 $n$개가 딱 하나만 겹치는 $2n - 1$개를 넘을 수 없다.

이 범위($n \le k \le 2n - 1$) 안에서는 몇 개의 행과 열이 최솟값을 공유하게 할지로 $k$를 직접 조절할 수 있다. $m$개의 행과 열이 대각선을 따라 최솟값을 공유하고 나머지 $n - m$개의 행과 $n - m$개의 열은 각자 따로 최솟값을 가지게 하면 $f(A)$의 크기는 $m + 2(n - m) = 2n - m$이 되므로, $m = 2n - k$로 잡으면 원하는 $k$를 정확히 맞출 수 있다. 이때 공유 대각선과 나머지 행·열의 최솟값 자리에 전체에서 가장 작은 수들부터 순서대로 채워 넣고 남은 칸은 큰 수들로 채우면, 지정한 자리들이 각자의 행과 열에서 항상 최솟값이 되는 게 보장된다.

---

## 2. 복잡도

| 접근 | 시간     | 공간     |
| ---- | -------- | -------- |
| 풀이 | $O(N^2)$ | $O(N^2)$ |

($N$ = 모든 테스트 케이스에 걸친 행렬 크기 `n`의 총합)

---

## 3. 코드

### 풀이 [C++]

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n, k;
    cin >> n >> k;

    if (k < n || 2 * n - 1 < k) {
        cout << -1 << '\n';
        return;
    }

    vector<vector<int>> a(n, vector<int>(n));
    int num = 1;
    int m = 2 * n - k;

    for (int i = 0; i < m; i++) a[i][i] = num++;
    for (int i = m; i < n; i++) a[m - 1][i] = num++;
    for (int i = m; i < n; i++) a[i][n - 1] = num++;

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (a[i][j] != 0) {
                cout << a[i][j] << ' ';
            } else {
                cout << num++ << ' ';
            }
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
