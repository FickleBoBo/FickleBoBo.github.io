---
title: "[BaekJoon] #23234 - The World Responds [Java][C++]"
date: 2026-01-01
categories: [PS, BaekJoon]
tags: ["warm up"]
slug: baekjoon-23234
media_subpath: /assets/img/posts/baekjoon-23234/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://www.acmicpc.net/problem/23234)
{: .prompt-info }

---

## 1. 아이디어

`The world says hello!`를 출력만 하면 된다.

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
        System.out.println("The world says hello!");
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);

    cout << "The world says hello!";
}
```

---
