---
title: "[LeetCode] 9번 - Palindrome Number [Java][C++]"
slug: leetcode-9
date: 2026-07-25
categories: [PS, LeetCode]
tags: [string, palindrome]
toc: true
math: true
---

[문제 링크](https://leetcode.com/problems/palindrome-number/)

---

## 1. 아이디어

정수 `x`가 팰린드롬이면 `true`를 아니면 `false`를 반환하는 문제로 정수 `x`를 문자열로 변환한 후 팰린드롬인지 확인하는 방식, 정수 `x`의 각 자릿수를 배열로 풀어낸 후 팰린드롬인지 확인하는 방식, 두 가지로 해결했다.

문자열로 변환하는 방식은 말 그대로 문자열로 변환한 후 이를 뒤집은 문자열이 기존 문자열과 일치하는지 여부로 팰린드롬 여부를 판단할 수 있다. `x`의 경우 음수 입력도 들어올 수 있는데 이 경우 `-` 기호로 인해 항상 팰린드롬이 아닌 것 역시 잘 판단할 수 있다.

배열로 변환하는 방식의 경우는 각 자릿수를 쪼개서 담은 배열을 만든 후 배열의 양 끝에서 부터 전부 일치하는 숫자인지 판단하면 된다. 이를 위해 음수인 경우만 먼저 필터링해줬다.

---

## 2. 복잡도

### 1. 문자열 변환

| 시간복잡도  | 공간복잡도  |
| :---------: | :---------: |
| $O(\log x)$ | $O(\log x)$ |

### 2. 배열 변환

| 시간복잡도  | 공간복잡도  |
| :---------: | :---------: |
| $O(\log x)$ | $O(\log x)$ |

---

## 3. 코드

### 1. 문자열 변환 [Java][C++]

`StringBuilder`의 `reverse` 메서드를 활용하면 간단하게 구현할 수 있다.

```java
class Solution {
    public boolean isPalindrome(int x) {
        String str = Integer.toString(x);
        String rev = new StringBuilder(str).reverse().toString();

        return str.equals(rev);
    }
}
```

`string`의 범위 생성자와 역방향 이터레이터를 활용하면 간단하게 구현할 수 있다.

```c++
#include <bits/stdc++.h>
using namespace std;

class Solution {
   public:
    bool isPalindrome(int x) {
        string str = to_string(x);
        string rev(str.rbegin(), str.rend());

        return str == rev;
    }
};
```

### 2. 배열 변환 [Java][C++]

숫자의 길이를 알 수 없어서 `List`를 활용했다. 원소가 `Integer` 타입이긴 하지만 자릿수라 `0` ~ `9` 사이의 숫자라서 `Integer`의 캐싱 범위 내이기 때문에 참조 비교로 탐색했다.

```java
import java.util.*;

class Solution {
    public boolean isPalindrome(int x) {
        if (x < 0) return false;

        List<Integer> list = new ArrayList<>();
        while (x != 0) {
            list.add(x % 10);
            x /= 10;
        }

        for (int i = 0; i < list.size() / 2; i++) {
            if (list.get(i) != list.get(list.size() - 1 - i)) return false;
        }

        return true;
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

class Solution {
   public:
    bool isPalindrome(int x) {
        if (x < 0) return false;

        vector<int> v;
        while (x != 0) {
            v.push_back(x % 10);
            x /= 10;
        }

        for (int i = 0; i < v.size() / 2; i++) {
            if (v[i] != v[(int)v.size() - 1 - i]) return false;
        }

        return true;
    }
};
```

---
