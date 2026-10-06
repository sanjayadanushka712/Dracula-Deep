# Changelog

All notable changes to Dracula Deep are documented here.
This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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