---
title: "[BaekJoon] #31429 - SUAPC 2023 Summer [Java][C++]"
date: 2026-01-03
categories: [PS, BaekJoon]
tags: ["warm up"]
slug: baekjoon-31429
media_subpath: /assets/img/posts/baekjoon-31429/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://www.acmicpc.net/problem/31429)
{: .prompt-info }

---

## 1. 아이디어

$N$등인 팀의 정보를 출력만 하면 된다.

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

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        int n = Integer.parseInt(br.readLine());

        if (n == 1) {
            System.out.println("12 1600");
        } else if (n == 2) {
            System.out.println("11 894");
        } else if (n == 3) {
            System.out.println("11 1327");
        } else if (n == 4) {
            System.out.println("10 1311");
        } else if (n == 5) {
            System.out.println("9 1004");
        } else if (n == 6) {
            System.out.println("9 1178");
        } else if (n == 7) {
            System.out.println("9 1357");
        } else if (n == 8) {
            System.out.println("8 837");
        } else if (n == 9) {
            System.out.println("7 1055");
        } else if (n == 10) {
            System.out.println("6 556");
        } else {
            System.out.println("6 773");
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

    int n;
    cin >> n;

    if (n == 1) {
        cout << "12 1600";
    } else if (n == 2) {
        cout << "11 894";
    } else if (n == 3) {
        cout << "11 1327";
    } else if (n == 4) {
        cout << "10 1311";
    } else if (n == 5) {
        cout << "9 1004";
    } else if (n == 6) {
        cout << "9 1178";
    } else if (n == 7) {
        cout << "9 1357";
    } else if (n == 8) {
        cout << "8 837";
    } else if (n == 9) {
        cout << "7 1055";
    } else if (n == 10) {
        cout << "6 556";
    } else {
        cout << "6 773";
    }
}
```

---
