# Dracula Deep

<img src="icon.png" width="128" alt="Dracula Deep logo">

**The eye-care angle stated outright.**

A low-glare dark theme for VS Code. Dracula Deep takes a familiar warm-dark
layout and pulls every text color down out of maximum brightness, so a long
session reads as calm rather than glaring.

![Dracula Deep palette](icon.png)

## Why

Long coding sessions on a dark background are easier when nothing sits at peak
brightness. Dracula Deep is built around a measured palette rather than taste
alone — every foreground is checked against the `#101010` editor background:

| Role | Color | Contrast |
|---|---|---|
| plain text | `#A8A8A8` | 8.0:1 |
| variables | `#C0CAD4` | 11.5:1 |
| parameters | `#9FB0C0` italic | 8.6:1 |
| strings | `#7FAFA5` | 7.8:1 |
| numbers, constants | `#8B9E86` | 6.6:1 |
| keywords | `#9C8CC0` | 6.3:1 |
| functions | `#B99A6E` | 7.2:1 |
| types, classes | `#B2AE7C` | 8.4:1 |
| properties | `#8FA8C4` | 7.8:1 |
| brackets | `#7E8C99` | 5.5:1 |
| comments | `#6B6B6B` italic | 3.6:1 |

Every token clears WCAG AA (4.5:1). Comments are intentionally below it, at
3.6:1, because de-emphasising them is the point.

Run `scripts/check-contrast.py` to re-verify those numbers after any edit.

## Design notes

**Distinct hues, uniform loudness.** Token types are separated by hue rather
than brightness, so nothing dominates. The closest pair in the palette
(attribute vs property) still measures 60 ΔE apart.

**Brackets recede.** Structural punctuation uses dim slate instead of another
competing hue, so nesting is traceable without adding to the glare. Bracket
*nesting depth* gets its own six-step ladder via
`editorBracketHighlight.foreground1`–`foreground6`.

**UI accents muted.** Warm accents are reserved for focus and selection rather
than decoration. Buttons are dark grey, selected rows are neutral, focus rings
are soft blue, and the activity bar badge is muted amber.

## Install

From the marketplace:

```
ext install Sanjaya-Danushka.dracula-deep
```

Or build from source:

```sh
npm install -g @vscode/vsce
vsce package
code-insiders --install-extension dracula-deep-0.1.0.vsix
```

Then pick **Dracula Deep** from <kbd>Ctrl</kbd>+<kbd>K</kbd>
<kbd>Ctrl</kbd>+<kbd>T</kbd>.

## Author

**Sanjaya Danushka** <dsanjaya712@gmail.com>

## Credits

Theme structure and base palette are derived from
[Vesper](https://marketplace.visualstudio.com/items?itemName=raunofreiberg.vesper)
by Reuben Morgan, used under the MIT licence. Dracula Deep is an independent
palette layered on top and is not endorsed by the original author.

## License

MIT