---
title: "[LeetCode] #268 - Missing Number [Java][C++][Python]"
date: 2026-09-13
categories: [PS, LeetCode]
tags: ["bit manipulation", "math", "warm up"]
slug: leetcode-268
media_subpath: /assets/img/posts/leetcode-268/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/missing-number/)
{: .prompt-info }

---

## 1. 아이디어

0부터 $n$까지의 수 중 하나가 빠진 길이 $n$의 배열에서 빠진 수를 찾는 문제다. 수가 서로 다르고 범위 안에서 정확히 하나가 빠져 있으므로 배열에 나온 수를 표시해 두고 표시되지 않은 수를 찾으면 된다.

이렇게 표시해 두는 방법은 $O(n)$의 추가 공간을 쓰는데, 지문의 Follow-up은 선형 시간에 상수 크기의 추가 공간만 쓰라고 요구한다. 빠진 수를 제외한 나머지 수는 배열에 정확히 한 번씩 나오므로 등차수열의 합 공식으로 구한 0부터 $n$까지의 합 $n(n + 1) / 2$에서 배열의 합을 빼면 빠진 수만 남고, $n \le 10^4$이라 합은 $5 \times 10^7$ 정도에 그쳐 32비트 정수에도 들어간다. 합 대신 XOR로도 선형 시간과 상수 공간으로 풀 수 있다. 0부터 $n$까지의 모든 수와 배열의 모든 수를 XOR하면 배열에 있는 수는 두 번씩 나와 $a \oplus a = 0$으로 사라지고 빠진 수만 한 번 나와 남는다.

---

## 2. 코드

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

0은 XOR해도 값이 변하지 않아 반복을 1부터 시작했다.

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
