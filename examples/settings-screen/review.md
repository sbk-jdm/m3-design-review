# M3 design review: Settings screen (habit-tracking PWA)

Surface: `examples/settings-screen/implementation.html`, rendered from a local server in headless Chrome (Playwright), web (PWA), compact window size class (plus one expanded check at 1024 px for AC-03 and AC-14)
Viewports and themes: 360, 390 and 412 x 800 CSS px with mobile emulation (DPR 2 for measure.js runs, DPR 1 for focus screenshots), 1024 x 800 for AC-03/AC-14; light and dark (emulated `prefers-color-scheme` and the in-app Theme setting); in-app text size Small, Medium and Large at every compact width; browser text 200% simulated two ways: reflow at 180 and 195 CSS px (zoom), and Chromium `Page.setFontSizes` with a 32 px default font (text size) at 360 and 390 px with in-app Large; offline, reduced motion and denied notification permission emulated; test hooks `?delay=`, `?fail=`, `?profile=`, `?unsynced=1`, `?seed=1` used for states.
Tolerance: inspired (set by user; the brief states the same)
References snapshot: 2026-05-21 (within 6 months; it passes the 6-month mark on 2026-11-21)
Project guidelines: brief "Design brief: Settings screen (habit-tracking PWA)" (2026-11-17)   Decisions ledger: not found (brief decisions B-01..B-20 used as recorded decisions)
Evidence: measured-rendered 5, measured-code 2, measured-simulation 2, estimated 0. 4 findings suppressed by recorded decisions (B-06 TMP-01/TMP-02, B-11 DLG-01 level3 shadow, B-12 BTN-04, B-13 PRG-02 size).
Privacy: no personal data visible (placeholder profile "Sample User" and seeded placeholder habits only)

Setup: every measure.js run had empty `warnings` (viewport meta present, `innerWidth` equal to `expectWidth`); no setup fix was needed.

## Summary

The screen follows the brief closely: geometry, color roles, tokens, text-size scaling, persistence, offline and dialog flows all match, and 34 of 37 acceptance criteria pass. The most important problem is keyboard focus on the Back button and the dialog buttons: the focus ring is drawn on a pseudo-element that sits at 10% opacity, so it is practically invisible (AC-25). Other floor problems: the Reminder time field has a 41 px tall hit area (AC-30), the first Tab skips Back, dialog actions are cut off at 200% zoom, and the avatar initials overlap the name at 200% text with in-app Large (AC-36).

```
Issues: F 6, C 1. Suggestions: C 2, E 0. Notes: 0. Not reviewed: RTL, real-device OS text scaling, screen-reader speech output, hover/pressed visuals on rows beyond computed styles.
```

## Brief acceptance criteria

Brief: Design brief: Settings screen (habit-tracking PWA), screen, 2026-11-17. Result: pass 34, fail 3, not checked 0.

| AC | Criterion (short) | Result | Evidence |
| --- | --- | --- | --- |
| AC-01 | Row content 16 px from left, trailing controls 16 px from right at 360/390/412 | pass | measured-rendered: every `.row` leading content starts at x = 16 px; `.sw` right inset 16 px; `.tf-box` 16 px each side; all three widths, both themes |
| AC-02 | App bar 64 px, full width, square, Back + "Settings" only | pass | measured-rendered: `header.appbar` 390 x 64 px, `border-radius: 0px`, 1 button (`#back`), h1 "Settings" |
| AC-03 | 1024 px: content column 600 px centered, app bar full width | pass | measured-rendered: `main` x = 212, width 600, right inset 212; app bar 1024 px wide |
| AC-04 | 360 px, browser text 200% + Large: vertical scroll only | pass | measured-simulation: `scrollWidth` 360 = `innerWidth` (root font 32 px, row label 40 px); reflow at 180 px also gives `scrollWidth` 180 |
| AC-05 | App bar fill surface to surface-container on scroll, no shadow | pass | measured-rendered: `rgb(243,252,242)` to `rgb(232,240,230)` light, `rgb(14,21,12)` to `rgb(27,33,26)` dark; `box-shadow: none` |
| AC-06 | Row heights (56 / 72 px minimums) | pass | measured-rendered at 390: Sign out and 8 radio rows 56 px; account, Daily reminder, Export, Delete 72 px (80 px at 360 where supporting text wraps) |
| AC-07 | Switch track 52 x 32, handle 16 off / 24 on | pass | measured-rendered: track 52 x 32 px; handle 16 x 16 off, 24 x 24 on (permission granted) |
| AC-08 | "Reminder time" label visible in every state | pass | measured-rendered: label shown with a value, with the value cleared (error state) and disabled |
| AC-09 | Field outline 3:1 with page | pass | measured-rendered: `.tf-box` `box-shadow: inset 0 0 0 1px rgb(112,122,110)` on #F3FCF2 = 4.26:1; dark #899487 on #0E150C = 5.88:1 (measure.js `nonTextContrast` item on `input#time` is a false positive: the boundary is drawn by the wrapper) |
| AC-10 | Three fieldsets with legends, 3/3/2 stacked radios | pass | measured-rendered: AX tree groups "Theme", "Text size", "Week starts on" with 3, 3 and 2 named radios |
| AC-11 | "Delete all data" label and dialog "Delete" in error | pass | measured-rendered: `rgb(192,0,19)` light, `rgb(255,180,165)` dark (disabled state: see F-07) |
| AC-12 | Dialog surface-container-high, 28 px, scrim #000 32% | pass | measured-rendered: `dialog` bg `rgb(226,234,225)` / `rgb(37,44,36)`, radius 28px, `::backdrop` `color(srgb 0 0 0 / 0.32)` |
| AC-13 | Two actions, trailing, Delete nearest edge | pass | measured-rendered at 390: Cancel then Delete, Delete right edge 48 px from window (24 margin + 24 padding), gap 8 px |
| AC-14 | Dialog 342 px at 390, 560 px at 1024 | pass | measured-rendered: 342 px and 560 px |
| AC-15 | Snackbar colors, 4 px corners, one at a time | pass | measured-rendered: bg `rgb(44,50,43)` / `rgb(220,229,219)`, text inverse-on-surface, radius 4px, height 48 px; 1 snackbar after three quick exports |
| AC-16 | Two or more cues for radio, switch, focused field | pass | measured-rendered: radio inner dot plus primary color; switch handle 16 to 24 px, x 8 to 24 px, outline to on-primary; field 3 px primary stroke plus primary label (grayscale emulation not run; cues are non-color by construction) |
| AC-17 | Reminder off: field at 38% and skipped by Tab | pass | measured-rendered: label/value `on-surface / 0.38`, outline `on-surface / 0.1`; `input#time` disabled; Tab from switch goes to the first theme radio |
| AC-18 | Cleared time shows "Enter a time" + icon, stored time kept | pass | measured-rendered: `.tf.invalid`, help "Enter a time" in `rgb(192,0,19)`, `.tf-err` displayed, `aria-invalid="true"`; stored and reloaded value 07:30 unchanged |
| AC-19 | Export over 200 ms busy text + named indicator; none under 200 ms | pass | measured-rendered: `?delay=1500` shows "Preparing your file…", `aria-busy="true"`, AX node progressbar "Exporting data"; `?delay=0` mutation observer saw no spinner and no busy text |
| AC-20 | Offline: status row at top, Delete disabled with TXT-26, Export works | pass | measured-rendered: `#offline` first in `main`, TXT-32 text, surface-container-high, 12 px corners; Delete disabled with "Connect to the internet to delete your data"; export downloaded `habits-2026-11-17.csv` offline |
| AC-21 | Dark sets `data-theme="dark"`, no light frame on reload | pass | measured-rendered: attribute `dark`, meta `#0E150C`; 18 screencast frames during reload under a light OS scheme all dark (mean luma 18-23 of 255) |
| AC-22 | System default follows OS scheme live, `theme-color` follows | pass | measured-simulation: emulated dark gives body `rgb(14,21,12)` and meta `#0E150C`; back to light gives `rgb(243,252,242)` and `#F3FCF2`, no reload |
| AC-23 | body-large 14 / 16 / 20 px for Small / Medium / Large | pass | measured-rendered: `#signout .lbl` 14px, 16px, 20px; app bar title stays 22px |
| AC-24 | Small: no content text under 12 px | pass | measured-rendered: smallest computed size 12px (tooltip, body-small floor) with the delete dialog open; measure.js `smallText` 0 at every width |
| AC-25 | 3 px secondary focus ring on every focusable element, both themes | fail | see F-01 |
| AC-26 | Dialog: focus on Cancel, Tab cycles inside, Escape returns to Delete row | pass | measured-rendered: focus `delCancel`; Tab/Shift+Tab alternate Cancel and Delete; Escape closes and focus is `#delete`; same for the sign-out dialog (`?unsynced=1`) |
| AC-27 | After deletion: focus on "Data", snackbar announced, both rows "No habit data yet" | pass | measured-rendered: focus `#dataHeading`; text "All habit data deleted" inserted into the `role="status"` `aria-live="polite"` region; both supporting texts TXT-25 (speech output not verified with a screen reader) |
| AC-28 | Snackbar polite, never focused, gone after 6 s | pass | measured-rendered: present at 5.6 s, removed by 6.4 s; `document.activeElement` stayed `#export` |
| AC-29 | Token text pairs 4.5:1, non-text 3:1, both themes | pass | measured-rendered: measure.js `contrastFailures` only lists the disabled time field (exempt, INT-07); brief pairs recomputed from the tokens: lowest 3.46:1 light / 3.88:1 dark (outline on surface-container-highest, non-text); the "after any regeneration" part can only be re-checked when the scheme changes |
| AC-30 | Every interactive element 48 x 48 px hit area at 390 | fail | see F-02 |
| AC-31 | Hit areas 8 px apart (dialog buttons), contiguous rows | pass | measured-rendered: dialog button gap 8 px, buttons 48 px tall; rows contiguous at 56/72 px |
| AC-32 | Accessible names contain visible labels; Back named "Back" | pass | measured-rendered: AX names "Back", "Sign out", switch "Daily reminder", "Reminder time", radios by label, "Export data", "Delete all data" (measure.js `labelInName` items for Export/Delete are false positives: the supporting text is the description) |
| AC-33 | Arrow keys move and select; one Tab stop per group | pass | measured-rendered: ArrowDown Medium to Large (selected), ArrowUp back; Tab leaves to the next group, Shift+Tab returns to the checked radio |
| AC-34 | All section-1 tasks keyboard-only | pass | measured-rendered: switch by Space and Enter, time typed (09:15 saved), radios by arrows, export, delete and sign out by Enter with dialogs closed by Escape (reaching Back needs Shift+Tab: see F-03) |
| AC-35 | One h1 "Settings", five h2 | pass | measured-rendered: heading outline h1 Settings; h2 Account, Reminders, Appearance, Calendar, Data |
| AC-36 | 390 px, browser 200% + Large: nothing clipped, overlapped or ellipsized | fail | see F-05 (dialog under zoom reflow: F-04). Also seen beyond the AC's setup, at 195 px reflow plus Large (about 250%): the time value is clipped by the native picker icon (the "M" of "08:00 PM" is cut off) |
| AC-37 | Reduced motion: no movement, snackbar fades, no spinner | pass | measured-simulation: body and dialog `animation-name: none`, switch and app bar transitions 0s, snackbar `fade-in`, `.spin` `display: none` with "Preparing your file…" shown |

Open questions still open in the brief: Q-01 (text-size multipliers), Q-02 (scope of "Delete all data").

## Findings

### F-01 Focus ring on Back and dialog buttons is drawn at 10% opacity
Area: Icon button and text buttons (shared `.icon-btn`, `.btn` focus style)   Tier: F   Kind: issue   Effort: S
Evidence (measured-rendered): `.icon-btn:focus-visible::before`, `.btn:focus-visible::before` - the 3 px secondary outline is set on the state-layer pseudo-element whose `opacity` is 0.1, so the ring renders at 10%; keyboard-focused screenshots contain 3 ring-colored pixels around `#back` and 0 around `#delCancel` (rows, switch and field: 2,500-3,100); `:focus-visible` matched; 5 occurrences: `#back`, `#delCancel`, `#delConfirm`, `#soCancel`, `#soConfirm`; both themes
Rule: A11-05 (foundations/interaction/states/applying-states@2025-08-05), also INT-12
Why it matters: keyboard users cannot see where focus is on the Back button and on every dialog action, including the destructive Delete.
Proposed change: draw the ring on a separate pseudo-element at full opacity: `.icon-btn:focus-visible::after, .btn:focus-visible::after { content: ""; position: absolute; inset: 4px; border-radius: var(--md-sys-shape-corner-full); outline: var(--app-focus-ring-width) solid var(--app-focus-ring-color); outline-offset: var(--app-focus-ring-offset); pointer-events: none; }` and remove `outline`/`outline-offset` from the `::before` rule (use `inset: 4px 0` for `.btn`, see F-08).
Decision: [ ] accept  [ ] reject  [ ] deviation   Note: ______

### F-02 Reminder time field hit area is 41 px tall
Area: Text field (Reminder time)   Tier: F   Kind: issue   Effort: S
Evidence (measured-rendered): `input#time` hit area 326 x 41 px (`hitAreaVia: probe`, `probe: ok`; input 24 px tall plus its 16 px label) inside the 56 px `.tf-box`; a tap 3 px inside the top or bottom edge of the field hits `.tf-box` and leaves focus on `body`; 1 occurrence, all widths, reminder on
Rule: A11-01 (foundations/designing/structure@2025-10-08), also TXF-01
Why it matters: on a phone, taps on the upper or lower part of the visible field do nothing, so users miss the control.
Proposed change: let the label and input fill the full container height: `.tf-box { padding-block: 0; } .tf-label { padding-top: 8px; } .tf-input { height: calc(var(--app-type-body-large-line-height) + 8px); padding-bottom: 8px; }` (visible layout unchanged; the label already focuses the input).
Decision: [ ] accept  [ ] reject  [ ] deviation   Note: ______

### F-03 First Tab skips the Back button
Area: App bar, initial focus   Tier: F   Kind: issue   Effort: S
Evidence (measured-rendered): on load focus is on `h1#title` (`$('title').focus()`); the first Tab lands on `#signout`; Back is reachable only with Shift+Tab, because Back precedes the h1 in DOM and visual order; 1 occurrence. The brief, section 6, asks for both "focus on h1" and "Tab then reaches Back", which cannot hold together with that order (A11-06).
Rule: APB-08 (components/app-bars/accessibility@2026-05-18), also A11-33, INT-30
Why it matters: keyboard and switch users opening Settings cannot get back with forward Tab; Back is the main exit of this secondary screen.
Proposed change: on screen open focus the first control instead of the title: replace `$('title').focus({ preventScroll: true })` with `$('back').focus({ preventScroll: true })` (A11-33 allows "first control"), keep `tabindex="-1"` on the h1, and update the brief's section 6 row "Screen opens" to "Focus after: Back".
Decision: [ ] accept  [ ] reject  [ ] deviation   Note: ______

### F-04 Dialog actions are cut off at 200% zoom
Area: Dialogs (`.dlg-actions`, shared by both dialogs)   Tier: F   Kind: issue   Effort: S
Evidence (measured-simulation): reflow at 195 px (390 px at 200% zoom), in-app Medium: dialog 147 px wide, Cancel starts at x = -16 px and shows as "ncel"; at 180 px (360 px at 200%): Cancel at x = -31 px and the body scrolls horizontally (scrollWidth 86 > clientWidth 84 for "permanently"); the action row never wraps; 2 dialogs (`#dlgDelete`, `#dlgSignout`). Decision B-11 accepts a dialog narrower than 280 dp at high zoom, but not lost content.
Rule: A11-08 (foundations/writing/text-resizing@2025-09-26), also WRT-04, DLG-02
Why it matters: at 200% zoom users cannot see or reliably tap "Cancel", the safe choice in a destructive confirmation.
Proposed change: `.dlg-actions { flex-wrap: wrap; } .dlg-head, .dlg-body { overflow-wrap: anywhere; }` (buttons stay trailing, Delete stays last).
Decision: [ ] accept  [ ] reject  [ ] deviation   Note: ______

### F-05 Avatar initials overflow the avatar and overlap the name at 200% text
Area: Account summary (`.avatar`)   Tier: F   Kind: issue   Effort: S
Evidence (measured-simulation): browser text 200% (root 32 px) with in-app Large at 360 and 390 px: initials 40 px font span 56 px (x 16-72) inside a fixed 40 x 40 px circle and run 4 px into the name and email column (x 68); with in-app Medium the initials still spill outside the circle (45 px wide); 1 occurrence. Fails AC-36.
Rule: A11-08 (foundations/writing/text-resizing@2025-09-26), also LST-03
Why it matters: at large text the initials collide with the account name and email, so the row reads as overlapped text.
Proposed change: let the avatar grow with its text while keeping 40 px at default size: `.avatar { width: max(40px, 2.5em); height: max(40px, 2.5em); }`.
Decision: [ ] accept  [ ] reject  [ ] deviation   Note: ______

### F-06 Back button has no hover or pressed state, and its tooltip appears only on focus
Area: Icon button (`.icon-btn`)   Tier: F   Kind: issue   Effort: S
Evidence (measured-rendered): mouse hover over `#back` (pointer context, `hover: hover`): `::before` opacity 0 and `.tip` opacity 0; no `.icon-btn:hover` or `.icon-btn:active` rule exists (only `.btn` has them); tooltip shows only under `:focus-visible`; 1 occurrence
Rule: TIP-04 (components/tooltips/accessibility@2026-01-30), also INT-03, INT-13
Why it matters: pointer users get no feedback or label on the only icon-only control, and touch users get no pressed feedback on Back.
Proposed change: `@media (hover: hover) { .icon-btn:hover::before { opacity: var(--app-state-hover); } .icon-btn:hover .tip { opacity: 1; } } .icon-btn:active::before { opacity: var(--app-state-pressed); }`
Decision: [ ] accept  [ ] reject  [ ] deviation   Note: ______

### F-07 Disabled "Delete all data" row keeps its error color
Area: List action rows (`.row.danger`)   Tier: C   Kind: issue   Effort: S
Evidence (measured-rendered): with the row disabled (offline, or after deletion with no data) `#delete .lbl` stays `rgb(192,0,19)` light / `rgb(255,180,165)` dark, while the disabled Export label correctly becomes `on-surface / 0.38`; cause: `.row.danger .lbl` has the same specificity as `.row:disabled .lbl` and comes later; 1 occurrence, 2 states
Rule: INT-06 (foundations/interaction/states/applying-states@2025-08-05), also BTN-05; brief section 5 (Delete row disabled "as action rows")
Why it matters: the row looks active and urgent but does nothing when tapped, so its state is unclear (inspired mode: harms usability).
Proposed change: after `.row.danger .lbl`, add `.row.danger:disabled .lbl { color: color-mix(in srgb, var(--md-sys-color-on-surface) calc(var(--app-disabled-content) * 100%), transparent); }`
Decision: [ ] accept  [ ] reject  [ ] deviation   Note: ______

### F-08 Dialog text buttons show a pill with 12 px side padding instead of 16 px
Area: Buttons (`.btn::before`)   Tier: C   Kind: suggestion   Effort: S
Evidence (measured-code): `.btn { padding: 0 16px }` with the state layer at `inset: 4px` on all sides, so the visible hover/focus/pressed pill (40 px tall, correct) is inset 4 px horizontally and leaves 12 px between label and pill edge; 4 buttons (`#delCancel`, `#delConfirm`, `#soCancel`, `#soConfirm`)
Rule: BTN-02 (components/buttons/specs@2026-05-18); brief section 4 "small, 16dp side padding"
Why it matters: the pressed and focused shapes look cramped next to the label and differ from the specified small button.
Proposed change: `.btn::before { inset: 4px 0; }` (keeps the 40 px visual height and the 48 px hit area).
Decision: [ ] accept  [ ] reject  [ ] deviation   Note: ______

### F-09 Dialog busy indicator stroke renders at 3.3 px
Area: Progress indicators (`.spin.sm`)   Tier: C   Kind: suggestion   Effort: S
Evidence (measured-code): `.spin.sm` is 20 x 20 px but keeps `stroke-width: 4` in a 24-unit viewBox, so the stroke renders at 3.33 px; 1 occurrence (Delete button while deleting)
Rule: PRG-02 (components/progress-indicators/specs@2026-02-27)
Why it matters: the two indicators on the screen look different in weight; minor visual inconsistency.
Proposed change: `.spin.sm circle { stroke-width: 4.8; }` (4 px at 20 px).
Decision: [ ] accept  [ ] reject  [ ] deviation   Note: ______

## Project and WCAG notes

No project or WCAG notes: every problem found maps to a rule ID above.

## Decision candidates

No decision candidates. The brief's decisions B-01..B-20 cover the project choices that depart from M3 (native time input, inline radio groups, error-colored destructive actions, no shadows, 24/20 dp indicators); 4 such items were suppressed (see header).

## Not covered

Not checked: RTL, OS-level text scaling on a real Android device (both 200% methods here are simulations), screen-reader speech (announcements inferred from live-region roles and the AX tree), row hover and pressed visuals beyond computed rules, the Back navigation result (`history.back()` target is out of scope), and the CSV content (out of scope). A device pass with TalkBack and system font at maximum would cover the first three.

## Next step

Mark each finding accept, reject or deviation (ranges are fine: "accept F-01..F-07"). Tier F items (F-01..F-06) can only be accepted or recorded as accepted risk. I will then record decisions (proposing `docs/design-decisions.md` for the ledger, since none exists) and give you the change list.
