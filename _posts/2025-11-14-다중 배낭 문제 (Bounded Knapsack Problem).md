---
title: "[자료구조/알고리즘] 다중 배낭 문제 (Bounded Knapsack Problem)"
slug: bounded-knapsack-problem
date: 2025-11-14
categories: [DSA]
tags: [Dynamic Programming, Knapsack]
toc: true
math: true
image: /assets/posts/bounded-knapsack-problem/thumbnail.png
---

## 1. 다중 배낭 문제

<br>

[0/1 배낭 문제](/posts/0-1-knapsack-problem) 가 각 물건이 1개씩 있고 배낭에 담느냐 안 담느냐를 선택하는 문제였다면 다중 배낭 문제는 각 물건이 1개 이상 있는 경우 배낭의 물건의 가치가 최대가 되게 하는 문제다. 이때 각 물건이 무한히 있지는 않다.

다중 배낭 문제는 이를 0/1 배낭 문제로 변형하여 해결할 수 있다.

---

## 2. 단순 변형

<br>

가장 간단한 방법은 각 물건 1개마다 0/1 배낭 문제를 적용하는 것이다. 물건의 무게와 가치가 $(6, 13)$ 인 물건이 2개, $(4, 8)$ 인 물건이 3개일 경우 총 5개의 물건에 대해 $N = 5$ 인 0/1 배낭 문제로 해결하는 것이다.

물건의 종류의 수가 $N$, 배낭에 담을 수 있는 무게의 최댓값이 $W$, 각 종류마다 $k_i$ 개의 물건이 있는 경우 단순한 방법으로는 $\displaystyle O(W \times \sum_{i=1}^{N} k_i)$ 의 시간복잡도가 소요된다.

간단한 방법이지만 총 물건의 수가 많을 경우 탐색량이 많다는 단점이 있다.

---

## 3. 이진 그룹핑 최적화 (Binary Grouping Optimization)

<br>

특정 물건이 $K$ 개 있을 경우 이를 $K$ 개로 분할해 0/1 배낭 문제를 적용하는 것을 좀 더 효율화한 것으로 보다 적은 그룹으로 분할하여 탐색량을 줄이는 기법이다.

핵심은 모든 자연수를 서로 다른 2의 거듭제곱의 합으로 표현할 수 있다는 것과 등비급수의 합으로 $1 + 2 + 4 + \ldots + 2^{k-1} = 2^k - 1$ 이면서 $$\{1, 2, 4, \ldots, 2^{k-1}\}$$ 의 부분집합의 합으로 $2^k$ 보다 작은 모든 자연수를 표현할 수 있다는 것이다. 이를 통해 $K$ 를 2의 거듭 제곱 그룹과 나머지($r < 2^k$)로 분리할 수 있고 그룹의 수는 $k + 1$ 개로 훨씬 줄일 수 있다.

이렇게 분리하면 $K = 2^k - 1 + r$ 이 된다.

이제 $1$ ~ $2^k - 1$ 까지는 2의 거듭 제곱 그룹의 조합으로 얻을 수 있고, 여기에 나머지를 더할 경우 $r$ ~ $2^k - 1 + r$ 까지 얻을 수 있다. 이때 $r < 2^k$ 이며 $2^k - 1 + r = K$ 이므로 $2^k$ ~ $K$ 까지 얻을 수 있어 $1$ ~ $K$ 사이의 모든 자연수를 2의 거듭 제곱 그룹과 나머지의 조합으로 얻을 수 있다.

<br>

예를 들면 $22$ 의 경우 $1 + 2 + 4 + 8 + 7$ 로 나눌 수 있다.

아래 그림으로 $1$ 부터 $22$ 까지 $$\{1, 2, 4, 8, 7\}$$ 의 조합으로 모든 수를 얻을 수 있는 것을 볼 수 있다. 기존 $22$ 개로 나눌 것을 $5$ 개로 나누어 효율적으로 탐색할 수 있다.

![](/assets/posts/bounded-knapsack-problem/photo01.drawio.svg)

<br>

위 과정에서 볼 수 있는 이진 그룹핑 최적화를 통해 $N = 22$ 인 0/1 배낭 문제를 $N = 5$ 인 0/1 배낭 문제로 해결할 수 있다. 물건의 종류의 수가 $N$, 배낭에 담을 수 있는 무게의 최댓값이 $W$, 각 종류마다 $k_i$ 개의 물건이 있는 경우 $\displaystyle O(W \times \sum_{i=1}^{N} \log{k_i})$ 의 시간복잡도로 해결할 수 있다.

---

## 4. Problems

<br>

- [BaekJoon 12920번 - 평범한 배낭 2](https://www.acmicpc.net/problem/12920)

---

## Ref

<br>

- [wikipedia - 배낭 문제](https://ko.wikipedia.org/wiki/%EB%B0%B0%EB%82%AD_%EB%AC%B8%EC%A0%9C)
- [cp-algorithms - Knapsack Problem](https://cp-algorithms.com/dynamic_programming/knapsack.html)

---
