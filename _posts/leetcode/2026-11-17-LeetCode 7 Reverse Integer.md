---
title: "[LeetCode] #7 - Reverse Integer [Java][C++]"
date: 2026-11-17
categories: [PS, LeetCode]
tags: ["implementation"]
slug: leetcode-7
media_subpath: /assets/img/posts/leetcode-7/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://leetcode.com/problems/reverse-integer/)
{: .prompt-info }

---

## 1. 아이디어

정수의 자릿수를 낮은 자리부터 하나씩 떼어 결과의 뒤에 붙이면 뒤집힌 수가 되고, 64비트 정수를 쓸 수 없으므로 범위를 벗어나는지는 붙이기 전에 확인해야 한다. 붙이면 결과가 10배가 되므로 결과가 $2^{31} - 1$을 10으로 나눈 몫 214,748,364를 넘거나(음수는 $-2^{31}$을 10으로 나눈 몫 -214,748,364보다 작거나) 하면 어떤 자리를 붙여도 범위를 벗어난다.

결과가 정확히 그 값일 때는 붙일 자리에 따라 갈리지만 따로 확인하지 않아도 된다. 결과가 214,748,364이면 아홉 자리를 붙였는데 아직 붙일 자리가 남았다는 뜻이라 입력은 열 자리 이상이고 32비트 정수는 열 자리를 넘지 않으므로 정확히 열 자리이며, 입력이 $2^{31} - 1$ 이하이므로 열 자리 입력의 맨 앞자리는 2 이하이다. 이 자리가 마지막에 붙으므로 $2^{31} - 1$의 끝자리인 7(음수는 $-2^{31}$의 끝자리인 8)을 넘을 수 없다.

---

## 2. 코드

### 풀이 [Java][C++]

```java
class Solution {
    public int reverse(int x) {
        int ans = 0;
        while (x != 0) {
            int d = x % 10;

            if (ans > Integer.MAX_VALUE / 10 || ans < Integer.MIN_VALUE / 10) return 0;
            ans = ans * 10 + d;
            x /= 10;
        }

        return ans;
    }
}
```

`%`와 `/`는 0 쪽으로 잘라 음수 입력에서도 `d`의 부호가 따라오므로 부호를 따로 처리하지 않았다.

```c++
#include <bits/stdc++.h>
using namespace std;

class Solution {
   public:
    int reverse(int x) {
        int ans = 0;
        while (x != 0) {
            int d = x % 10;

            if (ans > INT_MAX / 10 || ans < INT_MIN / 10) return 0;
            ans = ans * 10 + d;
            x /= 10;
        }

        return ans;
    }
};
```

`%`와 `/`는 0 쪽으로 잘라 음수 입력에서도 `d`의 부호가 따라오므로 부호를 따로 처리하지 않았다.

---
