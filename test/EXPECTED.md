# Expected results for seeded-violations.html

Run: `python3 test/check.py` (Python Playwright; add `--chrome /path/to/chrome` if the bundled browser is missing,
`--dump` to print the full JSON). Viewport 390 x 844 CSS px, light scheme. Every row must pass.

## Seeded violations

| ID | Element | Violation | Expected in measure.js output | Rule a reviewer would cite |
| --- | --- | --- | --- | --- |
| V01 | `<html>` | No `lang` attribute | `document.lang` is `null` | A11-12 (semantics; WCAG language of page) |
| V02 | viewport meta | `maximum-scale=1, user-scalable=no` | `document.zoomDisabled` is `true` | A11-08, WRT-01 |
| V03 | `button#v03` | Target 32 px tall | `smallTargets` item, `height` 32 | A11-01, A11-16 |
| V04 | `button#v04` | Icon-only button without accessible name | `unnamedControls` item, `iconOnly: true` | A11-07, A11-23 |
| V05 | `img#v05` | Image without `alt` | `imagesWithoutAlt` item | A11-27 |
| V06 | `p#v06` | Text 10 px | `smallText` item, `fontSizePx` 10 | TYP-01 (no size outside the scale) |
| V07 | `p#v07` | #999 on white, 14 px: 2.85:1 | `contrastFailures` item, `required` 4.5 | COL-05, TYP-02 |
| V08 | `p#v08` | #aaa on white, 24 px: 2.32:1 | `contrastFailures` item, `large: true`, `required` 3 | COL-06, TYP-03 |
| V09 | `p#v09` | Text on a gradient | `contrastUnresolved` item, reason contains `gradient` | COL-05 (verify by hand) |
| V10 | `button#v10` | Focus outline and shadow removed | `focusNotVisible` item | A11-05, INT-12 |
| V11 | stylesheet | Animation present, no `prefers-reduced-motion` query | `motion.reducedMotionQueryFound` false, `elementsWithAnimation` >= 1 | MOT-06 |
| V12 | `div#v12` | Corner 7 px, not on the shape scale | `radiusHistogram` has `7px` | SHP-01 |
| V13 | `p#v13` | Decorative script face for body text | `fontFamilies` lists `"Comic Sans MS"` | TYP-06 |
| V14 | `p#v14` | `rgba(0,0,0,.3)` text: about 2.1:1 after compositing | `contrastFailures` item | COL-05 |
| V15 | `input#v15` | Text field without label, 34 px tall | `unnamedControls` and `smallTargets` items | A11-07, A11-01 |
| V16 | `p#v16` | `color-mix()` text color, about 1.9:1 (tests the canvas color path) | `contrastFailures` item | COL-05 |

Also checked: `customProperties.count` is 4 and `customProperties.mdSysCount` is 2 (P1).

## Negative controls (must not be reported)

| ID | Why it must pass |
| --- | --- |
| `ok-button` | 48 px target, named, visible `:focus-visible` outline |
| `ok-disabled` | Low contrast but disabled (exempt, counted in `stats.contrastExemptDisabled`) |
| `ok-large` | #949494 at 24 px: 3.03:1, passes the large-text threshold |
| `ok-decorative` | `alt=""` marks a decorative image |
| `ok-sronly` | Visually hidden text (1 px clipped box) |
| `ok-checkbox` | Native checkbox whose wrapping label gives a 48 px hit area |
| `ok-inline` | Inline text link: reported in `smallTargets` but marked `inlineTextLink: true` (reviewer decides) |

## Script integrity

| ID | Check |
| --- | --- |
| M1 | `document.documentElement.outerHTML` is identical before and after the run |
| M2 | Focus is restored (here: back to `<body>`) |
| M3 | Invoking as `(<source>)()` gives the same result as `page.evaluate(source)` |
