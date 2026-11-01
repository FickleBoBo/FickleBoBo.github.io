---
title: "[LeetCode] #198 - House Robber [Java][C++][Python]"
date: 2026-09-04
categories: [PS, LeetCode]
tags: ["dynamic programming"]
slug: leetcode-198
media_subpath: /assets/img/posts/leetcode-198/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/house-robber/)
{: .prompt-info }

---

## 1. 아이디어

길을 따라 늘어선 집에서 이웃한 두 집은 함께 털 수 없을 때 털 수 있는 돈의 최댓값을 구하는 문제다. 앞에서부터 $i$채의 집만 놓고 얻을 수 있는 최댓값을 `dp[i]`라 하면, $i$번째 집에 대한 선택은 털지 않거나 털거나 둘뿐이다. 털지 않으면 앞의 $i - 1$채에서 얻은 최댓값 그대로이고, 털면 바로 앞집을 털 수 없으므로 앞의 $i - 2$채에서 얻은 최댓값에 이 집의 돈을 더한 값이다. 두 번째 경우에 앞의 $i - 2$채를 어떻게 털었든 $i$번째 집과는 이웃하지 않아 서로 영향이 없으므로 `dp[i - 2]`의 최적 선택을 그대로 쓸 수 있다. 따라서 `dp[i]`는 `dp[i - 1]`과 `dp[i - 2] + nums[i - 1]` 중 큰 값이고(`nums`는 0부터 세므로 $i$번째 집의 돈이 `nums[i - 1]`이다), $i = 1$일 때는 $i - 2$가 음수가 되지만 이 경우는 앞에 집이 없는 것과 같으므로 `dp[i - 2]`를 0으로 본다.

---

## 2. 코드

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

`i`가 1일 때의 `dp[i - 2]`는 `dp[-1]`, 곧 마지막 칸을 읽는데, 이 칸은 아직 채워지지 않은 0이라 `dp[0]`을 읽는 것과 같으므로 그대로 두었다.

---
