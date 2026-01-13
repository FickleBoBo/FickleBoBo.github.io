---
title: "[자료구조/알고리즘] 이분 탐색을 활용한 LIS (LIS using Binary Search)"
slug: lis-using-binary-search
date: 2025-11-28
categories: [DSA]
tags: [Dynamic Programming, LIS, Binary Search, Traceback]
toc: true
math: true
image: /assets/posts/lis-using-binary-search/thumbnail.drawio.svg
---

## 1. LIS

<br>

기존 2중 반복문을 활용한 [LIS](/posts/longest-increasing-subsequence) 는 간단하게 구현할 수 있다는 장점이 있지만 $O(N^2)$ 의 시간복잡도라는 성능의 아쉬움이 있었다. LIS를 구하는 과정에서 **이분 탐색**을 활용하면 시간복잡도를 $O(N\log{N})$ 까지 개선할 수 있다.

---

## 2. 이분 탐색을 활용한 LIS

<br>

주어진 수열이 $$\{10, 45, 30, 35, 20, 25, 40, 15\}$$ 일 때 dp 배열이 기존에는 해당 원소를 포함한 LIS의 길이를 저장했다면 이번엔 인덱스를 LIS의 길이로 갖는 가능한 최소 끝 값을 저장하면 된다. 이러면 기존에는 이전에 등장한 원소들을 전부 비교하며 dp를 갱신했다면 이제는 이분 탐색으로 비교할 수 있다.

<br>

주어진 수열은 아래와 같고 LIS의 길이의 최댓값은 수열의 길이와 같으므로 일단 수열의 길이만큼 dp 배열을 만들어준다. 동적 배열을 활용하면 미리 수열의 길이만큼 크기를 잡지 않고 원소의 추가가 발생할 때만 늘려도 된다.

![](/assets/posts/lis-using-binary-search/photo01.drawio.svg)

<br>

첫 번째 원소인 $10$ 에 대해 dp 배열에서 $10$ 이상인 최소 위치를 찾는다. 현재 dp 배열이 비어있으므로 최소 위치는 $1$ 이다.

![](/assets/posts/lis-using-binary-search/photo02.drawio.svg)

<br>

해당 위치에 $10$ 을 넣어준다. dp 배열의 원소의 수가 $1$ 개이므로 현재 LIS의 길이는 $1$ 이며 길이 $1$ 인 LIS의 끝 값의 최솟값은 $10$ 이다.

![](/assets/posts/lis-using-binary-search/photo03.drawio.svg)

<br>

두 번째 원소인 $45$ 에 대해 dp 배열에서 $45$ 이상인 최소 위치를 찾는다. 현재 최소 위치는 $2$ 다.

![](/assets/posts/lis-using-binary-search/photo04.drawio.svg)

<br>

해당 위치에 $45$ 를 넣어준다. dp 배열의 원소의 수가 $2$ 개이므로 현재 LIS의 길이는 $2$ 이며 길이 $1$ 인 LIS의 끝 값의 최솟값은 $10$, 길이 $2$ 인 LIS의 끝 값의 최솟값은 $45$ 다.

![](/assets/posts/lis-using-binary-search/photo05.drawio.svg)

<br>

세 번째 원소인 $30$ 에 대해 dp 배열에서 $30$ 이상인 최소 위치를 찾는다. 현재 최소 위치는 $2$ 다.

![](/assets/posts/lis-using-binary-search/photo06.drawio.svg)

<br>

해당 위치에 $30$ 을 넣어준다. dp 배열의 원소의 수가 $2$ 개이므로 현재 LIS의 길이는 $2$ 이며 길이 $1$ 인 LIS의 끝 값의 최솟값은 $10$, 길이 $2$ 인 LIS의 끝 값의 최솟값은 $30$ 이다.

![](/assets/posts/lis-using-binary-search/photo07.drawio.svg)

<br>

네 번째 원소인 $35$ 에 대해 dp 배열에서 $35$ 이상인 최소 위치를 찾는다. 현재 최소 위치는 $3$ 이다.

![](/assets/posts/lis-using-binary-search/photo08.drawio.svg)

<br>

해당 위치에 $35$ 를 넣어준다. dp 배열의 원소의 수가 $3$ 개이므로 현재 LIS의 길이는 $3$ 이며 길이 $1$ 인 LIS의 끝 값의 최솟값은 $10$, 길이 $2$ 인 LIS의 끝 값의 최솟값은 $30$, 길이 $3$ 인 LIS의 끝 값의 최솟값은 $35$ 다.

![](/assets/posts/lis-using-binary-search/photo09.drawio.svg)

<br>

다섯 번째 원소인 $20$ 에 대해 dp 배열에서 $20$ 이상인 최소 위치를 찾는다. 현재 최소 위치는 $2$ 다.

![](/assets/posts/lis-using-binary-search/photo10.drawio.svg)

<br>

해당 위치에 $20$ 을 넣어준다. dp 배열의 원소의 수가 $3$ 개이므로 현재 LIS의 길이는 $3$ 이며 길이 $1$ 인 LIS의 끝 값의 최솟값은 $10$, 길이 $2$ 인 LIS의 끝 값의 최솟값은 $20$, 길이 $3$ 인 LIS의 끝 값의 최솟값은 $35$ 다.

![](/assets/posts/lis-using-binary-search/photo11.drawio.svg)

<br>

여섯 번째 원소인 $25$ 에 대해 dp 배열에서 $25$ 이상인 최소 위치를 찾는다. 현재 최소 위치는 $3$ 이다.

![](/assets/posts/lis-using-binary-search/photo12.drawio.svg)

<br>

해당 위치에 $25$ 를 넣어준다. dp 배열의 원소의 수가 $3$ 개이므로 현재 LIS의 길이는 $3$ 이며 길이 $1$ 인 LIS의 끝 값의 최솟값은 $10$, 길이 $2$ 인 LIS의 끝 값의 최솟값은 $20$, 길이 $3$ 인 LIS의 끝 값의 최솟값은 $25$ 다.

![](/assets/posts/lis-using-binary-search/photo13.drawio.svg)

<br>

일곱 번째 원소인 $40$ 에 대해 dp 배열에서 $40$ 이상인 최소 위치를 찾는다. 현재 최소 위치는 $4$ 다.

![](/assets/posts/lis-using-binary-search/photo14.drawio.svg)

<br>

해당 위치에 $40$ 을 넣어준다. dp 배열의 원소의 수가 $4$ 개이므로 현재 LIS의 길이는 $4$ 이며 길이 $1$ 인 LIS의 끝 값의 최솟값은 $10$, 길이 $2$ 인 LIS의 끝 값의 최솟값은 $20$, 길이 $3$ 인 LIS의 끝 값의 최솟값은 $25$, 길이 $4$ 인 LIS의 끝 값의 최솟값은 $40$ 이다.

![](/assets/posts/lis-using-binary-search/photo15.drawio.svg)

<br>

마지막 원소인 $15$ 에 대해 dp 배열에서 $15$ 이상인 최소 위치를 찾는다. 현재 최소 위치는 $2$ 다.

![](/assets/posts/lis-using-binary-search/photo16.drawio.svg)

<br>

해당 위치에 $15$ 를 넣어준다. dp 배열의 원소의 수가 $4$ 개이므로 현재 LIS의 길이는 $4$ 이며 길이 $1$ 인 LIS의 끝 값의 최솟값은 $10$, 길이 $2$ 인 LIS의 끝 값의 최솟값은 $15$, 길이 $3$ 인 LIS의 끝 값의 최솟값은 $25$, 길이 $4$ 인 LIS의 끝 값의 최솟값은 $40$ 이다.

![](/assets/posts/lis-using-binary-search/photo17.drawio.svg)

<br>

모든 원소에 대해 탐색했으므로 탐색을 종료하면 되며 dp 배열의 원소 수가 $4$ 개라는 점에서 LIS의 길이가 $4$ 임을 구할 수 있다. dp 배열에서 해당 원소 이상인 최소 위치에 삽입하는 과정에서 항상 정렬된 상태를 유지함을 알 수 있고 이를 통해 Lower Bound 이분 탐색으로 삽입 위치를 $O(\log{N})$ 에 찾을 수 있다. dp 배열은 인덱스 정보가 LIS의 길이를, 값이 해당 길이의 LIS의 끝 값의 최솟값을 가지고 있으므로 새로운 원소가 기존 모든 끝 값보다 크면 LIS의 길이가 늘어나는 것과 작으면 최솟값을 갱신하는 것에서 LIS를 잘 구할 수 있음을 볼 수 있다.

---

## 3. 역추적을 통한 실제 LIS 구하기

<br>

위 방식으로 LIS의 길이는 잘 구할 수 있지만 dp 배열을 갱신하는 과정에서 이전 정보들이 덮어 씌워지기 때문에 dp 배열만 가지고 실제 LIS를 구할 수 없다. 이를 위해 별도의 저장 공간이 필요한데 수열에서 $i$ 번째 원소가 LIS의 몇 번째 자리인지 저장하는 `pos` 배열과, 해당 윈소 앞에오는 LIS 원소의 인덱스를 저장하는 `prev` 배열을 활용하면 된다. 위에서 dp 배열을 갱신하는 과정에 `pos`와 `prev` 배열을 갱신하는 과정을 추가해주자.

$10$ 은 dp 배열의 $0$ 번 인덱스에 위치했다. `pos` 배열의 $0$ 번 인덱스를 해당 원소의 인덱스(0-based)로 갱신해주면 $pos[0] = 0$ 이 된다. `prev` 배열은 $10$ 을 포함한 LIS에서 $10$ 앞에 오는 원소의 인덱스로 갱신하면 되는데 현재 그런 원소가 없으므로 없다는 의미로 $-1$ 로 채워줬다.

![](/assets/posts/lis-using-binary-search/photo18.drawio.svg)

<br>

$45$ 는 dp 배열의 $1$ 번 인덱스에 위치했다. `pos` 배열의 $1$ 번 인덱스를 해당 원소의 인덱스로 갱신해주면 $pos[1] = 1$ 이 된다. `prev` 배열은 $45$ 를 포함한 LIS에서 $45$ 앞에 오는 원소의 인덱스로 갱신하면 되는데 이는 $pos[0] = 0$ 을 통해 알 수 있다. dp 배열이 인덱스를 길이 정보로 갖기 때문에 인덱스가 1 작으면 LIS의 길이가 1 이 짧은 것이기 때문에 이전 인덱스를 통해 찾을 수 있다.

![](/assets/posts/lis-using-binary-search/photo19.drawio.svg)

<br>

$30$ 은 dp 배열의 $1$ 번 인덱스에 위치했다. `pos` 배열의 $1$ 번 인덱스를 해당 원소의 인덱스로 갱신해주면 $pos[1] = 2$ 이 된다. `prev` 배열은 $30$ 을 포함한 LIS에서 $30$ 앞에 오는 원소의 인덱스로 갱신하면 되는데 이는 $pos[0] = 0$ 을 통해 알 수 있다.

![](/assets/posts/lis-using-binary-search/photo20.drawio.svg)

<br>

$35$ 는 dp 배열의 $2$ 번 인덱스에 위치했다. `pos` 배열의 $2$ 번 인덱스를 해당 원소의 인덱스로 갱신해주면 $pos[2] = 3$ 이 된다. `prev` 배열은 $35$ 를 포함한 LIS에서 $35$ 앞에 오는 원소의 인덱스로 갱신하면 되는데 이는 $pos[1] = 2$ 를 통해 알 수 있다.

![](/assets/posts/lis-using-binary-search/photo21.drawio.svg)

<br>

$20$ 은 dp 배열의 $1$ 번 인덱스에 위치했다. `pos` 배열의 $1$ 번 인덱스를 해당 원소의 인덱스로 갱신해주면 $pos[1] = 4$ 가 된다. `prev` 배열은 $20$ 을 포함한 LIS에서 $20$ 앞에 오는 원소의 인덱스로 갱신하면 되는데 이는 $pos[0] = 0$ 을 통해 알 수 있다.

![](/assets/posts/lis-using-binary-search/photo22.drawio.svg)

<br>

$25$ 는 dp 배열의 $2$ 번 인덱스에 위치했다. `pos` 배열의 $2$ 번 인덱스를 해당 원소의 인덱스로 갱신해주면 $pos[2] = 5$ 이 된다. `prev` 배열은 $25$ 를 포함한 LIS에서 $25$ 앞에 오는 원소의 인덱스로 갱신하면 되는데 이는 $pos[1] = 4$ 를 통해 알 수 있다.

![](/assets/posts/lis-using-binary-search/photo23.drawio.svg)

<br>

$40$ 은 dp 배열의 $3$ 번 인덱스에 위치했다. `pos` 배열의 $3$ 번 인덱스를 해당 원소의 인덱스로 갱신해주면 $pos[3] = 6$ 이 된다. `prev` 배열은 $40$ 을 포함한 LIS에서 $40$ 앞에 오는 원소의 인덱스로 갱신하면 되는데 이는 $pos[2] = 5$ 를 통해 알 수 있다.

![](/assets/posts/lis-using-binary-search/photo24.drawio.svg)

<br>

$15$ 는 dp 배열의 $1$ 번 인덱스에 위치했다. `pos` 배열의 $1$ 번 인덱스를 해당 원소의 인덱스로 갱신해주면 $pos[1] = 7$ 이 된다. `prev` 배열은 $15$ 를 포함한 LIS에서 $15$ 앞에 오는 원소의 인덱스로 갱신하면 되는데 이는 $pos[0] = 0$ 을 통해 알 수 있다.

![](/assets/posts/lis-using-binary-search/photo25.drawio.svg)

<br>

이렇게 수열 전체에 대한 `prev` 배열을 `pos` 배열을 통해 구할 수 있었다. 해당 `prev` 배열을 통해 역추적을 하면 실제 LIS를 구할 수 있으며 이는 기존 2중 반복문을 활용한 [LIS](/posts/longest-increasing-subsequence) 에서의 역추적 과정과 동일하다. `prev` 배열의 원소가 약간 다른데 동일한 길이의 다른 LIS 후보에 대해 이전에는 반영하지 않았고 현재는 반영해서 그런 것으로 이전에는 $$\{10, 30, 35, 40\}$$ 보다 나중에 등장한 $$\{10, 20, 25, 40\}$$ 을 반영하지 않았고 현재는 반영했기 때문이다.

---

## 4. Problems

<br>

- [BaekJoon 12015번 - 가장 긴 증가하는 부분 수열 2](https://www.acmicpc.net/problem/12015)
- [BaekJoon 14003번 - 가장 긴 증가하는 부분 수열 5](https://www.acmicpc.net/problem/14003)
- [BaekJoon 13711번 - LCS 4](https://www.acmicpc.net/problem/13711)

---

## Ref

<br>

- [wikipedia - 최장 증가 부분 수열](https://en.wikipedia.org/wiki/Longest_increasing_subsequence)
- [cp-algorithms - Longest Increasing Subsequence](https://cp-algorithms.com/dynamic_programming/longest_increasing_subsequence.html)

---
