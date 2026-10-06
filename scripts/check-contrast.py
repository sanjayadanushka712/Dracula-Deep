#!/usr/bin/env python3
"""Verify Dracula Deep meets its contrast targets.

Reads themes/dracula-deep-color-theme.json, computes the WCAG contrast ratio of
every token foreground against the editor background, and fails if anything
unexpected drops below AA. Comments are a deliberate exception: they are meant
to recede.

    python3 scripts/check-contrast.py
"""
import json
import os
import sys

THEME = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "themes", "dracula-deep-color-theme.json",
)

AA = 4.5
BELOW_AA_ALLOWED = ("comment",)


def relative_luminance(hex_color):
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    channels = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]

    def linearize(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (linearize(c) for c in channels)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(fg, bg):
    a, b = relative_luminance(fg), relative_luminance(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def main():
    theme = json.load(open(THEME))
    bg = theme["colors"]["editor.background"]
    print(f"{theme['name']}  background {bg}\n")

    rows = [("editor.foreground", theme["colors"]["editor.foreground"], False)]
    for rule in theme["tokenColors"]:
        foreground = rule.get("settings", {}).get("foreground")
        if not foreground:
            continue
        scope = rule.get("scope") or []
        label = rule.get("name") or (scope[0] if scope else "(default foreground)")
        exempt = any(s in BELOW_AA_ALLOWED for s in scope) or rule.get("name") in BELOW_AA_ALLOWED
        rows.append((label, foreground, exempt))

    failures = []
    for label, color, exempt in rows:
        ratio = contrast_ratio(color, bg)
        status = "ok"
        if ratio < AA:
            if exempt:
                status = "below AA (exempt)"
            else:
                status = "FAIL"
                failures.append(label)
        print(f"  {label:<28} {color}  {ratio:>5.1f}:1  {status}")

    print()
    if failures:
        print(f"{len(failures)} below AA: {', '.join(failures)}")
        return 1
    print(f"all {len(rows)} colors meet AA ({AA}:1), comments exempt")
    return 0


if __name__ == "__main__":
    sys.exit(main())