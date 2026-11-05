---
title: "[LeetCode] #53 - Maximum Subarray [Java][C++][Python]"
date: 2026-11-05
categories: [PS, LeetCode]
tags: ["dynamic programming", "greedy", "kadane's algorithm"]
slug: leetcode-53
media_subpath: /assets/img/posts/leetcode-53/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/maximum-subarray/)
{: .prompt-info }

---

## 1. 아이디어

합이 가장 큰 연속 부분 배열의 합을 구하는 문제로, 배열을 앞에서부터 보며 각 원소에서 끝나는 부분 배열의 최대 합을 차례로 구한다. 어떤 원소에서 끝나는 부분 배열은 그 원소 하나만 쓰거나 바로 앞 원소에서 끝나는 부분 배열에 이 원소를 이어 붙인 것이다. 이어 붙인 합은 앞 부분 배열의 합에 이 원소를 더한 값이라 앞 합이 클수록 유리하므로, 앞 원소에서 끝나는 부분 배열 중 합이 가장 큰 것 하나만 보면 된다.

그래서 앞의 최대 합이 음수이면 이어 붙일수록 손해라 새로 시작하고 그렇지 않으면 이어 가며, 이렇게 구한 합들 중 최댓값이 답이다. 이 방법이 카데인 알고리즘이다.

부분 배열은 비어 있을 수 없어서 원소가 모두 음수인 배열에서는 가장 큰 원소 하나가 답이 된다. 그래서 답의 초기값을 0으로 두면 틀리고, 가능한 답보다 작은 값에서 시작해야 한다.

---

## 2. 코드

### 풀이 [Java][C++][Python]

```java
class Solution {
    public int maxSubArray(int[] nums) {
        int cur = 0;
        int ans = Integer.MIN_VALUE;
        for (int x : nums) {
            cur = Math.max(x, cur + x);
            ans = Math.max(ans, cur);
        }

        return ans;
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

class Solution {
   public:
    int maxSubArray(vector<int>& nums) {
        int cur = 0;
        int ans = INT_MIN;
        for (int x : nums) {
            cur = max(x, cur + x);
            ans = max(ans, cur);
        }

        return ans;
    }
};
```

```python
class Solution:
    def maxSubArray(self, nums: list[int]) -> int:
        cur = 0
        ans = -1_000_000_000
        for x in nums:
            cur = max(x, cur + x)
            ans = max(ans, cur)

        return ans
```

원소가 -10,000 이상이라 답도 그 이상이므로, `ans`의 초기값은 충분히 작은 `-1_000_000_000`으로 뒀다.

---
