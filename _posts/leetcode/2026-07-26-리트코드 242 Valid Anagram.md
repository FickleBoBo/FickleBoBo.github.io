---
title: "[LeetCode] 242번 - Valid Anagram [Java][C++]"
slug: leetcode-242
date: 2026-07-26
categories: [PS, LeetCode]
tags: [string, anagram]
toc: true
math: true
---

[문제 링크](https://leetcode.com/problems/valid-anagram/)

---

## 1. 아이디어

문자열 `s`와 `t`에 대해 `t`가 `s`의 애너그램이면 `true`, 아니면 `false`를 반환하는 문제다. `s`와 `t` 모두 알파벳 소문자로만 이루어져 있으므로 카운팅 배열을 활용해 `s`에 등장한 알파벳을 카운팅 배열에서 더해주고, `t`에 등장한 알파벳을 카운팅 배열에서 빼주어서 최종적으로 카운팅 배열이 모두 0으로 이루어져 있으면 애너그램 관계라는 점을 활용하면 해결할 수 있다.

---

## 2. 복잡도

### 1. 카운팅 배열

| 시간복잡도 | 공간복잡도 |
| :--------: | :--------: |
|   $O(N)$   |   $O(1)$   |

> $N$ = 문자열 `s`·`t`의 길이

### 2. 정렬

|  시간복잡도   | 공간복잡도 |
| :-----------: | :--------: |
| $O(N \log N)$ |   $O(1)$   |

> $N$ = 문자열 `s`·`t`의 길이

---

## 3. 코드

### 1. 카운팅 배열 [Java][C++]

```java
class Solution {
    public boolean isAnagram(String s, String t) {
        int[] cnt = new int[26];

        for (char c : s.toCharArray()) {
            cnt[c - 'a']++;
        }
        for (char c : t.toCharArray()) {
            cnt[c - 'a']--;
        }

        for (int x : cnt) {
            if (x != 0) return false;
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
    bool isAnagram(string s, string t) {
        int cnt[26] = {};

        for (char c : s) cnt[c - 'a']++;
        for (char c : t) cnt[c - 'a']--;

        for (int i = 0; i < 26; i++) {
            if (cnt[i] != 0) return false;
        }

        return true;
    }
};
```

### 2. 정렬 [C++]

cpp에서 문자열을 바로 정렬할 수 있는걸 활용해 카운팅 배열없이도 간단하게 해결할 수 있다.

```c++
#include <bits/stdc++.h>
using namespace std;

class Solution {
   public:
    bool isAnagram(string s, string t) {
        sort(s.begin(), s.end());
        sort(t.begin(), t.end());
        return s == t;
    }
};
```

---
