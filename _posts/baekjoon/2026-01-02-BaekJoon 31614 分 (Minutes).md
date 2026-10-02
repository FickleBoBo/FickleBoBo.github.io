---
title: "[BaekJoon] #31614 - 分 (Minutes) [Java][C++]"
date: 2026-01-02
categories: [PS, BaekJoon]
tags: ["warm up"]
slug: baekjoon-31614
media_subpath: /assets/img/posts/baekjoon-31614/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://www.acmicpc.net/problem/31614)
{: .prompt-info }

---

## 1. 아이디어

$H$시간 $M$분은 $H \times 60 + M$분이다.

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

        int h = Integer.parseInt(br.readLine());
        int m = Integer.parseInt(br.readLine());
        System.out.println(h * 60 + m);
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);

    int h, m;
    cin >> h >> m;
    cout << h * 60 + m;
}
```

---
