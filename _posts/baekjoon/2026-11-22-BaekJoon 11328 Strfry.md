---
title: "[BaekJoon] #11328 - Strfry [Java][C++][Python]"
date: 2026-11-22
categories: [PS, BaekJoon]
tags: ["string"]
slug: baekjoon-11328
media_subpath: /assets/img/posts/baekjoon-11328/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://www.acmicpc.net/problem/11328)
{: .prompt-info }

---

## 1. 아이디어

두 번째 문자열이 첫 번째 문자열의 문자를 재배열한 것, 곧 애너그램이려면 두 문자열에서 문자마다 나온 횟수가 모두 같아야 하고, 반대로 횟수가 모두 같으면 재배열로 만들 수 있다. 소문자가 26종뿐이라 첫 문자열의 문자는 해당 칸에 더하고 두 번째 문자열의 문자는 빼서 26칸이 모두 0이면 가능하다. 두 문자열을 각각 정렬하면 문자 횟수가 같을 때 같은 문자열이 되고 다르면 다른 문자열이 되므로, 정렬한 두 문자열이 같은지 비교해도 같은 판정이다.

---

## 2. 코드

### 풀이 [Java][C++][Python]

```java
import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));

        int t = Integer.parseInt(br.readLine());
        while (t-- > 0) {
            StringTokenizer st = new StringTokenizer(br.readLine());

            int[] cnt = new int[26];
            for (char c : st.nextToken().toCharArray()) {
                cnt[c - 'a']++;
            }
            for (char c : st.nextToken().toCharArray()) {
                cnt[c - 'a']--;
            }

            boolean flag = true;
            for (int x : cnt) {
                if (x != 0) {
                    flag = false;
                    break;
                }
            }

            if (flag) {
                bw.write("Possible\n");
            } else {
                bw.write("Impossible\n");
            }
        }

        bw.flush();
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);

    int t;
    cin >> t;

    while (t--) {
        string s1, s2;
        cin >> s1 >> s2;

        vector<int> cnt(26);
        for (char c : s1) cnt[c - 'a']++;
        for (char c : s2) cnt[c - 'a']--;

        bool flag = true;
        for (int x : cnt) {
            if (x != 0) {
                flag = false;
                break;
            }
        }

        if (flag) {
            cout << "Possible\n";
        } else {
            cout << "Impossible\n";
        }
    }
}
```

```python
import sys

input = sys.stdin.readline

n = int(input())
out = []
for _ in range(n):
    a, b = input().split()
    out.append("Possible" if sorted(a) == sorted(b) else "Impossible")

print("\n".join(out))
```

---
