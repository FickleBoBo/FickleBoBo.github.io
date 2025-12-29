---
title: "[자료구조/알고리즘] 선택 정렬 (Selection Sort)"
slug: selection-sort
date: 2025-11-17
categories: [DSA]
tags: [Sorting]
toc: true
math: true
image: /assets/posts/selection-sort/thumbnail.drawio.svg
---

## 1. 선택 정렬

선택 정렬은 정렬 알고리즘 중 하나로 정렬되지 않은 부분에서 최솟값이나 최댓값을 찾아서 정렬되지 않은 첫 원소와 자리를 교환하는 방식으로 정렬하는 알고리즘이다. 원리가 간단하기 때문에 한 번쯤 배워볼 만하다.

---

## 2. 선택 정렬 성능

| 평균 시간복잡도 | $O(N^2)$ |
| --------------- | -------- |
| 최선 시간복잡도 | $O(N^2)$ |
| 최악 시간복잡도 | $O(N^2)$ |
| 공간복잡도      | $O(1)$   |

<br>

$N$ 개의 원소에 대한 선택 정렬은 기본적으로 2중 반복문을 통해 정렬을 수행하여 시간복잡도가 $O(N^2)$ 이다. 하지만 버블 정렬은 교환 횟수도 최대 $O(N^2)$ 인데 비해 선택 정렬은 교환 횟수가 최대 $O(N)$ 이다.

선택 정렬은 제자리 정렬(In-place Sort)이기 때문에 스왑을 위한 변수 하나의 공간만 필요하여 공간복잡도는 $O(1)$ 이다.

선택 정렬은 두 수의 교환 과정에서 동일한 가중치의 두 수에 대해 정렬 후에 기존 순서가 보장되지 않는 불안정 정렬(Unstable Sort)이다.

---

## 3. 선택 정렬 진행 과정

선택 정렬은 정렬되지 않은 부분에서 최솟값이나 최댓값을 찾아서 정렬되지 않은 첫 원소와 자리를 교환하는 방식으로 진행된다.

<br>

주어진 수들이 $[4, 1, 8, 3, 6, 10, 8, 4]$ 일 경우 오름차순 선택 정렬 과정은 아래와 같이 진행된다.

![](/assets/posts/selection-sort/photo01.drawio.svg)

<br>

초록색으로 칠한 칸은 정렬되지 않는 부분이다.

![](/assets/posts/selection-sort/photo02.drawio.svg)

<br>

파란색으로 칠한 칸은 정렬되지 않은 부분의 최솟값이다.

![](/assets/posts/selection-sort/photo03.drawio.svg)

<br>

정렬되지 않은 부분의 첫 원소는 $4$ 다.

![](/assets/posts/selection-sort/photo04.drawio.svg)

<br>

두 수를 교환한다.

![](/assets/posts/selection-sort/photo05.drawio.svg)

<br>

가장 작은 원소를 정렬하는데 성공했다.

![](/assets/posts/selection-sort/photo06.drawio.svg)

<br>

초록색으로 칠한 칸은 정렬되지 않는 부분이다.

![](/assets/posts/selection-sort/photo07.drawio.svg)

<br>

파란색으로 칠한 칸은 정렬되지 않은 부분의 최솟값이다.

![](/assets/posts/selection-sort/photo08.drawio.svg)

<br>

정렬되지 않은 부분의 첫 원소는 $4$ 다.

![](/assets/posts/selection-sort/photo09.drawio.svg)

<br>

두 수를 교환한다.

![](/assets/posts/selection-sort/photo10.drawio.svg)

<br>

두 번째로 작은 원소를 정렬하는데 성공했다.

![](/assets/posts/selection-sort/photo11.drawio.svg)

<br>

초록색으로 칠한 칸은 정렬되지 않는 부분이다.

![](/assets/posts/selection-sort/photo12.drawio.svg)

<br>

파란색으로 칠한 칸은 정렬되지 않은 부분의 최솟값이다. 뒤에도 $4$ 가 존재하는데 어떤걸 선택하든 상관없다.

![](/assets/posts/selection-sort/photo13.drawio.svg)

<br>

정렬되지 않은 부분의 첫 원소는 $8$ 이다.

![](/assets/posts/selection-sort/photo14.drawio.svg)

<br>

두 수를 교환한다.

![](/assets/posts/selection-sort/photo15.drawio.svg)

<br>

세 번째로 작은 원소를 정렬하는데 성공했다.

![](/assets/posts/selection-sort/photo16.drawio.svg)

<br>

초록색으로 칠한 칸은 정렬되지 않는 부분이다.

![](/assets/posts/selection-sort/photo17.drawio.svg)

<br>

파란색으로 칠한 칸은 정렬되지 않은 부분의 최솟값이다.

![](/assets/posts/selection-sort/photo18.drawio.svg)

<br>

정렬되지 않은 부분의 첫 원소는 $8$ 이다.

![](/assets/posts/selection-sort/photo19.drawio.svg)

<br>

두 수를 교환한다. 두 수의 교환 과정에서 3번의 $8$ 이 7번의 $8$ 보다 뒤에 위치하게 됐다. 이런 메커니즘 때문에 선택 정렬은 불안정 정렬이다.

![](/assets/posts/selection-sort/photo20.drawio.svg)

<br>

네 번째로 작은 원소를 정렬하는데 성공했다.

![](/assets/posts/selection-sort/photo21.drawio.svg)

<br>

초록색으로 칠한 칸은 정렬되지 않는 부분이다.

![](/assets/posts/selection-sort/photo22.drawio.svg)

<br>

파란색으로 칠한 칸은 정렬되지 않은 부분의 최솟값이다.

![](/assets/posts/selection-sort/photo23.drawio.svg)

<br>

정렬되지 않은 부분의 첫 원소는 $6$ 이다.

![](/assets/posts/selection-sort/photo24.drawio.svg)

<br>

두 수를 교환한다. 정렬되지 않은 부분의 최솟값이 위치한 곳이 정렬되지 않은 부분의 첫 원소와 일치해서 자신과 자신을 교환한 꼴이다.

![](/assets/posts/selection-sort/photo25.drawio.svg)

<br>

다섯 번째로 작은 원소를 정렬하는데 성공했다.

![](/assets/posts/selection-sort/photo26.drawio.svg)

<br>

초록색으로 칠한 칸은 정렬되지 않는 부분이다.

![](/assets/posts/selection-sort/photo27.drawio.svg)

<br>

파란색으로 칠한 칸은 정렬되지 않은 부분의 최솟값이다.

![](/assets/posts/selection-sort/photo28.drawio.svg)

<br>

정렬되지 않은 부분의 첫 원소는 $10$ 이다.

![](/assets/posts/selection-sort/photo29.drawio.svg)

<br>

두 수를 교환한다.

![](/assets/posts/selection-sort/photo30.drawio.svg)

<br>

여섯 번째로 작은 원소를 정렬하는데 성공했다.

![](/assets/posts/selection-sort/photo31.drawio.svg)

<br>

초록색으로 칠한 칸은 정렬되지 않는 부분이다.

![](/assets/posts/selection-sort/photo32.drawio.svg)

<br>

파란색으로 칠한 칸은 정렬되지 않은 부분의 최솟값이다.

![](/assets/posts/selection-sort/photo33.drawio.svg)

<br>

정렬되지 않은 부분의 첫 원소는 $10$ 이다.

![](/assets/posts/selection-sort/photo34.drawio.svg)

<br>

두 수를 교환한다.

![](/assets/posts/selection-sort/photo35.drawio.svg)

<br>

일곱 번째로 작은 원소를 정렬하는데 성공했다.

![](/assets/posts/selection-sort/photo36.drawio.svg)

<br>

$N$ 개의 수 중에서 $N-1$ 개를 정렬했다. 남은 수는 주어진 수 중에서 가장 큰 수면서 이미 가장 뒤에 위치하게 되므로 선택 정렬을 종료한다. 이렇게 선택 정렬을 통해 주어진 수들을 오름차순으로 정렬하는데 성공했다.

![](/assets/posts/selection-sort/photo37.drawio.svg)

---

## 4. 선택 정렬 코드

### 1. 선택 정렬 [Java]

```java
static void selectionSort(int[] arr) {
    int N = arr.length;

    for (int i = 0; i < N - 1; i++) {  // N-1개만 정렬하면 됨
        int minIdx = i;  // 최솟값의 인덱스

        for (int j = i + 1; j < N; j++) {  // 정렬이 안된 구간만 탐색
            if (arr[j] < arr[minIdx]) {
                minIdx = j;
            }
        }

        // swap
        int tmp = arr[i];
        arr[i] = arr[minIdx];
        arr[minIdx] = tmp;
    }
}
```

### 2. 선택 정렬 [C++]

```c++
void selectionSort(vector<int>& v) {
    int n = v.size();

    for (int i = 0; i < n - 1; i++) {  // n-1개만 정렬하면 됨
        int mn = i;                    // 최솟값의 인덱스

        for (int j = i + 1; j < n; j++) {  // 정렬이 안된 구간만 탐색
            if (v[j] < v[mn]) {
                mn = j;
            }
        }

        swap(v[i], v[mn]);
    }
}
```

---

## Ref

- [wikipedia - 선택 정렬](https://ko.wikipedia.org/wiki/%EC%84%A0%ED%83%9D_%EC%A0%95%EB%A0%AC)

---
