---
title: "[알고리즘] 선택 정렬 (Selection Sort)"
date: 2025-11-17
categories: [Algorithm, Sort]
tags: [정렬]
toc: true
math: true
image: /assets/posts/2025-11/선택%20정렬%20(Selection%20Sort)/thumbnail.drawio.svg
---

## 선택 정렬

선택 정렬은 정렬 알고리즘 중 하나로 정렬되지 않은 부분에서 최솟값이나 최댓값을 찾아서 정렬되지 않은 첫 원소와 자리를 교환하는 방식으로 정렬하는 알고리즘이다. 원리가 간단하기 때문에 한 번쯤 배워볼 만하다.

---

## 선택 정렬 성능

| 평균 시간복잡도 | $O(N^2)$ |
| --------------- | -------- |
| 최선 시간복잡도 | $O(N^2)$ |
| 최악 시간복잡도 | $O(N^2)$ |
| 공간복잡도      | $O(1)$   |

$N$개의 원소에 대한 선택 정렬은 기본적으로 2중 반복문을 통해 정렬을 수행하여 시간복잡도가 $O(N^2)$이다. 하지만 버블 정렬은 교환 횟수도 최대 $O(N^2)$인데 비해 선택 정렬은 교환 횟수가 최대 $O(N)$이다.

선택 정렬은 제자리 정렬이기 때문에 스왑을 위한 변수 하나의 공간만 필요하여 공간복잡도는 $O(1)$이다.

선택 정렬은 두 수의 교환 과정에서 동일한 가중치의 두 수에 대해 정렬 후에 기존 순서가 보장되지 않는 불안정 정렬이다.

---

## 선택 정렬 진행 과정

선택 정렬은 정렬되지 않은 부분에서 최솟값이나 최댓값을 찾아서 정렬되지 않은 첫 원소와 자리를 교환하는 방식으로 진행된다.

주어진 수들이 $[4, 1, 8, 3, 6, 10, 8, 4]$일 경우 오름차순 선택 정렬 과정은 아래와 같이 진행된다.

![](</assets/posts/2025-11/선택%20정렬%20(Selection%20Sort)/photo01.drawio.svg>)

초록색으로 칠한 칸은 정렬되지 않는 부분이다.

![](</assets/posts/2025-11/선택%20정렬%20(Selection%20Sort)/photo02.drawio.svg>)

파란색으로 칠한 칸은 정렬되지 않은 부분의 최솟값이다.

![](</assets/posts/2025-11/선택%20정렬%20(Selection%20Sort)/photo03.drawio.svg>)

정렬되지 않은 부분의 첫 원소는 $4$다.

![](</assets/posts/2025-11/선택%20정렬%20(Selection%20Sort)/photo04.drawio.svg>)

두 수를 교환한다.

![](</assets/posts/2025-11/선택%20정렬%20(Selection%20Sort)/photo05.drawio.svg>)

가장 작은 원소를 정렬하는데 성공했다.

![](</assets/posts/2025-11/선택%20정렬%20(Selection%20Sort)/photo06.drawio.svg>)

초록색으로 칠한 칸은 정렬되지 않는 부분이다.

![](</assets/posts/2025-11/선택%20정렬%20(Selection%20Sort)/photo07.drawio.svg>)

파란색으로 칠한 칸은 정렬되지 않은 부분의 최솟값이다.

![](</assets/posts/2025-11/선택%20정렬%20(Selection%20Sort)/photo08.drawio.svg>)

정렬되지 않은 부분의 첫 원소는 $4$다.

![](</assets/posts/2025-11/선택%20정렬%20(Selection%20Sort)/photo09.drawio.svg>)

두 수를 교환한다.

![](</assets/posts/2025-11/선택%20정렬%20(Selection%20Sort)/photo10.drawio.svg>)

두 번째로 작은 원소를 정렬하는데 성공했다.

![](</assets/posts/2025-11/선택%20정렬%20(Selection%20Sort)/photo11.drawio.svg>)

초록색으로 칠한 칸은 정렬되지 않는 부분이다.

![](</assets/posts/2025-11/선택%20정렬%20(Selection%20Sort)/photo12.drawio.svg>)

파란색으로 칠한 칸은 정렬되지 않은 부분의 최솟값이다. 뒤에도 $4$가 존재하는데 어떤걸 선택하든 상관없다.

![](</assets/posts/2025-11/선택%20정렬%20(Selection%20Sort)/photo13.drawio.svg>)

정렬되지 않은 부분의 첫 원소는 $8$이다.

![](</assets/posts/2025-11/선택%20정렬%20(Selection%20Sort)/photo14.drawio.svg>)

두 수를 교환한다.

![](</assets/posts/2025-11/선택%20정렬%20(Selection%20Sort)/photo15.drawio.svg>)

세 번째로 작은 원소를 정렬하는데 성공했다.

![](</assets/posts/2025-11/선택%20정렬%20(Selection%20Sort)/photo16.drawio.svg>)

초록색으로 칠한 칸은 정렬되지 않는 부분이다.

![](</assets/posts/2025-11/선택%20정렬%20(Selection%20Sort)/photo17.drawio.svg>)

파란색으로 칠한 칸은 정렬되지 않은 부분의 최솟값이다.

![](</assets/posts/2025-11/선택%20정렬%20(Selection%20Sort)/photo18.drawio.svg>)

정렬되지 않은 부분의 첫 원소는 $8$이다.

![](</assets/posts/2025-11/선택%20정렬%20(Selection%20Sort)/photo19.drawio.svg>)

두 수를 교환한다. 두 수의 교환 과정에서 3번의 $8$이 7번의 $8$보다 뒤에 위치하게 됐다. 이런 메커니즘 때문에 선택 정렬은 불안정 정렬이다.

![](</assets/posts/2025-11/선택%20정렬%20(Selection%20Sort)/photo20.drawio.svg>)

네 번째로 작은 원소를 정렬하는데 성공했다.

![](</assets/posts/2025-11/선택%20정렬%20(Selection%20Sort)/photo21.drawio.svg>)

초록색으로 칠한 칸은 정렬되지 않는 부분이다.

![](</assets/posts/2025-11/선택%20정렬%20(Selection%20Sort)/photo22.drawio.svg>)

파란색으로 칠한 칸은 정렬되지 않은 부분의 최솟값이다.

![](</assets/posts/2025-11/선택%20정렬%20(Selection%20Sort)/photo23.drawio.svg>)

정렬되지 않은 부분의 첫 원소는 $6$이다.

![](</assets/posts/2025-11/선택%20정렬%20(Selection%20Sort)/photo24.drawio.svg>)

두 수를 교환한다. 정렬되지 않은 부분의 최솟값이 위치한 곳이 정렬되지 않은 부분의 첫 원소와 일치해서 자신과 자신을 교환한 꼴이다.

![](</assets/posts/2025-11/선택%20정렬%20(Selection%20Sort)/photo25.drawio.svg>)

다섯 번째로 작은 원소를 정렬하는데 성공했다.

![](</assets/posts/2025-11/선택%20정렬%20(Selection%20Sort)/photo26.drawio.svg>)

초록색으로 칠한 칸은 정렬되지 않는 부분이다.

![](</assets/posts/2025-11/선택%20정렬%20(Selection%20Sort)/photo27.drawio.svg>)

파란색으로 칠한 칸은 정렬되지 않은 부분의 최솟값이다.

![](</assets/posts/2025-11/선택%20정렬%20(Selection%20Sort)/photo28.drawio.svg>)

정렬되지 않은 부분의 첫 원소는 $10$이다.

![](</assets/posts/2025-11/선택%20정렬%20(Selection%20Sort)/photo29.drawio.svg>)

두 수를 교환한다.

![](</assets/posts/2025-11/선택%20정렬%20(Selection%20Sort)/photo30.drawio.svg>)

여섯 번째로 작은 원소를 정렬하는데 성공했다.

![](</assets/posts/2025-11/선택%20정렬%20(Selection%20Sort)/photo31.drawio.svg>)

초록색으로 칠한 칸은 정렬되지 않는 부분이다.

![](</assets/posts/2025-11/선택%20정렬%20(Selection%20Sort)/photo32.drawio.svg>)

파란색으로 칠한 칸은 정렬되지 않은 부분의 최솟값이다.

![](</assets/posts/2025-11/선택%20정렬%20(Selection%20Sort)/photo33.drawio.svg>)

정렬되지 않은 부분의 첫 원소는 $10$이다.

![](</assets/posts/2025-11/선택%20정렬%20(Selection%20Sort)/photo34.drawio.svg>)

두 수를 교환한다.

![](</assets/posts/2025-11/선택%20정렬%20(Selection%20Sort)/photo35.drawio.svg>)

일곱 번째로 작은 원소를 정렬하는데 성공했다.

![](</assets/posts/2025-11/선택%20정렬%20(Selection%20Sort)/photo36.drawio.svg>)

$N$개의 수 중에서 $N-1$개를 정렬했다. 남은 수는 주어진 수 중에서 가장 큰 수면서 이미 가장 뒤에 위치하게 되므로 선택 정렬을 종료한다. 이렇게 선택 정렬을 통해 주어진 수들을 오름차순으로 정렬하는데 성공했다.

![](</assets/posts/2025-11/선택%20정렬%20(Selection%20Sort)/photo37.drawio.svg>)

---

## 선택 정렬 코드

### 선택 정렬 [Java]

$100,000$개의 임의의 수들에 대한 정렬에서 약 2.8초정도 소요됐다.(Macbook M3 Air, JDK 21)

버블 정렬과 동일한 시간복잡도지만 두 배 가량 빠른 것을 볼 수 있었다.

```java
public static void selectionSort(int[] arr) {
    int N = arr.length;

    for (int i = 0; i < N - 1; i++) {  // N-1개만 정렬하면 됨
        int minIdx = i;  // 최솟값의 인덱스

        for (int j = i; j < N; j++) {  // 정렬이 안된 구간만 탐색
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

---

## Ref

- [wikipedia - 선택 정렬](https://ko.wikipedia.org/wiki/%EC%84%A0%ED%83%9D_%EC%A0%95%EB%A0%AC)

---
