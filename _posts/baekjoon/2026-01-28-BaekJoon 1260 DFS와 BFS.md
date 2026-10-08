---
title: "[BaekJoon] #1260 - DFS와 BFS [Java][C++]"
date: 2026-01-28
categories: [PS, BaekJoon]
tags: ["graph", "bfs", "dfs"]
slug: baekjoon-1260
media_subpath: /assets/img/posts/baekjoon-1260/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://www.acmicpc.net/problem/1260)
{: .prompt-info }

---

## 1. 아이디어

주어진 그래프를 DFS로 탐색한 결과와 BFS로 탐색한 결과를 출력하는 문제로 정점 번호가 작은 것을 먼저 방문해야 한다. 인접 리스트를 활용했는데 이때 정점 번호가 작은 것을 먼저 방문할 수 있게 정렬했다. 인접 리스트의 경우 양방향 연결을 해야 함에 주의해야 한다.

---

## 2. 복잡도

| 접근 | 시간              | 공간       |
| ---- | ----------------- | ---------- |
| 풀이 | $O(N + E \log E)$ | $O(N + E)$ |

($N$ = 입력값 `n`, $E$ = 입력값 `m`)

---

## 3. 코드

### 풀이 [Java][C++]

```java
import java.io.*;
import java.util.*;

public class Main {

    static StringBuilder sb = new StringBuilder();
    static List<Integer>[] adj;
    static boolean[] vis;

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());

        int n = Integer.parseInt(st.nextToken());
        int m = Integer.parseInt(st.nextToken());
        int k = Integer.parseInt(st.nextToken());

        adj = new ArrayList[1 + n];
        for (int i = 1; i <= n; i++) {
            adj[i] = new ArrayList<>();
        }

        while (m-- > 0) {
            st = new StringTokenizer(br.readLine());
            int u = Integer.parseInt(st.nextToken());
            int v = Integer.parseInt(st.nextToken());
            adj[u].add(v);
            adj[v].add(u);
        }
        for (int i = 1; i <= n; i++) {
            adj[i].sort(Comparator.naturalOrder());
        }

        vis = new boolean[1 + n];
        dfs(k);

        sb.append("\n");

        vis = new boolean[1 + n];
        bfs(k);

        System.out.println(sb);
    }

    static void dfs(int cur) {
        vis[cur] = true;
        sb.append(cur).append(" ");

        for (int nxt : adj[cur]) {
            if (vis[nxt]) continue;
            dfs(nxt);
        }
    }

    static void bfs(int start) {
        Queue<Integer> q = new ArrayDeque<>();
        q.offer(start);

        vis[start] = true;

        while (!q.isEmpty()) {
            int cur = q.poll();
            sb.append(cur).append(" ");

            for (int nxt : adj[cur]) {
                if (vis[nxt]) continue;

                q.offer(nxt);
                vis[nxt] = true;
            }
        }
    }
}
```

출력을 위해 `StringBuilder`를 활용했다.

```c++
#include <bits/stdc++.h>
using namespace std;

const int MAX_N = 1 + 1000;
vector<int> adj[MAX_N];
bool vis[MAX_N];

void dfs(int cur) {
    vis[cur] = true;
    cout << cur << ' ';

    for (int nxt : adj[cur]) {
        if (vis[nxt]) continue;
        dfs(nxt);
    }
}

void bfs(int start) {
    queue<int> q;
    q.push(start);

    vis[start] = true;

    while (!q.empty()) {
        int cur = q.front();
        q.pop();

        cout << cur << ' ';

        for (int nxt : adj[cur]) {
            if (vis[nxt]) continue;

            q.push(nxt);
            vis[nxt] = true;
        }
    }
}

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);

    int n, m, k;
    cin >> n >> m >> k;

    while (m--) {
        int u, v;
        cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    for (int i = 1; i <= n; i++) {
        sort(adj[i].begin(), adj[i].end());
    }

    dfs(k);

    cout << '\n';

    memset(vis, 0, sizeof(vis));
    bfs(k);
}
```

---
