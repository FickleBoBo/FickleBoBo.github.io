---
title: "[LeetCode] #242 - Valid Anagram [Java][C++][Python]"
date: 2026-09-11
categories: [PS, LeetCode]
tags: ["data structure", "hash table", "string"]
slug: leetcode-242
media_subpath: /assets/img/posts/leetcode-242/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/valid-anagram/)
{: .prompt-info }

---

## 1. 아이디어

두 문자열 `s`와 `t`가 애너그램인지 판단하는 문제로 애너그램은 각 문자열을 이루는 개별 문자의 종류와 수가 모두 일치하는 경우다. 두 문자열이 모두 알파벳 소문자로 이루어져 있으므로 26칸의 카운팅 배열을 통해 `s`의 문자는 세고, `t`의 문자는 빼면 카운팅 배열의 모든 원소가 0인지 여부로 애너그램을 판별할 수 있다.

Follow up은 유니코드 문자들에 대해 애너그램 여부를 판단하는 상황이다. 유니코드는 범위가 훨씬 넓으므로 이 경우 카운팅 맵을 활용해 카운팅을 하면 카운팅 맵의 모든 값들이 0인지 여부로 애너그램을 판단할 수 있다.

---

## 2. 복잡도

| 접근        | 시간       | 공간       |
| ----------- | ---------- | ---------- |
| 카운팅 배열 | $O(N + M)$ | $O(1)$     |
| 카운팅 맵   | $O(N + M)$ | $O(N + M)$ |

($N$ = `s`의 길이, $M$ = `t`의 길이. Python은 `Counter`가 해시맵이라 공간 $O(N + M)$)

---

## 3. 코드

### 풀이 1: 카운팅 배열 [Java][C++][Python]

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
        vector<int> cnt(26);
        for (char c : s) cnt[c - 'a']++;
        for (char c : t) cnt[c - 'a']--;

        for (int x : cnt) {
            if (x != 0) return false;
        }

        return true;
    }
};
```

```python
from collections import Counter


class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        return Counter(s) == Counter(t)
```

---

### 풀이 2: 카운팅 맵 [Java][C++]

```java
import java.util.*;

class Solution {
    public boolean isAnagram(String s, String t) {
        Map<Character, Integer> cnt = new HashMap<>();
        for (char c : s.toCharArray()) {
            cnt.put(c, cnt.getOrDefault(c, 0) + 1);
        }
        for (char c : t.toCharArray()) {
            cnt.put(c, cnt.getOrDefault(c, 0) - 1);
        }

        for (Map.Entry<Character, Integer> e : cnt.entrySet()) {
            if (e.getValue() != 0) return false;
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
        unordered_map<char, int> cnt;
        for (char c : s) cnt[c]++;
        for (char c : t) cnt[c]--;

        for (auto [_, v] : cnt) {
            if (v != 0) return false;
        }

        return true;
    }
};
```

---
