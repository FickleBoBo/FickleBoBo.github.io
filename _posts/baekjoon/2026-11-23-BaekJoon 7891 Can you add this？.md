---
title: "[BaekJoon] #7891 - Can you add this? [Java][C++][Python]"
date: 2026-11-23
categories: [PS, BaekJoon]
tags: ["warm up"]
slug: baekjoon-7891
media_subpath: /assets/img/posts/baekjoon-7891/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://www.acmicpc.net/problem/7891)
{: .prompt-info }

---

## 1. 아이디어

각 테스트 케이스에서 두 정수 $x$와 $y$의 합을 출력한다. $x$와 $y$가 $-10^9$ 이상 $10^9$ 이하라 합의 절댓값은 $2 \times 10^9$ 이하인데 32비트 정수는 약 21억까지 담을 수 있어 합이 넘치지 않는다.

---

## 2. 코드

### 풀이 [Java][C++][Python]

```java
import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder sb = new StringBuilder();

        int t = Integer.parseInt(br.readLine());
        while (t-- > 0) {
            StringTokenizer st = new StringTokenizer(br.readLine());
            int x = Integer.parseInt(st.nextToken());
            int y = Integer.parseInt(st.nextToken());
            sb.append(x + y).append("\n");
        }

        System.out.println(sb);
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
        int x, y;
        cin >> x >> y;
        cout << x + y << '\n';
    }
}
```

```python
import sys

input = sys.stdin.readline

t = int(input())
for _ in range(t):
    x, y = map(int, input().split())
    print(x + y)
```

---
