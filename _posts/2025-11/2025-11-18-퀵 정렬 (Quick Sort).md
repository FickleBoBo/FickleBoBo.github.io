---
title: "[알고리즘] 퀵 정렬 (Quick Sort)"
date: 2025-11-18
categories: [Algorithm, Sort]
tags: [정렬, 분할 정복]
toc: true
math: true
image: /assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/thumbnail.drawio.svg
---

## 퀵 정렬

퀵 정렬은 정렬 알고리즘 중 하나로 분할 정복을 통해 정렬하는 알고리즘이다. 이름 그대로 빠른 정렬이 특징인 정렬 알고리즘이다.

---

## 퀵 정렬 성능

| 평균 시간복잡도 | $O(N\log{N})$ |
| --------------- | ------------- |
| 최선 시간복잡도 | $O(N\log{N})$ |
| 최악 시간복잡도 | $O(N^2)$      |
| 평균 공간복잡도 | $O(\log{N})$  |
| 최악 공간복잡도 | $O(N)$        |

$N$개의 원소에 대한 퀵 정렬은 최선, 평균 시간복잡도가 $O(N\log{N})$으로 빠른 정렬 알고리즘이다. 심지어 동일한 시간 복잡도인 병합 정렬이나 힙 정렬보다도 일반적으로 더 빠른 정렬 성능을 보여준다. 퀵 정렬은 정렬에 피봇(Pivot)이라는 기준점을 활용하는데, 이 피봇이 어떻게 설정되느냐에 따라 분할의 균등 정도가 달라져서 성능 차이가 심하다. 이 피봇을 구간의 첫 번째, 마지막, 중간, 랜덤 값 등 설정하는 다양한 방법이 있으며 피봇을 여러 개 두기도 한다.

퀵 정렬은 제자리 정렬(In-place Sort)로 정렬을 위한 공간복잡도가 $O(1)$인데 재귀 스택이 $\log{N}$만큼 쌓여서 전체 공간복잡도는 $O(\log{N})$이 된다. 최악의 경우 각 원소마다 재귀 스택이 쌓여서 $O(N)$이 될 수도 있다.

퀵 정렬은 정렬 과정이 두 원소의 교환으로 이루어져서 순서가 유지되지 않는 불안정 정렬(Unstable Sort)이다.

---

## 퀵 정렬 진행 과정

퀵 정렬은 주어진 원소들에 대해 파티션을 나누며 정렬을 수행하고 이 과정이 재귀적으로 일어난다. 이 파티션을 나누며 정렬하는 방법은 크게 Lomuto Partition 방식과 Hoare Partition 방식이 있다. Lomuto Partition은 좀 더 이해하기 쉽지만 성능은 약간 떨어지며, Hoare Partition은 좀 더 이해하기 어렵지만 성능은 더 좋다. 일반적으로 퀵 정렬이라고 하면 Hoare Partition을 말한다.

### Lomuto Partition

Lomuto Partition은 주어진 구간의 마지막 원소를 피봇으로 선택하고 이 피봇이 들어갈 자리를 찾는 방식으로 동작한다. 피봇이 들어갈 자리를 정확하게 찾아내며 피봇으로 분할할 수 있는 좌우 구간에 대해 이 과정을 재귀적으로 반복한다. 피봇의 위치를 주어진 구간의 마지막 원소로 꼭 할 필요는 없지만 마지막 원소로 하는 것이 일반적인 구현 방법이며 실수의 여지가 없고 직관적이다.

주어진 수들이 $[4, 1, 8, 3, 6, 10, 8, 4]$일 경우 오름차순 Lomuto Partition은 아래와 같이 진행된다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo001.drawio.svg>)

피봇은 주어진 구간의 마지막 원소로 노란색 칸으로 표시했다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo002.drawio.svg>)

아래 검은 막대를 기준으로 피봇보다 작거나 같은 값은 왼쪽에 위치시킬 예정이고 파란 칸은 현재 교환을 위해 바라보는 칸이다. 파란 칸이 탐색하는 구간은 주어진 구간의 첫 번째 원소부터 피봇 전까지이다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo003.drawio.svg>)

1번 원소는 피봇과 동일한 값이므로 검은 막대를 한 칸 이동한다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo004.drawio.svg>)

검은 막대에 새로 포함된 원소와 파란 칸이 바라보는 원소를 교환한다. 현재는 자기 자신과 교환하는 꼴이다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo005.drawio.svg>)

검은 막대 왼쪽에는 피봇보다 작거나 같은 값만 위치하게 됐다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo006.drawio.svg>)

파란 칸을 한 칸 이동한다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo007.drawio.svg>)

2번 원소는 피봇보다 작은 값이므로 검은 막대를 한 칸 이동한다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo008.drawio.svg>)

검은 막대에 새로 포함된 원소와 파란 칸이 바라보는 원소를 교환한다. 현재는 자기 자신과 교환하는 꼴이다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo009.drawio.svg>)

검은 막대 왼쪽에는 피봇보다 작거나 같은 값만 위치하게 됐다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo010.drawio.svg>)

파란 칸을 한 칸 이동한다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo011.drawio.svg>)

3번 원소는 피봇보다 큰 값이므로 한 칸 이동한다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo012.drawio.svg>)

4번 원소는 피봇보다 작은 값이므로 검은 막대를 한 칸 이동한다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo013.drawio.svg>)

검은 막대에 새로 포함된 원소와 파란 칸이 바라보는 원소를 교환한다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo014.drawio.svg>)

검은 막대 왼쪽에는 피봇보다 작거나 같은 값만 위치하게 됐다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo015.drawio.svg>)

파란 칸을 한 칸 이동한다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo016.drawio.svg>)

5번 원소는 피봇보다 큰 값이므로 한 칸 이동한다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo017.drawio.svg>)

6번 원소는 피봇보다 큰 값이므로 한 칸 이동한다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo018.drawio.svg>)

7번 원소는 피봇보다 큰 값이라 교환이 일어나지 않고 탐색이 끝났다. 탐색이 종료되면 피봇과 검은 막대 바로 오른쪽 원소를 교환한다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo019.drawio.svg>)

교환이 완료된 모습으로 피봇은 주어진 구간에서 정렬된 적절한 곳에 위치하게 됐다. 방금 교환으로 3번의 $8$이 7번의 $8$보다 오른쪽에 위치하게 됐으며 이런 서로 떨어진 원소의 교환 과정 때문에 퀵 정렬은 불안정 정렬이다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo020.drawio.svg>)

피봇의 위치는 확정됐으며 피봇의 왼쪽 구간, 오른쪽 구간에 대해 방금의 탐색 과정을 재귀적으로 반복한다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo021.drawio.svg>)

왼쪽 구간은 1번, 2번, 4번 원소며 동일하게 탐색을 수행한다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo022.drawio.svg>)

파란 칸의 원소가 피봇보다 크므로 한 칸 이동한다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo023.drawio.svg>)

파란 칸의 원소가 피봇보다 작거나 같으므로 검은 막대를 한 칸 이동한다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo024.drawio.svg>)

검은 막대에 방금 추가된 원소와 파란 칸이 바라보는 원소를 교환한다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo025.drawio.svg>)

교환이 완료된 모습으로 검은 막대 왼쪽에 위치한 원소는 피봇보다 작거나 같은 원소들이다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo026.drawio.svg>)

파란 칸이 피봇 직전까지 모든 구간을 탐색했으므로 피봇과 검은 막대 바로 오른쪽 원소를 교환한다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo027.drawio.svg>)

교환이 완료된 모습이다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo028.drawio.svg>)

피봇의 위치를 확정한다. 피봇의 왼쪽 구간과 오른쪽 구간에 대해 탐색을 재귀적으로 진행한다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo029.drawio.svg>)

왼쪽 구간은 2번 원소 하나만 있으며 원소가 하나만 있으면 위치를 확정하고 탐색을 종료한다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo030.drawio.svg>)

오른쪽 구간은 1번 원소 하나만 있으며 원소가 하나만 있으면 위치를 확정하고 탐색을 종료한다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo031.drawio.svg>)

8번 원소의 왼쪽 구간을 재귀적으로 정렬을 완료했다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo032.drawio.svg>)

8번 원소의 오른쪽 구간에 대해 탐색 과정을 반복한다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo033.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo034.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo035.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo036.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo037.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo038.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo039.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo040.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo041.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo042.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo043.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo044.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo045.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo046.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo047.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo048.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo049.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo050.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo051.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo052.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo053.drawio.svg>)

Lomuto Partition 퀵 정렬이 완료됐다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo054.drawio.svg>)

Lomuto Partition은 피봇보다 작거나 같은 값을 검은 막대 왼쪽에 몰아 넣고 검은 막대 바로 오른쪽과 피봇을 교환함으로써 피봇을 정렬하며 이 과정을 재귀적으로 반복하는 정렬 알고리즘이다.

### Hoare Partition

Hoare Partition은 주어진 구간의 중간에 위치한 원소를 피봇으로 선택하고 양 끝에 포인터를 둔 후 두 포인터에 위치한 원소를 교환하다가 포인터가 교차하면 교차한 지점을 기준으로 분할하고 이 과정을 재귀적으로 반복하는 방식으로 동작한다. 피봇은 그저 교환의 기준만 되며 교환 이후 피봇의 위치가 정렬된 최종 위치는 아니다. 피봇을 주어진 구간의 중간에 위치한 원소로 꼭 할 필요는 없지만 중간에 위치한 원소로 하는 것이 일반적인 구현 방법이다.

주어진 수들이 $[4, 1, 8, 3, 6, 10, 8, 4]$일 경우 오름차순 Hoare Partition은 아래와 같이 진행된다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo001.drawio.svg>)

주어진 구간의 양 끝에 포인터를 위치시키고 중간 위치를 피봇으로 선택한다. $left$는 오른쪽으로 이동하며 피봇보다 크거나 같은 값을 탐색하며, $right$는 왼쪽으로 이동하며 피봇보다 작거나 같은 값을 탐색한다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo055.drawio.svg>)

탐색이 완료됐다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo056.drawio.svg>)

두 원소를 교환한다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo057.drawio.svg>)

교환이 완료됐다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo058.drawio.svg>)

다시 두 포인터를 이동하며 탐색을 수행한다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo059.drawio.svg>)

두 포인터가 교차했다. $left$의 오른쪽에는 피봇 이상인 원소들만 위치하게 됐고 $right$의 왼쪽에는 피봇 이하인 원소만 위치하게 됐다. 관습적인 $right$를 기준으로 구간을 분할한 후 이 과정을 재귀적으로 반복한다. 분할된 구간의 길이가 2, 6이라는 점에서 항상 구간을 균등하게 분할하는 병합 정렬과 달리 성능이 일관되지 않는다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo060.drawio.svg>)

왼쪽 구간은 4번, 2번이다. 양 끝에 포인터를 위치시킨다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo061.drawio.svg>)

탐색이 완료됐다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo062.drawio.svg>)

두 원소를 교환한다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo063.drawio.svg>)

교환이 완료됐다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo064.drawio.svg>)

다시 두 포인터를 이동하며 탐색을 수행한다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo065.drawio.svg>)

두 포인터가 교차했다. $right$를 기준으로 구간을 분할한 후 각 구간에 대해 재귀적으로 다시 탐색을 수행한다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo066.drawio.svg>)

2번, 4번 구간을 분할한 왼쪽 구간의 크기가 1이하면 더 이상 재귀적으로 탐색할 구간이 없다. 해당 위치를 정렬된 위치로 확정한다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo067.drawio.svg>)

2번, 4번 구간을 분할한 오른쪽 구간의 크기가 1이하면 더 이상 재귀적으로 탐색할 구간이 없다. 해당 위치를 정렬된 위치로 확정한다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo068.drawio.svg>)

1번 ~ 8번을 분할한 왼쪽 구간의 정렬이 완료됐다. 오른쪽 구간에 대해 정렬을 수행한다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo069.drawio.svg>)

두 포인터를 위치시킨다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo070.drawio.svg>)

탐색이 완료됐다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo071.drawio.svg>)

두 원소를 교환한다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo072.drawio.svg>)

교환이 완료됐다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo073.drawio.svg>)

다시 두 포인터를 이동하며 탐색을 수행한다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo074.drawio.svg>)

두 포인터가 교차했다. $right$를 기준으로 구간을 분할한 후 각 구간에 대해 재귀적으로 다시 탐색을 수행한다. 이하 과정은 아래와 같다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo075.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo076.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo077.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo078.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo079.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo080.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo081.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo082.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo083.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo084.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo085.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo086.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo087.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo088.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo089.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo090.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo091.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo092.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo093.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo094.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo095.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo096.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo097.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo098.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo099.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo100.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo101.drawio.svg>)
![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo102.drawio.svg>)

Hoare Partition 퀵 정렬이 완료됐다.

![](</assets/posts/2025-11/퀵%20정렬%20(Quick%20Sort)/photo103.drawio.svg>)

Hoare Partition은 피봇을 설정하고 두 포인터로 양 끝 원소를 교환해서 $right$ 왼쪽에는 피봇보다 작은 원소를 위치시키게 하는 과정을 재귀적으로 반복하는 정렬 알고리즘이다. Lomuto Partition에 비해 교환 횟수가 일반적으로 더 적다.

---

## 퀵 정렬 코드

### Lomuto Partition [Java]

Lomuto Partition은 구현이 직관적이고 간단하다는 장점이 있다.

$1,000,000$개의 임의의 수들에 대한 정렬에서 약 0.06초정도 소요됐다.(Macbook M3 Air, JDK 21)

병합 정렬보다 더 빠른 정렬 성능을 볼 수 있다.

```java
public static void quickSort(int[] arr) {
    quickSort(arr, 0, arr.length - 1);
}

private static void quickSort(int[] arr, int left, int right) {
    if (left >= right) return;

    int pivotIdx = partition(arr, left, right);  // Lomuto partition
    quickSort(arr, left, pivotIdx - 1);  // 피봇의 왼쪽 구간 재귀
    quickSort(arr, pivotIdx + 1, right);  // 피봇의 오른쪽 구간 재귀
}

private static int partition(int[] arr, int left, int right) {
    int pivot = arr[right];  // 구간 가장 오른쪽 값을 피봇으로 설정
    int i = left - 1;

    // 피봇 전까지 피봇보다 작거나 같은 원소 탐색
    for (int j = left; j < right; j++) {

        // 찾으면 스왑
        if (arr[j] <= pivot) {
            i++;

            // swap
            int tmp = arr[i];
            arr[i] = arr[j];
            arr[j] = tmp;
        }
    }

    // swap (i + 1 위치가 pivot의 최종 위치)
    int tmp = arr[i + 1];
    arr[i + 1] = arr[right];
    arr[right] = tmp;

    return i + 1;
}
```

### Hoare Partition [Java]

Hoare Partition은 `do ~ while`문을 통해 구현하는게 일반적인 관례인데 교환 이후 각 포인터가 최소 한 칸은 이동해야하기 때문이다. 이동시키지 않을 경우 무한 루프가 발생하기 쉬워 구현에 주의해야 한다.

$1,000,000$개의 임의의 수들에 대한 정렬에서 약 0.07초정도 소요됐다.(Macbook M3 Air, JDK 21)

병합 정렬보다 더 빠른 정렬 성능을 볼 수 있다.

```java
public static void quickSort(int[] arr) {
    quickSort(arr, 0, arr.length - 1);
}

private static void quickSort(int[] arr, int left, int right) {
    if (left >= right) return;

    int p = partition(arr, left, right);  // Hoare partition
    quickSort(arr, left, p);  // 피봇의 왼쪽 구간 재귀 (포함해야 함)
    quickSort(arr, p + 1, right);  // 피봇의 오른쪽 구간 재귀
}

private static int partition(int[] arr, int left, int right) {
    int pivot = arr[(left + right) / 2]; // 보통 가운데 값 많이 씀
    int i = left - 1;
    int j = right + 1;

    while (true) {
        do {
            i++;  // 한 칸은 이동시켜야 무한 루프 방지
        } while (arr[i] < pivot);

        do {
            j--;  // 한 칸은 이동시켜야 무한 루프 방지
        } while (arr[j] > pivot);

        if (i >= j) return j;

        // swap
        int tmp = arr[i];
        arr[i] = arr[j];
        arr[j] = tmp;
    }
}
```

---

## Ref

- [wikipedia - 퀵 정렬](https://ko.wikipedia.org/wiki/%ED%80%B5_%EC%A0%95%EB%A0%AC)

---
