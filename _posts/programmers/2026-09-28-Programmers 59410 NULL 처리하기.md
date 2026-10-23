---
title: "[Programmers] #59410 - NULL 처리하기 [MySQL]"
date: 2026-09-28
categories: [PS, Programmers]
tags: ["sql"]
slug: programmers-59410
media_subpath: /assets/img/posts/programmers-59410/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://school.programmers.co.kr/learn/courses/30/lessons/59410)
{: .prompt-info }

---

## 1. 아이디어

동물의 종, 이름, 성별 및 중성화 여부를 아이디 순으로 조회하되 이름이 없는 동물은 이름을 `'No name'`으로 표시하는 문제다. 이름이 없다는 것은 `NAME`이 NULL이라는 뜻이므로 `IFNULL`로 `'No name'`을 대신 채운다.

---

## 2. 쿼리

### 풀이 [MySQL]

```sql
SELECT ANIMAL_TYPE, IFNULL(NAME, 'No name'), SEX_UPON_INTAKE
FROM ANIMAL_INS
ORDER BY ANIMAL_ID
```

---
