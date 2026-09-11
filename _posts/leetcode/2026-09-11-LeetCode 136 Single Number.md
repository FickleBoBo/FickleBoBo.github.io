---
title: "[LeetCode] #136 - Single Number [Java][C++][Python]"
date: 2026-09-11
categories: [PS, LeetCode]
tags: ["bit manipulation"]
slug: leetcode-136
media_subpath: /assets/img/posts/leetcode-136/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/single-number/)
{: .prompt-info }

---

## 1. 아이디어

정수 배열 `nums`에 대해 하나의 원소를 제외한 나머지 원소가 모두 두 번씩 등장할 때, 한 번만 등장한 원소를 구하는 문제다. 비트 XOR 연산을 활용하면 간단하게 해결할 수 있는데 같은 수에 대한 비트 XOR 연산은 0이 된다는 점에서 모든 원소를 전부 비트 XOR 연산을 하면 한 번만 등장했던 원소를 구할 수 있다.

---

## 2. 복잡도

| 접근 | 시간   | 공간   |
| ---- | ------ | ------ |
| 풀이 | $O(N)$ | $O(1)$ |

($N$ = `nums`의 길이)

---

## 3. 코드

### 풀이 [Java][C++][Python]

```java
class Solution {
    public int singleNumber(int[] nums) {
        int ans = 0;
        for (int x : nums) {
            ans ^= x;
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
    int singleNumber(vector<int>& nums) {
        int ans = 0;
        for (int x : nums) {
            ans ^= x;
        }

        return ans;
    }
};
```

```python
class Solution:
    def singleNumber(self, nums: list[int]) -> int:
        ans = 0
        for x in nums:
            ans ^= x

        return ans
```

---
