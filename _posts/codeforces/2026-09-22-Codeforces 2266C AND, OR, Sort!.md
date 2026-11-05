---
title: "[Codeforces] #2266C - AND, OR, Sort! [C++]"
date: 2026-09-22
categories: [PS, Codeforces]
tags: ["ad hoc"]
slug: codeforces-2266c
media_subpath: /assets/img/posts/codeforces-2266c/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2266/C)
{: .prompt-info }

---

## 1. 아이디어

연산 하나는 문자 하나만 바꾸고, 첫 문자는 접두사가 자기뿐이라 바뀌지 않는다. 정렬된 결과는 `0...01...1` 꼴이고, 달라지는 문자마다 연산이 한 번은 필요하다.

첫 문자가 `1`이면 결과는 `1`만 남은 문자열이다. 접두사에 항상 `1`이 있어 OR이 `1`을 주므로, `0`마다 한 번씩 바꿔 `0`의 개수만큼 걸린다.

첫 문자가 `0`이면 결과는 `1`이 하나도 없어도 되는 `0...01...1` 꼴이다. 접두사에 첫 문자 `0`이 있어 AND로 어느 `1`이든 한 번에 `0`으로 바꿀 수 있는 반면, `0`을 `1`로 바꾸려면 접두사에 `1`이 있어야 한다.

결과의 `1` 구간이 처음부터 있던 `1` 하나에서 시작한다고 하자. 그러면 뒤의 `0`은 접두사의 그 `1`과 OR해 `1`로, 앞의 `1`은 첫 문자 `0`과 AND해 `0`으로 바꾸면 되어, (앞의 `1`의 개수) + (뒤의 `0`의 개수)번이면 충분하다. 달라지는 문자마다 한 번은 필요하므로 이보다 적게는 안 된다.

`1` 구간이 원래 `0`인 자리에서 시작하는 경우는 따질 필요가 없다. 그 자리를 `1`로 바꾸는 한 번이 더 들고, 그 뒤 첫 `1`에서 시작하는 편이 앞의 `1`의 개수는 같고 뒤의 `0`은 줄어 항상 적게 들기 때문이다. 뒤에 `1`이 없으면 앞의 `1`이 전부라, `1`을 전부 `0`으로 바꾸는 편이 한 번 덜 든다.

따라서 `1`마다 (앞의 `1`의 개수) + (뒤의 `0`의 개수)를 구하고, `1`을 전부 `0`으로 바꾸는 `1`의 개수와 비교해 최솟값을 답으로 한다.

---

## 2. 코드

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
