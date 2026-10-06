---
title: "[LeetCode] #191 - Number of 1 Bits [Java][C++][Python]"
date: 2026-09-13
categories: [PS, LeetCode]
tags: ["bit manipulation"]
slug: leetcode-191
media_subpath: /assets/img/posts/leetcode-191/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/number-of-1-bits/)
{: .prompt-info }

---

## 1. 아이디어

양의 정수 `n`에 대해 2진수로 표현했을 때, `1`인 비트의 수를 세는 문제다. `1`인 비트의 수는 2진수로 표현했을 때 끝자리 비트가 `1`이면 세고 비트 시프트로 오른쪽으로 한 칸 미는 과정을 반복하면 간단하게 셀 수 있다. 또는 내장 함수를 활용해도 된다.

Follow up은 최적화를 언급하고 있는데 기본적인 방식들도 이미 매우 빨라서 큰 의미는 없다. 1바이트의 숫자에 대한 모든 1의 개수를 구한 룩업 테이블을 만든 후 `n`의 각 바이트별로 세는 방식을 활용할 수도 있고, Brian Kernighan's Algorithm을 활용하면 효율적으로 `1`인 비트만 셀 수 있다.

---

## 2. 복잡도

| 접근                     | 시간        | 공간   |
| ------------------------ | ----------- | ------ |
| 비트 시프트              | $O(\log N)$ | $O(1)$ |
| 표준 라이브러리          | $O(1)$      | $O(1)$ |
| 브라이언 커니핸 알고리즘 | $O(\log N)$ | $O(1)$ |

($N$ = 입력값 `n`. Python은 `bit_count()`가 임의 정밀도 정수의 자릿수만큼 세어 표준 라이브러리 시간 $O(\log N)$)

---

## 3. 코드

### 풀이 1: 비트 시프트 [Java][C++][Python]

```java
class Solution {
    public int hammingWeight(int n) {
        int cnt = 0;
        while (n > 0) {
            if ((n & 1) == 1) cnt++;
            n >>= 1;
        }

        return cnt;
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

class Solution {
   public:
    int hammingWeight(int n) {
        int cnt = 0;
        while (n) {
            if (n & 1) cnt++;
            n >>= 1;
        }

        return cnt;
    }
};
```

```python
class Solution:
    def hammingWeight(self, n: int) -> int:
        cnt = 0
        while n:
            if n & 1:
                cnt += 1
            n >>= 1

        return cnt
```

---

### 풀이 2: 표준 라이브러리 [Java][C++][Python]

```java
class Solution {
    public int hammingWeight(int n) {
        return Integer.bitCount(n);
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

class Solution {
   public:
    int hammingWeight(int n) {
        return popcount((unsigned)n);
    }
};
```

```python
class Solution:
    def hammingWeight(self, n: int) -> int:
        return n.bit_count()
```

---

### 풀이 3: 브라이언 커니핸 알고리즘 [Java][C++][Python]

```java
class Solution {
    public int hammingWeight(int n) {
        int cnt = 0;
        while (n > 0) {
            n &= (n - 1);
            cnt++;
        }

        return cnt;
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

class Solution {
   public:
    int hammingWeight(int n) {
        int cnt = 0;
        while (n) {
            n &= (n - 1);
            cnt++;
        }

        return cnt;
    }
};
```

```python
class Solution:
    def hammingWeight(self, n: int) -> int:
        cnt = 0
        while n:
            n &= n - 1
            cnt += 1

        return cnt
```

---
