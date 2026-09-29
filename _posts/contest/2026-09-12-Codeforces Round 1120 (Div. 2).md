---
title: "Codeforces Round 1120 (Div. 2) 후기"
date: 2026-09-12
categories: [Contest]
tags: ["codeforces", "div 2"]
slug: codeforces-2263
media_subpath: /assets/img/posts/codeforces-2263/
image:
  path: preview.png
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [대회 링크](https://codeforces.com/contest/2263)
{: .prompt-info }

---

## 1. 대회 개요

| 항목      | 내용                           |
| --------- | ------------------------------ |
| 대회      | Codeforces Round 1120 (Div. 2) |
| 일시      | 2026-09-12 23:35 KST           |
| 배정 시간 | 180분                          |
| 문제 수   | 7 (A–F)                        |
| 참가 형태 | 공식 (rated)                   |

---

## 2. 결과

| 항목    | 내용                                                         |
| ------- | ------------------------------------------------------------ |
| 푼 문제 | 대회 중 A, B, C1 (3/7)                                       |
| 페널티  | 222분                                                        |
| 순위    | 5632 / 12033위 · 상위 46.8%                                  |
| 레이팅  | 736 → 953 (+217) · <span style="color:#808080">newbie</span> |

![레이팅 그래프](rating-graph.png)

---

## 3. 풀이 과정

| 문제                                                                                 | 결과   | 제출 시각 | WA  |
| ------------------------------------------------------------------------------------ | ------ | --------- | --- |
| [A. Min Max Game](https://codeforces.com/problemset/problem/2263/A)                  | AC     | 4:17      | 0   |
| [B. Min Matrices](https://codeforces.com/problemset/problem/2263/B)                  | AC     | 30:13     | 0   |
| [C1. Floor of MEX (Easy Version)](https://codeforces.com/problemset/problem/2263/C1) | AC     | 138:18    | 5   |
| [C2. Floor of MEX (Hard Version)](https://codeforces.com/problemset/problem/2263/C2) | 미완성 | —         | —   |
| [D. Culling Game](https://codeforces.com/problemset/problem/2263/D)                  | 미시도 | —         | —   |
| [E. Traveling the World](https://codeforces.com/problemset/problem/2263/E)           | 미시도 | —         | —   |
| [F. PLUSworld](https://codeforces.com/problemset/problem/2263/F)                     | 미시도 | —         | —   |

---

### A. Min Max Game

`"Bessie"`부터 번갈아가며 게임을 하는데 `"Bessie"`는 `1`을 최대한 남기는 게 좋고 `"Elsie"`는 `0`을 최대한 남기는 게 좋아 보였다. 서로 상대편 숫자를 최대한 없애려 할 것이므로 `0`과 `1`의 개수로 판별이 가능해보였다.

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n;
    cin >> n;

    vector<int> cnt(2);
    while (n--) {
        int x;
        cin >> x;
        cnt[x]++;
    }

    if (cnt[1] >= cnt[0]) {
        cout << "Bessie\n";
    } else {
        cout << "Elsie\n";
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

<!-- prettier-ignore -->
> 풀이 → [[Codeforces] #2263A - Min Max Game](/posts/codeforces-2263a/)
{: .prompt-tip }

---

### B. Min Matrices

Constructive한 문제라서 관찰로 해결이 가능해보였다. 각 행의 최솟값 집합과 각 열의 최솟값 집합의 합집합을 찾아야하는데 서로 최대한 겹치는 경우와 안 겹치는 경우로 `n` ~ `2 * n - 1`에서 집합 크기가 결정되고 최대한 겹치려면 대각선 위주로 배치해야 하는 게 보였다.

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

    vector<vector<int>> v(n, vector<int>(n));
    int num = 1;
    int p = 2 * n - k - 1;

    for (int i = 0; i <= p; i++) {
        v[i][i] = num++;
    }
    for (int i = p + 1; i < n; i++) {
        v[p][i] = num++;
    }
    for (int i = p + 1; i < n; i++) {
        v[i][n - 1] = num++;
    }

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (v[i][j] != 0) {
                cout << v[i][j] << ' ';
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

<!-- prettier-ignore -->
> 풀이 → [[Codeforces] #2263B - Min Matrices](/posts/codeforces-2263b/)
{: .prompt-tip }

---

### C1. Floor of MEX (Easy Version)

주어진 조건을 만족하는 딱 하나만 찾으면 되는 문제라 가장 쉬운 경우를 찾으려고 했다. 소거법 스타일로 일단 전부 담고 `b`들에 따라서 안 되는 수를 제거해 나가면 딱 되는 경우 중에서 가장 원소가 많은 하나를 찾을 수 있을 것으로 보였다. 항상 가능하다는 조건을 놓쳐서 쓸데없는 예외 처리를 하다가 좀 꼬였는데 보이고 나니 금방 해결할만해 보였다.

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n;
    cin >> n;

    vector<int> v(n);
    for (int& x : v) cin >> x;

    vector<bool> chk(n + 1, true);
    chk[n] = false;
    chk[v[0]] = false;

    for (int i = 1; i < n; i++) {
        int s = (i + 1) * v[i];
        int e = (i + 1) * (v[i] + 1);

        for (int j = min(s, n); j < min(e, n); j++) {
            chk[j] = false;
        }
    }

    int cnt = count(chk.begin(), chk.end(), true);
    cout << cnt << '\n';
    if (cnt) {
        for (int i = 0; i < n; i++) {
            if (chk[i]) cout << i << ' ';
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

<!-- prettier-ignore -->
> 풀이 → [[Codeforces] #2263C1 - Floor of MEX (Easy Version)](/posts/codeforces-2263c1/)
{: .prompt-tip }

---

### C2. Floor of MEX (Hard Version)

C1 문제에서 가능한 모든 케이스의 수를 구하는 문제로 C1에서 최대 크기인 집합을 구했으니 부분집합을 잘 고르면 될 거 같았다. 기본적으로 백트래킹스러워서 백트래킹으로 접근했는데 생각보다 조건이 너무 까다롭고 백트래킹을 하기엔 복잡도가 좀 애매한 거 같아서 꽤 어려웠다. 결국 못 풀었는데 업솔빙도 못했다.

```c++
#include <bits/stdc++.h>
using namespace std;

const int MOD = 1'000'000'007;

int dfs(vector<int>& v, vector<bool>& chk, int pos, vector<bool>& pick, int n) {
    if (pos == n) return 0;

    bool ok = false;
    for (int i = 1; i <= n; i++) {
        if ((pos + 1) % n == 0) {
            for (int j = i; j <= i + 1; j++) {
                if (pick[j]) ok = true;
            }
        }
    }
    if (!ok) return 0;

    int cnt = 1;

    if (chk[pos]) {
        pick[pos] = true;
        cnt += dfs(v, chk, pos + 1, pick, n) % MOD;

        pick[pos] = false;
        cnt += dfs(v, chk, pos + 1, pick, n) % MOD;
    } else {
        pick[pos] = false;
        cnt += dfs(v, chk, pos + 1, pick, n) % MOD;
    }

    return cnt % MOD;
}

void solve() {
    int n;
    cin >> n;

    vector<int> v(n);
    for (int& x : v) cin >> x;

    vector<bool> chk(n + 1, true);
    chk[n] = false;
    chk[v[0]] = false;

    for (int i = 1; i < n; i++) {
        int s = (i + 1) * v[i];
        int e = (i + 1) * (v[i] + 1);

        for (int j = min(s, n); j < min(e, n); j++) {
            chk[j] = false;
        }
    }

    vector<bool> pick(n);
    cout << dfs(v, chk, 0, pick, n) << '\n';
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

### D. Culling Game

대회 중 미시도.

---

### E. Traveling the World

대회 중 미시도.

---

### F. PLUSworld

대회 중 미시도.

---

## 총평

C1, C2 이렇게 나온 걸 이번에 처음 본 거 같은데 둘 다 마냥 쉽지는 않아서 좀 당황했다. C1의 경우 보고 나니 할만했던 거 같고 C2는 아닌 거 같다. MEX 관련 문제가 나온 대회를 한 번 봤어서 관찰이 중요하다고 생각했고, MEX의 이상한 성질을 찾으려 안 하고 착실히 관찰로 가니 해결할 수 있었던 것 같다. C1에서 WA로 페널티가 좀 많았던 것만 아쉬운 대회였다.

---
