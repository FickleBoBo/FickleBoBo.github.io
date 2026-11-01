---
title: "[LeetCode] #242 - Valid Anagram [Java][C++][Python]"
date: 2026-09-11
categories: [PS, LeetCode]
tags: ["data structure", "hash set/map", "string"]
slug: leetcode-242
media_subpath: /assets/img/posts/leetcode-242/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/valid-anagram/)
{: .prompt-info }

---

## 1. 아이디어

문자열 $t$가 $s$의 글자를 재배열한 것인지 판정하는 문제다. 재배열해서 같아질 수 있다는 것은 글자마다 쓰인 횟수가 같다는 것과 같은 말이므로 글자의 순서는 볼 필요 없이 글자별 횟수만 비교하면 된다. 문자열이 소문자로만 이루어져 글자 종류가 26가지뿐이라 길이 26의 배열을 글자별 횟수로 삼아, $s$의 글자마다 해당 칸을 1 올리고 $t$의 글자마다 1 내렸을 때 모든 칸이 0이면 횟수가 같은 것이다.

이 방법은 글자 종류가 적어 작은 칸 번호로 바꿀 수 있다는 데 기대므로, 지문의 Follow-up처럼 유니코드 글자가 들어오면 칸 대부분이 비는 큰 배열이 필요해진다. 그 방향으로는 등장한 글자만 키로 갖는 맵에 같은 방식으로 세는 방법이 있다.

---

## 2. 코드

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

26칸 배열 대신 `Counter`를 써서 글자별 횟수 비교를 `==` 한 번으로 줄였다.

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
