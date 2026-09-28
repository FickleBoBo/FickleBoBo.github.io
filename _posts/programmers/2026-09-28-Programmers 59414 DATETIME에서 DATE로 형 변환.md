---
title: "[Programmers] #59414 - DATETIME에서 DATE로 형 변환 [MySQL]"
date: 2026-09-28
categories: [PS, Programmers]
tags: ["sql"]
slug: programmers-59414
media_subpath: /assets/img/posts/programmers-59414/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://school.programmers.co.kr/learn/courses/30/lessons/59414)
{: .prompt-info }

---

## 1. 아이디어

`DATETIME` 컬럼에서 시각을 떼고 날짜만 남기는 문제다. `DATE()` 함수로 해결하면 된다.

---

## 2. 쿼리

### 풀이 [MySQL]

```sql
SELECT ANIMAL_ID, NAME, DATE(DATETIME) AS 날짜
FROM ANIMAL_INS
ORDER BY ANIMAL_ID
```

---
