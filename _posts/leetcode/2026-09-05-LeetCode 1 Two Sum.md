---
title: "[LeetCode] #1 - Two Sum [Java][C++][Python]"
date: 2026-09-05
categories: [PS, LeetCode]
tags: ["brute force", "data structure", "hash set/map"]
slug: leetcode-1
media_subpath: /assets/img/posts/leetcode-1/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/two-sum/)
{: .prompt-info }

---

## 1. 아이디어

정수 배열에서 합이 `target`이 되는 두 원소의 인덱스를 구하는 문제이고, 같은 원소를 두 번 쓸 수는 없다. 모든 쌍의 합을 확인하면 되는데, 배열의 길이를 $n$이라 하면 $O(n^2)$이라도 $n \le 10^4$이어서 통과한다.

지문의 Follow-up은 $O(n^2)$보다 빠른 방법을 묻는다. 원소의 값 하나를 $x$라 하면 그 원소와 짝이 될 수 있는 값은 `target`에서 $x$를 뺀 값 하나뿐이므로, 모든 쌍을 보는 대신 그 값이 있는지만 확인하면 된다. 앞에서부터 훑으며 지나온 값과 인덱스를 해시맵에 담아 두면 이 확인이 평균 상수 시간에 끝나고, 각 원소에서 짝이 될 값이 이미 해시맵에 있으면 그 인덱스와 현재 인덱스가 답이다. 짝이 해시맵에 있는지 먼저 확인한 뒤에 현재 원소를 담으므로 같은 원소를 두 번 쓰는 일이 없고, 짝이 되는 두 원소 중 나중 것을 만난 시점에는 먼저 것이 반드시 해시맵에 들어 있으므로 답이 되는 쌍을 놓치지 않는다.

---

## 2. 코드

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
            if (seen.containsKey(target - nums[i])) return new int[]{seen.get(target - nums[i]), i};
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
            if (seen.contains(target - nums[i])) return {seen[target - nums[i]], i};
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
