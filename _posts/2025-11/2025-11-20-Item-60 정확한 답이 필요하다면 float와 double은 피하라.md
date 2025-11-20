---
title: "[Item-60] 정확한 답이 필요하다면 float와 double은 피하라"
date: 2025-11-20
categories: [Book, Effective Java 3/E]
tags: [Effective Java 3/E]
toc: true
math: true
image: /assets/posts/2025-11/Item-60%20정확한%20답이%20필요하다면%20float와%20double은%20피하라/thumbnail.jpg
---

## Intro

float와 double 타입은 과학과 공학 계산용으로 설계되었다. 이진 부동소수점 연산에 쓰이며, 넓은 범위의 수를 빠르게 정밀한 '근사치'로 계산하도록 세심하게 설계되었다. 따라서 정확한 결과가 필요할 때는 사용하면 안 된다. float와 double 특히 금융 관련 계산과는 맞지 않는다. 0.1 혹은 10의 음의 거듭제곱수를 표현할 수 없기 때문이다. Java를 사용하면 int 혹은 long 같은 정수형 타입이나 BigInteger, BigDecimal 같은 클래스를 활용하자.

---

## 부동소수점 오차

아래는 부동소수점 오차의 예시로 오차는 양의 방향으로도 음의 방향으로도 발생할 수 있다. 이는 부등호를 사용해도 오류가 발생할 수 있다. PS에서 `Math.pow`나 `Math.sqrt` 연산 시 유의해야 한다.

```java
public class Main {
    public static void main(String[] args) {
        double x = 0.1 + 0.2;
        System.out.println("x = " + x);
        System.out.println(x > 0.3);

        double y = 1.0 - 0.9;
        System.out.println("y = " + y);
        System.out.println(y < 0.1);

        double z = 0.2 + 0.7;
        System.out.println("z = " + z);
        System.out.println(z < 0.9);
    }
}
```

실행 결과

```
x = 0.30000000000000004
true
y = 0.09999999999999998
true
z = 0.8999999999999999
true
```

---

## BigInteger, BigDecimal

BigInteger를 통해 메모리가 허락하는한 큰 수 연산을 수행할 수 있으며, BigDecimal을 통해 소수부가 있는 경우에도 수를 다룰 수 있다. BigDecimal의 경우 수의 표현 자체에 대한 오차는 없지만 예상할 수 있는 오차는 존재한다. 1/3 같이 소수부가 무한할 경우 BigDecimal은 반올림을 개발자가 지정할 것을 강제한다. 이 때문에 오차가 발생하더라도 예상 및 통제가 가능하다.

---

## Etc.

- [팬티엄 CPU 부동소수점 나눗셈 연산 버그](https://ko.wikipedia.org/wiki/%ED%8E%9C%ED%8B%B0%EC%97%84_FDIV_%EB%B2%84%EA%B7%B8)
- [부동소수점 반올림 오차로 지수 변동](https://en.wikipedia.org/wiki/Vancouver_Stock_Exchange)
- [부동소수점 누적 오차로 미사일 위치 계산 실패](https://en.wikipedia.org/wiki/MIM-104_Patriot)

---
