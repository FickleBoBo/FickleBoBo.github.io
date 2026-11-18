---
title: "[LeetCode] #48 - Rotate Image [Java][C++][Python]"
date: 2026-11-14
categories: [PS, LeetCode]
tags: ["implementation"]
slug: leetcode-48
media_subpath: /assets/img/posts/leetcode-48/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/rotate-image/)
{: .prompt-info }

---

## 1. 아이디어

$n \times n$ 행렬을 새 행렬 없이 시계 방향으로 90도 돌리는 문제로, 0부터 센 칸 $(i, j)$는 회전 뒤 $(j, n - 1 - i)$로 간다. 이는 대각선을 기준으로 전치해 $(i, j)$를 $(j, i)$로 보낸 뒤 각 행을 좌우로 뒤집어 $(j, i)$를 $(j, n - 1 - i)$로 보내는 두 단계와 같고, 두 단계 모두 칸끼리 맞바꾸기만 하므로 추가 행렬 없이 제자리에서 끝난다. 전치는 대각선 위쪽 칸만 훑어 쌍마다 한 번씩 맞바꿔야 하고, 전체를 훑으면 같은 쌍을 두 번 바꿔 원래대로 돌아온다.

---

## 2. 코드

### 풀이 [Java][C++][Python]

```java
class Solution {
    public void rotate(int[][] matrix) {
        int n = matrix.length;

        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                int tmp = matrix[i][j];
                matrix[i][j] = matrix[j][i];
                matrix[j][i] = tmp;
            }
        }

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n / 2; j++) {
                int tmp = matrix[i][j];
                matrix[i][j] = matrix[i][n - 1 - j];
                matrix[i][n - 1 - j] = tmp;
            }
        }
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

class Solution {
   public:
    void rotate(vector<vector<int>>& matrix) {
        int n = matrix.size();

        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                swap(matrix[i][j], matrix[j][i]);
            }
        }

        for (auto& row : matrix) {
            reverse(row.begin(), row.end());
        }
    }
};
```

행을 `auto&`로 받아 `std::reverse`로 `matrix`의 행을 직접 뒤집었다.

```python
class Solution:
    def rotate(self, matrix: list[list[int]]) -> None:
        n = len(matrix)

        for i in range(n):
            for j in range(i + 1, n):
                matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

        for row in matrix:
            row.reverse()
```

---
