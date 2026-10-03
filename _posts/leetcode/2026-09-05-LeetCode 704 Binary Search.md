---
title: "[LeetCode] #704 - Binary Search [Java][C++][Python]"
date: 2026-09-05
categories: [PS, LeetCode]
tags: ["binary search"]
slug: leetcode-704
media_subpath: /assets/img/posts/leetcode-704/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/binary-search/)
{: .prompt-info }

---

## 1. 아이디어

오름차순으로 정렬된 정수 배열 `nums`에 대해 `target`의 인덱스를 반환하는 문제로 제목 그대로 이분 탐색을 구현해서 해결하면 된다. `nums`가 오름차순으로 정렬되어 있고, 모든 원소가 유니크하므로 이분 탐색으로 발견시 인덱스를 반환하고 발견하지 못하면 -1을 반환했다.

---

## 2. 복잡도

| 접근 | 시간        | 공간   |
| ---- | ----------- | ------ |
| 풀이 | $O(\log N)$ | $O(1)$ |

($N$ = `nums`의 길이)

---

## 3. 코드

### 풀이 [Java][C++][Python]

```java
class Solution {
    public int search(int[] nums, int target) {
        return binarySearch(nums, target);
    }

    static int binarySearch(int[] arr, int target) {
        int lo = 0, hi = arr.length - 1;

        while (lo <= hi) {
            int mid = (lo + hi) / 2;

            if (arr[mid] < target) {
                lo = mid + 1;
            } else if (arr[mid] > target) {
                hi = mid - 1;
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
    int bin_search(vector<int>& v, int target) {
        int lo = 0, hi = v.size() - 1;

        while (lo <= hi) {
            int mid = (lo + hi) / 2;

            if (v[mid] < target) {
                lo = mid + 1;
            } else if (v[mid] > target) {
                hi = mid - 1;
            } else {
                return mid;
            }
        }

        return -1;
    }

    int search(vector<int>& nums, int target) {
        return bin_search(nums, target);
    }
};
```

```python
class Solution:
    def binary_search(self, nums, target):
        lo, hi = 0, len(nums) - 1

        while lo <= hi:
            mid = (lo + hi) // 2

            if nums[mid] < target:
                lo = mid + 1
            elif nums[mid] > target:
                hi = mid - 1
            else:
                return mid

        return -1

    def search(self, nums: list[int], target: int) -> int:
        return self.binary_search(nums, target)
```

---
