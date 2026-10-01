---
title: "[LeetCode] #1143 - Longest Common Subsequence [Java][C++][Python]"
date: 2026-10-01
categories: [PS, LeetCode]
tags: ["dynamic programming", "lcs", "string"]
slug: leetcode-1143
media_subpath: /assets/img/posts/leetcode-1143/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/longest-common-subsequence/)
{: .prompt-info }

---

## 1. 아이디어

문자열 `text1`과 `text2`의 longest common subsequence, 즉 LCS를 구하는 문제로 전형적인 다이나믹 프로그래밍을 활용한 LCS 문제다. `text1`의 길이 `i` 접두사, `text2`의 길이 `j` 접두사 사이의 LCS를 저장하는 `dp[i][j]`는 두 접두사의 끝 문자가 일치하면 `dp[i][j] = dp[i - 1][j - 1] + 1`, 일치하지 않으면 `dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])`라는 점을 활용하면 된다.

---

## 2. 복잡도

| 접근 | 시간            | 공간            |
| ---- | --------------- | --------------- |
| 풀이 | $O(N \times M)$ | $O(N \times M)$ |

($N$ = `text1`의 길이, $M$ = `text2`의 길이)

---

## 3. 코드

### 풀이 [Java][C++][Python]

```java
class Solution {
    public int longestCommonSubsequence(String text1, String text2) {
        int n = text1.length(), m = text2.length();
        int[][] dp = new int[1 + n][1 + m];

        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= m; j++) {
                if (text1.charAt(i - 1) == text2.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1] + 1;
                } else {
                    dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
                }
            }
        }

        return dp[n][m];
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

class Solution {
   public:
    int longestCommonSubsequence(string text1, string text2) {
        int n = text1.size(), m = text2.size();
        vector<vector<int>> dp(1 + n, vector<int>(1 + m));

        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= m; j++) {
                if (text1[i - 1] == text2[j - 1]) {
                    dp[i][j] = dp[i - 1][j - 1] + 1;
                } else {
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);
                }
            }
        }

        return dp[n][m];
    }
};
```

```python
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        n, m = len(text1), len(text2)
        dp = [[0] * (1 + m) for _ in range(1 + n)]

        for i in range(1, n + 1):
            for j in range(1, m + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        return dp[n][m]
```

---
