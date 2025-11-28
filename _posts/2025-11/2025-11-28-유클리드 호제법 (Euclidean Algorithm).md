---
title: "[알고리즘] 유클리드 호제법 (Euclidean Algorithm)"
date: 2025-11-28
categories: [Algorithm, Math]
tags: [수학, 정수론, 유클리드 호제법]
toc: true
math: true
image: /assets/posts/2025-11/유클리드%20호제법%20(Euclidean%20Algorithm)/thumbnail.drawio.svg
---

## 유클리드 호제법

유클리드 호제법은 두 자연수 또는 다항식의 최대공약수를 구하는 알고리즘의 하나이다. 호제법이란 말은 두 수가 서로 상대방 수를 나누어서 결국 원하는 수를 얻는다는 뜻이다. 기본 원리는 두 자연수(또는 다항식) $a$, $b$ 에 대해 $a$ 를 $b$ 로 나눈 나머지를 $r$ 이라 하면($a > b$) $a$ 와 $b$ 의 최대공약수는 $b$ 와 $r$ 의 최대공약수와 같다는 점이다. 이를 반복적으로 활용하여 최대공약수를 구하는 것으로 $78696$ 과 $19332$ 의 최대공약수는 아래와 같은 과정으로 구할 수 있다.

$$
\begin{aligned}
78696 &= 19332 \times 4 + 1368 \\
19332 &= 1368 \times 14 + 180 \\
1368  &= 180 \times 7 + 108 \\
180   &= 108 \times 1 + 72 \\
108   &= 72 \times 1 + 36 \\
72    &= 36 \times 2 + 0
\end{aligned}
$$

따라서, 최대공약수는 $36$ 이다.

TMI로 최대공약수는 GCD (Greatest Common Divisor), 최소공배수는 LCM(Least Common Multiple)으로 불려서 알고리즘에서 함수나 메서드명도 여기에 맞춰준다.

---

## 유클리드 호제법 성능

유클리드 호제법은 두 수 $a$, $b$ 에 대해 $O(\log{min(a, b)})$ 의 시간복잡도를 갖는 알고리즘이다. 나머지가 최대한 느리게 줄어들수록 계산량이 많아지는데 연속한 피보나치 수 쌍의 경우가 worst case이다.

---

## 유클리드 호제법 증명

자연수 $a$, $b$ 에 대해 $a > b$ 인 경우 아래와 같이 나타낼 수 있다.

$$
a = bq + r \qquad (0 \le r < b)
$$

$a$ 와 $b$ 의 최대공약수를 $d$ 라고 하면 $a = d\alpha$, $b = d\beta$ 이고 ($\alpha$, $\beta$ 는 서로소) $r = a - bq = d\alpha - dq\beta = d(\alpha - q\beta)$ 이므로 $r$ 은 $d$ 의 배수다.

이제 $r = d\gamma$ 라고 하자. 여기서 $\beta$ 와 $\gamma$ 가 서로소면 $b = d\beta$ 와 $r = d\gamma$ 의 최대공약수도 $d$ 가 된다.

만약 $\beta$ 와 $\gamma$ 가 서로소가 아니라서 $d' > 1$ 이라는 공약수를 가질 경우 $\beta = d'\beta'$, $\gamma = d'\gamma'$ 으로 두었을 때,

$$
\begin{alignat*}{4}
a &= bq + r \\[6pt]
\Rightarrow\quad
d\alpha &{}= d\beta q + d\gamma
&{}= dd'\beta' q + dd'\gamma'
&{}= dd'(\beta' q + \gamma') \\[6pt]
\Rightarrow\quad
\alpha &= d'(\beta' q + \gamma')
\end{alignat*}
$$

이는 $\alpha$ 가 $d'$ 의 배수라는 뜻인데 $\beta$ 도 $d'$ 을 공약수로 가져 배수가 되며 이는 $\alpha$ 와 $\beta$ 가 서로소인 것에 모순이므로 $\beta$ 와 $\gamma$ 가 $d' > 1$ 이라는 공약수를 가진다는 가정이 모순이다.

즉 $\beta$ 와 $\gamma$ 는 서로소이며 이는 $b$ 와 $r$ 의 최대공약수도 $d$ 이다.

---

## 유클리드 호제법 코드

### 유클리드 호제법 [Java]

재귀를 활용하면 깔끔하게 작성할 수 있다. $b$가 $a$보다 큰 경우 첫 재귀에서 두 수의 위치가 바뀌게 되어 범용적으로 활용할 수 있다.

```java
public static int gcd(int a, int b) {
    if (b == 0) return a;
    return gcd(b, a % b);
}
```

---

## Ref

- [wikipedia - 유클리드 호제법](https://ko.wikipedia.org/wiki/%EC%9C%A0%ED%81%B4%EB%A6%AC%EB%93%9C_%ED%98%B8%EC%A0%9C%EB%B2%95)
- [cp-algorithms - 유클리드 호제법](https://cp-algorithms.com/algebra/euclid-algorithm.html?utm_source=chatgpt.com)

---
