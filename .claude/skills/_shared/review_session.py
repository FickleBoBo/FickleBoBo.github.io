"""
`review-code`·`review-post` 오케스트레이터의 dispatch 전 준비와 취합 전 검증을 한 번에 한다.
`_drafts/`는 git 미추적이라 `git diff`가 서브에이전트의 변경을 못 잡아서, 스냅샷 대조로 대신한다.

사용법:
    review_session.py prepare <이름> <작업 디렉토리> <포스트 .md 경로> [...]
    review_session.py verify  <이름> <작업 디렉토리> <포스트 .md 경로> [...]

<이름>은 `reviewcode`/`reviewpost`처럼 스킬별로 구분하는 접두어, <작업 디렉토리>는 스크래치패드.

prepare: `<작업>/<이름>-snap/`에 포스트 사본(이전 실행 잔재는 비운다), `<작업>/<이름>-marker`,
  `<작업>/<이름>-src/`에 문제 원문(`fetch_statement.run`). 종료 코드는 원문 확보 결과를 그대로
  따른다(0 전부 확보, 1 실패 있음, 3 Codeforces 보류 — 스냅샷은 이미 떠 있다).
verify: 사본과 한 글자라도 다른 포스트, 마커 이후 수정된 `.claude`·`_drafts`·`_posts` 파일을 나열한다.
  종료 코드 0 깨끗함, 1 위반 또는 마커 이후 수정 파일 있음(사용자 에디터 저장이 섞이면 어느 파일인지
  보고 판단). 서브에이전트의 자기 보고("수정 안 했다")를 대신하는 검사다.
"""

import os
import shutil
import sys

from fetch_statement import run as fetch_run
from repo import REPO_ROOT

WATCHED = (".claude", "_drafts", "_posts")


def session_paths(name, work_dir):
    base = os.path.abspath(work_dir)
    return (
        os.path.join(base, f"{name}-snap"),
        os.path.join(base, f"{name}-marker"),
        os.path.join(base, f"{name}-src"),
    )


def prepare(name, work_dir, posts):
    snap, marker, src = session_paths(name, work_dir)
    shutil.rmtree(snap, ignore_errors=True)
    shutil.rmtree(src, ignore_errors=True)  # 이전 실행의 원문이 섞이지 않게
    os.makedirs(snap)
    for post in posts:
        shutil.copy(post, snap)
    with open(marker, "w"):
        pass
    print(f"스냅샷: {snap}\n원문: {src}")
    return fetch_run(src, posts, False)


def modified_since(marker):
    since = os.path.getmtime(marker)
    found = []
    for top in WATCHED:
        for d, dirs, files in os.walk(os.path.join(REPO_ROOT, top)):
            dirs[:] = [x for x in dirs if x != "__pycache__"]
            for f in files:
                if f == ".DS_Store":
                    continue
                path = os.path.join(d, f)
                if os.path.getmtime(path) > since:
                    found.append(path)
    return sorted(found)


def verify(name, work_dir, posts):
    snap, marker, _ = session_paths(name, work_dir)
    bad = 0
    for post in posts:
        copy = os.path.join(snap, os.path.basename(post))
        try:
            with open(copy, "rb") as a, open(post, "rb") as b:
                changed = a.read() != b.read()
        except FileNotFoundError:
            changed = True  # 삭제·이동도 변조다
        if changed:
            print(f"변조됨: {post}")
            bad += 1
    for path in modified_since(marker):
        print(f"마커 이후 수정됨: {path}")
        bad += 1
    if not bad:
        print("변조 없음")
    return 1 if bad else 0


def main():
    args = sys.argv[1:]
    if len(args) < 4 or args[0] not in ("prepare", "verify"):
        sys.exit(__doc__)
    action = {"prepare": prepare, "verify": verify}[args[0]]
    sys.exit(action(args[1], args[2], [os.path.abspath(p) for p in args[3:]]))


if __name__ == "__main__":
    main()
