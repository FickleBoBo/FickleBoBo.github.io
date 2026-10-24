---
title: "[Programmers] #181933 - flag에 따라 다른 값 반환하기 [Java][C++][Python]"
date: 2026-08-23
categories: [PS, Programmers]
tags: ["warm up"]
slug: programmers-181933
media_subpath: /assets/img/posts/programmers-181933/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://school.programmers.co.kr/learn/courses/30/lessons/181933)
{: .prompt-info }

---

## 1. 아이디어

`flag`가 참이면 두 수의 합을, 거짓이면 차를 반환한다.

---

## 2. 코드

### 풀이 [Java][C++][Python]

```java
class Solution {
    public int solution(int a, int b, boolean flag) {
        return flag ? a + b : a - b;
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

int solution(int a, int b, bool flag) {
    return flag ? a + b : a - b;
}
```

```python
def solution(a, b, flag):
    return a + b if flag else a - b
```

---
