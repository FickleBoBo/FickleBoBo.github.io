---
title: "[Programmers] #181933 - flag에 따라 다른 값 반환하기 [Java][C++][Python]"
date: 2026-08-23
categories: [PS, Programmers]
tags: ["warm up"]
slug: programmers-181933
media_subpath: /assets/img/posts/programmers-181933/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://school.programmers.co.kr/learn/courses/30/lessons/181933)
{: .prompt-info }

---

## 1. 아이디어

정수 `a`, `b`와 boolean `flag`가 주어질 때, `flag`가 `true`면 `a + b`를, `false`면 `a - b`를 반환하면 되는 문제다.

---

## 2. 복잡도

| 접근 | 시간   | 공간   |
| ---- | ------ | ------ |
| 풀이 | $O(1)$ | $O(1)$ |

---

## 3. 코드

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
