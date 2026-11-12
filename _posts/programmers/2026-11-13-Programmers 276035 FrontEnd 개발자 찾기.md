---
title: "[Programmers] #276035 - FrontEnd 개발자 찾기 [MySQL]"
date: 2026-11-13
categories: [PS, Programmers]
tags: ["sql"]
slug: programmers-276035
media_subpath: /assets/img/posts/programmers-276035/
math: true
---

<!-- prettier-ignore -->
> [문제 링크](https://school.programmers.co.kr/learn/courses/30/lessons/276035)
{: .prompt-info }

---

## 1. 아이디어

`DEVELOPERS`에서 Front End 스킬을 가진 개발자의 정보를 ID 순으로 조회하는 문제다. 스킬 코드가 2의 제곱수라 `SKILLCODES`의 `CODE`는 켜진 비트가 하나이고, 개발자의 `SKILL_CODE`에 그 비트가 켜져 있으면 그 스킬을 가진 것이므로 `SKILL_CODE & CODE`가 `CODE`와 같은지로 판별한다. `CATEGORY`가 Front End인 스킬 중 이를 만족하는 것이 하나라도 있으면 된다.

Front End 스킬이 여럿이라 둘 이상 가진 개발자는 `JOIN`하면 여러 번 조회되므로, 개발자마다 조건에 맞는 스킬이 있는지만 `EXISTS`로 확인한다.

---

## 2. 쿼리

### 풀이 [MySQL]

```sql
SELECT d.ID, d.EMAIL, d.FIRST_NAME, d.LAST_NAME
FROM DEVELOPERS d
WHERE EXISTS (
    SELECT 1
    FROM SKILLCODES s
    WHERE s.CATEGORY = 'Front End' AND d.SKILL_CODE & s.CODE = s.CODE
)
ORDER BY d.ID
```

`&`는 `=`보다 먼저 계산되므로 괄호 없이도 `(d.SKILL_CODE & s.CODE) = s.CODE`로 읽힌다.

---
