---
title: "[LeetCode] 347번 - Top K Frequent Elements [Java][C++]"
slug: leetcode-347
date: 2026-08-07
categories: [PS, LeetCode]
tags: [data structure, priority queue, sorting]
toc: true
math: true
---

[문제 링크](https://leetcode.com/problems/top-k-frequent-elements/)

---

## 1. 아이디어

정수 배열 `nums`에 대해 등장 빈도수가 `k`번째로 많은 수까지 찾아서 출력하는 문제로 해시맵을 활용한 방식과 버킷 정렬을 활용한 방식으로 해결할 수 있다.

해시맵의 경우 `key`에 해당 숫자, `value`에 등장 횟수를 저장한 카운팅 맵을 먼저 계산해주었다. 이후 수와 등장 횟수 객체를 갖는 우선순위 큐를 활용해 등장 횟수에 대한 내림차순으로 정렬하여 순서대로 `k`개를 꺼내 해당 숫자를 담아서 반환해줬다. 우선순위 큐에서 정렬 때문에 $O(n \log n)$ 의 시간복잡도가 소요된다.

Follow up의 경우 버킷 정렬을 활용하면 해결할 수 있는데 인덱스를 등장 횟수, 값을 해당 숫자로 하는 버킷 정렬 배열을 활용하면 된다. 이전처럼 해시맵으로 카운팅을 한 후 같은 빈도수의 여러 수가 존재할 수 있으므로 버킷 정렬을 위한 중첩 리스트를 선언해주었다. 인덱스가 등장 횟수이므로 역순으로 탐색하며 `k`개의 수를 담아서 반환하면 $O(n)$ 의 시간복잡도로 해결할 수 있다.

---

## 2. 복잡도

### 1. 카운팅 맵 + 우선순위 큐

|  시간복잡도   | 공간복잡도 |
| :-----------: | :--------: |
| $O(n \log n)$ |   $O(n)$   |

> $n$ = `nums` 길이

### 2. 버킷 정렬

| 시간복잡도 | 공간복잡도 |
| :--------: | :--------: |
|   $O(n)$   |   $O(n)$   |

> $n$ = `nums` 길이

---

## 3. 코드

### 1. 카운팅 맵 + 우선순위 큐 [Java][C++]

```java
import java.util.*;

class Solution {
    public int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> map = new HashMap<>();
        for (int x : nums) {
            map.put(x, map.getOrDefault(x, 0) + 1);
        }

        PriorityQueue<int[]> pq = new PriorityQueue<>((o1, o2) -> Integer.compare(o2[1], o1[1]));
        for (Map.Entry<Integer, Integer> e : map.entrySet()) {
            pq.offer(new int[]{e.getKey(), e.getValue()});
        }

        int[] ans = new int[k];
        for (int i = 0; i < k; i++) {
            ans[i] = pq.poll()[0];
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
        unordered_map<int, int> mp;
        for (int x : nums) {
            mp[x]++;
        }

        priority_queue<pair<int, int>> pq;
        for (auto& [num, freq] : mp) {
            pq.push({freq, num});
        }

        vector<int> res;
        while (k--) {
            res.push_back(pq.top().second);
            pq.pop();
        }

        return res;
    }
};
```

### 2. 버킷 정렬 [Java][C++]

```java
import java.util.*;

class Solution {
    public int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> map = new HashMap<>();
        for (int x : nums) {
            map.put(x, map.getOrDefault(x, 0) + 1);
        }

        List<Integer>[] bucket = new ArrayList[1 + nums.length];
        for (int i = 1; i < bucket.length; i++) {
            bucket[i] = new ArrayList<>();
        }

        for (Map.Entry<Integer, Integer> e : map.entrySet()) {
            bucket[e.getValue()].add(e.getKey());
        }

        int[] ans = new int[k];
        int idx = 0;

        for (int i = bucket.length - 1; i >= 1; i--) {
            for (int x : bucket[i]) {
                ans[idx++] = x;
                if (idx == k) return ans;
            }
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
        unordered_map<int, int> mp;
        for (int x : nums) {
            mp[x]++;
        }

        vector<vector<int>> bucket(1 + nums.size());
        for (auto [num, freq] : mp) {
            bucket[freq].push_back(num);
        }

        vector<int> ans;
        for (int i = bucket.size() - 1; i >= 1; i--) {
            for (int x : bucket[i]) {
                ans.push_back(x);
                if (ans.size() == k) return ans;
            }
        }

        return ans;
    }
};
```

---
