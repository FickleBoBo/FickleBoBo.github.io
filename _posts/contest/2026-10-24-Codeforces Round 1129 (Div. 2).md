---
title: "Codeforces Round 1129 (Div. 2) 후기"
description: "대회 중 1/7문제 해결 · 6316위 · 레이팅 1153 → 1093 (-60)"
date: 2026-10-24
categories: [Contest]
tags: ["codeforces", "div 2"]
slug: codeforces-2277
media_subpath: /assets/img/posts/codeforces-2277/
image:
  path: preview.png
math: true
---

<!-- prettier-ignore -->
> [대회 링크](https://codeforces.com/contest/2277)
{: .prompt-info }

---

## 1. 대회 개요

| 항목      | 내용                           |
| --------- | ------------------------------ |
| 대회      | Codeforces Round 1129 (Div. 2) |
| 일시      | 2026-10-24 20:05 KST           |
| 배정 시간 | 135분                          |
| 문제 수   | 7 (A–F)                        |
| 참가 형태 | 공식 (rated)                   |

---

## 2. 결과

| 항목    | 내용                                                          |
| ------- | ------------------------------------------------------------- |
| 푼 문제 | 대회 중 A (1/7)                                               |
| 페널티  | 21분                                                          |
| 순위    | 6316 / 8057위 · 상위 78.4%                                    |
| 레이팅  | 1153 → 1093 (-60) · <span style="color:#808080">newbie</span> |

![레이팅 그래프](rating-graph.png)

---

## 3. 풀이 과정

| 문제                                                                                     | 결과   | 제출 시각 | WA  |
| ---------------------------------------------------------------------------------------- | ------ | --------- | --- |
| [A. Subset Selecting](https://codeforces.com/problemset/problem/2277/A)                  | AC     | 21:01     | 0   |
| [B. Sequence Decreasing](https://codeforces.com/problemset/problem/2277/B)               | 미해결 | —         | —   |
| [C. Edge Addeleting](https://codeforces.com/problemset/problem/2277/C)                   | 미시도 | —         | —   |
| [D1. Number Operating (Easy Version)](https://codeforces.com/problemset/problem/2277/D1) | 미시도 | —         | —   |
| [D2. Number Operating (Hard Version)](https://codeforces.com/problemset/problem/2277/D2) | 미시도 | —         | —   |
| [E. Tree Guessing](https://codeforces.com/problemset/problem/2277/E)                     | 미시도 | —         | —   |
| [F. Token Re-Moving](https://codeforces.com/problemset/problem/2277/F)                   | 미시도 | —         | —   |

---

### A. Subset Selecting

카운팅 배열로 카운팅을 한 후 앞에서부터 `k`개씩 그룹핑을 해주는 방식이면 해결할 수 있어 보였다. A번 문제치고 제법 어려운 편이었던 것 같다.

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n, k;
    cin >> n >> k;

    vector<int> cnt(1 + 100);
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        cnt[x]++;
    }

    int left = 0;
    for (int i = 0; i <= 100 + 1; i++) {
        if (cnt[i] >= k) {
            left += cnt[i] - k;
        } else {
            if (cnt[i] > 0 && left >= k - cnt[i]) {
                left -= k - cnt[i];
            } else {
                cout << i << '\n';
                return;
            }
        }
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
> 풀이 → [[Codeforces] #2277A - Subset Selecting](/posts/codeforces-2277a/)
{: .prompt-tip }

---

### B. Sequence Decreasing

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n;
    cin >> n;

    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;

        if (x < n) {
            cout << n << '\n';
            return;
        }
    }

    cout << 0 << '\n';
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

### C. Edge Addeleting

대회 중 미시도.

---

### D1. Number Operating (Easy Version)

대회 중 미시도.

---

### D2. Number Operating (Hard Version)

대회 중 미시도.

---

### E. Tree Guessing

대회 중 미시도.

---

### F. Token Re-Moving

대회 중 미시도.

---

## 총평

B번 문제를 푸는 데 시간을 너무 많이 써서 한 문제밖에 못 풀었다. 당분간은 대회 참여보다는 기본기를 좀 더 쌓아야겠다.

---
