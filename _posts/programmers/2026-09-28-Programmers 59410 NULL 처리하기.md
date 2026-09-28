---
title: "[Programmers] #59410 - NULL 처리하기 [MySQL]"
date: 2026-09-28
categories: [PS, Programmers]
tags: ["sql"]
slug: programmers-59410
media_subpath: /assets/img/posts/programmers-59410/
math: true
mermaid: false
---

<!-- prettier-ignore -->
> [문제 링크](https://school.programmers.co.kr/learn/courses/30/lessons/59410)
{: .prompt-info }

---

## 1. 아이디어

동물의 생물 종, 이름, 성별 및 중성화 여부를 아이디 순으로 조회하는 문제다. 이름이 `NULL`인 동물은 `IFNULL`로 `'No name'`이라고 표시하면 된다.

---

## 2. 쿼리

### 풀이 [MySQL]

```sql
SELECT ANIMAL_TYPE, IFNULL(NAME, 'No name'), SEX_UPON_INTAKE
FROM ANIMAL_INS
ORDER BY ANIMAL_ID
```

---
