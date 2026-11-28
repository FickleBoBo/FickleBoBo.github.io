---
title: "[BaekJoon] #13136 - Do Not Touch Anything [Java][C++][Python]"
date: 2026-11-28
categories: [PS, BaekJoon]
tags: ["math"]
slug: baekjoon-13136
media_subpath: /assets/img/posts/baekjoon-13136/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://www.acmicpc.net/problem/13136)
{: .prompt-info }

---

## 1. 아이디어

$R$행 $C$열의 좌석을 한 대가 $N$행 $N$열을 촬영하는 CCTV로 모두 덮을 때 필요한 최소 대수를 구하는 문제다. 행과 열을 $N$칸씩 끊어 구역마다 한 대를 두면 $\lceil R / N \rceil \times \lceil C / N \rceil$대로 모두 덮인다. 이보다 줄일 수도 없다. 1행과 1열부터 $N$칸 간격인 좌석들을 고르면 어느 두 좌석이든 행이나 열의 번호가 $N$ 이상 차이 나는데, 한 대에 찍히는 좌석끼리는 그 차이가 최대 $N - 1$이라 고른 좌석을 둘 이상 찍는 CCTV는 없다. 고른 좌석이 정확히 $\lceil R / N \rceil \times \lceil C / N \rceil$개이므로 CCTV도 그만큼은 필요하다. $R$, $C$가 최대 $10^6$이라 답은 $10^{12}$까지 커질 수 있으므로 64비트 정수에 담아야 한다.

![R = 7, C = 9, N = 3의 좌석을 9개 구역으로 나누고, 1행·1열부터 3칸 간격인 좌석 9개는 어디에 놓은 CCTV든 많아야 하나만 담아 답이 9대임을 보이는 도식](cctv-light.svg){: .light }
![R = 7, C = 9, N = 3의 좌석을 9개 구역으로 나누고, 1행·1열부터 3칸 간격인 좌석 9개는 어디에 놓은 CCTV든 많아야 하나만 담아 답이 9대임을 보이는 도식](cctv-dark.svg){: .dark }

---

## 2. 코드

### 풀이 [Java][C++][Python]

올림한 몫은 `n - 1`을 더한 뒤 나눠, 실수를 거치지 않고 구했다.

```java
import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());

        int r = Integer.parseInt(st.nextToken());
        int c = Integer.parseInt(st.nextToken());
        int n = Integer.parseInt(st.nextToken());
        System.out.println((long) ((r + n - 1) / n) * ((c + n - 1) / n));
    }
}
```

첫 번째 몫을 `long`으로 형변환해 곱셈이 `long`으로 계산되게 했다. 곱한 결과를 형변환하면 이미 `int` 범위를 넘은 뒤다.

```c++
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);

    long long r, c, n;
    cin >> r >> c >> n;
    cout << ((r + n - 1) / n) * ((c + n - 1) / n);
}
```

```python
import sys

input = sys.stdin.readline

r, c, n = map(int, input().split())
print(((r + n - 1) // n) * ((c + n - 1) // n))
```

---
