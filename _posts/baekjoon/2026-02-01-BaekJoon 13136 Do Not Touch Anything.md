---
title: "[BaekJoon] #13136 - Do Not Touch Anything [Java][C++]"
date: 2026-02-01
categories: [PS, BaekJoon]
tags: ["math"]
slug: baekjoon-13136
media_subpath: /assets/img/posts/baekjoon-13136/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://www.acmicpc.net/problem/13136)
{: .prompt-info }

---

## 1. 아이디어

CCTV 한 대는 $N \times N$ 크기의 영역을 커버할 수 있다. 대회장의 크기는 입력으로 세로 $R$, 가로 $C$ 순서로 주어지지만 직관적인 설명을 위해 $R$을 가로, $C$를 세로로 두고 서술한다. 따라서 주어진 대회장의 가로에는 $R / N$을 올림 나눗셈한 만큼 배치를 해야 하고, 세로에는 $C / N$을 올림 나눗셈만큼 배치해야 하며 둘의 곱으로 필요한 최소 CCTV 수를 구할 수 있다. 이때 CCTV의 수가 정수 타입 오버플로우가 될 수 있음에 주의해야 한다.

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

        int r = Integer.parseInt(st.nextToken());
        int c = Integer.parseInt(st.nextToken());
        int n = Integer.parseInt(st.nextToken());

        System.out.println((long) ((r + n - 1) / n) * ((c + n - 1) / n));
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);

    long long r, c, n;
    cin >> r >> c >> n;
    cout << ((r + n - 1) / n) * ((c + n - 1) / n);
}
```

---
