---
title: "[BaekJoon] 2433번 - The Sound of Silence [Java][C++]"
slug: baekjoon-2433
date: 2025-12-20
categories: [PS, BaekJoon]
tags: [Sliding Window, Data Structures, Priority Queue, Monotonic Queue]
toc: true
math: true
---

[문제 링크](https://www.acmicpc.net/problem/2433)

---

## 1. 문제 풀이

<br>

[단조 큐를 활용한 슬라이딩 윈도우](/posts/sliding-window-maximum) 와 우선순위 큐 두 가지 방식 모두 적용 가능한 문제로 구간의 최솟값과 최댓값이 모두 필요한데 이를 각각 단조 증가 큐, 단조 감소 큐 또는 최소힙, 최대힙으로 관리하며 최댓값과 최솟값의 차를 $c$ 와 비교하는 방식으로 해결했다.

---

## 2. 코드

<br>

### 1. 단조 큐 [Java]

번호와 인덱스를 맞추기 위해 앞에 패딩을 한 칸 줬다.

```java
import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder sb = new StringBuilder();
        StringTokenizer st = new StringTokenizer(br.readLine());

        int n = Integer.parseInt(st.nextToken());
        int m = Integer.parseInt(st.nextToken());
        int c = Integer.parseInt(st.nextToken());

        int[] arr = new int[1 + n];
        st = new StringTokenizer(br.readLine());
        for (int i = 1; i <= n; i++) {
            arr[i] = Integer.parseInt(st.nextToken());
        }

        Deque<Integer> minDq = new ArrayDeque<>();  // 단조 증가 큐
        Deque<Integer> maxDq = new ArrayDeque<>();  // 단조 감소 큐
        for (int i = 1; i <= n; i++) {
            // 구간에서 나가는 인덱스 처리
            if (!minDq.isEmpty() && minDq.peekFirst() == (i - m)) {
                minDq.pollFirst();
            }

            // 구간으로 들어오는 인덱스 처리
            while (!minDq.isEmpty() && arr[i] <= arr[minDq.peekLast()]) {
                minDq.pollLast();
            }
            minDq.offerLast(i);

            // 구간에서 나가는 인덱스 처리
            if (!maxDq.isEmpty() && maxDq.peekFirst() == (i - m)) {
                maxDq.pollFirst();
            }

            // 구간으로 들어오는 인덱스 처리
            while (!maxDq.isEmpty() && arr[i] >= arr[maxDq.peekLast()]) {
                maxDq.pollLast();
            }
            maxDq.offerLast(i);

            // 윈도우 크기가 확보됐을 때부터 비교
            if ((i > m - 1) && (arr[maxDq.peekFirst()] - arr[minDq.peekFirst()] <= c)) {
                sb.append(i - m + 1).append("\n");
            }
        }

        if (sb.length() == 0) {
            System.out.println("NONE");
        } else {
            System.out.println(sb);
        }
    }
}
```

<br>

### 2. 우선순위 큐 [Java]

번호와 인덱스를 맞추기 위해 앞에 패딩을 한 칸 줬다.

```java
import java.io.*;
import java.util.*;

public class Main {

    static class Node {
        int value;
        int idx;

        public Node(int value, int idx) {
            this.value = value;
            this.idx = idx;
        }
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder sb = new StringBuilder();
        StringTokenizer st = new StringTokenizer(br.readLine());

        int n = Integer.parseInt(st.nextToken());
        int m = Integer.parseInt(st.nextToken());
        int c = Integer.parseInt(st.nextToken());

        int[] arr = new int[1 + n];
        st = new StringTokenizer(br.readLine());
        for (int i = 1; i <= n; i++) {
            arr[i] = Integer.parseInt(st.nextToken());
        }

        PriorityQueue<Node> minPq = new PriorityQueue<>(((o1, o2) -> {
            if (o1.value != o2.value) return Integer.compare(o1.value, o2.value);
            return Integer.compare(o1.idx, o2.idx);
        }));
        PriorityQueue<Node> maxPq = new PriorityQueue<>((o1, o2) -> {
            if (o1.value != o2.value) return Integer.compare(o2.value, o1.value);
            return Integer.compare(o1.idx, o2.idx);
        });
        for (int i = 1; i <= n; i++) {
            while (!minPq.isEmpty() && minPq.peek().idx <= (i - m)) {
                minPq.poll();
            }
            minPq.offer(new Node(arr[i], i));

            while (!maxPq.isEmpty() && maxPq.peek().idx <= (i - m)) {
                maxPq.poll();
            }
            maxPq.offer(new Node(arr[i], i));

            // 윈도우 크기가 확보됐을 때부터 비교
            if ((i > m - 1) && (maxPq.peek().value - minPq.peek().value <= c)) {
                sb.append(i - m + 1).append("\n");
            }
        }

        if (sb.length() == 0) {
            System.out.println("NONE");
        } else {
            System.out.println(sb);
        }
    }
}
```

<br>

### 3. 단조 큐 [C++]

```c++
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m, c;
    cin >> n >> m >> c;

    vector<int> v(n);
    for (int& x : v) cin >> x;

    deque<int> minDq;  // 단조 증가 큐
    deque<int> maxDq;  // 단조 감소 큐
    bool hasSilence = false;

    for (int i = 0; i < n; i++) {
        // 구간에서 나가는 인덱스 처리
        if (!minDq.empty() && minDq.front() == (i - m)) {
            minDq.pop_front();
        }

        // 구간으로 들어오는 인덱스 처리
        while (!minDq.empty() && v[i] <= v[minDq.back()]) {
            minDq.pop_back();
        }
        minDq.push_back(i);

        // 구간에서 나가는 인덱스 처리
        if (!maxDq.empty() && maxDq.front() == (i - m)) {
            maxDq.pop_front();
        }

        // 구간으로 들어오는 인덱스 처리
        while (!maxDq.empty() && v[i] >= v[maxDq.back()]) {
            maxDq.pop_back();
        }
        maxDq.push_back(i);

        // 윈도우 크기가 확보됐을 때부터 비교
        if ((i > m - 2) && (v[maxDq.front()] - v[minDq.front()] <= c)) {
            cout << i - m + 2 << '\n';
            hasSilence = true;
        }
    }

    if (!hasSilence) {
        cout << "NONE";
    }
}
```

<br>

### 4. 우선순위 큐 [C++]

```c++
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m, c;
    cin >> n >> m >> c;

    vector<int> v(n);
    for (int& x : v) cin >> x;

    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<>> minPq;  // 최소힙
    priority_queue<pair<int, int>> maxPq;                                     // 최대힙
    bool hasSilence = false;

    for (int i = 0; i < n; i++) {
        while (!minPq.empty() && minPq.top().second <= (i - m)) {
            minPq.pop();
        }
        minPq.push({v[i], i});

        while (!maxPq.empty() && maxPq.top().second <= (i - m)) {
            maxPq.pop();
        }
        maxPq.push({v[i], i});

        // 윈도우 크기가 확보됐을 때부터 비교
        if ((i > m - 2) && (maxPq.top().first - minPq.top().first <= c)) {
            cout << i - m + 2 << '\n';
            hasSilence = true;
        }
    }

    if (!hasSilence) {
        cout << "NONE";
    }
}
```

---
