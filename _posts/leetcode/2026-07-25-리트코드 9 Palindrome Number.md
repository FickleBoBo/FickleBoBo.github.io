---
title: "[LeetCode] 9번 - Palindrome Number [Java][C++]"
slug: leetcode-9
date: 2026-07-25
categories: [PS, LeetCode]
tags: [string, palindrome]
toc: true
math: true
---

[문제 링크](https://leetcode.com/problems/palindrome-number/)

---

## 1. 아이디어

정수 `x`가 팰린드롬이면 `true`를 아니면 `false`를 반환하는 문제로 정수의 각 자릿수를 확인해서 비교하는 방식으로 해결해도 되지만 더 간단한 방법인 정수 `x`를 문자열로 변환한 후 팰린드롬인지 확인하는 방식으로 해결했다. 문자열로 변환한 후 이를 뒤집은 문자열과 기존 문자열이 일치하는지 여부로 팰린드롬 여부를 판단할 수 있다. `x`의 경우 음수 입력도 들어올 수 있는데 이 경우 `-` 기호로 인해 항상 팰린드롬이 아닌 것 역시 잘 판단할 수 있다.

---

## 2. 복잡도

| 시간복잡도  | 공간복잡도  |
| :---------: | :---------: |
| $O(\log x)$ | $O(\log x)$ |

---

## 3. 코드

### 풀이 [Java][C++]

`StringBuilder`의 `reverse` 메서드를 활용하면 간단하게 구현할 수 있다.

```java
class Solution {
    public boolean isPalindrome(int x) {
        String str = Integer.toString(x);
        String rev = new StringBuilder(str).reverse().toString();

        return str.equals(rev);
    }
}
```

`string`의 범위 생성자와 역방향 이터레이터를 활용하면 간단하게 구현할 수 있다.

```c++
#include <bits/stdc++.h>
using namespace std;

class Solution {
   public:
    bool isPalindrome(int x) {
        string str = to_string(x);
        string rev(str.rbegin(), str.rend());

        return str == rev;
    }
};
```

---
