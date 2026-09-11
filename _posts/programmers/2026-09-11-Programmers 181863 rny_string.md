---
title: "[Programmers] #181863 - rny_string [Java][C++][Python]"
date: 2026-09-11
categories: [PS, Programmers]
tags: ["string"]
slug: programmers-181863
media_subpath: /assets/img/posts/programmers-181863/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://school.programmers.co.kr/learn/courses/30/lessons/181863)
{: .prompt-info }

---

## 1. 아이디어

`rny_string`에서 `m`을 전부 `rn`으로 바꾸면 되는 간단한 문제다.

---

## 2. 복잡도

| 접근 | 시간   | 공간   |
| ---- | ------ | ------ |
| 풀이 | $O(N)$ | $O(N)$ |

($N$ = `rny_string`의 길이)

---

## 3. 코드

### 풀이 [Java][C++][Python]

```java
class Solution {
    public String solution(String rny_string) {
        return rny_string.replace("m", "rn");
    }
}
```

`replace` 메서드를 활용해서 문자열 치환을 했다.

```c++
#include <bits/stdc++.h>
using namespace std;

string solution(string rny_string) {
    string s;
    for (char c : rny_string) {
        if (c == 'm') {
            s += "rn";
        } else {
            s += c;
        }
    }

    return s;
}
```

빈 문자열 `s`를 선언한 후 `rny_string`의 각 문자를 삽입하는데 `m`을 만날 때만 `rn`을 삽입했다.

```python
def solution(rny_string):
    return rny_string.replace("m", "rn")
```

`replace` 함수를 활용해서 문자열 치환을 했다.

---
