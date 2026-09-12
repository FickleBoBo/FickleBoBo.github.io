---
title: "[LeetCode] #1 - Two Sum [Java][C++][Python]"
date: 2026-09-05
categories: [PS, LeetCode]
tags: ["brute force", "data structure", "hash table"]
slug: leetcode-1
media_subpath: /assets/img/posts/leetcode-1/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/two-sum/)
{: .prompt-info }

---

## 1. 아이디어

정수 배열 `nums`와 정수 `target`이 주어질 때, `nums`에서 두 수의 합이 `target`이 될 경우 두 수의 인덱스를 반환하는 문제다. `nums`의 크기가 최대 $10^4$이어서 2중 반복문을 통한 브루트 포스로 $O(N^2)$의 시간복잡도로 해결할 수 있다.

Follow-up은 $O(N^2)$의 시간복잡도보다 빠른 알고리즘을 요구한다. 해시맵을 활용하면 $O(N)$의 공간을 사용하는 대신 $O(N)$의 시간복잡도로 해결할 수 있는데, $a + b = \text{target}$일 때 $\text{target} - a = b$임을 이용하는 것이다. key에 원소를 value에 인덱스를 저장할 해시맵을 선언한 후, `nums`를 순회하며 `target - nums[i]`가 해시맵에 있는지 조회해서 해시맵에 존재하면 해당 값의 인덱스와 현재 인덱스를 같이 반환하면 되고, 해시맵에 존재하지 않으면 `nums[i]`를 key로 인덱스를 value로 삽입하는 과정을 반복하면 된다.

---

## 2. 복잡도

| 접근      | 시간     | 공간   |
| --------- | -------- | ------ |
| 완전 탐색 | $O(N^2)$ | $O(1)$ |
| 해시맵    | $O(N)$   | $O(N)$ |

($N$ = `nums`의 길이)

---

## 3. 코드

### 풀이 1: 완전 탐색 [Java][C++][Python]

```java
class Solution {
    public int[] twoSum(int[] nums, int target) {
        for (int i = 0; i < nums.length - 1; i++) {
            for (int j = i + 1; j < nums.length; j++) {
                if (nums[i] + nums[j] == target) return new int[]{i, j};
            }
        }

        return null;
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

class Solution {
   public:
    vector<int> twoSum(vector<int>& nums, int target) {
        for (int i = 0; i < nums.size() - 1; i++) {
            for (int j = i + 1; j < nums.size(); j++) {
                if (nums[i] + nums[j] == target) return {i, j};
            }
        }

        return {};
    }
};
```

```python
class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        for i in range(len(nums) - 1):
            for j in range(i + 1, len(nums)):
                if nums[i] + nums[j] == target:
                    return [i, j]
```

---

### 풀이 2: 해시맵 [Java][C++][Python]

```java
import java.util.*;

class Solution {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> seen = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            if (seen.containsKey(target - nums[i])) {
                return new int[]{seen.get(target - nums[i]), i};
            }
            seen.put(nums[i], i);
        }

        return null;
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

class Solution {
   public:
    vector<int> twoSum(vector<int>& nums, int target) {
        unordered_map<int, int> seen;
        for (int i = 0; i < nums.size(); i++) {
            if (seen.contains(target - nums[i])) {
                return {seen[target - nums[i]], i};
            }
            seen[nums[i]] = i;
        }

        return {};
    }
};
```

```python
class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        seen = {}
        for i, x in enumerate(nums):
            if target - x in seen:
                return [seen[target - x], i]
            seen[x] = i
```

---
