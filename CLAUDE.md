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

초기 대량 처리(기발행분 전면 재작업 포함)는 2026-09에 끝났다. 지금은 포스트가
생길 때마다 개별로 파이프라인에 태운다 — `review-post`는 지목된 포스트 하나를
그날그날 처리하는 게 기본이고, 인자 없는 전체 배치는 초기용이다.

## 커밋 · 브랜치

- 포스트·스킬·인프라 커밋 전부 `main`에 직접 — 이 레포는 PR 플로우가 없고 `publish`도
  `main`에 커밋한다. "기본 브랜치면 브랜치부터" 기본 동작은 여기선 적용하지 않는다.
- push는 사용자 몫. Claude는 커밋까지만.
- 트레일러는 `Co-Authored-By` 한 줄만. **`Claude-Session:` 줄은 넣지 않는다** — 공개
  레포라 세션 링크는 죽은 링크 + 메타데이터 노출. 하네스 기본이 붙이려 해도 뺀다.

### 커밋 종류

| 종류               | 제목                                             | 트레일러                                                  |
| ------------------ | ------------------------------------------------ | --------------------------------------------------------- |
| `publish` 산출물   | `feat: [Platform] #번호 - 제목 [langs]`          | `Co-Authored-By: Claude <noreply@anthropic.com>`          |
| 발행 포스트 손수정 | `fix: [Platform] #번호 - <한 일>` (제목 생략)    | `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>` |
| 스킬 정의 변경     | `<type>: [Claude Skill] {스킬명} - <요약>`       | 〃                                                        |
| 블로그 인프라      | `<type>: <요약>` (`_config`·README·CLAUDE.md·CI) | 〃                                                        |

- `<type>` ∈ `feat`/`fix`/`docs`/`refactor`/`chore` — 변경 성격에 맞게 고른다. 포스트
  커밋만 `feat`(publish)/`fix`(손수정) 고정.
- **트레일러 모델명 규칙**: 커밋 시점에 버전을 알 수 없는 주체(정적 스크립트 —
  `publish`)가 커밋하면 모델명 없이 `Co-Authored-By: Claude <noreply@anthropic.com>`.
  Claude가 직접 커밋해 현재 버전을 아는 경우는 그 버전을 넣어
  `Co-Authored-By: Claude {현재 모델명} <noreply@anthropic.com>`(예: 이 세션은
  `Claude Sonnet 5`). 모델명은 **이름 부분**에 넣고 이메일 슬롯(`<>`)은 하나만 —
  구 `Claude <claude-sonnet-5> <noreply@...>` 이중 `<>` 형식은 폐기.
- 두 레포(블로그·PS) 메시지는 동일 문구 재사용(PS에서 지은 걸 블로그에도 — 블로그쪽은
  프로즈 변경분 접미어 허용).
- `rework:` 프리픽스는 2026-09 기발행분 재작업 1회성 — 종료, 더 쓰지 않는다.

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
