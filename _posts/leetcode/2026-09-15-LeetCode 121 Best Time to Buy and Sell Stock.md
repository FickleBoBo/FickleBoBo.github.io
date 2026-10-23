---
title: "[LeetCode] #121 - Best Time to Buy and Sell Stock [Java][C++][Python]"
date: 2026-09-15
categories: [PS, LeetCode]
tags: ["greedy"]
slug: leetcode-121
media_subpath: /assets/img/posts/leetcode-121/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/)
{: .prompt-info }

---

## 1. 아이디어

일별 주가가 주어질 때, 한 번 사고 그 이후에 한 번 팔아 얻을 수 있는 최대 이익을 구하는 문제다(이익을 낼 수 없으면 0이다). 날 수를 $n$이라 하면 모든 (사는 날, 파는 날) 쌍을 보는 방법은 $O(n^2)$이라 $n \le 10^5$에서 시간 초과다. 파는 날을 하루 고정할 때 그보다 앞선 날 중 가장 싼 날에 사는 것이 최선이니, 파는 날마다 앞선 날들의 최저가만 알면 그날 팔았을 때의 최대 이익이 정해진다. 그래서 첫날부터 훑으며 앞선 날들의 최저가를 들고 가면 각 날이 파는 날일 때의 최대 이익을 바로 구할 수 있고, 그 값들의 최댓값이 답이다.

---

## 2. 코드

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
