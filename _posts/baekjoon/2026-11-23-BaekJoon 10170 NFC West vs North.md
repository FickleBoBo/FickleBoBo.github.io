---
title: "[BaekJoon] #10170 - NFC West vs North [Java][C++][Python]"
date: 2026-11-23
categories: [PS, BaekJoon]
tags: ["warm up"]
slug: baekjoon-10170
media_subpath: /assets/img/posts/baekjoon-10170/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://www.acmicpc.net/problem/10170)
{: .prompt-info }

---

## 1. 아이디어

NFC 서부와 북부 디비전의 순위표를 예제 출력과 같은 모양으로 출력한다. 입력이 없어 표를 줄 단위로 그대로 옮기면 되고, 열을 맞추는 공백의 개수와 두 표 사이의 빈 줄까지 예제와 같아야 한다.

---

## 2. 코드

### 풀이 [Java][C++][Python]

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

```python
print("NFC West       W   L  T")
print("-----------------------")
print("Seattle        13  3  0")
print("San Francisco  12  4  0")
print("Arizona        10  6  0")
print("St. Louis      7   9  0")
print()
print("NFC North      W   L  T")
print("-----------------------")
print("Green Bay      8   7  1")
print("Chicago        8   8  0")
print("Detroit        7   9  0")
print("Minnesota      5  10  1")
```

---
