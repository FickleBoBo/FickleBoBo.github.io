"""PS 포스트 도식용 공용 모듈(스타일 정본은 IMAGE_STYLE.md).

도식 하나는 `draw(c, frame, solid_bg) -> str` 함수(`svg(...)`로 감싼 SVG 문자열 반환, `solid_bg`는
GIF용 단색 배경 여부)로 쓰고, `emit`이 라이트/다크 SVG와 (프레임이 여럿이면) GIF를 만든다.
알고리즘 상태(프레임)는 호출하는 쪽이 코드로 계산해 넘긴다.
GIF 래스터화에 `rsvg-convert`(brew install librsvg)와 Pillow가 필요하다.
"""

import io
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image

THEMES = {
    "light": dict(
        bg="#ffffff",
        cell="#f3f5f7",
        line="#9aa5b1",
        dim="#c5cbd3",
        text="#1f2933",
        muted="#7b8794",
        ink="#1f2933",
        tint="#e4e8ec",
        on_color="#ffffff",
        blue="#0072b2",
        blue_t="#d6e9f4",
        orange="#c77c00",
        orange_t="#fdeccb",
        green="#007a5a",
        green_t="#d2efe5",
        red="#d55e00",
        red_t="#fbe0cf",
        purple="#a8478a",
        purple_t="#f2dcec",
        yellow="#8f7500",
        yellow_t="#f5edbd",
    ),
    "dark": dict(
        bg="#1b1b1e",
        cell="#272a30",
        line="#5a6270",
        dim="#454c57",
        text="#e4e7eb",
        muted="#8b95a3",
        ink="#e4e7eb",
        tint="#343841",
        on_color="#0b1620",
        blue="#56b4e9",
        blue_t="#1f3a4d",
        orange="#f0b429",
        orange_t="#4a3a16",
        green="#3cc9a0",
        green_t="#1a3d33",
        red="#ff8c5a",
        red_t="#4d2a1a",
        purple="#e49ccb",
        purple_t="#44243b",
        yellow="#f0e442",
        yellow_t="#4a4410",
    ),
}
SANS = "Pretendard, 'Apple SD Gothic Neo', 'Noto Sans KR', system-ui, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

# ── 모든 도식이 같이 쓰는 틀(숫자의 정본, 설명은 IMAGE_STYLE.md `형태`·`형식`) ──
CANVAS_W = 560  # 캔버스 폭
MARGIN = 16  # 제목·단계·범례·캡션의 왼쪽 시작 x
HEADER_H = 68  # 제목(y 24)·단계(y 46) 아래, 그림이 시작하는 y
CELL_W, CELL_H, GAP = 92, 60, 8  # 격자 칸
FS_TITLE, FS_STEP, FS_CAPTION, FS_LEGEND, FS_CELL = 16, 13, 15, 15, 24
ROW = 34  # 그림 아래 상태 줄·범례·캡션 사이 세로 간격
LEGEND_ROW = 28  # 범례 항목 줄 간격
FRAME_MS, LAST_MS = 2000, 3500  # GIF: 프레임당, 마지막 프레임


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, fill, size=15, anchor="middle", mono=True, weight=500):
    """수직 중앙 기준 텍스트. 숫자·식은 mono, 한글 라벨은 mono=False."""
    return (
        f'<text x="{x}" y="{y}" fill="{fill}" font-size="{size}" font-weight="{weight}" '
        f'text-anchor="{anchor}" font-family="{MONO if mono else SANS}" '
        f'dominant-baseline="central">{esc(s)}</text>'
    )


def svg(w, h, body, c, solid_bg=False):
    """정적 SVG는 투명 배경(사이트 배경에 녹는다), GIF는 단색 배경(solid_bg)."""
    bg = f'<rect width="{w}" height="{h}" fill="{c["bg"]}"/>' if solid_bg else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'font-family="{SANS}">{bg}{body}</svg>'
    )


def rect(x, y, w, h, fill, stroke, sw=1.5, rx=8):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="{sw}"/>'
    )


def circle(x, y, r, fill, stroke, sw=2.5):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def line(x1, y1, x2, y2, stroke, sw=1.5):
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" '
        f'stroke-width="{sw}" stroke-linecap="round"/>'
    )


def pointer(cx, y, label, color):
    """칸 아래 삼각형 포인터와 라벨."""
    return f'<path d="M{cx} {y} l-7 11 h14 z" fill="{color}"/>' + text(
        cx, y + 24, label, color, 15, weight=700
    )


def header(c, title, step=None, total=None, unit="단계"):
    """제목(도식이 다루는 입력)과, GIF면 `k / N단계`(첫 프레임은 `시작`)를 왼쪽 위에 쓴다."""
    out = text(MARGIN, 24, title, c["text"], FS_TITLE, anchor="start", weight=700)
    if step is not None:
        label = f"{step} / {total}{unit}" if step else "시작"
        out += text(MARGIN, 46, label, c["muted"], FS_STEP, anchor="start", mono=False)
    return out


def caption(c, y, s, color=None, weight=500):
    """그림 아래 한 줄 설명. 마지막 프레임·결론 줄은 color=c["green"], weight=700."""
    return text(
        MARGIN,
        y,
        s,
        color or c["text"],
        FS_CAPTION,
        anchor="start",
        mono=False,
        weight=weight,
    )


def legend(c, items, y, cols=3, col_w=170):
    """범례. items=[(채움, 윤곽, 윤곽 굵기, 라벨)]를 cols열로 y부터 배치한다(줄 간격 LEGEND_ROW)."""
    out = ""
    for k, (fill, stroke, sw, label) in enumerate(items):
        x = MARGIN + (k % cols) * col_w
        yy = y + (k // cols) * LEGEND_ROW
        out += rect(x, yy - 9, 18, 18, fill, stroke, sw, rx=4)
        out += text(x + 26, yy, label, c["text"], FS_LEGEND, anchor="start", mono=False)
    return out


def grid_x0(cols):
    """칸 cols개를 가로 가운데에 놓는 왼쪽 x."""
    return (CANVAS_W - (cols * CELL_W + (cols - 1) * GAP)) // 2


def cell_xy(i, j, cols):
    """격자 (i, j)칸의 왼쪽 위 좌표."""
    return grid_x0(cols) + j * (CELL_W + GAP), HEADER_H + i * (CELL_H + GAP)


def grid_bottom(rows):
    """격자 rows줄의 아래 끝 y."""
    return HEADER_H + rows * CELL_H + (rows - 1) * GAP


def raster(svg_text, scale=2.5):
    p = subprocess.run(
        ["rsvg-convert", "-z", str(scale), "-f", "png"],
        input=svg_text.encode(),
        capture_output=True,
        check=True,
    )
    return Image.open(io.BytesIO(p.stdout)).convert("RGB")


def save_gif(images, path, ms=FRAME_MS, last_ms=LAST_MS):
    q = [
        im.quantize(
            colors=128, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE
        )
        for im in images
    ]
    q[0].save(
        path,
        save_all=True,
        append_images=q[1:],
        duration=[ms] * (len(q) - 1) + [last_ms],
        loop=0,
        optimize=True,
        disposal=1,
    )


def emit(
    out_dir,
    name,
    draw,
    frames,
    static_index=-1,
    gif=True,
    static=True,
    ms=FRAME_MS,
    last_ms=LAST_MS,
):
    """`{name}-light|dark.svg`(정적, frames[static_index], static=True일 때)와 gif=True면 `{name}-{mode}.gif`를 쓴다.
    static=False면 SVG 파일은 쓰지 않고 XML 검증만 한다(GIF만 쓰는 도식).
    draw(c, frame, solid_bg) -> svg 문자열."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    for mode, c in THEMES.items():
        svg_text = draw(c, frames[static_index], False)
        ET.fromstring(
            svg_text
        )  # XML 오류면 ParseError로 멈춘다(깨진 SVG를 쓰지 않는다)
        if static:
            (out / f"{name}-{mode}.svg").write_text(svg_text)
        if gif and len(frames) > 1:
            save_gif(
                [raster(draw(c, f, True)) for f in frames],
                out / f"{name}-{mode}.gif",
                ms=ms,
                last_ms=last_ms,
            )
