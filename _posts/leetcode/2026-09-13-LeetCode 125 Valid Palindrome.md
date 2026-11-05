---
title: "[LeetCode] #125 - Valid Palindrome [Java][C++][Python]"
date: 2026-09-13
categories: [PS, LeetCode]
tags: ["string", "palindrome", "two pointers"]
slug: leetcode-125
media_subpath: /assets/img/posts/leetcode-125/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/valid-palindrome/)
{: .prompt-info }

---

## 1. 아이디어

문자열에서 알파벳과 숫자만 남기고 대소문자를 무시했을 때 앞뒤로 읽어도 같은지 판정하는 문제다. 회문은 양 끝에서 같은 거리에 있는 글자끼리 모두 같다는 뜻이므로 양 끝에서 안쪽으로 좁혀 오며 마주 보는 글자를 비교하면 되고, 알파벳과 숫자가 아닌 글자는 비교 대상이 아니므로 문자열을 따로 정리하지 않고 포인터가 그런 글자를 만날 때 건너뛰게 한다.

건너뛰고 나면 두 포인터가 서로 다른 위치에 있을 때는 남겨야 할 글자 중 마주 보는 두 글자를 가리키므로 이 둘을 비교하고, 같은 위치에서 만나면 비교할 쌍이 더 없으므로 그때까지 어긋난 쌍이 하나도 없었다면 회문이다. 건너뛰는 반복에도 두 포인터가 교차하지 않는다는 조건을 함께 걸어야 하는데, 그렇지 않으면 알파벳과 숫자가 하나도 없는 입력에서 포인터가 문자열 밖으로 나간다.

---

## 2. 코드

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
