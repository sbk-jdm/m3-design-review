# Material 3 components, part 1 (app bars to divider)

Snapshot date: 2026-11-17. Base URL: https://m3.material.io/
A source `path` maps to `https://m3.material.io/<path>` (use the page's `source_url` when in doubt).
Distilled from Material Design 3 documentation (Apache 2.0 / CC BY 4.0); see NOTICE.md.
On the web, 1dp is treated as 1 CSS px. Tiers: F = floor, C = core M3, E = Expressive-only/optional/platform-specific.
Corner tokens: extra-small 4dp, small 8dp, medium 12dp, large 16dp, extra-large 28dp (full = pill).

## App bars
**Use:** Top-of-screen page title, navigation control and 1-2 essential actions.
**Dimensions & shape:** Small 64dp; medium flexible 112dp (136 with subtitle); large flexible 120dp (152 with subtitle); search field 56dp, pill. Icon 24dp, avatar 32dp. Leading/trailing space 4dp (search 8dp). Square corners, full window width. Search container fills the space between leading and trailing elements up to 312dp, then grows to 50% of it.
**Color roles:** container surface; on scroll surface-container (search: surface-container-highest), elevation level0 to level2. Title/leading icon on-surface; subtitle and trailing icons on-surface-variant; search container surface-container (surface-bright on darker backgrounds), label on-surface-variant.
**Do / Don't:**
- Do keep to one action, two at most; put many actions in a toolbar.
- Do fill the bar on scroll instead of using a shadow (or go transparent with container-filled icon buttons).
- Do use one filled/tonal icon button at most, to lift a primary action.
- Do include the word Search in the search bar hint; selecting it opens the search view.
- Don't truncate the title; wrap to two lines only in medium/large flexible.
- Don't round the container or shorten it below default height.
- Don't use medium/large baseline bars in Expressive; use the flexible ones.
**Accessibility:**
- First focus lands on the leading button; Tab moves on, Space/Enter activates.
- Icon buttons need action labels, not generic ones; title label matches the visible title.
- Search container vs label needs 3:1 minimum.
**Review checks:** heights match; no corner radius; at most two trailing actions (search bar: two plus avatar on mobile); title type role matches variant; scrolled state differs from rest.
| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| APB-01 | Container height by variant | small 64; medium-flexible 112/136; large-flexible 120/152; search 56dp | C | components/app-bars/specs@2026-07-24 |
| APB-02 | Title type role | search body-large; small title-large; medium-flexible headline-medium; large-flexible display-small | C | components/app-bars/guidelines@2026-07-24 |
| APB-03 | Subtitle type role | small label-medium; medium-flexible label-large; large-flexible title-medium | C | components/app-bars/guidelines@2026-07-24 |
| APB-04 | Shape and width | corner none; spans 100% of window width | C | components/app-bars/guidelines@2026-07-24 |
| APB-05 | Action count | 1-2 trailing icon buttons (up to 4 on large screens for search); avoid overflow menu | C | components/app-bars/guidelines@2026-07-24 |
| APB-06 | Scroll separation | rest = surface; scrolled = surface-container fill, no drop shadow | C | components/app-bars/specs@2026-07-24 |
| APB-07 | Search bar contrast | container vs label text at least 3:1; defaults surface-container / on-surface-variant | F | components/app-bars/accessibility@2026-07-24 |
| APB-08 | Initial focus | first focus on leading button; Tab/Space/Enter operable | F | components/app-bars/accessibility@2026-07-24 |
| APB-09 | Transparent on scroll | optional transparent container on scroll; then every icon button needs a container fill | C | components/app-bars/guidelines@2026-07-24 |
| APB-10 | Search app bar field | hint text includes "Search"; field fills space between elements up to 312dp, then 50%; selecting it opens search view; flexible bars never collapse into a search bar | C | components/app-bars/guidelines@2026-07-24 |

## Badges
**Use:** Notification dot or short count anchored to a navigation icon.
**Dimensions & shape:** Small badge 6dp circle (3dp radius); large badge 16dp tall pill (8dp radius), 16dp for one digit up to 16x34dp at max count; 4dp label padding; label-small text; max 4 characters including "+". Offset from icon's top trailing corner: small 6x6dp, large 14x12dp.
**Color roles:** container error, label on-error (both sizes).
**Do / Don't:**
- Do anchor at the icon's upper trailing edge, mirrored in RTL.
- Do hide the badge after its destination is opened (navigation bars).
- Do use a small badge where space is tight (app bars).
- Don't let the label clip or collide with a neighbour.
- Don't use custom roles unless contrast stays at least 3:1.
**Accessibility:**
- Counts are announced as numbers; dot badges announce "New notification".
**Review checks:** dot is 6dp, count badge 16dp; error/on-error colors; label at most 4 chars; no overlap with trailing elements.
| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| BDG-01 | Badge sizes | small 6dp (3dp radius); large 16dp tall, 16dp one digit to 16x34dp max (8dp radius) | C | components/badges/specs@2026-07-17 |
| BDG-02 | Badge colors | container error; large label on-error; label-small type | C | components/badges/specs@2026-07-17 |
| BDG-03 | Label length | at most 4 characters incl. "+" | C | components/badges/guidelines@2026-07-17 |
| BDG-04 | Custom color contrast | container vs label at least 3:1 | F | components/badges/accessibility@2026-07-17 |
| BDG-05 | Placement | upper trailing edge of icon bounds; large badge must not overlap trailing elements | C | components/badges/guidelines@2026-07-17 |
| BDG-06 | Badge offset | icon top trailing corner to badge bottom leading corner: small 6x6dp, large 14x12dp; large label padding 4dp | C | components/badges/specs@2026-07-17 |

## Bottom sheets
**Use:** Secondary content anchored at the bottom in compact/medium windows; standard (coexists) or modal (blocks).
**Dimensions & shape:** Top corners extra-large 28dp; full width up to 640dp; top margin 72dp; in windows wider than 640dp, 56dp top and side margins. Drag handle 32x4dp, 22dp padding above/below, 48dp-tall hit area; modal initial height capped at 50% of screen.
**Color roles:** container surface-container-low, elevation level1; drag handle on-surface-variant at 0.4 opacity; focus indicator secondary.
**Do / Don't:**
- Do offer scrim tap, swipe down and an item action as dismissals for modal sheets.
- Do show a close affordance on full-screen modal sheets.
- Do give a button alternative if multiple heights exist without a drag handle.
- Don't use modal sheets on desktop-class windows; use a side sheet.
- Don't make the sheet's content the app's main content.
**Accessibility:**
- Resizing needs a single-pointer alternative; handle toggles heights on Space/Enter.
- Handle is a tab stop with role button; label only the handle.
**Review checks:** 28dp top radius; handle 32x4 with 48dp target when interactive (BSH-02); modal opens at most 50% tall; scrim present for modal; width capped at 640dp with 56dp margins on wide windows.
| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| BSH-01 | Container shape and color | top corner 28dp (extra-large); surface-container-low; elevation level1 | C | components/bottom-sheets/specs@2026-07-28 |
| BSH-02 | Drag handle, when interactive | Applies when the sheet is user-resizable and the handle is present: 48dp-tall interactive area at the top of the sheet, Tab stop with role button, only the handle labelled, Space/Enter cycles heights (BSH-05). Look: 32x4dp, on-surface-variant at 0.4 opacity. A decorative handle on a non-resizable sheet is not a target: hide it from assistive tech and judge only its look, as tier C | F | components/bottom-sheets/accessibility@2026-07-28, components/bottom-sheets/specs@2026-07-28 |
| BSH-03 | Max width | 640dp on larger windows | C | components/bottom-sheets/overview@2026-07-28 |
| BSH-04 | Modal initial height | at most 50% of screen height | C | components/bottom-sheets/guidelines@2026-07-28 |
| BSH-05 | Drag alternative | any drag-to-resize needs a single-pointer alternative (handle press cycles heights) | F | components/bottom-sheets/accessibility@2026-07-28 |
| BSH-06 | Modal dismissal | Modal sheet closes by tapping the scrim, swiping down, an item action, or a close affordance in its app bar; a full-screen modal sheet must show a close affordance; Android predictive back closes it. Keyboard (Escape) and focus return are floor rules: A11-11, A11-34 | C | components/bottom-sheets/guidelines@2026-07-28 |
| BSH-07 | Margins | top margin 72dp; window wider than 640dp: 56dp top and 56dp start/end margins; drag handle centered with 22dp top/bottom padding | C | components/bottom-sheets/specs@2026-07-28 |

## Button groups
**Use:** Group related buttons; standard (adjacent buttons react) or connected (replaces segmented button).
**Dimensions & shape:** Group height follows its buttons (XS 32, S 40, M 56, L 96, XL 136dp; see BTN-01), including density. Standard gap XS 18, S 12, M/L/XL 8dp; pressed neighbour width change 15%. Connected gap 2dp, outer shape full (round) and inner corners XS 4, S 8, M 8, L 16, XL 20dp; XS/S connected buttons at least 48dp wide.
**Color roles:** inherited from member buttons (filled, tonal, outlined, elevated); no text or standard icon buttons; do not mix color styles in a connected group.
**Do / Don't:**
- Do keep one size and one shape per group.
- Do use connected groups only for toggle buttons.
- Do keep the group on one line; collapse trailing items to overflow.
- Don't use a connected group when no button can be toggled.
- Don't wrap to a second line.
**Accessibility:**
- Each button at least 48x48dp target; do not reduce XS/S padding.
- Container is not focusable; Tab reaches the first button, arrows move within the group.
**Review checks:** uniform button size; 2dp gap in connected groups; selected button shape changes; single row.
| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| BGR-01 | Container heights | no own height: hugs member buttons (XS 32, S 40, M 56, L 96, XL 136dp per BTN-01) and their density | C | components/button-groups/specs@2026-09-16 |
| BGR-02 | Gaps | standard 18/12/8/8/8dp (XS to XL); connected 2dp | C | components/button-groups/specs@2026-09-16 |
| BGR-03 | Uniform size and shape | same size XS-XL and shape in a group; mix only for hero moments | C | components/button-groups/guidelines@2026-09-16 |
| BGR-04 | Connected use | toggle buttons only; single color style | C | components/button-groups/guidelines@2026-09-16 |
| BGR-05 | Touch target | 48x48dp per button | F | components/button-groups/accessibility@2026-09-16 |
| BGR-06 | Selected state | selected button flips shape round/square | E | components/button-groups/guidelines@2026-09-16 |
| BGR-07 | Connected corners and width | outer corners full (round) or XS 4/S 8/M 8/L 16/XL 20dp (square); inner corners XS 4/S 8/M 8/L 16/XL 20dp; XS and S at least 48dp wide | E | components/button-groups/specs@2026-09-16 |
| BGR-08 | Keyboard | container not focusable or labelled; Tab to first button, arrow keys between buttons, Space/Enter activates | F | components/button-groups/accessibility@2026-09-16 |
| BGR-09 | Member styles | filled, tonal, outlined or elevated (toggle) buttons; avoid text and standard icon buttons (no container) | E | components/button-groups/specs@2026-09-16 |

## Buttons
**Use:** Actions; five color styles (elevated, filled, tonal, outlined, text), default or toggle.
**Dimensions & shape:** Height/icon/side padding: XS 32/20/12; S 40/20/16; M 56/24/24; L 96/32/48; XL 136/40/64dp. Icon-label gap XS 4, S/M 8, L 12, XL 16dp. Round = full; square 12/12/16/28/28dp (XS to XL). Pressed shape 8/8/12/16/16dp. XS and S need 48x48dp target.
**Color roles:** filled primary/on-primary; tonal secondary-container/on-secondary-container; elevated surface-container-low + primary label; outlined outline-variant stroke, on-surface-variant label; text primary label. Toggle selected: elevated/filled primary/on-primary, tonal secondary/on-secondary, outlined inverse-surface/inverse-on-surface; filled toggle unselected surface-container/on-surface-variant. Disabled: label/icon on-surface 0.38, container on-surface 0.1.
**Do / Don't:**
- Do keep labels 1-3 words, sentence case, one line.
- Do use filled for one primary action per page.
- Do put one icon, leading; outlined icon unselected, filled when selected on toggles.
- Don't underline text buttons; use links.
- Don't place outlined/text buttons over images or video.
- Don't overuse elevated (shadow).
**Accessibility:**
- Enabled button needs 3:1 against background (container for elevated/filled/tonal; label for outlined/text).
- Label fits two lines at 200% text size; accessible name matches visible label.
**Review checks:** one filled button per view; label single-line sentence case; XS/S target 48dp; heights from the scale.
| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| BTN-01 | Size scale | height XS 32, S 40, M 56, L 96, XL 136dp; small is default | C | components/buttons/specs@2026-07-24 |
| BTN-02 | Padding and icon | leading=trailing space 12/16/24/48/64dp; icon 20/20/24/32/40dp | C | components/buttons/specs@2026-07-24 |
| BTN-03 | Shape | round = full; square = 12/12/16/28/28dp (XS to XL); pressed 8/8/12/16/16dp for both shapes | C | components/buttons/specs@2026-07-24 |
| BTN-04 | Color roles by style | filled primary; tonal secondary-container; elevated surface-container-low; outlined outline-variant; text no container | C | components/buttons/specs@2026-07-24 |
| BTN-05 | Disabled | label and icon on-surface at 0.38; container on-surface at 0.1 | C | components/buttons/specs@2026-07-24 |
| BTN-06 | Label | 1-3 words, sentence case, single line, not truncated | C | components/buttons/guidelines@2026-07-24 |
| BTN-07 | Emphasis | filled for the single primary action; text for lowest priority; one high-emphasis button per screen | C | components/all-buttons@2026-07-17 |
| BTN-08 | Contrast | 3:1 vs background (container or label per style) | F | components/buttons/accessibility@2026-07-24 |
| BTN-09 | Target | XS and S buttons need 48x48dp hit area | F | components/buttons/specs@2026-07-24 |
| BTN-10 | Sizes and shapes beyond default | XS, M-XL sizes, square shape, toggle morph | E | components/buttons/overview@2026-07-24 |
| BTN-11 | Toggle colors | selected: elevated/filled primary + on-primary, tonal secondary + on-secondary, outlined inverse-surface + inverse-on-surface; filled unselected surface-container + on-surface-variant; no text toggle | E | components/buttons/specs@2026-07-24 |
| BTN-12 | Icon count and placement | at most one icon, on the leading side, grouped and centered with the label; never stacked above it | C | components/buttons/guidelines@2026-07-24 |
| BTN-13 | Icon-label gap | XS 4, S 8, M 8, L 12, XL 16dp | C | components/buttons/specs@2026-07-24 |

## Cards
**Use:** Container for content and actions about one subject; elevated, filled or outlined.
**Dimensions & shape:** Corner medium (12dp); left/right padding 16dp; gap between cards 8dp max; icon 24dp; outlined stroke 1dp; size follows content.
**Color roles:** elevated surface-container-low, level1; filled surface-container-highest, level0; outlined surface with outline-variant stroke, level0. Hover +1 elevation (elevated: level2; filled: level1); dragged level4 (elevated) / level3 (filled). Disabled 0.38.
**Do / Don't:**
- Do give one clear hierarchy of headline, subhead, supporting text.
- Do keep cards in a collection at the same resting elevation.
- Do put sort/filter controls outside the collection.
- Don't put text or icons on images without a scrim or enough contrast.
- Don't stack actionable elements inside an actionable card.
- Don't scroll content inside a card on mobile; expand the card instead.
**Accessibility:**
- Dragging/swiping needs a menu alternative.
- Only actionable cards ripple, hover and take focus; non-actionable cards expose their inner controls.
**Review checks:** one of three variants; medium corner; no nested tap targets; text over images has a scrim.
| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| CRD-01 | Variants | elevated, filled or outlined only; same function, style choice | C | components/cards/guidelines@2026-07-24 |
| CRD-02 | Container colors | elevated surface-container-low; filled surface-container-highest; outlined surface + 1dp outline-variant | C | components/cards/specs@2026-07-24 |
| CRD-03 | Shape and elevation | corner medium; rest level1 (elevated) / level0 (filled, outlined) | C | components/cards/specs@2026-07-24 |
| CRD-04 | Text over image | avoid; if used add scrim/shape for text contrast | F | components/cards/guidelines@2026-07-24 |
| CRD-05 | Drag/swipe alternative | single-pointer alternative (menu) | F | components/cards/accessibility@2026-07-24 |
| CRD-06 | No stacked actionables | actionable card holds no buttons/links; otherwise card is non-actionable | F | components/cards/accessibility@2026-07-24 |
| CRD-07 | Padding and spacing | left/right padding 16dp; at most 8dp between cards; label text start-aligned | C | components/cards/specs@2026-07-24 |
| CRD-08 | Scroll and swipe | no internal scroll on mobile (desktop may); one swipe action per card; no swipeable content (carousel, pagination) inside a card | C | components/cards/guidelines@2026-07-24 |

## Carousel
**Use:** Scrollable row of visual items; multi-browse, uncontained, uncontained multi-aspect, hero, center-aligned hero, full-screen.
**Dimensions & shape:** Item corner extra-large 28dp; small items 40-56dp wide; padding 16dp leading/trailing (uncontained: leading only), 8dp top/bottom, 8dp between items; full-screen 0dp padding, 16dp between items; compact windows show up to 3 items; uncontained multi-aspect widths 9:16 to 16:9.
**Color roles:** item container surface, level0; outline variant outline 1dp; focus indicator secondary.
**Do / Don't:**
- Do use snap-scrolling for multi-browse, hero, full-screen; default scroll for uncontained.
- Do keep item text brief; use uncontained or cards for text-heavy items.
- Do provide a Show all button (or header arrow) on vertically scrolling pages.
- Don't use full-screen layout in landscape.
- Don't add arrows beside the carousel as the accessible alternative.
**Accessibility:**
- Tab/arrows move between items; Space/Enter activates; up/down leave the carousel.
- Reduced motion removes parallax and size changes (all items equal size).
**Review checks:** Show all present; at most 3 text items in compact; snap behavior matches layout; corners 28dp.
| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| CAR-01 | Show-all alternative | vertical-scroll pages need Show all button or header arrow (not full-screen) | F | components/carousel/accessibility@2026-08-18 |
| CAR-02 | Item shape | corner extra-large; container surface | C | components/carousel/specs@2026-08-18 |
| CAR-03 | Small item width | 40-56dp | C | components/carousel/guidelines@2026-08-18 |
| CAR-04 | Compact item count | up to 3 items with text | C | components/carousel/guidelines@2026-08-18 |
| CAR-05 | Scroll mode | snap for multi-browse/hero/full-screen (full-screen must snap); default scroll only for uncontained, which may also snap | C | components/carousel/guidelines@2026-08-18 |
| CAR-06 | Reduced motion | no parallax, uniform item size | F | components/carousel/accessibility@2026-08-18 |
| CAR-07 | Layout padding | 16dp leading/trailing (uncontained: leading only), 8dp top/bottom, 8dp between items; full-screen 0dp padding, 16dp between items | C | components/carousel/specs@2026-08-18 |
| CAR-08 | Focus and labels | initial focus on first item, never the container; item label states position and total count | F | components/carousel/accessibility@2026-08-18 |

## Checkbox
**Use:** Select several options, sub-selections, or toggle in desktop contexts.
**Dimensions & shape:** Box 18dp, 2dp corner, unselected outline 2dp, state layer 40dp circle; target 48x48.
**Color roles:** selected container primary, check on-primary; unselected outline on-surface-variant; error container/outline error; disabled 0.38. Adjacent label on-surface in every state.
**Do / Don't:**
- Do use checkboxes (not switches) for multiple related options.
- Do make label clickable as well as the box.
- Do show indeterminate on a parent with mixed children.
- Don't apply compact density by default.
- Don't delay the effect when it toggles a setting.
**Accessibility:**
- Parent has three states; checking indeterminate checks all children.
- Targets at least 48x48 CSS px.
**Review checks:** 18dp box; error state exists; tri-state parent; label linked; target 48px.
| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| CHK-01 | Box geometry | 18dp box, 2dp corner, 2dp unselected outline, 40dp state layer | C | components/checkbox/specs@2026-08-12 |
| CHK-02 | Colors | selected primary + on-primary icon; unselected outline on-surface-variant; error uses error/on-error | C | components/checkbox/specs@2026-08-12 |
| CHK-03 | Target size | 48x48 CSS px; no default density reduction | F | components/checkbox/accessibility@2026-08-12 |
| CHK-04 | Parent-child | indeterminate when some children checked; checking it checks all | C | components/checkbox/guidelines@2026-08-12 |
| CHK-05 | Label hit area | label and box both toggle | F | components/checkbox/accessibility@2026-08-12 |
| CHK-06 | Label color | adjacent text label on-surface, unchanged by selection or interaction | C | components/checkbox/specs@2026-08-12 |

## Chips
**Use:** Context options: assist, filter, input, suggestion.
**Dimensions & shape:** Height 32dp; corner small 8dp; icon 18dp, avatar 24dp; side padding 16dp (8dp with icon); chip gap at least 8dp; target at least 48dp (may extend past container); label at most 20 characters, button typography.
**Color roles:** outline outline-variant (flat); elevated chips surface-container-low; selected filter secondary-container with on-secondary-container label; unselected filter label on-surface-variant; leading icon primary.
**Do / Don't:**
- Do write assist chips as verbs, filter chips as nouns.
- Do keep one select behavior (single or multi) per page.
- Do add a checkmark on selected filter chips.
- Do show chips in a set, never a single chip alone.
- Don't use chips for persistent/linear actions; use buttons.
- Don't show a trailing icon in compact windows if its target is under 48dp.
- Don't elevate chips placed directly on the page, or to show pressed state.
**Accessibility:**
- Label at least 3:1 contrast; chips need a secondary interactivity cue.
- Offer a reflow or menu alternative to horizontal-only overflow.
**Review checks:** 32dp tall, 8dp corner; gap 8dp; labels short; selected state distinct and not color-only.
| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| CHP-01 | Geometry | height 32dp, corner small 8dp, icon 18dp | C | components/chips/specs@2026-07-17 |
| CHP-02 | Spacing | at least 8dp between chips | C | components/chips/guidelines@2026-07-17 |
| CHP-03 | Target | 48dp minimum, no default density | F | components/chips/accessibility@2026-07-17 |
| CHP-04 | Label | at most 20 chars; contrast at least 3:1 | F | components/chips/guidelines@2026-07-17, components/chips/accessibility@2026-07-17 |
| CHP-05 | Selected filter | secondary-container fill, on-secondary-container label, leading check. A chip row that switches views instead of filtering is judged by CMP-01 | C | components/chips/specs@2026-07-17 |
| CHP-06 | Select mode | one behavior per page, single or multi | C | components/chips/guidelines@2026-07-17 |
| CHP-07 | Input chip remove | required trailing remove icon with own 48dp target; chip min width 88dp (or label 42dp) so both targets fit | C | components/chips/guidelines@2026-07-17 |
| CHP-08 | Interactivity cue | at least one secondary cue: intro label (e.g. Select type), page context, outline role instead of outline-variant (3:1), or action label/leading icon | F | components/chips/accessibility@2026-07-17 |
| CHP-09 | Elevation use | elevate only over images or dynamic backgrounds; never on plain page or as pressed state (use ripple) | C | components/chips/guidelines@2026-07-17 |

## Date pickers
**Use:** Pick a date or range; docked, modal, modal input.
**Dimensions & shape:** Docked 360x456dp, corner large; modal 360x524dp, corner extra-large, header 120dp (range 128); date cell 48dp docked / 40dp modal; year cell 72x36dp.
**Color roles:** container surface-container-high; selected date primary; range fill secondary-container.
**Do / Don't:**
- Do offer text entry plus calendar.
- Do use docked or modal input for far-past dates (e.g. birth dates).
- Do recommend full-screen modal on compact windows.
- Don't scale the picker with window size.
- Don't auto-insert slashes while typing.
**Accessibility:**
- Date text contrast at least 4.5:1; 48dp targets.
- Accept varied formats; helper text states format; label names the purpose.
**Review checks:** manual input path; 48dp cells in docked; selected date visible by color plus shape; format helper.
| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| DTP-01 | Sizes | docked 360x456dp; modal 360x524dp | C | components/date-pickers/specs@2026-10-22 |
| DTP-02 | Container | surface-container-high; docked corner large, modal extra-large | C | components/date-pickers/specs@2026-10-22 |
| DTP-03 | Date cell | docked 48dp; modal 40dp visual, 48dp target | C | components/date-pickers/specs@2026-10-22 |
| DTP-04 | Date contrast | at least 4.5:1 | F | components/date-pickers/accessibility@2026-10-22 |
| DTP-05 | Text entry | typed entry always available; format helper text | F | components/date-pickers/accessibility@2026-10-22 |
| DTP-06 | Far dates | no plain modal calendar for distant dates | C | components/date-pickers/guidelines@2026-10-22 |
| DTP-07 | Typed date format | format only after Enter or leaving the field, no input masks; accept dashes, spaces, slashes, dots and leading zeros; text field and calendar icon are separate tab stops | F | components/date-pickers/accessibility@2026-10-22 |

## Dialogs
**Use:** Interrupt for a decision or critical info; basic or full-screen (compact only).
**Dimensions & shape:** Basic: corner 28dp, width 280-560dp, padding 24dp, title-body and icon-title gap 16dp, body-actions gap 24dp, button gap 8dp, icon 24dp. Full-screen: header and action bar 56dp, corner 0, close icon 24dp, max width 560dp. Custom placement on large screens keeps 56dp from edges.
**Color roles:** container surface-container-high, level3; headline on-surface; supporting text on-surface-variant; icon secondary; buttons primary; full-screen container, header and action bar surface (header surface-container on scroll).
**Do / Don't:**
- Do use at most two actions, trailing aligned, confirm nearest the edge.
- Do state the specific verb (Send, Delete), not OK.
- Do pin title and buttons when content scrolls.
- Don't use vague or alarmist headlines ("Warning!", "Are you sure?").
- Don't add a third action such as Learn more.
- Don't use for low-importance messages; use a snackbar.
**Accessibility:**
- Focus to first interactive element; Tab cycles inside; Esc closes.
- Web basic dialog role: alert dialog; label equals title.
**Review checks:** 28dp corner and scrim; at most two actions; width in range; text buttons trailing.
| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| DLG-01 | Basic container | surface-container-high, level3, corner 28dp | C | components/dialogs/specs@2026-07-28 |
| DLG-02 | Basic layout | width 280-560dp; padding 24dp; title-body and icon-title 16dp; body-actions 24dp; button gap 8dp | C | components/dialogs/specs@2026-07-28 |
| DLG-03 | Actions | max two; trailing aligned; confirm closest to edge; single action = acknowledge | C | components/dialogs/guidelines@2026-07-28 |
| DLG-04 | Scrim | content behind scrimmed; modal blocks app | C | components/dialogs/guidelines@2026-07-28 |
| DLG-05 | Full-screen | compact windows only; header/action bar 56dp; close X only nav | C | components/dialogs/guidelines@2026-07-28 |
| DLG-06 | Focus and keys | initial focus first control; Tab loops; Esc closes | F | components/dialogs/accessibility@2026-07-28 |
| DLG-07 | Headline wording | brief; no apologies, alarm or "Are you sure?" | C | components/dialogs/guidelines@2026-07-28 |
| DLG-08 | Disabled actions | basic: confirm may stay disabled until a choice is made, dismiss never disabled; full-screen: never disable the confirm (Save) action | C | components/dialogs/guidelines@2026-07-28 |
| DLG-09 | Scrolling content | avoid scrolling; if needed, title pinned top and buttons pinned bottom; dialog never scrolls with the background | C | components/dialogs/guidelines@2026-07-28 |

## Divider
**Use:** Thin line grouping content; full-width or inset, horizontal or vertical.
**Dimensions & shape:** Thickness 1dp; inset 16dp leading, 0dp trailing; middle-inset 16dp both sides; 4dp from supporting text.
**Color roles:** outline-variant.
**Do / Don't:**
- Do use only when whitespace can't group items.
- Do use full-width between content types, inset between nested items.
- Don't separate every individual item.
- Don't make dividers bold.
**Accessibility:**
- Decorative; no contrast minimum.
**Review checks:** 1dp, outline-variant; not between every row; full vs inset used consistently.
| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| DIV-01 | Line spec | 1dp thick, outline-variant | C | components/divider/specs@2026-07-17 |
| DIV-02 | Usage | group content; prefer spacing; full-width for sections, inset for nested items | C | components/divider/guidelines@2026-07-17 |
| DIV-03 | Contrast | decorative, no contrast minimum | C | components/divider/accessibility@2026-07-17 |
| DIV-04 | Inset margins | inset 16dp leading / 0dp trailing; middle-inset 16dp both sides; full-width 100% | C | components/divider/specs@2026-07-17 |
