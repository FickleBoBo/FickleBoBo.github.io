---
title: "[BaekJoon] #31611 - 火曜日 (Tuesday) [Java][C++]"
date: 2026-01-03
categories: [PS, BaekJoon]
tags: ["warm up"]
slug: baekjoon-31611
media_subpath: /assets/img/posts/baekjoon-31611/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://www.acmicpc.net/problem/31611)
{: .prompt-info }

---

## 1. 아이디어

오늘이 일요일일 때, $X$일 후가 화요일인지 판단하는 문제로 7일 단위로 다시 일요일이 되므로 $X$를 7로 나눈 나머지가 2면 화요일이다.

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

        int x = Integer.parseInt(br.readLine());
        System.out.println(x % 7 == 2 ? 1 : 0);
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);

    int x;
    cin >> x;
    cout << (x % 7 == 2);
}
```

---
