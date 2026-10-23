---
title: "[LeetCode] #136 - Single Number [Java][C++][Python]"
date: 2026-09-11
categories: [PS, LeetCode]
tags: ["bit manipulation"]
slug: leetcode-136
media_subpath: /assets/img/posts/leetcode-136/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/single-number/)
{: .prompt-info }

---

## 1. 아이디어

배열에서 한 값만 한 번 나오고 나머지는 모두 두 번씩 나올 때, 그 값을 찾는 문제이고 선형 시간, 상수 공간이라는 조건이 붙는다. 배열의 길이를 $n$이라 할 때 해시 집합이나 맵을 쓰면 $O(n)$ 시간에 풀리지만 추가 공간이 필요하고, 정렬하면 추가 공간은 거의 안 쓰지만 선형 시간을 넘는다. 따라서 상수 크기의 값 하나만 들고 훑으면서 두 번 나온 값이 서로 지워지게 만드는 연산이 필요한데 XOR이 그렇다. XOR은 교환·결합법칙이 성립하고 임의의 $a$에 대해 $a \oplus a = 0$, $a \oplus 0 = a$이므로 순서와 상관없이 같은 값끼리 짝지어 지울 수 있고, 전부 XOR하면 두 번씩 나온 값은 0으로 사라지고 한 번 나온 값만 남는다.

---

## 2. 코드

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
