---
title: "Codeforces Round 1125 (Div. 3) 후기"
date: 2026-10-07
categories: [Contest]
tags: ["codeforces", "div 3"]
slug: codeforces-2275
media_subpath: /assets/img/posts/codeforces-2275/
image:
  path: preview.png
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [대회 링크](https://codeforces.com/contest/2275)
{: .prompt-info }

---

## 1. 대회 개요

| 항목      | 내용                           |
| --------- | ------------------------------ |
| 대회      | Codeforces Round 1125 (Div. 3) |
| 일시      | 2026-10-07 23:45 KST           |
| 배정 시간 | 150분                          |
| 문제 수   | 8 (A–H)                        |
| 참가 형태 | 공식 (rated)                   |

---

## 2. 결과

| 항목    | 내용                                                          |
| ------- | ------------------------------------------------------------- |
| 푼 문제 | 대회 중 A–C (3/8), 이후 D 업솔빙                              |
| 페널티  | 141분                                                         |
| 순위    | 6991 / 18322위 · 상위 38.2%                                   |
| 레이팅  | 1105 → 1145 (+40) · <span style="color:#808080">newbie</span> |

![레이팅 그래프](rating-graph.png)

---

## 3. 풀이 과정

| 문제                                                                                     | 결과   | 제출 시각 | WA  |
| ---------------------------------------------------------------------------------------- | ------ | --------- | --- |
| [A. In Search of Convenience](https://codeforces.com/problemset/problem/2275/A)          | AC     | 6:03      | 0   |
| [B. Did Not Go to Print](https://codeforces.com/problemset/problem/2275/B)               | AC     | 66:54     | 1   |
| [C. Unrequited Love](https://codeforces.com/problemset/problem/2275/C)                   | AC     | 59:42     | 0   |
| [D. Precision Alignment](https://codeforces.com/problemset/problem/2275/D)               | 업솔빙 | —         | —   |
| [E. Repentance Is Already on the Way](https://codeforces.com/problemset/problem/2275/E)  | 미시도 | —         | —   |
| [F. Tea Blend](https://codeforces.com/problemset/problem/2275/F)                         | 미시도 | —         | —   |
| [G. Copper Squander](https://codeforces.com/problemset/problem/2275/G)                   | 미시도 | —         | —   |
| [H. A Problem to Warm Up the Eyebrows](https://codeforces.com/problemset/problem/2275/H) | 미시도 | —         | —   |

---

### A. In Search of Convenience

`x` 또는 `y` 좌표에 `r`만 더하거나 빼는 게 가장 간단한 케이스인 걸 금방 찾았다.

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    int x, y, r;
    cin >> x >> y >> r;
    cout << x << ' ' << y + r << '\n';
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
> 풀이 → [[Codeforces] #2275A - In Search of Convenience](/posts/codeforces-2275a/)
{: .prompt-tip }

---

### B. Did Not Go to Print

스택으로 쓸 벡터 `v`랑 `'2'` 연산에서 출력이 안 되는 문서를 담는 벡터 `v2`를 활용했다. 같은 스택을 공유하는 줄 알아서 디버깅이 꽤 오래 걸렸다.

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n;
    string s;
    cin >> n >> s;

    vector<int> v;
    vector<int> v2;
    for (int i = 1; i <= n; i++) {
        int c = s[i - 1] - '0';
        if (c == 1) {
            v.push_back(i);
        } else if (c == 2) {
            if (!v.empty()) {
                v.pop_back();
                v2.push_back(i);
            }
        }
    }
    for (int x : v2) v.push_back(x);
    sort(v.begin(), v.end());

    cout << v.size() << '\n';
    for (int x : v) cout << x << ' ';
    cout << '\n';
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
> 풀이 → [[Codeforces] #2275B - Did Not Go to Print](/posts/codeforces-2275b/)
{: .prompt-tip }

---

### C. Unrequited Love

경우의 수를 구해야 하는데 브루트 포스로는 안 될 만한 숫자로 보여서 원리를 찾아보려고 했다. 중복만 고려하지 않으면 조합 공식으로 최종 개수는 빠르게 나와서 일단 구해 놓고 중복되는 화음을 누른 경우를 쭉 빼줬다.

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n;
    cin >> n;

    vector<int> a(n);
    for (int& x : a) cin >> x;

    unordered_map<int, long long> cnt;
    for (int i = 0; i < n - 4; i++) {
        cnt[a[i] + a[i + 2] - a[i + 4]]++;
    }

    long long ans = 0;
    for (auto [_, v] : cnt) {
        ans += v * (v - 1) / 2;
    }
    for (int i = 0; i < n - 6; i++) {
        if (a[i] + a[i + 2] - a[i + 4] == a[i + 2] + a[i + 4] - a[i + 6]) ans--;
    }
    for (int i = 0; i < n - 8; i++) {
        if (a[i] + a[i + 2] - a[i + 4] == a[i + 4] + a[i + 6] - a[i + 8]) ans--;
    }

    cout << ans << '\n';
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
> 풀이 → [[Codeforces] #2275C - Unrequited Love](/posts/codeforces-2275c/)
{: .prompt-tip }

---

### D. Precision Alignment

합이 작은 실험실부터 채워주는 평탄화 작업인데 +1을 하기 위해 조작을 약간 해줘야 하는 경우가 있는 것까지 알려줘서 조건 분기만 잘 하면 될 것 같았다. 약간의 조건 미스로 결국 못하고 업솔빙으로 넘어갔는데 조건만 맞춰도 해결이 되고, 심지어 매개변수 이분 탐색으로 더 간단한 방법이 있는 걸 보고 좀 놀랐다.

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n;
    long long k;
    cin >> n >> k;

    vector<pair<long long, long long>> v(n);
    for (int i = 0; i < n; i++) {
        long long a, b, c;
        cin >> a >> b >> c;

        v[i].first = a + b + c;
        if (a < b && b < c) {
            v[i].second = min(b - a, c - b) + 1;
        } else if ((a < b && b == c) || (a == b && b < c)) {
            v[i].second = b - a + 1;
        } else if (a == b && b == c) {
            v[i].second = -1;
        }
    }
    sort(v.begin(), v.end());

    for (int i = 1; i < n; i++) {
        auto [sum, cnt] = v[i];
        auto [psum, pcnt] = v[i - 1];

        if (pcnt == -1) {
            cout << psum << '\n';
            return;
        }
        if (pcnt > 0) {
            k -= pcnt * 2;
            if (k <= 0) {
                cout << psum << '\n';
                return;
            }
        }

        if (k < (sum - psum) * i) {
            cout << psum + k / i << '\n';
            return;
        }

        k -= (sum - psum) * i;
    }

    cout << v.back().first + k / n << '\n';
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
> 풀이 → [[Codeforces] #2275D - Precision Alignment](/posts/codeforces-2275d/)
{: .prompt-tip }

---

### E. Repentance Is Already on the Way

대회 중 미시도.

---

### F. Tea Blend

대회 중 미시도.

---

### G. Copper Squander

대회 중 미시도.

---

### H. A Problem to Warm Up the Eyebrows

대회 중 미시도.

---

## 총평

div 3 치고 약간 아쉬운 성적이었다. div 3에서 4솔 고정을 하고 싶은데 아직은 유형 숙달이 부족한 것 같다. 특히 D번은 이 정도 알고리즘까지 나올 줄 몰라서 약간 방심했는데 최소, 최대 쪽에서 매개변수 탐색이 종종 나오는 것으로 보여서 이에 대한 준비를 좀 해야 할 것 같다.

---
