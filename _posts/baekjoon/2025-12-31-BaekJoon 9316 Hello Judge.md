---
title: "[BaekJoon] #9316 - Hello Judge [Java][C++]"
date: 2025-12-31
categories: [PS, BaekJoon]
tags: ["warm up"]
slug: baekjoon-9316
media_subpath: /assets/img/posts/baekjoon-9316/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://www.acmicpc.net/problem/9316)
{: .prompt-info }

---

## 1. 아이디어

반복문을 활용해서 각 줄별로 양식에 맞게 출력하면 된다.

---

## 2. 복잡도

| 접근 | 시간   | 공간   |
| ---- | ------ | ------ |
| 풀이 | $O(N)$ | $O(1)$ |

($N$ = 입력값 `n`)

---

## 3. 코드

### 풀이 [Java][C++]

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

---
