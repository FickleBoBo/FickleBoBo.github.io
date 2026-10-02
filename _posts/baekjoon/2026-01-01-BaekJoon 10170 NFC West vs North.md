---
title: "[BaekJoon] #10170 - NFC West vs North [Java][C++]"
date: 2026-01-01
categories: [PS, BaekJoon]
tags: ["warm up"]
slug: baekjoon-10170
media_subpath: /assets/img/posts/baekjoon-10170/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://www.acmicpc.net/problem/10170)
{: .prompt-info }

---

## 1. 아이디어

주어진 양식에 맞춰서 출력만 하면 된다.

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
        System.out.println("NFC West       W   L  T");
        System.out.println("-----------------------");
        System.out.println("Seattle        13  3  0");
        System.out.println("San Francisco  12  4  0");
        System.out.println("Arizona        10  6  0");
        System.out.println("St. Louis      7   9  0");
        System.out.println();
        System.out.println("NFC North      W   L  T");
        System.out.println("-----------------------");
        System.out.println("Green Bay      8   7  1");
        System.out.println("Chicago        8   8  0");
        System.out.println("Detroit        7   9  0");
        System.out.println("Minnesota      5  10  1");
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);

    cout << "NFC West       W   L  T" << '\n';
    cout << "-----------------------" << '\n';
    cout << "Seattle        13  3  0" << '\n';
    cout << "San Francisco  12  4  0" << '\n';
    cout << "Arizona        10  6  0" << '\n';
    cout << "St. Louis      7   9  0" << '\n';
    cout << '\n';
    cout << "NFC North      W   L  T" << '\n';
    cout << "-----------------------" << '\n';
    cout << "Green Bay      8   7  1" << '\n';
    cout << "Chicago        8   8  0" << '\n';
    cout << "Detroit        7   9  0" << '\n';
    cout << "Minnesota      5  10  1" << '\n';
}
```

---
