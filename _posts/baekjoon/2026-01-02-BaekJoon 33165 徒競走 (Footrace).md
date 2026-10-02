---
title: "[BaekJoon] #33165 - 徒競走 (Footrace) [Java][C++]"
date: 2026-01-02
categories: [PS, BaekJoon]
tags: ["warm up"]
slug: baekjoon-33165
media_subpath: /assets/img/posts/baekjoon-33165/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://www.acmicpc.net/problem/33165)
{: .prompt-info }

---

## 1. 아이디어

1초에 $V$미터를 갈 수 있으니, $T$초 동안은 $V \times T$미터를 갈 수 있다.

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

        int t = Integer.parseInt(br.readLine());
        int v = Integer.parseInt(br.readLine());
        System.out.println(t * v);
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);

    int t, v;
    cin >> t >> v;
    cout << t * v;
}
```

---
