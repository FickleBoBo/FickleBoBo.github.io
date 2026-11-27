---
title: "[LeetCode] #213 - House Robber II [Java][C++][Python]"
date: 2026-09-04
categories: [PS, LeetCode]
tags: ["dynamic programming"]
slug: leetcode-213
media_subpath: /assets/img/posts/leetcode-213/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/house-robber-ii/)
{: .prompt-info }

---

## 1. 아이디어

원형으로 늘어선 집에서 이웃한 두 집은 함께 털 수 없을 때 털 수 있는 돈의 최댓값을 구하는 문제로, 일렬로 놓인 [[LeetCode] #198 - House Robber](/posts/leetcode-198/)에서 첫 집과 마지막 집도 이웃이라는 조건이 더해졌다. 첫 집과 마지막 집은 함께 털 수 없으므로 어떤 선택에서도 둘 중 적어도 하나는 털지 않는다. 첫 집을 털지 않았다면 남는 집은 첫 집을 뺀 일렬이고, 마지막 집을 털지 않았다면 마지막 집을 뺀 일렬이므로, 이 두 구간 각각에서 일렬일 때의 최댓값을 구해 큰 쪽을 고르면 된다.

두 구간 안에는 첫 집과 마지막 집이 함께 들어 있지 않아 구간 안에서 유효한 선택은 원형에서도 유효하고, 원형의 유효한 선택은 모두 두 구간 중 하나에 들어가므로 빠지는 경우도 없다.

일렬의 최댓값은 앞에서부터 $i$채에서 얻는 최댓값 `dp[i]`를 차례로 구해 얻는다. `dp[i]`는 $i$번째 집을 털지 않으면 `dp[i - 1]`이고 털면 바로 앞집을 털 수 없어 `dp[i - 2]`에 이 집의 돈을 더한 값이므로 둘 중 큰 쪽이다. 집이 하나뿐이면 두 구간이 모두 비어 0이 되지만 그 집은 털 수 있으므로 이때만 그 집의 돈이 답이다.

---

## 2. 코드

### 풀이 [Java][C++][Python]

구간 앞쪽의 칸은 채우지 않고 0으로 남겨 구간 밖의 집은 털지 않은 것으로 취급했다.

```java
class Solution {
    public int rob(int[] nums) {
        int n = nums.length;
        if (n == 1) return nums[0];

        int case1 = robRange(nums, 1, n - 1);
        int case2 = robRange(nums, 2, n);
        return Math.max(case1, case2);
    }

    static int robRange(int[] nums, int l, int r) {
        int n = nums.length;
        int[] dp = new int[1 + n];

        for (int i = l; i <= r; i++) {
            dp[i] = Math.max(dp[i - 1], dp[Math.max(i - 2, 0)] + nums[i - 1]);
        }
        return dp[r];
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

class Solution {
   public:
    int robRange(vector<int>& nums, int l, int r) {
        int n = nums.size();
        vector<int> dp(1 + n);

        for (int i = l; i <= r; i++) {
            dp[i] = max(dp[i - 1], dp[max(i - 2, 0)] + nums[i - 1]);
        }
        return dp[r];
    }

    int rob(vector<int>& nums) {
        int n = nums.size();
        if (n == 1) return nums[0];

        int case1 = robRange(nums, 1, n - 1);
        int case2 = robRange(nums, 2, n);
        return max(case1, case2);
    }
};
```

```python
class Solution:
    def rob(self, nums: list[int]) -> int:
        n = len(nums)
        if n == 1:
            return nums[0]

        def rob_range(l, r):
            dp = [0] * (1 + n)
            for i in range(l, r + 1):
                dp[i] = max(dp[i - 1], dp[i - 2] + nums[i - 1])
            return dp[r]

        case1 = rob_range(1, n - 1)
        case2 = rob_range(2, n)
        return max(case1, case2)
```

`rob_range(1, n - 1)`에서 `i`가 1일 때의 `dp[i - 2]`는 마지막 칸 `dp[-1]`을 읽지만, 이 호출은 그 칸을 채우지 않아 0이라 앞에 집이 없는 경우와 같으므로 그대로 두었다.

---
