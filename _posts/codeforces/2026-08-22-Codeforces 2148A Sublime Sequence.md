---
title: "[Codeforces] #2148A - Sublime Sequence [Java][C++][Python]"
date: 2026-08-22
categories: [PS, Codeforces]
tags: ["warm up"]
description: "x와 -x를 번갈아 나열한 길이 n 수열의 합을 n의 홀짝만으로 구하는 워밍업 문제."
slug: codeforces-2148a
media_subpath: /assets/img/posts/codeforces-2148a/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://codeforces.com/problemset/problem/2148/A)
{: .prompt-info }

---

## 1. 아이디어

정수 `x`로 시작해 `x`와 `-x`를 번갈아가며 길이 `n`인 수열을 만들 때, 수열 전체의 합을 구하면 되는 문제다. `x`와 `-x`는 짝을 이룰 때마다 서로 상쇄되므로, `n`이 짝수면 정확히 절반씩 상쇄되어 합은 0이고, `n`이 홀수면 상쇄되지 않은 마지막 `x` 하나가 남아 합은 `x`가 된다. 즉 각 테스트 케이스마다 `n`의 홀짝만 판별하면 답이 나온다.

---

## 2. 복잡도

| 접근 | 시간   | 공간   |
| ---- | ------ | ------ |
| 풀이 | $O(T)$ | $O(1)$ |

($T$ = 테스트 케이스의 개수)

---

## 3. 코드

### 풀이 [Java][C++][Python]

```java
import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        int t = Integer.parseInt(br.readLine());
        while (t-- > 0) {
            StringTokenizer st = new StringTokenizer(br.readLine());
            int x = Integer.parseInt(st.nextToken());
            int n = Integer.parseInt(st.nextToken());

            if (n % 2 == 1) {
                System.out.println(x);
            } else {
                System.out.println(0);
            }
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

    int t;
    cin >> t;

    while (t--) {
        int x, n;
        cin >> x >> n;

        if (n % 2) {
            cout << x << '\n';
        } else {
            cout << 0 << '\n';
        }
    }
}
```

```python
import sys

input = sys.stdin.readline

t = int(input())
for _ in range(t):
    x, n = map(int, input().split())
    if n % 2:
        print(x)
    else:
        print(0)
```

---
