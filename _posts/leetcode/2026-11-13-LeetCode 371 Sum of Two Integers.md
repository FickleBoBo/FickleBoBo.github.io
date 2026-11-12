---
title: "[LeetCode] #371 - Sum of Two Integers [Java][C++]"
date: 2026-11-13
categories: [PS, LeetCode]
tags: ["bit manipulation"]
slug: leetcode-371
media_subpath: /assets/img/posts/leetcode-371/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/sum-of-two-integers/)
{: .prompt-info }

---

## 1. 아이디어

`+`와 `-` 없이 두 정수 $a$, $b$의 합을 구하는 문제로, 두 수를 이진수로 보고 자리마다 더하면 올림을 뺀 합은 두 비트가 다른 자리만 켜진 $a \oplus b$이다. 올림은 두 비트가 모두 켜진 자리에서 생겨 바로 위 자리로 올라가므로 $a \land b$를 한 칸 왼쪽으로 민 값이다. 합은 이 둘을 다시 더한 값과 같으므로, 올림이 0이 될 때까지 같은 분해를 되풀이하면 덧셈 연산자 없이 합이 나온다.

되풀이할 때마다 새 올림은 이전 올림과 올림을 뺀 합이 모두 켜진 자리를 한 칸 위로 민 값이다. 그래서 올림의 가장 낮은 켜진 비트가 적어도 한 자리씩 올라가고 32비트를 넘어가면 사라지므로, 많아야 32번이면 올림이 0이 된다. 2의 보수에서는 음수의 덧셈도 부호 없이 비트별로 올림하는 덧셈과 같으므로 부호를 따로 나눌 필요가 없다.

---

## 2. 코드

### 풀이 [Java][C++]

```java
class Solution {
    public int getSum(int a, int b) {
        while (b != 0) {
            int carry = (a & b) << 1;
            a ^= b;
            b = carry;
        }

        return a;
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

class Solution {
   public:
    int getSum(int a, int b) {
        while (b != 0) {
            int carry = (a & b) << 1;
            a ^= b;
            b = carry;
        }

        return a;
    }
};
```

음수 값에 `<<`를 쓰는 것은 C++20부터 정의된 동작이다.

---
