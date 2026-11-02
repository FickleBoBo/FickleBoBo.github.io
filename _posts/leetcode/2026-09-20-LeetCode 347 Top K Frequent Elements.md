---
title: "[LeetCode] #347 - Top K Frequent Elements [Java][C++][Python]"
date: 2026-09-20
categories: [PS, LeetCode]
tags: ["data structure", "hash set/map", "sorting"]
slug: leetcode-347
media_subpath: /assets/img/posts/leetcode-347/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/top-k-frequent-elements/)
{: .prompt-info }

---

## 1. 아이디어

주어진 배열에서 가장 많이 등장한 원소 $k$개를 구하는 문제이고, 어느 풀이든 먼저 원소별 등장 횟수를 센다. 기본 풀이인 빈도순 정렬은 센 (원소, 횟수) 쌍을 횟수 내림차순으로 정렬해 앞의 $k$개를 취하며, 배열의 길이를 $n$이라 하면 고유 원소가 최대 $n$개라 $O(n \log n)$이다.

지문의 Follow-up은 시간 복잡도가 $O(n \log n)$보다 나을 것을 요구하므로 빈도순 정렬은 이를 만족하지 못하고, Follow-up에 맞춘 풀이가 버킷 정렬이다. 등장 횟수는 1 이상 $n$ 이하의 정수이므로 횟수를 인덱스로 하는 버킷에 원소를 담고 큰 인덱스부터 읽으면 정렬 없이 횟수 내림차순이 되어 $O(n)$에 끝난다.

---

## 2. 코드

### 풀이 1: 빈도순 정렬 [Java][C++][Python]

```java
import java.util.*;

class Solution {
    public int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> cnt = new HashMap<>();
        for (int x : nums) {
            cnt.put(x, cnt.getOrDefault(x, 0) + 1);
        }

        List<Map.Entry<Integer, Integer>> list = new ArrayList<>(cnt.entrySet());
        list.sort((o1, o2) -> Integer.compare(o2.getValue(), o1.getValue()));

        int[] ans = new int[k];
        for (int i = 0; i < k; i++) {
            ans[i] = list.get(i).getKey();
        }

        return ans;
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

class Solution {
   public:
    vector<int> topKFrequent(vector<int>& nums, int k) {
        unordered_map<int, int> cnt;
        for (int x : nums) cnt[x]++;

        vector<pair<int, int>> v(cnt.begin(), cnt.end());
        sort(v.begin(), v.end(), [](auto& a, auto& b) {
            return a.second > b.second;
        });

        vector<int> ans(k);
        for (int i = 0; i < k; i++) ans[i] = v[i].first;
        return ans;
    }
};
```

```python
from collections import Counter


class Solution:
    def topKFrequent(self, nums: list[int], k: int) -> list[int]:
        cnt = Counter(nums)
        return [x for x, _ in cnt.most_common(k)]
```

`most_common`에 `k`를 넘겨 횟수 내림차순 상위 `k`개를 바로 얻었다.

---

### 풀이 2: 버킷 정렬 [Java][C++][Python]

```java
import java.util.*;

class Solution {
    public int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> cnt = new HashMap<>();
        for (int x : nums) {
            cnt.put(x, cnt.getOrDefault(x, 0) + 1);
        }

        int len = nums.length;
        List<Integer>[] buckets = new ArrayList[1 + len];
        for (int i = 1; i <= len; i++) {
            buckets[i] = new ArrayList<>();
        }

        for (Map.Entry<Integer, Integer> e : cnt.entrySet()) {
            buckets[e.getValue()].add(e.getKey());
        }

        List<Integer> list = new ArrayList<>();
        for (int i = len; i > 0; i--) {
            list.addAll(buckets[i]);
        }

        return list.stream().limit(k).mapToInt(Integer::intValue).toArray();
    }
}
```

큰 횟수의 버킷부터 이어 붙인 리스트에서 스트림의 `limit`으로 앞의 `k`개만 취하고, `mapToInt`로 `int[]`로 바꿔 반환했다.

```c++
#include <bits/stdc++.h>
using namespace std;

class Solution {
   public:
    vector<int> topKFrequent(vector<int>& nums, int k) {
        unordered_map<int, int> cnt;
        for (int x : nums) cnt[x]++;

        int len = nums.size();
        vector<vector<int>> buckets(1 + len);
        for (auto [x, c] : cnt) buckets[c].push_back(x);

        vector<int> res;
        for (int i = len; i > 0; i--) {
            res.insert(res.end(), buckets[i].begin(), buckets[i].end());
        }
        res.resize(k);

        return res;
    }
};
```

큰 횟수의 버킷부터 `res`에 이어 붙인 뒤 `resize(k)`로 앞의 `k`개만 남겼다.

```python
from collections import Counter
from itertools import chain


class Solution:
    def topKFrequent(self, nums: list[int], k: int) -> list[int]:
        cnt = Counter(nums)

        n = len(nums)
        buckets = [[] for _ in range(1 + n)]
        for x, c in cnt.items():
            buckets[c].append(x)

        return list(chain.from_iterable(reversed(buckets)))[:k]
```

`reversed`로 큰 횟수의 버킷부터 `chain.from_iterable`로 하나로 이어 붙이고, 앞의 `k`개를 슬라이스했다.

---
