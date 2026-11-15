# Measurement with scripts/measure.js

`scripts/measure.js` is one self-contained function expression with no dependencies. It reads computed styles and the
DOM of a rendered page and returns a JSON-serializable object. It sends nothing over the network and does not change
the page; its only side effect is a transient `focus()` on each focusable element, after which the previously focused
element is restored.

On the web, treat 1dp as 1 CSS px. All sizes in the output are CSS px.

## How to run

The file evaluates to a function. Pass its full text to the tool; options are optional.

Playwright (Python):
```python
src = open("scripts/measure.js", encoding="utf-8").read()
page.set_viewport_size({"width": 390, "height": 844})
result = page.evaluate(src)                     # or page.evaluate(src, {"maxItems": 60})
```

Playwright (Node): `const result = await page.evaluate(\`(${src})()\`);`

Browser-automation JS tool or DevTools console: paste `(` + file contents + `)()` and run; copy the returned object.

Run once per viewport (for example 390 px compact and 1280 px expanded) and per theme. For dark theme use
`page.emulate_media(color_scheme="dark")` or the page's own theme switch; for reduced motion,
`page.emulate_media(reduced_motion="reduce")`. Wait until fonts and content have loaded
(`page.wait_for_load_state("networkidle")` or the page's own ready signal) before measuring.

If no browser is available, read the code instead and label findings `measured` only when the value is explicit in the
code (a declared `height: 32px`), otherwise `estimated`.

## Options

| Option | Default | Meaning |
| --- | --- | --- |
| `maxItems` | 40 | Max items kept per list (`count` is always the full total; `truncated` says if items were cut) |
| `maxElements` | 6000 | Max elements scanned in document order |
| `maxFocus` | 80 | Max elements focused in the focus check |
| `minTarget` | 48 | Target threshold in CSS px; use 44 for pointer-only desktop surfaces (A11-17) |
| `minTextPx` | 12 | Small-text threshold in CSS px |
| `maxProperties` | 200 | Max `:root` custom properties listed |

## Output fields and the rules they feed

| Field | Content | Rules to check against |
| --- | --- | --- |
| `viewport` | innerWidth/Height, clientWidth, devicePixelRatio, prefers-color-scheme, prefers-reduced-motion, root font size | Window size class (LAY rules); scale for any screenshot taken alongside |
| `document.lang`, `dir` | `<html lang>` and direction | A11-12; RTL rules in layout-interaction-a11y.md |
| `document.viewportMeta`, `viewportMetaMissing`, `zoomDisabled` | Viewport meta text; true if `user-scalable=no` or `maximum-scale` <= 1 | A11-08, WRT-01 (text scaling / zoom) |
| `document.h1Count`, `mainCount` | Heading and landmark counts | A11-20, A11-22 |
| `smallTargets` | Interactive elements under `minTarget` in width or height; size uses the larger of the element box and an associated `<label>` box (`hitAreaVia: "label"`); `inlineTextLink` marks links inside running text | A11-01, A11-16, A11-13, component target rules |
| `smallText` | Elements whose own text is under `minTextPx` | TYP-01 (type scale); readability |
| `contrastFailures` | Text below 4.5:1, or 3:1 for large text (>= 24 px, or >= 18.66 px and weight >= 700); color, background, ratio | COL-05, COL-06, TYP-02, TYP-03, component contrast rules |
| `contrastUnresolved` | Text whose background could not be resolved (image or gradient on an ancestor) | Check by hand or from a screenshot; label `estimated` |
| `unnamedControls` | Interactive elements with no accessible name; `iconOnly` hints at icon buttons | A11-07, A11-23, ICO-06, ICO-07 |
| `imagesWithoutAlt` | `<img>` with no `alt` attribute (not `alt=""`), and `role="img"` without a name | A11-27, A11-25 |
| `focusNotVisible` | Focusable elements with no visible change on focus (outline, box-shadow, border, background, color, text decoration all unchanged, on the element and its parent) | A11-05, INT-12 |
| `focusWeak` | Focus changes only border, background, color or decoration; no ring-like outline or shadow | INT-12 (ring expected); report as suggestion unless the change is hard to see |
| `customProperties` | Custom properties declared on `:root` or `html`, with computed values; `mdSysCount` counts `--md-sys-*` | COL-01, TOK rules (are roles used as tokens?) |
| `fontFamilies` | Computed font-family stacks of text elements, by frequency | TYP-06, TYP-07, TYP-16 |
| `radiusHistogram` | Corner radius values with counts and examples; `(pill/full)` when radius >= half the short side | SHP-01, SHP-02, component shape rules |
| `motion` | Whether any readable stylesheet has a `prefers-reduced-motion` query; counts of animated and transitioned elements; unreadable sheets | MOT-06 |
| `stats`, `notes`, `thresholds` | Coverage counters, caps hit, and the thresholds used | State coverage in the report |

## How to use the output

- Treat every item as a candidate. Confirm it against the rule and the element's role before reporting.
- Merge items with the same cause into one finding with a count and up to three example selectors.
- Selectors are hints (`tag#id`, or up to four `tag.class:nth-of-type()` steps); they are stable enough to find the
  element, not guaranteed unique.
- Report values exactly as measured; label the finding `measured`.
- Do not paste the raw JSON into the report. Do not save it; it may contain page text.

## Limits (state them when they matter)

- Hit areas extended by `::before`/`::after`, negative margins, a larger invisible parent, or `touch-action`
  wrappers are not seen. A target reported small may be fine: check the CSS before reporting.
- Target spacing (A11-02, A11-18) is not measured.
- Contrast is computed against the composited background colors of ancestors only. Not seen: elements positioned
  over other content that is not an ancestor, `backdrop-filter`, `mix-blend-mode`, text shadows, background images
  and gradients (reported as unresolved), ancestor opacity (noted), and canvas or SVG text fills. If no opaque
  background is found, a white canvas is assumed and noted; on dark pages that set the color only on a non-ancestor
  this gives false results.
- Non-text contrast (borders, icons, component containers against their background: COL-08, COL-22, BTN-08) is not
  measured. Check it from code or a screenshot.
- Placeholder text counts as a (weak) accessible name; ARIA name computation is simplified (no `aria-describedby`,
  no CSS generated content, no name from shadow DOM content).
- Shadow DOM and iframes are not traversed; only the top document's light DOM is scanned.
- Focus: styles applied only through `:focus-visible` are seen only if the browser matches `:focus-visible` after a
  scripted `focus()` (`focusVisibleMatched` reports it; headless Chromium does when no pointer was used). Styles
  that animate in with a transition may read as their start value (`hasTransition` marks these). Focus handlers on
  the page run when an element is focused; on pages with focus-triggered side effects, run the check on a test build
  or skip it (`maxFocus: 0`).
- State styles (hover, pressed, dragged, selected) are not exercised; only the rest state and focus are measured.
- Reduced motion: the script only detects that a query exists in a readable stylesheet, not that it covers every
  animation, and not motion driven from JavaScript. Cross-origin stylesheets cannot be read (counted in
  `stylesheetsUnreadable`).
- Custom properties declared on other selectors (`body`, `.theme-dark`) are not listed; they still affect
  computed values.
- Font families are the declared stacks; the script does not check which face actually rendered.
- Text size and type scale: the script reports sizes under the threshold only; mapping every text element to a type
  role is a reviewer task.
- Elements beyond `maxElements` are not scanned; `notes` says so.
