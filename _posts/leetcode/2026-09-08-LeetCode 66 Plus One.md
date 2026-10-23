---
title: "[LeetCode] #66 - Plus One [Java][C++][Python]"
date: 2026-09-08
categories: [PS, LeetCode]
tags: ["implementation"]
slug: leetcode-66
media_subpath: /assets/img/posts/leetcode-66/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/plus-one/)
{: .prompt-info }

---

## 1. 아이디어

자릿수 배열로 주어진 큰 수에 1을 더한 결과를 같은 형태의 배열로 구하는 문제다. 자릿수가 최대 100이라 기본 정수형에는 담기지 않으므로 끝자리부터 직접 올림을 처리해야 하는데, 1을 더했을 때 끝자리가 `9`가 아니면 그 자리만 1 커지고 나머지는 그대로이며, `9`이면 `0`이 되면서 올림이 윗자리로 넘어간다. 따라서 끝자리부터 훑으며 `9`는 `0`으로 바꾸고, 처음 만나는 `9`가 아닌 자리를 1 키우면 올림이 끝나므로 거기서 마치면 된다. 모든 자리가 `9`였다면 전부 `0`이 되고 올림이 맨 앞에 새로 생기므로, 맨 앞이 `1`이고 나머지가 모두 `0`인 길이가 1 더 긴 배열이 답이다.

---

## 2. 코드

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
