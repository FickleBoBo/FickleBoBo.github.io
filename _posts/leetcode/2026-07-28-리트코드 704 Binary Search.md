---
title: "[LeetCode] 704번 - Binary Search [Java][C++]"
slug: leetcode-704
date: 2026-07-28
categories: [PS, LeetCode]
tags: [binary search]
toc: true
math: true
---

[문제 링크](https://leetcode.com/problems/binary-search/)

---

## 1. 아이디어

이분 탐색을 직접 구현해보는 문제로 이분 탐색 과정에서 `mid`가 `target`이 되면 해당 인덱스를, 양 끝 포인터가 교차할 때까지 `target`을 찾지 못하면 `-1`을 반환만 해주면 된다. `nums`가 오름차순으로 정렬된채로 주어지기 때문에 바로 이분 탐색을 구현해줬다. 이분 탐색 과정에서 구간이 절반씩 줄어드므로 $O(\log N)$ 의 시간복잡도로 탐색을 할 수 있다.

---

## 2. 복잡도

| 시간복잡도  | 공간복잡도 |
| :---------: | :--------: |
| $O(\log N)$ |   $O(1)$   |

> $N$ = `nums` 길이

---

## 3. 코드

### 풀이 [Java][C++]

```java
class Solution {
    public int search(int[] nums, int target) {
        int left = 0;
        int right = nums.length - 1;

        while (left <= right) {
            int mid = (left + right) / 2;

            if (nums[mid] < target) {
                left = mid + 1;
            } else if (nums[mid] > target) {
                right = mid - 1;
            } else {
                return mid;
            }
        }

        return -1;
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

class Solution {
   public:
    int search(vector<int>& nums, int target) {
        int left = 0;
        int right = nums.size() - 1;

        while (left <= right) {
            int mid = (left + right) / 2;

            if (nums[mid] < target) {
                left = mid + 1;
            } else if (nums[mid] > target) {
                right = mid - 1;
            } else {
                return mid;
            }
        }

        return -1;
    }
};
```

---
