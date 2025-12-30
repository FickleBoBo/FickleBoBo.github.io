---
title: "[자료구조/알고리즘] CCW (Counter-Clockwise)"
slug: counter-clockwise
date: 2025-12-29
categories: [DSA]
tags: [Geometry, CCW]
toc: true
math: true
image: /assets/posts/counter-clockwise/thumbnail.drawio.svg
---

## 1. CCW

<br>

CCW(Counter-Clockwise)는 반시계 방향이라는 뜻으로, 평면 상의 세 점의 상대적인 방향을 판별하는 알고리즘이다.

서로 다른 세 점 $A$, $B$, $C$ 가 있을 때, $A \rightarrow B \rightarrow C$ 가 시계 방향인지 반시계 방향인지 아니면 일직선인지 판별할 수 있다.

---

## 2. 벡터의 외적

<br>

두 벡터 $A$, $B$ 의 외적(Cross Product)은 두 벡터 $A$, $B$ 에 모두 수직이며 크기는 $\lVert A \times B \rVert = \lVert A \rVert \, \lVert B \rVert \sin\theta$ 인 벡터가 된다. 교환 법칙이 성립하지 않아 순서에 따라 크기는 같고 방향이 반대인 벡터가 나온다.

![](/assets/posts/counter-clockwise/photo01.drawio.svg)

두 벡터 $A$, $B$ 가 각각 $A = (a_1,\ a_2,\ a_3)$, $B = (b_1,\ b_2,\ b_3)$ 일 때, 두 벡터의 외적 벡터는 $(a_2b_3 - a_3b_2,\ a_3b_1-a_1b_3,\ a_1b_2-a_2b_1)$ 가 된다. 외적 벡터의 방향은 간단하게 벡터 $A$ 방향으로 오른손 검지 손가락을 펴고, 벡터 $B$ 방향으로 오른손 검지 손가락을 말 때, 오른손 엄지 손가락이 가리키는 방향이다.

---

## 3. 위치 관계 판정

<br>

아래와 같이 평면 위에 세 점 $A$, $B$, $C$ 가 있을 때, $A \rightarrow B \rightarrow C$ 가 시계 방향인지 반시계 방향인지 아니면 일직선인지 판별해보자.

![](/assets/posts/counter-clockwise/photo02.drawio.svg)

<br>

$A \rightarrow B \rightarrow C$ 는 아래와 같이 반시계 방향이다.

![](/assets/posts/counter-clockwise/photo03.drawio.svg)

<br>

$A \rightarrow B \rightarrow C$ 의 방향 판별은 벡터 $\overrightarrow{AB}$ 와 벡터 $\overrightarrow{AC}$ 의 외적 벡터의 방향을 보면 알 수 있다. 외적 벡터의 방향이 화면 밖으로 나오는 방향이면 $A \rightarrow B \rightarrow C$ 는 반시계 방향이고, 외적 벡터의 방향이 화면 안으로 들어가는 방향이면 $A \rightarrow B \rightarrow C$ 는 시계 방향이다.

![](/assets/posts/counter-clockwise/photo04.drawio.svg)

세 점의 좌표가 각각 $A = (a_1,\ a_2,\ 0)$, $B = (b_1,\ b_2,\ 0)$, $C = (c_1,\ c_2,\ 0)$ 라고 하면 벡터 $\overrightarrow{AB}$ 는 $(b_1 - a_1,\ b_2 - a_2,\ 0)$, 벡터 $\overrightarrow{AC}$ 는 $(c_1 - a_1,\ c_2 - a_2,\ 0)$ 가 되며 외적 벡터는 $(0,\ 0,\ (b_1 - a_1)(c_2 - a_2) - (b_2 - a_2)(c_1 - a_1))$ 가 된다. 외적 벡터의 방향은 z축 성분의 부호로 판단할 수 있으므로 $(b_1 - a_1)(c_2 - a_2) - (b_2 - a_2)(c_1 - a_1)$ 가 양수이면 반시계 방향, 음수이면 시계 방향임을 알 수 있다.

<br>

아래와 같이 세 점이 일직선 상에 위치한 경우

![](/assets/posts/counter-clockwise/photo05.drawio.svg)

<br>

벡터 $\overrightarrow{AB}$ 와 벡터 $\overrightarrow{AC}$ 는 아래와 같다.

![](/assets/posts/counter-clockwise/photo06.drawio.svg)

세 점이 일직선 상에 있는 경우 또는 좌표가 동일한 두 점이 존재하는 경우 외적 벡터의 방향은 $0$ 이 된다. 이를 통해 세 점이 일직선 상에 있거나 좌표가 동일한 두 점이 있는지 여부도 판단할 수 있다.

---

## 4. CCW 코드

<br>

세 점의 좌표가 각각 $A = (x_1,\ y_1)$, $B = (x_2,\ y_2)$, $C = (x_3,\ y_3)$ 일 때, $A \rightarrow B \rightarrow C$ 의 방향을 구하는 CCW 코드는 아래와 같다. CCW는 방향 정보가 의미가 있고 크기 정보는 별 의미가 없어서 보통 $-1$, $0$, $1$ 같이 부호만 반환을 많이 한다.

<br>

### 1. CCW [Java]

`Integer.signum` 메서드로 부호만 반환할 수 있다.

```java
static int ccw(int x1, int y1, int x2, int y2, int x3, int y3) {
    return Integer.signum((x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1));
}
```

<br>

### 2. CCW [C++]

```c++
int ccw(int x1, int y1, int x2, int y2, int x3, int y3) {
    int cross = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1);
    return (cross > 0) - (cross < 0);
}
```

---

## 5. Problems

<br>

- [BaekJoon 1064번 - 평행사변형](https://www.acmicpc.net/problem/1064)

---

## Ref

<br>

- [cp-algorithms - Cross Product](https://cp-algorithms.com/geometry/basic-geometry.html#cross-product)

---
