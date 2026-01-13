---
title: "[자료구조/알고리즘] 세그먼트 트리 (Segment Tree)"
slug: segment-tree
date: 2025-12-31
categories: [DSA]
tags: [Data Structures, Segment Tree, Divide and Conquer]
toc: true
math: true
image: /assets/posts/segment-tree/thumbnail.drawio.svg
---

## 1. 세그먼트 트리

<br>

**세그먼트 트리(Segment Tree)**는 구간에 대한 정보를 트리 형태로 저장하는 자료구조로 이를 통해 구간 쿼리를 효율적으로 처리할 수 있다. 세그먼트 트리는 굉장히 유연한 자료구조로 다양한 문제들을 해결할 수 있는데, 이번 챕터에서는 단일 원소 갱신과 구간 쿼리(구간 합, 구간 곱, 구간 최솟값, 구간 최댓값)를 처리할 수 있는 기본적인 세그먼트 트리에 대해 서술하겠다.

---

## 2. 세그먼트 트리 예시

<br>

임의의 배열에 대해 단일 원소 갱신과 구간 합 쿼리를 처리할 수 있는 세그먼트 트리를 만든다고 해보자. 세그먼트 트리는 리프 노드와 리프 노드가 아닌 노드들로 이루어지는데, 리프 노드는 배열의 해당 수 자체를 저장하며 리프 노드가 아닌 노드는 왼쪽 자식 노드와 오른쪽 자식 노드의 합을 저장하면 된다. 구간 곱이나 구간 최솟값, 최댓값의 경우 해당 로직을 그대로 적용하면 된다.

<br>

주어진 배열이 아래와 같을 경우

![](/assets/posts/segment-tree/photo01.drawio.svg)

<br>

구간 합을 구하는 세그먼트 트리는 아래와 같이 만들 수 있다.

![](/assets/posts/segment-tree/photo02.drawio.svg)

<br>

리프 노드에는 배열의 해당 수 자체가 저장됐으며,

![](/assets/posts/segment-tree/photo03.drawio.svg)

<br>

리프 노드가 아닌 노드는 왼쪽 자식 노드와 오른쪽 자식 노드의 합이 저장됐다.

![](/assets/posts/segment-tree/photo04.drawio.svg)

<br>

각 노드의 값은 아래 구간의 합과 같다.

![](/assets/posts/segment-tree/photo05.drawio.svg)

<br>

만약 배열에서 인덱스 $2$ 부터 $8$ 까지의 구간 합을 구해야한다면 아래 표시한 노드들의 합으로 이를 처리할 수 있다. 배열만 있을 때는 $7$ 개의 원소를 모두 더해야 했지만, 세그먼트 트리에서는 $4$ 개의 노드만 더하면 된다.

![](/assets/posts/segment-tree/photo06.drawio.svg)

<br>

배열에서 특정 원소 하나를 갱신하는 것 역시 간단하게 해결할 수 있는데 해당 원소를 구간에 포함하는 노드들을 전부 갱신해주면 된다. 아래는 인덱스 $6$ 의 원소를 갱신할 경우 갱신해야 하는 노드들이다.

![](/assets/posts/segment-tree/photo07.drawio.svg)

---

## 3. 세그먼트 트리 - Build

<br>

세그먼트 트리의 기본적인 동작 원리를 파악했다면 이제 주어진 배열로부터 세그먼트 트리를 만드는 Build 단계를 알아보겠다.

<br>

세그먼트 트리는 배열을 활용해서 이진 트리로 구현하는데, 이때 원본 배열의 크기 $N$ 만큼의 리프 노드를 가진다. $N$ 이 2의 거듭제곱일 경우 **포화 이진 트리(Perfect Binary Tree)**가 돼서 트리가 딱 맞게 떨어지지만, 2의 거듭제곱이 아닐 경우 2의 거듭제곱까지 더미 노드를 채운다. 이때 $N$ 이상인 가장 가까운 2의 거듭제곱을 $M$ 이라고 하면 $N \le M < 2N$ 이 되며, 더미 노드를 포함한 전체 노드의 수는 $2M - 1$ 보다 작거나 같아서 $2M - 1 < 4N - 1$ 이기 때문에 관례적으로 세그먼트 트리를 위한 배열의 크기를 $4 \times N$ 으로 잡아준다.

<br>

위 세그먼트 트리의 경우 실제 트리를 표현한 배열에서 저장되는 인덱스가 아래와 같이 된다.

![](/assets/posts/segment-tree/photo08.drawio.svg)

자식 노드 계산의 편의를 위해 루트 노드를 인덱스 $1$ 에 매핑시켜줬고(1-based), $N = 10$ 이라서 트리 배열의 크기는 $40$ 이다. 인덱스 $32$ 부터 $39$ 까지는 편의상 생략했다.

<br>

코드로 구현할 때는 재귀를 활용하면 Build를 간단하게 할 수 있다. 기본적으로 현재 노드의 트리 배열에서의 인덱스와 현재 노드가 처리할 수 있는 원본 배열에서의 구간을 파라미터로 넘겨준다. 현재 노드의 트리 배열에서의 인덱스는 `node`로, 현재 노드가 처리할 수 있는 원본 배열에서의 구간은 `start`, `end`로 넘겨줬다. `start`와 `end`가 동일하면 리프 노드이므로 트리 배열에 해당 원소를 넣어주고 종료하면 되며, 현재 노드의 값은 양쪽 자식 노드의 합이므로 이를 처리해주면 된다. 대략적인 코드는 아래와 같다.

```
build(int[] arr, int node, int start, int end) {
    // 구간의 길이가 1이므로 현재 노드는 리프 노드
    if (start == end) {
        tree[node] = arr[start];
        return;
    }

    int mid = (start + end) / 2;

    build(arr, node * 2, start, mid);  // 왼쪽 자식 노드
    build(arr, node * 2 + 1, mid + 1, end);  // 오른쪽 자식 노드
    tree[node] = tree[node * 2] + tree[node * 2 + 1];  // 왼쪽 자식 노드와 오른쪽 자식 노드의 합이 현재 노드 값
}

// 세그먼트 트리
int[] tree = new int[4 * n];

// 루트 노드의 인덱스인 1과 루트 노드가 처리할 수 있는 구간(원본 배열 전체)을 넘겨서 초기화
build(arr, 1, 0, n - 1);
```

---

## 4. 세그먼트 트리 - Update

<br>

세그먼트 트리에서 특정 원소의 변경은 해당 원소를 구간 내에 포함한 노드들을 전부 갱신해주면 된다. 이 역시 재귀적으로 구현할 수 있다. 배열에서 인덱스가 `idx`인 원소를 `value`로 갱신할 경우 대략적인 코드는 아래와 같다.

```
update(int node, int start, int end, int idx, int value) {
    // 구간의 길이가 1이므로 현재 노드는 리프 노드
    if (start == end) {
        tree[node] = value;
        return;
    }

    int mid = (start + end) / 2;

    if (idx <= mid) {
        update(node * 2, start, mid, idx, value);  // 왼쪽 자식 노드에 포함되는 구간이면 재귀적으로 업데이트
    } else {
        update(node * 2 + 1, mid + 1, end, idx, value);  // 오른쪽 자식 노드에 포함되는 구간이면 재귀적으로 업데이트
    }
    tree[node] = tree[node * 2] + tree[node * 2 + 1];
}

update(1, 0, n - 1, idx, value);
```

<br>

현재 노드가 리프 노드이면 해당 원소의 갱신을 수행하면 되며 재귀 과정에서 갱신할 노드가 왼쪽 자식 노드에 포함됐는지 오른쪽 자식 노드에 포함됐는지 조건문을 통해 판단하며 재귀 스택을 내려간다. 갱신이 수행되면 부모 노드도 재귀적으로 갱신해주면 된다.

---

## 5. 세그먼트 트리 - Query

<br>

세그먼트 트리에서 구간 합을 구하는 쿼리는 구간의 양 끝을 의미하는 `left`, `right` 변수가 필요하다. 세그먼트 트리에서 현재 노드가 처리하는 구간이 주어진 구간에 완전히 포함되면 해당 노드의 값을 반환하면 되며, 일부만 포함될 경우 재귀적으로 구간이 나뉜 두 자식 노드에서 탐색을 반복하면 된다. 현재 노드가 처리하는 구간과 주어진 구간이 전혀 겹치지 않으면 탐색을 종료하면 되는데, 이때는 $0$ 을 반환해서 재귀적으로 양 쪽의 합을 반환하는 쿼리에서 해당 구간이 유효하지 않음을 나타내면 된다. 덧셈에 대한 항등원이 $0$ 이라서 여기서는 $0$ 을 반환하는데 구간 곱, 구간 최솟값, 최댓값 등에서는 각 연산의 항등원을 반환하면 된다. 대략적인 코드는 아래와 같다.

```
int query(int node, int start, int end, int left, int right) {
    if (left > end || right < start) return 0;  // 현재 노드가 처리할 수 있는 구간이 쿼리의 구간을 완전히 벗어나는 경우 항등원 반환
    if (left <= start && end <= right) return tree[node];  // 현재 노드가 처리할 수 있는 구간이 쿼리의 구간에 완전히 포함되면 해당 값 반환

    int mid = (start + end) / 2;

    int leftSum = query(node * 2, start, mid, left, right);
    int rightSum = query(node * 2 + 1, mid + 1, end, left, right);
    return leftSum + rightSum;
}

// 원본 배열에서 [left, right]의 구간 합 구하기
query(1, 0, n - 1, left, right);
```

<br>

이전의 인덱스 $2$ 부터 인덱스 $8$ 까지의 구간 합 쿼리의 경우 아래와 같은 재귀 과정으로 구간 합을 구한다.

<br>

재귀 스택 0

- 인덱스 $0$ ~ $9$ 가 인덱스 $2$ ~ $8$ 에 일부만 포함되므로 다음 재귀 스택으로 내려간다.

재귀 스택 1

- 인덱스 $0$ ~ $4$ 는 인덱스 $2$ ~ $8$ 에 일부만 포함되므로 다음 재귀 스택으로 내려간다.
- 인덱스 $5$ ~ $9$ 는 인덱스 $2$ ~ $8$ 에 일부만 포함되므로 다음 재귀 스택으로 내려간다.

재귀 스택 2

- 인덱스 $0$ ~ $2$ 는 인덱스 $2$ ~ $8$ 에 일부만 포함되므로 다음 재귀 스택으로 내려간다.
- 인덱스 $3$ ~ $4$ 는 인덱스 $2$ ~ $8$ 에 완전히 포함되므로 해당 값을 반환한다.
- 인덱스 $5$ ~ $7$ 은 인덱스 $2$ ~ $8$ 에 완전히 포함되므로 해당 값을 반환한다.
- 인덱스 $8$ ~ $9$ 는 인덱스 $2$ ~ $8$ 에 일부만 포함되므로 다음 재귀 스택으로 내려간다.

재귀 스택 3

- 인덱스 $0$ ~ $1$ 은 인덱스 $2$ ~ $8$ 을 완전히 벗어나므로 $0$ 을 반환한다.
- 인덱스 $2$ 는 인덱스 $2$ ~ $8$ 에 완전히 포함되므로 해당 값을 반환한다.
- 인덱스 $8$ 은 인덱스 $2$ ~ $8$ 에 완전히 포함되므로 해당 값을 반환한다.
- 인덱스 $9$ 는 인덱스 $2$ ~ $8$ 을 완전히 벗어나므로 $0$ 을 반환한다.

---

## 6. 세그먼트 트리 성능

<br>

세그먼트 트리는 원본 배열의 크기가 $N$ 일 때, Build에 $O(N)$, Update에 $O(\log{N})$, Query에 $O(\log{N})$ 의 시간복잡도와 $O(4 \times N)$ 의 공간복잡도가 소요되는 자료구조다.

구간 쿼리를 한 번만 할 경우는 그냥 계산해도 되지만 구간 쿼리가 반복되는 경우 이를 효율적으로 처리할 수 있으며, 단일 원소의 갱신 쿼리도 효율적으로 해결할 수 있어서, 누적 합이나 희소 테이블과 달리 갱신 쿼리에도 대응할 수 있다.

---

## 7. 세그먼트 트리 코드

<br>

일반적인 세그먼트 트리는 반복문으로도 구현이 가능한데 이해의 편의와 향후 확장성을 고려해서 재귀를 기반으로 구현했다. Java의 클래스나 C++의 구조체를 활용하지 않고 전역 배열과 함수 기반으로도 많이 구현하는데 구조화를 위해 객체 단위로 구현했다.

<br>

### 1. 세그먼트 트리 - 구간 합 [Java]

```java
public class SegmentTree {
    int n;
    long[] tree;

    public SegmentTree(int[] arr) {
        this.n = arr.length;
        this.tree = new long[4 * n];
        init(arr, 1, 0, n - 1);
    }

    void init(int[] arr, int node, int start, int end) {
        if (start == end) {
            tree[node] = arr[start];
            return;
        }

        int mid = (start + end) / 2;

        init(arr, node * 2, start, mid);
        init(arr, node * 2 + 1, mid + 1, end);
        tree[node] = tree[node * 2] + tree[node * 2 + 1];
    }

    void update(int idx, int value) {
        update(1, 0, n - 1, idx, value);
    }

    void update(int node, int start, int end, int idx, int value) {
        if (start == end) {
            tree[node] = value;
            return;
        }

        int mid = (start + end) / 2;

        if (idx <= mid) {
            update(node * 2, start, mid, idx, value);
        } else {
            update(node * 2 + 1, mid + 1, end, idx, value);
        }
        tree[node] = tree[node * 2] + tree[node * 2 + 1];
    }

    long sum(int left, int right) {
        return sum(1, 0, n - 1, left, right);
    }

    long sum(int node, int start, int end, int left, int right) {
        if (left > end || right < start) return 0;
        if (left <= start && end <= right) return tree[node];

        int mid = (start + end) / 2;

        long leftSum = sum(node * 2, start, mid, left, right);
        long rightSum = sum(node * 2 + 1, mid + 1, end, left, right);
        return leftSum + rightSum;
    }
}
```

<br>

### 2. 세그먼트 트리 - 구간 합 [C++]

```c++
struct SegTree {
    int n;
    vector<long long> tree;

    SegTree(int n) : n(n), tree(4 * n) {
    }

    void init(const vector<int>& arr, int node, int start, int end) {
        if (start == end) {
            tree[node] = arr[start];
            return;
        }

        int mid = (start + end) / 2;

        init(arr, node * 2, start, mid);
        init(arr, node * 2 + 1, mid + 1, end);
        tree[node] = tree[node * 2] + tree[node * 2 + 1];
    }

    void update(int node, int start, int end, int idx, int value) {
        if (start == end) {
            tree[node] = value;
            return;
        }

        int mid = (start + end) / 2;

        if (idx <= mid) {
            update(node * 2, start, mid, idx, value);
        } else {
            update(node * 2 + 1, mid + 1, end, idx, value);
        }
        tree[node] = tree[node * 2] + tree[node * 2 + 1];
    }

    long long query(int node, int start, int end, int left, int right) {
        if (left > end || right < start) return 0;
        if (left <= start && end <= right) return tree[node];

        int mid = (start + end) / 2;

        long long leftSum = query(node * 2, start, mid, left, right);
        long long rightSum = query(node * 2 + 1, mid + 1, end, left, right);
        return leftSum + rightSum;
    }
};
```

<br>

### 3. 세그먼트 트리 - 구간 곱 [Java]

```java
public class SegmentTree {
    int n;
    long[] tree;

    public SegmentTree(int[] arr) {
        this.n = arr.length;
        this.tree = new long[4 * n];
        init(arr, 1, 0, n - 1);
    }

    void init(int[] arr, int node, int start, int end) {
        if (start == end) {
            tree[node] = arr[start];
            return;
        }

        int mid = (start + end) / 2;

        init(arr, node * 2, start, mid);
        init(arr, node * 2 + 1, mid + 1, end);
        tree[node] = tree[node * 2] * tree[node * 2 + 1];
    }

    void update(int idx, int value) {
        update(1, 0, n - 1, idx, value);
    }

    void update(int node, int start, int end, int idx, int value) {
        if (start == end) {
            tree[node] = value;
            return;
        }

        int mid = (start + end) / 2;

        if (idx <= mid) {
            update(node * 2, start, mid, idx, value);
        } else {
            update(node * 2 + 1, mid + 1, end, idx, value);
        }
        tree[node] = tree[node * 2] * tree[node * 2 + 1];
    }

    long mul(int left, int right) {
        return mul(1, 0, n - 1, left, right);
    }

    long mul(int node, int start, int end, int left, int right) {
        if (left > end || right < start) return 1;
        if (left <= start && end <= right) return tree[node];

        int mid = (start + end) / 2;

        long leftMul = mul(node * 2, start, mid, left, right);
        long rightMul = mul(node * 2 + 1, mid + 1, end, left, right);
        return leftMul * rightMul;
    }
}
```

<br>

### 4. 세그먼트 트리 - 구간 곱 [C++]

```c++
struct SegTree {
    int n;
    vector<long long> tree;

    SegTree(int n) : n(n), tree(4 * n) {
    }

    void init(const vector<int>& arr, int node, int start, int end) {
        if (start == end) {
            tree[node] = arr[start];
            return;
        }

        int mid = (start + end) / 2;

        init(arr, node * 2, start, mid);
        init(arr, node * 2 + 1, mid + 1, end);
        tree[node] = tree[node * 2] * tree[node * 2 + 1];
    }

    void update(int node, int start, int end, int idx, int value) {
        if (start == end) {
            tree[node] = value;
            return;
        }

        int mid = (start + end) / 2;

        if (idx <= mid) {
            update(node * 2, start, mid, idx, value);
        } else {
            update(node * 2 + 1, mid + 1, end, idx, value);
        }
        tree[node] = tree[node * 2] * tree[node * 2 + 1];
    }

    long long query(int node, int start, int end, int left, int right) {
        if (left > end || right < start) return 1;
        if (left <= start && end <= right) return tree[node];

        int mid = (start + end) / 2;

        long long leftMul = query(node * 2, start, mid, left, right);
        long long rightMul = query(node * 2 + 1, mid + 1, end, left, right);
        return leftMul * rightMul;
    }
};
```

<br>

### 5. 세그먼트 트리 - 구간 최솟값 [Java]

```java
public class SegmentTree {

    static int MAX = Integer.MAX_VALUE;

    int n;
    int[] tree;

    public SegmentTree(int[] arr) {
        this.n = arr.length;
        this.tree = new int[4 * n];
        init(arr, 1, 0, n - 1);
    }

    void init(int[] arr, int node, int start, int end) {
        if (start == end) {
            tree[node] = arr[start];
            return;
        }

        int mid = (start + end) / 2;

        init(arr, node * 2, start, mid);
        init(arr, node * 2 + 1, mid + 1, end);
        tree[node] = Math.min(tree[node * 2], tree[node * 2 + 1]);
    }

    void update(int idx, int value) {
        update(1, 0, n - 1, idx, value);
    }

    void update(int node, int start, int end, int idx, int value) {
        if (start == end) {
            tree[node] = value;
            return;
        }

        int mid = (start + end) / 2;

        if (idx <= mid) {
            update(node * 2, start, mid, idx, value);
        } else {
            update(node * 2 + 1, mid + 1, end, idx, value);
        }
        tree[node] = Math.min(tree[node * 2], tree[node * 2 + 1]);
    }

    int min(int left, int right) {
        return min(1, 0, n - 1, left, right);
    }

    int min(int node, int start, int end, int left, int right) {
        if (left > end || right < start) return MAX;
        if (left <= start && end <= right) return tree[node];

        int mid = (start + end) / 2;

        int leftMin = min(node * 2, start, mid, left, right);
        int rightMin = min(node * 2 + 1, mid + 1, end, left, right);
        return Math.min(leftMin, rightMin);
    }
}
```

<br>

### 6. 세그먼트 트리 - 구간 최솟값 [C++]

```c++
constexpr int MAX = INT_MAX;

struct SegTree {
    int n;
    vector<int> tree;

    SegTree(int n) : n(n), tree(4 * n) {
    }

    void init(const vector<int>& arr, int node, int start, int end) {
        if (start == end) {
            tree[node] = arr[start];
            return;
        }

        int mid = (start + end) / 2;

        init(arr, node * 2, start, mid);
        init(arr, node * 2 + 1, mid + 1, end);
        tree[node] = min(tree[node * 2], tree[node * 2 + 1]);
    }

    void update(int node, int start, int end, int idx, int value) {
        if (start == end) {
            tree[node] = value;
            return;
        }

        int mid = (start + end) / 2;

        if (idx <= mid) {
            update(node * 2, start, mid, idx, value);
        } else {
            update(node * 2 + 1, mid + 1, end, idx, value);
        }
        tree[node] = min(tree[node * 2], tree[node * 2 + 1]);
    }

    int query(int node, int start, int end, int left, int right) {
        if (left > end || right < start) return MAX;
        if (left <= start && end <= right) return tree[node];

        int mid = (start + end) / 2;

        int leftMin = query(node * 2, start, mid, left, right);
        int rightMin = query(node * 2 + 1, mid + 1, end, left, right);
        return min(leftMin, rightMin);
    }
};
```

<br>

### 7. 세그먼트 트리 - 구간 최댓값 [Java]

```java
public class SegmentTree {

    static int MIN = Integer.MIN_VALUE;

    int n;
    int[] tree;

    public SegmentTree(int[] arr) {
        this.n = arr.length;
        this.tree = new int[4 * n];
        init(arr, 1, 0, n - 1);
    }

    void init(int[] arr, int node, int start, int end) {
        if (start == end) {
            tree[node] = arr[start];
            return;
        }

        int mid = (start + end) / 2;

        init(arr, node * 2, start, mid);
        init(arr, node * 2 + 1, mid + 1, end);
        tree[node] = Math.max(tree[node * 2], tree[node * 2 + 1]);
    }

    void update(int idx, int value) {
        update(1, 0, n - 1, idx, value);
    }

    void update(int node, int start, int end, int idx, int value) {
        if (start == end) {
            tree[node] = value;
            return;
        }

        int mid = (start + end) / 2;

        if (idx <= mid) {
            update(node * 2, start, mid, idx, value);
        } else {
            update(node * 2 + 1, mid + 1, end, idx, value);
        }
        tree[node] = Math.max(tree[node * 2], tree[node * 2 + 1]);
    }

    int max(int left, int right) {
        return max(1, 0, n - 1, left, right);
    }

    int max(int node, int start, int end, int left, int right) {
        if (left > end || right < start) return MIN;
        if (left <= start && end <= right) return tree[node];

        int mid = (start + end) / 2;

        int leftMax = max(node * 2, start, mid, left, right);
        int rightMax = max(node * 2 + 1, mid + 1, end, left, right);
        return Math.max(leftMax, rightMax);
    }
}
```

<br>

### 8. 세그먼트 트리 - 구간 최댓값 [C++]

```c++
constexpr int MIN = INT_MIN;

struct SegTree {
    int n;
    vector<int> tree;

    SegTree(int n) : n(n), tree(4 * n) {
    }

    void init(const vector<int>& arr, int node, int start, int end) {
        if (start == end) {
            tree[node] = arr[start];
            return;
        }

        int mid = (start + end) / 2;

        init(arr, node * 2, start, mid);
        init(arr, node * 2 + 1, mid + 1, end);
        tree[node] = max(tree[node * 2], tree[node * 2 + 1]);
    }

    void update(int node, int start, int end, int idx, int value) {
        if (start == end) {
            tree[node] = value;
            return;
        }

        int mid = (start + end) / 2;

        if (idx <= mid) {
            update(node * 2, start, mid, idx, value);
        } else {
            update(node * 2 + 1, mid + 1, end, idx, value);
        }
        tree[node] = max(tree[node * 2], tree[node * 2 + 1]);
    }

    int query(int node, int start, int end, int left, int right) {
        if (left > end || right < start) return MIN;
        if (left <= start && end <= right) return tree[node];

        int mid = (start + end) / 2;

        int leftMax = query(node * 2, start, mid, left, right);
        int rightMax = query(node * 2 + 1, mid + 1, end, left, right);
        return max(leftMax, rightMax);
    }
};
```

---

## 8. Problems

<br>

- [BaekJoon 2042번 - 구간 합 구하기](https://www.acmicpc.net/problem/2042)
- [BaekJoon 11505번 - 구간 곱 구하기](https://www.acmicpc.net/problem/11505)
- [BaekJoon 2357번 - 최솟값과 최댓값](https://www.acmicpc.net/problem/2357)
- [BaekJoon 18436번 - 수열과 쿼리 37](https://www.acmicpc.net/problem/18436)
- [BaekJoon 14428번 - 수열과 쿼리 16](https://www.acmicpc.net/problem/14428)

---

## Ref

<br>

- [BOJ BOOK - 세그먼트 트리](https://book.acmicpc.net/ds/segment-tree)
- [cp-algorithms - Segment Tree](https://cp-algorithms.com/data_structures/segment_tree.html)

---
