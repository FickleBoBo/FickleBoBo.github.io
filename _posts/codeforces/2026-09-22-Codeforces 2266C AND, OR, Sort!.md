---
title: "[Codeforces] #2266C - AND, OR, Sort! [C++]"
date: 2026-09-22
categories: [PS, Codeforces]
tags: ["prefix sum", "string"]
slug: codeforces-2266c
media_subpath: /assets/img/posts/codeforces-2266c/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2266/C)
{: .prompt-info }

---

## 1. 아이디어

이진 문자열 `s`가 주어질 때, 위치 `i`를 골라 `s[i]`를 `s[0]`부터 `s[i]`까지의 비트 AND 또는 비트 OR 값으로 바꾸는 연산을 원하는 만큼 반복해 `s`를 비내림차순으로 만드는 데 필요한 최소 연산 횟수를 구하는 문제다.

비내림차순 이진 문자열은 앞쪽이 전부 `0`, 뒤쪽이 전부 `1`인 형태뿐이다. 일단 전체를 `1`로 만드는 극단을 기준으로 잡으면 원래 `0`이던 자리 하나하나가 비트 OR로 바꿔야 할 대상이라 비용은 전체 `0`의 개수다. `s[0]`이 `1`이면 `s[0]`을 포함하는 모든 구간의 OR이 항상 `1`이라 이 극단 말고는 만들 수 있는 형태가 없으므로, 답은 그대로 전체 `0`의 개수다.

`s[0]`이 `0`이면 앞쪽 일부를 `0`으로 남겨두는 형태도 가능해진다. 왼쪽부터 훑으면서, 원래 `0`인 자리를 지나면 그 자리는 `0`-영역에 그대로 남겨두면 되니 비용에서 뺀다. 원래 `1`인 자리를 지날 땐 지금 여기서 `0`-영역을 멈춘다면(이 `1`을 그대로 둔다면) 드는 비용을 확인해두고, `0`-영역을 더 늘릴 경우를 대비해 이 `1`을 비트 AND로 되돌려야 할 대상으로 쌓아 둔다. 이렇게 매 `1`의 자리에서 확인한 값과 끝까지 다 `0`-영역으로 미는 경우(원래 `1`의 총 개수)를 통틀어 가장 작은 값이 답이다.

---

## 2. 복잡도

| 접근 | 시간   | 공간   |
| ---- | ------ | ------ |
| 풀이 | $O(N)$ | $O(N)$ |

($N$ = 모든 테스트 케이스에 걸친 `s`의 길이의 총합)

---

## 3. 코드

### 풀이 [C++]

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n;
    string s;
    cin >> n >> s;

    int cnt0 = count(s.begin(), s.end(), '0');
    if (s[0] == '1') {
        cout << cnt0 << '\n';
    } else {
        int ans = cnt0;
        int cnt1 = 0;
        for (int i = 0; i < n; i++) {
            if (s[i] == '0') {
                cnt0--;
            } else {
                ans = min(ans, cnt0 + cnt1);
                cnt1++;
            }
        }
        ans = min(ans, cnt1);

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

---
