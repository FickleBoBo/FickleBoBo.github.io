---
title: "[LeetCode] 9번 - Palindrome Number [Java][C++]"
slug: leetcode-9
date: 2025-12-23
categories: [PS, LeetCode]
tags: [Strings, Math]
toc: true
math: true
---

[문제 링크](https://leetcode.com/problems/palindrome-number/)

---

## 1. 문제 풀이

정수 $x$ 에 대해 팰린드롬이면 `true` 아니면 `false`를 반환하는 문제다. 팰린드롬은 앞에서부터 읽었을 때랑 뒤에서부터 읽었을 때 모두 동일한 문자열로 정수 $x$ 를 문자열로 변환하고 이를 뒤집는 함수를 통해 원본 문자열과 뒤집힌 문자열이 동일한지 여부로 판단해도 되고, $x$ 의 각 자릿수를 저장한 배열을 만들고 배열의 양 끝에서부터 중간까지 각 자리 숫자가 전부 동일한지 판단해도 된다. 또는 $x$ 를 문자열로 받고 양 끝부터 각 문자가 동일한지 비교해봐도 된다.

---

## 2. 코드

### 1. 문자열 [Java]

```java
class Solution {
    public boolean isPalindrome(int x) {
        String str = String.valueOf(x);
        String revStr = new StringBuilder(str).reverse().toString();

        return str.equals(revStr);
    }
}
```

### 2. 문자열 [Java]

```java
class Solution {
    public boolean isPalindrome(int x) {
        String str = String.valueOf(x);

        for (int i = 0; i < str.length() / 2; i++) {
            if (str.charAt(i) != str.charAt(str.length() - 1 - i)) return false;
        }

        return true;
    }
}
```

### 3. 수학 [Java]

$x$ 가 음수면 앞에 마이너스 부호가 있어서 먼저 가치지기를 해줬다.

```java
class Solution {
    public boolean isPalindrome(int x) {
        if (x < 0) return false;

        int[] arr = new int[32];
        int len = 0;
        while (x > 0) {
            arr[len++] = x % 10;
            x /= 10;
        }

        for (int i = 0; i < len / 2; i++) {
            if (arr[i] != arr[len - 1 - i]) return false;
        }

        return true;
    }
}
```

### 4. 문자열 [C++]

```c++
class Solution {
public:
    bool isPalindrome(int x) {
        string s = to_string(x);
        return s == string(s.rbegin(), s.rend());
    }
};
```

### 5. 문자열 [C++]

```c++
class Solution {
public:
    bool isPalindrome(int x) {
        string s = to_string(x);

        for (int i = 0; i < s.size() / 2; i++) {
            if (s[i] != s[s.size() - 1 - i]) return false;
        }

        return true;
    }
};
```

### 6. 수학 [C++]

$x$ 가 음수면 앞에 마이너스 부호가 있어서 먼저 가치지기를 해줬다.

```c++
class Solution {
public:
    bool isPalindrome(int x) {
        if (x < 0) return false;

        vector<int> v;
        while (x > 0) {
            v.push_back(x % 10);
            x /= 10;
        }

        int len = v.size();
        for (int i = 0; i < len / 2; i++) {
            if (v[i] != v[len - 1 - i]) return false;
        }

        return true;
    }
};
```

---
