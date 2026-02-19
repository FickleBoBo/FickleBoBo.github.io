---
title: "[자료구조/알고리즘] 누적 합 (Prefix Sum)"
slug: prefix-sum
date: 2025-12-22
categories: [DSA]
tags: [Prefix Sum]
toc: true
math: true
image: /assets/posts/prefix-sum/thumbnail.drawio.svg
---

## 1. 누적 합

<br>

**누적 합(Prefix Sum)**은 배열의 앞에서부터의 합을 미리 계산해 두는 일종의 **전처리(Preprocessing)** 기법이다.

주어진 배열에서 반복적으로 임의의 구간의 합을 구해야 하는 문제를 상상해보자. 배열의 크기가 $N$, 쿼리의 수가 $M$ 일 때, 각 쿼리마다 매번 주어진 구간의 시작 위치부터 끝 위치까지 더하는 과정을 반복한다면 $O(N \times M)$ 의 시간복잡도와 $O(1)$ 의 공간복잡도가 소요될 것이다.

이때 누적 합을 활용하면 $O(N)$ 의 공간복잡도를 소요하는 대신 $O(N + M)$ 의 시간복잡도로 문제를 해결할 수 있다.

<br>

누적 합의 기본 아이디어는 $A_1, A_2, \ldots, A_N$ 과 같이 주어진 수열이 있을 때, $A_i$ 부터 $A_j$ 까지의 합은 $A_1$ 부터 $A_j$ 까지의 합에서 $A_1$ 부터 $A_{i-1}$ 까지의 합을 뺀 것과 같다는 것이다. $A_1$ 부터 $A_j$ 까지의 합과 $A_1$ 부터 $A_{i-1}$ 까지의 합 모두 누적 합 배열에서 $O(1)$ 의 시간복잡도로 조회가 가능하기에 반복되는 구간 합 쿼리를 효율적으로 해결할 수 있다.

다만 누적 합은 원본 배열에 갱신이 발생할 경우 누적 합 배열에서 갱신 위치를 포함하는 원소들도 전부 갱신해줘야 해서 주어진 배열이 **정적 배열일 때 효율적**이다.

---

## 2. 누적 합 예시

<br>

주어진 배열($arr$)이 아래와 같을 때 다음과 같이 누적 합 배열($prefix\ sum$)을 생성할 수 있다.

![](/assets/posts/prefix-sum/photo01.drawio.svg)

이때 누적 합 배열의 인덱스 $0$ 은 패딩으로 두고 $arr[0]$ 부터 $arr[i]$ 까지의 합을 $prefix\ sum$ 의 $i + 1$ 번 인덱스에 저장하는 방식으로 만들면 코드를 깔끔하게 작성할 수도 있고 주어진 구간이 첫 원소의 위치를 $1$ 로 가정할 경우 쿼리도 깔끔하게 작성할 수 있다. 첫 번째 원소부터 $i$ 번째 원소까지의 합은 첫 번째 원소부터 $i - 1$ 번째 원소까지의 합에 $i$ 번째 원소를 더하면 된다는 점에서 $O(N)$ 의 시간복잡도로 누적 합 배열을 생성할 수 있다.

<br>

원본 배열의 인덱스 $2$ 부터 $4$ 까지의 구간 합은 누적 합 배열의 $5$ 번 원소에서 $2$ 번 원소의 값을 뺀 것으로 구할 수 있다.

![](/assets/posts/prefix-sum/photo02.drawio.svg)

<br>

원본 배열의 인덱스 $7$ 부터 $8$ 까지의 구간 합은 누적 합 배열의 $9$ 번 원소에서 $7$ 번 원소의 값을 뺀 것으로 구할 수 있다.

![](/assets/posts/prefix-sum/photo03.drawio.svg)

---

## 3. 누적 합 코드

<br>

인덱스 $0$ 에 패딩을 준 덕분에 누적 합 배열의 첫 번째 원소를 초기화할 때 음수 인덱스를 참조하게 되는 예외 처리를 하지 않아도 되게 된다.

<br>

### 1. 누적 합 [Java]

```java
int[] psum = new int[1 + n];

for (int i = 1; i <= n; i++) {
    psum[i] = psum[i - 1] + arr[i - 1];
}
```

<br>

### 2. 누적 합 [C++]

```c++
vector<int> psum(1 + n);

for (int i = 1; i <= n; i++) {
    psum[i] = psum[i - 1] + v[i - 1];
}
```

---

## 4. Problems

<br>

- [BaekJoon 11659번 - 구간 합 구하기 4](https://www.acmicpc.net/problem/11659)
- [BaekJoon 21921번 - 블로그](https://www.acmicpc.net/problem/21921)

---

## Ref

<br>

- [BOJ BOOK - 누적 합](https://book.acmicpc.net/algorithm/prefix-sum)

---
