---
title: "[BaekJoon] #9316 - Hello Judge [Java][C++][Python]"
date: 2026-11-23
categories: [PS, BaekJoon]
tags: ["warm up"]
slug: baekjoon-9316
media_subpath: /assets/img/posts/baekjoon-9316/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://www.acmicpc.net/problem/9316)
{: .prompt-info }

---

## 1. 아이디어

$N$개의 줄에 걸쳐 $i$번째 줄에는 `Hello World, Judge i!`의 `i` 자리에 줄 번호를 넣어 출력한다. 줄 번호는 예제처럼 1부터 센다.

---

## 2. 코드

### 풀이 [Java][C++][Python]

```java
import java.io.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder sb = new StringBuilder();

        int n = Integer.parseInt(br.readLine());
        for (int i = 1; i <= n; i++) {
            sb.append("Hello World, Judge ").append(i).append("!\n");
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

    int n;
    cin >> n;

    for (int i = 1; i <= n; i++) {
        cout << "Hello World, Judge " << i << '!' << '\n';
    }
}
```

```python
import sys

input = sys.stdin.readline

n = int(input())
for i in range(1, n + 1):
    print(f"Hello World, Judge {i}!")
```

---
