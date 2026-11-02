"""
`review-code`·`review-post` 서브에이전트의 JSON 보고를 읽는 공용 도구. 보고 형식(스키마) 검증과 출력 모양은
스킬마다 다르므로 각 스킬의 `scripts/render_report.py`가 갖고, 여기엔 스킬과 무관한 것만 둔다.
"""

import json
import re
import sys

FENCE = re.compile(r"```json\s*(.*?)```", re.DOTALL)


def load_report(path):
    """보고 파일(서브에이전트가 낸 텍스트 그대로)에서 JSON을 읽어 항목 리스트로 돌려준다.

    ```json 펜스가 있으면 그 안을, 없으면 파일 전체를 JSON으로 파싱한다. 파싱 실패는 OSError·ValueError.
    """
    with open(path, encoding="utf-8") as f:
        text = f.read()
    m = FENCE.search(text)
    data = json.loads(m.group(1) if m else text)
    return data if isinstance(data, list) else [data]


def collect(paths, check):
    """보고 파일들의 항목을 모은다. `check(항목)`은 그 항목의 형식 오류 문자열 목록을 돌려준다.
    (항목들, 오류들)이며, 오류는 첫 번째에서 멈추지 않고 전부 모은다."""
    entries, errors = [], []
    for path in paths:
        try:
            parsed = load_report(path)
        except (OSError, ValueError) as e:
            errors.append(f"{path}: 읽기·JSON 파싱 실패 — {e}")
            continue
        for i, entry in enumerate(parsed):
            errors += [f"{path}[{i}]: {e}" for e in check(entry)]
            entries.append(entry)
    return entries, errors


def exit_on_errors(errors):
    """오류가 있으면 사유만 출력하고 종료 코드 1로 끝낸다(아무것도 렌더링하지 않는다)."""
    if errors:
        print(
            "형식 오류 — 서브에이전트에 고쳐서 다시 내도록 요청:\n"
            + "\n".join(f"  {e}" for e in errors)
        )
        sys.exit(1)


def cell(s):
    """마크다운 표 셀에 안전하도록 `|`를 이스케이프하고 줄바꿈을 공백으로 바꾼다."""
    return str(s).replace("|", "\\|").replace("\n", " ")
