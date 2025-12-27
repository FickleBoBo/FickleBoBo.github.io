---
title: "[자료구조/알고리즘] 유클리드 호제법 (Euclidean Algorithm)"
slug: euclidean-algorithm
date: 2025-12-17
categories: [DSA]
tags: [Number Theory, Euclidean Algorithm]
toc: true
math: true
image: /assets/posts/euclidean-algorithm/thumbnail.drawio.svg
---

## 1. 유클리드 호제법

유클리드 호제법(Euclidean Algorithm)은 두 자연수 또는 다항식의 최대공약수(GCD, Greatest Common Divisor)를 구하는 알고리즘의 하나이다. 호제법이란 말은 두 수가 서로 상대방 수를 나누어서 결국 원하는 수를 얻는다는 뜻이다.

유클리드 호제법의 기본 원리는 두 자연수(또는 다항식) $a$, $b$ 에 대해 $a$ 를 $b$ 로 나눈 나머지를 $r$ 이라 하면($a > b$) $a$ 와 $b$ 의 최대공약수는 $b$ 와 $r$ 의 최대공약수와 같다는 점이다. 이를 반복적으로 활용하여 최대공약수를 구하는 것으로 $78696$ 과 $19332$ 의 최대공약수는 아래와 같은 과정으로 구할 수 있다.

<br>

$$
\begin{aligned}
78696 &= 19332 \times 4 + 1368 \\\\
19332 &= 1368 \times 14 + 180 \\\\
1368  &= 180 \times 7 + 108 \\\\
180   &= 108 \times 1 + 72 \\\\
108   &= 72 \times 1 + 36 \\\\
72    &= 36 \times 2 + 0
\end{aligned}
$$

<br>

$72$ 를 $36$ 으로 나눈 나머지가 $0$ 이 됐다. 따라서, $78696$ 과 $19332$ 의 최대공약수는 $72$ 와 $36$ 의 최대공약수인 $36$ 이다.

---

## 2. 유클리드 호제법 성능

유클리드 호제법은 두 수 $a$, $b$ 에 대해 $O(\log{\min(a, b)})$ 의 시간복잡도를 갖는 알고리즘이다. 나머지가 최대한 느리게 줄어들수록 계산량이 많아지는데 Lamé's theorem에 따르면 연속한 피보나치 수 쌍의 경우가 worst case이다.

---

## 3. 유클리드 호제법 증명

자연수 $a$, $b$ 에 대해 $a > b$ 인 경우 아래와 같이 나타낼 수 있다.($0 \le r < b$)

<br>

$$
a = bq + r
$$

<br>

$a$ 와 $b$ 의 최대공약수를 $d$ 라고 하면 $a = d\alpha$, $b = d\beta$ 이고 ($\alpha$, $\beta$ 는 서로소) $r = a - bq = d\alpha - d\beta q = d(\alpha - \beta q)$ 이므로 $r$ 은 $d$ 의 배수다.

이제 $r = d\gamma$ 라고 하자. 여기서 $\beta$ 와 $\gamma$ 가 서로소면 $b = d\beta$ 와 $r = d\gamma$ 의 최대공약수도 $d$ 가 된다.

만약 $\beta$ 와 $\gamma$ 가 서로소가 아니라서 $d' > 1$ 이라는 공약수를 가질 경우 $\beta = d'\beta'$, $\gamma = d'\gamma'$ 으로 두었을 때,

<br>

$$
\begin{aligned}
\phantom{\Rightarrow\quad} & a = bq + r \qquad (0 \le r < b) \\\\
\Rightarrow\quad & d\alpha = d\beta q + d\gamma
    = dd'\beta' q + dd'\gamma'
    = dd'(\beta' q + \gamma') \\\\
\Rightarrow\quad & \alpha = d'(\beta' q + \gamma')
\end{aligned}
$$

<br>

이는 $\alpha$ 가 $d'$ 의 배수라는 뜻인데 $\beta$ 도 $d'$ 을 약수로 가져 배수가 되며 이는 $\alpha$ 와 $\beta$ 가 서로소인 것에 모순이므로 $\beta$ 와 $\gamma$ 가 $d' > 1$ 이라는 공약수를 가진다는 가정이 모순이다.

즉 $\beta$ 와 $\gamma$ 는 서로소이며 이는 $b$ 와 $r$ 의 최대공약수도 $d$ 라는 뜻이다.

$a$ 와 $b$ 의 최대공약수가 $b$ 와 $r$ 의 최대공약수와 같다는 점을 통해 점화식을 아래와 같이 세울 수 있다.

<br>

$$
gcd(a, b) =
\begin{cases}
a, & \text{if } b = 0 \\\\
gcd(b, a \bmod b), & \text{otherwise}
\end{cases}
$$

<br>

최소공배수(LCM, Least Common Multiple)는 두 수의 곱을 최대공약수로 나누면 간단하게 구할 수 있다.

<br>

$$
lcm(a, b) = \dfrac{a \times b}{gcd(a, b)}
$$

<br>

---

## 4. 유클리드 호제법 코드

유클리드 호제법은 재귀를 활용한 구현과 재귀를 활용하지 않은 구현 두 가지 모두 가능하다.

재귀를 활용할 경우 위 점화식을 그대로 코드로 옮기기만 하면 되며, 재귀를 활용하지 않을 경우 두 수를 swap 하는 과정을 추가해주면 된다.

두 방식 모두 $a < b$ 인 경우 다음 재귀나 swap을 통해 두 수가 바뀐 채 실행되기 때문에 두 수의 대소 관계를 고려하지 않아도 동작한다.

C++의 경우 C++ 17부터 `std::gcd`로 아예 함수를 제공한다.(`std::lcm`도 있다.)

### 1. 재귀를 활용한 유클리드 호제법 [Java]

```java
static int gcd(int a, int b) {
    if (b == 0) return a;
    return gcd(b, a % b);
}
```

### 2. 반복문을 활용한 유클리드 호제법 [Java]

```java
static int gcd(int a, int b) {
    while (b > 0) {
        a %= b;

        // swap
        int tmp = a;
        a = b;
        b = tmp;
    }
    return a;
}
```

### 3. 재귀를 활용한 유클리드 호제법 [C++]

```c++
int gcd(int a, int b) {
    if (b == 0) return a;
    return gcd(b, a % b);
}
```

### 4. 반복문을 활용한 유클리드 호제법 [C++]

```c++
int gcd(int a, int b) {
    while (b > 0) {
        a %= b;

        // swap
        int tmp = a;
        a = b;
        b = tmp;
    }
    return a;
}
```

---

## 5. Problems

- [BaekJoon 9613번 - GCD 합](https://www.acmicpc.net/problem/9613)
- [BaekJoon 1735번 - 분수 합](https://www.acmicpc.net/problem/1735)
- [BaekJoon 5347번 - LCM](https://www.acmicpc.net/problem/5347)
- [BaekJoon 17087번 - 숨바꼭질 6](https://www.acmicpc.net/problem/17087)

---

## Ref

- [wikipedia - 유클리드 호제법](https://ko.wikipedia.org/wiki/%EC%9C%A0%ED%81%B4%EB%A6%AC%EB%93%9C_%ED%98%B8%EC%A0%9C%EB%B2%95)
- [cp-algorithms - Euclidean Algorithm](https://cp-algorithms.com/algebra/euclid-algorithm.html)

---
