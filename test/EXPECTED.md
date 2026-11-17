# Expected results for seeded-violations.html

Run: `python3 test/check.py` (Python Playwright; add `--chrome /path/to/chrome` if the bundled browser is missing,
`--dump` to print the full JSON). Viewport 390 x 844 CSS px, light scheme, options
`{"expectWidth": 390, "nonTextSelectors": [".bar > i"]}`. Every row must pass.

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
| V17 | `button#v17` | 36 px chip, `::after` `inset: -6px`, 1 px border: band 34 + 12 = 46 px | `smallTargets` item, `visualHeight` 36, `hitHeight` ~46, `hitAreaVia` `pseudo` | A11-01 |
| V18 | `div#v18` | Ellipsis-truncated label without `title` | `truncated` item, `via` `ellipsis`, `hasTitle` false | A11-09 |
| V19 | `input#v19` | Field fill #ece6f0 on card #f7f2fa (~1.11:1), no border | `nonTextContrast` item, `part` `fill`, `kind` `field` | TXF-04 |
| V20 | `button#v20` | `aria-label="Submit form"`, visible text "Send now" | `labelInName` item | A11-31 |
| V21 | `button#v21` | `role="radio"` with `aria-pressed` (and no `aria-checked`) | `ariaConflicts` item mentioning `aria-pressed` | A11-26, A11-32 |
| V22 | `h1#v22` | `h1` inside a `hidden` section | `document.h1Count` 1 (`h1CountAll` 2), `headingCount` 2 | A11-22, A11-35 |
| V23 | `div#v23` | 320 px row inside a 200 px `overflow: hidden` box | `layoutOverflow` item; `horizontalScroll` false | A11-08 |
| V24 | `i#v24` | Chart segment #eeeeee on the card (~1.05:1) | `nonTextContrast` item, `kind` `selector` | A11-29, A11-03 |

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
| `ok-chip-pseudo` | 36 px chip, no border, `::after` `inset: -6px`: 48 px |
| `ok-icon-centered` | 24 px icon button with a centered, translated 48 px `::before` |
| `ok-fits` | Ellipsis set but the text fits |
| `ok-field` | Field with a 1 px #79747e border (~4.1:1) |
| `ok-labelname` | `aria-label` contains the visible text |
| `ok-radio` | Valid `role="radio"` with `aria-checked`, roving tabindex |
| `ok-seg` | Chart segment #6750a4 (passes 3:1) |

Inventory lists (`radiusHistogram` examples) are excluded from the negative check.

## Hit-test probe, options and setup

| ID | Check |
| --- | --- |
| P2 | `button#ok-child-hit` (a child `span` with `inset: -6px` gives 48 px) is below the fold in the main run: reported with `probe` `offscreen`, `hitAreaVia` `box` (documents the limit) |
| P3 | After the harness scrolls V17 into view: `probe` `ok` confirms the 46 px pseudo band |
| P4 | In view: `ok-chip-pseudo` and `ok-child-hit` (found by the probe) are not reported |
| H1 | `hitScan: false` reproduces the v0.1 box-only result (`ok-chip-pseudo` reported at 36 px) |
| W1 | Main run: `warnings` empty, `viewport.mismatch` false |
| W2 | `test/no-viewport.html` in a mobile context (`is_mobile`) with `expectWidth: 390`: `warnings` has `viewport-meta-missing` and `viewport-width-mismatch`; `innerWidth` 980 |
| W3 | Seeded page in the same mobile context: no warnings |

## Script integrity

| ID | Check |
| --- | --- |
| M1 | `document.documentElement.outerHTML` is identical before and after the run |
| M2 | Focus is restored (here: back to `<body>`) |
| M3 | Invoking as `(<source>)()` gives the same result as `page.evaluate(source)` |
| M4 | Scroll position unchanged by the script |
