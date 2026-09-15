---
title: "[LeetCode] #121 - Best Time to Buy and Sell Stock [Java][C++][Python]"
date: 2026-09-15
categories: [PS, LeetCode]
tags: ["greedy"]
slug: leetcode-121
media_subpath: /assets/img/posts/leetcode-121/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/)
{: .prompt-info }

---

## 1. 아이디어

주가가 저장된 배열 `prices`가 주어졌을 때, 임의의 두 날을 골라서 앞 날에 사고 뒷 날에 팔아서 수익을 최대화해야 하는 문제다.

두 번째 날부터 마지막 날까지 `i`일에 주식을 판다고 생각하면 각 `i`일에 최대 수익을 얻으려면 첫 번째 날부터 `i - 1`일 중 가장 주가가 쌀 때 사고 `i`일에 팔아야 한다. 따라서 1일부터 `i - 1`일까지 중 최솟값을 매번 저장 갱신하며 최대 수익을 탐색해나가면 된다.

---

## 2. 복잡도

| 접근 | 시간   | 공간   |
| ---- | ------ | ------ |
| 풀이 | $O(N)$ | $O(1)$ |

($N$ = `prices`의 길이)

---

## 3. 코드

### 풀이 [Java][C++][Python]

```java
class Solution {
    public int maxProfit(int[] prices) {
        int min = prices[0];
        int diff = 0;
        for (int i = 1; i < prices.length; i++) {
            diff = Math.max(diff, prices[i] - min);
            min = Math.min(min, prices[i]);
        }

        return diff;
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

class Solution {
   public:
    int maxProfit(vector<int>& prices) {
        int mn = prices[0];
        int diff = 0;
        for (int i = 1; i < prices.size(); i++) {
            diff = max(diff, prices[i] - mn);
            mn = min(mn, prices[i]);
        }

        return diff;
    }
};
```

```python
class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        mn = prices[0]
        diff = 0
        for p in prices[1:]:
            diff = max(diff, p - mn)
            mn = min(mn, p)

        return diff
```

---
