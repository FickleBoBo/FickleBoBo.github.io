# FickleBoBo.github.io — BoBo World 블로그

Chirpy 테마 Jekyll 블로그. PS 문제풀이 포스트 자동화가 핵심.

## 레포 구성

- 이 레포: 블로그(공개, GitHub Pages가 `main`에서 배포).
- PS 소스 레포: 로컬에서 이 레포와 같은 부모 폴더의 `PS/`(`_shared/blog_common.py`의
  `PS_REPO`가 이 상대 위치로 잡는다). 포스트 코드 블록의 원본 출처.

## 워크플로우

`ps` → `sync` → `review-code` → (태그) → `sync` → `review-post` → `publish`.
각 스킬은 `.claude/skills/*/SKILL.md`에 문서화돼 있다(`review-code`·`review-post`는 서브에이전트가
읽는 절차를 `PROCEDURE.md`로 분리, 서브에이전트 정의는 `.claude/agents/`). `publish`는 포스트 하나씩,
완료 게이트(카테고리·태그·아이디어·복잡도)를 통과한 것만 발행한다. 프로즈·표기 정본은
`.claude/skills/review-post/STYLE.md`. `_drafts/` 작성 중 → `_posts/` 발행.
발행본 손수정도 가능.

스킬 스크립트가 공유하는 레포 상수·front matter 파서·git 커밋 헬퍼(`blog_common.py`),
문제 원문 조회(`fetch_statement.py`), 리뷰 청크 분할(`chunk_drafts.py`)은 스킬이 아닌
`.claude/skills/_shared/`에 있다(SKILL.md 없음).

`ps`의 대상 시작일은 2025-12-01이다(`ps/SKILL.md` 참고). 이 날짜 이후 풀이는 일회성으로 `_drafts/`에
일괄 스캐폴드했고, 그 백로그를 포스트 단위로(보통 한 번에 20개 안팎) 파이프라인에 태운다 — 처리된 건
`_posts/`로 발행되고 아직 안 탄 건 `_drafts/{platform}/`에 남아 있다. `review-*`·`sync`도 지목한 포스트
하나를 그날그날 처리하는 게 기본이다.

### 대회 후기 (별도 장르)

대회 참여 기록은 `Contest` 카테고리의 독립 장르 — PS 파이프라인 밖이다. `contest` 스킬이
스캐폴드(`scaffold_contest.py`)와 발행(`publish_contest.py`)을 맡고, 서술·라이브 코드·총평은
사람이 채운다. 동작·발행 절차는 `.claude/skills/contest/SKILL.md`. 나머지 스킬은 스캔 범위가
`blog_common.PLATFORM_DIRS` 폴더로 한정돼 있어 `contest/` 폴더를 건드리지 않는다.

## 커밋 · 브랜치

- 포스트·스킬·인프라 커밋 전부 `main`에 직접 — 이 레포는 PR 플로우가 없고 `publish`도
  `main`에 커밋한다. "기본 브랜치면 브랜치부터" 기본 동작은 여기선 적용하지 않는다.
- push는 사용자 몫. Claude는 커밋까지만.
- 트레일러는 `Co-Authored-By` 한 줄만. **`Claude-Session:` 줄은 넣지 않는다** — 공개
  레포라 세션 링크는 죽은 링크 + 메타데이터 노출. 하네스 기본이 붙이려 해도 뺀다.

### 커밋 종류

| 종류               | 제목                                                        | 트레일러                                                       |
| ------------------ | ----------------------------------------------------------- | -------------------------------------------------------------- |
| `publish` 산출물   | `feat: [Platform] #번호 - 제목 [langs]`                     | `Co-Authored-By: Claude <noreply@anthropic.com>`               |
| 발행 포스트 손수정 | `fix: [Platform] #번호 - <한 일>` (제목 생략)               | `Co-Authored-By: Claude {현재 모델명} <noreply@anthropic.com>` |
| 대회 후기 발행     | `feat: [Contest] {CF API 대회명} 후기`                      | `Co-Authored-By: Claude <noreply@anthropic.com>`               |
| 대회 후기 손수정   | `fix: [Contest] {CF API 대회명} - <한 일>`                  | `Co-Authored-By: Claude {현재 모델명} <noreply@anthropic.com>` |
| 스킬 정의 변경     | `<type>: [Claude Skill] {스킬명} - <요약>` (`_shared` 포함) | 〃                                                             |
| 블로그 인프라      | `<type>: <요약>` (`_config`·README·CLAUDE.md·CI)            | 〃                                                             |

- `<type>` ∈ `feat`/`fix`/`docs`/`refactor`/`chore` — 변경 성격에 맞게 고른다. 포스트·후기
  커밋만 `feat`(발행)/`fix`(손수정) 고정.
- 대회 후기의 `{CF API 대회명}`은 CF API의 `name` 그대로(정규화·브래킷 접두어 없음, 포스트
  `title`과 동일) — `Codeforces Round 1119 (Div. 3)`처럼 "Codeforces"가 들어 있어도 손대지 않는다.
- **트레일러 모델명 규칙**: 정적 스크립트(`publish`·`publish_contest`)는 커밋 시점 모델 버전을 몰라
  모델명 없이 `Co-Authored-By: Claude <noreply@anthropic.com>`. Claude가 직접 커밋하면 현재 버전을
  이름 부분에 넣어 `Co-Authored-By: Claude {현재 모델명} <noreply@anthropic.com>`(예: `Claude Sonnet 5.5`) —
  이메일 슬롯(`<>`)은 하나만.
- 두 레포(블로그·PS) 메시지는 동일 문구 재사용(PS에서 지은 걸 블로그에도 — 블로그쪽은
  프로즈 변경분 접미어 허용). `publish`·`publish_contest`도 두 레포에 같은 메시지로 커밋.

## 실행 스타일

- git·파일 작업(add/commit, Read/Edit/Write, 읽기 전용 git 조회)은 Claude가 바로 실행. 단 이는 실행 권한이지 커밋 시점이 아니다 — 커밋은 사용자가 "커밋해"처럼 명시한 뒤에만 하고, "메시지 설계"·"수정해"는 커밋 지시가 아니다.
- 서버 기동(`jekyll serve`), 네트워크 진단, push는 사용자가 직접.
- 전역 CLAUDE.md의 "학습 프로젝트는 CLI를 사용자가 직접" 규칙보다 이 레포 규칙이 우선.

## 로컬 개발

`bundle exec jekyll serve -l` (초안 포함 시 `--drafts`). 기본 http://127.0.0.1:4000

## 건드리지 말 것

- 이 레포의 Claude 프로젝트 메모리 디렉토리(`~/.claude/projects/<이 레포 슬러그>/memory/`) —
  삭제 금지. 정리 시 `*.jsonl` transcript만 지우고 `memory/`는 제외.
- 파비콘 zip의 `site.webmanifest` — 레포에 넣지 않는다(Chirpy가 생성, 충돌).
