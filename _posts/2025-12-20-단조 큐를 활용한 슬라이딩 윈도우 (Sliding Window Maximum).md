---
title: "[자료구조/알고리즘] 단조 큐를 활용한 슬라이딩 윈도우 (Sliding Window Maximum)"
slug: sliding-window-maximum
date: 2025-12-20
categories: [DSA]
tags: [Sliding Window, Data Structures, Priority Queue, Monotonic Queue]
toc: true
math: true
image: /assets/posts/sliding-window-maximum/thumbnail.drawio.svg
---

## 1. 단조 큐를 활용한 슬라이딩 윈도우

단조 큐를 활용한 슬라이딩 윈도우(Sliding Window Maximum)는 배열이나 리스트와 같은 데이터 구조에서 연속된 부분 배열의 최솟값이나 최댓값을 효율적으로 계산할 수 있는 일종의 테크닉이다. 기존 [슬라이딩 윈도우](/posts/sliding-window) 로 구간 합을 구할 때는 윈도우에서 나가는 정보와 들어오는 정보만 기존의 구간 합에서 갱신해주면 됐지만 최솟값이나 최댓값을 구할 경우 기존의 아이디어를 적용하기 어렵다. 이때 단조 큐를 활용하면 이 문제를 효율적으로 해결할 수 있다.

---

## 2. 단순 탐색

$N$ 개의 수 $A_1, A_2, \ldots, A_N$ 과 자연수 $L$ 이 주어지고 구간 $A_{i-L+1}$ ~ $A_i$ 의 최솟값 또는 최댓값을 구해야 할 때, 몇 번만 구해야 한다면 단순 탐색으로 간단하게 해결할 수 있지만 모든 $i$ 에 대해 최솟값 또는 최댓값을 구해야 할 경우 $O(N \times L)$ 만큼의 시간이 걸릴 것이다.

---

## 3. 힙을 이용한 구간 최댓값 계산

힙을 활용하면 삽입, 삭제에 $O(\log{N})$ 의 시간복잡도를 보이므로 모든 원소에 대해 진행 시 $O(N\log{N})$ 의 시간복잡도와 $O(N)$ 의 공간복잡도로 이 문제를 해결할 수 있다. 구간의 최솟값을 구해야 하면 최소힙, 구간의 최댓값을 구해야 하면 최대힙을 사용하면 되며 힙에는 해당 수의 인덱스와 값을 같이 저장하여 값을 기준으로 먼저 정렬하고 값이 동일하면 인덱스를 기준으로 정렬하면 된다.

이러면 윈도우를 한 칸씩 이동할 때 새로 추가되는 원소는 힙에 그냥 추가하면 되며 반복문으로 구간을 벗어난 원소들을 힙에서 전부 제거하면 된다. 구간에서 벗어났는지 여부를 판단하기 위해 인덱스를 같이 저장하며 힙 내에서 인덱스는 단조 증가 또는 단조 감소하지 않으므로 반복문을 활용해 제거해야 한다.(윈도우를 한 칸 이동할 때마다 1개를 제거함이 보장되지 않고 1개 이상 제거해야 할 수 있다.)

---

## 4. 단조 큐를 이용한 구간 최댓값 계산

주어진 수열이 $$\{1, 5, 2, 3, 6, 2, 3, 7, 3, 5, 2, 6\}$$ 이고 $L$ 이 $3$ 이며 모든 $i$ 에 대한 구간 $A_{i-L+1}$ ~ $A_i$ 의 최솟값을 구하는 경우 정답은 $$\{1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 2, 2\}$$ 이 된다. 이는 아래 표를 통해 확인할 수 있다.

![](/assets/posts/sliding-window-maximum/photo01.drawio.svg)

<br>

단조 큐를 활용한 슬라이딩 윈도우는 큐 내의 원소들이 선형 증가하는 단조 큐를 활용해서 이 문제를 $O(N)$ 의 시간복잡도와 $O(K)$ 의 공간복잡도로 효율적으로 해결한다. 이때 단조 큐는 현재 바라보는 윈도우의 정보를 가지고 있게 된다.

단조 큐를 활용한 슬라이딩 윈도우는 아래 4개의 아이디어를 활용한다.

1. 수열의 첫 번째 원소부터 순서대로 접근하며 덱의 뒤에 인덱스를 삽입하면 이 덱은 단조 큐가 된다.
2. 덱의 뒤에 인덱스를 삽입할 때, 구간의 최솟값 또는 최댓값이 될 수 없는 원소들을 뒤에서부터 전부 제거한 후 삽입하면 이 덱은 인덱스에 대해서도 값에 대해서도 단조성을 띈다. 나중에 등장한 값보다 최솟값 또는 최댓값의 대표성을 띄지 않는 값은 윈도우 내에서 더 이상 유용하지 않은 정보(최솟값이나 최댓값이 될 수 없는 정보)라 제거해도 상관없다.
3. 인덱스를 저장한 덱이 단조 큐를 이루므로 윈도우에서 빠지는 원소의 인덱스는 덱의 앞 원소를 조회하면 알 수 있다.
4. 구간의 최솟값 또는 최댓값은 덱이 값에 대해서도 단조성을 띄므로 덱의 앞 원소(인덱스)를 통해 원래 수열에서 조회하면 알 수 있다.

---

## 5. 단조 큐를 이용한 구간 최댓값 계산 진행 과정

아까와 동일한 수열 $$\{1, 5, 2, 3, 6, 2, 3, 7, 3, 5, 2, 6\}$$, 구간의 크기 $L = 3$ 에 대해 모든 구간의 최솟값을 단조 큐를 활용해서 구해보자.

<br>

$A_1$ 의 인덱스는 $0$, 값은 $1$ 이다. 구간은 $A_{-1}$ ~ $A_1$ 인데 구간을 벗어나는 경우는 무시한다고 하자. 그러면 실제 구간은 $A_1$ ~ $A_1$ 이 된다.

단조 큐가 비어있으므로 삭제는 일어나지 않고, 단조 큐가 비어있으므로 $1$ 보다 작거나 같은 원소가 없어 단조 큐에 인덱스를 삽입한다. 단조 큐의 맨 앞 원소를 통해 얻은 인덱스로 수열에서 조회하면 구간 $A_1$ ~ $A_1$ 의 최솟값은 $1$ 이 된다.

<br>

수열

![](/assets/posts/sliding-window-maximum/photo02.drawio.svg)

단조 큐 (인덱스 $0$ 삽입)

![](/assets/posts/sliding-window-maximum/photo03.drawio.svg)

<br>

$A_2$ 의 인덱스는 $1$, 값은 $5$ 이다. 구간은 $A_0$ ~ $A_2$ 인데 구간을 벗어나는 경우는 무시한다고 하자. 그러면 실제 구간은 $A_1$ ~ $A_2$ 이 된다.

단조 큐가 비어있지 않으므로 단조 큐의 맨 앞 원소가 구간을 벗어났는지 검사한다. 현재 벗어나지 않았다. 단조 큐가 비어있지 않으므로 단조 큐의 맨 뒤 원소부터 현재 값보다 작거나 같으면 단조 큐에서 제거하자. 현재 인덱스 $0$ 의 값인 $1$ 이 더 작으므로 제거하지 않고 이후 새로 추가된 인덱스를 삽입한다. 단조 큐의 맨 앞 원소를 통해 얻은 인덱스로 수열에서 조회하면 구간 $A_1$ ~ $A_2$ 의 최솟값은 $1$ 이 된다.

<br>

수열

![](/assets/posts/sliding-window-maximum/photo04.drawio.svg)

단조 큐 (인덱스 $0$ 은 구간을 벗어나지 않음)

![](/assets/posts/sliding-window-maximum/photo05.drawio.svg)

단조 큐 (인덱스 $0$ 의 값 $1$ 이 인덱스 $1$ 의 값 $5$ 보다 작아서 삭제하지 않음)

![](/assets/posts/sliding-window-maximum/photo06.drawio.svg)

단조 큐 (인덱스 $1$ 삽입)

![](/assets/posts/sliding-window-maximum/photo07.drawio.svg)

<br>

$A_3$ 의 인덱스는 $2$, 값은 $2$ 이다. 구간은 $A_1$ ~ $A_3$ 이 된다.

단조 큐가 비어있지 않으므로 단조 큐의 맨 앞 원소가 구간을 벗어났는지 검사한다. 현재 벗어나지 않았다. 단조 큐가 비어있지 않으므로 단조 큐의 맨 뒤 원소부터 현재 값보다 작거나 같으면 단조 큐에서 제거하자. 현재 인덱스 $1$ 의 값인 $5$ 가 더 크므로 제거한다.(인덱스 $2$ 의 값 $2$ 가 인덱스 $1$ 의 값 $5$ 보다 작으므로 인덱스 $1$ 의 값 $5$ 는 더 이상 윈도우 내 최솟값이 될 수 없다.) 다음 원소인 $0$ 의 값은 $1$ 이며 이는 새로 추가하는 값보다 작으므로 삭제하지 않고 이후 새로 추가된 인덱스를 삽입한다. 단조 큐의 맨 앞 원소를 통해 얻은 인덱스로 수열에서 조회하면 구간 $A_1$ ~ $A_3$ 의 최솟값은 $1$ 이 된다.

<br>

수열

![](/assets/posts/sliding-window-maximum/photo08.drawio.svg)

단조 큐 (인덱스 $0$ 은 구간을 벗어나지 않음)

![](/assets/posts/sliding-window-maximum/photo09.drawio.svg)

단조 큐 (인덱스 $1$ 의 값 $5$ 가 인덱스 $2$ 의 값 $2$ 보다 크므로 삭제)

![](/assets/posts/sliding-window-maximum/photo10.drawio.svg)

단조 큐 (인덱스 $0$ 의 값 $1$ 이 인덱스 $2$ 의 값 $2$ 보다 작아서 삭제하지 않음)

![](/assets/posts/sliding-window-maximum/photo11.drawio.svg)

단조 큐 (인덱스 $2$ 삽입)

![](/assets/posts/sliding-window-maximum/photo12.drawio.svg)

<br>

$A_4$ 의 인덱스는 $3$, 값은 $3$ 이다. 구간은 $A_2$ ~ $A_4$ 가 된다.

단조 큐가 비어있지 않으므로 단조 큐의 맨 앞 원소가 구간을 벗어났는지 검사한다. 현재 벗어났으므로 단조 큐에서 제거한다. 단조 큐가 비어있지 않으므로 단조 큐의 맨 뒤 원소부터 현재 값보다 작거나 같으면 단조 큐에서 제거하자. 현재 인덱스 $2$ 의 값인 $2$ 가 더 작으므로 제거하지 않고 이후 새로 추가된 인덱스를 삽입한다. 단조 큐의 맨 앞 원소를 통해 얻은 인덱스로 수열에서 조회하면 구간 $A_2$ ~ $A_4$ 의 최솟값은 $2$ 가 된다.

<br>

수열

![](/assets/posts/sliding-window-maximum/photo13.drawio.svg)

단조 큐 (인덱스 $0$ 은 구간을 벗어났으므로 삭제)

![](/assets/posts/sliding-window-maximum/photo14.drawio.svg)

단조 큐 (인덱스 $2$ 의 값 $2$ 가 인덱스 $3$ 의 값 $3$ 보다 작아서 삭제하지 않음)

![](/assets/posts/sliding-window-maximum/photo15.drawio.svg)

단조 큐 (인덱스 $3$ 삽입)

![](/assets/posts/sliding-window-maximum/photo16.drawio.svg)

<br>

마찬가지로 $A_5$ 에 대해서는 아래와 같이 되고 구간은 $A_3$ ~ $A_5$ 의 최솟값은 $2$ 가 된다.

<br>

수열

![](/assets/posts/sliding-window-maximum/photo17.drawio.svg)

단조 큐 (인덱스 $4$ 삽입)

![](/assets/posts/sliding-window-maximum/photo18.drawio.svg)

<br>

$A_6$ 의 인덱스는 $5$, 값은 $2$ 이다. 구간은 $A_4$ ~ $A_6$ 이 된다.

단조 큐가 비어있지 않으므로 단조 큐의 맨 앞 원소가 구간을 벗어났는지 검사한다. 현재 벗어났으므로 단조 큐에서 제거한다. 단조 큐가 비어있지 않으므로 단조 큐의 맨 뒤 원소부터 현재 값보다 작거나 같으면 단조 큐에서 제거하자. 현재 인덱스 $2$ 의 값인 $2$ 가 더 작으므로 제거하지 않고 이후 새로 추가된 인덱스를 삽입한다. 단조 큐의 맨 앞 원소를 통해 얻은 인덱스로 수열에서 조회하면 구간 $A_2$ ~ $A_4$ 의 최솟값은 $2$ 가 된다.

<br>

수열

![](/assets/posts/sliding-window-maximum/photo19.drawio.svg)

단조 큐 (인덱스 $2$는 구간을 벗어났으므로 삭제)

![](/assets/posts/sliding-window-maximum/photo20.drawio.svg)

단조 큐 (인덱스 $4$ 의 값 $6$ 이 인덱스 $5$ 의 값 $2$ 보다 크므로 삭제)

![](/assets/posts/sliding-window-maximum/photo21.drawio.svg)

단조 큐 (인덱스 $3$ 의 값 $3$ 이 인덱스 $5$ 의 값 $2$ 보다 크므로 삭제)

![](/assets/posts/sliding-window-maximum/photo22.drawio.svg)

단조 큐 (인덱스 $5$ 삽입)

![](/assets/posts/sliding-window-maximum/photo23.drawio.svg)

<br>

이러한 삽입, 삭제, 조회를 반복하면 수열을 한번만 순회하며 각 구간의 최솟값을 모두 구할 수 있다.

---

## 6. Problems

- [BaekJoon 11003번 - 최솟값 찾기](https://www.acmicpc.net/problem/11003)
- [BaekJoon 2433번 - The Sound of Silence](https://www.acmicpc.net/problem/2433)

---

## Ref

- [IOI KOREA - Deque을 이용한 구간 쿼리 구하기](https://www.youtube.com/watch?v=eBAbXG4bmvk)
- [GeeksforGeeks - Sliding Window Maximum](https://www.geeksforgeeks.org/dsa/sliding-window-maximum-maximum-of-all-subarrays-of-size-k/)

---
