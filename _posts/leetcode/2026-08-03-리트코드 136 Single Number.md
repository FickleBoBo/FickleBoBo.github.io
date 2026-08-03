---
title: "[LeetCode] 136번 - Single Number [Java][C++]"
slug: leetcode-136
date: 2026-08-03
categories: [PS, LeetCode]
tags: [bit manipulation]
toc: true
math: true
---

[문제 링크](https://leetcode.com/problems/single-number/)

---

## 1. 아이디어

같은 수를 두 번 XOR하면 0이 되어 상쇄된다. 배열 전체를 한 번에 XOR로 누적하면 짝을 이룬 값들은 모두 사라지고, 짝이 없는 유일한 값만 남게 된다.

---

## 2. 복잡도

| 시간복잡도 | 공간복잡도 |
| :--------: | :--------: |
|   $O(N)$   |   $O(1)$   |

> $N$ = `nums` 길이

---

## 3. 코드

### 풀이 [Java][C++]

```java
class Solution {
    public int singleNumber(int[] nums) {
        int res = 0;
        for (int x : nums) {
            res ^= x;
        }

        return res;
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

class Solution {
   public:
    int singleNumber(vector<int>& nums) {
        int res = 0;
        for (int x : nums) {
            res ^= x;
        }

        return res;
    }
};
```

---
