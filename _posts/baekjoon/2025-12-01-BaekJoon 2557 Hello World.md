---
title: "[BaekJoon] #2557 - Hello World [Java][C++]"
date: 2025-12-01
categories: [PS, BaekJoon]
tags: ["warm up"]
slug: baekjoon-2557
media_subpath: /assets/img/posts/baekjoon-2557/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://www.acmicpc.net/problem/2557)
{: .prompt-info }

---

## 1. 아이디어

`Hello World!`를 출력하면 된다.

---

## 2. 복잡도

| 접근 | 시간   | 공간   |
| ---- | ------ | ------ |
| 풀이 | $O(1)$ | $O(1)$ |

---

## 3. 코드

### 풀이 [Java][C++]

```java
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello World!");
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);

    cout << "Hello World!";
}
```

---
