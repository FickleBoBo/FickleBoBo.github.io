---
title: "[Programmers] #276013 - Python 개발자 찾기 [MySQL]"
date: 2026-11-13
categories: [PS, Programmers]
tags: ["sql"]
slug: programmers-276013
media_subpath: /assets/img/posts/programmers-276013/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://school.programmers.co.kr/learn/courses/30/lessons/276013)
{: .prompt-info }

---

## 1. 아이디어

Python 스킬을 가진 개발자의 정보를 ID 순으로 조회하는 문제다. 스킬이 `SKILL_1`부터 `SKILL_3`까지 세 컬럼에 나뉘어 있어 `Python`이 어느 칸에든 올 수 있으므로, 세 컬럼 중 하나라도 `Python`이면 조회한다. 세 컬럼 모두 NULL을 허용하지만 NULL과의 비교는 참이 되지 않아, 빈 칸이 있어도 다른 칸이 `Python`이면 걸린다.

---

## 2. 쿼리

### 풀이 [MySQL]

```sql
SELECT ID, EMAIL, FIRST_NAME, LAST_NAME
FROM DEVELOPER_INFOS
WHERE 'Python' IN (SKILL_1, SKILL_2, SKILL_3)
ORDER BY ID
```

`IN`의 왼쪽에 값을 두고 오른쪽 목록에 세 컬럼을 넣어 `OR` 세 개를 한 번에 대신했다.

---
