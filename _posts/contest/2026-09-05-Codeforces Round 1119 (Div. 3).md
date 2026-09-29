---
title: "Codeforces Round 1119 (Div. 3) 후기"
date: 2026-09-05
categories: [Contest]
tags: ["codeforces", "div 3"]
slug: codeforces-2259
media_subpath: /assets/img/posts/codeforces-2259/
image:
  path: preview.png
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [대회 링크](https://codeforces.com/contest/2259)
{: .prompt-info }

---

## 1. 대회 개요

| 항목      | 내용                           |
| --------- | ------------------------------ |
| 대회      | Codeforces Round 1119 (Div. 3) |
| 일시      | 2026-09-05 23:45 KST           |
| 배정 시간 | 135분                          |
| 문제 수   | 8 (A–H)                        |
| 참가 형태 | 공식 (rated)                   |

---

## 2. 결과

| 항목    | 내용                                                                  |
| ------- | --------------------------------------------------------------------- |
| 푼 문제 | 대회 중 A–D (4/8), 이후 E 업솔빙                                      |
| 페널티  | 188분                                                                 |
| 순위    | 5272 / 19146위 · 상위 27.5%                                           |
| 레이팅  | 100 → 474 (+374, 첫 대회) · <span style="color:#808080">newbie</span> |

![레이팅 그래프](rating-graph.png)

---

## 3. 풀이 과정

| 문제                                                                                                   | 결과   | 제출 시각 | WA  |
| ------------------------------------------------------------------------------------------------------ | ------ | --------- | --- |
| [A. Moo Language School](https://codeforces.com/problemset/problem/2259/A)                             | AC     | 14:23     | 0   |
| [B. Minus Two](https://codeforces.com/problemset/problem/2259/B)                                       | AC     | 22:22     | 0   |
| [C. 101](https://codeforces.com/problemset/problem/2259/C)                                             | AC     | 38:46     | 0   |
| [D. MEX Multiset](https://codeforces.com/problemset/problem/2259/D)                                    | AC     | 104:54    | 1   |
| [E. Treasure Map Destruction (Constructive Version)](https://codeforces.com/problemset/problem/2259/E) | 업솔빙 | —         | —   |
| [F. Binary Bubble Sort Inversions](https://codeforces.com/problemset/problem/2259/F)                   | 미시도 | —         | —   |
| [G. Index Removal](https://codeforces.com/problemset/problem/2259/G)                                   | 미시도 | —         | —   |
| [H. Treasure Map Destruction (Counting Version)](https://codeforces.com/problemset/problem/2259/H)     | 미시도 | —         | —   |

---

### A. Moo Language School

`n`개의 문자들을 `k`개 단위로 끊어서 각 청크별로 전부 `1`인지 판단하면 됐다. 독해력 이슈로 생각보다 오래 걸렸는데 알고 보니 간단한 문제였다.

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n, k;
    string s;
    cin >> n >> k >> s;

    int cnt = 0;
    for (int i = 0; i < n; i += k) {
        bool flag = false;
        for (int j = i; j < i + k; j++) {
            if (s[j] == '0') flag = true;
        }

        if (!flag) cnt++;
    }

    cout << cnt << '\n';
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
> 풀이 → [[Codeforces] #2259A - Moo Language School](/posts/codeforces-2259a/)
{: .prompt-tip }

---

### B. Minus Two

수식이 약간 특이했는데 무한히 시행하면 `0`, `1`, `2` 중 하나가 된다는 규칙을 발견했다. 홀수는 `1`, 짝수는 `0` 또는 `2`를 엇박으로 진동한다는 점에서 3그룹으로 분류했다.

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n;
    cin >> n;

    int odd = 0, even1 = 0, even2 = 0;
    while (n--) {
        int x;
        cin >> x;

        if (x % 2) {
            odd++;
        } else {
            if (x / 2 % 2) {
                even1++;
            } else {
                even2++;
            }
        }
    }

    cout << max({odd, even1, even2}) << '\n';
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
> 풀이 → [[Codeforces] #2259B - Minus Two](/posts/codeforces-2259b/)
{: .prompt-tip }

---

### C. 101

가급적 `-1`을 `0`으로 바꾸는 게 이득인데 부득이하게 `1`로 바꿔야 하는 순간들이 있는 것을 알았다. 양 끝에서부터 `-1` 또는 `1`이 나오는 위치를 찾고 그 사이의 `-1`은 전부 `0`으로, 해당 끝들은 `1`로 바꾸는 것이 최적인 것으로 생각했다.

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n;
    cin >> n;

    vector<int> v(n);
    for (int& x : v) cin >> x;

    int s = -1, e = -1;
    for (int i = 0; i < v.size(); i++) {
        if (v[i] != 0) {
            s = i;
            break;
        }
    }
    for (int i = (int)v.size() - 1; i >= 0; i--) {
        if (v[i] != 0) {
            e = i;
            break;
        }
    }
    for (int i = s + 1; i < e; i++) {
        if (v[i] == -1) v[i] = 0;
    }

    if (s != -1) {
        v[s] = v[e] = 1;
    }

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
> 풀이 → [[Codeforces] #2259C - 101](/posts/codeforces-2259c/)
{: .prompt-tip }

---

### D. MEX Multiset

스프라그 그런디 정리에서 MEX 함수를 본 적이 있어서 특별한 성질이 있을 것으로 생각하고 이를 발견하려고 하다가 시간을 많이 썼다. MEX는 해당 집합에 포함되지 않는 가장 작은 음이 아닌 정수라는 점에서 혹시 초반 몇 개의 수로 이미 결정나지 않을까 했고 한 집합에 모든 수를 몰아 넣고 작은 수부터 분배를 해보다가 `0`의 개수에 따라 갈리는 것을 알았다. 아이디어를 떠올리기 꽤 어려운 문제였던 것 같다.

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n;
    cin >> n;

    vector<int> v(n);
    for (int& x : v) cin >> x;

    int cnt0 = count(v.begin(), v.end(), 0);

    if (cnt0 != 1) {
        bool vis = false;
        cout << "YES\n";
        for (int x : v) {
            if (x > 0) {
                cout << 'A';
            } else {
                if (!vis) {
                    cout << 'B';
                    vis = true;
                } else {
                    cout << 'C';
                }
            }
        }
        cout << '\n';
    } else {
        cout << "NO\n";
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
> 풀이 → [[Codeforces] #2259D - MEX Multiset](/posts/codeforces-2259d/)
{: .prompt-tip }

---

### E. Treasure Map Destruction (Constructive Version)

얼핏 보면 간단해 보였는데 `-1`을 어떤 수로 바꿀지 감이 안 왔다. 가장 큰 수부터 좌우를 내림차순으로 배치하는 약간 그리디한 접근을 떠올렸는데 해결이 안 됐고 시간도 타이트해서 포기했다. 이후 업솔빙에서 차분 배열로 보물이 배치될 수 없는 곳을 거른 후 남은 곳에 전부 배치하고 모순을 찾는 로직에서 난이도가 많이 높았다고 느꼈다.

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n;
    cin >> n;

    vector<int> v(n);
    for (int& x : v) cin >> x;

    vector<bool> vis(n);

    bool ok = true;

    priority_queue<pair<int, int>, vector<pair<int, int>>> pq;
    for (int i = 0; i < v.size(); i++) {
        pq.push({v[i], i});
    }

    while (!pq.empty()) {
        auto [pos, idx] = pq.top();
        pq.pop();
    }

    for (int i = 0; i < v.size(); i++) {
        if (v[i] == 0) {
            ans[i] = 1;
        }
    }

    if (ok) {
        vector<int> ans(n);
        for (int x : ans) {
            cout << x;
        }
        cout << '\n';
    } else {
        cout << -1;
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
> 풀이 → [[Codeforces] #2259E - Treasure Map Destruction (Constructive Version)](/posts/codeforces-2259e/)
{: .prompt-tip }

---

### F. Binary Bubble Sort Inversions

대회 중 미시도.

---

### G. Index Removal

대회 중 미시도.

---

### H. Treasure Map Destruction (Counting Version)

대회 중 미시도.

---

## 총평

첫 대회치고는 무난하게 풀어낸 것 같아서 나름 만족스러운 대회였다. D번 문제에서 시간을 많이 쓴 것이 처음엔 좀 아쉬웠는데 E번 문제를 업솔빙하며 E번은 시간을 아무리 줘도 못 풀었을 것 같아서 풀 수 있는 만큼 풀었던 것 같다. 전반적으로 그리디한 느낌의 문제들과 해 구성하기 유형이 많았던 것 같고 백준, 프로그래머스, 리트코드 같은 플랫폼이랑 문제 스타일이 확실히 좀 달랐던 것 같다. 코드포스는 관찰이나 인사이트가 중요한 문제들이 좀 있다고 했는데 딱 그런 느낌이었다.

---
