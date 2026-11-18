---
title: "[Programmers] #42747 - H-Index [Java][C++][Python]"
date: 2026-11-17
categories: [PS, Programmers]
tags: ["sorting"]
slug: programmers-42747
media_subpath: /assets/img/posts/programmers-42747/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://school.programmers.co.kr/learn/courses/30/lessons/42747)
{: .prompt-info }

---

## 1. 아이디어

논문 $n$편 중 $h$번 이상 인용된 논문이 $h$편 이상이고 나머지는 $h$번 이하 인용되는 $h$의 최댓값을 구하는 문제로, 인용 횟수를 오름차순으로 정렬하고 0부터 센 위치를 $i$라 하면 위치 $i$부터의 $n - i$편이 가장 많이 인용된 논문들이다. $h = n - i$로 두면 $h$번 이상 인용된 논문이 $h$편 이상이라는 조건은 이 $n - i$편이 모두 $h$ 이상, 곧 그중 가장 적은 위치 $i$의 인용 횟수가 $h$ 이상이라는 말과 같다.

$h$는 $i$가 작을수록 크니 앞에서부터 처음 조건을 만족하는 $i$가 최댓값을 주고, 그 바로 앞 위치는 조건을 만족하지 못하므로 그 논문의 인용 횟수는 $h$ 이하이며 더 앞 논문은 정렬되어 있어 그보다 크지 않으므로, 나머지 논문이 $h$번 이하라는 조건도 같이 성립한다. 만족하는 위치가 없으면 모든 논문의 인용 횟수가 0이라 $h$는 0이다.

---

## 2. 코드

### 풀이 [Java][C++][Python]

```java
import java.util.*;

class Solution {
    public int solution(int[] citations) {
        Arrays.sort(citations);

        int n = citations.length;
        for (int i = 0; i < n; i++) {
            int h = n - i;
            if (citations[i] >= h) return h;
        }

        return 0;
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

int solution(vector<int> citations) {
    sort(citations.begin(), citations.end());

    int n = citations.size();
    for (int i = 0; i < n; i++) {
        int h = n - i;
        if (citations[i] >= h) return h;
    }

    return 0;
}
```

```python
def solution(citations):
    citations.sort()

    n = len(citations)
    for i in range(n):
        h = n - i
        if citations[i] >= h:
            return h

    return 0
```

---
