---
title: "[Programmers] #181903 - qr code [Java][C++][Python]"
date: 2026-08-26
categories: [PS, Programmers]
tags: ["string"]
description: "인덱스를 q로 나눈 나머지가 r인 위치의 문자를 앞에서부터 이어 붙이는 문제."
slug: programmers-181903
media_subpath: /assets/img/posts/programmers-181903/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://school.programmers.co.kr/learn/courses/30/lessons/181903)
{: .prompt-info }

---

## 1. 아이디어

인덱스를 `q`로 나눈 나머지가 `r`인 위치는 제약 `0 ≤ r < q` 덕분에 `r`, `r + q`, `r + 2q`, ... 순서로 나타난다. 시작 인덱스 `r`에서 출발해 `q`씩 증가시키며 문자열 끝까지 문자를 모아 이어 붙이면 된다.

---

## 2. 복잡도

| 접근 | 시간   | 공간   |
| ---- | ------ | ------ |
| 풀이 | $O(N)$ | $O(N)$ |

($N$ = `code`의 길이. 결과 문자열의 길이가 최대 $N$까지 커질 수 있다)

---

## 3. 코드

### 풀이 [Java][C++][Python]

```java
class Solution {
    public String solution(int q, int r, String code) {
        StringBuilder sb = new StringBuilder();
        for (int i = r; i < code.length(); i += q) {
            sb.append(code.charAt(i));
        }

        return sb.toString();
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

string solution(int q, int r, string code) {
    string s;
    for (int i = r; i < code.size(); i += q) {
        s += code[i];
    }

    return s;
}
```

```python
def solution(q, r, code):
    return code[r::q]
```

---
