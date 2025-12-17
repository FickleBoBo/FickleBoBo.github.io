---
title: "[알고리즘] 에라토스테네스의 체 (Sieve of Eratosthenes)"
date: 2025-12-17
categories: [Algorithm]
tags: [수학, 정수론, 소수 판정, 에라토스테네스의 체]
toc: true
math: true
image: /assets/posts/2025-12/에라토스테네스의%20체%20(Sieve%20of%20Eratosthenes)/thumbnail.drawio.svg
---

## 1. 에라토스테네스의 체

에라토스테네스의 체(Sieve of Eratosthenes)는 고대 그리스 수학자 에라토스테네스가 만들어 낸 소수를 찾는 방법으로 $N$ 보다 작거나 같은 모든 소수를 판정할 수 있는 빠르고 쉬운 알고리즘이다. 에라토스테네스의 체는 소수의 배수들은 소수가 아니라는 점을 활용하여 소수가 아닌 수들을 지워가며 최종적으로 소수를 찾는다.

---

## 2. 에라토스테네스의 체 성능

에라토스테네스의 체는 $O(N\log{\log{N}})$ 의 시간복잡도와 $O(N)$ 의 공간복잡도를 갖는 알고리즘이다.
시간복잡도가 조금 특이한데 소수의 배수를 지우는 과정에서 전체 연산 횟수가 소수의 역수들의 합에 비례하게 되는데 Mertens' second theorem에 의해 소수의 역수들의 합이 $\log{\log{N}}$ 에 비례하기 때문에 전체 구간을 곱한 $O(N\log{\log{N}})$ 이 시간복잡도가 된다. 공간복잡도의 경우 전체 구간만큼 소수를 판정할 공간이 필요하기 때문에 $O(N)$ 이 된다.

---

## 3. 에라토스테네스의 체 진행 과정

$1$ 부터 $100$ 사이의 소수를 구하는 과정을 살펴보자. 주어진 수들을 $10 \times 10$ 으로 나타내면 아래와 같다.

![](</assets/posts/2025-12/에라토스테네스의%20체%20(Sieve%20of%20Eratosthenes)/photo01.drawio.svg>)

$1$ 은 소수가 아니므로 소수가 아니라는 의미로 빨간색 칸으로 칠했다.

![](</assets/posts/2025-12/에라토스테네스의%20체%20(Sieve%20of%20Eratosthenes)/photo02.drawio.svg>)

$2$ 는 소수인데 에라토스테네스의 체는 $2$ 이상의 수에 대해 소수가 아니라고 판정되지 않았으면 소수로 판단한다. $2$ 는 현재 소수가 아니라고 판정되지 않았으므로 소수이다.

![](</assets/posts/2025-12/에라토스테네스의%20체%20(Sieve%20of%20Eratosthenes)/photo03.drawio.svg>)

$2$ 가 소수이므로 $2$ 의 배수들은 소수가 아니게 된다. $2$ 의 배수들을 노란색 칸으로 칠했다.

![](</assets/posts/2025-12/에라토스테네스의%20체%20(Sieve%20of%20Eratosthenes)/photo04.drawio.svg>)

소수가 아닌 수들을 거르고 난 후 모습은 아래와 같다.

![](</assets/posts/2025-12/에라토스테네스의%20체%20(Sieve%20of%20Eratosthenes)/photo05.drawio.svg>)

$3$ 은 소수인데 이는 현재 $3$ 이 소수가 아니라고 판정되지 않았기 때문이다.

![](</assets/posts/2025-12/에라토스테네스의%20체%20(Sieve%20of%20Eratosthenes)/photo06.drawio.svg>)

$3$ 이 소수이므로 $3$ 의 배수들은 소수가 아니게 된다. $3$ 의 배수들을 노란색 칸으로 칠했다. 이때 $6$ 의 경우 $3 \times 2 = 6$ 으로 이미 $2$ 의 배수를 거르는 과정에서 걸러지게 된다. 특정 소수 $p$ 에 대해 $p \times p$ 보다 작은 합성수는 $p$ 보다 작은 소수의 배수로 이미 걸러지기 때문에 $p^2$ 부터 거를 수를 탐색하는 방식으로 최적화를 할 수 있다. 현재 $p = 3$ 이므로 $9$ 부터 $3$ 의 배수를 거르면 된다.

![](</assets/posts/2025-12/에라토스테네스의%20체%20(Sieve%20of%20Eratosthenes)/photo07.drawio.svg>)

소수가 아닌 수들을 거르고 난 후 모습은 아래와 같다.

![](</assets/posts/2025-12/에라토스테네스의%20체%20(Sieve%20of%20Eratosthenes)/photo08.drawio.svg>)

$4$ 는 소수가 아니라고 판정됐기 때문에 넘어간다. 합성수의 배수는 이미 해당 합성수를 이룬 소수의 배수로 걸러지기 때문에 탐색할 필요가 없어서 소수의 배수만 탐색하는 방식으로 최적화를 할 수 있다. 모든 $4$ 의 배수는 $2$ 의 배수이므로 탐색할 필요가 없다.

다음은 $5$ 로 현재 소수가 아니라고 판정되지 않았으므로 소수이다.

![](</assets/posts/2025-12/에라토스테네스의%20체%20(Sieve%20of%20Eratosthenes)/photo09.drawio.svg>)

$5$ 의 배수인 $10$, $15$, $20$ 의 경우 $5 \times 2 = 10$, $5 \times 3 = 15$, $5 \times 4 = 20$ 로 전부 이미 걸러지는게 확정이기 때문에 $25$ 부터 탐색한다.

![](</assets/posts/2025-12/에라토스테네스의%20체%20(Sieve%20of%20Eratosthenes)/photo10.drawio.svg>)

소수가 아닌 수들을 거르고 난 후 모습은 아래와 같다.

![](</assets/posts/2025-12/에라토스테네스의%20체%20(Sieve%20of%20Eratosthenes)/photo11.drawio.svg>)

$6$ 은 소수가 아니라고 판정됐기 때문에 넘어간다. $7$ 은 소수이다.

![](</assets/posts/2025-12/에라토스테네스의%20체%20(Sieve%20of%20Eratosthenes)/photo12.drawio.svg>)

$49$ 부터 $7$ 의 배수를 탐색한다.

![](</assets/posts/2025-12/에라토스테네스의%20체%20(Sieve%20of%20Eratosthenes)/photo13.drawio.svg>)

소수가 아닌 수들을 거르고 난 후 모습은 아래와 같다.

![](</assets/posts/2025-12/에라토스테네스의%20체%20(Sieve%20of%20Eratosthenes)/photo14.drawio.svg>)

$8$, $9$, $10$ 은 소수가 아니다. $\sqrt{100} = 10$ 이기 때문에 $100$ 이하의 합성수는 반드시 $10$ 이하의 소수로 나누어진다. 따라서 $10$ 까지만 탐색하면 $100$ 이하의 모든 합성수를 걸러낼 수 있다. 탐색을 종료한 후 모습은 아래와 같으며 $25$ 개의 소수를 구할 수 있다.

![](</assets/posts/2025-12/에라토스테네스의%20체%20(Sieve%20of%20Eratosthenes)/photo15.drawio.svg>)

---

## 4. 에라토스테네스의 체 코드

기본적으로 2중 반복문을 활용하지만 최적화가 이루어져 $O(N^2)$ 의 시간복잡도가 아니다. 바깥쪽 반복문은 $\sqrt{N}$ 까지 배수를 탐색할 소수를, 안쪽 반복문은 소수일 경우 그 배수들을 거르는 역할을 한다. 정확하게 구현해야 최적의 시간복잡도로 동작한다.

### 1. 에라토스테네스의 체 [Java]

```java
static boolean[] sieve(int N) {
    boolean[] isPrime = new boolean[1 + N];
    Arrays.fill(isPrime, true);
    isPrime[0] = isPrime[1] = false;

    for (int i = 2; i * i <= N; i++) {
        if (isPrime[i]) {
            for (int j = i * i; j <= N; j += i) {
                isPrime[j] = false;
            }
        }
    }

    return isPrime;
}
```

### 2. 에라토스테네스의 체 [C++]

```c++
vector<bool> sieve(int n) {
    vector<bool> isPrime(1 + n, true);
    isPrime[0] = isPrime[1] = false;

    for (int i = 2; i * i <= n; i++) {
        if (isPrime[i]) {
            for (int j = i * i; j <= n; j += i) {
                isPrime[j] = false;
            }
        }
    }

    return isPrime;
}
```

---

## 5. Problems

- [백준 1929번 - 소수 구하기](https://www.acmicpc.net/problem/1929)
- [백준 17103번 - 골드바흐 파티션](https://www.acmicpc.net/problem/17103)
- [백준 15965번 - K번째 소수](https://www.acmicpc.net/problem/15965)
- [백준 2312번 - 수 복원하기](https://www.acmicpc.net/problem/2312)
- [백준 2960번 - 에라토스테네스의 체](https://www.acmicpc.net/problem/2960)
- [백준 1963번 - 소수 경로](https://www.acmicpc.net/problem/1963)
- [백준 1644번 - 소수의 연속합](https://www.acmicpc.net/problem/1644)

---

## Ref

- [cp-algorithms - Sieve of Eratosthenes](https://cp-algorithms.com/algebra/sieve-of-eratosthenes.html)

---
