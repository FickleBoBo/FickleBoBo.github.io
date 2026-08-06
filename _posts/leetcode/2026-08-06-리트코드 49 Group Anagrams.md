---
title: "[LeetCode] 49번 - Group Anagrams [Java][C++]"
slug: leetcode-49
date: 2026-08-06
categories: [PS, LeetCode]
tags: [data structure, string, anagram, hash set／hash map]
toc: true
math: true
---

[문제 링크](https://leetcode.com/problems/group-anagrams/)

---

## 1. 아이디어

주어진 문자열 배열 `strs`에서 애너그램끼리 그룹을 묶는 문제로 애너그램은 보유한 문자의 종류와 수가 동일하다는 점을 활용해서 해결할 수도 있고 문자열의 각 문자를 사전순으로 정렬했을 때 동일한 문자열이 나옴을 활용할 수도 있다.

처음엔 애너그램 그룹을 의미하는 `ans`를 둔 후 `strs`의 각 문자열에 대해, `ans`의 각 그룹에 대해 그룹의 첫 번째 문자열과 `strs`의 해당 문자열이 애너그램 관계면 그룹에 추가하고 아니면 다음 그룹에 대해 비교하는 방식을 반복했다. AC는 됐지만 효율적이지 않아 시간 소요가 많았다.

두 번째는 해시맵을 활용해서 `key`에 그룹을 대표하는 사전순 애너그램 문자열, `value`에 그룹의 문자열을 두도록 했다. `strs`의 각 문자열에 대해 사전순 애너그램 문자열로 변환한 후 해시맵에 `key`가 존재하면 그룹에 담고, `key`가 존재하지 않으면 그룹의 첫 번째 멤버로 추가해줬다.

---

## 2. 복잡도

### 1. 리스트

| 시간복잡도 | 공간복잡도 |
| :--------: | :--------: |
| $O(N^2 L)$ |   $O(1)$   |

> N = strs 길이(문자열 개수), L = 개별 문자열 길이

### 2. 해시맵

|   시간복잡도   | 공간복잡도 |
| :------------: | :--------: |
| $O(NL \log L)$ |  $O(NL)$   |

> N = strs 길이(문자열 개수), L = 개별 문자열 길이

---

## 3. 코드

### 1. 리스트 [Java][C++]

```java
import java.util.*;

class Solution {
    public List<List<String>> groupAnagrams(String[] strs) {
        List<List<String>> ans = new ArrayList<>();

        out:
        for (String str : strs) {
            for (List<String> list : ans) {
                if (list.get(0).length() == str.length() && isAnagram(list.get(0), str)) {
                    list.add(str);
                    continue out;
                }
            }

            List<String> list = new ArrayList<>();
            list.add(str);
            ans.add(list);
        }

        return ans;
    }

    static boolean isAnagram(String s1, String s2) {
        int[] cnt = new int[26];
        for (char c : s1.toCharArray()) {
            cnt[c - 'a']++;
        }
        for (char c : s2.toCharArray()) {
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
    bool isAnagram(string& s1, string& s2) {
        vector<int> cnt(26);
        for (char c : s1) {
            cnt[c - 'a']++;
        }
        for (char c : s2) {
            cnt[c - 'a']--;
        }

        for (int x : cnt) {
            if (x != 0) return false;
        }

        return true;
    }

    vector<vector<string>> groupAnagrams(vector<string>& strs) {
        vector<vector<string>> ans;

        for (string& str : strs) {
            bool flag = false;

            for (vector<string>& v : ans) {
                if (v[0].size() == str.size() && isAnagram(v[0], str)) {
                    v.push_back(str);
                    flag = true;
                    break;
                }
            }

            if (flag) continue;

            vector<string> v;
            v.push_back(str);
            ans.push_back(v);
        }

        return ans;
    }
};
```

### 2. 해시맵 [Java][C++]

```java
import java.util.*;

class Solution {
    public List<List<String>> groupAnagrams(String[] strs) {
        Map<String, List<String>> map = new HashMap<>();
        for (String str : strs) {
            char[] arr = str.toCharArray();
            Arrays.sort(arr);
            String key = new String(arr);
            map.computeIfAbsent(key, k -> new ArrayList<>()).add(str);
        }

        return new ArrayList<>(map.values());
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
        for (string& str : strs) {
            string key = str;
            sort(key.begin(), key.end());
            mp[key].push_back(str);
        }

        vector<vector<string>> ans;
        for (auto& [_, v] : mp) {
            ans.push_back(v);
        }

        return ans;
    }
};
```

---
