# FickleBoBo.github.io — BoBo World 블로그

Chirpy 테마 Jekyll 블로그. PS 문제풀이 포스트를 `.claude/skills/`의 스킬로 자동화한다. 이 레포는 Claude Code 전용으로 운영한다.

## 레포 구성

- 이 레포: 블로그(공개, GitHub Pages가 `main`에서 배포). `_drafts/` 작성 중 → `_posts/` 발행.
- PS 소스 레포: 이 레포와 같은 부모 폴더의 `PS/`(`_shared/repo.py`의 `PS_REPO`). 포스트 코드 블록의 원본 출처다. 언어 버전 정본은 `PS/CONVENTIONS.md`이고, 사용자가 이미 정해 둔 사실은 되묻기 전에 PS 레포 문서부터 찾는다.
- PS 폴더명은 소문자(`cofo_2257a`), 블로그 slug·제목은 대문자(`2257A`)다. PS 경로를 직접 조회할 때는 `ls`로 폴더명부터 확인한다(대문자로 조회하면 출력이 비어 "변경 없음"으로 오인한다).

## 명령

- 로컬 실행: `bundle exec jekyll serve -l`(초안 포함 `--drafts`), http://127.0.0.1:4000
- 포스트 린트: `python3 .claude/skills/_shared/lint_post.py <포스트 경로>`(이슈가 있으면 종료 코드 1, 결과이지 실패가 아니다)
- 포매팅: md·yaml은 Prettier, Python은 Ruff. 둘 다 CLI가 PATH에 없어 VS Code 확장 번들을 쓴다. Ruff는 기본값이라 긴 한글 줄(E501)과 `sys.path` 선삽입(E402)이 남는 것이 정상이다.

## 워크플로우

`ps` → `review-code` → `write-post` → `review-post` → `tag` → `publish`. 각 스킬의 동작은 `.claude/skills/*/SKILL.md`가 정본이다.

- 아이디어·접근 이름·블록 설명은 `write-post`로 쓰거나 사용자가 직접 쓴다. `review-post`는 평가만 하고 쓰지 않으며, `tag`는 아이디어가 작성된 뒤에 돌린다.
- PS 코드를 고치면 그때마다 `sync`로 포스트에 반영한다(안 하면 `publish`가 막는다). `publish`는 포스트 하나씩 돌린다.
- `review-code`·`review-post`는 읽기 전용 서브에이전트(`.claude/agents/`)를 쓴다. 에이전트 정의는 세션 시작 때 로드되므로 바꾸면 세션을 다시 시작해야 한다.
- 프로즈·표기 정본은 `.claude/skills/_shared/STYLE.md`, 태그 정본은 `_shared/tags.yaml`과 `tag/RULES.md`다. 같은 규칙을 둘 이상의 문서에 옮겨 적지 않는다.

## 포스트 규약

- 구조는 `## 1. 아이디어` → `## 2. 코드`(SQL은 `## 2. 쿼리`). 복잡도 섹션은 두지 않고, 방법을 고르는 근거일 때만 아이디어에 녹인다. 실수·오답 원인 같은 구체적 사건이 있을 때만 사용자가 `## 3. 회고`를 둔다.
- 한 문제 한 포스트. 다중 접근은 `### 풀이 N: 이름`. 아이디어 기준과 시리즈·Follow-up 서술은 `STYLE.md`가 정한다.
- 제목 언어 브라켓은 `[Java][C++][Python]` 순서. `date`는 풀이한 날짜(PS 레포와 쌍), slug는 `{platform}-{번호}`(`baekjoon-13034`)로 permalink를 유지한다.
- 대상은 블로그 개설일(2026-08-17) 이후 PS 레포의 풀이 전부다. 새 포스트마다 `review-code`·`review-post`를 전수 실행한다.
- 코드 블록에 Chirpy `{: file }` 라벨을 쓰지 않는다(헤더가 언어명으로 자동 생성된다).
- 이미지는 Claude가 만든다(정적 SVG, 동작은 GIF, 라이트·다크 두 벌). 정본은 `_shared/image/IMAGE_STYLE.md`이고, 알고리즘 상태 도식은 코드로 실제 값을 계산해 생성한 뒤 생성 스크립트(`make_diagrams.py`)를 결과물과 같은 `assets/img/posts/{slug}/`에 둔다.
- **리부트 이전 포스트(`_backup/`)는 소급 수정하지 않고** 스킬 스캔 대상도 아니다.

### 풀이 언어 정책

| 저지        | 언어                |
| ----------- | ------------------- |
| BaekJoon    | Java · C++ · Python |
| Programmers | Java · C++ · Python |
| LeetCode    | Java · C++ · Python |
| Codeforces  | C++                 |

- 3언어 저지도 특정 언어가 AC 불가·제출 불가·과하게 복잡해지면 그 언어만 사유 없이 비운다(C++ 큰 수 연산처럼). SQL 문제는 MySQL로 통일한다.
- BaekJoon의 Python은 재오픈 이후 새로 푸는 문제부터 적용하고 기존 포스트에는 소급하지 않는다.
- 저지는 위 4개가 전부이고 언어는 3개를 넘기지 않는다.
- 버전: Java 21, C++20(Codeforces·LeetCode는 C++23), Python은 미정. 코드 설명을 검증할 때는 저지별 버전으로 컴파일·실행한다.

### 대회 후기 (별도 장르)

`Contest` 카테고리의 독립 장르로 PS 파이프라인 밖이다. 스캐폴드와 발행은 `contest` 스킬로만 하고 서술·라이브 코드·총평은 사람이 채운다(`contest/SKILL.md`). 다른 스킬은 `contest/`를 건드리지 않는다.

## 스킬·스크립트 규약

- 둘 이상의 스킬이 쓰는 스크립트는 스킬이 아닌 `_shared/`에 둔다(SKILL.md 없음). 한 모듈은 한 책임이고, 스킬 스크립트는 이 모듈들을 조합한다. 한 스킬만 쓰는 로직은 그 스킬의 `scripts/`에 남긴다.
- 스킬은 자기 폴더와 `_shared`만 import하고 다른 스킬의 `scripts/`는 import하지 않는다. 엔트리 스크립트는 `_shared`를 `sys.path` 앞에 넣은 뒤 import한다.
- `_shared` 스크립트는 `python3 -I`로 돌리지 않는다(형제 모듈 import가 깨진다).
- 스킬 SKILL.md에는 절차만 적고 규칙 본문은 정본 문서로 연결한다.

## 커밋 · 브랜치

- 포스트·스킬·인프라 커밋 전부 `main`에 직접 — PR 플로우가 없고 `publish`도 `main`에 커밋한다. "기본 브랜치면 브랜치부터" 기본 동작은 여기선 적용하지 않는다.
- **push는 사용자 몫이고 Claude는 커밋까지만 한다.** 커밋도 사용자가 "커밋해"처럼 명시한 뒤에만 한다("메시지 설계"·"수정해"는 커밋 지시가 아니다).
- 트레일러는 `Co-Authored-By` 한 줄만. **`Claude-Session:` 줄은 넣지 않는다** — 공개 레포라 세션 링크는 죽은 링크 + 메타데이터 노출이고, 하네스 기본이 붙이려 해도 뺀다.

### 커밋 종류

| 종류               | 제목                                                        | 트레일러                                                       |
| ------------------ | ----------------------------------------------------------- | -------------------------------------------------------------- |
| `publish` 산출물   | `feat: [Platform] #번호 - 제목 [langs]`                     | `Co-Authored-By: Claude <noreply@anthropic.com>`               |
| 발행 포스트 손수정 | `fix: [Platform] #번호 - <한 일>` (제목 생략)               | `Co-Authored-By: Claude {현재 모델명} <noreply@anthropic.com>` |
| 대회 후기 발행     | `feat: [Contest] {CF API 대회명} 후기`                      | `Co-Authored-By: Claude <noreply@anthropic.com>`               |
| 대회 후기 손수정   | `fix: [Contest] {CF API 대회명} - <한 일>`                  | `Co-Authored-By: Claude {현재 모델명} <noreply@anthropic.com>` |
| 스킬 정의 변경     | `<type>: [Claude Skill] {스킬명} - <요약>` (`_shared` 포함) | 〃                                                             |
| 블로그 인프라      | `<type>: <요약>` (`_config`·README·CLAUDE.md·CI)            | 〃                                                             |

- `<type>` ∈ `feat`/`fix`/`docs`/`refactor`/`chore` — 변경 성격에 맞게 고른다. 포스트·후기 커밋만 `feat`(발행)/`fix`(손수정) 고정.
- 대회 후기의 `{CF API 대회명}`은 CF API의 `name` 그대로(정규화·접두어 없음, 포스트 `title`과 동일)다. `Codeforces Round 1119 (Div. 3)`처럼 "Codeforces"가 들어 있어도 손대지 않는다.
- 트레일러의 모델명: 정적 스크립트(`publish`·`publish_contest`)는 커밋 시점 모델을 몰라 모델명 없이 `Claude`. Claude가 직접 커밋하면 현재 모델 이름을 넣는다(예: `Claude Sonnet 5.5`). 이메일 슬롯(`<>`)은 하나만.
- 두 레포(블로그·PS) 메시지는 동일 문구를 쓴다(블로그 쪽은 프로즈 변경분 접미어 허용). `publish`·`publish_contest`도 두 레포에 같은 메시지로 커밋하고, `sync`로 고친 손수정은 PS 쪽 미커밋 변경과 1:1이라 같이 커밋한다.
- 스킬 변경은 스킬 단위로 쪼개고 의존 순서(`_shared` → `ps` → `sync` → `review-code` → `review-post` → `publish` → `contest` → 문서)로 커밋해야 중간 커밋도 import가 맞는다.
- 커밋은 경로를 지정한다: `git add -- <파일>` 뒤 `git commit -m ... -- <파일>`. 인덱스에 이전 작업의 스테이징분이 남아 있을 수 있기 때문이다.

## 실행 스타일

- git·파일 작업(Read/Edit/Write, 읽기 전용 git 조회)은 Claude가 바로 실행한다.
- 파일을 덮어쓰는 명령은 전역 규칙대로 대상 목록을 먼저 확인한다. 이 셸은 zsh라 배열이 1부터 시작하고 오류가 나도 반복문이 계속 돈다 — 반복은 `while read` 또는 Python으로 하고 경로는 항상 명시한다.
- 서버 기동(`jekyll serve`)과 네트워크 진단은 사용자가 직접 한다.
- 전역 CLAUDE.md의 "학습 프로젝트는 CLI를 사용자가 직접" 규칙보다 이 레포 규칙이 우선한다.

## 건드리지 말 것

- 이 레포의 Claude 프로젝트 메모리 디렉토리(`~/.claude/projects/<이 레포 슬러그>/memory/`) — 삭제 금지. 정리 시 `*.jsonl` transcript만 지운다.
- `_backup/`·`_drafts/` — git 미추적이라 덮어쓰거나 지우면 복구할 수 없다. 포매터·일괄 변환은 대상 파일을 명시해서만 돌리고, 삭제는 사용자가 지시한 목록만(삭제 전 git 사본과 대조).
- `_config.yml` posts `defaults`의 `render_with_liquid: false` — 코드 펜스의 `{{`·`{%`(C++ `{{1, 0}, {0, 1}}` 등)를 Liquid가 해석하면 빌드가 실패하거나 글자가 사라진다. 포스트 본문에서 Liquid를 쓰려면 그 포스트 front matter에서 `true`로 덮어쓴다.
- GitHub Discussions — giscus 댓글의 백엔드라 끄면 안 된다(레포 설정 정리 요청에도 예외).
- 파비콘 zip의 `site.webmanifest` — 레포에 넣지 않는다(Chirpy가 생성, 충돌).
- 다른 AI 도구용 파일(`AGENTS.md`, `.codex/`, `.agents/`) — 만들지 않는다. 보이면 다른 앱의 임포트 부산물이라 지운다.
