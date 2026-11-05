---
title: "[Codeforces] #2263A - Min Max Game [C++]"
date: 2026-09-13
categories: [PS, Codeforces]
tags: ["math", "game theory"]
slug: codeforces-2263a
media_subpath: /assets/img/posts/codeforces-2263a/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2263/A)
{: .prompt-info }

---

## 1. 아이디어

`1`의 개수에서 `0`의 개수를 뺀 값을 $d$라 하자. 한 번 둘 때마다 원소가 정확히 하나 사라지므로 $d$는 매번 1씩 변하고, 원소가 하나 남았을 때 $d$는 1이면 `1`, $-1$이면 `0`이 남은 것이다. 그러니 $d$의 부호를 누가 지키는지가 승부를 가른다.

Bessie는 `0`이 있으면 그것을 이웃과 `max`로 합쳐 `0` 하나를 없애 $d$를 1 늘릴 수 있다(이웃이 `1`이면 `1`이, `0`이면 `0`이 남는다). Elsie도 `1`이 있으면 이웃과 `min`으로 합쳐 `1` 하나를 없애 $d$를 1 줄일 수 있다.

Bessie 차례가 시작될 때 $d \ge 0$이면 Bessie가 이긴다. 그녀가 $d \ge 1$로 만들고(`0`이 없다면 이미 `1`만 남은 상태다) Elsie가 아무리 줄여도 $d \ge 0$이라, 이 상태가 끝까지 유지된다. Bessie가 마지막 수를 두면 $d \ge 1$이고 Elsie가 두면 $d \ge 0$인데 원소가 하나 남았을 때 $d$는 1이나 $-1$이므로, 어느 쪽이든 남은 하나는 `1`이다.

반대로 $d < 0$이면 Elsie가 이긴다. Bessie가 $d \le 0$까지 올려도 Elsie가 다시 $d < 0$으로 내리고(`1`이 없다면 이미 `0`만 남은 상태다), 이 상태가 유지되어 남은 하나는 `0`이다.

따라서 `1`의 개수가 `0`의 개수 이상일 때만 Bessie가 이긴다.

---

## 2. 코드

### 풀이 [C++]

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

    cout << (cnt[1] >= cnt[0] ? "Bessie\n" : "Elsie\n");
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
