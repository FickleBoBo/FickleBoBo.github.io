---
title: "[LeetCode] #347 - Top K Frequent Elements [Java][C++][Python]"
date: 2026-09-20
categories: [PS, LeetCode]
tags: ["data structure", "hash table", "sorting"]
slug: leetcode-347
media_subpath: /assets/img/posts/leetcode-347/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/top-k-frequent-elements/)
{: .prompt-info }

---

## 1. 아이디어

정수 배열 `nums`와 정수 `k`가 주어질 때, `nums`에서 가장 등장 빈도가 높은 `k`가지 원소를 구하는 문제다. 카운팅 맵을 활용해 각 원소와 등장 횟수를 기록한 후 등장 횟수를 기준으로 내림차순 정렬한 후 `k`개의 원소를 앞에서부터 순서대로 뽑으면 간단하게 해결할 수 있다.

Follow up은 $O(N \log N)$보다 빠른 시간복잡도로 이 문제를 해결해야 한다. 이때는 버킷 정렬을 활용하면 해결할 수 있는데 인덱스에 빈도수, 값에 원소들을 저장하는 배열을 만들어 카운팅 맵의 각 엔트리에 대해 버킷 정렬에 삽입하면 된다. 인덱스가 빈도수이므로 역순으로 순회하며 각 원소를 `k`개 담으면 된다.

---

## 2. 복잡도

| 접근        | 시간          | 공간   |
| ----------- | ------------- | ------ |
| 빈도순 정렬 | $O(N \log N)$ | $O(N)$ |
| 버킷 정렬   | $O(N)$        | $O(N)$ |

($N$ = `nums`의 길이)

---

## 3. 코드

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

---
