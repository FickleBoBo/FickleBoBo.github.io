---
title: "[LeetCode] #338 - Counting Bits [Java][C++][Python]"
date: 2026-09-13
categories: [PS, LeetCode]
tags: ["bit manipulation", "dynamic programming"]
slug: leetcode-338
media_subpath: /assets/img/posts/leetcode-338/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/counting-bits/)
{: .prompt-info }

---

## 1. 아이디어

`0`부터 `n`까지 각 수를 2진수로 표현했을 때, 1인 비트의 수를 구하는 문제로 built-in function을 사용하지 못하므로 직접 반복문으로 1의 자리 비트를 세고 시프트하는 과정을 반복하면 된다.

Follow up은 선형 시간으로 이 문제를 해결하는 것으로 다이나믹 프로그래밍과 Brian Kernighan's Algorithm을 활용하면 해결할 수 있는데, 임의의 자연수 `x`에 대해 `x`의 1인 비트의 수는 `x & (x - 1)`보다 하나 많은 점을 dp 테이블로 연산하는 방법이다. `x & (x - 1)`이 `x`보다 작아서 이미 dp 테이블에 계산되어 있으므로 이를 활용해 선형 시간에 계산할 수 있다.

---

## 2. 복잡도

| 접근               | 시간          | 공간   |
| ------------------ | ------------- | ------ |
| 비트 시프트        | $O(N \log N)$ | $O(N)$ |
| 브라이언 커니핸 DP | $O(N)$        | $O(N)$ |

($N$ = 입력값 `n`)

---

## 3. 코드

### 풀이 1: 비트 시프트 [Java][C++][Python]

```java
class Solution {
    public int[] countBits(int n) {
        int[] ans = new int[1 + n];
        for (int i = 1; i <= n; i++) {
            int x = i;
            int cnt = 0;
            while (x > 0) {
                if ((x & 1) == 1) cnt++;
                x >>= 1;
            }
            ans[i] = cnt;
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
    vector<int> countBits(int n) {
        vector<int> ans(1 + n);
        for (int i = 1; i <= n; i++) {
            int x = i;
            int cnt = 0;
            while (x) {
                if (x & 1) cnt++;
                x >>= 1;
            }
            ans[i] = cnt;
        }

        return ans;
    }
};
```

```python
class Solution:
    def countBits(self, n: int) -> list[int]:
        ans = [0] * (1 + n)
        for i in range(1, n + 1):
            x = i
            cnt = 0
            while x:
                if x & 1:
                    cnt += 1
                x >>= 1
            ans[i] = cnt

        return ans
```

---

### 풀이 2: 브라이언 커니핸 DP [Java][C++][Python]

```java
class Solution {
    public int[] countBits(int n) {
        int[] ans = new int[1 + n];
        for (int i = 1; i <= n; i++) {
            ans[i] = ans[i & (i - 1)] + 1;
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
    vector<int> countBits(int n) {
        vector<int> ans(1 + n);
        for (int i = 1; i <= n; i++) {
            ans[i] = ans[i & (i - 1)] + 1;
        }

        return ans;
    }
};
```

```python
class Solution:
    def countBits(self, n: int) -> list[int]:
        ans = [0] * (1 + n)
        for i in range(1, n + 1):
            ans[i] = ans[i & (i - 1)] + 1

        return ans
```

---
