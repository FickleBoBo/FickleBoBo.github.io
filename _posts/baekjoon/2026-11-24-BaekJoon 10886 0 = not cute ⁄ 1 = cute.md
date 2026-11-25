---
title: "[BaekJoon] #10886 - 0 = not cute / 1 = cute [Java][Python]"
date: 2026-11-24
categories: [PS, BaekJoon]
tags: ["warm up"]
slug: baekjoon-10886
media_subpath: /assets/img/posts/baekjoon-10886/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://www.acmicpc.net/problem/10886)
{: .prompt-info }

---

## 1. 아이디어

의견이 `0`인 사람과 `1`인 사람 중 더 많은 쪽을 고르는 문제로, 설문에 참여한 인원 $N$이 홀수라 동수가 될 수 없어 다수결이 항상 정해진다.

---

## 2. 코드

### 풀이 [Java][Python]

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

```python
import sys

input = sys.stdin.readline

n = int(input())
cnt = 0

for _ in range(n):
    x = int(input())
    if x == 0:
        cnt += 1
    else:
        cnt -= 1

if cnt > 0:
    print("Junhee is not cute!")
else:
    print("Junhee is cute!")
```

---
