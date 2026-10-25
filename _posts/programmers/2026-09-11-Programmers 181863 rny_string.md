---
title: "[Programmers] #181863 - rny_string [Java][C++][Python]"
date: 2026-09-11
categories: [PS, Programmers]
tags: ["string"]
slug: programmers-181863
media_subpath: /assets/img/posts/programmers-181863/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://school.programmers.co.kr/learn/courses/30/lessons/181863)
{: .prompt-info }

---

## 1. 아이디어

`"m"`을 만날 때마다 `"rn"`으로 바꾸면 되고, `"rn"`에는 `"m"`이 없어서 바꾼 결과를 다시 치환할 일이 없으니 원본을 한 번 훑는 것으로 끝난다.

---

## 2. 코드

### 풀이 [Java][C++][Python]

```java
class Solution {
    public String solution(String rny_string) {
        return rny_string.replace("m", "rn");
    }
}
```

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

`std::string`의 `replace`는 위치와 길이로 구간을 바꾸는 함수라 모든 `"m"`을 한 번에 바꾸지 못해서, 문자를 하나씩 보며 새 문자열에 이어 붙였다.

```python
def solution(rny_string):
    return rny_string.replace("m", "rn")
```

---
