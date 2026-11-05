---
title: "[LeetCode] #1143 - Longest Common Subsequence [Java][C++][Python]"
date: 2026-10-01
categories: [PS, LeetCode]
tags: ["dynamic programming", "lcs", "string"]
slug: leetcode-1143
media_subpath: /assets/img/posts/leetcode-1143/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/longest-common-subsequence/)
{: .prompt-info }

---

## 1. 아이디어

두 문자열의 가장 긴 공통 부분 수열(LCS)의 길이를 구하는 대표적인 DP 문제다. 첫 번째 문자열의 앞 $i$글자와 두 번째 문자열의 앞 $j$글자의 가장 긴 공통 부분 수열 길이를 `dp[i][j]`로 두면, 두 부분의 마지막 글자가 같은지로 경우가 갈린다. 공통 부분 수열은 두 문자열의 같은 글자를 순서대로 짝지은 것으로 볼 수 있고, 각 부분의 마지막 글자는 가장 뒤에 있어 쓰인다면 반드시 마지막 짝에 들어간다.

두 마지막 글자가 같으면 가장 긴 공통 부분 수열의 끝을 이 두 글자의 짝으로 맞춰도 길이가 줄지 않으므로 `dp[i][j] = dp[i - 1][j - 1] + 1`이다. 다를 때는 두 글자가 모두 쓰이려면 서로 마지막 짝이어야 하는데 글자가 달라 그럴 수 없으므로, 한쪽은 빠지고 `dp[i][j]`는 `dp[i - 1][j]`와 `dp[i][j - 1]` 중 큰 값이다. 빈 문자열과의 공통 부분 수열은 길이 0이라 `dp[0][j]`와 `dp[i][0]`은 0이고, 이를 시작으로 `dp`를 채워 가면 된다.

---

## 2. 코드

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
