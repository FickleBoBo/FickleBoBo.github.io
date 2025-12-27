---
title: "[자료구조/알고리즘] 이진 거듭제곱 (Binary Exponentiation)"
slug: binary-exponentiation
date: 2025-12-10
categories: [DSA]
tags: [Math, Divide and Conquer, Binary Exponentiation]
toc: true
math: true
image: /assets/posts/binary-exponentiation/thumbnail.drawio.svg
---

## 1. 이진 거듭제곱

이진 거듭제곱(Binary Exponentiation, Exponentiation by Squaring)은 $a^n$ 연산의 결과를 $O(\log{n})$ 의 시간복잡도로 해결하는 알고리즘이다.

$a^n$ 은 $a$ 를 $n$ 번 곱한 수이므로 반복문을 활용해 $a \times a \times \cdots \times a$ 처럼 $a$ 를 $n$ 번을 곱하면 시간복잡도는 $O(n)$ 이 된다. 재귀를 활용할 경우 $a^0 = 1$, $a^n = a \times a^{n-1}$ 을 종료 조건과 재귀 조건으로 활용해 재귀 함수를 만들 수 있고, 이 경우 재귀 스택은 $n$ 번 쌓이게 되며 역시 시간복잡도가 $O(n)$ 이 된다.

---

## 2. 이진 거듭제곱 아이디어

이진 거듭제곱의 핵심 아이디어는 지수인 $n$ 을 2진수로 표현하여 계산을 나누는 것이다.

예를 들어 $3^{13}$ 의 경우 아래와 같이 2진수로 표현 후, $a^{n_1 + n_2} = a^{n_1} \times a^{n_2}$ 을 통해 계산을 나눌 수 있다.

<br>

$$
3^{13} = 3^{1101_2} = 3^{1000_2 + 0100_2 + 0001_2} = 3^8 \times 3^4 \times 3^1
$$

<br>

위 방식으로 지수를 나눌 경우 2진수의 자릿수는 $\lfloor \log_2{n} \rfloor + 1$ 개가 되며, 이 때문에 $a^1, a^2, a^4 \ldots a^{\lfloor \log_2{n} \rfloor}$ 이 무엇인지만 안다면 $O(\log{n})$ 의 시간복잡도로 연산을 할 수 있다.

각 항들을 보면 지수가 2배씩 증가하는 것을 볼 수 있는데 $a^n = (a^{\frac{n}{2}})^2$ 을 통해 첫 항만 알면 다음 항을 상수 시간 내에 구할 수 있다. $3^{13}$ 의 경우 아래와 같은 과정으로 각 항을 빠르게 알아낼 수 있다.

<br>

$$
\begin{aligned}
3^1 &= 3 \\\\
3^2 &= (3^1)^2 = 3^2 = 9 \\\\
3^4 &= (3^2)^2 = 9^2 = 81 \\\\
3^8 &= (3^4)^2 = 81^2 = 6561
\end{aligned}
$$

<br>

이렇게 알아낸 각 항의 값을 통해 $3^{13} = 3^8 \times 3^4 \times 3^1 = 6561 \times 81 \times 3 = 1594323$ 으로 이진 거듭제곱을 활용해 3개의 항만으로 연산 결과를 알 수 있다.

재귀를 활용할 경우도 동일한 아이디어를 활용하며 점화식은 아래와 같다.

<br>

$$
a^n =
\begin{cases}
1, & \text{if } n = 0 \\\\
\left(a^{\frac{n}{2}}\right)^2, & \text{if } n > 0 \text{ and } n \text{ even} \\\\
a \times \left(a^{\frac{n-1}{2}}\right)^2, & \text{if } n > 0 \text{ and } n \text{ odd}
\end{cases}
$$

<br>

이진 거듭제곱은 자연수의 거듭제곱 뿐만 아니라 곱셈에 대한 결합법칙을 만족하는 다양한 연산에 응용될 수 있다. 예를 들면 행렬 역시 곱셈에 대한 결합법칙이 성립하기 때문에 행렬의 거듭제곱 역시 이진 거듭제곱으로 빠르게 계산할 수 있다.

---

## 3. 이진 거듭제곱 코드

반복문을 활용한 이진 거듭제곱은 $n$ 에 대한 2진수 표현과 비트 연산을 활용해 이진 거듭제곱을 구현한다. 먼저 거듭제곱의 결과를 나타내는 변수 $res$ 를 $1$ 로 초기화한다. $n$ 과 자연수 $1$ 과의 비트 AND 연산은 $n$ 을 2진수로 나타냈을 때 마지막 자릿수가 $1$ 인지 여부를 알 수 있다. 2진수로 나타냈을 때 1인 비트는 계산에 포함하는 항이고 0인 비트는 계산에 포함하지 않는 항이므로 1일 경우 $res = res * a$ 로 해당 항을 곱해준다. 이후 다음 항에서 이 과정을 반복해야 하는데 이때 $a$ 는 거듭제곱을 하면 다음 항의 값이 되고, $n$ 은 비트 시프트 연산으로 2진수로 나타낸 끝 자리를 날려서 다음 비트로 이동한 효과를 주면 된다. 비트 연산 대신 몫과 나머지를 구하는 방식으로 구현해도 된다.

재귀를 활용한 이진 거듭제곱은 위의 재귀 점화식을 그대로 구현하면 된다. $a^0 = 1$ 이 종료 조건으로 $n = 0$ 일 때, $1$ 을 반환하면 되며 그 외의 경우 $n$ 이 짝수면 $a^{\frac{n}{2}}$, $n$ 이 홀수면 $a^{\frac{n-1}{2}}$ 의 재귀 반환 값을 $half$ 변수에 담고 $n$ 이 짝수면 $half \times half \times a$, $n$ 이 홀수면 $half \times half$ 를 반환하면 된다. 홀수를 $2$ 로 나눌 경우 나머지를 버림 처리하는 언어의 특성까지 활용하면 $half$ 를 구할 때 $n$ 이 짝수인지 홀수인지 여부를 신경쓰지 않아도 된다.

구현 측면에서는 재귀를 활용한 방식이 좀 더 직관적이고 간단하지만 재귀 스택에 대한 오버 헤드가 있어서 동일한 시간복잡도여도 반복문을 활용한 방식이 일반적으로 좀 더 빠르다.

### 1. 반복문을 활용한 이진 거듭제곱 [Java]

```java
static int binPow(int a, int n) {
    int res = 1;
    while (n > 0) {
        if ((n & 1) > 0) res *= a;
        a = a * a;
        n >>= 1;
    }
    return res;
}
```

### 2. 재귀를 활용한 이진 거듭제곱 [Java]

```java
static int binPow(int a, int n) {
    if (n == 0) return 1;
    int half = binPow(a, n / 2);
    if (n % 2 == 1) {
        return half * half * a;
    } else {
        return half * half;
    }
}
```

### 3. 반복문을 활용한 이진 거듭제곱 [C++]

```c++
int binpow(int a, int n) {
    int res = 1;
    while (n > 0) {
        if (n & 1) res *= a;
        a = a * a;
        n >>= 1;
    }
    return res;
}
```

### 4. 재귀를 활용한 이진 거듭제곱 [C++]

```c++
int binpow(int a, int n) {
    if (n == 0) return 1;
    int half = binpow(a, n / 2);
    if (n % 2) {
        return half * half * a;
    } else {
        return half * half;
    }
}
```

---

## 4. Problems

- [BaekJoon 1629번 - 곱셈](https://www.acmicpc.net/problem/1629)
- [BaekJoon 10830번 - 행렬 제곱](https://www.acmicpc.net/problem/10830)

---

## Ref

- [cp-algorithms - Binary Exponentiation](https://cp-algorithms.com/algebra/binary-exp.html)
- [IOI KOREA - 빠른 거듭제곱](https://www.youtube.com/watch?v=6LBjvH39WNo)

---
