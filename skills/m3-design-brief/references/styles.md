# Material 3 styles: typography, shape, elevation, spacing, motion, icons

- Snapshot date: 2026-05-21. Base URL: https://m3.material.io/
- `Source` paths map to `https://m3.material.io/<path>` (use the page's `source_url` when in doubt).
- Distilled from Material Design 3 documentation (Apache 2.0 / CC BY 4.0); see NOTICE.md.
- Units: dp as in the source. On the web, treat 1dp as 1 CSS px.
- Tiers: F = floor (never negotiable), C = core M3 (deviation needs an explicit decision), E = Expressive-only, optional or platform-specific.

## Typography

Use: pick styles from the M3 scale by role; do not invent ad hoc sizes.

Type scale structure (the doc's numeric token table is an image and is not reproduced here; read sizes, line heights, weights and tracking from the `md.sys.typescale.<role>-<size>.*` tokens of the product, or from the page):

| Role | Sizes | Intended use |
| --- | --- | --- |
| Display | large, medium, small | Short, important text or numerals; large screens |
| Headline | large, medium, small | Short high-emphasis text; small screens; dialog titles |
| Title | large, medium, small | Medium emphasis, short text; app bar titles, section headers |
| Body | large, medium, small | Long passages and reading text |
| Label | large, medium, small | Text inside components, captions, timecodes; buttons use label-large |

Facts: 5 roles x 3 sizes = 15 baseline styles plus 15 emphasized styles (30 total). Base size is 14 on a Major Second ratio (1.125). Token properties per style: font, size, line-height, tracking, weight (`md.sys.typescale.<role>-<size>.<prop>`). Emphasized token form: `md.sys.typescale.emphasized.<role>-<size>`. Web font size unit is rem (px / 16, e.g. 12sp = 0.75rem, 24sp = 1.5rem, 60sp = 3.75rem). Letter spacing = tracking / font size (0.2 / 16 = 0.0125 em).

Fonts: default Roboto (Android and M3 scale). Roboto Flex, Roboto Serif, Roboto Mono and Noto Sans are the documented companions. Fallback order for Roboto Flex: Roboto, then Noto Sans collection. Roboto Mono suits code and aligned numbers. Brand typeface for large styles (display, headline), plain typeface for small styles (body, label).

Color of text: default on-surface, alternative on-surface-variant, links primary (or tertiary for quieter links) and underlined.

| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| TYP-01 | Text uses the five roles (display, headline, title, body, label), each in large/medium/small | Every text element maps to one role+size; no one-off sizes outside the scale. Minimum size for content text: A11-30 | C | styles/typography/applying-type@2026-05-06 |
| TYP-02 | Normal text contrast | >= 4.5:1 for small text | F | styles/typography/applying-type@2026-05-06 |
| TYP-03 | Large text contrast | >= 3:1 for large text | F | styles/typography/applying-type@2026-05-06 |
| TYP-04 | Line-height ratio for display, headline, title | About 1.2 x font size | C | styles/typography/applying-type@2026-05-06 |
| TYP-05 | Line-height ratio for body and label | About 1.5 x font size; neither cramped nor loose | C | styles/typography/applying-type@2026-05-06 |
| TYP-06 | Body text uses a readable typeface | No expressive, decorative, handwritten or script fonts for body text | C | styles/typography/applying-type@2026-05-06 |
| TYP-07 | Titles avoid expressive fonts | Use caution with display/handwritten/script faces in title styles | C | styles/typography/applying-type@2026-05-06 |
| TYP-08 | Expressive fonts confined to display and headline | Headline expressive fonts also need adjusted line height and letter spacing | E | styles/typography/applying-type@2026-05-06 |
| TYP-09 | Default text color is on-surface (or on-surface-variant) | Not arbitrary grays or pure black/white on tonal surfaces | C | styles/typography/applying-type@2026-05-06 |
| TYP-10 | Hyperlinks are underlined and colored primary (or tertiary) | Underline present; color alone is not the cue | F | styles/typography/applying-type@2026-05-06 |
| TYP-11 | Changing type size is avoided when customizing | Adjust line height, tracking, family instead; size changes break component reflow | C | styles/typography/type-scale-tokens@2026-05-06 |
| TYP-12 | Tabular figures for tables and changing values | Monospaced digits for clocks, tables, counters to avoid layout shift | C | styles/typography/applying-type@2026-05-06 |
| TYP-13 | Font sizes in web code are rem-based | px / 16 = rem; respects user text scaling | C | styles/typography/type-scale-tokens@2026-05-06 |
| TYP-14 | Emphasized styles are used selectively | For selected states, primary actions, unread items, badges, headlines; components do not use them by default | C | styles/typography/type-scale-tokens@2026-05-06 |
| TYP-15 | Emphasized styles pair with text that already carries weight | Swap the baseline token for the emphasized token of the same role/size | E | styles/typography/type-scale-tokens@2026-05-06 |
| TYP-16 | Font fallback chain defined | Variable font first, then Roboto, then Noto Sans | C | styles/typography/fonts@2026-05-06 |
| TYP-17 | Editorial treatments are not used for labels or plain information | Reserve for showcase moments; keep similar moments consistent; do not mix clashing styles in one layout | E | styles/typography/editorial-treatments@2026-05-06 |
| TYP-18 | Spacing survives text scaling | At 200% text scale the same spacing is preserved | F | styles/spacing/applying-spacing@2026-05-18 |

## Shape

Use: corners come from the 10-step radius scale; button-like components default to Full.

| Step | Value |
| --- | --- |
| None | 0dp |
| Extra small | 4dp |
| Small | 8dp |
| Medium | 12dp |
| Large | 16dp |
| Large increased | 20dp |
| Extra large | 28dp |
| Extra large increased | 32dp |
| Extra extra large | 48dp |
| Full | fully rounded |

Large increased, extra large increased and extra extra large arrived with M3 Expressive (M3 base scale: none through extra large and full). Asymmetric shapes use the same scale; inner corners appear in closely grouped items (menus, split buttons). Shape library has 35 shapes; shape morph is Compose-only (web not available).

| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| SHP-01 | Corner radii come from the scale | Values from {0, 4, 8, 12, 16, 20, 28, 32, 48, full}; hardcoded in-between radii need a reason | C | styles/shape/corner-radius-scale@2026-05-06 |
| SHP-02 | Similar components share the same corner style | A component maps to one scale step product-wide (e.g. all buttons Full) | C | styles/shape/corner-radius-scale@2026-05-06 |
| SHP-03 | Full means fully rounded | Use `full`/pill radius, not 50% of the component size, as the Expressive token | E | styles/shape/overview-principles@2026-05-06 |
| SHP-04 | Nested rounded shapes use optical roundness | Inner radius = outer radius - padding (e.g. 48 - 14 = 34dp); not identical radii | C | styles/shape/corner-radius-scale@2026-05-06 |
| SHP-05 | Cut corners get extra padding | Large cut corners clip content more than rounded ones of the same size | C | styles/shape/corner-radius-scale@2026-05-06 |
| SHP-06 | Library/abstract shapes are for visual elements | Not text-heavy containers; use sparingly and with a reason | C | styles/shape/corner-radius-scale@2026-05-06 |
| SHP-07 | Shape is not semantic | Do not give one shape a fixed literal meaning; avoid shapes added without purpose | E | styles/shape/overview-principles@2026-05-06 |
| SHP-08 | Shape morph is used for state/progress feedback only | Selected state, in-progress, environment change; standard button group and loading indicator use it | E | styles/shape/shape-morph@2026-05-06 |
| SHP-09 | Shape and type are used in harmony | Roundness of shapes should echo the typeface character | E | styles/shape/overview-principles@2026-05-06 |

## Elevation

Use: elevation is a z-axis distance; M3 shows it with tonal surface color by default, shadows only when needed.

| Level | dp | Resting components (examples) |
| --- | --- | --- |
| 0 | 0dp | Filled/tonal/outlined buttons, filled/outlined cards, chips, icon buttons, lists, nav rail, tabs, sliders, app bar (not scrolled), docked side sheet |
| 1 | 1dp | Elevated button/card/chip, banner, modal bottom sheet, modal nav drawer, modal side sheet |
| 2 | 3dp | Scrolled app bar, menu, navigation bar, rich tooltip, toolbar |
| 3 | 6dp | FAB, extended FAB, modal dialog, search, date and time pickers |
| 4 | 8dp | Not a resting level; hover/drag |
| 5 | 12dp | Not a resting level; hover/drag |

Resting state uses levels 0 to 3; levels 4 and 5 are for interaction states (hover, dragged). Hover or focus usually raises one level (FAB 3 to 4). Surface tint color is deprecated; use level tokens 0 to 5. Tokens carry no shadow or color; each platform decides. Scrims use the scrim color role at 32% opacity.

| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| ELV-01 | Few elevation levels in a UI | Stick to a small set; shadow levels used sparingly | C | styles/elevation/overview@2026-02-11 |
| ELV-02 | Default resting elevation is kept | Do not raise components above their level in the table (e.g. no shadows on level-0 buttons/cards at rest) | C | styles/elevation/overview@2026-02-11 |
| ELV-03 | Resting levels only 0 to 3 | Levels 4 and 5 appear only on hover, focus, drag | C | styles/elevation/applying-elevation@2026-02-11 |
| ELV-04 | Interaction raises elevation by one level, consistently | All buttons +1 on hover; similar elements behave alike | C | styles/elevation/overview@2026-02-11 |
| ELV-05 | Separation is tonal by default | Overlapping containment areas use different surface/surface-container roles, not shadow on everything | C | styles/elevation/applying-elevation@2026-02-11 |
| ELV-06 | Shadows only to protect or encourage interaction | Use on busy/patterned backgrounds or for lift on focus, selection, swipe | C | styles/elevation/applying-elevation@2026-02-11 |
| ELV-07 | Larger distance = larger, softer shadow | Small sharp shadow means close; big diffuse means far | C | styles/elevation/applying-elevation@2026-02-11 |
| ELV-08 | Interactive surface edges have sufficient contrast | Floating elements stay distinguishable from the surface beneath (meets accessible contrast) | F | styles/elevation/applying-elevation@2026-02-11 |
| ELV-09 | Modals and expanded nav use a scrim | Scrim color role at 32% opacity | C | styles/elevation/applying-elevation@2026-02-11 |
| ELV-10 | Elevation-tint overlays are not used | Surface tint is deprecated; use elevation level tokens and surface container roles | C | styles/elevation/tokens@2026-02-11 |

## Spacing

Use: 8dp linear scale; padding is inside an element, gap between elements, margin outside.

Base token `md.sys.measurement.space100` = 8dp; new tokens follow the multiplier pattern (space225 = 18dp = 8 x 2.25). Nested units not multiples of 8 (2, 4, 6, 10dp) are legitimate in components. System spacing tokens are Jetpack Compose only; on the web treat them as a guide. Example from search: 8dp vertical padding, 8dp horizontal gaps, 24dp horizontal margins (12dp when focused). Leading/trailing swap in RTL.

| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| SPC-01 | Spacing values sit on the 8dp scale | Multiples of 8 for layout; 2, 4, 6, 10dp allowed as nested units inside components | C | styles/spacing/tokens@2026-05-18 |
| SPC-02 | Spacing is tokenized, not hardcoded | Reuse a small set of spacing values/variables across custom components and layouts | C | styles/spacing/applying-spacing@2026-05-18 |
| SPC-03 | Padding and gaps before margins | Define padding/gap on the parent container; avoid per-child margins | C | styles/spacing/overview@2026-05-18 |
| SPC-04 | Spacing adapts to context | Different values per device class or density (e.g. vertical padding by density) | C | styles/spacing/applying-spacing@2026-05-18 |
| SPC-05 | Spacing is unchanged when text scales | Same spacing at 200% text size | F | styles/spacing/applying-spacing@2026-05-18 |
| SPC-06 | Leading/trailing, not left/right | Horizontal spacing mirrors in RTL | C | styles/spacing/overview@2026-05-18 |
| SPC-07 | Custom tokens follow the multiplier of 8dp | New values expressed as 8dp x n | E | styles/spacing/applying-spacing@2026-05-18 |

## Motion

Two systems. Physics (springs) is the current Expressive system; easing and duration is the legacy system, still used for transitions.

Physics: schemes expressive (default for hero moments and key interactions) and standard (utilitarian, minimal bounce). Spatial springs (position, size, rotation, corner radius) overshoot; effects springs (color, opacity) never overshoot. Speeds fast (small components such as switches and buttons), default (partial-screen, e.g. bottom sheet), slow (full-screen). Token form `md.sys.motion.spring.<speed>.<spatial|effects>`. Web curve equivalents:

| Spring | cubic-bezier | Duration |
| --- | --- | --- |
| Expressive fast / default / slow spatial | 0.42,1.67,0.21,0.90 / 0.38,1.21,0.22,1.00 / 0.39,1.29,0.35,0.98 | 350 / 500 / 650ms |
| Expressive fast / default / slow effects | 0.31,0.94,0.34,1.00 / 0.34,0.80,0.34,1.00 / 0.34,0.88,0.34,1.00 | 150 / 200 / 300ms |
| Standard fast / default / slow spatial | 0.27,1.06,0.18,1.00 (all) | 350 / 500 / 750ms |
| Standard fast / default / slow effects | same as expressive effects | 150 / 200 / 300ms |

Duration tokens: short1-4 = 50, 100, 150, 200ms; medium1-4 = 250, 300, 350, 400ms; long1-4 = 450, 500, 550, 600ms; extra-long1-4 = 700, 800, 900, 1000ms (rare, ambient, no user input).

Easing tokens (CSS): emphasized has no CSS curve (use standard as fallback); emphasized.decelerate `cubic-bezier(0.05, 0.7, 0.1, 1.0)`; emphasized.accelerate `cubic-bezier(0.3, 0.0, 0.8, 0.15)`; standard `cubic-bezier(0.2, 0.0, 0, 1.0)`; standard.decelerate `cubic-bezier(0, 0, 0, 1)`; standard.accelerate `cubic-bezier(0.3, 0, 1, 1)`.

| Easing | Duration | Transition type |
| --- | --- | --- |
| Emphasized | 500ms | Begin and end on screen |
| Emphasized decelerate | 400ms | Enter the screen |
| Emphasized accelerate | 200ms | Exit the screen |
| Standard | 300ms | Begin and end on screen |
| Standard decelerate | 250ms | Enter the screen |
| Standard accelerate | 200ms | Exit the screen |

Transition patterns (legacy easing/duration): Container transform (card to detail; hero moments, shallow hierarchies; most dramatic), Forward and backward (consecutive hierarchy levels; platform defaults), Lateral (peer content such as tabs, slide in unison), Top level (nav bar/rail/drawer destinations; quick fade, no grouping), Enter and exit (dialogs, menus, sheets; expands away from the device edge), Skeleton loaders (pulse from top left to bottom right, content fades in over them).

| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| MOT-01 | Animations use easing, not linear or instant | Every transition has an easing curve from the token sets | C | styles/motion/easing-and-duration/applying-easing-and-duration@2025-09-26 |
| MOT-02 | Easing matches movement | Enter: emphasized/standard decelerate; exit permanently: accelerate; on-screen to on-screen: emphasized/standard | C | styles/motion/easing-and-duration/applying-easing-and-duration@2025-09-26 |
| MOT-03 | Durations come from tokens | 50 to 1000ms steps listed above; typical pairs in the table | C | styles/motion/easing-and-duration/tokens-specs@2025-09-26 |
| MOT-04 | Exit shorter than enter | Exit ~200ms; enter ~250 to 400ms | C | styles/motion/easing-and-duration/applying-easing-and-duration@2025-09-26 |
| MOT-05 | Duration scales with distance/area | Small utility changes short; large traversals long; extra-long only for ambient motion | C | styles/motion/easing-and-duration/applying-easing-and-duration@2025-09-26 |
| MOT-06 | Reduced-motion setting honored | Subtle fades replace slides/scales; parallax and shape morph disabled (repeated in the floor as A11-15) | F | styles/motion/transitions/applying-transitions@2025-09-26 |
| MOT-07 | Effects (color, opacity) do not overshoot | Spatial properties may overshoot; effects springs/curves must not | E | styles/motion/overview/how-it-works@2026-05-06 |
| MOT-08 | One motion scheme per product | Expressive for hero/key moments, standard for utility; mixing is deliberate per element | E | styles/motion/overview/how-it-works@2026-05-06 |
| MOT-09 | Fade out before fade in | No overlapping semi-transparent content; short fades for dialogs | C | styles/motion/transitions/applying-transitions@2025-09-26 |
| MOT-10 | Loading uses skeletons, no layout jumps | Content must not shift or pop in | C | styles/motion/transitions/applying-transitions@2025-09-26 |
| MOT-11 | Top-level navigation uses a quick fade | Not lateral sliding between nav destinations | C | styles/motion/transitions/applying-transitions@2025-09-26 |
| MOT-12 | Lateral slide only for peer content | Tabs/carousels; not for hierarchical screens | C | styles/motion/transitions/applying-transitions@2025-09-26 |
| MOT-13 | Full-height or full-width slides not used for hierarchy | Enter/exit pattern is for components, not hierarchical screens | C | styles/motion/transitions/applying-transitions@2025-09-26 |
| MOT-14 | Container transform reserved for hero or shallow-hierarchy moments | Not the default for every navigation | C | styles/motion/transitions/applying-transitions@2025-09-26 |
| MOT-15 | Consistent direction and simple style | Elements move along one primary axis; no highly stylized motion in frequent transitions | C | styles/motion/transitions/applying-transitions@2025-09-26 |
| MOT-16 | Components enter from their origin edge | Top menu expands down; bottom snackbar up; nav drawer from left; bottom sheet from bottom | C | styles/motion/transitions/transition-patterns@2025-09-26 |
| MOT-17 | Jump cuts avoided | Instant screen changes only when efficiency is the priority (e.g. opening a menu) | C | styles/motion/transitions/applying-transitions@2025-09-26 |

## Icons

Use: Material Symbols (outlined, rounded, sharp) at 24dp by default, with a sufficient touch target and a label where meaning is unclear.

Facts: standard size 24dp x 24dp; optical sizes 20, 24, 40, 48dp (20 for desktop and dense layouts, 40 and 48 for display/headline contexts). Axes: weight 100 to 700 (400 regular, 2dp stroke), fill 0 to 1, grade (default 0 for dark-on-light, -25 for light-on-dark; positive for active/emphasized), optical size 20 to 48. Default corner radius 2dp. All icon content must stay inside the trim area.

| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| ICO-01 | Default icon size is 24dp | Other sizes only 20, 40, 48dp | C | styles/icons/designing-icons@2026-05-18 |
| ICO-02 | One symbol style per product | Outlined, rounded or sharp, not mixed | C | styles/icons/applying-icons@2026-05-18 |
| ICO-03 | Stroke weight regular (400, 2dp) unless matched to type | Weight range 100 to 700; keep consistent across icons | C | styles/icons/designing-icons@2026-05-18 |
| ICO-04 | Icon target size for 24dp icons | >= 48dp target | F | styles/icons/applying-icons@2026-05-18 |
| ICO-05 | Icon target size for 20dp icons | >= 40dp target; condensed only for mouse/keyboard-primary UIs | F | styles/icons/applying-icons@2026-05-18 |
| ICO-06 | Small icons carry a label | Complex icons and key-action icons below 20dp need an accompanying text label | F | styles/icons/applying-icons@2026-05-18 |
| ICO-07 | Navigation icons have labels | Abstract icons get text; nav items must be labeled | F | styles/icons/applying-icons@2026-05-18 |
| ICO-08 | Fill conveys state | Filled vs unfilled (0 to 1) for selected/unselected | C | styles/icons/applying-icons@2026-05-18 |
| ICO-09 | Optical size matches rendered size | Use the optical-size axis rather than scaling a 24dp glyph, so stroke weight stays balanced | C | styles/icons/applying-icons@2026-05-18 |
| ICO-10 | Grade compensates for polarity | Light icons on dark use lower grade (-25) so apparent size matches | E | styles/icons/applying-icons@2026-05-18 |
| ICO-11 | Icon weight/grade harmonized with adjacent text | Match grade between text font and symbols | E | styles/icons/applying-icons@2026-05-18 |
| ICO-12 | Icon art stays within trim area | No parts outside the trim area; complex icons use optical corrections without distortion | C | styles/icons/designing-icons@2026-05-18 |
