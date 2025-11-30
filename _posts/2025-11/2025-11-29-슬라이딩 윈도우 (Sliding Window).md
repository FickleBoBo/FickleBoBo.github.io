---
title: "[알고리즘] 슬라이딩 윈도우 (Sliding Window)"
date: 2025-11-29
categories: [Algorithm, Two Pointers & Sliding Window]
tags: [슬라이딩 윈도우]
toc: true
math: true
image: /assets/posts/2025-11/슬라이딩%20윈도우%20(Sliding%20Window)/thumbnail.drawio.svg
---

## 1. 슬라이딩 윈도우

슬라이딩 윈도우 알고리즘은 배열이나 리스트와 같은 데이터 구조에서 연속된 부분 배열의 합이나 최댓값 등을 효율적으로 계산하는 데 사용되는 일종의 테크닉이다. 주로 고정된 크기의 윈도우를 활용하여 데이터를 처리하며 이 과정에서 반복적인 계산을 줄여 시간복잡도를 낮출 수 있다.

---

## 2. 단순 탐색

주어진 배열이 아래와 같을 때 배열에서 크기가 $4$ 인 연속된 구간의 합을 모두 구해야 하는 상황을 가정하자. 단순한 방법으로는 2중 반복문을 통해 바깥쪽 반복문은 각 원소를 출발점으로 순회하고 안쪽 반복문은 $4$ 칸의 합계를 구하는 방법이다.

![](</assets/posts/2025-11/슬라이딩%20윈도우%20(Sliding%20Window)/photo01.drawio.svg>)

배열의 크기가 $10$ 이고 구간의 크기가 $4$ 이므로 인덱스 $0$ 부터 인덱스 $6$ 까지 각각 구간의 시작점으로 잡고 네 칸의 합을 구하면 된다. 아래와 같이 모든 크기 $4$ 인 연속된 구간의 합을 계산할 수 있다.

![](</assets/posts/2025-11/슬라이딩%20윈도우%20(Sliding%20Window)/photo02.drawio.svg>)
![](</assets/posts/2025-11/슬라이딩%20윈도우%20(Sliding%20Window)/photo03.drawio.svg>)
![](</assets/posts/2025-11/슬라이딩%20윈도우%20(Sliding%20Window)/photo04.drawio.svg>)
![](</assets/posts/2025-11/슬라이딩%20윈도우%20(Sliding%20Window)/photo05.drawio.svg>)
![](</assets/posts/2025-11/슬라이딩%20윈도우%20(Sliding%20Window)/photo06.drawio.svg>)
![](</assets/posts/2025-11/슬라이딩%20윈도우%20(Sliding%20Window)/photo07.drawio.svg>)
![](</assets/posts/2025-11/슬라이딩%20윈도우%20(Sliding%20Window)/photo08.drawio.svg>)

배열의 크기가 $N$, 구간의 크기가 $K$ 일 때, $O(NK)$ 의 시간복잡도로 탐색을 완료할 수 있다.

---

## 3. 슬라이딩 윈도우 탐색

동일한 배열에 대해 슬라이딩 윈도우를 적용할 경우 $O(N)$ 의 시간복잡도로 탐색을 완료할 수 있다.

![](</assets/posts/2025-11/슬라이딩%20윈도우%20(Sliding%20Window)/photo01.drawio.svg>)

먼저 인덱스 $0$ ~ $3$ 으로 이루어진 첫 구간의 합을 계산해준다.

![](</assets/posts/2025-11/슬라이딩%20윈도우%20(Sliding%20Window)/photo02.drawio.svg>)

두 번째 구간의 인덱스는 $1$ ~ $4$ 이다. 이때 이전 구간과 비교하면 겹치는 영역이 있고 새롭게 추가되거나 빠진 영역이 있다. 다시 인덱스 $1$ 부터 $4$ 까지 합을 계산하지 않고 이전 구간의 합에서 새로 추가된 구간의 값을 더하고 빠지는 구간의 값을 빼면 두 번째 구간의 합을 구할 수 있다.

![](</assets/posts/2025-11/슬라이딩%20윈도우%20(Sliding%20Window)/photo03.drawio.svg>)

세 번째 구간 역시 마찬가지로 두 번째 구간의 합에서 $9$ 를 더하고 $5$ 를 빼주면 세 번째 구간의 합을 구할 수 있다.

![](</assets/posts/2025-11/슬라이딩%20윈도우%20(Sliding%20Window)/photo04.drawio.svg>)

나머지 구간들 역시 마찬가지로 구할 수 있다.

![](</assets/posts/2025-11/슬라이딩%20윈도우%20(Sliding%20Window)/photo05.drawio.svg>)
![](</assets/posts/2025-11/슬라이딩%20윈도우%20(Sliding%20Window)/photo06.drawio.svg>)
![](</assets/posts/2025-11/슬라이딩%20윈도우%20(Sliding%20Window)/photo07.drawio.svg>)
![](</assets/posts/2025-11/슬라이딩%20윈도우%20(Sliding%20Window)/photo08.drawio.svg>)

위 과정을 통해 매번 구간의 합을 처음부터 더해서 계산하는 것이 아니라 양 끝 정보만 처리함으로써 기존에 각 구간 당 $K$ 번의 연산이 필요했던 것 대비 $2$ 번의 연산만 필요하다. 이렇듯 윈도우가 미끄러지듯이 이동하며 윈도우 내 정보를 효율적으로 처리하는 테크닉이 슬라이딩 윈도우이다.

---

## Ref

- [F-Lab - 슬라이딩 윈도우](https://f-lab.kr/insight/sliding-window-algorithm-20240516)

---
