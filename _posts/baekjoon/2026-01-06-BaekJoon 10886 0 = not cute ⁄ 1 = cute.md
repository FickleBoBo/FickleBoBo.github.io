---
title: "[BaekJoon] #10886 - 0 = not cute / 1 = cute [Java][C++]"
date: 2026-01-06
categories: [PS, BaekJoon]
tags: ["warm up"]
slug: baekjoon-10886
media_subpath: /assets/img/posts/baekjoon-10886/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://www.acmicpc.net/problem/10886)
{: .prompt-info }

---

## 1. 아이디어

`0`과 `1`의 등장 횟수를 비교만 하면 되는 문제로 `0`의 개수에서 `1`의 개수를 뺀 것이 양수인지 음수인지 판단하는 방식으로 해결했다.

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

        int n = Integer.parseInt(br.readLine());
        int cnt = 0;

        while (n-- > 0) {
            int x = Integer.parseInt(br.readLine());

            if (x == 0) {
                cnt++;
            } else {
                cnt--;
            }
        }

        if (cnt > 0) {
            System.out.println("Junhee is not cute!");
        } else {
            System.out.println("Junhee is cute!");
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
    cin >> n;

    int cnt = 0;

    while (n--) {
        int x;
        cin >> x;

        if (x == 0) {
            cnt++;
        } else {
            cnt--;
        }
    }

    if (cnt > 0) {
        cout << "Junhee is not cute!";
    } else {
        cout << "Junhee is cute!";
    }
}
```

---
