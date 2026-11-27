---
title: "[LeetCode] #704 - Binary Search [Java][C++][Python]"
date: 2026-09-05
categories: [PS, LeetCode]
tags: ["binary search"]
slug: leetcode-704
media_subpath: /assets/img/posts/leetcode-704/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/binary-search/)
{: .prompt-info }

---

## 1. 아이디어

오름차순으로 정렬된 배열에서 `target`의 인덱스를 찾고 없으면 -1을 반환하는 전형적인 이분 탐색 문제이고, 배열의 길이를 $n$이라 할 때 $O(\log n)$ 시간을 요구하므로 가운데 원소를 `target`과 비교해 후보를 절반씩 버려야 한다. 후보를 양 끝을 포함하는 구간으로 잡으면 비교한 가운데 원소는 이미 확인했으므로 다음 구간은 그 바로 옆부터 시작한다. 원소가 하나만 남은 구간도 확인해야 하므로 구간이 빌 때까지 반복하며, 그동안 찾지 못했다면 -1이다.

---

## 2. 코드

### 풀이 [Java][C++][Python]

```java
class Solution {
    public int search(int[] nums, int target) {
        return binarySearch(nums, target);
    }

    static int binarySearch(int[] arr, int target) {
        int lo = 0, hi = arr.length - 1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
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
    int binarySearch(vector<int>& v, int target) {
        int lo = 0, hi = v.size() - 1;
        while (lo <= hi) {
            int mid = lo + (hi - lo) / 2;
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
        return binarySearch(nums, target);
    }
};
```

```python
class Solution:
    def binary_search(self, nums, target):
        lo, hi = 0, len(nums) - 1
        while lo <= hi:
            mid = lo + (hi - lo) // 2
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
