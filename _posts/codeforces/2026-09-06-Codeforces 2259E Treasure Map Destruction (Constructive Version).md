---
title: "[Codeforces] #2259E - Treasure Map Destruction (Constructive Version) [C++]"
date: 2026-09-06
categories: [PS, Codeforces]
tags: ["difference array", "greedy", "constructive"]
slug: codeforces-2259e
media_subpath: /assets/img/posts/codeforces-2259e/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2259/E)
{: .prompt-info }

---

## 1. 아이디어

원래 배열 `a`에서 `a[i]`는 섬 `i`에서 가장 가까운 보물 섬까지의 거리이고, 주어지는 `b`는 그중 일부가 `-1`로 지워진 것이다. 섬은 일직선상에 놓여 있고, `-1`이 아닌 값을 전부 만족하는 보물 배치를 아무거나 찾거나 그런 배치가 없으면 -1을 출력하면 되는 문제다.

`b[i]`가 양수라면 섬 `i`로부터 거리가 `b[i]` 미만인 위치에는 보물이 놓일 수 없다. 그런 위치에 보물이 있으면 최단 거리가 `b[i]`보다 작아져 모순이기 때문이다. 그래서 `b[i]`가 양수인 원소마다 좌우로 `b[i] - 1`칸씩 보물을 놓을 수 없다고 표시했는데, 이걸 그대로 반복하면 TLE가 나므로 차분 배열에 양 끝만 남기고 한 번에 누적했다.

차분 배열을 누적해 값이 `0`인 칸이 보물을 놓을 수 있는 칸이다. `b[i]`가 양수인 칸은 자기 제약이 자기 위치까지 금지하므로, 놓을 수 있는 칸에 남는 건 `b[i]`가 `0`이거나 `-1`인 경우뿐이다. `b[i]`가 `0`이면 섬 `i` 자체가 보물이어야 하니 반드시 놓고, `-1`이면 놓든 말든 자유지만 전부 놓았다. 보물은 많이 놓을수록 모든 섬의 최단 거리를 줄이기만 하고, 거리가 줄어들면 안 되는 위치는 이미 금지로 비워뒀으므로, 놓을 수 있는 칸을 전부 채우는 편이 뒤의 검사에 가장 유리하다.

배치가 끝나면 `b`가 애초에 모순인지 확인한다. 먼저 `b[i]`가 `0`인데 금지로 표시된 칸은 `-1`을 어떻게 채우든 섬 `i`에 보물을 놓을 수 없으므로 바로 -1을 출력했다.

다음으로 `b[i]`가 양수인 칸마다 거리가 정확히 `b[i]`인 위치, 즉 일직선상에서 `i - b[i]`와 `i + b[i]` 두 곳 중 하나에 보물이 실제로 놓였는지를 봤다. 놓을 수 있는 칸은 이미 다 채웠으니 두 곳이 모두 비어 있다면 남은 자리는 전부 금지 구역이라 어떤 배치로도 `b[i]`를 맞출 수 없다. 이 경우에도 -1을 출력하고, 모든 칸이 통과하면 만들어진 배치가 답이다.

---

## 2. 복잡도

| 접근 | 시간   | 공간   |
| ---- | ------ | ------ |
| 풀이 | $O(N)$ | $O(N)$ |

($N$ = 모든 테스트 케이스에 걸친 섬의 수의 총합)

---

## 3. 코드

### 풀이 [C++]

```c++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n;
    cin >> n;

    vector<int> b(n);
    for (int& x : b) cin >> x;

    vector<int> diff(n + 1);
    for (int i = 0; i < n; i++) {
        if (b[i] > 0) {
            diff[max(i - b[i] + 1, 0)]++;
            diff[min(i + b[i], n)]--;
        }
    }
    for (int i = 1; i <= n; i++) {
        diff[i] += diff[i - 1];
    }

    string ans(n, '0');
    for (int i = 0; i < n; i++) {
        if (diff[i] == 0) ans[i] = '1';
    }

    for (int i = 0; i < n; i++) {
        if (b[i] == 0 && ans[i] == '0') {
            cout << -1 << '\n';
            return;
        }
    }

    for (int i = 0; i < n; i++) {
        if (b[i] <= 0) continue;
        int l = i - b[i], r = i + b[i];
        if (!((l >= 0 && ans[l] == '1') || (r < n && ans[r] == '1'))) {
            cout << -1 << '\n';
            return;
        }
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

---
