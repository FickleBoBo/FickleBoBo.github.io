---
title: "Educational Codeforces Round 194 (Rated for Div. 2) 후기"
date: 2026-09-08
categories: [Contest]
tags: ["codeforces", "div 2"]
slug: codeforces-2260
media_subpath: /assets/img/posts/codeforces-2260/
image:
  path: preview.png
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [대회 링크](https://codeforces.com/contest/2260)
{: .prompt-info }

---

## 1. 대회 개요

| 항목      | 내용                                                |
| --------- | --------------------------------------------------- |
| 대회      | Educational Codeforces Round 194 (Rated for Div. 2) |
| 일시      | 2026-09-08 23:35 KST                                |
| 배정 시간 | 120분                                               |
| 문제 수   | 7 (A–G)                                             |
| 참가 형태 | 공식 (rated)                                        |

---

## 2. 결과

| 항목    | 내용                                                         |
| ------- | ------------------------------------------------------------ |
| 푼 문제 | 대회 중 A–B (2/7), 이후 C 업솔빙                             |
| 페널티  | 100분                                                        |
| 순위    | 8720 / 14074위 · 상위 62.0%                                  |
| 레이팅  | 474 → 736 (+262) · <span style="color:#808080">newbie</span> |

![레이팅 그래프](rating-graph.png)

---

## 3. 풀이 과정

| 문제                                                                                     | 결과   | 제출 시각 | WA  |
| ---------------------------------------------------------------------------------------- | ------ | --------- | --- |
| [A. Monocarp's Contest](https://codeforces.com/problemset/problem/2260/A)                | AC     | 6:21      | 0   |
| [B. Monocarp and Projects](https://codeforces.com/problemset/problem/2260/B)             | AC     | 64:37     | 3   |
| [C. Maximize XOR, Minimize Operations](https://codeforces.com/problemset/problem/2260/C) | 업솔빙 | —         | —   |
| [D. Signs of Prefix Sums](https://codeforces.com/problemset/problem/2260/D)              | 미시도 | —         | —   |
| [E. Cyclic Balance](https://codeforces.com/problemset/problem/2260/E)                    | 미시도 | —         | —   |
| [F. Edge Three-Coloring](https://codeforces.com/problemset/problem/2260/F)               | 미시도 | —         | —   |
| [G. Sortable Permutations](https://codeforces.com/problemset/problem/2260/G)             | 미시도 | —         | —   |

---

### A. Monocarp's Contest

두 문제의 난이도를 바꿀 수 있을 때, 첫 번째 문제와 마지막 문제의 난이도를 쉽게 만들어야 했다. 중간 문제중 쉬운 문제의 수를 센 후 첫 번째 문제와 마지막 문제가 쉬운지 어려운지로 조건 분기하니 금방 해결됐다.

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n;
    cin >> n;

    vector<int> v(n);
    for (int& x : v) cin >> x;

    int cnt0 = count(v.begin() + 1, v.end() - 1, 0);

    if (v.front() == 0 && v.back() == 0) {
        cout << 0 << '\n';
        return;
    }
    if ((v.front() == 0 || v.back() == 0) && cnt0 >= 1) {
        cout << 1 << '\n';
        return;
    }
    if (cnt0 >= 2) {
        cout << 2 << '\n';
        return;
    }
    cout << -1 << '\n';
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
> 풀이 → [[Codeforces] #2260A - Monocarp's Contest](/posts/codeforces-2260a/)
{: .prompt-tip }

---

### B. Monocarp and Projects

`k`가 상당히 커서 브루트 포스로는 안 되고 관찰이 필요한 문제일 것 같았다. 몇 가지 케이스를 해보니 특정 시점부터는 나머지가 항상 똑같이 나와서 반복을 생략할 수 있는 것을 알았고 이걸로 앞부분은 반복하고 이 시점부터는 그냥 한방에 곱셈으로 해결할 수 있을 것 같았다. 접근 자체는 맞는 걸 확신했는데 계속 AC가 안 돼서 뭔가 경계 조건 문제나 반례가 있을 것 같았는데 경계 조건 문제도 있었고, `x`와 `y`의 차가 작을 때도 고려해야 한다는 것을 놓쳤다. 디버깅에 시간이 너무 많이 걸려서 좀 아쉬웠다.

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    long long x, y, k;
    cin >> x >> y >> k;

    long long sum = 0;
    if (y - 2 * x < 0) {
        sum += (y - x) * k;
    } else {
        if (y - 2 * x >= k) {
            for (int i = 0; i < k; i++) {
                sum += (y + i) % (x + i);
            }
        } else {
            for (int i = 0; i < y - 2 * x; i++) {
                sum += (y + i) % (x + i);
            }
            sum += (y - x) * (k - y + 2 * x - 1);
        }
    }

    cout << sum << '\n';
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
> 풀이 → [[Codeforces] #2260B - Monocarp and Projects](/posts/codeforces-2260b/)
{: .prompt-tip }

---

### C. Maximize XOR, Minimize Operations

최대는 분명 `x + y`일 때로 보였는데 연산 횟수를 브루트 포스없이 구하는 걸 찾는 게 좀 어려웠다. 분명 비트를 활용해 30번 언저리로 처리하는 것 같았는데 규칙이 잘 안 보였다. 이후 풀다가 앞에서부터 좀 뭉텅이로 던져주는 방식으로 느낌적으로 될 것 같았는데 시간이 좀 빠듯해서 마무리를 못했다. 아래 코드는 통과는 안 됐지만 업솔빙 과정에서는 `diff`를 `y`에서 해당 위치보다 작은 비트들만 구해서 빼주니 해결됐다. 이후 찾아보니 서브 마스크를 활용하면 훨씬 간단하게 해결되는 걸 알았다.

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    int x, y;
    cin >> x >> y;

    int sum = x + y;
    int k = 1 << 30;
    int cnt = 0;

    // while (k > 0 && (sum & k) == 0) k >>= 1;
    while (k > 0) {
        if (k & sum) {
            int tmp = (k & x) ^ (k & y);
            if (!tmp) {
                int diff = k - y;
                x -= diff;
                y += diff;
                cnt += diff;
            }
        }

        // cout << "k = " << k << '\n';
        k >>= 1;
    }

    cout << sum << ' ' << cnt << '\n';
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
> 풀이 → [[Codeforces] #2260C - Maximize XOR, Minimize Operations](/posts/codeforces-2260c/)
{: .prompt-tip }

---

### D. Signs of Prefix Sums

대회 중 미시도.

---

### E. Cyclic Balance

대회 중 미시도.

---

### F. Edge Three-Coloring

대회 중 미시도.

---

### G. Sortable Permutations

대회 중 미시도.

---

## 총평

대회 이후 조금 더 하니 C도 해결이 돼서 여러모로 좀 아쉬웠다. B 문제의 디버깅이 좀 빨랐으면 다르지 않았을까 하지만 결과는 결과이니 앞으로 좀만 침착하면 좋을 것 같다. 모듈러에 대한 성질, 비트 마스크 모두 코드포스에서는 자주 나오는 개념이지만 일반 코딩테스트에서는 잘 안 나와서 아직은 코포 유형에 적응이 좀 부족하다는 게 크게 느껴졌다.

---
