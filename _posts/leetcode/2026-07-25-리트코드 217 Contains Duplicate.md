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

정수 배열 `nums`에 대해 겹치는 원소가 하나라도 있으면 `true`, 없으면 `false`를 반환하는 문제로 집합을 활용하면 간단하게 해결할 수 있다. `nums`의 각 원소를 집합에 넣을 때 이미 집합에 존재하면 겹치는 원소가 존재하는 것이므로 `true`를 반환하고 한번도 발견한적이 없는 채 종료되면 `false`를 반환해줬다.

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
            if (set.contains(x)) return true;
            set.add(x);
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
        unordered_set<int> st;
        for (int x : nums) {
            if (st.count(x)) return true;
            st.insert(x);
        }

        return false;
    }
};
```

---
