---
title: "[LeetCode] #268 - Missing Number [Java][C++][Python]"
date: 2026-09-13
categories: [PS, LeetCode]
tags: ["bit manipulation", "math", "warm up"]
slug: leetcode-268
media_subpath: /assets/img/posts/leetcode-268/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/missing-number/)
{: .prompt-info }

---

## 1. 아이디어

`0`부터 `n` 사이에서 빠진 숫자 하나를 찾는 문제로 방문 체크를 활용하면 된다. `nums`의 각 원소에 대한 방문 체크 후 방문하지 않은 원소를 발견하면 된다.

Follow up은 $O(1)$의 공간복잡도와 $O(N)$의 시간복잡도로 해결해야 한다. 간단하게는 등차수열의 합 공식인 `1`부터 `n`까지의 합이 $\dfrac{n \times (n + 1)}{2}$인 점을 활용해 해당 합에서 `nums`의 합을 빼면 된다. 다른 방법으로는 비트 XOR의 성질을 활용하는 것으로 `1`부터 `n`까지의 비트 XOR과 `nums`의 모든 원소의 비트 XOR을 비트 XOR하면 한 번만 등장한 해당 수를 제외한 나머지는 전부 2번 등장해서 상쇄되므로 해당 수를 바로 구할 수 있다.

---

## 2. 복잡도

| 접근             | 시간   | 공간   |
| ---------------- | ------ | ------ |
| 방문 체크        | $O(N)$ | $O(N)$ |
| 등차수열 합 공식 | $O(N)$ | $O(1)$ |
| XOR 상쇄         | $O(N)$ | $O(1)$ |

($N$ = `nums`의 길이)

---

## 3. 코드

### 풀이 1: 방문 체크 [Java][C++][Python]

```java
class Solution {
    public int missingNumber(int[] nums) {
        int n = nums.length;
        boolean[] seen = new boolean[1 + n];
        for (int x : nums) {
            seen[x] = true;
        }

        for (int i = 0; i <= n; i++) {
            if (!seen[i]) return i;
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
    int missingNumber(vector<int>& nums) {
        int n = nums.size();
        vector<bool> seen(1 + n);
        for (int x : nums) seen[x] = true;

        for (int i = 0; i <= n; i++) {
            if (!seen[i]) return i;
        }

        return -1;
    }
};
```

```python
class Solution:
    def missingNumber(self, nums: list[int]) -> int:
        seen = set(nums)
        for i in range(len(nums) + 1):
            if i not in seen:
                return i
```

---

### 풀이 2: 등차수열 합 공식 [Java][C++][Python]

```java
class Solution {
    public int missingNumber(int[] nums) {
        int n = nums.length;
        int sum = 0;
        for (int x : nums) {
            sum += x;
        }

        return n * (n + 1) / 2 - sum;
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

class Solution {
   public:
    int missingNumber(vector<int>& nums) {
        int n = nums.size();
        int sum = 0;
        for (int x : nums) sum += x;

        return n * (n + 1) / 2 - sum;
    }
};
```

```python
class Solution:
    def missingNumber(self, nums: list[int]) -> int:
        n = len(nums)
        return n * (n + 1) // 2 - sum(nums)
```

---

### 풀이 3: XOR 상쇄 [Java][C++][Python]

```java
class Solution {
    public int missingNumber(int[] nums) {
        int ans = 0;
        for (int i = 1; i <= nums.length; i++) {
            ans ^= i;
        }
        for (int x : nums) {
            ans ^= x;
        }

        return ans;
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

class Solution {
   public:
    int missingNumber(vector<int>& nums) {
        int ans = 0;
        for (int i = 1; i <= nums.size(); i++) ans ^= i;
        for (int x : nums) ans ^= x;

        return ans;
    }
};
```

```python
class Solution:
    def missingNumber(self, nums: list[int]) -> int:
        ans = 0
        for i in range(1, len(nums) + 1):
            ans ^= i
        for x in nums:
            ans ^= x

        return ans
```

---
