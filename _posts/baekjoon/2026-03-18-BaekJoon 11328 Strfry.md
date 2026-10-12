---
title: "[BaekJoon] #11328 - Strfry [Java][C++]"
date: 2026-03-18
categories: [PS, BaekJoon]
tags: ["string"]
slug: baekjoon-11328
media_subpath: /assets/img/posts/baekjoon-11328/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://www.acmicpc.net/problem/11328)
{: .prompt-info }

---

## 1. 아이디어

`strfry` 함수는 입력된 문자열을 무작위로 재배열하여 새로운 문자열을 만들어내는 함수로 1번째 문자열에 대해 2번째 문자열이 `strfry` 함수를 통해 얻어질 수 있으려면 두 단어가 애너그램 관계에 있으면 된다. 따라서 카운팅 배열을 활용해서 1번째 단어의 문자를 카운팅 배열에 더하고 2번째 단어의 문자를 카운팅 배열에서 뺐을 때 카운팅 배열의 모든 값이 0이면 두 단어가 애너그램 관계에 있어서 얻어질 수 있는 단어이고, 0이 아니면 얻어질 수 없는 단어인 것으로 판정했다.

---

## 2. 복잡도

| 접근 | 시간            | 공간   |
| ---- | --------------- | ------ |
| 풀이 | $O(T \times L)$ | $O(L)$ |

($T$ = 테스트 케이스 수, $L$ = 케이스당 `s1`과 `s2`의 길이의 최댓값)

---

## 3. 코드

### 풀이 [Java][C++]

```java
import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));
        StringTokenizer st;

        int t = Integer.parseInt(br.readLine());
        while (t-- > 0) {
            st = new StringTokenizer(br.readLine());
            String s1 = st.nextToken();
            String s2 = st.nextToken();

            int[] cnt = new int[26];
            for (char c : s1.toCharArray()) {
                cnt[c - 'a']++;
            }
            for (char c : s2.toCharArray()) {
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

int cnt[26];

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);

    int t;
    cin >> t;

    while (t--) {
        string s1, s2;
        cin >> s1 >> s2;

        memset(cnt, 0, sizeof(cnt));
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

---
