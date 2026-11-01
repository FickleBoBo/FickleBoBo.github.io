---
title: "[LeetCode] #202 - Happy Number [Java][C++][Python]"
date: 2026-09-11
categories: [PS, LeetCode]
tags: ["data structure", "hash set/map", "floyd's cycle detection"]
slug: leetcode-202
media_subpath: /assets/img/posts/leetcode-202/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/happy-number/)
{: .prompt-info }

---

## 1. 아이디어

양의 정수의 각 자리 숫자를 제곱해 더하는 연산을 반복했을 때 1에 도달하는지 판별하는 문제다. 지문대로 이 과정은 1에 도달하거나 1이 없는 사이클을 돈다. 다음 값이 현재 값 하나로 정해지므로 한 번 나온 값이 다시 나오면 그 뒤는 같은 값들이 되풀이된다. 1은 연산해도 1이라 자기 자신으로 돌아오는 값으로 볼 수 있으니 두 경우 모두 어떤 값이 반복되는 것으로 통일된다. 처음 반복된 값이 1이면 행복한 수이고, 아니면 행복하지 않은 수다. 그래서 지나온 값을 모아 두고 새 값이 이미 있는지만 확인하면 반복을 알 수 있다.

지나온 값을 저장해야 반복을 알 수 있는 것은 아니다. 다음 값이 현재 값 하나로 정해지는 수열이므로 플로이드 사이클 탐지(토끼와 거북이 알고리즘)처럼 한 칸씩 가는 값(`slow`)과 한 칸 앞에서 출발해 두 칸씩 가는 값(`fast`)을 함께 보내면 둘은 결국 같은 값에서 만난다. 둘이 사이클에 들어선 뒤에는 `fast`가 사이클을 돌아 `slow`를 따라잡을 때까지 남은 거리(사이클 안에서 센 거리)가 한 번 진행할 때마다 1씩 줄어 0이 되기 때문이다. 1은 자기 자신으로 돌아오므로 행복한 수에서는 둘이 1에서 만나고, 행복하지 않은 수의 사이클에는 1이 없어 만난 값이 1이 아니다. 그러므로 만난 값이 1인지가 곧 판정이다. 이 방법은 값을 저장하지 않아 추가 메모리가 필요 없다.

![n = 19에서 slow와 fast가 4번째 반복에 1에서 만나는 과정](floyd-happy-light.gif){: .light }
![n = 19에서 slow와 fast가 4번째 반복에 1에서 만나는 과정](floyd-happy-dark.gif){: .dark }

![n = 2에서 slow와 fast가 7번째 반복에 사이클 안의 42에서 만나는 과정](floyd-unhappy-light.gif){: .light }
![n = 2에서 slow와 fast가 7번째 반복에 사이클 안의 42에서 만나는 과정](floyd-unhappy-dark.gif){: .dark }

---

## 2. 코드

### 풀이 1: 해시셋 [Java][C++][Python]

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
