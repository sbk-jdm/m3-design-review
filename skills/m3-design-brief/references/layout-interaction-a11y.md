# Layout, interaction, accessibility and writing rules

Snapshot date: 2026-05-21. Base URL: https://m3.material.io/
The `Source` column holds `path@lastmod`; `path` maps to `https://m3.material.io/<path>` (use the page's `source_url` when in doubt).
Units: dp as in the source; on the web 1dp is treated as 1 CSS px.
Distilled from Material Design 3 documentation (Apache 2.0 / CC BY 4.0); see NOTICE.md.

Tiers: F = floor (accessibility/usability minimum, never negotiable), C = core M3 (deviation needs an explicit decision), E = Expressive-only, optional or platform-specific.
ID prefixes: LAY- layout, INT- interaction, A11- accessibility structure/semantics, WRT- writing and text, CMP- cross-component.

## Accessibility floor

Apply these to any surface. A11-01..A11-15 repeat a rule defined elsewhere (cross-reference in the row); A11-29..A11-35 are defined here and point to related rules.
Where a row cites WCAG 2.2 or the WAI-ARIA Authoring Practices (APG), M3 does not state the rule in the pages covered.

| ID | Floor check | Criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| A11-01 | Touch target size | Every interactive element has a hit area of at least 48 x 48dp, even when the visible icon is smaller (see LAY-30) | F | foundations/designing/structure@2025-10-08 |
| A11-02 | Target spacing | Adjacent targets separated by 8dp or more | F | foundations/designing/structure@2025-10-08 |
| A11-03 | Text contrast | Essential text 4.5:1 (small) or 3:1 (large); essential non-text graphics 3:1. Disabled elements are exempt. Full color rules live in the color reference | F | foundations/writing/best-practices@2025-09-26 |
| A11-04 | Two visual state indicators | Each interactive state is signaled by more than one visual cue, not color alone (see INT-01) | F | foundations/interaction/states/overview@2025-08-05 |
| A11-05 | Visible keyboard focus | Every interactive element shows a ring-like focus indicator when reached by Tab (see INT-12) | F | foundations/interaction/states/applying-states@2025-08-05 |
| A11-06 | Logical focus order | Tab order follows reading order (DOM order, left to right, top to bottom) and matches the visual arrangement | F | foundations/designing/flow@2025-10-08 |
| A11-07 | Labels | Icon-only and ambiguous controls, meaningful images and status visuals carry an accessible label; decorative visuals are hidden from assistive tech (see A11-20..A11-24) | F | foundations/designing/elements@2025-10-08 |
| A11-08 | Text scaling | UI survives a text increase of at least 200% without clipping, overlap or lost content or function (see WRT-01..WRT-06) | F | foundations/writing/text-resizing@2025-09-26 |
| A11-09 | Truncation | Any ellipsis has a way to reveal the full text (tooltip or link) | F | foundations/writing/text-truncation@2025-09-26 |
| A11-10 | Keyboard operability | Primary and secondary journeys are completable with Tab, arrows, Enter and Escape alone | F | foundations/designing/flow@2025-10-08 |
| A11-11 | Dialog focus | Opening a dialog, modal pane or modal sheet moves focus into it; closing returns focus to the trigger (see LAY-27). Menus and popups: A11-34; view or page changes: A11-33 | F | foundations/designing/flow@2025-10-08 |
| A11-12 | Semantics | Use native controls and semantic HTML; interactive elements carry a role; headings do not skip levels | F | foundations/designing/overview@2025-10-08 |
| A11-13 | Density never shrinks targets | Default density keeps targets at 48 x 48 CSS px; denser modes are opt-in only (see LAY-28) | F | foundations/layout/grids-spacing/density@2026-05-15 |
| A11-14 | Single-key shortcuts | Any keyboard shortcut defaults to two or more keys; single-key shortcuts must be remappable or focus-scoped (see INT-25) | F | foundations/designing/flow@2025-10-08 |
| A11-15 | Motion reduction | With the reduced-motion setting on (`prefers-reduced-motion` on the web), subtle fades replace sliding and scaling; parallax and shape morph are disabled (repeats MOT-06) | F | styles/motion/transitions/applying-transitions@2025-09-26 |
| A11-29 | Color is never the only cue in data and status | Each chart series, segment, legend entry and status state is also told apart by a non-color cue (direct label, value, pattern, marker shape, icon or text). Parts needed to read the chart meet 3:1 against adjacent colors (COL-06). Charts carry a text summary or alt text (data type plus reason for the chart). See A11-04, INT-01 | F | WCAG 2.2 SC 1.4.1, WCAG 2.2 SC 1.4.11, foundations/content-design/alt-text@2025-09-26 |
| A11-30 | Minimum text size | Content text (body, values, captions, chart and axis labels) renders at 12 CSS px or more at default zoom; adapters may raise the threshold, not lower it. Text that M3 maps to the label-small token (badges, list overlines, trailing supporting text) is judged by TYP-01 instead. Heuristic: WCAG 2.2 sets no minimum size, and 12 px is the smallest common readable default for content text | F | heuristic |
| A11-31 | Accessible name contains the visible label | A control with visible text has an accessible name that contains that text (best starting with it), so voice users can say what they see; an aria-label with different words fails. M3 states the label of chips and segmented buttons is their visible text. Icon-only controls: A11-23 | F | WCAG 2.2 SC 2.5.3, components/chips/accessibility@2026-05-18, components/segmented-buttons/accessibility@2026-05-18 |
| A11-32 | Arrow keys in composite widgets | An element with a composite role (tablist, radiogroup, menu, menubar, listbox, toolbar, grid) moves focus between its items with the arrow keys (radios move and select), and Tab leaves the group; a roving tabindex or aria-activedescendant is the recommended web technique. Where M3 sets Tab per item (segmented buttons, navigation bar), Tab per item is not a violation, but arrows must still work if a composite role is claimed. Otherwise do not claim the role: use buttons with aria-pressed, or links with aria-current (see INT-29) | F | components/radio-button/accessibility@2026-02-16, components/tabs/accessibility@2026-05-18, components/chips/accessibility@2026-05-18, components/menus/accessibility@2026-05-18, WAI-ARIA APG Developing a Keyboard Interface (roving tabindex) |
| A11-33 | Focus after a view or page change | When the main view is replaced (route, navigation destination, full-screen sheet or detail view), focus goes to the new view's title, heading or first control if the activating control is gone; it may stay on the control if it remains on screen (tab, navigation item). Focus never falls to the document body or a removed element; back or close returns focus to the control that opened the view (see INT-30) | F | foundations/designing/flow@2025-10-08, WCAG 2.2 SC 2.4.3 |
| A11-34 | Menus, popups and modal surfaces manage focus | On open, focus moves inside (first item for menus, MNU-06); arrows move between menu items; Escape, outside tap and back close; Tab never moves focus behind a modal surface or into a closed popup. Escape or cancel returns focus to the trigger; after choosing an item, focus goes to the trigger or to the result of the action (M3 leaves this to the app), never to the body. Content behind a modal dialog, sheet or pane is inert (LAY-27) | F | components/menus/accessibility@2026-05-18, foundations/designing/flow@2025-10-08, foundations/layout/scaffold/panes@2026-05-19, WAI-ARIA APG Menu Button pattern, WAI-ARIA APG Dialog (Modal) pattern |
| A11-35 | Headings present | Each screen and major region marks its visible section titles as headings (or labelled landmarks), so screen-reader users can jump between blocks; a title styled like a heading but exposed as plain text fails. Hierarchy: A11-22 | F | foundations/designing/structure@2025-10-08, WCAG 2.2 SC 1.3.1 |

## Layout: breakpoints and window size classes

| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| LAY-01 | Use exactly five breakpoints (formerly window size classes) | Compact < 600dp; Medium 600-839dp; Expanded 840-1199dp; Large 1200-1599dp; Extra-large 1600dp and up | C | foundations/layout/breakpoints/overview@2026-05-19 |
| LAY-02 | Design for breakpoints, not for named devices | Window width changes with multi-window, unfolding and orientation; layout must respond to the live width | C | foundations/layout/breakpoints/overview@2026-05-19 |
| LAY-03 | Recommended pane count per breakpoint | Compact 1; Medium 1 (2 allowed for low-density content); Expanded 2 (1 allowed); Large 2 (1 allowed); Extra-large 2 (1 or 3 allowed) | C | foundations/layout/scaffold/panes@2026-05-19 |
| LAY-04 | Never more than three panes | Third pane only at extra-large, as a standard side sheet | C | foundations/layout/breakpoints/large-extra-large@2026-05-19 |
| LAY-05 | Medium two-pane only for low-density content | Not for high information density (for example a settings list with quick switches is fine, dense data is not) | C | foundations/layout/breakpoints/overview@2026-05-19 |
| LAY-06 | Single pane reserved for immersive or dense content at Expanded and up | Video, games, calls, creative tools; otherwise use two panes | C | foundations/layout/breakpoints/expanded@2026-05-19 |
| LAY-07 | Line length across all breakpoints | Adjust margins and type so body text stays 40-60 characters per line | C | foundations/layout/breakpoints/overview@2026-05-19 |
| LAY-08 | Navigation component by breakpoint | Compact: navigation bar or modal expanded rail; Medium: navigation rail (single pane) or navigation bar (two panes); Expanded/Large/Extra-large: navigation rail, collapsed or expanded | C | foundations/layout/breakpoints/overview@2026-05-19, foundations/layout/breakpoints/medium@2026-05-19 |
| LAY-09 | Expanded navigation rail suits Extra-large | Collapse it when space is needed or on deep pages | C | foundations/layout/breakpoints/large-extra-large@2026-05-19 |
| LAY-10 | Supplemental selection and dialogs by breakpoint | Compact: bottom sheet, simple or full-screen dialog; Medium and up: menu and simple dialog | C | foundations/layout/breakpoints/overview@2026-05-19 |
| LAY-11 | Only swap functionally equivalent components | Navigation bar to rail is fine; button to chip or button to menu is not | C | foundations/layout/breakpoints/overview@2026-05-19 |
| LAY-12 | Layout transitions dynamically | Compact/Medium/Expanded layouts must reflow on rotate, unfold, split-screen and free-form resize without a reload | C | foundations/layout/breakpoints/compact@2026-05-19 |
| LAY-13 | Reachability | Keep essential actions out of the top 25% of large handheld screens and away from the bottom edge; compact navigation sits near the bottom | C | foundations/layout/breakpoints/medium@2026-05-19 |
| LAY-14 | Height breakpoints are optional | Compact/medium/expanded height classes exist on Android; rarely needed because content scrolls vertically | E | foundations/layout/breakpoints/overview@2026-05-19 |
| LAY-15 | Large and extra-large are optional on some products | Use only when platform and users call for desktop layouts | E | foundations/layout/breakpoints/large-extra-large@2026-05-19 |

## Layout: margins, spacers, panes

| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| LAY-16 | Window margins | Compact 16dp each side; Medium, Expanded, Large and Extra-large 24dp each side | C | foundations/layout/breakpoints/compact@2026-05-19 |
| LAY-17 | Spacer between panes | 24dp at Medium, Expanded, Large and Extra-large | C | foundations/layout/breakpoints/medium@2026-05-19 |
| LAY-18 | Medium two-pane widths | Each pane 50% of window width by default; no custom widths; drag handle may expand a pane to 100% | C | foundations/layout/breakpoints/medium@2026-05-19 |
| LAY-19 | Fixed pane width | Expanded 360dp by default; Large and Extra-large 412dp by default | C | foundations/layout/breakpoints/expanded@2026-05-19 |
| LAY-20 | Side sheet as third pane | Maximum default width 400dp; fixed panes there stay 412dp | C | foundations/layout/breakpoints/large-extra-large@2026-05-19 |
| LAY-21 | Every layout has at least one flexible pane | Panes are fixed or flexible; all content sits inside a pane | C | foundations/layout/scaffold/panes@2026-05-19 |
| LAY-22 | Split-pane layout | Spacer visually centered; with a rail or drawer only one pane shrinks, the other stays 50% of window; with a navigation bar or no nav both are 50% | C | foundations/layout/scaffold/panes@2026-05-19 |
| LAY-23 | Resizing snap widths | Recommended custom snap widths: 360dp, 412dp, and centered split | C | foundations/layout/scaffold/panes@2026-05-19 |
| LAY-24 | Drag handle behavior | Resizes flexible panes or collapses/expands the fixed pane; selecting it toggles layout size (tap, double tap or long press) | C | foundations/layout/scaffold/panes@2026-05-19 |
| LAY-25 | Pane presentation | Persistent tools are co-planar with primary content; temporary tasks (dialogs) stay floating at every breakpoint; docked panes pin to a window edge | C | foundations/layout/scaffold/panes@2026-05-19 |
| LAY-26 | Pane adaptation strategies | Show/hide, levitate, or reflow (for example supporting pane moves under the primary pane in portrait) | C | foundations/layout/scaffold/panes@2026-05-19 |
| LAY-27 | Pane focus handling | Co-planar panes: focus order matches visual arrangement. Modal floating pane: background inert, focus moves in and returns to trigger. Non-modal: focus can enter and leave | F | foundations/layout/scaffold/panes@2026-05-19 |

## Layout: density, spacing, scaffold

| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| LAY-28 | Default target size | At least 48 x 48 CSS px by default; do not apply component density scaling by default if it drops below this | F | foundations/layout/grids-spacing/density@2026-05-15 |
| LAY-29 | Dense layouts are opt-in | Density must not change automatically across breakpoints or orientation; the control to revert density must itself use 48 x 48 targets | C | foundations/layout/grids-spacing/density@2026-05-15 |
| LAY-30 | Visual element may be smaller than target | Icon can be smaller visually if the interactive area keeps 48 x 48dp | F | foundations/layout/grids-spacing/density@2026-05-15 |
| LAY-31 | Component density scale | 0 is default, then -1, -2, -3; each step usually trims top/bottom padding or height by 4dp; content stays centered; text size does not change | C | foundations/layout/grids-spacing/density@2026-05-15 |
| LAY-32 | State layer vs target | State layer is 40dp while the interactive target is 48dp | C | foundations/interaction/states/state-layers@2025-08-05 |
| LAY-33 | Spacing groups content | Related items sit close (proximity); explicit grouping uses outlines/dividers/shadows, implicit grouping uses space; buttons sit near the content they affect | C | foundations/layout/grids-spacing/spacing@2026-05-15 |
| LAY-34 | Consistent rhythm and alignment | Similar elements share spacing and size; leading thumbnails, avatars and icons are aligned | C | foundations/layout/grids-spacing/spacing@2026-05-15 |
| LAY-35 | Scaffold order | Place bars and rails nearest the screen edges first, then panes in the main region | C | foundations/layout/grids-spacing/grids@2026-05-15 |
| LAY-36 | App bar content | Top app bar carries a title and 1-2 essential actions (for example search or back) | C | foundations/layout/scaffold/bars@2026-05-19 |
| LAY-37 | Navigation bar destinations | 3-5 primary views, at compact or medium breakpoints | C | foundations/layout/scaffold/bars@2026-05-19 |
| LAY-38 | Safety region | No primary content under system UI (status bar, gesture bar) | C | foundations/layout/scaffold/bars@2026-05-19 |
| LAY-39 | Rail regions | Compact: top/bottom rail regions hold toolbars, chat inputs, FABs. Larger: leading rail holds navigation rail; trailing rail holds supporting controls for pane content | C | foundations/layout/scaffold/rails@2026-05-19 |

## Layout: canonical layouts and adaptation

| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| LAY-40 | Start from a canonical layout | Feed, list-detail, or supporting pane | C | foundations/layout/canonical-examples/overview@2026-05-19 |
| LAY-41 | Feed | Compact: single stacked column filling pane width; Medium and up: multiple columns, count usually increases at Expanded; items reflow on rotate, unfold or resize | C | foundations/layout/canonical-examples/feed@2026-05-19 |
| LAY-42 | List-detail panes | Compact: 1 pane, list or detail one at a time; Medium: 1 (recommended) or 2; Expanded and up: 2 | C | foundations/layout/canonical-examples/list-detail@2026-05-19 |
| LAY-43 | List-detail behavior | Back button only in detail view of single-pane; selected state shown in list only in two-pane; empty detail pane shows placeholder; read/unread state persists | C | foundations/layout/canonical-examples/list-detail@2026-05-19 |
| LAY-44 | Supporting pane | Use only when secondary content depends on primary; below the focus pane at Compact/Medium (flexible width), leading or trailing at Expanded (fixed 360dp); parent-child data uses list-detail instead | C | foundations/layout/canonical-examples/supporting-pane@2026-05-19 |
| LAY-45 | Bottom sheet for supporting content | At compact, a bottom sheet can keep focus on the primary pane | C | foundations/layout/canonical-examples/supporting-pane@2026-05-19 |
| LAY-46 | Adapt components, not only layout | Resize (hug or scale), show/hide detail, or change presentation (FAB to extended FAB, collapsed to expanded rail) as space grows | C | foundations/layout/layout-overview/adaptive-design@2026-05-19 |
| LAY-47 | Support all input types at every size | Touch, pointer and physical keyboard must all work, even on a phone | C | foundations/layout/layout-overview/adaptive-design@2026-05-19 |
| LAY-48 | Primary task emphasis | One primary task per page, largest element is the main CTA, secondary goals discoverable but quieter | C | foundations/usability/overview@2026-01-22 |
| LAY-49 | Limit expressive tactics | Do not stack many emphasis tactics at once; motion is used sparingly | C | foundations/usability/overview@2026-01-22 |

## Layout: bidirectionality (RTL)

| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| LAY-50 | Use leading/trailing, not left/right | Layouts must mirror in RTL: nav rail on the right, reading starts top right, text right-aligned | C | foundations/layout/bidirectionality-rtl@2026-05-19 |
| LAY-51 | Mirror directional icons | Back/forward arrows mirror; clocks, circular refresh and clockwise progress arrows do not | C | foundations/layout/bidirectionality-rtl@2026-05-19 |
| LAY-52 | Do not mirror everything | Charts and graphs stay LTR for Persian and Urdu; media controls are always LTR; Hebrew timelines stay LTR | C | foundations/layout/bidirectionality-rtl@2026-05-19 |
| LAY-53 | Linear progress in RTL | Moves right to left (except Hebrew, which stays LTR); circular progress unchanged | C | foundations/layout/bidirectionality-rtl@2026-05-19 |
| LAY-54 | Mirror toolbars, app bars and badges | Reverse tool order, app bar layout and badge position/alignment | C | foundations/layout/bidirectionality-rtl@2026-05-19 |
| LAY-55 | Text field and chip icons | Leading and trailing icons swap sides; chip trailing icon sits at the end edge (left in RTL) | C | foundations/layout/bidirectionality-rtl@2026-05-19 |
| LAY-56 | Mirror swipe gestures | A swipe-to-reveal from the right in LTR reveals from the left in RTL; predictive back mirrors too | C | foundations/layout/bidirectionality-rtl@2026-05-19 |
| LAY-57 | Clock AM/PM placement in RTL | Time still runs clockwise; AM/PM marker goes to the left | E | foundations/layout/bidirectionality-rtl@2026-05-19 |
| LAY-58 | RTL text rendering | Check text entry, cursor position, punctuation, phone numbers and URLs | C | foundations/layout/bidirectionality-rtl@2026-05-19 |

## Interaction: states and state layers

| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| INT-01 | Two visual indicators per state | Each state is shown with at least two visual cues; states can combine (for example selected plus hover) | F | foundations/interaction/states/overview@2025-08-05 |
| INT-02 | State set | Enabled, disabled, hover, focused, pressed, dragged (plus selected/activated) must exist for interactive components | C | foundations/interaction/states/overview@2025-08-05 |
| INT-03 | State layer opacities | Hover 8%; Focus 10%; Press 10%; Drag 16% | C | foundations/interaction/states/state-layers@2025-08-05 |
| INT-04 | State layer color | Overlay uses the content (on-) color of the component, for example on-secondary-container over a secondary-container fill, primary over a surface fill | C | foundations/interaction/states/state-layers@2025-08-05 |
| INT-05 | One state layer at a time | Only one state layer is applied at a given time; it can cover the whole element or a circle | C | foundations/interaction/states/state-layers@2025-08-05 |
| INT-06 | Disabled behavior | Not focusable, draggable or pressable; no change on hover or tap; shown through color change and reduced elevation | C | foundations/interaction/states/applying-states@2025-08-05 |
| INT-07 | Disabled contrast exemption | Disabled elements need not meet contrast requirements | C | foundations/interaction/states/applying-states@2025-08-05 |
| INT-08 | Disabled inheritance | Buttons, cards, checkboxes, chips, list items, radios, switches, text fields have disabled states; app bars, badges, dialogs, FABs, menus, nav bar/drawer/rail, sheets, tabs, tooltips do not | C | foundations/interaction/states/applying-states@2025-08-05 |
| INT-09 | Hover behavior | Pause-over with a cursor; lower-emphasis overlay; combinable with focus, selected, pressed; only one hover at a time | C | foundations/interaction/states/applying-states@2025-08-05 |
| INT-10 | Hover inheritance | Buttons, cards, checkbox, chips, pickers, list items, slider, switch, text fields; not app bars, badges, dialogs, menus, nav components, sheets, tabs | C | foundations/interaction/states/applying-states@2025-08-05 |
| INT-11 | Focus applies to all interactive components | Higher-emphasis overlay than hover; one focus at a time; combinable with hover, activated, selected | C | foundations/interaction/states/applying-states@2025-08-05 |
| INT-12 | Keyboard focus indicator | Tabbing to an element shows a ring-like indicator in addition to the state layer | F | foundations/interaction/states/applying-states@2025-08-05 |
| INT-13 | Pressed state | High emphasis; ripple overlay; buttons and cards may also gain elevation; one pressed at a time. Applies to every actionable element; inside the containers of INT-14 it shows on the actionable item, not the container | C | foundations/interaction/states/applying-states@2025-08-05 |
| INT-14 | Pressed not inherited by containers | App bars, badges, bottom navigation, dialogs, menus, sheets and tabs show no pressed state as a whole; their actionable items (app bar action, navigation item, tab) do (INT-13) | C | foundations/interaction/states/applying-states@2025-08-05 |
| INT-15 | Dragged state | Low emphasis so it does not distract; list items, chips, cards may gain elevation; started by touch-and-hold; one at a time | C | foundations/interaction/states/applying-states@2025-08-05 |
| INT-16 | Dragged inheritance | Cards, chips, list items, sliders only; not buttons, app bars, badges, dialogs, menus, nav components | C | foundations/interaction/states/applying-states@2025-08-05 |

## Interaction: selection, gestures, inputs

| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| INT-17 | Selection indicator | Shown by a check mark, a checkbox, a surface color change, or a combination; never a change that is invisible | C | foundations/interaction/selection@2025-09-26 |
| INT-18 | Single active indicator for navigation | Navigation bar, drawer, rail and tabs show one active indicator; exactly one item selected at a time | C | foundations/interaction/selection@2025-09-26 |
| INT-19 | Touch selection mode | Enter by long press or a shortcut (for example tapping an avatar); then tap to add items; exit by deselecting all or tapping a toolbar action | C | foundations/interaction/selection@2025-09-26 |
| INT-20 | Desktop selection | Checkboxes always visible when selection is primary; when secondary, show a checkbox on hover for one item, and for all items once one is selected | C | foundations/interaction/selection@2025-09-26 |
| INT-21 | Long-press drag select | Do not use long-press-and-drag multi-select where it already means pick up and move | C | foundations/interaction/selection@2025-09-26 |
| INT-22 | Gestures respond in real time | Tap, double tap (zoom), long press (extra actions), scroll/pan, swipe (switch peer views or complete actions), drag, pick up and move (reorder), pinch | C | foundations/interaction/gestures@2026-01-09 |
| INT-23 | Predictive back (Android) | Supported by bottom sheet, navigation bar, navigation rail, search bar, side sheet; user can abort mid-swipe | E | foundations/interaction/gestures@2026-01-09 |
| INT-24 | Mouse and pointer behavior | Show a cursor; primary click gives the same feedback as touch (ripple); secondary click opens a context menu; hover changes state and may show tooltips | C | foundations/interaction/inputs@2025-09-26 |
| INT-25 | Cursor shapes | Pointer by default; hand on links; resize arrows on resizable edges; I-beam over text | C | foundations/interaction/inputs@2025-09-26 |
| INT-26 | Text selection with pointer | Single-color highlight, no touch handles when using mouse or stylus; touch always shows touch controls | C | foundations/interaction/inputs@2025-09-26 |
| INT-27 | Scrolling with pointer | Wheel and two-finger trackpad scroll vertically and horizontally; dragging in text selects rather than scrolls | C | foundations/interaction/inputs@2025-09-26 |
| INT-28 | Keyboard conventions | Enter activates/sends; Space plays or pauses media; Escape dismisses, removes focus or clears selection; physical keyboard hides the virtual one | C | foundations/interaction/inputs@2025-09-26 |
| INT-29 | Tab focus order | Logical order, left to right and top to bottom; Shift+Tab reverses; arrows move inside components | F | foundations/interaction/inputs@2025-09-26 |
| INT-30 | Initial focus defined | Define initial focus per screen and per multi-control component (dialog, complex card) | C | foundations/designing/flow@2025-10-08 |
| INT-31 | Keyboard shortcuts | Default to two or more keys; document all custom shortcuts; single-key shortcuts need remap, focus-scoped activation, or off switch (in that preference order) | F | foundations/designing/flow@2025-10-08 |

## Accessibility: structure, targets, labels

| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| A11-16 | Touch target minimum | At least 48 x 48dp (about 9mm; recommended physical range 7-10mm); iOS recommends 44 x 44dp | F | foundations/designing/structure@2025-10-08 |
| A11-17 | Pointer target minimum | At least 44 x 44dp for mouse and stylus targets | F | foundations/designing/structure@2025-10-08 |
| A11-18 | Target spacing | 8dp or more between targets in most cases | F | foundations/designing/structure@2025-10-08 |
| A11-19 | Source order equals reading order | Screen readers follow HTML order, not CSS visual order; DOM order must match the intended reading sequence | F | foundations/designing/structure@2025-10-08 |
| A11-20 | Landmarks (web) | Use navigation, search, main, banner, complementary, contentinfo, region, form; exactly one main, one banner, one contentinfo | C | foundations/designing/structure@2025-10-08 |
| A11-21 | Landmark labels | Label every region and every repeated landmark (for example two navs); do not repeat the role word inside the label | C | foundations/designing/structure@2025-10-08 |
| A11-22 | Heading hierarchy | Headings follow content hierarchy, not visual style, sequential H1-H6 with no skipped level (the floor check). M3 recommends a single H1 for the page title: report a missing or repeated H1 as a suggestion, not a floor issue. Presence of headings: A11-35 | F | foundations/designing/structure@2025-10-08 |
| A11-23 | Elements needing labels | Icon-only buttons, interactive images, progress and error cues, status icons, meaningful images; also generic link text ("Learn more") and repeated generic buttons ("Save") | F | foundations/designing/elements@2025-10-08 |
| A11-24 | Labels exclude the role | Do not put "button" or "menu" in the label; do not label non-interactive text or buttons whose text is already descriptive | C | foundations/designing/elements@2025-10-08 |
| A11-25 | Decorative visuals hidden | Mark decorative icons and images as decorative so assistive tech skips them | F | foundations/designing/elements@2025-10-08 |
| A11-26 | Roles on interactive elements | Assign ARIA roles (web) or component type (mobile); prefer native controls and semantic HTML | F | foundations/designing/elements@2025-10-08 |
| A11-27 | Alt text | Short label, up to 125 characters, no "image of"; essential text embedded in an image must be repeated in alt text or adjacent text | F | foundations/writing/best-practices@2025-09-26 |
| A11-28 | Design for assistive tech | Keyboard/D-pad, screen readers (TalkBack, VoiceOver, JAWS), switch input and voice input must reach all functions | F | foundations/overview/assistive-technology@2025-09-26 |

## Cross-component rules

| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| CMP-01 | Classify a control by its function, not its look | Decide what the control does, then apply that component's rules and report once under them. A single-select chip row that switches views or sorts (2-5 options) works as a segmented button (connected button group in Expressive): selection cue SEG-05 and outline contrast SEG-04 apply, while chip geometry (CHP-01..CHP-03) still applies to shape and size. A chip row that filters a collection stays a filter chip set (M3 offers single-select filter chips as an alternative to segmented buttons), so CHP-05 and COL-23 apply. A row that swaps content panels is tabs (TAB-*, A11-32) | C | components/chips/guidelines@2026-05-18, components/segmented-buttons/guidelines@2026-05-18 |

## Writing and text

| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| WRT-01 | Text scaling support | Support at least 200% text increase (OS setting or in-app 1.5x/2x multipliers) | F | foundations/writing/text-resizing@2025-09-26 |
| WRT-02 | Scaling behavior | Text and line height scale by the multiplier; padding and inter-element spacing stay at 1x | C | foundations/writing/text-resizing@2025-09-26 |
| WRT-03 | Non-text components unaffected | Progress indicators, checkboxes, radio buttons do not scale with text | C | foundations/writing/text-resizing@2025-09-26 |
| WRT-04 | Large-type strategies | Grow containers, reflow (stack instead of side by side), allow one-direction scroll (vertical preferred, never both axes) | F | foundations/writing/text-resizing@2025-09-26 |
| WRT-05 | Tight bars use tooltips | Top app bar, nav bar, nav rail and fixed tabs keep 1x text and show enlarged label in a touch-and-hold tooltip | C | foundations/writing/text-resizing@2025-09-26 |
| WRT-06 | No content loss | Larger type, spacing or longer translations must not lose content, understanding or function | F | foundations/writing/text-truncation@2025-09-26 |
| WRT-07 | Wrap when critical | Wrap text when it is essential to understanding or when the component has room; components may grow in height or width | C | foundations/writing/text-truncation@2025-09-26 |
| WRT-08 | Ellipsis needs a reveal path | Truncated text is acceptable only if full text is available via tooltip or link; an ellipsis with no way to see the rest is inaccessible | F | foundations/writing/text-truncation@2025-09-26 |
| WRT-09 | Text contrast for essential content | 4.5:1 small text, 3:1 large text | F | foundations/writing/best-practices@2025-09-26 |
| WRT-10 | Captions and adjacent text | Provide caption or nearby text conveying key image information | C | foundations/writing/best-practices@2025-09-26 |

## Review checks

- Resize the viewport through 599, 600, 839, 840, 1199, 1200 and 1600px: pane count, nav component, margins (16 or 24) and spacers (24) change at the right widths.
- Measure computed target size of every button, icon button, chip and list row: 48 x 48 minimum, 8px gap.
- Tab through the page: ring visible on each stop, order matches visual order, dialogs, sheets and menus contain and return focus (A11-34), arrows work in composite widgets (A11-32).
- Set text to 200%: nothing clipped, overlapped or hidden; check ellipses have a title/tooltip.
- Switch to dir=rtl: nav rail on the right, directional icons flipped, charts and media controls not flipped.
- Inspect hover/focus/press overlays against 8/10/10% and confirm a second cue beyond color.
