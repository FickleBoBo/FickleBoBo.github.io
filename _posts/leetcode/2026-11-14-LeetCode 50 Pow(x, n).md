---
title: "[LeetCode] #50 - Pow(x, n) [Java][C++][Python]"
date: 2026-11-14
categories: [PS, LeetCode]
tags: ["math", "binary exponentiation", "warm up"]
slug: leetcode-50
media_subpath: /assets/img/posts/leetcode-50/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/powx-n/)
{: .prompt-info }

---

## 1. 아이디어

$x$의 $n$제곱을 구하는 문제로, $n$이 최대 약 21억이라 $n$번 곱할 수는 없고 이진 거듭제곱으로 곱셈 횟수를 로그 수준으로 줄여 푼다. $n$이 음수이면 $-n$제곱의 역수를 취한다.

표준 라이브러리는 같은 거듭제곱을 내장 기능 한 번으로 얻는 동등한 대안이다.

---

## 2. 코드

### 풀이 1: 이진 거듭제곱 [Java][C++][Python]

```java
class Solution {
    public double myPow(double x, int n) {
        if (n >= 0) {
            return binpow(x, n);
        } else {
            return 1 / binpow(x, -(long) n);
        }
    }

    static double binpow(double a, long n) {
        double res = 1;
        while (n > 0) {
            if ((n & 1) > 0) res *= a;
            a *= a;
            n >>= 1;
        }

        return res;
    }
}
```

`n`이 `int`의 최솟값이면 `-n`에서 오버플로우가 일어나 여전히 음수이므로 `-(long) n`으로 넓혀 부호를 뒤집었다.

```c++
#include <bits/stdc++.h>
using namespace std;

class Solution {
   public:
    double binpow(double a, long long n) {
        double res = 1;
        while (n > 0) {
            if (n & 1) res *= a;
            a *= a;
            n >>= 1;
        }

        return res;
    }

    double myPow(double x, int n) {
        if (n >= 0) {
            return binpow(x, n);
        } else {
            return 1 / binpow(x, -1LL * n);
        }
    }
};
```

`n`이 `int`의 최솟값이면 `-n`에서 오버플로우가 일어나므로 `-1LL * n`으로 `long long`으로 넓혀 부호를 뒤집었다.

```python
class Solution:
    def binpow(self, a, n):
        res = 1
        while n > 0:
            if n & 1:
                res *= a
            a *= a
            n >>= 1

        return res

    def myPow(self, x: float, n: int) -> float:
        if n >= 0:
            return self.binpow(x, n)
        else:
            return 1 / self.binpow(x, -n)
```

---

### 풀이 2: 표준 라이브러리 [Java][C++][Python]

```java
class Solution {
    public double myPow(double x, int n) {
        return Math.pow(x, n);
    }
}
```

`Math.pow`는 지수를 `double`로 받아 음수 지수와 `int`의 최솟값도 그대로 처리하므로 부호를 따로 다루지 않았다. 곱셈을 지수만큼 반복하지 않고 로그·지수 계산으로 한 번에 구하므로 지수가 커도 느리지 않다.

```c++
#include <bits/stdc++.h>
using namespace std;

class Solution {
   public:
    double myPow(double x, int n) {
        return pow(x, n);
    }
};
```

`std::pow`는 정수 지수를 `double`로 승격해 받아 음수 지수와 `int`의 최솟값도 그대로 처리하므로 부호를 따로 다루지 않았다. 곱셈을 지수만큼 반복하지 않고 로그·지수 계산으로 한 번에 구하므로 지수가 커도 느리지 않다.

```python
class Solution:
    def myPow(self, x: float, n: int) -> float:
        return x**n
```

실수의 `**`는 음수 지수도 그대로 처리해 실수를 돌려주므로 부호를 따로 다루지 않았다. 곱셈을 지수만큼 반복하지 않고 로그·지수 계산으로 한 번에 구하므로 지수가 커도 느리지 않다.

---
