---
title: "[BaekJoon] #10214 - Baseball [Java][C++]"
date: 2026-01-31
categories: [PS, BaekJoon]
tags: ["warm up"]
slug: baekjoon-10214
media_subpath: /assets/img/posts/baekjoon-10214/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://www.acmicpc.net/problem/10214)
{: .prompt-info }

---

## 1. 아이디어

테스트 케이스별로 9회 동안 각 팀의 점수 합을 더해서 비교만 하면 된다.

---

## 2. 복잡도

| 접근 | 시간   | 공간   |
| ---- | ------ | ------ |
| 풀이 | $O(T)$ | $O(1)$ |

($T$ = 테스트 케이스 수)

---

## 3. 코드

### 풀이 [Java][C++]

```java
import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));
        StringTokenizer st;

        int t = Integer.parseInt(br.readLine());
        while (t-- > 0) {
            int ysum = 0;
            int ksum = 0;

            for (int i = 0; i < 9; i++) {
                st = new StringTokenizer(br.readLine());
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

---
