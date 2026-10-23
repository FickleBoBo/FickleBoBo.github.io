---
title: "[LeetCode] #217 - Contains Duplicate [Java][C++][Python]"
date: 2026-09-01
categories: [PS, LeetCode]
tags: ["data structure", "hash table"]
slug: leetcode-217
media_subpath: /assets/img/posts/leetcode-217/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/contains-duplicate/)
{: .prompt-info }

---

## 1. 아이디어

배열에 같은 값이 두 번 이상 나오는지 판별하는 문제다. 배열의 길이를 $n$이라 하면 모든 쌍을 비교하는 방법은 $O(n^2)$이라 $n \le 10^5$에서 시간 초과이므로, 이미 나온 값을 모아 두고 새 원소가 그중에 있는지만 확인하면 된다. 값의 범위가 $-10^9$ 이상 $10^9$ 이하로 넓어 카운팅 배열은 쓸 수 없으니 해시 집합을 쓴다. 집합에는 같은 값이 한 번만 들어가므로 원소를 모두 넣었을 때 집합의 크기가 $n$보다 작으면 중복이 있다는 뜻이고, 넣는 도중 이미 들어 있는 값을 만나면 그 자리에서 중복을 발견할 수도 있다.

---

## 2. 코드

### 풀이 [Java][C++][Python]

```java
import java.util.*;

class Solution {
    public boolean containsDuplicate(int[] nums) {
        Set<Integer> seen = new HashSet<>();
        for (int x : nums) {
            if (!seen.add(x)) return true;
        }

        return false;
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

class Solution {
   public:
    bool containsDuplicate(vector<int>& nums) {
        return unordered_set(nums.begin(), nums.end()).size() < nums.size();
    }
};
```

```python
class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        return len(set(nums)) < len(nums)
```

---
