---
title: "[자료구조/알고리즘] 버블 정렬 (Bubble Sort)"
slug: bubble-sort
date: 2025-11-17
categories: [DSA]
tags: [Sorting]
toc: true
math: true
image: /assets/posts/bubble-sort/thumbnail.drawio.svg
---

## 1. 버블 정렬

<br>

버블 정렬은 정렬 알고리즘 중 하나로 원소의 이동이 거품이 수면으로 올라오는 듯한 모습으로 보이기 때문에 지어진 이름이다. 코드가 단순하기 때문에 간단한 정렬 알고리즘으로 한 번쯤 배워볼 만하다.

---

## 2. 버블 정렬 성능

<br>

| 평균 시간복잡도 | $O(N^2)$         |
| --------------- | ---------------- |
| 최선 시간복잡도 | $O(N^2)$, $O(N)$ |
| 최악 시간복잡도 | $O(N^2)$         |
| 공간복잡도      | $O(1)$           |

<br>

$N$ 개의 원소에 대한 버블 정렬은 기본적으로 2중 반복문을 통해 정렬을 수행하여 시간복잡도가 $O(N^2)$ 이다. 원소들이 처음부터 정렬되어 있을 경우 비교 작업을 수행하지 않도록 최적화하면 최선 시간복잡도는 $O(N)$ 까지도 가능하다. 오름차순으로 정렬하고자 할 때 원소들이 역순으로 주어지면 비교마다 교환이 계속 반복돼서 최악으로 동작한다.

버블 정렬은 제자리 정렬(In-place Sort)이기 때문에 스왑을 위한 변수 하나의 공간만 필요하여 공간복잡도는 $O(1)$ 이다.

버블 정렬은 동일한 가중치의 두 수에 대해 정렬 후에도 기존 순서를 보장하는 안정 정렬(Stable Sort)이다.

---

## 3. 버블 정렬 진행 과정

<br>

버블 정렬은 기본적으로 두 수($a$, $b$)를 선택한 뒤, 만약 그 두 수가 정렬되었다면 놔두고 아니라면 두 수를 바꾸는 방식으로 진행된다. 오름차순으로 정렬할 때는 $a < b$, 내림차순이라면 $a > b$ 여야 정렬된 것으로 판단한다. 이를 주어진 수에 대해 반복한다.

<br>

주어진 수들이 $[4, 1, 8, 3, 6, 10, 8, 4]$ 일 경우 오름차순 버블 정렬 과정은 아래와 같이 진행된다.

![](/assets/posts/bubble-sort/photo01.drawio.svg)

<br>

먼저 처음 두 수가 오름차순인지 비교한다.

![](/assets/posts/bubble-sort/photo02.drawio.svg)

<br>

오름차순이 아니므로 두 수를 바꾼다.

![](/assets/posts/bubble-sort/photo03.drawio.svg)

<br>

한 칸 이동한 뒤 다시 두 수가 오름차순인지 비교한다.

![](/assets/posts/bubble-sort/photo04.drawio.svg)

<br>

오름차순이므로 두 수를 바꾸지 않는다.

![](/assets/posts/bubble-sort/photo05.drawio.svg)

<br>

한 칸 이동한 뒤 다시 두 수가 오름차순인지 비교한다.

![](/assets/posts/bubble-sort/photo06.drawio.svg)

<br>

오름차순이 아니므로 두 수를 바꾼다.

![](/assets/posts/bubble-sort/photo07.drawio.svg)

<br>

한 칸 이동한 뒤 다시 두 수가 오름차순인지 비교한다.

![](/assets/posts/bubble-sort/photo08.drawio.svg)

<br>

오름차순이 아니므로 두 수를 바꾼다.

![](/assets/posts/bubble-sort/photo09.drawio.svg)

<br>

한 칸 이동한 뒤 다시 두 수가 오름차순인지 비교한다.

![](/assets/posts/bubble-sort/photo10.drawio.svg)

<br>

오름차순이므로 두 수를 바꾸지 않는다.

![](/assets/posts/bubble-sort/photo11.drawio.svg)

<br>

한 칸 이동한 뒤 다시 두 수가 오름차순인지 비교한다.

![](/assets/posts/bubble-sort/photo12.drawio.svg)

<br>

오름차순이 아니므로 두 수를 바꾼다.

![](/assets/posts/bubble-sort/photo13.drawio.svg)

<br>

한 칸 이동한 뒤 다시 두 수가 오름차순인지 비교한다.

![](/assets/posts/bubble-sort/photo14.drawio.svg)

<br>

오름차순이 아니므로 두 수를 바꾼다.

![](/assets/posts/bubble-sort/photo15.drawio.svg)

<br>

주어진 수의 끝에 도달했으며 교환 과정을 통해 주어진 수 중 가장 큰 수인 $10$ 이 끝에 위치하게 됐다. 하나의 수를 정렬하는데 성공했다.

![](/assets/posts/bubble-sort/photo16.drawio.svg)

<br>

다시 처음 두 수가 오름차순인지 비교한다.

![](/assets/posts/bubble-sort/photo17.drawio.svg)

<br>

오름차순이므로 두 수를 바꾸지 않는다.

![](/assets/posts/bubble-sort/photo18.drawio.svg)

<br>

한 칸 이동한 뒤 다시 두 수가 오름차순인지 비교한다.

![](/assets/posts/bubble-sort/photo19.drawio.svg)

<br>

오름차순이 아니므로 두 수를 바꾼다.

![](/assets/posts/bubble-sort/photo20.drawio.svg)

<br>

한 칸 이동한 뒤 다시 두 수가 오름차순인지 비교한다.

![](/assets/posts/bubble-sort/photo21.drawio.svg)

<br>

오름차순이므로 두 수를 바꾸지 않는다.

![](/assets/posts/bubble-sort/photo22.drawio.svg)

<br>

한 칸 이동한 뒤 다시 두 수가 오름차순인지 비교한다.

![](/assets/posts/bubble-sort/photo23.drawio.svg)

<br>

오름차순이므로 두 수를 바꾸지 않는다.

![](/assets/posts/bubble-sort/photo24.drawio.svg)

<br>

한 칸 이동한 뒤 다시 두 수가 오름차순인지 비교한다.

![](/assets/posts/bubble-sort/photo25.drawio.svg)

<br>

오름차순이므로 두 수를 바꾸지 않는다. 동일한 두 수에 대해 두 수를 바꾸지 않기 때문에 3번의 $8$ 이 7번의 $8$ 보다 항상 앞에 위치하게 되고 이를 통해 안정 정렬이 된다.

![](/assets/posts/bubble-sort/photo26.drawio.svg)

<br>

한 칸 이동한 뒤 다시 두 수가 오름차순인지 비교한다.

![](/assets/posts/bubble-sort/photo27.drawio.svg)

<br>

오름차순이 아니므로 두 수를 바꾼다.

![](/assets/posts/bubble-sort/photo28.drawio.svg)

<br>

주어진 수의 끝에는 이미 가장 큰 $10$ 이 있으므로 오름차순인지 더 비교하지 않아도 된다. $10$ 앞에 주어진 수 중 두 번째로 큰 수인 $8$ 이 위치하게 됐다. 두 개의 수 정렬하는데 성공했다.

![](/assets/posts/bubble-sort/photo29.drawio.svg)

<br>

다시 처음 두 수부터 다음 정렬은 아래와 같이 이어진다.

![](/assets/posts/bubble-sort/photo30.drawio.svg)

![](/assets/posts/bubble-sort/photo32.drawio.svg)

![](/assets/posts/bubble-sort/photo34.drawio.svg)

![](/assets/posts/bubble-sort/photo36.drawio.svg)

![](/assets/posts/bubble-sort/photo38.drawio.svg)

![](/assets/posts/bubble-sort/photo39.drawio.svg)

![](/assets/posts/bubble-sort/photo40.drawio.svg)

<br>

다시 처음 두 수부터 다음 정렬은 아래와 같이 이어진다.

![](/assets/posts/bubble-sort/photo41.drawio.svg)

![](/assets/posts/bubble-sort/photo43.drawio.svg)

![](/assets/posts/bubble-sort/photo45.drawio.svg)

![](/assets/posts/bubble-sort/photo47.drawio.svg)

![](/assets/posts/bubble-sort/photo48.drawio.svg)

![](/assets/posts/bubble-sort/photo49.drawio.svg)

<br>

다시 처음 두 수부터 다음 정렬은 아래와 같이 이어진다.

![](/assets/posts/bubble-sort/photo50.drawio.svg)

![](/assets/posts/bubble-sort/photo52.drawio.svg)

![](/assets/posts/bubble-sort/photo54.drawio.svg)

![](/assets/posts/bubble-sort/photo56.drawio.svg)

<br>

다시 처음 두 수부터 다음 정렬은 아래와 같이 이어진다.

![](/assets/posts/bubble-sort/photo57.drawio.svg)

![](/assets/posts/bubble-sort/photo59.drawio.svg)

![](/assets/posts/bubble-sort/photo61.drawio.svg)

<br>

다시 처음 두 수부터 다음 정렬은 아래와 같이 이어진다.

![](/assets/posts/bubble-sort/photo62.drawio.svg)

![](/assets/posts/bubble-sort/photo64.drawio.svg)

<br>

$N$ 개의 수 중에서 $N-1$ 개를 정렬했다. 남은 수는 주어진 수 중에서 가장 작은 수면서 이미 가장 앞에 위치하게 되므로 버블 정렬을 종료한다. 이렇게 버블 정렬을 통해 주어진 수들을 오름차순으로 정렬하는데 성공했다.

![](/assets/posts/bubble-sort/photo65.drawio.svg)

<br>

버블 정렬의 진행과정을 보면 버블 정렬은 정렬이 안된 구간 중 가장 큰 수를 찾아서 이동시키는 과정을 반복하는 것을 볼 수 있다.

---

## 4. 버블 정렬 코드

<br>

### 1. 버블 정렬 [Java]

```java
static void bubbleSort(int[] arr) {
    int N = arr.length;

    for (int i = 0; i < N - 1; i++) {  // N-1개만 정렬하면 됨
        for (int j = 0; j < N - 1 - i; j++) {  // 정렬이 안된 구간만 탐색
            if (arr[j] > arr[j + 1]) {

                // swap
                int tmp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = tmp;
            }
        }
    }
}
```

<br>

### 2. 스왑 체크로 최적화 [Java]

```java
static void optimizedBubbleSort(int[] arr) {
    int N = arr.length;

    for (int i = 0; i < N - 1; i++) {
        boolean swapped = false;  // 교환 여부

        for (int j = 0; j < N - 1 - i; j++) {
            if (arr[j] > arr[j + 1]) {

                // swap
                int tmp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = tmp;
                swapped = true;
            }
        }

        // 한번도 교환된 적이 없으면 남은 구간이 전부 정렬된 상태이므로 종료
        if (!swapped) {
            break;
        }
    }
}
```

<br>

### 3. 버블 정렬 [C++]

```c++
void bubbleSort(vector<int>& v) {
    int n = v.size();

    for (int i = 0; i < n - 1; i++) {          // n-1개만 정렬하면 됨
        for (int j = 0; j < n - 1 - i; j++) {  // 정렬이 안된 구간만 탐색
            if (v[j] > v[j + 1]) {
                swap(v[j], v[j + 1]);
            }
        }
    }
}
```

<br>

### 4. 스왑 체크로 최적화 [C++]

```c++
void optimizedBubbleSort(vector<int>& v) {
    int n = v.size();

    for (int i = 0; i < n - 1; i++) {
        bool swapped = false;  // 교환 여부

        for (int j = 0; j < n - 1 - i; j++) {
            if (v[j] > v[j + 1]) {
                swap(v[j], v[j + 1]);
                swapped = true;
            }
        }

        // 한번도 교환된 적이 없으면 남은 구간이 전부 정렬된 상태이므로 종료
        if (!swapped) break;
    }
}
```

---

## Ref

<br>

- [wikipedia - 버블 정렬](https://ko.wikipedia.org/wiki/%EB%B2%84%EB%B8%94_%EC%A0%95%EB%A0%AC)

---
