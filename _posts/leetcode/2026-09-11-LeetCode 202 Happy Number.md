---
title: "[LeetCode] #202 - Happy Number [Java][C++][Python]"
date: 2026-09-11
categories: [PS, LeetCode]
tags: ["data structure", "hash table", "floyd's cycle detection"]
slug: leetcode-202
media_subpath: /assets/img/posts/leetcode-202/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/happy-number/)
{: .prompt-info }

---

## 1. 아이디어

Happy Number를 구하는 문제로 Happy Number는 각 자릿수의 제곱의 합을 구하는 과정을 반복했을 때 1이 되는 수다. 1은 한 스텝을 더 가도 다시 1이라 수들은 루프를 돌거나 1로 가는 점을 볼 수 있고, 이 때문에 집합을 활용해 한 번 등장했던 수를 집합에 저장하면 같은 수가 다시 등장했을 때 루프가 시작되는 것을 탐지할 수 있다.

플로이드 사이클 탐지 알고리즘을 활용하면 $O(1)$의 공간을 사용하면서 더 효율적으로 해결할 수 있는데 1스텝씩 가는 거북이 포인터와 2스텝씩 가는 토끼 포인터를 출발시켜 서로 만나는 경우 해당 위치가 반드시 사이클 내부이므로 이때 위치가 1인지 여부로도 판단할 수 있다.

---

## 2. 복잡도

| 접근                 | 시간   | 공간   |
| -------------------- | ------ | ------ |
| 해시 셋              | $O(D)$ | $O(D)$ |
| 플로이드 사이클 탐지 | $O(D)$ | $O(1)$ |

($D$ = `n`의 자릿수 $\approx \log_{10} n$)

---

## 3. 코드

### 풀이 1: 해시 셋 [Java][C++][Python]

```java
import java.util.*;

class Solution {
    public boolean isHappy(int n) {
        Set<Integer> seen = new HashSet<>();
        while (!seen.contains(n)) {
            seen.add(n);
            n = step(n);
        }

        return n == 1;
    }

    static int step(int x) {
        int sum = 0;
        while (x > 0) {
            int d = x % 10;
            sum += d * d;
            x /= 10;
        }

        return sum;
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

class Solution {
   public:
    int step(int x) {
        int sum = 0;
        while (x > 0) {
            int d = x % 10;
            sum += d * d;
            x /= 10;
        }

        return sum;
    }

    bool isHappy(int n) {
        unordered_set<int> seen;
        while (!seen.contains(n)) {
            seen.insert(n);
            n = step(n);
        }

        return n == 1;
    }
};
```

```python
class Solution:
    def isHappy(self, n: int) -> bool:
        seen = set()
        while n not in seen:
            seen.add(n)
            n = sum(int(d) ** 2 for d in str(n))

        return n == 1
```

---

### 풀이 2: 플로이드 사이클 탐지 [Java][C++][Python]

```java
class Solution {
    public boolean isHappy(int n) {
        int slow = n, fast = step(n);
        while (slow != fast) {
            slow = step(slow);
            fast = step(step(fast));
        }

        return slow == 1;
    }

    static int step(int x) {
        int sum = 0;
        while (x > 0) {
            int d = x % 10;
            sum += d * d;
            x /= 10;
        }

        return sum;
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

class Solution {
   public:
    int step(int x) {
        int sum = 0;
        while (x > 0) {
            int d = x % 10;
            sum += d * d;
            x /= 10;
        }

        return sum;
    }

    bool isHappy(int n) {
        int slow = n, fast = step(n);
        while (slow != fast) {
            slow = step(slow);
            fast = step(step(fast));
        }

        return slow == 1;
    }
};
```

```python
class Solution:
    def isHappy(self, n: int) -> bool:
        def step(x):
            return sum(int(d) ** 2 for d in str(x))

        slow, fast = n, step(n)
        while slow != fast:
            slow = step(slow)
            fast = step(step(fast))

        return slow == 1
```

---
