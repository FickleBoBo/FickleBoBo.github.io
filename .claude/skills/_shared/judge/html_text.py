"""문제 지문 HTML 조각을 읽기 좋은 평문(마크다운 비슷한 형태)으로 바꾼다."""

import re
from html.parser import HTMLParser


class HtmlToText(HTMLParser):
    """HTML 조각을 읽기 좋은 평문으로. `capture_class`를 주면 그 class의 div 안만 변환."""

    BLOCKS = {"p", "div", "ul", "ol", "table", "tr", "blockquote", "section"}

    def __init__(self, capture_class=None):
        super().__init__(convert_charrefs=True)
        self.capture_class = capture_class
        self.capturing = capture_class is None
        self.div_depth = 0
        self.out = []
        self.pre = 0
        self.skip = 0
        self.list_depth = 0

    def _emit(self, s):
        if self.capturing and not self.skip:
            self.out.append(s)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if not self.capturing:
            if tag == "div" and self.capture_class in (a.get("class") or ""):
                self.capturing = True
                self.div_depth = 1
            return
        if tag == "div":
            self.div_depth += 1
        if tag in ("script", "style"):
            self.skip += 1
        elif tag == "pre":
            self.pre += 1
            self._emit("\n```\n")
        elif tag in ("ul", "ol"):
            self.list_depth += 1
            self._emit("\n")
        elif tag == "li":
            self._emit("\n" + "  " * (self.list_depth - 1) + "- ")
        elif tag == "br":
            self._emit("\n")
        elif tag in ("td", "th"):
            self._emit(" | ")
        elif tag == "tr":
            self._emit("\n")
        elif tag == "sup":
            self._emit("^{")
        elif tag == "sub":
            self._emit("_{")
        elif tag == "img":
            self._emit(f"[이미지: {a.get('src', '')}]")
        elif tag == "code" and not self.pre:
            self._emit("`")
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._emit("\n\n### ")
        elif tag in self.BLOCKS:
            self._emit("\n\n")

    def handle_endtag(self, tag):
        if not self.capturing:
            return
        if tag == "div":
            self.div_depth -= 1
            if self.capture_class is not None and self.div_depth == 0:
                self.capturing = False
                return
        if tag in ("script", "style"):
            self.skip -= 1
        elif tag == "pre":
            self.pre -= 1
            self._emit("\n```\n")
        elif tag in ("ul", "ol"):
            self.list_depth -= 1
            self._emit("\n")
        elif tag == "sup" or tag == "sub":
            self._emit("}")
        elif tag == "code" and not self.pre:
            self._emit("`")
        elif tag in ("p", "table", "blockquote") or tag.startswith("h"):
            self._emit("\n\n")

    def handle_data(self, data):
        if not self.capturing or self.skip:
            return
        self.out.append(data if self.pre else re.sub(r"\s+", " ", data))

    def text(self):
        s = "".join(self.out)
        s = re.sub(r"[ \t]+\n", "\n", s)
        s = re.sub(r"\n{3,}", "\n\n", s)
        return s.strip()


def html_to_text(html, capture_class=None):
    parser = HtmlToText(capture_class)
    parser.feed(html)
    return parser.text()
