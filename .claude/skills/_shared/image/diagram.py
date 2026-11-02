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
    ),
}
SANS = "Pretendard, 'Apple SD Gothic Neo', 'Noto Sans KR', system-ui, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"


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


def raster(svg_text, scale=2.5):
    p = subprocess.run(
        ["rsvg-convert", "-z", str(scale), "-f", "png"],
        input=svg_text.encode(),
        capture_output=True,
        check=True,
    )
    return Image.open(io.BytesIO(p.stdout)).convert("RGB")


def save_gif(images, path, ms=1000, last_ms=2200):
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


def emit(out_dir, name, draw, frames, static_index=-1, gif=True, ms=1000):
    """`{name}-light.svg`·`{name}-dark.svg`(정적, frames[static_index])와 gif=True면 `{name}-{mode}.gif`를 쓴다.
    draw(c, frame, solid_bg) -> svg 문자열."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    for mode, c in THEMES.items():
        static = draw(c, frames[static_index], False)
        ET.fromstring(static)  # XML 오류면 ParseError로 멈춘다(깨진 SVG를 쓰지 않는다)
        (out / f"{name}-{mode}.svg").write_text(static)
        if gif and len(frames) > 1:
            save_gif(
                [raster(draw(c, f, True)) for f in frames],
                out / f"{name}-{mode}.gif",
                ms=ms,
            )
