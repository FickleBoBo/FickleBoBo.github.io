---
title: "[알고리즘] 최장 증가 부분 수열 (LIS, Longest Increasing Subsequence)"
date: 2025-11-27
categories: [Algorithm, DP]
tags: [다이나믹 프로그래밍, LIS, 역추적]
toc: true
math: true
image: /assets/posts/2025-11/최장%20증가%20부분%20수열%20(LIS,%20Longest%20Increasing%20Subsequence)/thumbnail.drawio.svg
---

## LIS

LIS는 Longest Increasing Subsequence의 약자로 최장 증가 부분 수열을 의미한다. 컴퓨터 공학에서 LIS 문제는 주어진 수열에서 오름차순으로 정렬된 가장 긴 부분 수열을 찾는 문제로 여기서의 부분 수열은 연속적이거나 유일할 필요는 없다. LIS는 DP 문제로 전체 수열의 LIS를 더 작은 부분 수열의 LIS를 통해 구해나가며 기존 계산한 LIS 값들을 활용한다.

---

## 2중 반복문을 활용한 LIS

주어진 수열이 $$\{10, 45, 30, 35, 20, 25, 40, 15\}$$일 때 2중 반복문을 활용하면 간단하게 LIS를 구할 수 있다.

먼저 주어진 수열과 같은 크기의 dp 배열을 선언해준다. dp 배열은 해당 원소를 포함하는 LIS의 길이다.

![](</assets/posts/2025-11/최장%20증가%20부분%20수열%20(LIS,%20Longest%20Increasing%20Subsequence)/photo01.drawio.svg>)

첫 번째 원소인 $10$을 포함하는 LIS의 길이는 $1$이므로 해당 dp 배열의 값은 $1$이 된다.

![](</assets/posts/2025-11/최장%20증가%20부분%20수열%20(LIS,%20Longest%20Increasing%20Subsequence)/photo02.drawio.svg>)

두 번째 원소인 $45$를 포함하는 LIS의 길이는 해당 원소 이전까지의 원소들 중 해당 원소보다 작은 원소들의 LIS에서 해당 원소를 뒤에 더하면 LIS가 되므로 해당 dp 배열의 값은 $2$이 된다. (10 뒤에 45)

![](</assets/posts/2025-11/최장%20증가%20부분%20수열%20(LIS,%20Longest%20Increasing%20Subsequence)/photo03.drawio.svg>)

세 번째 원소인 $30$을 포함하는 LIS의 길이는 해당 원소 이전까지의 원소들 중 해당 원소보다 작은 원소들의 LIS에서 해당 원소를 뒤에 더하면 LIS가 되므로 해당 dp 배열의 값은 $2$이 된다. (10 뒤에 30)

![](</assets/posts/2025-11/최장%20증가%20부분%20수열%20(LIS,%20Longest%20Increasing%20Subsequence)/photo04.drawio.svg>)

네 번째 원소인 $35$를 포함하는 LIS의 길이는 해당 원소 이전까지의 원소들 중 해당 원소보다 작은 원소들의 LIS에서 해당 원소를 뒤에 더하면 LIS가 되므로 해당 dp 배열의 값은 $3$이 된다. (30 뒤에 35)

![](</assets/posts/2025-11/최장%20증가%20부분%20수열%20(LIS,%20Longest%20Increasing%20Subsequence)/photo05.drawio.svg>)

다섯 번째 원소인 $20$을 포함하는 LIS의 길이는 해당 원소 이전까지의 원소들 중 해당 원소보다 작은 원소들의 LIS에서 해당 원소를 뒤에 더하면 LIS가 되므로 해당 dp 배열의 값은 $2$이 된다. (10 뒤에 20)

![](</assets/posts/2025-11/최장%20증가%20부분%20수열%20(LIS,%20Longest%20Increasing%20Subsequence)/photo06.drawio.svg>)

여섯 번째 원소인 $25$를 포함하는 LIS의 길이는 해당 원소 이전까지의 원소들 중 해당 원소보다 작은 원소들의 LIS에서 해당 원소를 뒤에 더하면 LIS가 되므로 해당 dp 배열의 값은 $3$이 된다. (20 뒤에 25)

![](</assets/posts/2025-11/최장%20증가%20부분%20수열%20(LIS,%20Longest%20Increasing%20Subsequence)/photo07.drawio.svg>)

일곱 번째 원소인 $40$을 포함하는 LIS의 길이는 해당 원소 이전까지의 원소들 중 해당 원소보다 작은 원소들의 LIS에서 해당 원소를 뒤에 더하면 LIS가 되므로 해당 dp 배열의 값은 $4$이 된다. (35 뒤에 40 또는 25 뒤에 40)

![](</assets/posts/2025-11/최장%20증가%20부분%20수열%20(LIS,%20Longest%20Increasing%20Subsequence)/photo08.drawio.svg>)

마지막 원소인 $15$를 포함하는 LIS의 길이는 해당 원소 이전까지의 원소들 중 해당 원소보다 작은 원소들의 LIS에서 해당 원소를 뒤에 더하면 LIS가 되므로 해당 dp 배열의 값은 $2$이 된다. (10 뒤에 15)

![](</assets/posts/2025-11/최장%20증가%20부분%20수열%20(LIS,%20Longest%20Increasing%20Subsequence)/photo09.drawio.svg>)

이렇게 각 원소를 포함하는 LIS의 길이를 dp 배열에 모두 구할 수 있다. dp 배열의 최댓값인 $4$가 해당 수열의 LIS가 되며 각 원소에 대한 순회와 각 원소의 앞 원소 중 LIS 후보를 찾는 과정때문에 $O(N^2)$의 시간복잡도와 dp 배열을 위한 $O(N)$의 공간복잡도가 소요된다.

위 dp 과정에 대한 점화식은 아래와 같다.

초기값 (자기 자신만으로 LIS)

$$
dp[i] = 1
$$

점화식

$$
dp[i] = \max_{\substack{0 \le j < i \\ A[j] < A[i]}} \left( dp[j] + 1 \right)
$$

$$
\text{LIS 길이} = \max_{0 \le i < N} dp[i]
$$

---

## 역추적을 통한 실제 LIS 구하기

위 과정을 통해 주어진 수열의 LIS의 길이를 구할 수 있었는데 dp 배열을 활용하면 실제 LIS도 구할 수 있다. 포인트는 역방향으로 dp 배열을 조회하며 LIS의 길이와 일치하면 해당 원소를 포함하고 다시 길이가 1 작은 LIS에 대해 같은 과정을 반복하는 것이다.

마지막 값인 $2$는 LIS의 길이인 $4$가 아니므로 LIS 후보가 아니다.

![](</assets/posts/2025-11/최장%20증가%20부분%20수열%20(LIS,%20Longest%20Increasing%20Subsequence)/photo10.drawio.svg>)

일곱 번째 값인 $4$는 LIS의 길이인 $4$이므로 LIS 후보다.

![](</assets/posts/2025-11/최장%20증가%20부분%20수열%20(LIS,%20Longest%20Increasing%20Subsequence)/photo11.drawio.svg>)

해당 위치를 확정하고 이제 LIS의 길이 $3$인 값을 찾는다.

![](</assets/posts/2025-11/최장%20증가%20부분%20수열%20(LIS,%20Longest%20Increasing%20Subsequence)/photo12.drawio.svg>)

여섯 번째 값인 $3$은 LIS의 길이인 $3$이므로 LIS 후보다.

![](</assets/posts/2025-11/최장%20증가%20부분%20수열%20(LIS,%20Longest%20Increasing%20Subsequence)/photo13.drawio.svg>)

해당 위치를 확정하고 이제 LIS의 길이 $2$인 값을 찾는다.

![](</assets/posts/2025-11/최장%20증가%20부분%20수열%20(LIS,%20Longest%20Increasing%20Subsequence)/photo14.drawio.svg>)

다섯 번째 값인 $2$는 LIS의 길이인 $2$이므로 LIS 후보다.

![](</assets/posts/2025-11/최장%20증가%20부분%20수열%20(LIS,%20Longest%20Increasing%20Subsequence)/photo15.drawio.svg>)

해당 위치를 확정하고 이제 LIS의 길이 $1$인 값을 찾는다.

![](</assets/posts/2025-11/최장%20증가%20부분%20수열%20(LIS,%20Longest%20Increasing%20Subsequence)/photo16.drawio.svg>)

네 번째 값인 $3$은 LIS의 길이인 $1$이 아니므로 LIS 후보가 아니다.

![](</assets/posts/2025-11/최장%20증가%20부분%20수열%20(LIS,%20Longest%20Increasing%20Subsequence)/photo17.drawio.svg>)

세 번째 값인 $2$는 LIS의 길이인 $1$이 아니므로 LIS 후보가 아니다.

![](</assets/posts/2025-11/최장%20증가%20부분%20수열%20(LIS,%20Longest%20Increasing%20Subsequence)/photo18.drawio.svg>)

두 번째 값인 $2$는 LIS의 길이인 $1$이 아니므로 LIS 후보가 아니다.

![](</assets/posts/2025-11/최장%20증가%20부분%20수열%20(LIS,%20Longest%20Increasing%20Subsequence)/photo19.drawio.svg>)

첫 번째 값인 $1$은 LIS의 길이인 $1$이므로 LIS 후보다.

![](</assets/posts/2025-11/최장%20증가%20부분%20수열%20(LIS,%20Longest%20Increasing%20Subsequence)/photo20.drawio.svg>)

해당 위치를 확정하고 탐색을 종료한다.

![](</assets/posts/2025-11/최장%20증가%20부분%20수열%20(LIS,%20Longest%20Increasing%20Subsequence)/photo21.drawio.svg>)

위 과정을 통해 실제 LIS를 구할 수 있었다. 해당 수열의 경우 $$\{10, 20, 25, 40\}$$말고도 $$\{10, 30, 35, 40\}$$ 역시 LIS인데 위 과정의 경우 여러 LIS 중 하나만 구할 수 있었다. 하나의 LIS 후보만 구해야한다면 위 방법으로 간단하게 해결할 수 있다.

위 과정에서 1, 2, 3, 4를 아무렇게나 뽑으면 안되는데 첫 번째, 두 번째, 여섯 번째, 일곱 번째를 뽑을 경우 1, 2, 3, 4는 되지만 실제 부분 수열은 $$\{10, 45, 25, 40\}$$이 돼서 LIS가 아니다. 역방향으로 조회하며 LIS의 길이와 값이 일치하는 위치를 바로 뽑으면 항상 LIS가 되는데 이는 직전 원소가 LIS 후보가 안될 경우 애초에 LIS의 길이가 일치할 수 없기 때문이다.

예를 들면 여섯 번째 원소를 확정한 후 LIS의 길이가 $2$인 위치를 찾을 때, 다섯 번째 원소가 $2$가 되므로 바로 뽑으면 된다. 만약 다섯 번째 원소가 $2$인데 LIS 후보가 아닐 경우 여섯 번째 원소를 $3$으로 만들어준 $2$가 다섯 번째보다 앞에 있다는 말인데 그럼 해당 원소가 다섯 번째 원소도 $3$으로 만들어야 해서 모순이 발생한다.

---

## Ref

- [wikipedia - 최장 증가 부분 수열](https://en.wikipedia.org/wiki/Longest_increasing_subsequence)

---
