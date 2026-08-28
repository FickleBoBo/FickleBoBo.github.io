# FickleBoBo.github.io — BoBo World 블로그

Chirpy 테마 Jekyll 블로그. PS 문제풀이 포스트 자동화가 핵심.

## 레포 구성

- 이 레포: 블로그(공개, GitHub Pages가 `main`에서 배포).
- PS 소스 레포: 로컬에서 이 레포와 같은 부모 폴더의 `PS/`
  (이 환경 기준 `/Users/mwzz6/Desktop/github/PS`). 포스트 코드 블록의 원본 출처.

## 워크플로우

`ps` → `sync` → `review-code` → (태그) → `sync` → `review-post` → `publish`.
각 스킬은 `.claude/skills/*/SKILL.md`에 자기완결 문서화. 프로즈·표기 정본은
`.claude/skills/review-post/STYLE.md`. `_drafts/` 작성 중 → `_posts/` 발행.
발행본 손수정도 가능.

## 커밋 · 브랜치

- 포스트·스킬 커밋은 `main`에 직접 한다 — 이 레포는 PR 플로우가 없고 `publish`도
  `main`에 커밋한다. "기본 브랜치면 브랜치부터" 기본 동작은 여기선 적용하지 않는다.
- push는 사용자 몫. Claude는 커밋까지만.
- 트레일러는 `Co-Authored-By`만. **`Claude-Session:` 줄은 넣지 않는다** — 공개 레포라
  세션 링크는 죽은 링크 + 메타데이터 노출. 하네스 기본이 붙이려 해도 뺀다.
- 커밋 종류별:
  - `publish` 산출물: `feat: [Platform] #번호 - 제목 [langs]`. 트레일러는 스크립트가
    모델명 없이 `Co-Authored-By: Claude <noreply@anthropic.com>`로 고정.
  - 세션 중 손수정: `fix: [Platform] #번호 - <한 일>`. 트레일러
    `Co-Authored-By: Claude <실행 중인 모델명> <noreply@anthropic.com>`. 양 레포에 평행한
    메시지(블로그쪽은 프로즈 변경분 접미어 허용).
  - 스킬 정의 변경: `feat: [Claude Skill] {스킬명} - <요약>`. 트레일러는 손수정과 동일.

## 실행 스타일

- git·파일 작업(add/commit, Read/Edit/Write, 읽기 전용 git 조회)은 Claude가 바로 실행.
- 서버 기동(`jekyll serve`), 네트워크 진단, push는 사용자가 직접.
- 전역 CLAUDE.md의 "학습 프로젝트는 CLI를 사용자가 직접" 규칙보다 이 레포 규칙이 우선.

## 로컬 개발

`bundle exec jekyll serve -l` (초안 포함 시 `--drafts`). 기본 http://127.0.0.1:4000

## 건드리지 말 것

- 이 레포의 Claude 프로젝트 메모리 디렉토리(`~/.claude/projects/<이 레포 슬러그>/memory/`) —
  삭제 금지. 정리 시 `*.jsonl` transcript만 지우고 `memory/`는 제외.
- 파비콘 zip의 `site.webmanifest` — 레포에 넣지 않는다(Chirpy가 생성, 충돌).
