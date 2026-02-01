---
title: "[BaekJoon] 13136번 - Do Not Touch Anything [Java][C++]"
slug: baekjoon-13136
date: 2026-02-01
categories: [PS, BaekJoon]
tags: [Math]
toc: true
math: true
---

[문제 링크](https://www.acmicpc.net/problem/13136)

---

## 1. 문제 풀이

<br>

CCTV 한 대는 $N \times N$ 크기의 영역을 커버할 수 있다. 따라서 주어진 대회장의 가로에는 $R / N$ 을 올림 나눗셈한만큼 배치를 해야하고, 세로에는 $C / N$ 을 올림 나눗셈만큼 배치해야하며 둘의 곱으로 필요한 최소 CCTV 수를 구할 수 있다. 이때 CCTV의 수가 정수 타입 오버플로우가 될 수 있음에 주의해야 한다.

---

## 2. 코드

<br>

### 1. 풀이 [Java]

```java
import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());

        int R = Integer.parseInt(st.nextToken());
        int C = Integer.parseInt(st.nextToken());
        int N = Integer.parseInt(st.nextToken());

        System.out.println((long) ((R + N - 1) / N) * ((C + N - 1) / N));
    }
}
```

<br>

### 2. 풀이 [C++]

```c++
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long r, c, n;
    cin >> r >> c >> n;
    cout << ((r + n - 1) / n) * ((c + n - 1) / n);
}
```

---
