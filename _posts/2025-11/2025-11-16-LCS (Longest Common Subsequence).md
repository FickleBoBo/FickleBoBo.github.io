---
title: "[알고리즘] LCS (Longest Common Subsequence)"
date: 2025-11-16
categories: [Algorithm]
tags: [다이나믹 프로그래밍, LCS]
toc: true
math: true
image: /assets/posts/2025-11/LCS%20(Longest%20Common%20Subsequence)/image.png
---

## LCS

LCS(Longest Common Subsequence)는 최장 공통 부분 수열이라는 뜻으로 주어진 여러 개의 수열 모두의 부분 수열이 되는 수열들 중에 가장 긴 것을 찾는 문제다. 이 문제를 해결하는 간단한 방법은 다이나믹 프로그래밍을 활용하는 것이다.

---

## 2차원 배열을 활용한 LCS

주어진 두 문자열의 LCS를 구하는 상황을 가정해보자. 문자열은 문자의 수열로 볼 수 있으니 LCS를 구할 수 있다.

$dp[i][j]$를 문자열 $A$의 길이 $i$인 접두사와 문자열 $B$의 길이 $j$인 접두사와의 LCS 길이로 정의하면 다음과 같은 점화식으로 $A$와 $B$의 LCS 길이를 구할 수 있다.

$$
dp[i][j] =
\begin{cases}
0, & \text{if } i = 0 \text{ or } j = 0 \\[8pt]
dp[i-1][j-1] + 1, & \text{if } A[i] = B[j] \\[8pt]
\max(dp[i-1][j],\ dp[i][j-1]), & \text{otherwise}
\end{cases}
$$

문자열 $A$가 $ACAYKP$, 문자열 $B$가 $CAPCAK$ 일 때 LCS를 구하는 과정을 보면 이해가 잘 된다. 두 문자열을 2차원 배열로 표현하면 아래와 같이 문자와 인덱스를 매핑할 수 있다.

<div>
	<table style="border-collapse:collapse; width:100%; text-align:center; table-layout:fixed;">
		<tr>
            <td style="border:1px solid black;">col \ row</td>
			<td style="border:1px solid black;">C</td>
			<td style="border:1px solid black;">A</td>
			<td style="border:1px solid black;">P</td>
			<td style="border:1px solid black;">C</td>
			<td style="border:1px solid black;">A</td>
			<td style="border:1px solid black;">K</td>
		</tr>
		<tr>
			<td style="border:1px solid black;">A</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
		</tr>
        <tr>
			<td style="border:1px solid black;">C</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
		</tr>
        <tr>
            <td style="border:1px solid black;">A</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
		</tr>
        <tr>
            <td style="border:1px solid black;">Y</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
		</tr>
        <tr>
            <td style="border:1px solid black;">K</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
		</tr>
        <tr>
            <td style="border:1px solid black;">P</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
		</tr>
	</table>
</div>

$(1, 1)$은 $A$의 접두사 $A$와 $B$의 접두사 $C$의 LCS로 두 접두사의 끝 문자가 일치하지 않으므로 현재 LCS의 길이는 $0$이다. 이는 $A$의 접두사가 공백이고 $B$의 접두사가 $C$인 상황에서 $A$의 접두사 뒤에 $A$를 붙인 경우 또는 $A$의 접두사가 $A$이고 $B$의 접두사가 공백인 상황에서 $B$의 접두사 뒤에 $C$를 붙인 경우로 볼 수 있다. 현재 끝 문자가 일치하지 않으니 두 경우의 LCS 중 큰 값이 현재 상태의 LCS가 된다.

<div>
	<table style="border-collapse:collapse; width:100%; text-align:center; table-layout:fixed;">
		<tr>
            <td style="border:1px solid black;">col \ row</td>
			<td style="border:1px solid black; background-color:#fb923c;">C</td>
			<td style="border:1px solid black;">A</td>
			<td style="border:1px solid black;">P</td>
			<td style="border:1px solid black;">C</td>
			<td style="border:1px solid black;">A</td>
			<td style="border:1px solid black;">K</td>
		</tr>
		<tr>
			<td style="border:1px solid black; background-color:#fb923c;">A</td>
			<td style="border:1px solid black; background-color:#60a5fa;">0</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
		</tr>
        <tr>
			<td style="border:1px solid black;">C</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
		</tr>
        <tr>
            <td style="border:1px solid black;">A</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
		</tr>
        <tr>
            <td style="border:1px solid black;">Y</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
		</tr>
        <tr>
            <td style="border:1px solid black;">K</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
		</tr>
        <tr>
            <td style="border:1px solid black;">P</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
		</tr>
	</table>
</div>

$(1, 2)$은 $A$의 접두사 $A$와 $B$의 접두사 $CA$의 LCS로 두 접두사의 끝 문자가 일치하므로 현재 LCS의 길이는 $1$이다. 이는 $A$의 접두사가 공백이고 $B$의 접두사가 $C$인 상황에서 두 접두사 뒤에 $A$를 붙인 것으로 볼 수 있다. 공통 부분 문자가 새로 생겼으니 해당 경우의 LCS + 1이 현재의 LCS가 된다.

<div>
	<table style="border-collapse:collapse; width:100%; text-align:center; table-layout:fixed;">
		<tr>
            <td style="border:1px solid black;">col \ row</td>
			<td style="border:1px solid black; background-color:#fb923c;">C</td>
			<td style="border:1px solid black; background-color:#fb923c;">A</td>
			<td style="border:1px solid black;">P</td>
			<td style="border:1px solid black;">C</td>
			<td style="border:1px solid black;">A</td>
			<td style="border:1px solid black;">K</td>
		</tr>
		<tr>
			<td style="border:1px solid black; background-color:#fb923c;">A</td>
			<td style="border:1px solid black;">0</td>
			<td style="border:1px solid black; background-color:#60a5fa;">1</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
		</tr>
        <tr>
			<td style="border:1px solid black;">C</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
		</tr>
        <tr>
            <td style="border:1px solid black;">A</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
		</tr>
        <tr>
            <td style="border:1px solid black;">Y</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
		</tr>
        <tr>
            <td style="border:1px solid black;">K</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
		</tr>
        <tr>
            <td style="border:1px solid black;">P</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
		</tr>
	</table>
</div>

$(1, 3)$은 $A$의 접두사 $A$와 $B$의 접두사 $CAP$의 LCS로 두 접두사의 끝 문자가 일치하지 않으므로 현재 LCS의 길이는 $1$이다. 이는 $A$의 접두사가 공백이고 $B$의 접두사가 $CAP$인 상황에서 $A$의 접두사 뒤에 $A$를 붙인 경우 또는 $A$의 접두사가 $A$이고 $B$의 접두사가 $CA$인 상황에서 $B$의 접두사 뒤에 $P$를 붙인 경우로 볼 수 있다. 현재 끝 문자가 일치하지 않으니 두 경우의 LCS 중 큰 값이 현재 상태의 LCS가 된다.

<div>
	<table style="border-collapse:collapse; width:100%; text-align:center; table-layout:fixed;">
		<tr>
            <td style="border:1px solid black;">col \ row</td>
			<td style="border:1px solid black; background-color:#fb923c;">C</td>
			<td style="border:1px solid black; background-color:#fb923c;">A</td>
			<td style="border:1px solid black; background-color:#fb923c;">P</td>
			<td style="border:1px solid black;">C</td>
			<td style="border:1px solid black;">A</td>
			<td style="border:1px solid black;">K</td>
		</tr>
		<tr>
			<td style="border:1px solid black; background-color:#fb923c;">A</td>
			<td style="border:1px solid black;">0</td>
			<td style="border:1px solid black;">1</td>
			<td style="border:1px solid black; background-color:#60a5fa;">1</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
		</tr>
        <tr>
			<td style="border:1px solid black;">C</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
		</tr>
        <tr>
            <td style="border:1px solid black;">A</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
		</tr>
        <tr>
            <td style="border:1px solid black;">Y</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
		</tr>
        <tr>
            <td style="border:1px solid black;">K</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
		</tr>
        <tr>
            <td style="border:1px solid black;">P</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
			<td style="border:1px solid black;">&nbsp;</td>
		</tr>
	</table>
</div>

이 과정을 반복하면 아래와 같이 dp 테이블을 채울 수 있다.

<div>
	<table style="border-collapse:collapse; width:100%; text-align:center; table-layout:fixed;">
		<tr>
            <td style="border:1px solid black;">col \ row</td>
			<td style="border:1px solid black;">C</td>
			<td style="border:1px solid black;">A</td>
			<td style="border:1px solid black;">P</td>
			<td style="border:1px solid black;">C</td>
			<td style="border:1px solid black;">A</td>
			<td style="border:1px solid black;">K</td>
		</tr>
		<tr>
			<td style="border:1px solid black;">A</td>
			<td style="border:1px solid black;">0</td>
			<td style="border:1px solid black;">1</td>
			<td style="border:1px solid black;">1</td>
			<td style="border:1px solid black;">1</td>
			<td style="border:1px solid black;">1</td>
			<td style="border:1px solid black;">1</td>
		</tr>
        <tr>
			<td style="border:1px solid black;">C</td>
			<td style="border:1px solid black;">1</td>
			<td style="border:1px solid black;">1</td>
			<td style="border:1px solid black;">1</td>
			<td style="border:1px solid black;">2</td>
			<td style="border:1px solid black;">2</td>
			<td style="border:1px solid black;">2</td>
		</tr>
        <tr>
            <td style="border:1px solid black;">A</td>
			<td style="border:1px solid black;">1</td>
			<td style="border:1px solid black;">2</td>
			<td style="border:1px solid black;">2</td>
			<td style="border:1px solid black;">2</td>
			<td style="border:1px solid black;">3</td>
			<td style="border:1px solid black;">3</td>
		</tr>
        <tr>
            <td style="border:1px solid black;">Y</td>
			<td style="border:1px solid black;">1</td>
			<td style="border:1px solid black;">2</td>
			<td style="border:1px solid black;">2</td>
			<td style="border:1px solid black;">2</td>
			<td style="border:1px solid black;">3</td>
			<td style="border:1px solid black;">3</td>
		</tr>
        <tr>
            <td style="border:1px solid black;">K</td>
			<td style="border:1px solid black;">1</td>
			<td style="border:1px solid black;">2</td>
			<td style="border:1px solid black;">2</td>
			<td style="border:1px solid black;">2</td>
			<td style="border:1px solid black;">3</td>
			<td style="border:1px solid black;">4</td>
		</tr>
        <tr>
            <td style="border:1px solid black;">P</td>
			<td style="border:1px solid black;">1</td>
			<td style="border:1px solid black;">2</td>
			<td style="border:1px solid black;">3</td>
			<td style="border:1px solid black;">3</td>
			<td style="border:1px solid black;">3</td>
			<td style="border:1px solid black;">4</td>
		</tr>
	</table>
</div>

이를 통해 두 문자열 $A$, $B$의 어떤 접두사에 대해서든지 LCS의 길이를 구할 수 있다. 2차원 배열을 활용한 다이나믹 프로그래밍은 $A$의 길이가 $N$, $B$의 길이가 $M$일 때, 시간 복잡도는 $O(NM)$, 공간 복잡도는 $O(NM)$ 이다. dp 테이블을 갱신할 때 이전 행의 정보만 필요하다는 점에서 토글링을 활용하면 공간 복잡도를 $O(2 * min(N, M))$까지 줄일 수 있다.

---

## 역추적을 통한 실제 LCS 구하기

위와 같이 2차원 배열을 활용해 LCS의 길이를 구했다면 이를 역추적하는 과정을 통해 실제 LCS가 무엇인지도 찾을 수 있다. 실제 LCS를 찾는 방법은 두 접두사의 끝 문자가 동일할 경우 이를 LCS에 포함된 문자로 선택하고 각 접두사의 끝에서 해당 문자를 탈락시키는 것을 반복하면 된다. 두 접두사의 끝 문자가 동일하지 않을 경우 LCS를 이어 받지 않은 쪽 끝 문자를 탈락시키면 된다.

방금 구한 dp 테이블에 대해 $(6, 6)$부터 역추적하여 아래와 같이 실제 LCS를 얻을 수 있다. 여기서 파란색 칸이 실제 LCS에 포함되는 칸이고 주황색 칸은 탐색 과정에서 거쳐간 칸이다.

<div>
	<table style="border-collapse:collapse; width:100%; text-align:center; table-layout:fixed;">
		<tr>
            <td style="border:1px solid black;">col \ row</td>
			<td style="border:1px solid black;">C</td>
			<td style="border:1px solid black;">A</td>
			<td style="border:1px solid black;">P</td>
			<td style="border:1px solid black;">C</td>
			<td style="border:1px solid black;">A</td>
			<td style="border:1px solid black;">K</td>
		</tr>
		<tr>
			<td style="border:1px solid black;">A</td>
			<td style="border:1px solid black;">0</td>
			<td style="border:1px solid black; background-color:#60a5fa;">1</td>
			<td style="border:1px solid black; background-color:#fb923c;">1</td>
			<td style="border:1px solid black;">1</td>
			<td style="border:1px solid black;">1</td>
			<td style="border:1px solid black;">1</td>
		</tr>
        <tr>
			<td style="border:1px solid black;">C</td>
			<td style="border:1px solid black;">1</td>
			<td style="border:1px solid black;">1</td>
			<td style="border:1px solid black;">1</td>
			<td style="border:1px solid black; background-color:#60a5fa;">2</td>
			<td style="border:1px solid black;">2</td>
			<td style="border:1px solid black;">2</td>
		</tr>
        <tr>
            <td style="border:1px solid black;">A</td>
			<td style="border:1px solid black;">1</td>
			<td style="border:1px solid black;">2</td>
			<td style="border:1px solid black;">2</td>
			<td style="border:1px solid black;">2</td>
			<td style="border:1px solid black; background-color:#60a5fa;">3</td>
			<td style="border:1px solid black;">3</td>
		</tr>
        <tr>
            <td style="border:1px solid black;">Y</td>
			<td style="border:1px solid black;">1</td>
			<td style="border:1px solid black;">2</td>
			<td style="border:1px solid black;">2</td>
			<td style="border:1px solid black;">2</td>
			<td style="border:1px solid black; background-color:#fb923c;">3</td>
			<td style="border:1px solid black;">3</td>
		</tr>
        <tr>
            <td style="border:1px solid black;">K</td>
			<td style="border:1px solid black;">1</td>
			<td style="border:1px solid black;">2</td>
			<td style="border:1px solid black;">2</td>
			<td style="border:1px solid black;">2</td>
			<td style="border:1px solid black;">3</td>
			<td style="border:1px solid black; background-color:#60a5fa;">4</td>
		</tr>
        <tr>
            <td style="border:1px solid black;">P</td>
			<td style="border:1px solid black;">1</td>
			<td style="border:1px solid black;">2</td>
			<td style="border:1px solid black;">3</td>
			<td style="border:1px solid black;">3</td>
			<td style="border:1px solid black;">3</td>
			<td style="border:1px solid black; background-color:#fb923c;">4</td>
		</tr>
	</table>
</div>

역추적을 통한 실제 LCS 구하기는 2차원 배열의 모든 정보가 필요하므로 토글링 기법을 활용했을 때는 실제 LCS를 구할 수 없다.

---

## Ref

- [Samsung S/W 멤버십 기술 블로그 - LCS 알고리즘 최적화](https://infossm.github.io/blog/2025/02/25/LCS-optimization/)

---
