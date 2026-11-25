---
title: "[BaekJoon] #10214 - Baseball [Java][C++][Python]"
date: 2026-11-24
categories: [PS, BaekJoon]
tags: ["warm up"]
slug: baekjoon-10214
media_subpath: /assets/img/posts/baekjoon-10214/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://www.acmicpc.net/problem/10214)
{: .prompt-info }

---

## 1. 아이디어

경기마다 9회의 득점을 팀별로 합산해 합이 큰 팀을, 같으면 무승부를 출력하는 문제다.

---

## 2. 코드

### 풀이 [Java][C++][Python]

```java
import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));

        int t = Integer.parseInt(br.readLine());
        while (t-- > 0) {
            int ysum = 0;
            int ksum = 0;

            for (int i = 0; i < 9; i++) {
                StringTokenizer st = new StringTokenizer(br.readLine());
                int y = Integer.parseInt(st.nextToken());
                int k = Integer.parseInt(st.nextToken());
                ysum += y;
                ksum += k;
            }

            if (ysum > ksum) {
                bw.write("Yonsei\n");
            } else if (ysum < ksum) {
                bw.write("Korea\n");
            } else {
                bw.write("Draw\n");
            }
        }

        bw.flush();
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);

    int t;
    cin >> t;

    while (t--) {
        int ysum = 0;
        int ksum = 0;

        for (int i = 0; i < 9; i++) {
            int y, k;
            cin >> y >> k;
            ysum += y;
            ksum += k;
        }

        if (ysum > ksum) {
            cout << "Yonsei\n";
        } else if (ysum < ksum) {
            cout << "Korea\n";
        } else {
            cout << "Draw\n";
        }
    }
}
```

```python
import sys

input = sys.stdin.readline

t = int(input())
for _ in range(t):
    ysum, ksum = 0, 0
    for _ in range(9):
        y, k = map(int, input().split())
        ysum += y
        ksum += k

    if ysum > ksum:
        print("Yonsei")
    elif ysum < ksum:
        print("Korea")
    else:
        print("Draw")
```

---
