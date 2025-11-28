---
title: "[알고리즘] 이분 탐색을 활용한 LIS (LIS using Binary Search)"
date: 2025-11-28
categories: [Algorithm, DP]
tags: [다이나믹 프로그래밍, LIS, 이분 탐색, 역추적]
toc: true
math: true
image: /assets/posts/2025-11/이분%20탐색을%20활용한%20LIS%20(LIS%20using%20Binary%20Search)/thumbnail.drawio.svg
---

## LIS

기존 2중 반복문을 활용한 [LIS]({% post_url 2025-11/2025-11-27-최장 증가 부분 수열 (LIS, Longest Increasing Subsequence) %}) 는 간단하게 구현할 수 있다는 장점이 있지만 $O(N^2)$의 시간복잡도라는 성능의 아쉬움이 있었다. LIS를 구하는 과정에서 이분 탐색을 활용하면 시간복잡도를 $O(N\log{N})$까지 개선할 수 있다.

---

## 이분 탐색을 활용한 LIS

주어진 수열이 $$\{10, 45, 30, 35, 20, 25, 40, 15\}$$일 때 dp 배열이 기존에는 해당 원소를 포함한 LIS의 길이를 저장했다면 이번엔 인덱스를 LIS의 길이로 갖는 가능한 최소 끝 값을 저장하면 된다. 이러면 기존에는 이전에 등장한 원소들을 전부 비교하며 dp를 갱신했다면 이제는 이분 탐색으로 비교할 수 있다.

주어진 수열은 아래와 같고 LIS의 길이의 최댓값은 수열의 길이와 같으므로 일단 수열의 길이만큼 dp 배열을 만들어준다.

![](</assets/posts/2025-11/이분%20탐색을%20활용한%20LIS%20(LIS%20using%20Binary%20Search)/photo01.drawio.svg>)

첫 번째 원소인 $10$에 대해 dp 배열에서 $10$ 이상인 최소 위치를 찾는다. 현재 dp 배열이 비어있으므로 최소 위치는 $1$이다.

![](</assets/posts/2025-11/이분%20탐색을%20활용한%20LIS%20(LIS%20using%20Binary%20Search)/photo02.drawio.svg>)

해당 위치에 $10$을 넣어준다. dp 배열의 원소의 수가 $1$개이므로 현재 LIS의 길이는 $1$이며 길이 $1$인 LIS의 끝 값의 최솟값은 $10$이다.

![](</assets/posts/2025-11/이분%20탐색을%20활용한%20LIS%20(LIS%20using%20Binary%20Search)/photo03.drawio.svg>)

두 번째 원소인 $45$에 대해 dp 배열에서 $45$ 이상인 최소 위치를 찾는다. 현재 최소 위치는 $2$다.

![](</assets/posts/2025-11/이분%20탐색을%20활용한%20LIS%20(LIS%20using%20Binary%20Search)/photo04.drawio.svg>)

해당 위치에 $45$를 넣어준다. dp 배열의 원소의 수가 $2$개이므로 현재 LIS의 길이는 $2$이며 길이 $1$인 LIS의 끝 값의 최솟값은 $10$, 길이 $2$인 LIS의 끝 값의 최솟값은 $45$다.

![](</assets/posts/2025-11/이분%20탐색을%20활용한%20LIS%20(LIS%20using%20Binary%20Search)/photo05.drawio.svg>)

세 번째 원소인 $30$에 대해 dp 배열에서 $30$ 이상인 최소 위치를 찾는다. 현재 최소 위치는 $2$다.

![](</assets/posts/2025-11/이분%20탐색을%20활용한%20LIS%20(LIS%20using%20Binary%20Search)/photo06.drawio.svg>)

해당 위치에 $30$을 넣어준다. dp 배열의 원소의 수가 $2$개이므로 현재 LIS의 길이는 $2$이며 길이 $1$인 LIS의 끝 값의 최솟값은 $10$, 길이 $2$인 LIS의 끝 값의 최솟값은 $30$다.

![](</assets/posts/2025-11/이분%20탐색을%20활용한%20LIS%20(LIS%20using%20Binary%20Search)/photo07.drawio.svg>)

네 번째 원소인 $35$에 대해 dp 배열에서 $35$ 이상인 최소 위치를 찾는다. 현재 최소 위치는 $3$이다.

![](</assets/posts/2025-11/이분%20탐색을%20활용한%20LIS%20(LIS%20using%20Binary%20Search)/photo08.drawio.svg>)

해당 위치에 $35$를 넣어준다. dp 배열의 원소의 수가 $3$개이므로 현재 LIS의 길이는 $3$이며 길이 $1$인 LIS의 끝 값의 최솟값은 $10$, 길이 $2$인 LIS의 끝 값의 최솟값은 $30$, 길이 $3$인 LIS의 끝 값의 최솟값은 $35$다.

![](</assets/posts/2025-11/이분%20탐색을%20활용한%20LIS%20(LIS%20using%20Binary%20Search)/photo09.drawio.svg>)

다섯 번째 원소인 $20$에 대해 dp 배열에서 $20$ 이상인 최소 위치를 찾는다. 현재 최소 위치는 $2$다.

![](</assets/posts/2025-11/이분%20탐색을%20활용한%20LIS%20(LIS%20using%20Binary%20Search)/photo10.drawio.svg>)

해당 위치에 $20$을 넣어준다. dp 배열의 원소의 수가 $3$개이므로 현재 LIS의 길이는 $3$이며 길이 $1$인 LIS의 끝 값의 최솟값은 $10$, 길이 $2$인 LIS의 끝 값의 최솟값은 $20$, 길이 $3$인 LIS의 끝 값의 최솟값은 $35$다.

![](</assets/posts/2025-11/이분%20탐색을%20활용한%20LIS%20(LIS%20using%20Binary%20Search)/photo11.drawio.svg>)

여섯 번째 원소인 $25$에 대해 dp 배열에서 $25$ 이상인 최소 위치를 찾는다. 현재 최소 위치는 $3$다.

![](</assets/posts/2025-11/이분%20탐색을%20활용한%20LIS%20(LIS%20using%20Binary%20Search)/photo12.drawio.svg>)

해당 위치에 $25$를 넣어준다. dp 배열의 원소의 수가 $3$개이므로 현재 LIS의 길이는 $3$이며 길이 $1$인 LIS의 끝 값의 최솟값은 $10$, 길이 $2$인 LIS의 끝 값의 최솟값은 $20$, 길이 $3$인 LIS의 끝 값의 최솟값은 $25$다.

![](</assets/posts/2025-11/이분%20탐색을%20활용한%20LIS%20(LIS%20using%20Binary%20Search)/photo13.drawio.svg>)

일곱 번째 원소인 $40$에 대해 dp 배열에서 $40$ 이상인 최소 위치를 찾는다. 현재 최소 위치는 $4$다.

![](</assets/posts/2025-11/이분%20탐색을%20활용한%20LIS%20(LIS%20using%20Binary%20Search)/photo14.drawio.svg>)

해당 위치에 $40$을 넣어준다. dp 배열의 원소의 수가 $4$개이므로 현재 LIS의 길이는 $4$이며 길이 $1$인 LIS의 끝 값의 최솟값은 $10$, 길이 $2$인 LIS의 끝 값의 최솟값은 $20$, 길이 $3$인 LIS의 끝 값의 최솟값은 $25$, 길이 $4$인 LIS의 끝 값의 최솟값은 $40$이다.

![](</assets/posts/2025-11/이분%20탐색을%20활용한%20LIS%20(LIS%20using%20Binary%20Search)/photo15.drawio.svg>)

마지막 원소인 $15$에 대해 dp 배열에서 $15$ 이상인 최소 위치를 찾는다. 현재 최소 위치는 $2$다.

![](</assets/posts/2025-11/이분%20탐색을%20활용한%20LIS%20(LIS%20using%20Binary%20Search)/photo16.drawio.svg>)

해당 위치에 $15$를 넣어준다. dp 배열의 원소의 수가 $4$개이므로 현재 LIS의 길이는 $4$이며 길이 $1$인 LIS의 끝 값의 최솟값은 $10$, 길이 $2$인 LIS의 끝 값의 최솟값은 $15$, 길이 $3$인 LIS의 끝 값의 최솟값은 $25$, 길이 $4$인 LIS의 끝 값의 최솟값은 $40$이다.

![](</assets/posts/2025-11/이분%20탐색을%20활용한%20LIS%20(LIS%20using%20Binary%20Search)/photo17.drawio.svg>)

모든 원소에 대해 탐색했으므로 탐색을 종료하면 되며 dp 배열의 원소 수가 $4$개라는 점에서 LIS의 길이가 $4$임을 구할 수 있다. dp 배열에서 해당 원소 이상인 최소 위치에 삽입하는 과정에서 항상 정렬된 상태를 유지함을 알 수 있고 이를 통해 Lower Bound 이분 탐색으로 삽입 위치를 $O(\log{N})$에 찾을 수 있다. dp 배열은 인덱스 정보가 LIS의 길이를, 값이 해당 길이의 LIS의 끝 값의 최솟값을 가지고 있으므로 새로운 원소가 기존 모든 끝 값보다 크면 LIS의 길이가 늘어나는 것과 작으면 최솟값을 갱신하는 것에서 LIS를 잘 구할 수 있음을 볼 수 있다.

---

## 역추적을 통한 실제 LIS 구하기

위 방식으로 LIS의 길이는 잘 구할 수 있지만 dp 배열을 갱신하는 과정에서 이전 정보들이 덮어 씌워지기 때문에 dp 배열만 가지고 실제 LIS를 구할 수 없다. 이를 위해 별도의 저장 공간이 필요한데 바로 해당 원소가 삽입된 위치를 갖는 배열을 활용하면 된다. 해당 원소가 삽입된 위치는 곧 해당 원소를 끝 값으로 갖는 LIS의 길이이며 이는 $O(N^2)$ 방식의 dp 배열과 동일하다.

동일한 수열에 대해 아래와 같은 과정으로 $prev$ 배열을 채울 수 있다.

첫 번째 원소의 삽입 위치는 $1$이다.

![](</assets/posts/2025-11/이분%20탐색을%20활용한%20LIS%20(LIS%20using%20Binary%20Search)/photo19.drawio.svg>)

두 번째 원소의 삽입 위치는 $2$이다.

![](</assets/posts/2025-11/이분%20탐색을%20활용한%20LIS%20(LIS%20using%20Binary%20Search)/photo21.drawio.svg>)

세 번째 원소의 삽입 위치는 $2$이다.

![](</assets/posts/2025-11/이분%20탐색을%20활용한%20LIS%20(LIS%20using%20Binary%20Search)/photo23.drawio.svg>)

네 번째 원소의 삽입 위치는 $3$이다.

![](</assets/posts/2025-11/이분%20탐색을%20활용한%20LIS%20(LIS%20using%20Binary%20Search)/photo25.drawio.svg>)

다섯 번째 원소의 삽입 위치는 $2$이다.

![](</assets/posts/2025-11/이분%20탐색을%20활용한%20LIS%20(LIS%20using%20Binary%20Search)/photo27.drawio.svg>)

여섯 번째 원소의 삽입 위치는 $3$이다.

![](</assets/posts/2025-11/이분%20탐색을%20활용한%20LIS%20(LIS%20using%20Binary%20Search)/photo29.drawio.svg>)

일곱 번째 원소의 삽입 위치는 $4$이다.

![](</assets/posts/2025-11/이분%20탐색을%20활용한%20LIS%20(LIS%20using%20Binary%20Search)/photo31.drawio.svg>)

마지막 원소의 삽입 위치는 $2$이다.

![](</assets/posts/2025-11/이분%20탐색을%20활용한%20LIS%20(LIS%20using%20Binary%20Search)/photo33.drawio.svg>)

기존 $O(N^2)$ 방식의 dp 배열과 동일한 배열을 얻을 수 있고 이를 역방향 탐색하여 실제 LIS 중 하나를 구할 수 있다.

---
