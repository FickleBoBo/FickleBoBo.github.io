---
title: "Codeforces Round 1122 (Div. 3) 후기"
date: 2026-09-21
categories: [Contest]
tags: ["codeforces", "div 3"]
slug: codeforces-2266
media_subpath: /assets/img/posts/codeforces-2266/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [대회 링크](https://codeforces.com/contest/2266)
{: .prompt-info }

---

## 1. 대회 개요

| 항목      | 내용                           |
| --------- | ------------------------------ |
| 대회      | Codeforces Round 1122 (Div. 3) |
| 일시      | 2026-09-21 23:35 KST           |
| 배정 시간 | 150분                          |
| 문제 수   | 8 (A–H)                        |
| 참가 형태 | 공식 (rated)                   |

---

## 2. 결과

| 항목    | 내용                                                          |
| ------- | ------------------------------------------------------------- |
| 푼 문제 | 대회 중 A–C (3/8), 이후 D 업솔빙                              |
| 페널티  | 162분                                                         |
| 순위    | 9176 / 20851위 · 상위 44.0%                                   |
| 레이팅  | 1043 → 1105 (+62) · <span style="color:#808080">newbie</span> |

![레이팅 그래프](rating-graph.png)

---

## 3. 풀이 과정

| 문제                                                                     | 결과   | 제출 시각 | WA  |
| ------------------------------------------------------------------------ | ------ | --------- | --- |
| [A. Good Contest](https://codeforces.com/problemset/problem/2266/A)      | AC     | 20:17     | 0   |
| [B. Three Piles](https://codeforces.com/problemset/problem/2266/B)       | AC     | 28:45     | 0   |
| [C. AND, OR, Sort!](https://codeforces.com/problemset/problem/2266/C)    | AC     | 104:22    | 1   |
| [D. Falling Concrete](https://codeforces.com/problemset/problem/2266/D)  | 업솔빙 | —         | —   |
| [E. Prime Destruction](https://codeforces.com/problemset/problem/2266/E) | 미시도 | —         | —   |
| [F. MEX Replacement](https://codeforces.com/problemset/problem/2266/F)   | 미시도 | —         | —   |
| [G. Modular Tree](https://codeforces.com/problemset/problem/2266/G)      | 미시도 | —         | —   |
| [H. Deque Malfunction](https://codeforces.com/problemset/problem/2266/H) | 미시도 | —         | —   |

---

### A. Good Contest

세 문제를 모두 풀지 못한 사람의 최솟값을 구해야 하는데 이는 세 문제를 모두 푼 사람의 최댓값을 구하면 구할 수 있다. 세 문제를 모두 푼 사람의 최댓값은 $a_1$, $a_2$, $a_3$ 중 최솟값만큼까지 가능하므로 `n`에서 해당 값을 빼면 됐다.

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n, a1, a2, a3;
    cin >> n >> a1 >> a2 >> a3;
    cout << n - min({a1, a2, a3}) << '\n';
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
> 풀이 → [[Codeforces] #2266A - Good Contest](/posts/codeforces-2266a/)
{: .prompt-tip }

---

### B. Three Piles

Alice와 Bob, 더미까지 총 세 개의 파일이 있고 각자 최선의 전략을 펼쳐야 해서 게임 이론 문제구나 했다. Alice와 Bob의 현재 파일 상태에 따라 전략을 다르게 취해야 할 것 같았는데 Alice가 Bob보다 파일이 크거나 같으면 더미를 다 가져가는 게 유리하므로 다 가져갔고, Alice보다 Bob의 파일이 많으면 전부 가져가는 게 나을 때는 전부 가져갔고 아닐 경우 안 가져갔다.

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    long long a, b, c;
    cin >> a >> b >> c;

    if (a < b) {
        if (abs(a + c - b) > abs(a - b)) {
            cout << abs(a + c - b) << '\n';
        } else {
            cout << abs(a - b) << '\n';
        }
    } else {
        cout << abs(a + c - b) << '\n';
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
> 풀이 → [[Codeforces] #2266B - Three Piles](/posts/codeforces-2266b/)
{: .prompt-tip }

---

### C. AND, OR, Sort!

이진 문자열 `s`를 오름차순으로 정렬하는 문제로 특정 비트를 바꿀 수 있는데 해당 비트부터 이전에 등장한 모든 비트까지의 비트 AND 연산이나 비트 OR 연산의 결과로 바꿀 수 있었다. 몇 번 해보니 첫 비트가 1인 경우와 아닌 경우로 나눌 수 있었고 첫 비트가 1이 아니면 이후 등장한 1 이후의 비트는 해당 비트 포함 원하는 비트로 변경할 수 있었다. 원리 자체는 금방 찾았는데 최소 케이스를 구현하는 게 오래 걸렸고 최소 케이스는 누적 합의 아이디어가 좀 필요했다.

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n;
    string s;
    cin >> n >> s;

    int ans = count(s.begin(), s.end(), '0');
    if (s[0] == '1') {
        cout << ans << '\n';
    } else {
        vector<int> cnt0(n + 1);
        for (int i = n - 1; i >= 0; i--) {
            cnt0[i] += cnt0[i + 1];
            if (s[i] == '0') cnt0[i]++;
        }
        vector<int> cnt1(n + 1);
        for (int i = 1; i < n; i++) {
            cnt1[i] += cnt1[i - 1];
            if (s[i] == '1') cnt1[i]++;
        }

        for (int i = 1; i < n; i++) {
            if (s[i] == '1') {
                ans = min({ans, cnt0[i + 1] + cnt1[i - 1]});
            }
        }
        ans = min({ans, cnt1[n - 1]});

        cout << ans << '\n';
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
> 풀이 → [[Codeforces] #2266C - AND, OR, Sort!](/posts/codeforces-2266c/)
{: .prompt-tip }

---

### D. Falling Concrete

시간이 거의 없었는데 뭔가 관찰로 쉽게 풀릴 거 같아서 도전했다. 처음엔 적당히 평탄화가 잘 될 줄 알았는데 세 번째 테케를 보고 쉽지 않구나 생각하고 포기했다.

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n;
    cin >> n;

    int sum = 0;
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        sum += x;
    }

    cout << sum % n << '\n';
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
> 풀이 → [[Codeforces] #2266D - Falling Concrete](/posts/codeforces-2266d/)
{: .prompt-tip }

---

### E. Prime Destruction

대회 중 미시도.

---

### F. MEX Replacement

대회 중 미시도.

---

### G. Modular Tree

대회 중 미시도.

---

### H. Deque Malfunction

대회 중 미시도.

---

## 총평

Codyssey 일정으로 대회 참여를 15분 정도 늦게 해서 문제 풀이가 좀 늦었다. 대회를 마치고 보니 D번 문제는 대회 중에 풀 만한 난이도는 아니었던 거 같아서 그냥 실력만큼 본 거 같다. 다만 C번 문제에 대한 구현이 너무 느렸던 게 약간은 아쉬웠다. 코드포스 대회 배치고사가 6회 정도라는 클로드 피셜 때문에 배치 단계에서 뉴비를 탈출하고 싶었는데 약간 아슬아슬한 거 같다.

---
