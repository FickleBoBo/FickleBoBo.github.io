---
title: "[LeetCode] #9 - Palindrome Number [Java][C++][Python]"
date: 2026-11-14
categories: [PS, LeetCode]
tags: ["string", "palindrome"]
slug: leetcode-9
media_subpath: /assets/img/posts/leetcode-9/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/palindrome-number/)
{: .prompt-info }

---

## 1. 아이디어

정수가 회문인지, 즉 문자열로 바꿨을 때 앞뒤로 똑같이 읽히는지 보는 문제로, 문자열을 뒤집어 원래와 같은지 비교하면 된다.

지문의 Follow-up은 문자열로 바꾸지 않고 푸는 것을 묻고, 절반 뒤집기가 그것에 맞춘 풀이이다. 수 전체를 뒤집으면 2,147,483,647이 7,463,847,412가 되듯 뒤집은 값이 32비트 범위를 넘을 수 있어서 뒤 절반만 뒤집는다. 낮은 자리를 하나씩 떼어 뒤집은 수에 붙이는 일을 뒤집은 수가 남은 수 이상이 될 때까지 되풀이하는데, 회문이면 이때 남은 수가 앞 절반이고 뒤집은 수가 뒤 절반이라 둘이 같고(자릿수가 홀수이면 가운데 자리가 뒤집은 수 쪽에 들어가므로 뒤집은 수를 10으로 나눈 몫과 같다), 회문이 아니면 어디서 멈추든 둘이 같지 않다.

음수는 `-` 때문에, 끝자리가 0인 수(0은 제외)는 앞자리가 0일 수 없어서 회문이 될 수 없으므로 처음에 거짓으로 처리한다. 끝자리 0을 거르지 않으면 입력 10에서 반복이 끝난 뒤 남은 수 0과 뒤집은 수 1을 10으로 나눈 몫 0이 같아져 참이 되어 버린다.

---

## 2. 코드

### 풀이 1: 문자열 변환 [Java][C++][Python]

```java
class Solution {
    public boolean isPalindrome(int x) {
        String s = String.valueOf(x);
        return s.equals(new StringBuilder(s).reverse().toString());
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

class Solution {
   public:
    bool isPalindrome(int x) {
        string s = to_string(x);
        return s == string(s.rbegin(), s.rend());
    }
};
```

```python
class Solution:
    def isPalindrome(self, x: int) -> bool:
        s = str(x)
        return s == s[::-1]
```

---

### 풀이 2: 절반 뒤집기 [Java][C++][Python]

```java
class Solution {
    public boolean isPalindrome(int x) {
        if (x < 0 || (x != 0 && x % 10 == 0)) return false;

        int rev = 0;
        while (x > rev) {
            rev = rev * 10 + x % 10;
            x /= 10;
        }

        return x == rev || x == rev / 10;
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

class Solution {
   public:
    bool isPalindrome(int x) {
        if (x < 0 || (x != 0 && x % 10 == 0)) return false;

        int rev = 0;
        while (x > rev) {
            rev = rev * 10 + x % 10;
            x /= 10;
        }

        return x == rev || x == rev / 10;
    }
};
```

```python
class Solution:
    def isPalindrome(self, x: int) -> bool:
        if x < 0 or (x != 0 and x % 10 == 0):
            return False

        rev = 0
        while x > rev:
            rev = rev * 10 + x % 10
            x //= 10

        return x == rev or x == rev // 10
```

---
