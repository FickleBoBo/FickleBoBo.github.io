"""
저지 사이트 조회. 저지마다 모듈 하나(`baekjoon`·`programmers`·`leetcode`·`codeforces`)이고, 모두 같은 모양이다:

- `PREFIX`(PS 레포 폴더 접두사), `PLATFORM`(포스트의 플랫폼 표기. `_drafts`·`_posts`의 폴더명은 소문자),
  `HOST`(문제 URL의 호스트)
- `title_and_url(number)`: 문제 번호로 (제목, 문제 URL). `ps`가 스캐폴드 때 쓴다.
- `statement(url)`: 문제 원문 텍스트. 직접 조회가 막힌 저지는 `None`이고, 그런 저지는 외부에서 받은
  텍스트를 검사하는 `check_statement(url, text)`(문제 목록, 비면 통과)를 갖는다(Codeforces).

`repo.PLATFORM_MAP`이 이 목록에서 파생되므로 저지를 추가하면 다른 곳을 고칠 필요가 없다.

새 저지를 붙이려면 모듈 하나를 만들어 `JUDGES`에 넣는다.
"""

from . import baekjoon, codeforces, leetcode, programmers

JUDGES = (baekjoon, programmers, leetcode, codeforces)


def by_prefix(prefix):
    for judge in JUDGES:
        if judge.PREFIX == prefix:
            return judge
    raise ValueError(f"알 수 없는 저지 접두사: {prefix}")


def by_url(url):
    for judge in JUDGES:
        if judge.HOST in url:
            return judge
    raise ValueError(f"지원하지 않는 문제 주소: {url}")


def title_and_url(prefix, number):
    return by_prefix(prefix).title_and_url(number)
