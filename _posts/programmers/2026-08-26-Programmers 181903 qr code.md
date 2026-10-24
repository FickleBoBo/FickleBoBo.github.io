---
title: "[Programmers] #181903 - qr code [Java][C++][Python]"
date: 2026-08-26
categories: [PS, Programmers]
tags: ["string"]
slug: programmers-181903
media_subpath: /assets/img/posts/programmers-181903/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://school.programmers.co.kr/learn/courses/30/lessons/181903)
{: .prompt-info }

---

## 1. 아이디어

인덱스를 $q$로 나눈 나머지가 $r$인 위치의 글자를 이어 붙이는 문제다. 그런 위치는 $r$, $r + q$, $r + 2q$, ...이다. $r < q$이므로 $r$이 그중 가장 작고, `code`의 길이보다도 작아 시작 인덱스가 문자열 안에 있다. 따라서 $r$부터 $q$씩 건너뛰며 읽으면 된다.

---

## 2. 코드

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
