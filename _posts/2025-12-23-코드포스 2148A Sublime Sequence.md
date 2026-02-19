---
title: "[Codeforces] #2148A - Sublime Sequence [Java][C++]"
slug: codeforces-9
date: 2025-12-23
categories: [PS, Codeforces]
tags: [Math]
toc: true
math: true
---

[문제 링크](https://codeforces.com/problemset/problem/2148/A)

---

## 1. 문제 풀이

<br>

$x$ 와 $n$ 이 주어졌을 때, 수열은 $x$, $-x$, $x$, $\ldots$ 와 같이 $x$ 의 부호가 바뀐 것이 $n$ 번 반복된다. 이때 수열의 합을 구하는 문제로 두 항마다 합이 $0$ 이 되므로 $n$ 이 짝수면 수열의 합은 $0$ 이 되며, $n$ 이 홀수면 수열의 합이 $x$ 가 된다.

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
        StringBuilder sb = new StringBuilder();
        StringTokenizer st;

        int t = Integer.parseInt(br.readLine());
        while (t-- > 0) {
            st = new StringTokenizer(br.readLine());
            int x = Integer.parseInt(st.nextToken());
            int n = Integer.parseInt(st.nextToken());

            if (n % 2 == 0) {
                sb.append("0\n");
            } else {
                sb.append(x).append("\n");
            }
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
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;

    while (t--) {
        int x, n;
        cin >> x >> n;

        if (n % 2 == 0) {
            cout << '0' << '\n';
        } else {
            cout << x << '\n';
        }
    }
}
```

---
