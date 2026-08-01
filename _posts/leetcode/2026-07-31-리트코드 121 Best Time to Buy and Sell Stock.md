---
title: "[LeetCode] 121번 - Best Time to Buy and Sell Stock [Java][C++]"
slug: leetcode-121
date: 2026-07-31
categories: [PS, LeetCode]
tags: [greedy]
toc: true
math: true
---

[문제 링크](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/)

---

## 1. 아이디어

`i`번째 일의 주식 가격이 담긴 배열 `prices`에서 두 날을 골라서 앞 날에 주식을 사고 뒷 날에 주식을 팔 때 최대 수익을 구하는 문제다. 첫째 날부터 마지막 날까지 순회하며 현재 날 이전까지 등장했던 최소 주식 가격을 기억하고 있으면 해당 가격에 샀다고 치고 오늘 팔았을 때 수익을 구해서 이들 중 최댓값을 구하면 해당 값이 전체 `prices`에서 얻을 수 있는 최대 수익이 된다.

---

## 2. 복잡도

| 시간복잡도 | 공간복잡도 |
| :--------: | :--------: |
|   $O(N)$   |   $O(1)$   |

> $N$ = `prices` 길이

---

## 3. 코드

### 풀이 [Java][C++]

```java
class Solution {
    public int maxProfit(int[] prices) {
        int min = prices[0];
        int max = 0;

        for (int i = 1; i < prices.length; i++) {
            max = Math.max(max, prices[i] - min);
            min = Math.min(min, prices[i]);
        }

        return max;
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
        int mx = 0;

        for (int i = 1; i < prices.size(); i++) {
            mx = max(mx, prices[i] - mn);
            mn = min(mn, prices[i]);
        }

        return mx;
    }
};
```

---
