#!/usr/bin/env python3
"""Строит PNG-мокапы окон SecureBooking из модели SysML v2 (текстовая нотация).

Модель: docs/sysml/Mockups.sysml (элементы из библиотеки docs/sysml/UiKit.sysml).
Каждая часть типа Window превращается в изображение docs/images/mockup-NN-<имя>.png.

Запуск из корня репозитория:
    pip install pillow
    python docs/tools/sysml2png.py

Поддерживается подмножество SysML v2, использованное в Mockups.sysml:
пакеты, части (part имя : Тип { ... }) и переопределения атрибутов
(attribute :>> имя = значение; значение — строка, число, true/false,
литерал перечисления Тип::литерал или список в скобках).
"""
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

DOCS = Path(__file__).resolve().parent.parent
MODEL = DOCS / "sysml" / "Mockups.sysml"
IMAGES = DOCS / "images"

# ============================================================ разбор модели

TOKENS = re.compile(r"""
      (?P<comment>/\*.*?\*/|//[^\n]*)
    | (?P<string>"(?:[^"\\]|\\.)*")
    | (?P<symbol>:>>|:>|[{};=(),:])
    | (?P<word>[\w.]+(?:::[\w.]+)*)
""", re.S | re.X)


class Element:
    """Узел модели: заголовок (лексемы до '{' или ';') и вложенные элементы."""

    def __init__(self, header):
        self.header = header
        self.children = []

    @property
    def words(self):
        return [v for _, v in self.header]

    @property
    def keyword(self):
        return self.words[0] if self.words else ""

    @property
    def name(self):
        w = self.words
        return w[1] if len(w) > 1 and w[1] not in (":", ":>>") else ""

    @property
    def type(self):
        w = self.words
        return w[w.index(":") + 1].split("::")[-1] if ":" in w else ""

    def parts(self):
        return [c for c in self.children if c.keyword == "part"]

    def attrs(self):
        """{имя: значение} для строк вида  attribute :>> имя = значение;"""
        result = {}
        for c in self.children:
            w = c.words
            if c.keyword != "attribute" or ":>>" not in w or "=" not in w:
                continue
            key = w[w.index(":>>") + 1]
            raw = c.header[w.index("=") + 1:]
            values = [unquote(v) if k == "string" else v.split("::")[-1]
                      for k, v in raw if v not in ("(", ")", ",")]
            is_list = any(v == "(" for _, v in raw)
            result[key] = values if is_list else (values[0] if values else "")
        return result


def unquote(s):
    return s[1:-1].replace('\\"', '"')


def parse(text):
    root = Element([])
    stack, header = [root], []
    for m in TOKENS.finditer(text):
        kind, value = m.lastgroup, m.group()
        if kind == "comment":
            continue
        if value == "{":
            node = Element(header)
            stack[-1].children.append(node)
            stack.append(node)
            header = []
        elif value == "}":
            if header:
                stack[-1].children.append(Element(header))
            stack.pop()
            header = []
        elif value == ";":
            if header:
                stack[-1].children.append(Element(header))
            header = []
        else:
            header.append((kind, value))
    return root


def walk(node):
    yield node
    for c in node.children:
        yield from walk(c)


# ============================================================ оформление

def load_font(names, size):
    for n in names:
        try:
            return ImageFont.truetype(n, size)
        except OSError:
            continue
    return ImageFont.load_default()


REG = ["segoeui.ttf", "DejaVuSans.ttf", "arial.ttf"]
BOLD = ["segoeuib.ttf", "DejaVuSans-Bold.ttf", "arialbd.ttf"]
MONO = ["consola.ttf", "DejaVuSansMono.ttf", "cour.ttf"]

F = load_font(REG, 15)
FS = load_font(REG, 13)
FB = load_font(BOLD, 15)
FH = load_font(BOLD, 17)
FBIG = load_font(BOLD, 24)
FM = load_font(MONO, 13)

INK = "#1f2933"
MUTED = "#7b8794"
LINE = "#cbd2d9"
BG = "#eef1f5"
HEAD = "#f5f7fa"
ACCENT = "#2f6fde"
SELECT = "#dbe7fb"
GREEN = "#2e8b57"
RED = "#c0392b"

WIDTH = 1180
GAP = 14
PAD = 16
CONTAINERS = ("Window", "Row", "Column", "Card")
FIELDS = ("TextField", "PasswordField", "DateField", "ComboBox")


def fit(d, text, font, width):
    if d.textlength(text, font=font) <= width:
        return text
    while text and d.textlength(text + "…", font=font) > width:
        text = text[:-1]
    return text + "…"


def widths(kids, total):
    weights = [int(k.attrs().get("weight", 1)) for k in kids]
    free = total - GAP * (len(kids) - 1)
    return [free * w / sum(weights) for w in weights]


# ============================================================ размеры

def height(node, w):
    t, a = node.type, node.attrs()
    kids = node.parts()
    if t in CONTAINERS:
        inner = w - (2 * PAD if t == "Card" else 0)
        if t == "Row":
            h = max((height(k, kw) for k, kw in zip(kids, widths(kids, inner))), default=0)
        else:
            h = sum(height(k, inner) for k in kids) + GAP * max(len(kids) - 1, 0)
        if t == "Card":
            h += 2 * PAD + (34 if a.get("text") else 0)
        return h
    if t == "MenuBar":
        return 34
    if t in FIELDS:
        return 34 + (21 if a.get("label") else 0)
    if t == "Button":
        return 36
    if t == "StatCard":
        return 80
    if t == "RoomCard":
        return 108
    if t == "Table":
        return 32 * (1 + len(kids))
    if t == "CodeBlock":
        return 20 * len(a.get("lines", [])) + 20
    return 22  # Label


# ============================================================ отрисовка

def card(d, x, y, w, h, border=LINE, width=1):
    d.rounded_rectangle([x + 2, y + 3, x + w + 2, y + h + 3], 10, fill="#d9dee5")  # тень
    d.rounded_rectangle([x, y, x + w, y + h], 10, fill="white", outline=border, width=width)


def draw(d, node, x, y, w):
    t, a = node.type, node.attrs()
    text = a.get("text", "")
    h = height(node, w)
    kids = node.parts()

    if t in CONTAINERS:
        if t == "Card":
            card(d, x, y, w, h)
            x, y, w = x + PAD, y + PAD, w - 2 * PAD
            if text:
                d.text((x, y), fit(d, text, FH, w), font=FH, fill=INK)
                y += 34
        if t == "Row":
            for k, kw in zip(kids, widths(kids, w)):
                draw(d, k, x, y, kw)
                x += kw + GAP
        else:
            for k in kids:
                draw(d, k, x, y, w)
                y += height(k, w) + GAP

    elif t == "MenuBar":
        disabled = a.get("disabled", [])
        if isinstance(disabled, str):
            disabled = [disabled]
        cx = x + PAD
        for item in a.get("items", []):
            d.text((cx, y + 8), item, font=F, fill=MUTED if item in disabled else INK)
            cx += d.textlength(item, font=F) + 26
        if a.get("user"):
            u = a["user"]
            d.text((x + w - PAD - d.textlength(u, font=FS), y + 10), u, font=FS, fill=MUTED)

    elif t in FIELDS:
        if a.get("label"):
            d.text((x, y), a["label"], font=FS, fill=INK)
            y += 21
        d.rounded_rectangle([x, y, x + w, y + 34], 5, fill="white", outline=LINE)
        d.text((x + 10, y + 8), fit(d, text, F, w - 44), font=F, fill=INK)
        if t == "ComboBox":
            d.polygon([(x + w - 22, y + 14), (x + w - 10, y + 14), (x + w - 16, y + 21)], fill=INK)
        elif t == "DateField":
            d.rectangle([x + w - 26, y + 9, x + w - 10, y + 25], outline=INK)
            d.line([x + w - 26, y + 14, x + w - 10, y + 14], fill=INK)

    elif t == "Button":
        primary = a.get("primary") == "true"
        d.rounded_rectangle([x, y, x + w, y + 36], 6, fill=ACCENT if primary else "white",
                            outline=ACCENT if primary else "#9aa5b1")
        label = fit(d, text, FB, w - 12)
        d.text((x + (w - d.textlength(label, font=FB)) / 2, y + 8), label, font=FB,
               fill="white" if primary else INK)

    elif t == "StatCard":
        card(d, x, y, w, h)
        d.rounded_rectangle([x, y, x + 6, y + h], 3, fill=ACCENT)
        d.text((x + PAD + 4, y + 12), fit(d, a.get("label", ""), FS, w - 2 * PAD), font=FS, fill=MUTED)
        d.text((x + PAD + 4, y + 36), fit(d, text, FBIG, w - 2 * PAD), font=FBIG, fill=INK)

    elif t == "RoomCard":
        selected = a.get("selected") == "true"
        card(d, x, y, w, h, ACCENT if selected else LINE, 3 if selected else 1)
        free = a.get("status", "free") == "free"
        d.text((x + PAD, y + 12), fit(d, text, FH, w - 120), font=FH, fill=INK)
        pill = "свободна" if free else "занята"
        pw = d.textlength(pill, font=FS) + 20
        d.rounded_rectangle([x + w - PAD - pw, y + 12, x + w - PAD, y + 34], 11,
                            fill="#e3f4ea" if free else "#fbe4e1")
        d.text((x + w - PAD - pw + 10, y + 15), pill, font=FS, fill=GREEN if free else RED)
        d.text((x + PAD, y + 46), fit(d, a.get("info", ""), FS, w - 2 * PAD), font=FS, fill=MUTED)
        if a.get("note"):
            d.text((x + PAD, y + 72), fit(d, a["note"], F, w - 2 * PAD), font=F, fill=GREEN if free else RED)

    elif t == "Table":
        cols = a.get("columns", [])
        rows = [(r.attrs().get("cells", []), r.attrs().get("selected") == "true") for r in kids]
        need = []
        for j, c in enumerate(cols):
            longest = max([d.textlength(c, font=FB)] +
                          [d.textlength(r[j], font=FS) for r, _ in rows if j < len(r)])
            need.append(longest + 24)
        cws = [n * w / sum(need) for n in need]
        d.rectangle([x, y, x + w, y + 32], fill=HEAD)
        for i, (cells, selected) in enumerate([(cols, False)] + rows):
            ry = y + 32 * i
            if selected:
                d.rectangle([x + 1, ry + 1, x + w - 1, ry + 31], fill=SELECT)
            cx = x
            for cell, cw in zip(cells, cws):
                font = FB if i == 0 else FS
                color = GREEN if cell == "свободно" else INK
                d.text((cx + 10, ry + 8), fit(d, cell, font, cw - 16), font=font, fill=color)
                cx += cw
            d.line([x, ry + 32, x + w, ry + 32], fill=LINE)
        d.rectangle([x, y, x + w, y + 32 * (len(rows) + 1)], outline=LINE)

    elif t == "CodeBlock":
        d.rounded_rectangle([x, y, x + w, y + h], 6, fill="#f7f8fa", outline=LINE)
        for i, line in enumerate(a.get("lines", [])):
            d.text((x + 12, y + 10 + 20 * i), fit(d, line, FM, w - 24), font=FM, fill=INK)

    else:  # Label
        style = a.get("style", "normal")
        font, color = {"title": (FH, INK), "muted": (FS, MUTED), "warning": (FS, RED)}.get(style, (F, INK))
        d.text((x, y + 2), fit(d, text, font, w), font=font, fill=color)


def render_window(node, path):
    a = node.attrs()
    titlebar = 38
    kids = node.parts()
    menu = kids[0] if kids and kids[0].type == "MenuBar" else None
    body = kids[1:] if menu else kids
    inner = WIDTH - 2 * PAD
    total = titlebar + (35 if menu else 0) + PAD
    total += sum(height(k, inner) for k in body) + GAP * max(len(body) - 1, 0) + PAD

    img = Image.new("RGB", (WIDTH, total), BG)
    d = ImageDraw.Draw(img)
    # заголовок окна Windows
    d.rectangle([0, 0, WIDTH, titlebar], fill="white")
    d.rounded_rectangle([12, 10, 30, 28], 4, fill=ACCENT)
    d.text((16, 9), "S", font=FB, fill="white")
    d.text((42, 10), a.get("title", ""), font=F, fill=INK)
    for i, sym in enumerate(("✕", "☐", "—")):
        d.text((WIDTH - 34 - i * 46, 9), sym, font=F, fill=INK)
    d.line([0, titlebar, WIDTH, titlebar], fill=LINE)
    y = titlebar
    if menu:
        d.rectangle([0, y + 1, WIDTH, y + 35], fill="white")
        draw(d, menu, 0, y + 1, WIDTH)
        d.line([0, y + 35, WIDTH, y + 35], fill=LINE)
        y += 35
    y += PAD
    for k in body:
        draw(d, k, PAD, y, inner)
        y += height(k, inner) + GAP
    d.rectangle([0, 0, WIDTH - 1, total - 1], outline="#9aa5b1")
    img.save(path)


def file_name(index, part_name):
    base = re.sub(r"Window$", "", part_name)
    base = re.sub(r"(?<!^)([A-Z])", r"-\1", base).lower()
    return f"mockup-{index:02d}-{base}.png"


def main():
    IMAGES.mkdir(exist_ok=True)
    model = parse(MODEL.read_text(encoding="utf-8"))
    windows = [n for n in walk(model) if n.keyword == "part" and n.type == "Window"]
    if not windows:
        sys.exit("В модели нет частей типа Window")
    for i, win in enumerate(windows, 1):
        target = IMAGES / file_name(i, win.name)
        render_window(win, target)
        print("создан", target.relative_to(DOCS.parent))


if __name__ == "__main__":
    main()
