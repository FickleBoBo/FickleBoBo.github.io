---
title: "[LeetCode] #54 - Spiral Matrix [Java][C++][Python]"
date: 2026-11-14
categories: [PS, LeetCode]
tags: ["implementation"]
slug: leetcode-54
media_subpath: /assets/img/posts/leetcode-54/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/spiral-matrix/)
{: .prompt-info }

---

## 1. 아이디어

$m \times n$ 행렬의 원소를 바깥 테두리에서 안쪽으로 나선 순서로 모으는 문제로, 위쪽 행, 오른쪽 열, 아래쪽 행, 왼쪽 열을 차례로 훑고 훑은 줄만큼 그 쪽 경계를 한 칸 안으로 좁히는 것을 한 바퀴로 반복하면 모든 칸이 정확히 한 번씩 담긴다. 다만 위쪽 행과 오른쪽 열을 훑고 경계를 좁힌 뒤 남은 영역이 비면, 좁히기 전 영역이 한 행이나 한 열뿐이라 그 두 단계에서 이미 다 담긴 것이므로, 반복을 여기서 끝내야 아래쪽 행과 왼쪽 열이 같은 칸을 반대 방향으로 다시 담지 않는다. 한 바퀴를 마친 뒤에는 다음 바퀴의 반복 조건이 같은 검사를 하므로 따로 확인하지 않아도 된다.

---

## 2. 코드

### 풀이 [Java][C++][Python]

```java
import java.util.*;

class Solution {
    public List<Integer> spiralOrder(int[][] matrix) {
        List<Integer> ans = new ArrayList<>();
        int top = 0, bottom = matrix.length - 1;
        int left = 0, right = matrix[0].length - 1;

        while (top <= bottom && left <= right) {
            for (int c = left; c <= right; c++) {
                ans.add(matrix[top][c]);
            }
            top++;

            for (int r = top; r <= bottom; r++) {
                ans.add(matrix[r][right]);
            }
            right--;

            if (top > bottom || left > right) break;

            for (int c = right; c >= left; c--) {
                ans.add(matrix[bottom][c]);
            }
            bottom--;

            for (int r = bottom; r >= top; r--) {
                ans.add(matrix[r][left]);
            }
            left++;
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
    vector<int> spiralOrder(vector<vector<int>>& matrix) {
        vector<int> ans;
        int top = 0, bottom = matrix.size() - 1;
        int left = 0, right = matrix[0].size() - 1;

        while (top <= bottom && left <= right) {
            for (int c = left; c <= right; c++) ans.push_back(matrix[top][c]);
            top++;

            for (int r = top; r <= bottom; r++) ans.push_back(matrix[r][right]);
            right--;

            if (top > bottom || left > right) break;

            for (int c = right; c >= left; c--) ans.push_back(matrix[bottom][c]);
            bottom--;

            for (int r = bottom; r >= top; r--) ans.push_back(matrix[r][left]);
            left++;
        }

        return ans;
    }
};
```

```python
class Solution:
    def spiralOrder(self, matrix: list[list[int]]) -> list[int]:
        ans = []
        top, bottom = 0, len(matrix) - 1
        left, right = 0, len(matrix[0]) - 1

        while top <= bottom and left <= right:
            for c in range(left, right + 1):
                ans.append(matrix[top][c])
            top += 1

            for r in range(top, bottom + 1):
                ans.append(matrix[r][right])
            right -= 1

            if top > bottom or left > right:
                break

            for c in range(right, left - 1, -1):
                ans.append(matrix[bottom][c])
            bottom -= 1

            for r in range(bottom, top - 1, -1):
                ans.append(matrix[r][left])
            left += 1

        return ans
```

---
