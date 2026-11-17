# Material 3 Expressive

Snapshot date: 2026-11-17. Base URL: https://m3.material.io/
`path` in the Source column maps to `https://m3.material.io/<path>` (use the page `source_url` when in doubt).
Distilled from Material Design 3 documentation (Apache 2.0 / CC BY 4.0); see NOTICE.md.
Units: dp as in the source; on the web 1dp is treated as 1 CSS px.

## How to treat Expressive in a review

- Expressive is an evolution of M3, not a new version: baseline M3 is not deprecated and this is not "M4". Adopting Expressive is optional.
- A screen that follows baseline M3 is not wrong for lacking Expressive features. Never report a baseline-vs-Expressive mismatch as a violation; report it as a Suggestion (tier E) at most.
- Exception: where the docs mark a baseline component "no longer recommended" (table below), mention it as a Suggestion with the stated replacement, not as a defect.
- Mixed use is fine, but flag inconsistency inside one product (e.g. one screen with Expressive nav bar, another with baseline) as a suggestion to pick one family.
- Floors (accessibility, touch target, contrast) and core rules in other reference files still apply to Expressive designs. The docs state no Expressive-specific floors.
- Do not demand Expressive features that the target platform cannot ship (see Platform availability).

## Platform availability

| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| EXP-01 | Web has no Expressive component implementations in the official libraries | Component overviews list "Web: Expressive" as UNAVAILABLE for app bars, buttons, button groups, extended FAB, FAB, FAB menu, icon buttons, lists, loading indicator, menus, nav bar, nav rail, progress indicators, search, sliders, split button, toolbars. Do not require them on web; custom CSS builds are the implementer's choice | E | components/buttons/overview@2026-05-18 |
| EXP-02 | Jetpack Compose is the lead platform | Expressive components are listed AVAILABLE on Compose for all items in EXP-01; Android Views (MDC-Android) lists most as AVAILABLE, but FAB menu, menus and search as UNAVAILABLE | E | components/fab-menu/overview@2026-05-18 |
| EXP-03 | Motion physics on web | Web is "compatible": use springs where possible, otherwise the spring-to-curve conversion table below. Android Views: spring tokens available but not added to components | E | styles/motion/overview/specs@2026-07-17 |
| EXP-04 | Shape morph API | Available via the Compose Shapes API; Web "not currently available". A web design may still show a shape change but has no official morph API | E | styles/shape/shape-morph@2026-07-17 |
| EXP-05 | Flutter motion physics | Listed as unavailable | E | styles/motion/overview/how-it-works@2026-07-17 |

## Expressive tactics (design-level checks)

| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| EXP-10 | One clear focal point per screen | The primary action/content is the largest, highest-contrast element; supporting controls are smaller or in lighter containers. Several equally large, equally colored elements competing = hierarchy problem | E | foundations/usability/applying-m3-expressive@2026-07-17 |
| EXP-11 | Differentiate color roles by purpose | Primary role for the main action/key data; secondary / secondary container for selected or supportive states; do not use the same role (e.g. primary + primary container) for every action and data point | E | foundations/usability/applying-m3-expressive@2026-07-17 |
| EXP-12 | Contain and group related content | Related items share a container or background tone; ungrouped lists that blend together are weaker. Key content gets generous space and the brightest surface mapping | E | blog/building-with-m3-expressive@2026-05-07 |
| EXP-13 | Emphasized type for key moments | Use the emphasized type styles (heavier weight, larger size) for headlines, the primary action, or key numbers; keep supporting text on regular styles | E | blog/building-with-m3-expressive@2026-05-07 |
| EXP-14 | Mix shapes deliberately | Combine round and square shapes or break from the surrounding shape style to draw attention to one element; avoid same-sized small shapes for essential actions | E | blog/building-with-m3-expressive@2026-05-07 |
| EXP-15 | Hero moments are rare | At most 1-2 hero moments per product; a hero moment combines several tactics for an emotionally impactful or key interaction. More = overwhelming | E | blog/building-with-m3-expressive@2026-05-07 |
| EXP-16 | Calm layouts around expressive shapes | Uniform shape sizes, even spacing, no overlapping shapes when comparing data; secondary goals use fewer tactics than the primary goal | E | foundations/usability/applying-m3-expressive@2026-07-17 |
| EXP-17 | Primary action placement | Primary action is large and placed low on a phone screen for thumb reach; secondary actions (e.g. pause/stop during a task) are less prominent and spaced away from the hero visual | E | foundations/usability/applying-m3-expressive@2026-07-17 |
| EXP-18 | Shape library only on visual elements | The 35-shape library suits decorative items (image crops, avatars, metric badges); avoid unconventional shapes on text-heavy containers; use sparingly | E | styles/shape/corner-radius-scale@2026-07-17, styles/shape/overview-principles@2026-07-17 |

## Shape additions

| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| EXP-20 | Corner scale has ten steps | None 0, XS 4, S 8, M 12, L 16, L-increased 20, XL 28, XL-increased 32, XXL 48dp, Full. The docs do not label which steps are Expressive-only | E | styles/shape/corner-radius-scale@2026-07-17 |
| EXP-21 | Nested radii use optical roundness | Inner radius = outer radius - padding (example 48 - 14 = 34dp); identical radii on nested containers look unbalanced | E | styles/shape/corner-radius-scale@2026-07-17 |
| EXP-22 | Cut corners need extra padding | Switching rounded to cut corners clips content more than a same-size rounded corner; pad information-dense components | E | styles/shape/corner-radius-scale@2026-07-17 |
| EXP-23 | Inner corners for grouped items | Closely grouped items (menus, split buttons) use asymmetric corners; same 10-step scale | E | styles/shape/corner-radius-scale@2026-07-17 |
| EXP-24 | Shape morph | Used in standard button group and loading indicator; defaults to the expressive motion scheme | E | styles/shape/shape-morph@2026-07-17 |

## Motion physics

| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| EXP-30 | Two schemes | Expressive: bouncy, for most UIs, hero moments and key interactions. Standard: minimal bounce, for utilitarian products. Pick one per product; swap per element only to emphasize a key moment | E | styles/motion/overview/how-it-works@2026-07-17 |
| EXP-31 | Spatial vs effects | Spatial springs (position, rotation, size, rounded corners) may overshoot. Effects springs (color, opacity) must not overshoot | E | styles/motion/overview/how-it-works@2026-07-17 |
| EXP-32 | Three speeds | Default: partial-screen motion (bottom sheet, expanded rail). Fast: small components (switch, button). Slow: full-screen motion. Token form: `md.sys.motion.spring.fast.spatial`, scheme not in token name | E | styles/motion/overview/how-it-works@2026-07-17 |
| EXP-33 | Springs are interruptible | Gestures and retargeting should continue from current velocity, not restart a fixed-duration tween | E | blog/m3-expressive-motion-theming@2026-05-08 |
| EXP-34 | Custom components reuse the scheme | Custom components animate size/position with spatial and color/opacity with effects specs of the theme, not ad hoc durations | E | blog/m3-expressive-motion-theming@2026-05-08 |
| EXP-35 | Legacy easing/duration | Still valid fallback and still used for transitions; not an error to find | E | styles/motion/overview/specs@2026-07-17 |

Web spring-to-curve (cubic-bezier x1,y1,x2,y2 / duration), source styles/motion/overview/specs@2026-07-17:

| Token | Expressive | Standard |
| --- | --- | --- |
| Fast spatial | 0.42,1.67,0.21,0.90 / 350ms | 0.27,1.06,0.18,1.00 / 350ms |
| Default spatial | 0.38,1.21,0.22,1.00 / 500ms | 0.27,1.06,0.18,1.00 / 500ms |
| Slow spatial | 0.39,1.29,0.35,0.98 / 650ms | 0.27,1.06,0.18,1.00 / 750ms |
| Fast effects | 0.31,0.94,0.34,1.00 / 150ms | same |
| Default effects | 0.34,0.80,0.34,1.00 / 200ms | same |
| Slow effects | 0.34,0.88,0.34,1.00 / 300ms | same |

## Component deltas: baseline M3 -> Expressive

| Component | What Expressive adds, changes, or deprecates | Source |
| --- | --- | --- |
| Common buttons | Five sizes: XS 32, S 40 (default), M 56, L 96, XL 136dp container height; default and toggle variants; round and square shapes; shape morphs when pressed and, for toggles, when selected; small-button padding 16dp recommended (24dp no longer recommended). Per-style tokens `md.comp.button.<style>` replace deprecated filled/tonal/outlined/text/elevated button tokens | components/buttons/overview@2026-07-24, components/buttons/specs@2026-07-24 |
| Button groups | New. Standard and connected groups; apply shape, motion and width changes to buttons and icon buttons; all sizes XS-XL, single-select, multi-select or selection-required. Connected group replaces segmented button | components/button-groups/overview@2026-09-16 |
| Segmented buttons | No longer recommended; use connected button group | components/segmented-buttons/overview@2026-09-16 |
| Icon buttons | More shapes and sizes (XS 32, S 40, M 56, L 96, XL 136dp), three widths (narrow, default, wide); shape changes when selected; neighbors in a button group react when pressed | components/icon-buttons/overview@2026-07-17 |
| Split button | New. Separate menu button that rotates and changes shape when active; sizes XS-XL, elevated/filled/tonal/outlined; can sit alongside other buttons of the same size | components/split-button/overview@2026-09-08 |
| FAB | Medium FAB added (80dp); FAB 56 and large 96dp unchanged; small FAB no longer recommended; surface color not recommended; color sets renamed to primary/secondary/tertiary container, with new solid primary/secondary/tertiary | components/floating-action-button/overview@2026-07-27, components/floating-action-button/specs@2026-07-27 |
| Extended FAB | Small 56 / medium 80 / large 96dp, matching FAB heights; small uses title medium (was label large) with smaller inner padding; baseline extended FAB replaced by small; surface color not recommended (surface and branded exist only as baseline token sets) | components/extended-fab/overview@2026-07-27, components/extended-fab/specs@2026-07-27 |
| FAB menu | New. Opens from any FAB with 2-6 related actions (not used with extended FABs); primary, secondary or tertiary color set. Should replace speed dial and stacked small FABs | components/fab-menu/overview@2026-07-17 |
| Navigation bar | New flexible bar replaces baseline: container 64dp (baseline 80dp); horizontal items supported in medium windows; active label color changed to secondary; tokens `md.comp.nav-bar`, not `md.comp.navigation-bar` | components/navigation-bar/overview@2026-07-28, components/navigation-bar/specs@2026-07-28 |
| Navigation rail | Collapsed and expanded rails replace baseline rail (80dp wide); expanded rail (non-modal or modal) replaces navigation drawer and can hide when collapsed; active label on vertical items changed to secondary; tokens `md.comp.nav-rail` (+ `.collapsed`, `.item`) | components/navigation-rail/overview@2026-07-24, components/navigation-rail/specs@2026-07-24 |
| Navigation drawer | No longer recommended; use expanded navigation rail | components/navigation-drawer/overview@2026-07-30 |
| Toolbars | New. Docked toolbar (64dp, square corners by default; may be rounded on web and large screens) replaces bottom app bar; floating toolbar (64dp, full corners, horizontal or vertical, can pair with a FAB) for more actions and varied placement; standard and vibrant color styles. Not shown together with a navigation bar | components/toolbars/overview@2026-07-28, components/toolbars/specs@2026-07-28 |
| App bars | Renamed from top app bar. Search app bar added (opens the search view); medium flexible and large flexible replace baseline medium and large (shorter, subtitle, wrapping, centered or leading text); small gains subtitle and centered text; center-aligned merged into small | components/app-bars/overview@2026-07-24 |
| Progress indicators | Configurable track height (default 4dp); optional wave on the active track (linear and circular) | components/progress-indicators/overview@2026-07-29 |
| Loading indicator | New. For waits of about 200 ms to 5 s; morphing shapes; replaces most indeterminate circular indicators; contained or uncontained; scalable (default 48dp, 24-240dp); never decorative | components/loading-indicator/overview@2026-07-29 |
| Sliders | Five sizes (XS default, S, M, L, XL; tokens `md.comp.slider.<size>`, e.g. xsmall); vertical or horizontal; optional inset icon (standard slider only); discrete slider is now the stops configuration | components/sliders/overview@2026-07-17, components/sliders/specs@2026-07-17 |
| Lists | Expressive list recommended for new designs (baseline not recommended): standard or segmented style, highlighted selection states, slot support; Android Views and Compose | components/lists/overview@2026-08-06 |
| Menus | Vertical menus recommended for new designs: new shapes, standard or vibrant colors, grouped layout, selection states, submenu motion; gaps noted for Android; baseline menu still available | components/menus/overview@2026-07-28 |
| Search | Contained style (recommended) replaces the divided baseline; new motion (bar widens when focused), gaps between result groups, more flexible trailing icons | components/search/overview@2026-07-27 |

Expressive layout (I/O 2026): new layout scaffold, an 8dp-based spacing system applied via tokens to margins, padding and gaps, and guidance for watches and XR. Source: blog/whats-new-at-io26@2026-05-19.

| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| EXP-40 | Flag deprecated baseline parts as suggestions | Segmented button, navigation drawer, bottom app bar, small FAB, baseline extended FAB, speed dial / stacked small FABs: suggest the replacement named in the table; never mark as a violation | E | components/segmented-buttons/overview@2026-09-16, components/navigation-drawer/overview@2026-07-30, components/toolbars/overview@2026-07-28, components/floating-action-button/overview@2026-07-27, components/extended-fab/overview@2026-07-27, components/fab-menu/overview@2026-07-17 |
| EXP-41 | Do not mix baseline and Expressive size sets within a component family | e.g. extended FAB and FAB on one screen share the same height step | E | components/extended-fab/overview@2026-05-18 |
| EXP-42 | Loading indicator vs progress | Under 200 ms: no indicator. About 200 ms to 5 s: loading indicator (indeterminate). Over 5 s or measurable progress: progress indicator. Never morph a loading indicator into a progress indicator | E | components/loading-indicator/overview@2026-07-29 |
| EXP-43 | Spacing from the 8dp scale | Margins, padding and gaps should use spacing tokens so layouts adapt to density and device | E | styles/spacing/overview@2026-07-17 |
| EXP-44 | More baseline parts marked not recommended (extends EXP-40) | Medium and large baseline app bars (use flexible), baseline navigation bar (use flexible), baseline navigation rail (use collapsed), baseline list (use expressive list), divided search (use contained), surface-colored FAB and extended FAB, 24dp small-button padding (use 16dp). Baseline menu is still available, so not a finding. Suggestion only | E | components/app-bars/overview@2026-07-24, components/navigation-bar/overview@2026-07-28, components/navigation-rail/overview@2026-07-24, components/lists/overview@2026-08-06, components/search/overview@2026-07-27, components/floating-action-button/overview@2026-07-27, components/buttons/specs@2026-07-24 |
| EXP-45 | Toolbar and navigation bar are not shown together | Both sit at the bottom of the window: navigation bar on primary pages, toolbar on subsequent pages with actions. Docked toolbar only at the bottom; avoid rounded corners on it except on web and large screens. Floating toolbar: no square icon buttons, at most one emphasized action | E | components/toolbars/overview@2026-07-28 |
| EXP-46 | Button group consistency | Standard group: one size and one shape across buttons; mixed sizes only for hero moments; a different shape only for the selected state or to add meaning. Connected group: toggle buttons only, one color style, replaces segmented button. Each button keeps a 48dp target | E | components/button-groups/overview@2026-09-16 |
| EXP-47 | Vibrant color is for emphasis only | Menus and toolbars offer a vibrant (tertiary- or primary-container-based) style besides standard; vibrant is more prominent, so use it sparingly or to signal a temporary mode such as editing | E | components/menus/overview@2026-07-28, components/toolbars/overview@2026-07-28 |
