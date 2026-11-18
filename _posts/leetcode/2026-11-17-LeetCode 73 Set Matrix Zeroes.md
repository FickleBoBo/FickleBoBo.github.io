---
title: "[LeetCode] #73 - Set Matrix Zeroes [Java][C++][Python]"
date: 2026-11-17
categories: [PS, LeetCode]
tags: ["implementation"]
slug: leetcode-73
media_subpath: /assets/img/posts/leetcode-73/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/set-matrix-zeroes/)
{: .prompt-info }

---

## 1. 아이디어

`0`이 있는 칸의 행과 열을 모두 `0`으로 만드는 문제이다. `0`을 발견하자마자 바꾸면 새로 생긴 `0`을 원래 있던 `0`과 구분할 수 없어 다른 행과 열로 번지므로, 먼저 `0`이 있는 행과 열을 표시해 두고 나중에 한꺼번에 바꾼다. 행마다 하나, 열마다 하나씩 표시를 두면 보조 공간은 $O(m + n)$이다.

지문의 Follow-up은 보조 공간을 상수로 줄이는 것을 묻고, 첫 행·열 재사용이 그것에 맞춘 풀이이다. 별도 배열 대신 첫 행의 칸을 그 열의 표시로, 첫 열의 칸을 그 행의 표시로 쓴다. 첫 행의 칸에 원래 있던 `0`은 그 열이 어차피 `0`이 되어야 한다는 뜻이고 첫 열도 마찬가지라, 표시로 읽혀도 결과가 같다. 다만 첫 행과 첫 열 자체에 `0`이 있었는지는 표시가 덮어써 사라지므로 표시하기 전에 기억해 둔다.

첫 행과 첫 열은 안쪽 칸을 모두 바꾼 뒤 마지막에 처리한다. 먼저 `0`으로 바꾸면 표시 칸이 전부 `0`이 되어 표시가 없던 안쪽 칸까지 `0`이 되기 때문이다.

![4×5 행렬 [[1,1,1,0,1],[1,0,1,1,1],[1,1,1,1,1],[1,1,0,1,1]]에서 첫 행·열을 표시로 재사용해 [[0,0,0,0,0],[0,0,0,0,0],[1,0,0,0,1],[0,0,0,0,0]]이 되는 과정](first-rowcol-light.gif){: .light }
![4×5 행렬 [[1,1,1,0,1],[1,0,1,1,1],[1,1,1,1,1],[1,1,0,1,1]]에서 첫 행·열을 표시로 재사용해 [[0,0,0,0,0],[0,0,0,0,0],[1,0,0,0,1],[0,0,0,0,0]]이 되는 과정](first-rowcol-dark.gif){: .dark }

---

## 2. 코드

### 풀이 1: 행·열 표시 배열 [Java][C++][Python]

```java
class Solution {
    public void setZeroes(int[][] matrix) {
        int m = matrix.length, n = matrix[0].length;
        boolean[] row = new boolean[m];
        boolean[] col = new boolean[n];

        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (matrix[i][j] == 0) {
                    row[i] = true;
                    col[j] = true;
                }
            }
        }

        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (row[i] || col[j]) matrix[i][j] = 0;
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
    void setZeroes(vector<vector<int>>& matrix) {
        int m = matrix.size(), n = matrix[0].size();
        vector<bool> row(m);
        vector<bool> col(n);

        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (matrix[i][j] == 0) {
                    row[i] = true;
                    col[j] = true;
                }
            }
        }

        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (row[i] || col[j]) matrix[i][j] = 0;
            }
        }
    }
};
```

```python
class Solution:
    def setZeroes(self, matrix: list[list[int]]) -> None:
        m, n = len(matrix), len(matrix[0])
        row = [False] * m
        col = [False] * n

        for i in range(m):
            for j in range(n):
                if matrix[i][j] == 0:
                    row[i] = True
                    col[j] = True

        for i in range(m):
            for j in range(n):
                if row[i] or col[j]:
                    matrix[i][j] = 0
```

---

### 풀이 2: 첫 행·열 재사용 [Java][C++][Python]

```java
class Solution {
    public void setZeroes(int[][] matrix) {
        int m = matrix.length, n = matrix[0].length;
        boolean firstRowHas0 = false, firstColHas0 = false;

        for (int i = 0; i < m; i++) {
            if (matrix[i][0] == 0) firstColHas0 = true;
        }
        for (int j = 0; j < n; j++) {
            if (matrix[0][j] == 0) firstRowHas0 = true;
        }

        for (int i = 1; i < m; i++) {
            for (int j = 1; j < n; j++) {
                if (matrix[i][j] == 0) {
                    matrix[i][0] = 0;
                    matrix[0][j] = 0;
                }
            }
        }

        for (int i = 1; i < m; i++) {
            for (int j = 1; j < n; j++) {
                if (matrix[i][0] == 0 || matrix[0][j] == 0) matrix[i][j] = 0;
            }
        }

        if (firstColHas0) {
            for (int i = 0; i < m; i++) {
                matrix[i][0] = 0;
            }
        }
        if (firstRowHas0) {
            for (int j = 0; j < n; j++) {
                matrix[0][j] = 0;
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
    void setZeroes(vector<vector<int>>& matrix) {
        int m = matrix.size(), n = matrix[0].size();
        bool first_row_has_0 = false, first_col_has_0 = false;

        for (int i = 0; i < m; i++) {
            if (matrix[i][0] == 0) first_col_has_0 = true;
        }
        for (int j = 0; j < n; j++) {
            if (matrix[0][j] == 0) first_row_has_0 = true;
        }

        for (int i = 1; i < m; i++) {
            for (int j = 1; j < n; j++) {
                if (matrix[i][j] == 0) {
                    matrix[i][0] = 0;
                    matrix[0][j] = 0;
                }
            }
        }

        for (int i = 1; i < m; i++) {
            for (int j = 1; j < n; j++) {
                if (matrix[i][0] == 0 || matrix[0][j] == 0) matrix[i][j] = 0;
            }
        }

        if (first_col_has_0) {
            for (int i = 0; i < m; i++) matrix[i][0] = 0;
        }
        if (first_row_has_0) {
            for (int j = 0; j < n; j++) matrix[0][j] = 0;
        }
    }
};
```

```python
class Solution:
    def setZeroes(self, matrix: list[list[int]]) -> None:
        m, n = len(matrix), len(matrix[0])
        first_row_has_0, first_col_has_0 = False, False

        for i in range(m):
            if matrix[i][0] == 0:
                first_col_has_0 = True
        for j in range(n):
            if matrix[0][j] == 0:
                first_row_has_0 = True

        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][j] == 0:
                    matrix[i][0] = 0
                    matrix[0][j] = 0

        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][0] == 0 or matrix[0][j] == 0:
                    matrix[i][j] = 0

        if first_col_has_0:
            for i in range(m):
                matrix[i][0] = 0
        if first_row_has_0:
            for j in range(n):
                matrix[0][j] = 0
```

---
