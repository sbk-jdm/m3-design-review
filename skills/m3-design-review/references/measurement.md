# Measurement with scripts/measure.js

Check `warnings` first. If it contains `viewport-meta-missing` or `viewport-width-mismatch`, stop: the page was laid
out at a width you did not intend, so every size, overflow and target value is wrong. Fix the setup (see
[Setup check](#setup-check)) and measure again before you report anything.

`scripts/measure.js` (output `version` 1.1.0) is one self-contained function expression with no dependencies. It reads
the DOM, computed styles and hit tests of a rendered page and returns a JSON-serializable object. It sends nothing over
the network, does not change the DOM or styles and does not scroll; its only side effect is a transient `focus()` on
each focusable element, after which the previously focused element is restored. All sizes are CSS px (1dp = 1 CSS px).

Evidence labels: values read from the rendered page are `measured-rendered`; values read from source or declared CSS
without rendering are `measured-code`; values taken under a simulation (narrow viewport for text zoom, emulated
setting) are `measured-simulation`; values inferred from an image are `estimated`.

## How to run

Playwright (Python):
```python
src = open("scripts/measure.js", encoding="utf-8").read()
ctx = browser.new_context(viewport={"width": 360, "height": 800}, is_mobile=True, has_touch=True)
page = ctx.new_page(); page.goto(url); page.wait_for_load_state("networkidle")
result = page.evaluate(src, {"expectWidth": 360})      # options are optional
```

Playwright (Node): `const result = await page.evaluate(\`(${src})(${JSON.stringify({ expectWidth: 360 })})\`);`

Browser-automation JS tool or DevTools console: paste `(` + file contents + `)({expectWidth: 360})` and copy the result.

Widths: use the widths the project adapter names; they win over anything here. Without an adapter, measure one compact
width (360 or 390). A second, expanded width (for example 1280) is optional: add it only when the product is used on
large screens. Repeat per theme (`page.emulate_media(color_scheme="dark")` or the page's own switch) and, for motion,
with `reduced_motion="reduce"`. Wait for fonts and data before measuring.

If no browser is available, read the code instead: label a value `measured-code` only when it is explicit (a declared
`height: 32px`), otherwise `estimated`.

## Options

| Option | Default | Meaning |
| --- | --- | --- |
| `maxItems` | 40 | Max items kept per list (`count` is always the full total; `truncated: true` if items were cut) |
| `maxElements` | 6000 | Max elements scanned in document order (also caps ARIA and `nonTextSelectors` scans) |
| `maxFocus` | 80 | Max elements focused in the focus check (`0` skips it) |
| `minTarget` | 48 | Target threshold in CSS px; 44 for pointer-only desktop surfaces (A11-17) |
| `minTextPx` | 12 | Small-text threshold in CSS px (A11-30 default; an adapter may raise it) |
| `maxProperties` | 200 | Max `:root` custom properties listed |
| `hitScan` | true | Effective hit areas from the box, `::before`/`::after` geometry and a hit-test probe; `false` gives the v0.1 box-only result |
| `maxProbe` | 300 | Max small-target candidates probed with `elementFromPoint` |
| `expectWidth` | none | Expected CSS viewport width; a different `innerWidth` raises `viewport-width-mismatch` |
| `nonTextSelectors` | [] | CSS selectors of extra graphics (chart segments, legend swatches, status dots) checked at 3:1 against the background behind them |

## Output fields and the rules they feed

| Field | Content | Rules |
| --- | --- | --- |
| `warnings` | Setup problems: `viewport-meta-missing`, `viewport-width-mismatch` | Stop and fix the setup |
| `viewport` | innerWidth/Height, clientWidth, devicePixelRatio, color scheme, reduced motion, root font size, `metaViewport`, `expectWidth`, `mismatch` | Window size class (LAY rules) |
| `document.lang`, `dir` | `<html lang>` and direction | A11-12; RTL rules |
| `document.viewportMeta`, `viewportMetaMissing`, `zoomDisabled` | Viewport meta; true if `user-scalable=no` or `maximum-scale` <= 1 | A11-08, WRT-01 |
| `document.h1Count`, `headingCount`, `headingSkips`, `headingOutline`, `h1CountAll`, `mainCount` | Headings exposed to assistive tech (hidden views excluded; `h1CountAll` counts every `h1`), skipped levels, first headings, `main` landmarks | A11-35 (headings present), A11-22 (no skipped level), A11-20 |
| `smallTargets` | Interactive elements whose effective hit area is under `minTarget`: `width`/`height` (= `hitWidth`/`hitHeight`), `visualWidth`/`visualHeight`, `hitAreaVia`, `probe`, `covered`, `inlineTextLink`, `disabled` | A11-01, A11-16, A11-13, component target rules |
| `smallText` | Elements whose own text is under `minTextPx` | A11-30, TYP-01 |
| `contrastFailures` | Text below 4.5:1, or 3:1 for large text (>= 24 px, or >= 18.66 px and weight >= 700) | COL-05, COL-06, TYP-02, TYP-03 |
| `contrastUnresolved` | Text over an image or gradient; check by hand | COL-05 (`estimated`) |
| `nonTextContrast` | `part` (`border`, `fill`, `outline`), `ratio`, `required` 3, `kind` (`field`, `control`, `selector`), colors, `fillRatio`, `vsPrevious` (selector items) | Fields: TXF-04; outlined controls: COL-22, COL-23, BTN-08, SEG-04; groups: COL-08; `selector` items: A11-03, A11-29 |
| `truncated` | Text cut by `text-overflow: ellipsis`, line clamp, or a no-wrap clipping box: `text`, `via`, `hasTitle`, `nameHasFullText` | A11-09, TXF-05 |
| `layoutOverflow` | `documentScrollWidth`, `horizontalScroll`, and boxes with `overflow: hidden/clip` whose text content overflows (`axis`, scroll and client sizes) | A11-08, WRT-01 (with the 200% recipe) |
| `labelInName` | Controls with `aria-label`/`aria-labelledby` whose name does not contain the visible text (normalized, case-insensitive) | A11-31 |
| `ariaConflicts` | `issue` per element: `aria-pressed` on a non-button role, `aria-checked`/`aria-selected` on roles that do not support them, tab without `aria-selected` or outside a tablist, radio/checkbox/switch without `aria-checked`, radio outside a radiogroup, option or menuitem outside its container, composite widget with several tab stops, `aria-hidden` on or around focusable elements, nested buttons or links | A11-26, A11-12, A11-32 (tab stops), A11-34 (`aria-hidden` focusables) |
| `unnamedControls` | Interactive elements with no accessible name; `iconOnly` hints at icon buttons | A11-07, A11-23 |
| `imagesWithoutAlt` | `<img>` without `alt`, `role="img"` without a name | A11-27, A11-25 |
| `focusNotVisible`, `focusWeak` | No visible change on focus; or only border, background, color or decoration changes | A11-05, INT-12 |
| `customProperties` | `:root`/`html` custom properties; `mdSysCount` counts `--md-sys-*` | COL-01, token rules |
| `fontFamilies`, `radiusHistogram` | Font stacks by frequency; corner radii with examples | TYP-06, TYP-07, SHP-01, SHP-02 |
| `motion` | Reduced-motion query found, animated and transitioned element counts | MOT-06, A11-15 |
| `stats`, `notes`, `thresholds` | Coverage counters (including hit-probe and non-text counts), caps hit | State coverage in the report |

`nonTextContrast` checks every form field, and interactive elements that draw a border or a rest-state outline. A
component passes if its fill or any drawn boundary reaches 3:1 against what is behind it; the item names the boundary
the design relies on. Filled or text-only controls without a border are not checked: their label identifies them.
For chip or button borders under 3:1, judge with COL-22/COL-23 (and CMP-01 for a chip row that works as a selector).

## Setup check

1. `warnings` must be empty. `viewport-meta-missing`: the page has no `<meta name="viewport">`; mobile browsers and
   mobile emulation (`is_mobile=True`) lay it out at about 980 px. That is itself a finding for the page, but measure
   the intended layout anyway: add the tag in a local copy or test build and rerun. `viewport-width-mismatch`:
   `innerWidth` differs from `expectWidth`; fix the harness (viewport size, device emulation, zoom) and rerun.
2. Check `viewport.innerWidth` and `devicePixelRatio` against what you meant to emulate, and `viewport.prefersDark`
   against the theme you are reviewing.
3. Confirm the content rendered (non-zero `stats.textElementsChecked`, expected headings in `document.headingOutline`).
   An error page or empty shell measures cleanly and proves nothing.

## Effective hit areas

With `hitScan` on, each interactive element under `minTarget` in its box gets an effective hit area from:

- the element box, or its associated `<label>` when larger (`hitAreaVia: "box"` or `"label"`);
- absolutely positioned `::before`/`::after` (`"pseudo"`). The band is computed from the containing block's padding
  box plus the insets, so a border shrinks it: a 36 px chip with `inset: -6px` and a 1 px border gives 34 + 12 = 46 px,
  not 48. Transforms on the pseudo-element and `overflow` clipping by the containing block and its ancestors are
  applied;
- a probe (`"probe"`): `elementFromPoint` walks out from each edge along the center lines while the hit still lands on
  the element, a descendant or its label. It runs only when the element center is inside the viewport. When it
  disagrees with geometry by more than 1 px, the probe wins: a child element enlarges the target, a neighbour's band
  overlaps it, or a clipping box cuts it.

`probe` says what happened: `ok`; `covered` (something else is on top of the center, for example a fixed bar; decide
whether that is true when the user taps it); `offscreen` (geometry only; scroll the element into view in the harness,
never in the script, and run again for confirmation); `limited` (the viewport edge stopped the probe; geometry used).
Report `hitWidth` x `hitHeight` as `measured-rendered`, and give the visual size beside it when they differ.
Spacing between targets (A11-02, A11-18) is not measured; overlapping bands show up as a shorter probe result.

## Recipe: text at 200%

Reflow method (web equivalent of 200% zoom): render at half the target CSS width, for example 180 px for a 360 px
target, and measure.

```python
page.set_viewport_size({"width": 180, "height": 800}); page.wait_for_timeout(300)
r = page.evaluate(src, {"expectWidth": 180})
print(r["layoutOverflow"], r["truncated"]["items"], r["warnings"])
page.screenshot(path="text-200.png", full_page=True)   # look for overlaps and cut-off text
```
Node: `await page.setViewportSize({ width: 180, height: 800 }); const r = await page.evaluate(\`(${src})({expectWidth: 180})\`);`

Read `layoutOverflow.horizontalScroll` (two-dimensional scrolling for ordinary text is a failure), its items (text
clipped inside a fixed box), `truncated` (new ellipses: is the full text reachable?) and the screenshot for overlapping
text. Font-scale variant: when the app has its own text-size setting, set it to the largest value at the normal width
and repeat; pages sized in `rem` from the browser default can also be tested with Chromium's experimental
`Page.setFontSizes` (CDP). Label results `measured-simulation` and recommend confirming on a real device with the OS
text size at its maximum (A11-08, WRT-01).

## Recipe: focus flow

Drive the keyboard and read `document.activeElement` at each step (A11-10, A11-11, A11-32, A11-33, A11-34).

```python
who = "() => { const a = document.activeElement; return a ? a.tagName.toLowerCase() + (a.id ? '#' + a.id : '') + ' ' + (a.getAttribute('aria-label') || a.textContent || '').trim().slice(0, 30) : null }"
page.focus("#open-menu"); page.keyboard.press("Enter")
print("open", page.evaluate(who))           # menu/dialog/sheet: focus inside it (first item, title or first control)
for _ in range(15): page.keyboard.press("Tab")
print("tabbed", page.evaluate(who))         # modal: still inside; menu: closed or still inside, never behind it
page.keyboard.press("Escape")
print("escape", page.evaluate(who))         # closed, focus back on #open-menu
```
Node: `await page.focus('#open-menu'); await page.keyboard.press('Enter'); console.log(await page.evaluate(who));`

- Menus, dialogs, sheets: check after open, after Tab past the last item, after Escape (and the scrim or Back for
  sheets). Content behind a modal surface must not receive focus (`inert` or equivalent).
- Tabs and radiogroups: focus the selected item, press ArrowRight/ArrowLeft and check that focus and the selection
  state move; one Tab must leave the group (roving tabindex). `ariaConflicts` flags groups with several tab stops.
- Page or view changes: activate a navigation destination and check focus lands in the new view (its heading or first
  control), not on `<body>` or a hidden control; go back and check focus returns to the control that opened it.
With a browser-automation tool instead of Playwright, send the same keys and evaluate the `who` expression.
Label results `measured-rendered`.

## How to use the output

- Every item is a candidate. Confirm it against the rule and the element's role before reporting.
- Merge items with the same cause (one shared component) into one finding with a count and up to three selectors.
- Selectors are hints (`tag#id`, or up to four `tag.class:nth-of-type()` steps), not guaranteed unique.
- Report values exactly as measured, with their evidence label. Do not paste or save the raw JSON: it may contain
  page text.

## Limits (state them when they matter)

- Hit areas: the probe checks only the center lines and only inside the viewport; transforms on the element itself,
  `position: fixed` pseudo-elements and `clip-path` are ignored; a larger clickable parent is a separate target.
- Contrast uses composited ancestor background colors only: not seen are content positioned behind that is not an
  ancestor, `backdrop-filter`, blend modes, text shadows, images and gradients (unresolved), ancestor opacity (noted)
  and canvas text. Without an opaque background a white canvas is assumed and noted.
- Non-text contrast compares against the background behind the element, not between adjacent parts; icons, focus
  rings and SVG gradient fills are not checked; pass chart parts with `nonTextSelectors`.
- Truncation is detected only when CSS clips (`text-overflow`, line clamp, no-wrap clipping box); strings shortened
  in code ("...") are not seen. `layoutOverflow` also lists intentional crops (thumbnails, carousels): confirm each.
- Names: simplified computation (no `aria-describedby`, CSS generated content or shadow DOM); placeholder counts as a
  weak name. `labelInName` runs only on controls with `aria-label`/`aria-labelledby`; icon-font glyphs are skipped.
- `ariaConflicts` is a heuristic subset of ARIA rules, not a validator. Shadow DOM and iframes are not traversed.
- Focus: `:focus-visible` styles are seen only if the browser matches it after a scripted `focus()`
  (`focusVisibleMatched`); transitions may read as their start value (`hasTransition`). On pages with
  focus-triggered side effects, use a test build or `maxFocus: 0`.
- Hover, pressed, dragged and selected states are not exercised; only rest state and focus.
- Reduced motion: only the presence of a query in readable stylesheets; not JavaScript motion; cross-origin sheets
  are counted in `stylesheetsUnreadable`.
- Custom properties on other selectors are not listed; font families are declared stacks, not rendered faces.
- Elements beyond `maxElements` and probes beyond `maxProbe` are skipped; `notes` says so.
