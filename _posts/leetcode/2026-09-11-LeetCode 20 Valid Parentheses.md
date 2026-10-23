---
title: "[LeetCode] #20 - Valid Parentheses [Java][C++][Python]"
date: 2026-09-11
categories: [PS, LeetCode]
tags: ["data structure", "stack"]
slug: leetcode-20
media_subpath: /assets/img/posts/leetcode-20/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/valid-parentheses/)
{: .prompt-info }

---

## 1. 아이디어

세 종류의 괄호로만 이루어진 문자열이 유효한지 판별하는 문제다. 올바른 순서로 닫히려면 닫는 괄호는 아직 닫히지 않은 열린 괄호 중 가장 나중에 열린 것과 짝이어야 한다. 가장 나중에 열린 것부터 꺼내는 구조이므로 열린 괄호는 스택에 넣고, 닫는 괄호가 나오면 맨 위와 종류가 같은지 확인한다. 같으면 꺼내고, 다르거나 스택이 비어 있으면 유효하지 않다. 끝까지 읽은 뒤에도 스택에 열린 괄호가 남아 있다면 닫히지 못한 괄호가 있는 것이므로 이 경우도 유효하지 않다.

---

## 2. 코드

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

닫는 괄호를 키, 짝이 되는 여는 괄호를 값으로 하는 딕셔너리를 두면 괄호 종류별 분기 없이 비교할 수 있다.

---
