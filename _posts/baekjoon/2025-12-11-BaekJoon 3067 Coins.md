---
title: "[BaekJoon] #3067 - Coins [Java][C++]"
date: 2025-12-11
categories: [PS, BaekJoon]
tags: ["dynamic programming", "knapsack"]
slug: baekjoon-3067
media_subpath: /assets/img/posts/baekjoon-3067/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://www.acmicpc.net/problem/3067)
{: .prompt-info }

---

## 1. 아이디어

$N$가지 동전을 무한히 사용할 수 있을 때 그 합이 $M$이 되는 경우의 수를 구하는 문제다. 일종의 무한 배낭 문제로 여기서는 최댓값이 아닌 모든 경우의 수를 구해야 한다.

경우의 수는 현재 동전을 고려하는 상황에서 현재 동전을 사용하지 않을 경우 이전 동전들로만 만들 수 있었던 경우의 수만큼은 만들 수 있다. 현재 동전을 사용하는 경우 이전 동전들로만 만들 수 있었으면서 현재 동전의 가치만큼 더 적게 담은 배낭에서 담지 않고 현재 동전까지 사용했을 수 있으면서 현재 동전의 가치만큼 더 적게 담은 배낭에서 담아야 한다. 그래야 현재 동전을 여러 번 사용하는 경우까지 전부 셀 수 있다.

어떤 동전도 사용하지 않았을 때 0원을 만드는 경우의 수는 1가지이므로 `dp` 테이블을 해당 값으로 초기화한 후 갱신하며 구하면 된다.

---

## 2. 복잡도

| 접근           | 시간                     | 공간            |
| -------------- | ------------------------ | --------------- |
| 배열 DP        | $O(T \times N \times M)$ | $O(N \times M)$ |
| 공간 최적화 DP | $O(T \times N \times M)$ | $O(N + M)$      |

($T$ = 테스트 케이스 수, $N$ = 케이스당 입력값 `n`의 최댓값, $M$ = 케이스당 입력값 `m`의 최댓값)

---

## 3. 코드

### 풀이 1: 배열 DP [Java][C++]

```java
import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder sb = new StringBuilder();
        StringTokenizer st;

        int t = Integer.parseInt(br.readLine());
        while (t-- > 0) {
            int n = Integer.parseInt(br.readLine());

            int[] coins = new int[1 + n];
            st = new StringTokenizer(br.readLine());
            for (int i = 1; i <= n; i++) {
                coins[i] = Integer.parseInt(st.nextToken());
            }

            int m = Integer.parseInt(br.readLine());

            int[][] dp = new int[1 + n][1 + m];
            dp[0][0] = 1;  // 어떤 동전도 사용하지 않았을 때 0원을 만드는 경우는 1가지
            for (int i = 1; i <= n; i++) {
                int coin = coins[i];

                for (int j = 0; j <= m; j++) {
                    if (j < coin) {
                        dp[i][j] = dp[i - 1][j];
                    } else {
                        dp[i][j] = dp[i - 1][j] + dp[i][j - coin];
                    }
                }
            }

            sb.append(dp[n][m]).append("\n");
        }

        System.out.println(sb);
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

int dp[1 + 20][1 + 10000];

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);

    int t;
    cin >> t;

    while (t--) {
        int n;
        cin >> n;

        vector<int> coins(n);
        for (int& x : coins) cin >> x;

        int m;
        cin >> m;

        memset(dp, 0, sizeof(dp));
        dp[0][0] = 1;  // 어떤 동전도 사용하지 않았을 때 0원을 만드는 경우는 1가지
        for (int i = 1; i <= n; i++) {
            int coin = coins[i - 1];

            for (int j = 0; j <= m; j++) {
                if (j < coin) {
                    dp[i][j] = dp[i - 1][j];
                } else {
                    dp[i][j] = dp[i - 1][j] + dp[i][j - coin];
                }
            }
        }

        cout << dp[n][m] << '\n';
    }
}
```

---

### 풀이 2: 공간 최적화 DP [Java][C++]

```java
import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder sb = new StringBuilder();
        StringTokenizer st;

        int t = Integer.parseInt(br.readLine());
        while (t-- > 0) {
            int n = Integer.parseInt(br.readLine());

            int[] coins = new int[n];
            st = new StringTokenizer(br.readLine());
            for (int i = 0; i < n; i++) {
                coins[i] = Integer.parseInt(st.nextToken());
            }

            int m = Integer.parseInt(br.readLine());

            int[] dp = new int[1 + m];
            dp[0] = 1;  // 어떤 동전도 사용하지 않았을 때 0원을 만드는 경우는 1가지
            for (int coin : coins) {
                for (int j = coin; j <= m; j++) {
                    dp[j] += dp[j - coin];
                }
            }

            sb.append(dp[m]).append("\n");
        }

        System.out.println(sb);
    }
}
```

```c++
#include <bits/stdc++.h>
using namespace std;

int dp[1 + 10000];

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);

    int t;
    cin >> t;

    while (t--) {
        int n;
        cin >> n;

        vector<int> coins(n);
        for (int& x : coins) cin >> x;

        int m;
        cin >> m;

        memset(dp, 0, sizeof(dp));
        dp[0] = 1;  // 어떤 동전도 사용하지 않았을 때 0원을 만드는 경우는 1가지
        for (int coin : coins) {
            for (int j = coin; j <= m; j++) {
                dp[j] += dp[j - coin];
            }
        }

        cout << dp[m] << '\n';
    }
}
```

---
