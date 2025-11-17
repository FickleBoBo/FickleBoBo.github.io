---
title: "[알고리즘] 삽입 정렬 (Insertion Sort)"
date: 2025-11-17
categories: [Algorithm, Sort]
tags: [정렬]
toc: true
math: true
image: /assets/posts/2025-11/삽입%20정렬%20(Insertion%20Sort)/thumbnail.drawio.svg
---

## 삽입 정렬

삽입 정렬은 정렬 알고리즘 중 하나로 정렬되지 않은 각 원소를 정렬된 부분의 적절한 위치에 삽입하는 방식으로 정렬하는 알고리즘이다. 원리가 간단하기 때문에 한 번쯤 배워볼 만하다.

---

## 삽입 정렬 성능

| 평균 시간복잡도 | $O(N^2)$ |
| --------------- | -------- |
| 최선 시간복잡도 | $O(N)$   |
| 최악 시간복잡도 | $O(N^2)$ |
| 공간복잡도      | $O(1)$   |

$N$개의 원소에 대한 삽입 정렬은 기본적으로 2중 반복문을 통해 정렬을 수행하여 시간복잡도가 $O(N^2)$이다. 버블 정렬이나 선택 정렬과 동일한 시간복잡도지만 일반적으로 더 빠르게 동작한다. 오름차순으로 정렬하고자 할 때 원소들이 역순으로 주어지면 삽입을 위한 원소 이동이 정렬된 모든 부분에서 반복돼서 최악으로 동작한다. 원소들이 정렬된 상태로 주어질 경우 각 원소당 한 번씩의 비교, 삽입만 발생해서 최선의 시간복잡도는 $O(N)$이다. 주어진 원소들이 거의 정렬된 상태일 경우 매우 효율적으로 동작한다.

삽입 정렬은 제자리 정렬(In-place Sort)이기 때문에 스왑을 위한 변수 하나의 공간만 필요하여 공간복잡도는 $O(1)$이다.

삽입 정렬은 삽입 과정에서 동일한 가중치의 수 뒤에 삽입을 하므로 순서가 유지되는 안정 정렬(Stable Sort)이다.

---

## 삽입 정렬 진행 과정

삽입 정렬은 정렬되지 않은 각 원소를 정렬된 부분의 적절한 위치에 삽입하는 방식으로 진행된다. 적절한 위치를 찾을 때까지 정렬된 원소를 뒤로 밀어서 공간을 확보한 후 적절한 위치에 삽입하면 된다.

주어진 수들이 $[4, 1, 8, 3, 6, 10, 8, 4]$일 경우 오름차순 삽입 정렬 과정은 아래와 같이 진행된다.

![](</assets/posts/2025-11/삽입%20정렬%20(Insertion%20Sort)/photo01.drawio.svg>)

삽입 정렬은 두 번째 원소부터 진행하며 선택한 원소의 앞 부분은 정렬된 부분이다. 현재 앞 부분에 원소가 하나 밖에 없으므로 정렬이 된 상태로 볼 수 있다. 삽입할 원소를 미리 복사해 놓는다.

![](</assets/posts/2025-11/삽입%20정렬%20(Insertion%20Sort)/photo02.drawio.svg>)

정렬된 부분의 마지막 원소인 $4$가 $1$보다 크므로 뒤로 한칸 민다.

![](</assets/posts/2025-11/삽입%20정렬%20(Insertion%20Sort)/photo03.drawio.svg>)

더 이상 밀 원소가 없다. 첫 번째 칸이 삽입에 적절한 위치다.

![](</assets/posts/2025-11/삽입%20정렬%20(Insertion%20Sort)/photo04.drawio.svg>)

삽입을 완료한 모습으로 빨간색으로 칠한 구간이 정렬되어 있는 것을 볼 수 있다.

![](</assets/posts/2025-11/삽입%20정렬%20(Insertion%20Sort)/photo05.drawio.svg>)

세 번째 원소를 삽입할 차례로 미리 복사해 놓는다.

![](</assets/posts/2025-11/삽입%20정렬%20(Insertion%20Sort)/photo06.drawio.svg>)

정렬된 부분의 마지막 원소인 $4$가 $8$보다 작으므로 뒤로 밀지 않고 해당 위치에 $8$을 삽입한다. 삽입을 완료한 모습으로 빨간색으로 칠한 구간이 정렬되어 있는 것을 볼 수 있다.

![](</assets/posts/2025-11/삽입%20정렬%20(Insertion%20Sort)/photo07.drawio.svg>)

네 번째 원소를 삽입할 차례로 미리 복사해 놓는다.

![](</assets/posts/2025-11/삽입%20정렬%20(Insertion%20Sort)/photo08.drawio.svg>)

정렬된 부분의 마지막 원소인 $8$이 $3$보다 크므로 뒤로 한칸 민다.

![](</assets/posts/2025-11/삽입%20정렬%20(Insertion%20Sort)/photo09.drawio.svg>)

이전 원소인 $4$가 $3$보다 크므로 뒤로 한칸 민다.

![](</assets/posts/2025-11/삽입%20정렬%20(Insertion%20Sort)/photo10.drawio.svg>)

이전 원소인 $1$이 $3$보다 작으므로 뒤로 밀지 않고 해당 위치에 $3$을 삽입한다.

![](</assets/posts/2025-11/삽입%20정렬%20(Insertion%20Sort)/photo11.drawio.svg>)

삽입을 완료한 모습으로 빨간색으로 칠한 구간이 정렬되어 있는 것을 볼 수 있다.

![](</assets/posts/2025-11/삽입%20정렬%20(Insertion%20Sort)/photo12.drawio.svg>)

다섯 번째 원소를 삽입할 차례로 미리 복사해 놓는다.

![](</assets/posts/2025-11/삽입%20정렬%20(Insertion%20Sort)/photo13.drawio.svg>)

정렬된 부분의 마지막 원소인 $8$이 $6$보다 크므로 뒤로 한칸 민다.

![](</assets/posts/2025-11/삽입%20정렬%20(Insertion%20Sort)/photo14.drawio.svg>)

이전 원소인 $4$가 $6$보다 작으므로 뒤로 밀지 않고 해당 위치에 $6$을 삽입한다.

![](</assets/posts/2025-11/삽입%20정렬%20(Insertion%20Sort)/photo15.drawio.svg>)

삽입을 완료한 모습으로 빨간색으로 칠한 구간이 정렬되어 있는 것을 볼 수 있다.

![](</assets/posts/2025-11/삽입%20정렬%20(Insertion%20Sort)/photo16.drawio.svg>)

여섯 번째 원소를 삽입할 차례로 미리 복사해 놓는다.

![](</assets/posts/2025-11/삽입%20정렬%20(Insertion%20Sort)/photo17.drawio.svg>)

정렬된 부분의 마지막 원소인 $8$이 $10$보다 작으므로 뒤로 밀지 않고 해당 위치에 $10$을 삽입한다. 삽입을 완료한 모습으로 빨간색으로 칠한 구간이 정렬되어 있는 것을 볼 수 있다.

![](</assets/posts/2025-11/삽입%20정렬%20(Insertion%20Sort)/photo18.drawio.svg>)

일곱 번째 원소를 삽입할 차례로 미리 복사해 놓는다.

![](</assets/posts/2025-11/삽입%20정렬%20(Insertion%20Sort)/photo19.drawio.svg>)

정렬된 부분의 마지막 원소인 $10$이 $8$보다 크므로 뒤로 한칸 민다.

![](</assets/posts/2025-11/삽입%20정렬%20(Insertion%20Sort)/photo20.drawio.svg>)

이전 원소인 $8$이 $8$과 같으므로 뒤로 밀지 않고 해당 위치에 $8$을 삽입한다. 동일한 가중치일 때 뒤에 있던 원소가 그대로 뒤에 삽입되기 때문에 삽입 정렬은 안정 정렬이다.

![](</assets/posts/2025-11/삽입%20정렬%20(Insertion%20Sort)/photo21.drawio.svg>)

삽입을 완료한 모습으로 빨간색으로 칠한 구간이 정렬되어 있는 것을 볼 수 있다.

![](</assets/posts/2025-11/삽입%20정렬%20(Insertion%20Sort)/photo22.drawio.svg>)

마지막 원소를 삽입할 차례로 미리 복사해 놓는다.

![](</assets/posts/2025-11/삽입%20정렬%20(Insertion%20Sort)/photo23.drawio.svg>)

정렬된 부분의 마지막 원소인 $10$이 $4$보다 크므로 뒤로 한칸 민다.

![](</assets/posts/2025-11/삽입%20정렬%20(Insertion%20Sort)/photo24.drawio.svg>)

이전 원소인 $8$이 $4$보다 크므로 뒤로 한칸 민다.

![](</assets/posts/2025-11/삽입%20정렬%20(Insertion%20Sort)/photo25.drawio.svg>)

이전 원소인 $8$이 $4$보다 크므로 뒤로 한칸 민다.

![](</assets/posts/2025-11/삽입%20정렬%20(Insertion%20Sort)/photo26.drawio.svg>)

이전 원소인 $6$이 $4$보다 크므로 뒤로 한칸 민다.

![](</assets/posts/2025-11/삽입%20정렬%20(Insertion%20Sort)/photo27.drawio.svg>)

이전 원소인 $4$가 $4$와 같으므로 뒤로 밀지 않고 해당 위치에 $4$을 삽입한다.

![](</assets/posts/2025-11/삽입%20정렬%20(Insertion%20Sort)/photo28.drawio.svg>)

삽입을 완료한 모습으로 빨간색으로 칠한 구간이 정렬되어 있는 것을 볼 수 있다.

![](</assets/posts/2025-11/삽입%20정렬%20(Insertion%20Sort)/photo29.drawio.svg>)

마지막 수까지 삽입을 완료했으므로 삽입 정렬을 종료한다. 이렇게 삽입 정렬을 통해 주어진 수들을 오름차순으로 정렬하는데 성공했다.

---

## 삽입 정렬 코드

### 삽입 정렬 [Java]

$100,000$개의 임의의 수들에 대한 정렬에서 약 1.4초정도 소요됐다.(Macbook M3 Air, JDK 21)

버블 정렬이나 선택 정렬과 동일한 시간복잡도지만 더 빠른 것을 볼 수 있었다.

```java
public static void insertionSort(int[] arr) {
    int N = arr.length;

    for (int i = 1; i < N; i++) {  // N-1개만 정렬하면 됨
        int key = arr[i];  // 삽입할 원소 복사
        int j = i - 1;

        // 삽입할 원소보다 더 큰 원소들은 뒤로 한칸씩 이동
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j--;
        }

        arr[j + 1] = key;  // 삽입
    }
}
```

---

## Ref

- [wikipedia - 삽입 정렬](https://ko.wikipedia.org/wiki/%EC%82%BD%EC%9E%85_%EC%A0%95%EB%A0%AC)

---
