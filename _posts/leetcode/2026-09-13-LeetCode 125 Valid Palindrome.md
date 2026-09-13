---
title: "[LeetCode] #125 - Valid Palindrome [Java][C++][Python]"
date: 2026-09-13
categories: [PS, LeetCode]
tags: ["string", "palindrome", "two pointers"]
slug: leetcode-125
media_subpath: /assets/img/posts/leetcode-125/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/valid-palindrome/)
{: .prompt-info }

---

## 1. 아이디어

유효한 팰린드롬인지 판단하는 문제로 문자열 `s`에서 알파벳, 숫자가 아닌 것은 제거하고 전부 소문자로 변환한 문자열에 대해 판단해야 한다. `s`의 양 끝에 포인터를 배치한 후 알파벳, 숫자가 아닌 경우는 무시하며 양 끝 포인터가 가리키는 문자가 일치하는지 비교했다. 알파벳은 대소문자를 구분하지 않으므로 소문자로 변환했고, 두 포인터가 교차할 때까지 지장이 없으면 유효한 팰린드롬이 된다.

---

## 2. 복잡도

| 접근 | 시간   | 공간   |
| ---- | ------ | ------ |
| 풀이 | $O(N)$ | $O(1)$ |

($N$ = `s`의 길이)

---

## 3. 코드

### 풀이 [Java][C++][Python]

```java
class Solution {
    public boolean isPalindrome(String s) {
        int l = 0, r = s.length() - 1;
        while (l < r) {
            while (l < r && !Character.isLetterOrDigit(s.charAt(l))) {
                l++;
            }
            while (l < r && !Character.isLetterOrDigit(s.charAt(r))) {
                r--;
            }

            if (Character.toLowerCase(s.charAt(l)) != Character.toLowerCase(s.charAt(r))) return false;
            l++;
            r--;
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
        int l = 0, r = s.size() - 1;
        while (l < r) {
            while (l < r && !isalnum(s[l])) l++;
            while (l < r && !isalnum(s[r])) r--;

            if (tolower(s[l]) != tolower(s[r])) return false;
            l++;
            r--;
        }

        return true;
    }
};
```

```python
class Solution:
    def isPalindrome(self, s: str) -> bool:
        l, r = 0, len(s) - 1
        while l < r:
            while l < r and not s[l].isalnum():
                l += 1
            while l < r and not s[r].isalnum():
                r -= 1

            if s[l].lower() != s[r].lower():
                return False

            l += 1
            r -= 1

        return True
```

---
