---
title: "[자료구조/알고리즘] 최장 공통 부분 문자열 (LCS, Longest Common Substring)"
slug: longest-common-substring
date: 2025-12-27
categories: [DSA]
tags: [Strings, Dynamic Programming, LCS]
toc: true
math: true
image: /assets/posts/longest-common-substring/thumbnail.drawio.svg
---

## 1. LCS

<br>

LCS(Longest Common Substring)는 최장 공통 부분 문자열이라는 뜻으로 주어진 여러 개의 문자열 모두의 부분 문자열이 되는 문자열들 중에 가장 긴 것을 찾는 문제다. 최장 공통 부분 수열인 [LCS(Longest Common Subsequence)](/posts/longest-common-subsequence) 와는 다르다는 것에 주의해야 한다. 최장 공통 부분 수열과 마찬가지로 최장 공통 부분 문자열 역시 다이나믹 프로그래밍을 활용해 해결할 수 있다.

---

## 2. 2차원 배열을 활용한 LCS

<br>

최장 공통 부분 문자열 LCS의 점화식은 아래와 같다.

<br>

$$
dp[i][j] =
\begin{cases}
dp[i-1][j-1] + 1, & \text{if } A[i] = B[j] \\\\
0, & \text{otherwise}
\end{cases}
$$

<br>

실제 문자열들에 대해 최장 공통 부분 문자열을 구하는 과정은 최장 공통 부분 수열을 구하는 과정과 거의 유사한데 끝 문자가 일치하지 않으면 최댓값으로 갱신하던 것과 달리 끝 문자가 일치하지 않으면 서로 다른 문자열이므로 $0$ 이 된다.

---

## 3. Problems

<br>

- [BaekJoon 5582번 - 공통 부분 문자열](https://www.acmicpc.net/problem/5582)

---
