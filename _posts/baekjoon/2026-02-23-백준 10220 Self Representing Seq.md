---
title: "[BaekJoon] 10220번 - Self Representing Seq [Java][C++]"
slug: baekjoon-10220
date: 2026-02-23
categories: [PS, BaekJoon]
tags: [Math, Ad Hoc]
toc: true
math: true
---

[문제 링크](https://www.acmicpc.net/problem/10220)

---

## 1. 문제 풀이

<br>

주어진 조건을 만족하는 수열의 개수를 구해야하는 문제로 $N = 5$ 일 경우 주어진 조건을 만족하는 수열은 $[2, 1, 2, 0, 0]$ 뿐인데, 이는 $0$ 의 개수가 $2$ 개, $1$ 의 개수가 $1$ 개, $2$ 의 개수가 $2$ 개이면서 $A_0 = 2$, $A_1 = 1$, $A_2 = 2$ 이기 때문이다. DFS를 활용해서 $N = 1$ 일 때부터 $N = 100$ 일 때까지 탐색해보면 $N$ 이 $7$ 이상일 때부터 $A_0 = N - 4$, $A_1 = 2$, $A_2 = 1$, $A_{N - 4} = 1$, 나머지 항은 전부 $0$ 인 수열만 주어진 조건이 성립하는 것을 볼 수 있다.(성능상 $N = 18$ 까지만 돌려졌다.) 이러한 규칙을 토대로 $N = 1, 2, 3, 6$ 일 때는 주어진 조건을 만족하는 수열이 없으며, $N = 4$ 일 때는 주어진 조건을 만족하는 수열이 $2$ 개 존재하고, 그 외의 경우는 하나가 존재한다. $N < 7$ 까지는 직접 찾고, $N \ge 7$ 부터는 귀류적으로 증명도 할 수 있다고 하는데 아직 엄밀하게 증명되지는 않아서 이 부분은 생략했다.

---

## 2. 코드

<br>

### 1. 풀이 [Java]

```java
import java.io.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        int t = Integer.parseInt(br.readLine());
        while (t-- > 0) {
            int n = Integer.parseInt(br.readLine());
            if (n == 4) {
                System.out.println(2);
            } else if (n <= 3 || n == 6) {
                System.out.println(0);
            } else {
                System.out.println(1);
            }
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
    ios::sync_with_stdio(0);
    cin.tie(0);

    int t;
    cin >> t;

    while (t--) {
        int n;
        cin >> n;

        if (n == 4) {
            cout << 2 << '\n';
        } else if (n <= 3 || n == 6) {
            cout << 0 << '\n';
        } else {
            cout << 1 << '\n';
        }
    }
}
```

---
