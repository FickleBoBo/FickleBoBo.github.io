---
title: "[LeetCode] #49 - Group Anagrams [Java][C++][Python]"
date: 2026-09-20
categories: [PS, LeetCode]
tags: ["data structure", "hash table", "sorting", "string"]
slug: leetcode-49
media_subpath: /assets/img/posts/leetcode-49/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/group-anagrams/)
{: .prompt-info }

---

## 1. 아이디어

애너그램 관계에 있는 문자열을 그룹핑해서 배열로 반환하는 문제로 해시맵을 활용하면 해결할 수 있다. 해시맵의 value에 애너그램 관계에 있는 문자열 그룹을, key에 해당 그룹의 문자열 중 하나를 사전순 정렬한 문자열로 두면 특정 문자열이 새로운 그룹을 만든다면 정렬 후 이를 key로 사용해 새로운 그룹을 저장하고, 기존 그룹에 포함되면 그대로 더하는 방식으로 효율적으로 처리할 수 있다.

---

## 2. 복잡도

| 접근 | 시간                   | 공간            |
| ---- | ---------------------- | --------------- |
| 풀이 | $O(N \times K \log K)$ | $O(N \times K)$ |

($N$ = `strs`의 길이, $K$ = `strs` 원소 중 최대 길이)

---

## 3. 코드

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
