---
title: "[LeetCode] #213 - House Robber II [Java][C++][Python]"
date: 2026-09-04
categories: [PS, LeetCode]
tags: ["dynamic programming"]
slug: leetcode-213
media_subpath: /assets/img/posts/leetcode-213/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/house-robber-ii/)
{: .prompt-info }

---

## 1. 아이디어

원형으로 배치된 집들이 주어지고 도둑이 연결된 두 집을 동시에 털 수 없을 때 얻을 수 있는 최대 금액을 구하는 문제로 다이나믹 프로그래밍을 활용하면 해결할 수 있다.

`dp[i]`를 첫 번째 집부터 `i`번째 집까지를 고려했을 때, 얻을 수 있는 최대 금액으로 정의하면 `i`번째 집을 안 터는 경우는 `i - 1`번째 집을 털 수도 있으므로 `dp[i - 1]`이 최대 금액이 되고, `i`번째 집을 털 경우는 `i - 1`번째 집은 털 수 없으므로 `i - 2`번째 집을 터는 경우까지 고려한 `dp[i - 2]`에 `nums[i - 1]`을 더한 값 중 최댓값이 `dp[i]`가 된다.

다만 해당 문제는 마지막 집과 첫 번째 집이 연결되어 있어 이러면 첫 번째 집과 마지막 집을 모두 턴 경우를 거를 수 없는데 두 집이 연결되어 있으므로 최댓값은 마지막 집을 안 턴 경우와 첫 번째 집을 안 턴 경우 중 하나에 존재한다. 이를 위해 `dp` 구간을 나눠 마지막 집을 제외한 구간에서 최댓값을 한 번 구하고, 첫 번째 집을 제외한 구간에서 최댓값을 한 번 구해서 둘 중 최댓값을 반환하는 방식으로 해결했다. 두 집 모두 안 턴 경우도 이 둘 중 하나에 포함되기에 모든 경우를 탐색할 수 있다.

---

## 2. 복잡도

| 접근 | 시간   | 공간   |
| ---- | ------ | ------ |
| 풀이 | $O(N)$ | $O(N)$ |

($N$ = `nums`의 길이)

---

## 3. 코드

### 풀이 [Java][C++][Python]

집이 1개 이상의 자연수로 주어져 있어서 집이 1개인 경우는 첫 번째 집과 마지막 집이 일치하게 되어 `dp`식이 성립하지 않는다. 따라서 이 경우만 별도로 예외 처리를 했다.

```java
class Solution {
    public int rob(int[] nums) {
        int n = nums.length;
        if (n == 1) return nums[0];

        int case1 = solve(nums, 1, n - 1);
        int case2 = solve(nums, 2, n);
        return Math.max(case1, case2);
    }

    static int solve(int[] nums, int l, int r) {
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
    int solve(vector<int>& nums, int l, int r) {
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

        int case1 = solve(nums, 1, n - 1);
        int case2 = solve(nums, 2, n);
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

        def solve(l, r):
            dp = [0] * (1 + n)
            for i in range(l, r + 1):
                dp[i] = max(dp[i - 1], dp[i - 2] + nums[i - 1])

            return dp[r]

        case1 = solve(1, n - 1)
        case2 = solve(2, n)
        return max(case1, case2)
```

---
