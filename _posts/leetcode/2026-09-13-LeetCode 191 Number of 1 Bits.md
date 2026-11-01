---
title: "[LeetCode] #191 - Number of 1 Bits [Java][C++][Python]"
date: 2026-09-13
categories: [PS, LeetCode]
tags: ["bit manipulation"]
slug: leetcode-191
media_subpath: /assets/img/posts/leetcode-191/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/number-of-1-bits/)
{: .prompt-info }

---

## 1. 아이디어

양의 정수 $n$을 이진수로 썼을 때 `1`인 비트가 몇 개인지 세는 문제다. 1의 개수는 각 자리가 `1`인지를 따로 보고 더한 것과 같으므로, 가장 낮은 자리가 `1`인지 확인하고 오른쪽으로 한 칸 밀어 다음 자리를 가장 낮은 자리로 가져오는 일을 $n$이 0이 될 때까지 되풀이하면 모든 자리를 한 번씩 보게 된다. 표준 라이브러리의 비트 개수 함수를 쓰면 이 과정이 한 줄로 끝난다.

지문의 Follow-up은 이렇게 세는 함수를 여러 번 호출할 때의 최적화를 묻는데, 호출 한 번의 비용부터 보면 비트를 밀어 가며 보는 방법은 `1`이 몇 개든 가장 높은 `1`의 자리까지 매번 돌아야 한다. 반면 `n & (n - 1)`은 $n$의 가장 낮은 `1`을 정확히 하나 지운다. `n - 1`은 가장 낮은 `1`을 `0`으로 바꾸고 그 아래의 `0`들을 모두 `1`로 바꾸되 위쪽 비트는 건드리지 않으므로, $n$과 AND하면 가장 낮은 `1`과 그 아래는 모두 `0`이 되고 위쪽은 그대로 남는다. 따라서 이 연산으로 $n$이 0이 될 때까지 걸리는 횟수가 곧 1의 개수이고, 반복이 가장 높은 `1`의 자리 수가 아니라 1의 개수만큼으로 줄어든다. 이 방법을 브라이언 커니핸 알고리즘이라 한다.

---

## 2. 코드

### 풀이 1: 비트 순회 [Java][C++][Python]

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

`std::popcount`는 부호 없는 정수만 받아서 `n`을 `(unsigned)`로 바꿔 넘겼다.

```python
class Solution:
    def hammingWeight(self, n: int) -> int:
        return n.bit_count()
```

`bit_count` 메서드(Python 3.10에서 추가)로 바로 구했다.

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
