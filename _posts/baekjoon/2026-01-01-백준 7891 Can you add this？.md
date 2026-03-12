---
title: "[BaekJoon] 7891번 - Can you add this? [Java][C++]"
slug: baekjoon-7891
date: 2026-01-01
categories: [PS, BaekJoon]
tags: [Unlinked]
toc: true
math: true
---

[문제 링크](https://www.acmicpc.net/problem/7891)

---

## 1. 아이디어

<br>

두 수의 합을 구하면 되는 간단한 문제다.

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
        StringTokenizer st;
        StringBuilder sb = new StringBuilder();

        int t = Integer.parseInt(br.readLine());
        while (t-- > 0) {
            st = new StringTokenizer(br.readLine());
            int x = Integer.parseInt(st.nextToken());
            int y = Integer.parseInt(st.nextToken());
            sb.append(x + y).append("\n");
        }

        System.out.println(sb);
    }
}
```

<br>

### 2. 풀이 [C++]

```c++
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);

    int t;
    cin >> t;

    while (t--) {
        int x, y;
        cin >> x >> y;
        cout << x + y << '\n';
    }
}
```

---

## 3. 디버깅

<br>

없음.

---

## 4. 참고

<br>

없음.

---
