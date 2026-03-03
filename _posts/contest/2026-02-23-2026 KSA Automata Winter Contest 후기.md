---
title: "2026 KSA Automata Winter Contest 후기"
slug: 2026-ksa-automata-winter-contest
date: 2026-02-23
categories: [PS, Contest]
toc: true
math: true
---

## 1. 후기

<br>

첫 대회로 [2026 KSA Automata Winter Contest](https://www.acmicpc.net/contest/view/1647)에 참여하게 되었다. Solved.ac에서 대회에 참여하거나 한 문제 이상을 풀면 뱃지나 배경을 주는데 이걸 받고 싶어서 가벼운 마음으로 참여했고 대회에서도 100점 이상 달성시 뱃지를, 202.6점 이상 달성시 배경을 지급한다고 했다. 전날 잠을 못자서 체감 난이도가 실버 수준인 문제는 다 풀고 골드 문제는 하나 정도만 풀고 쉬려고 했는데, 문제들을 보니 A, B번 문제는 실버 정도로 C번 부터는 골드 이상으로 보여서 3문제만 풀고 자려고 했다. 언어는 아직 익숙한 Java를 사용했는데 대회가 끝나고 맞힌 사람 현황을 보니 확실히 C++가 압도적으로 많았다.

<br>

![](/assets/posts/2026-ksa-automata-winter-contest/photo01.png)

---

## 2. 문제 풀이

<br>

### [A번](https://www.acmicpc.net/problem/35295) [Java]

최소공배수가 소수가 되는지를 판단하는게 중요해보였는데 소수는 1과 자기 자신만 약수로 가지므로 최소공배수가 소수이려면 한 수는 1, 다른 수는 소수여야한다. 정렬을 통해 주어진 수들을 정렬해줬고 에라토스테네스의 체로 소수 판정을 해줘서 양식에 맞게 출력해주는 식으로 해결했다. 10분 정도 걸려서 해결했다. 소수 판정 로직이 필요해서 체감 난이도는 실버 3 정도였다.

```java
import java.io.*;
import java.util.*;

public class Main {

    static final int MAX = 1000;

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder sb = new StringBuilder();
        StringTokenizer st;

        boolean[] isPrime = sieve();

        int n = Integer.parseInt(br.readLine());

        int[] arr = new int[n];
        st = new StringTokenizer(br.readLine());
        for (int i = 0; i < n; i++) {
            arr[i] = Integer.parseInt(st.nextToken());
        }
        Arrays.sort(arr);

        if (arr[arr.length - 2] == 1 && isPrime[arr[arr.length - 1]]) {
            sb.append("NO");
        } else {
            sb.append("YES\n");
            sb.append(2).append("\n");
            sb.append(arr[arr.length - 2]).append(" ").append(arr[arr.length - 1]);
        }

        System.out.println(sb);
    }

    static boolean[] sieve() {
        boolean[] isPrime = new boolean[1 + MAX];
        Arrays.fill(isPrime, true);
        isPrime[0] = isPrime[1] = false;

        for (int i = 2; i * i <= MAX; i++) {
            if (isPrime[i]) {
                for (int j = i * i; j <= MAX; j += i) {
                    isPrime[j] = false;
                }
            }
        }

        return isPrime;
    }
}
```

<br>

### [B번](https://www.acmicpc.net/problem/35296) [Java]

주어진 출석부를 최소 인원으로 채워야하는 문제로 다른 사람도 한명을 체크해줄 수 있는데 이때 번호가 1 차이나면서 바로 옆 칸이어야 한다. 처음에 단순히 사방탐색으로 했는데 좌우는 1 차이가 아닐수도 있다는 점을 간과했다. 출석부가 한 행인 경우에만 좌우도 체크가 가능하다는 점을 포함해서 조건에 맞게 출력하니 통과가 됐다. 20분 정도 소요됐고 그리디한 접근과 조건 분기 때문에 체감 난이도는 실버 2 정도였다.

```java
import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder sb = new StringBuilder();
        StringTokenizer st = new StringTokenizer(br.readLine());

        int n = Integer.parseInt(st.nextToken());
        int m = Integer.parseInt(st.nextToken());

        char[][] map = new char[n][m];
        for (int i = 0; i < n; i++) {
            map[i] = br.readLine().toCharArray();
        }

        int cnt = 0;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                if (map[i][j] == 'X') {
                    if (i < n - 1 && map[i + 1][j] == 'X') {
                        sb.append(2).append(" ").append(i + 1 + n * j).append(" ").append(i + 2 + n * j).append("\n");
                        map[i][j] = 'O';
                        map[i + 1][j] = 'O';
                    } else if (n == 1 && j < m - 1 && map[i][j + 1] == 'X') {
                        sb.append(2).append(" ").append(i + 1 + n * j).append(" ").append(i + 1 + n * (j + 1)).append("\n");
                        map[i][j] = 'O';
                        map[i][j + 1] = 'O';
                    } else {
                        sb.append(1).append(" ").append(i + 1 + n * j).append("\n");
                        map[i][j] = 'O';
                    }
                    cnt++;
                }
            }
        }

        System.out.println(cnt);
        System.out.println(sb);
    }
}
```

<br>

### [C번](https://www.acmicpc.net/problem/35297) [Java]

주어진 문자열을 KSA가 좋아하는 문자열로 바꾸는 문제로 익숙한 그리디 계열의 문제로 보였는데 생각보다 어려워서 놀랐다. KSA가 반복되는 문자열은 KK, SS, AA, ...를 적당히 붙이고 2개씩 적당히 제거하면 만들 수 있는 것으로 보였는데 정확한 최소 횟수를 어떻게 구하는지가 떠오르지 않았다. 1시간 정도 해보다가 안돼서 그냥 포기하고 D번 문제를 좀 보다가 잤는데 현재 골드 1로 책정된걸 보니 어려운 문제가 맞았다. 체감 난이도도 골드 1 ~ 2 정도였다.

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        String str = br.readLine();
        if (str.length() % 2 == 0) {

        } else {

        }
    }
}
// KSA 반복

// 3
// K(KS)S
// KS

// 6
// K(KS)SA(AK)K
// KSAK

// 9
// K(KS)SA(AK)KS(SA)A
// KSAKSA

// ASKK

```

<br>

### [D번](https://www.acmicpc.net/problem/35298) [Java]

$1$ 부터 $N$ 까지의 수로 이루어진 순열에서 주어진 규칙을 통해 $N^2$ 번 이내에 정렬을 완료할 수 있는지, 있다면 어떤 과정으로 되는지 찾는 문제로 완전히 처음 보는 문제였다. 가능하다면 최소 횟수가 아니어도 출력할 수 있다는데 이런 유형은 처음봐서 접근법 자체가 안떠올랐고 무조건 플래티넘 수준의 문제로 보였다. 혹시 애드 혹 계열이 아닐까하고 고민하다가 모르겠어서 빠르게 포기하고 잤다.

```java
import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder sb = new StringBuilder();
        StringTokenizer st;

        int n = Integer.parseInt(br.readLine());

        int[] arr = new int[n];
        st = new StringTokenizer(br.readLine());
        for (int i = 0; i < n; i++) {
            arr[i] = Integer.parseInt(st.nextToken());
        }


    }
}
// 1 2 4 5 3
// 5 3 1 2 4
// 1 2 5 3 4
// 3 4 1 2 5
// 1 2 3 4 5

// 2 3 1
// 3 1 2
// 1 2 3

// 1 2 4 5 3
// 1 2 5 3 4

// 1 3 2
// 2 1 3
// 3 2 1

```

---
