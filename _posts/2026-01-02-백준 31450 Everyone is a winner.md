---
title: "[BaekJoon] 31450번 - Everyone is a winner [Java][C++]"
slug: baekjoon-31450
date: 2026-01-02
categories: [PS, BaekJoon]
tags: [Warm Up]
toc: true
math: true
---

[문제 링크](https://www.acmicpc.net/problem/31450)

---

## 1. 문제 풀이

<br>

모든 아이들이 똑같은 개수의 메달을 받아야 하므로 $M$ 을 $K$ 로 나눈 나머지가 $0$ 인지 판단하면 된다.

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

        int M = Integer.parseInt(st.nextToken());
        int K = Integer.parseInt(st.nextToken());

        if (M % K == 0) {
            System.out.println("Yes");
        } else {
            System.out.println("No");
        }
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

    int m, k;
    cin >> m >> k;

    if (m % k == 0) {
        cout << "Yes";
    } else {
        cout << "No";
    }
}
```

---
