---
title: "[LeetCode] #217 - Contains Duplicate [Java][C++][Python]"
date: 2026-09-01
categories: [PS, LeetCode]
tags: ["hash table", "data structure"]
slug: leetcode-217
media_subpath: /assets/img/posts/leetcode-217/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/contains-duplicate/)
{: .prompt-info }

---

## 1. 아이디어

정수 배열 `nums`에 대해 두 번 이상 등장한 원소가 있으면 `true`를 아니면 `false`를 반환하는 문제다. 각 정수의 중복 여부를 판단한다는 점에서 해시 집합을 활용하면 간단하게 해결할 수 있다.

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
