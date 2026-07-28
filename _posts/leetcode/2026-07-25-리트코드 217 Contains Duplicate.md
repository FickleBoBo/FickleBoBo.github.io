---
title: "[LeetCode] 217번 - Contains Duplicate [Java][C++]"
slug: leetcode-217
date: 2026-07-25
categories: [PS, LeetCode]
tags: [data structure, hash set／hash map]
toc: true
math: true
---

[문제 링크](https://leetcode.com/problems/contains-duplicate/)

---

## 1. 아이디어

정수 배열 `nums`에 대해 겹치는 원소가 하나라도 있으면 `true`, 없으면 `false`를 반환하는 문제로 집합을 활용하면 간단하게 해결할 수 있다. `nums`의 모든 원소를 담은 집합의 크기가 `nums`의 크기와 같으면 겹치는 원소가 없는 것이고 작다면 겹치는 원소가 하나라도 존재하는 것이다.

---

## 2. 복잡도

| 시간복잡도 | 공간복잡도 |
| :--------: | :--------: |
|   $O(N)$   |   $O(N)$   |

> $N$ = `nums` 길이

---

## 3. 코드

### 풀이 [Java][C++]

```java
import java.util.*;

class Solution {
    public boolean containsDuplicate(int[] nums) {
        Set<Integer> set = new HashSet<>();
        for (int x : nums) {
            set.add(x);
        }

        return set.size() != nums.length;
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

class Solution {
   public:
    bool containsDuplicate(vector<int>& nums) {
        unordered_set<int> st(nums.begin(), nums.end());
        return st.size() != nums.size();
    }
};
```

---
