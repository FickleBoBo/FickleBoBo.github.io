---
title: "[LeetCode] #198 - House Robber [Java][C++][Python]"
date: 2026-09-04
categories: [PS, LeetCode]
tags: ["dynamic programming"]
slug: leetcode-198
media_subpath: /assets/img/posts/leetcode-198/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/house-robber/)
{: .prompt-info }

---

## 1. 아이디어

일렬로 배치된 집들이 주어지고 도둑이 연결된 두 집을 동시에 털 수 없을 때 얻을 수 있는 최대 금액을 구하는 문제로 다이나믹 프로그래밍을 활용하면 해결할 수 있다.

`dp[i]`를 첫 번째 집부터 `i`번째 집까지를 고려했을 때, 얻을 수 있는 최대 금액으로 정의하면 `i`번째 집을 안 터는 경우는 `i - 1`번째 집을 털 수도 있으므로 `dp[i - 1]`이 최대 금액이 되고, `i`번째 집을 털 경우는 `i - 1`번째 집은 털 수 없으므로 `i - 2`번째 집을 터는 경우까지 고려한 `dp[i - 2]`에 `nums[i - 1]`을 더한 값 중 최댓값이 `dp[i]`가 된다.

---

## 2. 복잡도

| 접근 | 시간   | 공간   |
| ---- | ------ | ------ |
| 풀이 | $O(N)$ | $O(N)$ |

($N$ = `nums`의 길이)

---

## 3. 코드

### 풀이 [Java][C++][Python]

```java
class Solution {
    public int rob(int[] nums) {
        int n = nums.length;
        int[] dp = new int[1 + n];

        for (int i = 1; i <= n; i++) {
            dp[i] = Math.max(dp[i - 1], dp[Math.max(i - 2, 0)] + nums[i - 1]);
        }

        return dp[n];
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

class Solution {
   public:
    int rob(vector<int>& nums) {
        int n = nums.size();
        vector<int> dp(1 + n);

        for (int i = 1; i <= n; i++) {
            dp[i] = max(dp[i - 1], dp[max(i - 2, 0)] + nums[i - 1]);
        }

        return dp[n];
    }
};
```

```python
class Solution:
    def rob(self, nums: list[int]) -> int:
        n = len(nums)
        dp = [0] * (1 + n)

        for i in range(1, n + 1):
            dp[i] = max(dp[i - 1], dp[i - 2] + nums[i - 1])

        return dp[n]
```

---
