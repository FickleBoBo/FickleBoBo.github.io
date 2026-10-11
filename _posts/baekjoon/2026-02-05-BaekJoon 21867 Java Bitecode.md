---
title: "[BaekJoon] #21867 - Java Bitecode [Java][C++]"
date: 2026-02-05
categories: [PS, BaekJoon]
tags: ["string"]
slug: baekjoon-21867
media_subpath: /assets/img/posts/baekjoon-21867/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://www.acmicpc.net/problem/21867)
{: .prompt-info }

---

## 1. 아이디어

주어진 문자열에서 `J`, `A`, `V`를 뺀 나머지 문자들로 새로운 문자열을 만드는 방식으로 해결할 수 있다.

---

## 2. 복잡도

| 접근 | 시간   | 공간   |
| ---- | ------ | ------ |
| 풀이 | $O(N)$ | $O(N)$ |

($N$ = `s`의 길이)

---

## 3. 코드

### 풀이 [Java][C++]

```java
import java.io.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder sb = new StringBuilder();

        br.readLine();
        String s = br.readLine();

        for (char c : s.toCharArray()) {
            if (c == 'J' || c == 'A' || c == 'V') continue;
            sb.append(c);
        }

        if (sb.length() == 0) {
            System.out.println("nojava");
        } else {
            System.out.println(sb);
        }
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
    string s;
    cin >> n >> s;

    string res;
    for (char c : s) {
        if (c == 'J' || c == 'A' || c == 'V') continue;
        res += c;
    }

    if (res.empty()) {
        cout << "nojava";
    } else {
        cout << res;
    }
}
```

---
