---
title: "[BaekJoon] #31654 - Adding Trouble [Java][C++]"
date: 2025-12-31
categories: [PS, BaekJoon]
tags: ["warm up"]
slug: baekjoon-31654
media_subpath: /assets/img/posts/baekjoon-31654/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://www.acmicpc.net/problem/31654)
{: .prompt-info }

---

## 1. 아이디어

$A + B = C$인지 판별하는 문제로 조건문을 활용하면 해결할 수 있다.

---

## 2. 복잡도

| 접근 | 시간   | 공간   |
| ---- | ------ | ------ |
| 풀이 | $O(1)$ | $O(1)$ |

---

## 3. 코드

### 풀이 [Java][C++]

```java
import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());

        int a = Integer.parseInt(st.nextToken());
        int b = Integer.parseInt(st.nextToken());
        int c = Integer.parseInt(st.nextToken());

        if (a + b == c) {
            System.out.println("correct!");
        } else {
            System.out.println("wrong!");
        }
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);

    int a, b, c;
    cin >> a >> b >> c;

    if (a + b == c) {
        cout << "correct!";
    } else {
        cout << "wrong!";
    }
}
```

---
