---
title: "[자료구조/알고리즘] 병합 정렬 (Merge Sort)"
slug: merge-sort
date: 2025-11-18
categories: [DSA]
tags: [Sorting, Divide and Conquer]
toc: true
math: true
image: /assets/posts/merge-sort/thumbnail.drawio.svg
---

## 1. 병합 정렬

<br>

**병합 정렬(Merge Sort)**은 정렬 알고리즘 중 하나로 **분할 정복을 통해 정렬**하는 알고리즘이다. 병합 정렬 또는 합병 정렬이라고 불린다.

---

## 2. 병합 정렬 성능

<br>

| 평균 시간복잡도 | $O(N\log{N})$ |
| --------------- | ------------- |
| 최선 시간복잡도 | $O(N\log{N})$ |
| 최악 시간복잡도 | $O(N\log{N})$ |
| 공간복잡도      | $O(N)$        |

<br>

$N$ 개의 원소에 대한 병합 정렬은 최선, 평균, 최악 시간복잡도 모두 $O(N\log{N})$ 으로 일관된 성능을 보여준다. 이 때문에 거의 정렬된 상태로 원소들이 주어져도 성능이 더 빨라지지 않지만 **최소한의 성능은 보장**한다는 장점이 있다.

병합 정렬은 주어진 원소들을 분할 후 정복(병합)하는 과정에서 임시 공간을 사용하며 이는 병합하는 두 원소들의 크기만큼이 된다. 최종 병합 과정에서는 전체 원소 크기만큼의 임시 공간이 필요하게 되고 이 때문에 병합 정렬의 공간복잡도는 $O(N)$ 이다.

병합 정렬은 병합 과정에서 동일한 가중치의 수에 대해 먼저 등장한 수를 먼저 병합할 수 있어 순서가 유지되는 **안정 정렬(Stable Sort)**이다.

---

## 3. 병합 정렬 진행 과정

<br>

병합 정렬은 주어진 원소들을 두 구간으로 분할하는 과정을 더 이상 분할할 수 없을 때까지 반복한 후 이를 임시 공간에 정렬하고 원본에 반영하는 방식으로 동작한다. 반복문을 통한 Bottom-Up 방식의 병합 정렬도 가능하지만 재귀를 통한 Top-Down 방식의 병합 정렬이 보다 일반적이라 재귀를 통한 병합 정렬로 진행하겠다.

<br>

주어진 수들이 $[4, 1, 8, 3, 6, 10, 8, 4]$ 일 경우 오름차순 병합 정렬 과정은 아래와 같이 진행된다.

![](/assets/posts/merge-sort/photo01.drawio.svg)

<br>

먼저 주어진 원소들을 두 부분으로 분할한다. 분할은 중간 위치를 기준으로 분할하며 주어진 원소가 하나일 때까지 반복한다. 현재 1번부터 4번까지가 분할한 앞 부분이 된다.

![](/assets/posts/merge-sort/photo02.drawio.svg)

<br>

아직 분할할 수 있으므로 두 부분으로 분할한다. 현재 1번부터 2번까지가 분할한 앞 부분이 된다.

![](/assets/posts/merge-sort/photo03.drawio.svg)

<br>

아직 분할할 수 있으므로 두 부분으로 분할한다. 현재 1번부터 1번까지가 분할한 앞 부분이 된다.

![](/assets/posts/merge-sort/photo04.drawio.svg)

<br>

더 이상 분할할 수 없으므로 이전으로 돌아가 이전에 분할했던 뒷 부분에 대해 똑같이 시도한다.

![](/assets/posts/merge-sort/photo05.drawio.svg)

<br>

1번부터 2번 구간에 대한 분할이 끝났으므로 병합한다. 병합은 2칸짜리 임시 공간을 만들고 병합할 앞 부분과 뒷 부분의 첫 번째 원소부터 작은 것들을 순서대로 넣어준다.

![](/assets/posts/merge-sort/photo06.drawio.svg)

<br>

1번부터 4번 구간에 대한 앞 부분의 병합이 완료됐다. 이제 뒷 부분에 대해 분할을 시작한다.

![](/assets/posts/merge-sort/photo07.drawio.svg)

<br>

더 이상 분할할 수 없을 때까지 분할한다.

![](/assets/posts/merge-sort/photo08.drawio.svg)

<br>

더 이상 분할할 수 없을 때까지 분할한다.

![](/assets/posts/merge-sort/photo09.drawio.svg)

<br>

3번부터 4번 구간에 대한 분할이 끝났으므로 병합한다. 병합은 2칸짜리 임시 공간을 만들고 병합할 앞 부분과 뒷 부분의 첫 번째 원소부터 작은 것들을 순서대로 넣어준다.

![](/assets/posts/merge-sort/photo10.drawio.svg)

<br>

1번부터 4번 구간에 대해 앞 부분의 병합과 뒷 부분의 병합이 각각 완료됐다. 이제 앞 부분과 뒷 부분도 병합해준다.

![](/assets/posts/merge-sort/photo11.drawio.svg)

<br>

1번부터 8번 구간에 대해 앞 부분의 병합이 완료됐다. 이제 5번부터 8번 구간에 대해 똑같이 진행한다.

![](/assets/posts/merge-sort/photo12.drawio.svg)

<br>

5번부터 6번 구간으로 분할해준다.

![](/assets/posts/merge-sort/photo13.drawio.svg)

<br>

5번부터 5번 구간으로 분할해준다. 더 이상 분할할 수 없으므로 종료한다.

![](/assets/posts/merge-sort/photo14.drawio.svg)

<br>

6번부터 6번 구간으로 분할해준다. 더 이상 분할할 수 없으므로 종료한다.

![](/assets/posts/merge-sort/photo15.drawio.svg)

<br>

5번부터 6번 구간에 대한 분할이 끝났으므로 병합해준다.

![](/assets/posts/merge-sort/photo16.drawio.svg)

<br>

5번부터 8번 구간의 뒷 부분에 대해 분할을 시작한다.

![](/assets/posts/merge-sort/photo17.drawio.svg)

<br>

7번부터 7번 구간으로 분할해준다. 더 이상 분할할 수 없으므로 종료한다.

![](/assets/posts/merge-sort/photo18.drawio.svg)

<br>

8번부터 8번 구간으로 분할해준다. 더 이상 분할할 수 없으므로 종료한다.

![](/assets/posts/merge-sort/photo19.drawio.svg)

<br>

7번부터 8번 구간에 대한 분할이 끝났으므로 병합해준다.

![](/assets/posts/merge-sort/photo20.drawio.svg)

<br>

5번부터 8번 구간에 대한 앞 부분 병합과 뒷 부분 병합이 각각 완료됐다. 이제 앞 부분과 뒷 부분을 병합해준다.

![](/assets/posts/merge-sort/photo21.drawio.svg)

<br>

1번부터 8번 구간에 대한 앞 부분 병합과 뒷 부분 병합이 각각 완료됐다. 이제 앞 부분과 뒷 부분을 병합해준다. 이때 전체 구간의 길이만큼의 임시 배열이 필요해서 병합 정렬의 공간 복잡도는 $O(N)$ 이 되며 각 구간에서 동일한 가중치를 갖는 $4$, $8$ 에 대해 앞 구간의 원소를 먼저 병합하면 돼서 병합 정렬은 안정 정렬이다. 또한 분할이 $\log{N}$ 번 깊이로 발생하며 각 단계에서 $N$ 번의 병합이 이루어지므로 병합 정렬의 시간복잡도는 $O(N\log{N})$ 이다.

![](/assets/posts/merge-sort/photo22.drawio.svg)

<br>

전체 구간에 대한 병합을 완료했으므로 병합 정렬을 종료한다. 이렇게 병합 정렬을 통해 주어진 수들을 오름차순으로 정렬하는데 성공했다.

![](/assets/posts/merge-sort/photo23.drawio.svg)

---

## 4. 병합 정렬 코드

<br>

### 1. 병합 정렬 [Java]

```java
static void mergeSort(int[] arr) {
    int[] tmp = new int[arr.length];
    mergeSort(arr, tmp, 0, arr.length - 1);
}

static void mergeSort(int[] arr, int[] tmp, int left, int right) {
    if (left >= right) return;  // 더 이상 분할할 수 없으면 분할 종료

    int mid = (left + right) / 2;  // 분할점 선정

    mergeSort(arr, tmp, left, mid);  // 앞 부분 재귀적으로 분할
    mergeSort(arr, tmp, mid + 1, right);  // 뒷 부분 재귀적으로 분할
    merge(arr, tmp, left, mid, right);  // 병합
}

static void merge(int[] arr, int[] tmp, int left, int mid, int right) {
    int i = left;  // 앞 부분의 포인터
    int j = mid + 1;  // 뒷 부분의 포인터
    int k = left;  // 임시 공간의 포인터

    while (i <= mid && j <= right) {
        // 앞 부분의 포인터가 가리키는 원소가 뒷 부분의 포인터가 가리키는 원소보다 작거나 같으면 임시 공간에 넣고 포인터 이동
        // 이때 같아도 앞 부분의 원소를 먼저 넣어서 안정 정렬이 됨
        if (arr[i] <= arr[j]) {
            tmp[k++] = arr[i++];
        }
        // 뒷 부분의 포인터가 가리키는 원소가 앞 부분의 포인터가 가리키는 원소보다 작으면 임시 공간에 넣고 포인터 이동
        else {
            tmp[k++] = arr[j++];
        }
    }

    // 앞 부분의 남은 자투리 넣기
    while (i <= mid) {
        tmp[k++] = arr[i++];
    }

    // 뒷 부분의 남은 자투리 넣기
    while (j <= right) {
        tmp[k++] = arr[j++];
    }

    // 병합 정렬 결과 원본에 반영
    System.arraycopy(tmp, left, arr, left, right - left + 1);
}
```

<br>

### 2. 병합 정렬 [C++]

```c++
void merge(vector<int>& a, vector<int>& tmp, int l, int m, int r) {
    int i = l;      // 앞 부분의 포인터
    int j = m + 1;  // 뒷 부분의 포인터
    int k = l;      // 임시 공간의 포인터

    while (i <= m && j <= r) {
        // 앞 부분의 포인터가 가리키는 원소가 뒷 부분의 포인터가 가리키는 원소보다 작거나 같으면 임시 공간에 넣고 포인터
        // 이동 이때 같아도 앞 부분의 원소를 먼저 넣어서 안정 정렬이 됨
        if (a[i] <= a[j]) {
            tmp[k++] = a[i++];
        }
        // 뒷 부분의 포인터가 가리키는 원소가 앞 부분의 포인터가 가리키는 원소보다 작으면 임시 공간에 넣고 포인터 이동
        else {
            tmp[k++] = a[j++];
        }
    }

    while (i <= m) tmp[k++] = a[i++];  // 앞 부분의 남은 자투리 넣기
    while (j <= r) tmp[k++] = a[j++];  // 뒷 부분의 남은 자투리 넣기

    for (int idx = l; idx <= r; idx++) a[idx] = tmp[idx];  // 병합 정렬 결과 원본에 반영
}

void mergeSort(vector<int>& a, vector<int>& tmp, int l, int r) {
    if (l >= r) return;  // 더 이상 분할할 수 없으면 분할 종료

    int m = (l + r) / 2;  // 분할점 선정

    mergeSort(a, tmp, l, m);      // 앞 부분 재귀적으로 분할
    mergeSort(a, tmp, m + 1, r);  // 뒷 부분 재귀적으로 분할
    merge(a, tmp, l, m, r);       // 병합
}

void mergeSort(vector<int>& a) {
    vector<int> tmp(a.size());
    mergeSort(a, tmp, 0, a.size() - 1);
}
```

---

## Ref

<br>

- [wikipedia - 병합 정렬](https://ko.wikipedia.org/wiki/%ED%95%A9%EB%B3%91_%EC%A0%95%EB%A0%AC)

---
