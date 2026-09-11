---
title: "[LeetCode] #20 - Valid Parentheses [Java][C++][Python]"
date: 2026-09-11
categories: [PS, LeetCode]
tags: ["stack", "data structure"]
slug: leetcode-20
media_subpath: /assets/img/posts/leetcode-20/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/valid-parentheses/)
{: .prompt-info }

---

## 1. 아이디어

소괄호, 중괄호, 대괄호들로 이루어진 문자열 `s`에 대해 유효한 문자열인지 판단하는 문제로 괄호 유효성 검사라는 면에서 스택을 활용하면 해결할 수 있다. 열린 괄호는 스택에 넣고 닫힌 괄호는 스택의 top과 같으면 top을 제거 후 반복, top과 다르거나 스택이 비어있으면 유효하지 않은 괄호열이다.

---

## 2. 복잡도

| 접근 | 시간   | 공간   |
| ---- | ------ | ------ |
| 풀이 | $O(N)$ | $O(N)$ |

($N$ = `s`의 길이)

---

## 3. 코드

### 풀이 [Java][C++][Python]

```java
import java.util.*;

class Solution {
    public boolean isValid(String s) {
        Deque<Character> stack = new ArrayDeque<>();
        for (char c : s.toCharArray()) {
            if (c == '(' || c == '[' || c == '{') {
                stack.push(c);
            } else {
                if (stack.isEmpty()) return false;

                char top = stack.peek();
                if (top == '(' && c == ')') {
                    stack.pop();
                } else if (top == '{' && c == '}') {
                    stack.pop();
                } else if (top == '[' && c == ']') {
                    stack.pop();
                } else {
                    return false;
                }
            }
        }

        return stack.isEmpty();
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

class Solution {
   public:
    bool isValid(string s) {
        stack<char> st;
        for (char c : s) {
            if (c == '(' || c == '[' || c == '{') {
                st.push(c);
            } else {
                if (st.empty()) return false;

                char top = st.top();
                if (top == '(' && c == ')') {
                    st.pop();
                } else if (top == '{' && c == '}') {
                    st.pop();
                } else if (top == '[' && c == ']') {
                    st.pop();
                } else {
                    return false;
                }
            }
        }

        return st.empty();
    }
};
```

```python
class Solution:
    def isValid(self, s: str) -> bool:
        pairs = {")": "(", "}": "{", "]": "["}
        stack = []
        for c in s:
            if c in pairs:
                if not stack or stack.pop() != pairs[c]:
                    return False
            else:
                stack.append(c)

        return not stack
```

---
