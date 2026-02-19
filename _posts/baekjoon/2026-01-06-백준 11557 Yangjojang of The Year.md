---
title: "[BaekJoon] 11557번 - Yangjojang of The Year [Java][C++]"
slug: baekjoon-11557
date: 2026-01-06
categories: [PS, BaekJoon]
tags: [Sorting]
toc: true
math: true
---

[문제 링크](https://www.acmicpc.net/problem/11557)

---

## 1. 문제 풀이

<br>

각 테스트 케이스별로 가장 술을 많이 먹는 학교를 구하는 문제로 각 테스트 케이스 내에서 학교 이름은 중복되지 않으며 소비한 술의 양이 같은 학교도 없다. 학교와 소비한 술을 쌍으로 다루고 정렬을 활용하면 해결할 수 있다.

---

## 2. 코드

<br>

### 1. 풀이 [Java]

`Node` 클래스를 활용해 쌍으로 묶고 `Comparable` 인터페이스를 구현해서 소비한 술에 대한 내림차순으로 정렬 기준을 설정해주었다.

```java
import java.io.*;
import java.util.*;

public class Main {

    static class Node implements Comparable<Node> {
        String name;
        int amount;

        public Node(String name, int amount) {
            this.name = name;
            this.amount = amount;
        }

        @Override
        public int compareTo(Node o) {
            return Integer.compare(o.amount, this.amount);
        }
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder sb = new StringBuilder();
        StringTokenizer st;

        int t = Integer.parseInt(br.readLine());
        while (t-- > 0) {
            int n = Integer.parseInt(br.readLine());
            Node[] nodes = new Node[n];

            for (int i = 0; i < n; i++) {
                st = new StringTokenizer(br.readLine());
                String name = st.nextToken();
                int amount = Integer.parseInt(st.nextToken());

                nodes[i] = new Node(name, amount);
            }
            Arrays.sort(nodes);

            sb.append(nodes[0].name).append("\n");
        }

        System.out.print(sb);
    }
}
```

<br>

### 2. 풀이 [C++]

`pair`를 활용해서 쌍으로 묶어줬다. `pair`의 정렬 기준을 그대로 활용하기 위해 `first`를 소비한 술로 넣어줬다.

```c++
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;

    while (t--) {
        int n;
        cin >> n;

        vector<pair<int, string>> v;
        for (int i = 0; i < n; i++) {
            string name;
            int amount;
            cin >> name >> amount;

            v.push_back({amount, name});
        }
        sort(v.begin(), v.end());

        cout << v.back().second << '\n';
    }
}
```

---
