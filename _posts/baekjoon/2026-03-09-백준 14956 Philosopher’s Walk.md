---
title: "[BaekJoon] 14956번 - Philosopher’s Walk [Java][C++]"
slug: baekjoon-14956
date: 2026-03-09
categories: [PS, BaekJoon]
tags: [Unlinked]
toc: true
math: true
---

[문제 링크](https://www.acmicpc.net/problem/14956)

---

## 1. 아이디어

<br>

철학자의 산책로 상에서 철학자의 위치를 구하는 문제로 산책로는 힐베르트 곡선의 모양을 하고 있다. 비슷한 구조가 반복되는 것 같다는 점에서 분할 정복을 활용해서 해결했는데 크기별 산책로는 아래와 같은 관계를 보이고 있다.

<br>

0번 영역의 산책로는 $W_i$ 산책로에서 $y = x$ 에 대칭한 형태이며, 1번, 2번 영역의 산책로는 $W_i$ 산책로에서 평행 이동만 된 형태이다. 3번 산책로는 $y = -x$ 에 대칭 후 평행 이동까지 한 형태이다.

![](/assets/posts/baekjoon-14956/photo01.drawio.svg)

<br>

재귀의 경우 현재 바라보는 산책로 정사각형 한 변의 길이와 걸음 수를 받아서 해당하는 좌표를 반환하는 방식으로 구성했다. $W_{i + 1}$ 산책로를 기준으로 보면 걸음수를 기준으로 0번 영역에 속했을 경우 $W_i$ 산책로에서 구한 좌표를 $y = x$ 에 대해 반전시키면 $W_{i + 1}$ 산책로에서의 좌표가 된다. 1번, 2번 영역에 속했을 경우에는 $W_i$ 산책로에서 구한 좌표를 평행 이동만 시키면 $W_{i + 1}$ 산책로에서의 좌표가 된다. 3번 영역 역시 마찬가지며 이런 재귀적인 구조로 하위 산책로에서의 좌표를 현재 산책로에 맞춰 변환하는 것을 반복하는 과정으로 구했다.

---

## 2. 코드

<br>

### 1. 풀이 [Java]

```java
import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());

        int n = Integer.parseInt(st.nextToken());
        int m = Integer.parseInt(st.nextToken());

        int[] pos = dfs(n, m);
        System.out.println(pos[0] + " " + pos[1]);
    }

    static int[] dfs(int n, int m) {
        if (n == 1) return new int[]{1, 1};

        int len = n / 2;
        int area = len * len;

        int q = (m - 1) / area;
        int nxt = (m - 1) % area + 1;

        int[] p = dfs(n / 2, nxt);
        int x = p[0];
        int y = p[1];

        if (q == 0) return new int[]{y, x};
        if (q == 1) return new int[]{x, y + len};
        if (q == 2) return new int[]{x + len, y + len};
        return new int[]{2 * len - y + 1, len - x + 1};
    }
}
```

<br>

### 2. 풀이 [C++]

```c++
#include <bits/stdc++.h>
using namespace std;

pair<int, int> dfs(int n, int m) {
    if (n == 1) return {1, 1};

    int len = n / 2;
    int area = len * len;

    int q = (m - 1) / area;
    int nxt = (m - 1) % area + 1;

    auto [x, y] = dfs(n / 2, nxt);

    if (q == 0) return {y, x};
    if (q == 1) return {x, y + len};
    if (q == 2) return {x + len, y + len};
    return {2 * len - y + 1, len - x + 1};
}

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);

    int n, m;
    cin >> n >> m;

    auto [x, y] = dfs(n, m);
    cout << x << ' ' << y;
}
```

---

## 3. 디버깅

<br>

절대 좌표를 설정하고 이를 이동시키는 방향으로 설계했는데 분할 정복 과정에서 좌표계 처리가 너무 까다로웠다. 상대 좌표를 반환하는 방식으로 하니 깔끔하게 해결되는 것 같다.

---

## 4. 참고

<br>

없음.

---
