---
title: "[BaekJoon] 10170번 - NFC West vs North [Java][C++]"
slug: baekjoon-10170
date: 2026-01-01
categories: [PS, BaekJoon]
tags: [Warm Up]
toc: true
math: true
---

[문제 링크](https://www.acmicpc.net/problem/10170)

---

## 1. 문제 풀이

<br>

주어진 양식에 맞춰서 출력만 하면 된다.

---

## 2. 코드

<br>

### 1. 풀이 [Java]

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

<br>

### 2. 풀이 [C++]

```c++
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

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
