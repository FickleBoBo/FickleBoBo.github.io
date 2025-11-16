---
title: "[백준] 2433번 - The Sound of Silence [Java]"
date: 2025-11-16
categories: [PS, BaekJoon]
tags: [슬라이딩 윈도우, 덱, 덱을 이용한 구간 최대/최소 트릭]
toc: true
math: true
---

[문제 링크](https://www.acmicpc.net/problem/2433)

![](/assets/posts/2025-11/백준%202433%20The%20Sound%20of%20Silence/photo1.png)
![](/assets/posts/2025-11/백준%202433%20The%20Sound%20of%20Silence/photo2.png)

---

## 문제 풀이

[덱을 이용한 구간 최대/최소 트릭]({% post_url 2025-11/2025-11-16-덱을 이용한 구간 최대／최소 트릭 (Sliding Window Maximum／Minimum with a Monotonic Deque) %}) 을 활용하면 해결할 수 있는 문제로 구간의 최솟값과 최댓값이 모두 필요한데 이를 각각 단조 증가 덱, 단조 감소 덱으로 관리하며 최댓값과 최솟값의 차를 `c`와 비교하는 방식으로 해결했다.

---

## 코드

### 1. 덱을 이용한 구간 최대/최소 트릭 [Java]

번호와 인덱스를 맞추기 위해 앞에 패딩을 한 칸 줬다.

```java
import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));
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

        Deque<Integer> minDq = new ArrayDeque<>();  // 단조 증가 덱
        Deque<Integer> maxDq = new ArrayDeque<>();  // 단조 감소 덱
        for (int i = 1; i <= n; i++) {
            // 구간에서 나가는 인덱스 처리
            if (!minDq.isEmpty() && minDq.peekFirst() < (i - m + 1)) {
                minDq.pollFirst();
            }

            // 구간으로 들어오는 인덱스 처리
            while (!minDq.isEmpty() && arr[minDq.peekLast()] >= arr[i]) {
                minDq.pollLast();
            }
            minDq.offerLast(i);

            // 구간에서 나가는 인덱스 처리
            if (!maxDq.isEmpty() && maxDq.peekFirst() < (i - m + 1)) {
                maxDq.pollFirst();
            }

            // 구간으로 들어오는 인덱스 처리
            while (!maxDq.isEmpty() && arr[maxDq.peekLast()] <= arr[i]) {
                maxDq.pollLast();
            }
            maxDq.offerLast(i);

            // 윈도우 크기가 확보됐을 때부터 비교
            if ((i > m - 1) && (arr[maxDq.peekFirst()] - arr[minDq.peekFirst()] <= c)) {
                sb.append(i - m + 1).append('\n');
            }
        }

        if (sb.length() == 0) {
            bw.write("NONE");
        } else {
            bw.write(sb.toString());
        }
        bw.flush();
    }
}
```

---

## 풀이 정보

### 1. 덱을 이용한 구간 최대/최소 트릭 [Java]

- 35 min

![](/assets/posts/2025-11/백준%202433%20The%20Sound%20of%20Silence/photo3.png)

---
