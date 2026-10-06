#!/usr/bin/env python3
"""Render README visuals straight from the theme JSON.

    python3 scripts/render-preview.py

Produces images/palette.png and images/bracket-ladder.png.
Because the colours are read from the theme file rather than hardcoded, the
README imagery cannot drift away from the shipped palette.
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THEME = os.path.join(ROOT, "themes", "dracula-deep-color-theme.json")
OUT = os.path.join(ROOT, "images")

MONO = "/usr/share/fonts/TTF/JetBrainsMonoNerdFontMono-{}.ttf"
SANS = "/usr/share/fonts/Adwaita/AdwaitaSans-{}.ttf"

_fonts = {}


def font(kind, size, weight="Regular"):
    key = (kind, size, weight)
    if key not in _fonts:
        path = (MONO if kind == "mono" else SANS).format(weight)
        _fonts[key] = ImageFont.truetype(path, size)
    return _fonts[key]


def rgba(color, alpha=None):
    h = color.lstrip("#")
    if len(h) == 8 and alpha is None:
        h, alpha = h[:6], int(h[6:], 16)
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    if alpha is None:
        return (r, g, b)
    return (r, g, b, max(0, min(255, alpha)))


def luminance(color):
    h = color.lstrip("#")[:6]

    def lin(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (lin(int(h[i:i + 2], 16)) for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(fg, bg):
    a, b = luminance(fg), luminance(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def blend(color, alpha, over="#101010"):
    f, b = rgba(color), rgba(over)
    return tuple(int(f[i] * alpha + b[i] * (1 - alpha)) for i in range(3))


def composite(color, over):
    h = color.lstrip("#")
    if len(h) == 8:
        return blend(h[:6], int(h[6:], 16) / 255, over)
    return rgba(color)


class Theme:
    def __init__(self):
        data = json.load(open(THEME))
        self.colors = data["colors"]
        self.rules = data["tokenColors"]
        self.name = data["name"]
        self.bg = self.colors["editor.background"]
        self.fg = self.colors["editor.foreground"]

    def token(self, scope):
        for rule in self.rules:
            if scope in (rule.get("scope") or []):
                return rule["settings"].get("foreground", self.fg), rule["settings"].get("fontStyle")
        raise KeyError(scope)

    def ui(self, key, default):
        return self.colors.get(key, default)


TOKENS = [
    ("comment", "comment"),
    ("string", "string"),
    ("number", "constant.numeric"),
    ("keyword", "keyword"),
    ("function", "entity.name.function"),
    ("type", "entity.name"),
    ("parameter", "variable.parameter"),
    ("variable", "variable"),
    ("property", "variable.other.property"),
    ("attribute", "entity.other.attribute-name"),
    ("tag", "entity.name.tag"),
    ("punctuation", "meta.brace"),
    ("operator", "keyword.operator"),
]


def render_palette(t):
    W = 900
    row_h = 46
    head = 96
    pad = 28
    H = head + row_h * len(TOKENS) + pad + 44
    img = Image.new("RGB", (W, H), t.bg)
    d = ImageDraw.Draw(img)

    title_font = font("sans", 26)
    sub_font = font("mono", 13)
    d.text((pad, 30), "Syntax palette", font=title_font, fill=t.fg)
    d.text((pad, 64), f"{t.name}  ·  measured against {t.bg}",
           font=sub_font, fill=blend(t.fg, 0.55))
    d.text((W - pad, 40), "WCAG", font=font("sans", 15),
           fill=blend(t.fg, 0.45), anchor="ra")
    d.text((W - pad, 62), "contrast", font=font("sans", 15),
           fill=blend(t.fg, 0.45), anchor="ra")

    mono_font = font("mono", 15)
    ratio_font = font("mono", 14)
    for i, (label, scope) in enumerate(TOKENS):
        fg, style = t.token(scope)
        y = head + i * row_h
        d.rounded_rectangle([pad, y + 4, pad + 34, y + 34], radius=6,
                            fill=rgba(fg), outline=blend(t.fg, 0.20))
        suffix = "  italic" if style and "i" in style else ""
        d.text((pad + 50, y + 19), label, font=mono_font, fill=blend(t.fg, 0.92), anchor="lm")
        d.text((pad + 250, y + 19), fg.upper(), font=mono_font, fill=blend(t.fg, 0.50), anchor="lm")
        d.text((pad + 390, y + 19), suffix, font=font("mono", 12),
               fill=blend(t.fg, 0.35), anchor="lm")

        ratio = contrast(fg, t.bg)
        passes = ratio >= 4.5
        d.text((W - pad, y + 19), f"{ratio:.1f}:1", font=ratio_font,
               fill=blend(active_green(), 0.85) if passes else blend(t.fg, 0.55), anchor="ra")
        d.text((W - pad - 78, y + 19), "AA" if passes else "below", font=font("mono", 12),
               fill=blend(active_green(), 0.7) if passes else blend(t.fg, 0.35), anchor="ra")

    d.text((pad, H - pad - 4),
           "comments sit below AA by design — they are meant to recede",
           font=font("mono", 12), fill=blend(t.fg, 0.42))

    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "palette.png")
    img.save(path, optimize=True)
    print("wrote", path)


def active_green():
    return "#7FAFA5"


def render_ladder(t):
    W = 900
    pad = 28
    cell = 108
    H = 300
    img = Image.new("RGB", (W, H), t.bg)
    d = ImageDraw.Draw(img)

    d.text((pad, 30), "Bracket depth ladder", font=font("sans", 26), fill=t.fg)
    d.text((pad, 64), "editorBracketHighlight.foreground1–6 — nesting is visible without adding glare",
           font=font("mono", 13), fill=blend(t.fg, 0.55))

    ladder = [t.colors[f"editorBracketHighlight.foreground{i}"] for i in range(1, 7)]

    x = pad
    y = 120
    f = font("mono", 22)
    pairs = [
        ("config", t.fg), ("(", ladder[0]), ("{", ladder[0]), (" ", t.fg),
        ("verify", t.ui("variable.other.property", "#8FA8C4")), (": ", t.fg),
        ("[", ladder[1]), ("[", ladder[2]), ("{", ladder[3]), (" ", t.fg),
        ("level", t.ui("variable.other.property", "#8FA8C4")), (": ", t.fg),
        ("\"deep\"", t.token("string")[0]), (" ", t.fg), ("}", ladder[3]),
        ("]", ladder[2]), ("]", ladder[1]), (" ", t.fg), ("}", ladder[0]),
        (")", ladder[0]),
    ]
    for text, color in pairs:
        d.text((x, y), text, font=f, fill=color, anchor="lm")
        x += d.textlength(text, font=f)

    sx = pad
    sy = 196
    for i, color in enumerate(ladder):
        d.rounded_rectangle([sx, sy, sx + cell - 12, sy + 46], radius=6,
                            fill=rgba(color), outline=blend(t.fg, 0.18))
        d.text((sx + 8, sy + 60), f"depth {i + 1}", font=font("mono", 12),
               fill=blend(t.fg, 0.60))
        d.text((sx + 8, sy + 78), color.upper(), font=font("mono", 11),
               fill=blend(t.fg, 0.40))
        d.text((sx + 8, sy + 96), f"{contrast(color, t.bg):.1f}:1", font=font("mono", 11),
               fill=blend(t.fg, 0.35))
        sx += cell

    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "bracket-ladder.png")
    img.save(path, optimize=True)
    print("wrote", path)


def main():
    t = Theme()
    os.makedirs(OUT, exist_ok=True)
    render_palette(t)
    render_ladder(t)
    return 0


if __name__ == "__main__":
    sys.exit(main())