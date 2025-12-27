---
title: "[자료구조/알고리즘] 슬라이딩 윈도우 (Sliding Window)"
slug: sliding-window
date: 2025-12-19
categories: [DSA]
tags: [Sliding Window]
toc: true
math: true
image: /assets/posts/sliding-window/thumbnail.drawio.svg
---

## 1. 슬라이딩 윈도우

슬라이딩 윈도우(Sliding Window)는 배열이나 리스트와 같은 데이터 구조에서 연속된 부분 배열의 합이나 애너그램(Anagram) 등을 효율적으로 계산하는 데 사용되는 일종의 테크닉이다. 주로 고정된 크기의 윈도우(Window)를 활용하여 데이터를 처리하며 이 과정에서 반복적인 계산을 줄여 시간복잡도를 낮출 수 있다.

슬라이딩 윈도우의 기본 아이디어는 윈도우의 크기를 $W$ 라고 할 때, 윈도우를 한 칸 옮기면 $(W - 1)$ 칸은 겹친다는 것을 활용한다. 이를 통해 이전 윈도우의 계산 결과를 다음 윈도우에 대한 계산에 활용할 수 있다.

---

## 2. 단순 탐색

주어진 배열($arr$)이 아래와 같을 때 배열에서 크기가 $4$ 인 연속된 구간의 합을 모두 구해야 하는 상황을 가정하자. 단순한 탐색 방법으로는 2중 반복문을 통해 바깥쪽 반복문은 각 원소를 출발점으로 순회하고 안쪽 반복문은 $4$ 칸의 합계를 구하는 방법이다.

![](/assets/posts/sliding-window/photo01.drawio.svg)

<br>

배열의 크기가 $10$ 이고 구간의 크기가 $4$ 이므로 인덱스 $0$ 부터 인덱스 $6$ 까지 각각 구간의 시작점으로 잡고 네 칸의 합을 구하면 된다. 아래와 같이 모든 크기 $4$ 인 연속된 구간의 합을 계산할 수 있다.

<br>

$$
i = 0,\qquad \displaystyle sum = \sum_{j=i}^{i+3} arr[j]
$$

![](/assets/posts/sliding-window/photo02.drawio.svg)

<br>

$$
i = 1,\qquad \displaystyle sum = \sum_{j=i}^{i+3} arr[j]
$$

![](/assets/posts/sliding-window/photo03.drawio.svg)

<br>

$$
i = 2,\qquad \displaystyle sum = \sum_{j=i}^{i+3} arr[j]
$$

![](/assets/posts/sliding-window/photo04.drawio.svg)

<br>

$$
i = 3,\qquad \displaystyle sum = \sum_{j=i}^{i+3} arr[j]
$$

![](/assets/posts/sliding-window/photo05.drawio.svg)

<br>

$$
i = 4,\qquad \displaystyle sum = \sum_{j=i}^{i+3} arr[j]
$$

![](/assets/posts/sliding-window/photo06.drawio.svg)

<br>

$$
i = 5,\qquad \displaystyle sum = \sum_{j=i}^{i+3} arr[j]
$$

![](/assets/posts/sliding-window/photo07.drawio.svg)

<br>

$$
i = 6,\qquad \displaystyle sum = \sum_{j=i}^{i+3} arr[j]
$$

![](/assets/posts/sliding-window/photo08.drawio.svg)

<br>

배열의 크기가 $N$, 구간의 크기가 $K$ 일 때, $(N - K + 1) \times K$ 의 연산이 필요하므로 $O(NK)$ 의 시간복잡도로 탐색을 완료할 수 있다.

---

## 3. 슬라이딩 윈도우 탐색

동일한 배열에 대해 슬라이딩 윈도우를 적용할 경우 $O(N)$ 의 시간복잡도로 탐색을 완료할 수 있다.

![](/assets/posts/sliding-window/photo01.drawio.svg)

<br>

먼저 인덱스 $0$ ~ $3$ 으로 이루어진 첫 구간의 합($sum$)을 계산해준다.

![](/assets/posts/sliding-window/photo02.drawio.svg)

<br>

두 번째 구간의 인덱스는 $1$ ~ $4$ 이다. 이때 이전 구간과 비교하면 인덱스 $1$ ~ $3$ 은 겹치는 영역이고, 인덱스 $4$ 는 추가되는 영역, 인덱스 $0$ 은 빠지는 영역이다. 이때 첫 구간의 합($sum$)에서 추가되는 영역의 값을 더해주고 빠지는 영역의 값을 빼주는 것으로 두 번째 구간의 합을 구할 수 있다.

![](/assets/posts/sliding-window/photo03.drawio.svg)

<br>

세 번째 구간 역시 마찬가지로 두 번째 구간의 합에서 $9$ 를 더하고 $5$ 를 빼주면 세 번째 구간의 합을 구할 수 있다.

![](/assets/posts/sliding-window/photo04.drawio.svg)

<br>

나머지 구간들 역시 마찬가지로 구할 수 있다.

<br>

$$
i = 3,\qquad sum' = sum - arr[2] + arr[6]
$$

![](/assets/posts/sliding-window/photo05.drawio.svg)

<br>

$$
i = 4,\qquad sum' = sum - arr[3] + arr[7]
$$

![](/assets/posts/sliding-window/photo06.drawio.svg)

<br>

$$
i = 5,\qquad sum' = sum - arr[4] + arr[8]
$$

![](/assets/posts/sliding-window/photo07.drawio.svg)

<br>

$$
i = 6,\qquad sum' = sum - arr[5] + arr[9]
$$

![](/assets/posts/sliding-window/photo08.drawio.svg)

<br>

위 과정을 통해 매번 구간의 합을 구간의 처음부터 하나하나 더해서 계산하는 것이 아니라 겹치지 않는 양 끝 정보만 처리함으로써 기존에 각 구간 당 $K$ 번의 연산이 필요했던 것 대비 $2$ 번의 연산만 필요하다. 이렇듯 윈도우가 미끄러지듯이 이동하며 윈도우 내 정보를 효율적으로 처리하는 테크닉이 슬라이딩 윈도우이다.

---

## 4. Problems

- [BaekJoon 21921번 - 블로그](https://www.acmicpc.net/problem/21921)
- [BaekJoon 24499번 - blobyum](https://www.acmicpc.net/problem/24499)
- [BaekJoon 15565번 - 귀여운 라이언](https://www.acmicpc.net/problem/15565)
- [BaekJoon 1522번 - 문자열 교환](https://www.acmicpc.net/problem/1522)
- [BaekJoon 1593번 - 문자 해독](https://www.acmicpc.net/problem/1593)
- [BaekJoon 20437번 - 문자열 게임 2](https://www.acmicpc.net/problem/20437)

---

## Ref

- [IOI KOREA - Sliding Window, 슬라이딩 윈도우](https://www.youtube.com/watch?v=uH9VJRIpIDY)
- [F-Lab - 슬라이딩 윈도우 알고리즘](https://f-lab.kr/insight/sliding-window-algorithm-20240516)
- [GeeksforGeeks - Sliding Window Technique](https://www.geeksforgeeks.org/dsa/window-sliding-technique/)

---
