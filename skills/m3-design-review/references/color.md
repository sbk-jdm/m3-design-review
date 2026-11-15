# Color and design tokens

Snapshot date: 2026-05-21. Base URL: https://m3.material.io/
The `Source` path maps to `https://m3.material.io/<path>` (use the page's `source_url` when in doubt).
Distilled from Material Design 3 documentation (Apache 2.0 / CC BY 4.0); see NOTICE.md.
Units: dp as in the source; on the web 1dp is treated as 1 CSS px.

Tiers: F = floor (accessibility minimum), C = core M3 (deviation needs an explicit decision), E = optional / add-on.

## 1. Concepts a reviewer needs

- A color role is a named purpose ("number" in a paint-by-number canvas). UI elements get roles, roles get colors. 26 standard roles in six groups: primary, secondary, tertiary, error, surface, outline; plus add-on roles (fixed, dim/bright surfaces) and inverse, scrim, shadow.
- Role-name vocabulary: Surface = background and large low-emphasis areas. Primary/Secondary/Tertiary = accents. Container = fill for foreground elements (not for text or icons). On = text/icons placed on the paired parent. Variant = lower-emphasis alternative.
- Roles are the same in static (baseline or brand) and dynamic schemes; only the values change. Light and dark themes use the same role names with different tones. Three contrast levels exist (standard, medium, high) and apply to both themes.
- Review by role and purpose, not by hex value: a color is correct if the role matches the element's job and pairs are respected.

## 2. Role catalogue (what each is for)

| Role | Use |
| --- | --- |
| primary / on-primary | Highest-emphasis fills, text, icons against surface (filled button, active states); on-primary for content on it |
| primary-container / on-primary-container | Standout fill for key components (FAB); on-* for content on it |
| secondary / secondary-container (+ on-*) | Less prominent elements: filter chips, tonal buttons, selected nav icon, dismissive buttons |
| tertiary / tertiary-container (+ on-*) | Contrasting accent for small elements needing special attention (badge, input field); at designer discretion |
| error / error-container (+ on-*) | Error states and urgency; static in dynamic schemes, still adapts to light/dark |
| surface | Default background |
| surface-container-lowest / low / (default) / high / highest | Container fills ordered by emphasis (cards, sheets, dialogs, nav areas) |
| on-surface | Default text and icons on any surface or surface container |
| on-surface-variant | Lower-emphasis text and icons on any surface or surface container |
| outline | Important boundaries (text-field border) |
| outline-variant | Decorative lines (dividers) and borders where inner content has 4.5:1 |
| inverse-surface / inverse-on-surface / inverse-primary | Reversed-contrast elements, e.g. snackbar background, text, and its text button |
| surface-dim / surface-bright (add-on) | Dimmest / brightest surface in both themes (keep relative brightness across themes) |
| primary/secondary/tertiary-fixed, -fixed-dim, on-*-fixed, on-*-fixed-variant (add-on) | Same tone in light and dark; for deliberately theme-invariant fills |

Default surface-container mappings on components: container-low for elevated button and card; container for top/bottom bars; container-high for FAB (default surface FAB) and basic dialog; container-highest for input label and off switch.

## 3. Rules

| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| COL-01 | Colors come from roles, not raw values | Use role tokens; no static hex or tonal-palette values in components, which break with light/dark, contrast control and other features | C | styles/color/advanced/apply-colors@2025-09-26 |
| COL-02 | Foreground uses the matching `on-*` of its fill | on-primary on primary, on-primary-container on primary-container, on-secondary-container on secondary-container, on-tertiary(-container), on-error(-container); on-surface / on-surface-variant on surface and surface containers; inverse-on-surface on inverse-surface | C | styles/color/roles@2026-05-18 |
| COL-03 | Apply roles only in intended pairs or layering orders | Improper mixing (e.g. primary-container fill with on-surface text) can lose legibility when contrast level or theme changes | C | styles/color/roles@2026-05-18 |
| COL-04 | Do not invent pairs outside the on-* pairs without checking contrast | Only "on-" pairs are guaranteed sufficient contrast; other pairs may miss 4.5:1 (small text) / 3:1 (large text) | F | styles/color/advanced/apply-colors@2025-09-26 |
| COL-05 | Small text contrast | At least 4.5:1 against its background | F | foundations/designing/color-contrast@2025-10-08 |
| COL-06 | Large text and graphics contrast | At least 3:1; "large" = 14 pt bold / 18 pt regular and up | F | foundations/designing/color-contrast@2025-10-08 |
| COL-07 | Disabled states are exempt from contrast minimums | No ratio required for disabled | F | foundations/designing/color-contrast@2025-10-08 |
| COL-08 | Clustered non-text elements (e.g. a button group) need container-vs-background contrast | At least 3:1 between container color and its background | F | foundations/designing/color-contrast@2025-10-08 |
| COL-09 | Standalone prominent elements (e.g. FAB) are exempt from the 3:1 container rule | Do not flag a FAB container below 3:1 against background | C | foundations/designing/color-contrast@2025-10-08 |
| COL-10 | Color pairs in roles give at least 3:1 | Role pairs are built on tone distance; medium contrast level gives 3:1, high gives 7:1 | C | styles/color/system/how-the-system-works@2026-05-06 |
| COL-11 | Custom components must support contrast levels via roles | e.g. custom slider uses primary-container and on-primary-container rather than fixed colors | C | styles/color/system/how-the-system-works@2026-05-06 |
| COL-12 | Primary = most prominent/important elements | FAB, high-emphasis buttons, active states; reserve for emphasis, not decoration | C | styles/color/roles@2026-05-18 |
| COL-13 | Secondary = recessive elements | Filter chips, tonal buttons, selected nav icon; not for elements needing immediate attention | C | styles/color/roles@2026-05-18 |
| COL-14 | Tertiary = small, special-emphasis accents | Badge, notification, input field; balances primary and secondary | C | styles/color/roles@2026-05-18 |
| COL-15 | Containers are fills only | Container roles are not to be used for text or icons | C | styles/color/roles@2026-05-18 |
| COL-16 | Error roles communicate error states | e.g. invalid input; error color stays red-family regardless of dynamic source | C | styles/color/roles@2026-05-18 |
| COL-17 | Page background is `surface`; nav area is `surface-container` | Same layout region keeps the same role across window size classes (mobile and tablet) | C | styles/color/roles@2026-05-18 |
| COL-18 | Container hierarchy by emphasis | lowest < low < default < high < highest; use higher/lower steps for nested containers and expanded layouts, applied consistently | C | styles/color/roles@2026-05-18 |
| COL-19 | Surface roles are not tied to elevation | Tone-based surface containers replaced the old elevation-tinted surfaces (+1 to +5) | C | styles/color/system/overview@2026-05-06 |
| COL-20 | Dividers use `outline-variant`, not `outline` | Outline has different contrast requirements | C | styles/color/roles@2026-05-18 |
| COL-21 | Multi-element containers (cards) use `outline-variant` for borders, not `outline` | Same rationale | C | styles/color/roles@2026-05-18 |
| COL-22 | Borders that define an interactive target use `outline` or another role with 3:1 against surface | Do not use outline-variant to carry hierarchy or define target boundaries | F | styles/color/roles@2026-05-18 |
| COL-23 | `outline-variant` borders are allowed on chips/buttons only if inner content has 4.5:1 | Text and icons inside meet 4.5:1 | F | styles/color/roles@2026-05-18 |
| COL-24 | Inverse roles are selective | Use for reversed-contrast surfaces such as snackbars; text button on it uses inverse-primary | C | styles/color/roles@2026-05-18 |
| COL-25 | Fixed colors are not used where contrast is needed | They do not change between light/dark; use primary/secondary/tertiary roles for buttons and accents | E | styles/color/roles@2026-05-18 |
| COL-26 | Fixed fills pair with `on-*-fixed`, variants with `on-*-fixed-variant` | Primary-fixed with on-primary-fixed; lower emphasis with on-primary-fixed-variant | E | styles/color/roles@2026-05-18 |
| COL-27 | Surface-bright/dim keep relative brightness across themes | Use only when a region must stay brightest/dimmest in both themes; default surface inverts | E | styles/color/roles@2026-05-18 |
| COL-28 | Both themes must be provided from one role set | Same role names in light and dark; a dark theme made by hard-coding separate colors per component is a smell | C | styles/color/system/how-the-system-works@2026-05-06 |
| COL-29 | Dynamic-color content schemes: max two color source types per screen | e.g. baseline/wallpaper scheme plus one content-based scheme | E | styles/color/advanced/apply-colors@2025-09-26 |
| COL-30 | Content-based color stays next to its source content | Do not apply it where the source image is not visible | E | styles/color/advanced/apply-colors@2025-09-26 |
| COL-31 | Do not replace semantic colors with dynamic color | Red error and green success keep conventional meaning | C | styles/color/advanced/apply-colors@2025-09-26 |
| COL-32 | Extra semantic/brand colors are defined as static color roles | Four derived roles (color, on-color, container, on-container) following accent conventions; Material's error red needs no custom equivalent | E | styles/color/advanced/define-new-colors@2025-09-26 |
| COL-33 | Harmonize static semantic colors in dynamic schemes; do not harmonize brand colors | Harmonization shifts hue slightly toward primary while keeping its meaning | E | styles/color/advanced/adjust-existing-colors@2025-09-26 |
| COL-34 | Custom color roles must state palette+tone for both themes, pairings, and meet contrast minimums | Define only if existing roles and static colors cannot meet the need | E | styles/color/advanced/define-new-colors@2025-09-26 |
| COL-35 | Static (baseline/brand) scheme: take colors from the generated scheme's roles | Baseline suits enterprise, M2 migration, iOS, or when dynamic color is not ready; role mapping is identical to dynamic | E | styles/color/choosing-a-scheme@2025-09-26 |
| TOK-01 | Use tokens instead of hard-coded values | Tokens point to values (color, font, size); names stay stable if values change | C | foundations/design-tokens/overview@2025-11-27 |
| TOK-02 | Token names go general to specific, period-separated | `md` (system) . class (`ref`, `sys`, `comp`) . descriptive role words | C | foundations/design-tokens/overview@2025-11-27 |
| TOK-03 | Three token classes with distinct jobs | ref = raw options (e.g. `md.ref.palette.secondary90` = #E8DEF8); sys = purpose/theming (e.g. `md.sys.color.secondary-container`); comp = per-component (e.g. `md.comp.fab.primary.container.color`) | C | foundations/design-tokens/overview@2025-11-27 |
| TOK-04 | System tokens point to reference tokens, not static values | Theming (light/dark, density, RTL) is done by the sys token resolving to different ref tokens per context | C | foundations/design-tokens/overview@2025-11-27 |
| TOK-05 | Component tokens point to system or reference tokens, no hex | A style decision shared by similar components should be a token | C | foundations/design-tokens/overview@2025-11-27 |
| TOK-06 | Tokens are named by purpose/location, not by appearance | A name states how or where it is used; avoid names like "blue-500" for roles | C | foundations/design-tokens/overview@2025-11-27 |

## 4. Dark theme behavior

- Dark theme is generated from the same roles; roles flip tone (surface is light in light theme, dark in dark theme; containers change tone). Do not hand-tune per component.
- Error roles adapt to light/dark but remain red-family. Fixed roles do not change tone between themes (hence the contrast risk, COL-25). Surface-bright/dim keep relative brightness.
- Dark theme surface roles were slightly darkened in the 2023 update; default light surface is tone 98 (not 99).
- Medium contrast (3:1) is noted to risk halation at higher contrasts for some users; high contrast (7:1) applies to content, e.g. a card's content but not the card container.

## 5. Misuse patterns the docs state

- Raw hex/tonal values instead of roles (COL-01); wrong pairings such as primary-container with on-surface text (COL-03).
- Outline for dividers or cards; outline-variant for interactive boundaries (COL-20 to COL-22).
- Fixed colors for buttons on surface (COL-25).
- Replacing semantic red/green with content-based color (COL-31).
- Container roles used for text or icons (COL-15).
- Different surface/nav role mappings per breakpoint (COL-17).
- The docs give no numeric limit for how much of a screen primary may cover; they define primary as for key, prominent elements and surface roles for large areas. Flag large primary fills as a COL-12/COL-17 concern, not a numeric violation.

## 6. Mapping a custom token system to M3 roles

1. Inventory variables (e.g. `--bg`, `--card`, `--accent`, `--text-2`, `--line`). Ignore names; classify each by what it paints.
2. Map by purpose:
   - Page background -> surface. Cards, sheets, dialogs, nav bars, input fills -> a surface-container step; more nested or emphasized = higher step.
   - Main body text/icons -> on-surface; secondary/muted text -> on-surface-variant.
   - Brand/action color for the main CTA, FAB, active states -> primary, its text -> on-primary. Tonal/less prominent controls and selected states -> secondary-container + on-secondary-container. Small attention accents -> tertiary(-container).
   - Danger/invalid -> error(-container) with on-*. Success/warning/info are not M3 roles: treat as static semantic roles with four parts (COL-32).
   - Borders on inputs and interactive targets -> outline; dividers and card borders -> outline-variant.
   - Toast/snackbar -> inverse-surface family. Scrim/overlay -> scrim; drop shadows -> shadow.
3. Check completeness: every fill variable should have a foreground partner; flag fills with no `on-` counterpart, and text variables used on more than one unrelated fill.
4. Check theme parity: each variable needs both light and dark values (or resolve through a theme context), per COL-28 and TOK-04.
5. Verify contrast per pair: 4.5:1 small text, 3:1 large text and non-text container/border (COL-05 to COL-08), after the mapping, using computed values.
6. A custom variable that fits no role is a candidate for a custom/static role (COL-32, COL-34); report it as a gap, not as a violation.
