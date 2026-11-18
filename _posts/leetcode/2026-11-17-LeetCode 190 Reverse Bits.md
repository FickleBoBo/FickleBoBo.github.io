---
title: "[LeetCode] #190 - Reverse Bits [Java][C++][Python]"
date: 2026-11-17
categories: [PS, LeetCode]
tags: ["bit manipulation"]
slug: leetcode-190
media_subpath: /assets/img/posts/leetcode-190/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/reverse-bits/)
{: .prompt-info }

---

## 1. 아이디어

32비트 정수의 비트 순서를 뒤집는 문제로, 입력의 가장 낮은 비트부터 하나씩 떼어 결과를 한 칸 왼쪽으로 밀고 그 자리에 붙이면 먼저 뗀 비트가 밀려 올라가 결국 가장 높은 자리에 놓여 순서가 뒤집힌다. 입력이 0이 될 때까지가 아니라 32번을 정확히 돌려야 하는데, 입력의 높은 자리가 `0`이면 일찍 0이 되어 멈추고, 그 `0`들이 있어야 할 결과의 낮은 자리만큼 결과를 더 밀어 올리지 못해 값이 작아지기 때문이다.

---

## 2. 코드

### 풀이 1: 비트 순회 [Java][C++][Python]

```java
class Solution {
    public int reverseBits(int n) {
        int ans = 0;
        for (int i = 0; i < 32; i++) {
            ans = (ans << 1) | (n & 1);
            n >>= 1;
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
    int reverseBits(int n) {
        int ans = 0;
        for (int i = 0; i < 32; i++) {
            ans = (ans << 1) | (n & 1);
            n >>= 1;
        }

        return ans;
    }
};
```

```python
class Solution:
    def reverseBits(self, n: int) -> int:
        ans = 0
        for _ in range(32):
            ans = (ans << 1) | (n & 1)
            n >>= 1

        return ans
```

---

### 풀이 2: 표준 라이브러리 [Java]

```java
class Solution {
    public int reverseBits(int n) {
        return Integer.reverse(n);
    }
}
```

`Integer.reverse`는 인접한 1비트, 2비트, 4비트 묶음을 차례로 맞바꾸고 마지막에 바이트 순서를 뒤집으므로 32번 반복하지 않고 정해진 몇 번의 연산으로 끝난다.

---
