---
title: "[LeetCode] #338 - Counting Bits [Java][C++][Python]"
date: 2026-09-13
categories: [PS, LeetCode]
tags: ["bit manipulation", "dynamic programming"]
slug: leetcode-338
media_subpath: /assets/img/posts/leetcode-338/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/counting-bits/)
{: .prompt-info }

---

## 1. 아이디어

0부터 $n$까지 각 수를 이진수로 썼을 때 1의 개수를 배열로 구하는 문제다. 수마다 비트를 하나씩 세면 수 하나에 그 비트 수만큼 걸려 전체가 $O(n \log n)$이다.

지문의 Follow-up은 이를 선형 시간으로 줄일 수 있는지 묻는다. `i & (i - 1)`은 $i$에서 가장 낮은 `1`만 지운 수다. `i - 1`은 가장 낮은 `1`과 그 아래 비트만 뒤집으므로 AND하면 그 부분이 모두 `0`이 되고 위쪽은 그대로이기 때문이며, 이 연산이 브라이언 커니핸 알고리즘의 핵심이다. 그 수는 $i$보다 작아 `ans`에 이미 채워져 있고 1의 개수가 정확히 하나 적으므로, `ans[i] = ans[i & (i - 1)] + 1`이라는 점화식으로 작은 수부터 채우는 DP가 된다. $i$가 1 이상이면 가장 낮은 `1`이 항상 있어 이 관계가 모든 $i$에서 성립하고, `1`이 없는 0은 `ans[0] = 0`이 출발점이 된다.

---

## 2. 코드

### 풀이 1: 비트 순회 [Java][C++][Python]

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
