---
title: "[LeetCode] #49 - Group Anagrams [Java][C++][Python]"
date: 2026-09-20
categories: [PS, LeetCode]
tags: ["data structure", "hash set/map", "sorting", "string"]
slug: leetcode-49
media_subpath: /assets/img/posts/leetcode-49/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/group-anagrams/)
{: .prompt-info }

---

## 1. 아이디어

서로 애너그램인 문자열끼리 묶는 문제다. 두 문자열이 애너그램이라는 것은 각 글자가 쓰인 횟수가 같다는 뜻이고, 글자를 정렬하면 글자 구성이 같은 문자열은 항상 같은 문자열이, 구성이 다른 문자열은 다른 문자열이 된다. 따라서 정렬한 문자열이 같은지가 애너그램 여부의 판정이 되고, 정렬한 문자열을 키로 해시맵에 문자열들을 모으면 같은 키에 모인 것이 곧 한 그룹이다. 문자열의 길이가 100 이하라 문자열마다 정렬해 키를 만들어도 비용이 작다.

---

## 2. 코드

### 풀이 [Java][C++][Python]

```java
import java.util.*;

class Solution {
    public List<List<String>> groupAnagrams(String[] strs) {
        Map<String, List<String>> map = new HashMap<>();
        for (String s : strs) {
            map.computeIfAbsent(sort(s), k -> new ArrayList<>()).add(s);
        }

        return new ArrayList<>(map.values());
    }

    static String sort(String s) {
        char[] arr = s.toCharArray();
        Arrays.sort(arr);
        return new String(arr);
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

class Solution {
   public:
    vector<vector<string>> groupAnagrams(vector<string>& strs) {
        unordered_map<string, vector<string>> mp;
        for (string& s : strs) {
            string key = s;
            sort(key.begin(), key.end());
            mp[key].push_back(s);
        }

        vector<vector<string>> res;
        for (auto& [_, v] : mp) res.push_back(v);
        return res;
    }
};
```

```python
from collections import defaultdict


class Solution:
    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        res = defaultdict(list)
        for s in strs:
            res["".join(sorted(s))].append(s)

        return list(res.values())
```

---
