---
title: "[Codeforces] #2266D - Falling Concrete [C++]"
date: 2026-09-22
categories: [PS, Codeforces]
tags: ["constructive", "sorting"]
slug: codeforces-2266d
media_subpath: /assets/img/posts/codeforces-2266d/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2266/D)
{: .prompt-info }

---

## 1. 아이디어

길이 `n`인 배열 `a`에서 두 위치 $i < j$를 골라 $j$번째 칸을 $i$번째 자리로 옮기는 연산을 원하는 만큼 반복해, 만들 수 있는 가장 긴 평평한(높이가 모두 같은) 연속 구간의 길이를 구하는 문제다. 이때 옮겨진 칸은 높이가 $j - i$만큼 줄고, 그 사이에 있던 나머지 칸들은 한 칸씩 뒤로 밀리며 높이가 1씩 는다.

이걸 잘 관찰해보면 이동을 한 후 인덱스의 변화량이 높이의 변화량과 같다는 점을 알 수 있다. 즉 $a_k - k$는 시프트 전후 값은 변하지 않고 자리만 이동하는 꼴이 된다. 따라서 $b_i = a_i - i$로 정의하면 이 연산은 배열 `b`의 특정 구간의 원소들을 시프트만 한 꼴이 되며 크기가 2인 구간으로 잡으면 배열 `b`의 원소를 버블 정렬처럼 아무렇게나 재배치할 수 있다.

배열 `a`에서 연산 이후 만들 수 있는 평평한 연속 구간의 최대 길이는 배열 `b`에서 만들 수 있는 단조 증가하는 수열의 최대 길이로 볼 수 있고 따라서 배열 `b`에서 1씩 증가하는 가장 긴 수열의 길이를 구하면 원하는 값을 구할 수 있다.

---

## 2. 복잡도

| 접근 | 시간          | 공간   |
| ---- | ------------- | ------ |
| 풀이 | $O(N \log N)$ | $O(N)$ |

($N$ = 모든 테스트 케이스에 걸친 `n`의 총합)

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
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        b[i] = x - (i + 1);
    }

    sort(b.begin(), b.end());
    b.erase(unique(b.begin(), b.end()), b.end());

    int ans = 1, len = 1;
    for (int i = 1; i < b.size(); i++) {
        len = (b[i] == b[i - 1] + 1) ? len + 1 : 1;
        ans = max(ans, len);
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

`b`를 벡터로 받은 후 정렬한 뒤 `erase`와 `unique`를 통해 중복을 제거했다. 이후 단조 증가하는 최대 길이를 `len`과 `ans`로 갱신하며 최대 길이를 구했다.

---
