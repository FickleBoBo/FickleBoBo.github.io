---
title: "[LeetCode] 125번 - Valid Palindrome [Java][C++]"
slug: leetcode-125
date: 2026-07-28
categories: [PS, LeetCode]
tags: [string, palindrome, two pointers]
toc: true
math: true
---

[문제 링크](https://leetcode.com/problems/valid-palindrome/)

---

## 1. 아이디어

주어진 문자열이 팰린드롬인지 판단하는 문제로 이때 알파벳이나 숫자가 아닌 문자는 제거하고 알파벳은 소문자로 치환한 후 팰린드롬이 되는지 판단하는 문제다. 해당 문제는 투 포인터를 활용하면 해결할 수 있는데 주어진 문자열의 양 끝에서부터 서로 교차하는 방향으로 포인터를 진행시키는데 알파벳이나 숫자가 아닌 문자는 건너뛰고 알파벳 대문자는 소문자로 변환한 후 두 포인터가 가리키는 문자가 일치하면 각 포인터를 서로를 향하는 방향으로 한 칸 이동시키는 과정을 두 포인터가 교차할 때까지 반복하여 두 포인터가 교차하면 팰린드롬이 됨을 알 수 있다.

---

## 2. 복잡도

| 시간복잡도 | 공간복잡도 |
| :--------: | :--------: |
|   $O(N)$   |   $O(1)$   |

> $N$ = 문자열 `s` 길이

---

## 3. 코드

### 풀이 [Java][C++]

```java
class Solution {
    public boolean isPalindrome(String s) {
        int left = 0;
        int right = s.length() - 1;

        while (left < right) {
            char l = s.charAt(left);
            if (!('0' <= l && l <= '9' || 'a' <= l && l <= 'z' || 'A' <= l && l <= 'Z')) {
                left++;
                continue;
            }

            char r = s.charAt(right);
            if (!('0' <= r && r <= '9' || 'a' <= r && r <= 'z' || 'A' <= r && r <= 'Z')) {
                right--;
                continue;
            }

            if (Character.toLowerCase(l) != Character.toLowerCase(r)) return false;
            left++;
            right--;
        }

        return true;
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

class Solution {
   public:
    bool isPalindrome(string s) {
        int left = 0;
        int right = s.size() - 1;

        while (left < right) {
            char l = s[left];
            if (!('0' <= l && l <= '9' || 'a' <= l && l <= 'z' || 'A' <= l && l <= 'Z')) {
                left++;
                continue;
            }

            char r = s[right];
            if (!('0' <= r && r <= '9' || 'a' <= r && r <= 'z' || 'A' <= r && r <= 'Z')) {
                right--;
                continue;
            }

            if (tolower(l) != tolower(r)) return false;
            left++;
            right--;
        }

        return true;
    }
};
```

---
