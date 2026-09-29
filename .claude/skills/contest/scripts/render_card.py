#!/usr/bin/env python3
"""
대회 후기 프리뷰 카드(1200×630, 2x 렌더 → 2400×1260 PNG) 렌더러. 순수 함수 —
CF API를 부르지 않고, 데이터(dict)를 받아 HTML을 만든 뒤 헤드리스 Chrome으로
스크린샷을 찍는다. 데이터 수집은 `scaffold_contest.py`가 담당.

**디자인 '양식'은 이 파일의 CSS/레이아웃이 정본.** 코드를 고칠 때 옆 코드만 봐선
안 보이는 '왜'만 남긴다:

- **2x 렌더**(`--force-device-scale-factor=2`): 1x면 레티나에서 확대돼 흐리다.
- **Y축은 데이터 기반 동적 범위**(`_axis`): 레이팅이 올라도 그래프가 안 삐져나오고,
  눈금 간격도 자동. 최소 레이팅이 높은 계정이면 0부터 안 시작한다(변화가 보이게).
- **점 개수가 많으면 마커 생략**(`MARKER_MAX`): 대회가 쌓이면 점이 빽빽해진다. 선은
  전부, 마커는 `MARKER_MAX`개 이하일 때만(끝점은 항상 강조).
- **레이팅 하락은 빨강**(`DOWN`): 델타·끝점·선 끝 색이 같이 바뀐다.
- **레이팅 이력이 2점 미만이면 그래프 없는 레이아웃**(`chart=None`): unrated
  첫 참가 등. 칩만 아래로 내려 빈 화면을 막는다. 레이팅 변동이 없는 대회(unrated)는
  델타·끝점 강조 없이 현재 레이팅만 라벨로.
- **제목 줄바꿈은 첫 `(` 앞**에서: `Codeforces Round 1122` / `(Div. 3) 후기`.
  `(`가 없으면 `후기`만 둘째 줄. 글자 크기는 가장 긴 줄 길이에 맞춰 축소(`_title_size`).
- 폰트는 macOS 기본 Apple SD Gothic Neo 우선(로컬 렌더 전제). 다른 환경이면
  폴백 체인의 다음 폰트.
- Chrome이 없으면 예외(`ChromeNotFound`) — 호출부가 잡아서 카드 없이 진행.

사용(디버그): `python3 render_card.py <out.png>` — 샘플 데이터로 렌더.
"""

import html
import math
import os
import shutil
import subprocess
import sys
import tempfile

MARKER_MAX = 12
UP = "#7fe3b0"
DOWN = "#ff8a8a"

CHROME_CANDIDATES = [
    os.environ.get("CHROME_BIN", ""),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "google-chrome",
    "chromium",
    "chrome",
]


class ChromeNotFound(RuntimeError):
    pass


def find_chrome():
    for c in CHROME_CANDIDATES:
        if not c:
            continue
        if os.path.isabs(c):
            if os.path.exists(c):
                return c
        elif shutil.which(c):
            return shutil.which(c)
    raise ChromeNotFound("Chrome을 못 찾음(CHROME_BIN 환경변수로 지정 가능)")


# ── 차트 ─────────────────────────────────────────────────────────────────────

CHART_W, CHART_H = 1040, 170
_STEPS = [50, 100, 200, 250, 400, 500, 1000]


def _axis(vals):
    """데이터 범위 → (ymin, ymax, step). 눈금 대략 4칸 이하."""
    lo, hi = min(vals), max(vals)
    rng = max(hi - lo, 1)
    ymin_raw = max(0, lo - max(0.1 * rng, 50))
    ymax_raw = hi + max(0.08 * rng, 30)
    step = next(
        (s for s in _STEPS if math.ceil((ymax_raw - ymin_raw) / s) <= 4), _STEPS[-1]
    )
    ymin = int(ymin_raw // step) * step
    ymax = int(math.ceil(ymax_raw / step)) * step
    return ymin, ymax, step


def _chart_svg(vals, delta):
    """vals: 레이팅 이력(시작값 포함, 2점 이상). delta: 이번 대회 변동(None이면 unrated)."""
    W, H = CHART_W, CHART_H
    ymin, ymax, step = _axis(vals)
    n = len(vals)
    X = lambda i: i * (W / (n - 1))
    Y = lambda v: H - (v - ymin) / (ymax - ymin) * H
    pts = [(X(i), Y(v)) for i, v in enumerate(vals)]
    line = " ".join(
        f"{'M' if i == 0 else 'L'}{x:.1f},{y:.1f}" for i, (x, y) in enumerate(pts)
    )
    area = f"{line} L{W},{H} L0,{H} Z"
    lx, ly = pts[-1]

    end = DOWN if (delta is not None and delta < 0) else UP
    grid = "".join(
        f'<line x1="0" x2="{W}" y1="{Y(v):.1f}" y2="{Y(v):.1f}" stroke="#fff" stroke-opacity=".08" stroke-dasharray="4 8"/>'
        f'<text x="0" y="{Y(v) - 8:.1f}" fill="#7d8092" font-size="16">{v}</text>'
        for v in range(ymin + step, ymax + 1, step)
    )
    dots = ""
    if n <= MARKER_MAX:
        dots = "".join(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="#0d0f16" stroke="#c9cbd6" stroke-width="3"/>'
            for x, y in pts[:-1]
        )
    if delta is None:
        tail = ""
    else:
        tail = f' <tspan fill="{"#4fd08a" if delta >= 0 else "#ff6b6b"}" font-size="26">{delta:+d}</tspan>'
    label = f'<text x="{lx:.1f}" y="{ly - 34:.1f}" text-anchor="end" fill="#fff" font-size="38" font-weight="800">{vals[-1]}{tail}</text>'
    highlight = delta is not None
    end_dot = (
        f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="16" fill="{end}" filter="url(#g)" opacity=".8"/>'
        f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="8" fill="{end}" stroke="#0d0f16" stroke-width="3"/>'
        if highlight
        else f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="7" fill="#0d0f16" stroke="#c9cbd6" stroke-width="3"/>'
    )
    guide = f'<line x1="{lx:.1f}" x2="{lx:.1f}" y1="{ly:.1f}" y2="{H}" stroke="{end}" stroke-opacity=".35" stroke-dasharray="4 6"/>'
    return f"""<svg class="chart" width="{W + 60}" height="{H + 90}" viewBox="-20 -70 {W + 60} {H + 90}">
<defs><linearGradient id="a" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8f96ff" stop-opacity=".4"/><stop offset="1" stop-color="#8f96ff" stop-opacity="0"/></linearGradient>
<linearGradient id="l" x1="0" x2="1"><stop offset="0" stop-color="#8f96ff"/><stop offset="1" stop-color="{end}"/></linearGradient>
<filter id="g" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="7"/></filter></defs>
{grid}<path d="{area}" fill="url(#a)"/><path d="{line}" fill="none" stroke="url(#l)" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>{guide}{dots}{end_dot}{label}
</svg>"""


# ── 제목 ─────────────────────────────────────────────────────────────────────


def _split_title(name):
    """('첫 줄', '괄호 부분 또는 None')."""
    i = name.find(" (")
    if i == -1:
        return name, None
    return name[:i], name[i + 1 :]


def _title_size(lines):
    longest = max(len(s) for s in lines)
    return max(40, min(66, int(1000 / (longest * 0.5))))


def _title_html(name):
    first, paren = _split_title(name)
    if paren:
        lines = [first, paren + " 후기"]
        body = f"{html.escape(first)}<br><span>{html.escape(paren)}</span> 후기"
    else:
        lines = [first, "후기"]
        body = f"{html.escape(first)}<br><span>후기</span>"
    return body, _title_size(lines)


# ── 렌더 ─────────────────────────────────────────────────────────────────────


def build_html(d):
    """d: {name, date('YYYY.MM.DD'), solved, total, penalty,
    rank(None 가능), rank_count, pct, ratings(list, 시작값 포함), delta(None 가능)}"""
    title_body, size = _title_html(d["name"])
    chips = [
        f'<div class="chip"><b>{d["solved"]}</b> / {d["total"]} solved</div>',
        f'<div class="chip">penalty <b>{d["penalty"]}</b></div>',
    ]
    if d.get("rank"):
        chips.append(
            f'<div class="chip">rank <b>{d["rank"]}</b> / {d["rank_count"]}</div>'
        )
        chips.append(f'<div class="chip">상위 <b>{d["pct"]}%</b></div>')
    ratings = d.get("ratings") or []
    chart = _chart_svg(ratings, d.get("delta")) if len(ratings) >= 2 else ""
    chips_top = 290 if chart else 400

    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
*{{margin:0;box-sizing:border-box}}
body{{width:1200px;height:630px;font-family:"Apple SD Gothic Neo","Noto Sans KR","Pretendard",sans-serif;color:#f4f4f8;position:relative;overflow:hidden;
background:radial-gradient(700px 420px at 12% -5%,rgba(120,130,255,.28),transparent 70%),radial-gradient(600px 400px at 100% 100%,rgba(79,208,138,.16),transparent 70%),#0d0f16}}
.dots{{position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.07) 1.2px,transparent 1.4px);background-size:28px 28px;-webkit-mask-image:linear-gradient(180deg,#000,transparent 60%)}}
.pill{{position:absolute;left:72px;top:56px;font-size:20px;letter-spacing:.16em;font-weight:700;color:#aeb2ff;padding:8px 18px;border:1.5px solid rgba(174,178,255,.4);border-radius:999px;background:rgba(174,178,255,.08)}}
.brand{{position:absolute;right:72px;top:62px;font-size:20px;color:#6f7285;letter-spacing:.06em}}
h1{{position:absolute;left:72px;right:72px;top:118px;font-size:{size}px;line-height:1.12;font-weight:800;letter-spacing:-.025em}}
h1 span{{background:linear-gradient(90deg,#aeb2ff,#7fe3b0);-webkit-background-clip:text;color:transparent}}
.chips{{position:absolute;left:72px;top:{chips_top}px;display:flex;gap:12px}}
.chip{{font-size:22px;padding:9px 18px;border-radius:12px;background:rgba(255,255,255,.07);color:#d5d7e3;font-weight:600}}
.chip b{{color:#fff}}
.chart{{position:absolute;left:52px;top:352px}}
</style></head><body><div class="dots"></div>
<div class="pill">CONTEST REVIEW · {html.escape(d["date"])}</div><div class="brand">BoBo World</div>
<h1>{title_body}</h1>
<div class="chips">{"".join(chips)}</div>
{chart}</body></html>"""


def render_card(data, out_path):
    """카드 PNG를 out_path에 쓴다. Chrome이 없으면 ChromeNotFound."""
    chrome = find_chrome()
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, "card.html")
        with open(src, "w", encoding="utf-8") as f:
            f.write(build_html(data))
        subprocess.run(
            [
                chrome,
                "--headless=new",
                "--disable-gpu",
                "--hide-scrollbars",
                "--force-device-scale-factor=2",
                "--window-size=1200,630",
                f"--screenshot={out_path}",
                f"file://{src}",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=90,
            check=True,
        )
    if not os.path.exists(out_path):
        raise RuntimeError(f"Chrome이 스크린샷을 안 만듦: {out_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    render_card(
        {
            "name": "Codeforces Round 1122 (Div. 3)",
            "date": "2026.09.21",
            "solved": 3,
            "total": 8,
            "penalty": 162,
            "rank": 9176,
            "rank_count": 20851,
            "pct": 44.0,
            "ratings": [100, 474, 736, 953, 1043, 1105],
            "delta": 62,
        },
        sys.argv[1],
    )
    print(sys.argv[1])
