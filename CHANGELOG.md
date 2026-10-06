# Changelog

All notable changes to Dracula Deep are documented here.
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.1] - 2026-10-06

### Fixed

- The second README screenshot carried a hardcoded `width="1859" height="955"`.
  GitHub narrows the width to its column but left the height pinned at 955px,
  stretching the image vertically and blurring it. It now scales from its own
  aspect ratio, the way the first screenshot always has.

## [1.1.0] - 2026-10-06

### Changed

- Inactive tab label darkened `#828282` → `#5A5A5A` so the active tab is the
  only light label in the strip. Active stays `#E8E8E8`; the light/dark gap
  widens from 2.82× to 5.07×. Both labels stay legible against their
  backgrounds.
- Active tab's bottom rule darkened `#B99A6E` → `#7A6446`, taking it from
  7.17:1 to 3.39:1 against the tab bar — same amber, markedly less glare.
  The top rule remains `#B99A6E`.
- The bracket-pair ramp was six near-identical blue-greys (`#7E8C99` through
  `#A8A8A8`) that rendered as a single colour. The six levels now cycle
  amber → green → blue → purple → teal → pink, every one of them a colour
  already used elsewhere in the syntax palette, inside a tight 6.3–7.8:1
  brightness band.

### Added

- `tab.activeModifiedBorder` `#D9B98A` and `tab.inactiveModifiedBorder`
  `#6B5636`, so modified tabs carry their own marker independent of the
  accent rule.
- Explicit `gitDecoration.untrackedResourceForeground` `#7FA37A` and
  `gitDecoration.modifiedResourceForeground` `#B99A6E` instead of relying on
  whatever the editor defaults to.

## [1.0.0] - 2026-10-06

### Changed

- Rebuilt the tab strip as a four-step background ladder so the active tab is
  findable from the background alone, not only from the accent border:
  editor `#101010` (4.7 L*) → inactive `#161616` (7.2) → hover and
  unfocused-active `#1C1C1C` (10.3) → active `#202020` (12.3).
  Inactive tabs now sit 2.6 L* above the editor and the active tab a further
  5.0 L* above inactive, with each step subtle enough to stay low-glare.
- Active tab label raised `#A8A8A8` → `#E8E8E8`, moving it from 6.85:1 to
  13.30:1 against the active background. The active/inactive label gap was
  only 1.46×, too small to pick a tab out of a row; it is now 2.82×.
  Backgrounds and the accent border are deliberately untouched.

### Fixed

- Added `tab.unfocusedActiveBackground`. Without it the active tab in a
  non-focused editor group had no background of its own.
- Inactive tab labels moved `#7A7A7A` → `#828282`, clearing 4.5:1 against the
  lighter inactive tab background (4.71:1).

## [0.1.1] - 2026-10-06

### Fixed

- Active tab was visually indistinguishable from inactive tabs
  (`tab.activeBackground` differed by only 2.6 L*, a 1.05:1 ratio).
  Active background now `#1C1C1C` (5.6 L* apart) and the accent border uses
  `#B99A6E`, raising it from 2.6:1 to 6.4:1.
- Added `tab.unfocusedActiveBorder`. Without it, the active tab in a
  non-focused editor group had no border at all.
- Added `tab.hoverBackground`.

## [0.1.0] - 2026-10-06

### Added

- Initial release. The eye-care angle stated outright: a low-glare dark theme
  with a dimmed syntax palette and muted UI accents.
- Syntax tokens separated by hue rather than brightness, all clearing 5:1
  contrast except comments (3.6:1, intentionally de-emphasised).
- Six-step bracket-depth ladder via `editorBracketHighlight.foreground1-6`.
- Structural punctuation in dim slate so nesting is traceable without glare.
- 90 UI colour overrides muting the warm accent across 15 slots, including
  selected rows, buttons, focus rings, and the active tab border.
- `scripts/check-contrast.py` verifies every token against WCAG AA.