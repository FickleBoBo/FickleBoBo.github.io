---
title: "[Programmers] #59414 - DATETIME에서 DATE로 형 변환 [MySQL]"
date: 2026-09-28
categories: [PS, Programmers]
tags: ["sql"]
slug: programmers-59414
media_subpath: /assets/img/posts/programmers-59414/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://school.programmers.co.kr/learn/courses/30/lessons/59414)
{: .prompt-info }

---

## 1. 아이디어

모든 동물의 아이디, 이름, 들어온 날짜를 아이디 순으로 조회하는 문제다. `DATETIME`에는 시각까지 들어 있는데 시각을 뺀 날짜만 보여 달라고 했으므로 `DATE`로 날짜 부분만 꺼낸다.

---

## 2. 쿼리

### 풀이 [MySQL]

```sql
SELECT ANIMAL_ID, NAME, DATE(DATETIME)
FROM ANIMAL_INS
ORDER BY ANIMAL_ID
```

---
