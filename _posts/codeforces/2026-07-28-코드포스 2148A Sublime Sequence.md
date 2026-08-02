---
title: "[Codeforces] 2148A - Sublime Sequence [Java][C++]"
slug: codeforces-2148a
date: 2026-07-28
categories: [PS, Codeforces]
tags: [ad hoc, math]
toc: true
math: true
---

[문제 링크](https://codeforces.com/problemset/problem/2148/A)

---

## 1. 아이디어

`x`, `-x`, `x`, ... 와 같이 `x`의 부호가 뒤바뀌며 `n`번 반복되는 수열의 합을 구하는 문제로 첫 항부터 두 항씩 묶어보면 두 항의 합이 0이 된다는 점에서 `n`이 짝수이면 모든 항이 두 항씩 짝이 묶이므로 수열의 합은 `0`이 되며, `n`이 홀수이면 가장 마지막 항을 제외한 모든 항이 두 항씩 짝이 묶이고 가장 마지막 항은 `x`이므로 수열의 합은 `x`가 된다.

---

## 2. 복잡도

| 시간복잡도 | 공간복잡도 |
| :--------: | :--------: |
|   $O(1)$   |   $O(1)$   |

---

## 3. 코드

### 풀이 [Java][C++]

```java
import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st;

        int t = Integer.parseInt(br.readLine());
        while (t-- > 0) {
            st = new StringTokenizer(br.readLine());
            int x = Integer.parseInt(st.nextToken());
            int n = Integer.parseInt(st.nextToken());

            if (n % 2 == 0) {
                System.out.println(0);
            } else {
                System.out.println(x);
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

        if (n % 2 == 0) {
            cout << 0 << '\n';
        } else {
            cout << x << '\n';
        }
    }
}
```

---
