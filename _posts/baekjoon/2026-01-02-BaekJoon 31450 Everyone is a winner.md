---
title: "[BaekJoon] #31450 - Everyone is a winner [Java][C++]"
date: 2026-01-02
categories: [PS, BaekJoon]
tags: ["warm up"]
slug: baekjoon-31450
media_subpath: /assets/img/posts/baekjoon-31450/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://www.acmicpc.net/problem/31450)
{: .prompt-info }

---

## 1. 아이디어

모든 아이들이 똑같은 개수의 메달을 받아야 하므로 $M$을 $K$로 나눈 나머지가 0인지 판단하면 된다.

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

        int m = Integer.parseInt(st.nextToken());
        int k = Integer.parseInt(st.nextToken());

        if (m % k == 0) {
            System.out.println("Yes");
        } else {
            System.out.println("No");
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
