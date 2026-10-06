---
title: "[LeetCode] #66 - Plus One [Java][C++][Python]"
date: 2026-09-08
categories: [PS, LeetCode]
tags: ["implementation"]
slug: leetcode-66
media_subpath: /assets/img/posts/leetcode-66/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/plus-one/)
{: .prompt-info }

---

## 1. 아이디어

임의의 큰 정수를 각 자릿수를 담은 배열 `digits`로 표현한 후 1을 더했을 때 배열을 구하는 문제다. 1을 더하는 것은 배열의 마지막 원소에 1을 더하는 것으로 이때 자릿수 올림이 발생하면 이를 도미노처럼 반영해야 한다. 더하는 수가 1이므로 끝자리부터 자릿수가 9가 아니라면 올림이 더이상 발생하지 않으므로 해당 자리에 1을 더한 후 그대로 반환하고, 올림이 발생하면 해당 자리는 0이 되므로 0으로 변경하는 과정을 반복하면 된다. 모든 자리에서 올림이 발생하면 최종 결과는 `digits`보다 길이가 1만큼 길고 첫 번째 원소만 1인 배열이 되므로 이 경우만 별도로 반환했다.

---

## 2. 복잡도

| 접근 | 시간   | 공간   |
| ---- | ------ | ------ |
| 풀이 | $O(N)$ | $O(N)$ |

($N$ = `digits`의 길이)

---

## 3. 코드

### 풀이 [Java][C++][Python]

```java
class Solution {
    public int[] plusOne(int[] digits) {
        for (int i = digits.length - 1; i >= 0; i--) {
            if (digits[i] < 9) {
                digits[i]++;
                return digits;
            }
            digits[i] = 0;
        }

        int[] ans = new int[1 + digits.length];
        ans[0] = 1;
        return ans;
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

class Solution {
   public:
    vector<int> plusOne(vector<int>& digits) {
        for (int i = digits.size() - 1; i >= 0; i--) {
            if (digits[i] < 9) {
                digits[i]++;
                return digits;
            }
            digits[i] = 0;
        }

        vector<int> ans(1 + digits.size());
        ans[0] = 1;
        return ans;
    }
};
```

```python
class Solution:
    def plusOne(self, digits: list[int]) -> list[int]:
        for i in reversed(range(len(digits))):
            if digits[i] < 9:
                digits[i] += 1
                return digits
            digits[i] = 0

        return [1] + [0] * len(digits)
```

---
