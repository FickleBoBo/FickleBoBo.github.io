---
title: "Codeforces Round 1121 (Div. 2) 후기"
date: 2026-09-14
categories: [Contest]
tags: ["codeforces", "div 2"]
slug: codeforces-2264
media_subpath: /assets/img/posts/codeforces-2264/
image:
  path: preview.png
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [대회 링크](https://codeforces.com/contest/2264)
{: .prompt-info }

---

## 1. 대회 개요

| 항목      | 내용                           |
| --------- | ------------------------------ |
| 대회      | Codeforces Round 1121 (Div. 2) |
| 일시      | 2026-09-14 02:05 KST           |
| 배정 시간 | 120분                          |
| 문제 수   | 7 (A–F)                        |
| 참가 형태 | 공식 (rated)                   |

---

## 2. 결과

| 항목    | 내용                                                         |
| ------- | ------------------------------------------------------------ |
| 푼 문제 | 대회 중 A (1/7), 이후 B 업솔빙                               |
| 페널티  | 9분                                                          |
| 순위    | 6263 / 9118위 · 상위 68.7%                                   |
| 레이팅  | 953 → 1043 (+90) · <span style="color:#808080">newbie</span> |

![레이팅 그래프](rating-graph.png)

---

## 3. 풀이 과정

| 문제                                                                                  | 결과   | 제출 시각 | WA  |
| ------------------------------------------------------------------------------------- | ------ | --------- | --- |
| [A. Rumb Needs a Hand](https://codeforces.com/problemset/problem/2264/A)              | AC     | 9:30      | 0   |
| [B. Knife's Pill Farm](https://codeforces.com/problemset/problem/2264/B)              | 업솔빙 | —         | —   |
| [C. Madamant's Skating Dynasty](https://codeforces.com/problemset/problem/2264/C)     | 미시도 | —         | —   |
| [D. Dr. Agos's Dark Mode](https://codeforces.com/problemset/problem/2264/D)           | 미시도 | —         | —   |
| [E1. A Prime Flood (Easy Version)](https://codeforces.com/problemset/problem/2264/E1) | 미시도 | —         | —   |
| [E2. A Prime Flood (Hard Version)](https://codeforces.com/problemset/problem/2264/E2) | 미시도 | —         | —   |
| [F. Deranged Calculator](https://codeforces.com/problemset/problem/2264/F)            | 미시도 | —         | —   |

---

### A. Rumb Needs a Hand

몇 개의 원소들을 고른 후 이들만 역순으로 배치해서 전체를 오름차순으로 만들어야 했다. 위치가 잘못된 원소들이 내림차순으로 배치되어 있어야 역순으로 배치하면 모든 원소가 제자리에 올 수 있을 것이라고 생각했다.

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n;
    cin >> n;

    vector<int> p(n);
    for (int& x : p) cin >> x;

    vector<bool> seen(n);
    for (int i = 0; i < n; i++) {
        if (p[i] == i + 1) seen[i] = true;
    }

    bool ok = true;
    int prv = n + 1;
    for (int i = 0; i < n; i++) {
        if (!seen[i]) {
            if (prv > p[i]) {
                prv = p[i];
            } else {
                ok = false;
            }
        }
    }

    cout << (ok ? "YES\n" : "NO\n");
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
> 풀이 → [[Codeforces] #2264A - Rumb Needs a Hand](/posts/codeforces-2264a/)
{: .prompt-tip }

---

### B. Knife's Pill Farm

인접한 원소 간 차가 포인트라고 생각했는데 이후에 막혔다. dp, 그리디 모두 아이디어가 안 떠올라서 많이 당황했다. 복잡도상 분명 선형 스캔으로 끝날 거 같고 뭔가 관찰로 해결할 수 있을 거 같았는데 감이 안 잡혔다.

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n, m;
    cin >> n >> m;

    vector<int> a(n);
    for (int& x : a) cin >> x;

    vector<int> diff(n);
    for (int i = 1; i < n; i++) {
        diff[i] = a[i] - a[i - 1];
    }
    vector<bool> chk(n, true);
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
> 풀이 → [[Codeforces] #2264B - Knife's Pill Farm](/posts/codeforces-2264b/)
{: .prompt-tip }

---

### C. Madamant's Skating Dynasty

대회 중 미시도.

---

### D. Dr. Agos's Dark Mode

대회 중 미시도.

---

### E1. A Prime Flood (Easy Version)

대회 중 미시도.

---

### E2. A Prime Flood (Hard Version)

대회 중 미시도.

---

### F. Deranged Calculator

대회 중 미시도.

---

## 총평

지금까지 봤던 대회 중 가장 못 봤다. A, B까지는 그냥 관찰로 발견하면 짧은 코드로 해결 가능하다고 믿었는데 약간 믿음이 깨지는 기분이었다. 결국은 둘 다 관찰이 맞았는데 B의 경우 `a`와 차를 가지고 자꾸 고민했던 게 큰 패착이었다. 좀 더 다양한 문제에 대한 훈련이 필요함을 느꼈다.

---
