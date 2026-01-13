---
title: "[자료구조/알고리즘] 최장 증가 부분 수열 (LIS, Longest Increasing Subsequence)"
slug: longest-increasing-subsequence
date: 2025-11-27
categories: [DSA]
tags: [Dynamic Programming, LIS, Traceback]
toc: true
math: true
image: /assets/posts/longest-increasing-subsequence/thumbnail.drawio.svg
---

## 1. LIS

<br>

LIS는 Longest Increasing Subsequence의 약자로 **최장 증가 부분 수열**을 의미한다. 컴퓨터 공학에서 LIS 문제는 **주어진 수열에서 오름차순으로 정렬된 가장 긴 부분 수열을 찾는 문제**로 여기서의 부분 수열은 연속적이거나 유일할 필요는 없다. LIS는 DP 문제로 전체 수열의 LIS를 더 작은 부분 수열의 LIS를 통해 구해나가며 기존 계산한 LIS 값들을 활용한다.

---

## 2. 2중 반복문을 활용한 LIS

<br>

주어진 수열이 $$\{10, 45, 30, 35, 20, 25, 40, 15\}$$ 일 때 2중 반복문을 활용하면 간단하게 LIS를 구할 수 있다.

<br>

먼저 주어진 수열과 같은 크기의 dp 배열을 선언해준다. dp 배열은 해당 원소를 포함하는(끝 값으로 갖는) LIS의 길이를 갖는다.

![](/assets/posts/longest-increasing-subsequence/photo01.drawio.svg)

<br>

첫 번째 원소인 $10$ 을 포함하는 LIS의 길이는 $1$ 이므로 해당 dp 배열의 값은 $1$ 이 된다.

![](/assets/posts/longest-increasing-subsequence/photo02.drawio.svg)

<br>

두 번째 원소인 $45$ 를 포함하는 LIS의 길이는 해당 원소 이전까지의 원소들 중 해당 원소보다 작은 원소들의 LIS에서 해당 원소를 뒤에 더하면 LIS가 되므로 해당 dp 배열의 값은 $2$ 이 된다. ($10$ 뒤에 $45$)

![](/assets/posts/longest-increasing-subsequence/photo03.drawio.svg)

<br>

세 번째 원소인 $30$ 을 포함하는 LIS의 길이는 해당 원소 이전까지의 원소들 중 해당 원소보다 작은 원소들의 LIS에서 해당 원소를 뒤에 더하면 LIS가 되므로 해당 dp 배열의 값은 $2$ 이 된다. ($10$ 뒤에 $30$)

![](/assets/posts/longest-increasing-subsequence/photo04.drawio.svg)

<br>

네 번째 원소인 $35$ 를 포함하는 LIS의 길이는 해당 원소 이전까지의 원소들 중 해당 원소보다 작은 원소들의 LIS에서 해당 원소를 뒤에 더하면 LIS가 되므로 해당 dp 배열의 값은 $3$ 이 된다. ($30$ 뒤에 $35$)

$10$ 과 $30$ 모두 $35$ 보다 작은데 이때는 더 긴 LIS를 선택하면 된다.

![](/assets/posts/longest-increasing-subsequence/photo05.drawio.svg)

<br>

다섯 번째 원소인 $20$ 을 포함하는 LIS의 길이는 해당 원소 이전까지의 원소들 중 해당 원소보다 작은 원소들의 LIS에서 해당 원소를 뒤에 더하면 LIS가 되므로 해당 dp 배열의 값은 $2$ 이 된다. ($10$ 뒤에 $20$)

![](/assets/posts/longest-increasing-subsequence/photo06.drawio.svg)

<br>

여섯 번째 원소인 $25$ 를 포함하는 LIS의 길이는 해당 원소 이전까지의 원소들 중 해당 원소보다 작은 원소들의 LIS에서 해당 원소를 뒤에 더하면 LIS가 되므로 해당 dp 배열의 값은 $3$ 이 된다. ($20$ 뒤에 $25$)

![](/assets/posts/longest-increasing-subsequence/photo07.drawio.svg)

<br>

일곱 번째 원소인 $40$ 을 포함하는 LIS의 길이는 해당 원소 이전까지의 원소들 중 해당 원소보다 작은 원소들의 LIS에서 해당 원소를 뒤에 더하면 LIS가 되므로 해당 dp 배열의 값은 $4$ 이 된다. ($35$ 뒤에 $40$ 또는 $25$ 뒤에 $40$)

![](/assets/posts/longest-increasing-subsequence/photo08.drawio.svg)

<br>

마지막 원소인 $15$ 를 포함하는 LIS의 길이는 해당 원소 이전까지의 원소들 중 해당 원소보다 작은 원소들의 LIS에서 해당 원소를 뒤에 더하면 LIS가 되므로 해당 dp 배열의 값은 $2$ 이 된다. ($10$ 뒤에 $15$)

![](/assets/posts/longest-increasing-subsequence/photo09.drawio.svg)

<br>

이렇게 각 원소를 포함하는 LIS의 길이를 dp 배열에 모두 구할 수 있다. dp 배열의 최댓값인 $4$ 가 해당 수열의 LIS가 되며 각 원소에 대한 순회와 각 원소의 앞 원소 중 LIS 후보를 찾는 과정때문에 $O(N^2)$ 의 시간복잡도와 dp 배열을 위한 $O(N)$ 의 공간복잡도가 소요된다.

<br>

2중 반복문을 활용한 LIS에서 dp 배열의 초기값은 자기 자신만으로 LIS가 가능하므로 $1$ 이 되며 점화식은 아래와 같다.

<br>

$$
dp[i] = \max_{\substack{0 \le j < i \\ A[j] < A[i]}} \left( dp[j] + 1 \right)
$$

<br>

2중 반복문을 활용한 LIS는 수열의 길이가 $N$ 일 때, $O(N^2)$ 의 시간복잡도와 $O(N)$ 의 공간복잡도가 소요되는 알고리즘이다.

---

## 3. 역추적을 통한 실제 LIS 구하기

<br>

위 과정을 통해 주어진 수열의 LIS의 길이를 구할 수 있었는데 LIS의 길이 뿐만 아니라 실제 LIS도 구할 수 있다. 실제 LIS를 구하기 위해 $prev$ 라는 임시 배열을 활용하는데 이 $prev$ 에는 dp 배열에 LIS의 갱신을 발생시켰던 원소의 인덱스를 저장한다. 인덱스는 $0$ 이상의 정수이기 때문에 이전의 어떤 원소도 LIS의 갱신을 발생시키지 않았음을 표현하기 위해 초기에는 $-1$ 같은 음수로 초기화하면 된다.

<br>

위 수열에 대해 $prev$ 배열을 구하면 아래와 같다.

![](/assets/posts/longest-increasing-subsequence/photo10.drawio.svg)

<br>

dp 배열에서 최댓값이 위치한 곳이 LIS의 끝 원소이므로 해당 위치부터 $prev$ 배열을 통해 역순으로 LIS를 구할 수 있다. dp 배열의 최댓값이 $4$ 이므로, LIS를 탐색할 초기 위치는 아래와 같다. 표시한 곳과 동일한 인덱스인 $40$ 이 실제 LIS의 마지막 원소가 된다.

![](/assets/posts/longest-increasing-subsequence/photo11.drawio.svg)

<br>

이전에 파란색으로 표시한 칸의 값이 $3$ 이므로 인덱스 $3$ 으로 점프하면 $40$ 이전의 LIS 원소를 구할 수 있다. $35$ 는 실제 LIS의 원소가 된다.

![](/assets/posts/longest-increasing-subsequence/photo12.drawio.svg)

<br>

이전에 파란색으로 표시한 칸의 값이 $2$ 이므로 인덱스 $2$ 으로 점프하면 $35$ 이전의 LIS 원소를 구할 수 있다. $30$ 은 실제 LIS의 원소가 된다.

![](/assets/posts/longest-increasing-subsequence/photo13.drawio.svg)

<br>

이전에 파란색으로 표시한 칸의 값이 $0$ 이므로 인덱스 $0$ 으로 점프하면 $30$ 이전의 LIS 원소를 구할 수 있다. $10$ 은 실제 LIS의 원소가 된다.

![](/assets/posts/longest-increasing-subsequence/photo14.drawio.svg)

<br>

이제 파란색으로 표시한 칸의 값이 $-1$ 이므로 LIS 탐색을 종료한다. 이렇게 실제 LIS인 $$\{10, 30, 35, 40\}$$ 을 구할 수 있다. 역추적을 통한 실제 LIS 계산은 LIS의 길이가 $K$ 일 때, $O(K)$ 의 시간복잡도를 소요된다.

---

## 4. Problems

<br>

- [BaekJoon 11053번 - 가장 긴 증가하는 부분 수열](https://www.acmicpc.net/problem/11053)
- [BaekJoon 11054번 - 가장 긴 바이토닉 부분 수열](https://www.acmicpc.net/problem/11054)
- [BaekJoon 14002번 - 가장 긴 증가하는 부분 수열 4](https://www.acmicpc.net/problem/14002)

---

## Ref

<br>

- [wikipedia - 최장 증가 부분 수열](https://en.wikipedia.org/wiki/Longest_increasing_subsequence)
- [cp-algorithms - Longest Increasing Subsequence](https://cp-algorithms.com/dynamic_programming/longest_increasing_subsequence.html)

---
