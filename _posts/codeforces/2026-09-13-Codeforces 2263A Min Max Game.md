---
title: "[Codeforces] #2263A - Min Max Game [C++]"
date: 2026-09-13
categories: [PS, Codeforces]
tags: ["math", "game theory"]
slug: codeforces-2263a
media_subpath: /assets/img/posts/codeforces-2263a/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2263/A)
{: .prompt-info }

---

## 1. 아이디어

이진 배열에서 `"Bessie"`가 먼저 인접한 두 원소 중 더 큰 값으로, 이어서 `"Elsie"`가 인접한 두 원소 중 더 작은 값으로 합치는 걸 번갈아 반복해 하나만 남기는 게임인데, `"Bessie"`는 마지막 값이 `1`이길 바라고 `"Elsie"`는 `0`이길 바란다. 같은 값끼리 합치는 건 그저 중복 하나를 지울 뿐이라 영향이 없지만, `0`과 `1`을 합치면 `"Bessie"`의 차례엔 항상 `1`이, `"Elsie"`의 차례엔 항상 `0`이 남으므로 그 턴의 주인이 자기 값은 지키면서 상대 값을 하나 지울 수 있다는 점이 핵심이다. 따라서 최적 플레이에서는 서로 이 기회를 놓치지 않고 계속 상대 값을 깎는 싸움이 되고, 결국 누가 먼저 자기 값을 소진하느냐로 승패가 갈리니 `1`과 `0`의 개수를 단순 비교하면 된다. `"Bessie"`가 선공이라 개수가 같을 때도 유리해지므로 `1`의 개수가 `0`의 개수 이상이면 `"Bessie"`가 이긴다.

---

## 2. 복잡도

| 접근 | 시간            | 공간   |
| ---- | --------------- | ------ |
| 풀이 | $O(T \times N)$ | $O(1)$ |

($T$ = 테스트 케이스 수, $N$ = 케이스당 `n`의 최댓값)

---

## 3. 코드

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
