---
title: "[LeetCode] 20번 - Valid Parentheses [Java][C++]"
slug: leetcode-20
date: 2026-07-27
categories: [PS, LeetCode]
tags: [data structure, stack]
toc: true
math: true
---

[문제 링크](https://leetcode.com/problems/valid-parentheses/)

---

## 1. 아이디어

유효한 괄호열인지 판단하는 문제로 스택 자료구조를 활용하는 대표적인 문제이다. 열린 괄호가 등장하면 스택에 담고 닫힌 괄호가 등장하면 스택의 top에 위치한 괄호와 짝이 맞는지 판단해서 짝이 맞으면 top에 위치한 괄호를 제거하는 과정을 반복하면 괄호 규칙에 맞는지 판단할 수 있다. 괄호열을 전부 확인한 이후에는 스택에 열린 괄호가 남아 있지 않아야 전체 괄호열에 대해 유효한지 판단할 수 있다.

---

## 2. 복잡도

| 시간복잡도 | 공간복잡도 |
| :--------: | :--------: |
|   $O(N)$   |   $O(N)$   |

> $N$ = 문자열 `s` 길이

---

## 3. 코드

### 풀이 [Java][C++]

```java
import java.util.*;

class Solution {
    public boolean isValid(String s) {
        Deque<Character> stk = new ArrayDeque<>();

        for (char c : s.toCharArray()) {
            if (c == '(' || c == '[' || c == '{') {
                stk.push(c);
            } else {
                if (stk.isEmpty()) return false;

                char x = stk.pop();
                if (c == ')' && x != '(') return false;
                if (c == '}' && x != '{') return false;
                if (c == ']' && x != '[') return false;
            }
        }

        return stk.isEmpty();
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

class Solution {
   public:
    bool isValid(string s) {
        stack<char> stk;

        for (char c : s) {
            if (c == '(' || c == '[' || c == '{') {
                stk.push(c);
            } else {
                if (stk.empty()) return false;

                char x = stk.top();
                stk.pop();

                if (c == ')' && x != '(') return false;
                if (c == '}' && x != '{') return false;
                if (c == ']' && x != '[') return false;
            }
        }

        return stk.empty();
    }
};
```

---
