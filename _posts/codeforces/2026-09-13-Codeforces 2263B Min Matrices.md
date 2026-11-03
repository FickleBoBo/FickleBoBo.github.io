---
title: "[Codeforces] #2263B - Min Matrices [C++]"
date: 2026-09-13
categories: [PS, Codeforces]
tags: ["constructive"]
slug: codeforces-2263b
media_subpath: /assets/img/posts/codeforces-2263b/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2263/B)
{: .prompt-info }

---

## 1. 아이디어

1부터 $n^2$까지를 한 번씩 써서 $n \times n$ 행렬을 채워 행 $n$개와 열 $n$개의 최솟값 중 서로 다른 값이 정확히 $k$개가 되게 하는 문제다. 행마다 최솟값이 서로 다른 칸에 있고 칸마다 수가 달라 값도 모두 다르므로 $k \ge n$이고, 최솟값 $2n$개 중 1은 자기 행과 열의 최솟값을 동시에 맡아 한 값이 둘로 세어지므로 $k \le 2n - 1$이어서 이 범위 밖은 불가능하다. 행과 열의 최솟값을 함께 맡는 칸이 $m$개이면 값이 $m$개 겹쳐 $k = 2n - m$이 되므로 범위 안에서는 $m = 2n - k$개를 만들면 되는데, 대각선 앞쪽 $m$칸에 1부터 $m$까지를 두면 이 칸들이 자기 행과 열의 최솟값이 되어 겹침이 $m$개 생긴다. 나머지 $n - m$개 열의 최솟값은 대각선의 $m$번째 칸이 있는 행에서 그 칸의 오른쪽 $n - m$칸에, 나머지 $n - m$개 행의 최솟값은 마지막 열의 $m + 1$행부터 $n$행까지 $n - m$칸에 $m$보다 큰 수를 이어서 차례로 두어 맡긴다. 열 쪽 칸은 같은 행의 대각선 값 $m$보다 크고 행 쪽 칸은 같은 열 위쪽의 열 쪽 칸보다 커서 각자 열이나 행 하나의 최솟값일 뿐이므로 더 겹치지 않고, 남은 칸은 이미 둔 수보다 모두 큰 수로 채워서 수를 둔 칸들이 각자의 최솟값으로 남게 한다. $n = 5$, $k = 7$이면 $m = 3$이라 아래처럼 1, 2, 3이 대각선에서 행과 열의 최솟값을 함께 맡고, 4, 5가 열의 최솟값을, 6, 7이 행의 최솟값을 맡아 서로 다른 최솟값이 7개가 된다.

![5×5 행렬(n = 5, k = 7)에서 대각선 앞쪽 세 칸(1, 2, 3)이 행과 열의 최솟값을 함께 맡고, 3이 있는 행의 오른쪽 두 칸(4, 5)이 열의 최솟값, 마지막 열의 그 아래 두 칸(6, 7)이 행의 최솟값을 맡으며, 나머지 칸은 8 이상의 큰 수이고, 행 최솟값 1, 2, 3, 6, 7과 열 최솟값 1, 2, 3, 4, 5를 합치면 서로 다른 값이 7개인 모습](construction-light.svg){: .light }
![5×5 행렬(n = 5, k = 7)에서 대각선 앞쪽 세 칸(1, 2, 3)이 행과 열의 최솟값을 함께 맡고, 3이 있는 행의 오른쪽 두 칸(4, 5)이 열의 최솟값, 마지막 열의 그 아래 두 칸(6, 7)이 행의 최솟값을 맡으며, 나머지 칸은 8 이상의 큰 수이고, 행 최솟값 1, 2, 3, 6, 7과 열 최솟값 1, 2, 3, 4, 5를 합치면 서로 다른 값이 7개인 모습](construction-dark.svg){: .dark }

---

## 2. 코드

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
