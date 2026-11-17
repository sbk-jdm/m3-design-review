# Material 3 components, part 2 (FABs to radio button)

Snapshot date: 2026-05-21. Base URL: https://m3.material.io/
A source `path` maps to `https://m3.material.io/<path>` (use the page's `source_url` when in doubt).
Distilled from Material Design 3 documentation (Apache 2.0 / CC BY 4.0); see NOTICE.md.
On the web, 1dp is treated as 1 CSS px. Tiers: F = floor, C = core M3, E = Expressive-only/optional/platform-specific.
Corner tokens: extra-small 4dp, small 8dp, medium 12dp, large 16dp, large-increased 20dp, extra-large 28dp (full = pill).

## Extended FAB
**Use:** One prominent labeled primary action floating over long or scrolling content.
**Dimensions & shape:** Baseline 56dp high, corner large. Expressive: small 56 (title-medium, icon 24, pad 16, gap 8); medium 80 (title-large, icon 28, corner large-increased, pad 26, gap 12); large 96 (headline-small, icon 36, corner extra-large, pad 28, gap 16). Width hugs content.
**Color roles:** primary-container/on-primary-container (or secondary/tertiary sets, or solid primary/on-primary); level3, hover level4.
**Do / Don't:**
- Do use one per screen with a 1-2 word label.
- Do mirror icon and label in RTL.
- Don't use it as one option in a button set (use filled button) or on cards, toolbars, or the upper half of a phone.
- Don't wrap or truncate the label; no icon-only variant.
**Accessibility:**
- Icon and label are one focus target; no tooltip needed.
- Accessible name starts with the visible label's first word.
- Never cover another actionable element.
**Review checks:** one extended FAB; label one line; height 56/80/96; bottom placement.
| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| EFB-01 | Container height | 56dp baseline; Expressive small 56 / medium 80 / large 96 | C | components/extended-fab/specs@2026-05-18 |
| EFB-02 | Label type role | small title-medium; medium title-large; large headline-small | C | components/extended-fab/specs@2026-05-18 |
| EFB-03 | Count and combos | one per screen; not with a floating toolbar | C | components/extended-fab/guidelines@2026-05-18 |
| EFB-04 | Label | 1-2 words, no wrap or truncation; icon only alongside text | C | components/extended-fab/guidelines@2026-05-18 |
| EFB-05 | Placement | compact/medium bottom (centered or trailing); expanded bottom-right or top of expanded rail | C | components/extended-fab/guidelines@2026-05-18 |
| EFB-06 | Accessible name | begins with the visible label word | F | components/extended-fab/accessibility@2026-05-18 |

## FAB menu
**Use:** Reveals 2-6 closely related actions from a FAB.
**Dimensions & shape:** Close button 56x56dp, icon 20, pill, level3. Items 56dp high, icon 24, pill, pad 24, icon gap 8, 4dp between items, hug content. Margins 16dp (24 on large windows).
**Color roles:** close button primary/on-primary (or secondary, tertiary); items primary-container/on-primary-container in the matching set.
**Do / Don't:**
- Do open it in place of the FAB, trailing-edge aligned.
- Don't open from an extended FAB, or pair with a floating toolbar or rail.
- Don't drop item icons or truncate labels.
**Accessibility:**
- All targets at least 48dp.
- Initial focus on close button, then items top to bottom.
- Close button labeled with expanded/collapsed state.
**Review checks:** 2-6 items, each with icon and label; color set matches FAB.
| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| FBM-01 | Item count | 2-6 related actions | C | components/fab-menu/guidelines@2026-05-18 |
| FBM-02 | Origin | from a FAB only; not extended FAB; no floating toolbar/rail pairing | C | components/fab-menu/guidelines@2026-05-18 |
| FBM-03 | Sizes | item 56dp; close button 56dp square, icon 20dp; pill shapes | C | components/fab-menu/specs@2026-05-18 |
| FBM-04 | Color set | primary/secondary/tertiary FAB styles use the same menu set | C | components/fab-menu/guidelines@2026-05-18 |
| FBM-05 | Min target | at least 48dp; focus close button first | F | components/fab-menu/accessibility@2026-05-18 |

## Floating action button
**Use:** The single most important constructive action on a screen.
**Dimensions & shape:** FAB 56x56dp, icon 24, corner large; medium 80 (icon 28, corner large-increased, most recommended); large 96 (icon 36, corner extra-large). Small 40dp is discouraged.
**Color roles:** primary-container/on-primary-container (or secondary/tertiary container, or solid); level3, hover level4.
**Do / Don't:**
- Do use for create, share, favorite, start a process; filled icon; tooltip on web.
- Don't use for minor or destructive actions (archive, trash, alerts).
- Don't disable it; hide it if unavailable.
- Don't animate it with body content when switching tabs.
**Accessibility:**
- Icon at least 3:1 against container.
- Accessible name describes the action.
- Do not fully hide another focus indicator.
**Review checks:** one FAB; lower right on compact/medium; not covered by badges.
| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| FAB-01 | Sizes | 56 / 80 / 96dp square | C | components/floating-action-button/specs@2026-05-18 |
| FAB-02 | Size by window | FAB or medium on compact/medium; large on expanded+ | E | components/floating-action-button/guidelines@2026-05-18 |
| FAB-03 | Purpose | one constructive primary action; no destructive actions | C | components/floating-action-button/guidelines@2026-05-18 |
| FAB-04 | Icon contrast | at least 3:1 with container | F | components/floating-action-button/accessibility@2026-05-18 |
| FAB-05 | Never disabled | remove when action unavailable | F | components/floating-action-button/accessibility@2026-05-18 |
| FAB-06 | Placement | lower right on compact/medium; may sit top-left in rail on expanded | C | components/floating-action-button/guidelines@2026-05-18 |

## Icon buttons
**Use:** Common actions (default) or on/off actions (toggle) shown as an icon.
**Dimensions & shape:** Heights: xsmall 32 (icon 20), small 40 default (24), medium 56 (24), large 96 (32), xlarge 136 (40). Widths narrow/default/wide (small padding 4/8/14dp). Round = full corner; square = medium (xs, s), large (m), extra-large (l). Selected toggle swaps shape. Touch target at least 48x48dp.
**Color roles:** filled primary/on-primary (unselected toggle surface-container); tonal secondary-container/on-secondary-container; outlined outline-variant border, on-surface-variant icon; standard on-surface-variant (selected primary).
**Do / Don't:**
- Do use filled sparingly; give equal-priority buttons equal size.
- Do use outlined icon unselected, filled icon selected.
- Don't signal selection by color alone; use fill or heavier weight.
- Don't apply density by default (targets below 48dp).
**Accessibility:**
- Icon at least 3:1 against surface.
- Name describes the action; tooltip on web hover.
- Tab focuses, Space/Enter activates.
**Review checks:** target at least 48px; toggle state differs beyond color; accessible name present.
| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| ICB-01 | Sizes | container 32 / 40 / 56 / 96 / 136dp; icon 20 / 24 / 24 / 32 / 40dp | C | components/icon-buttons/specs@2026-02-11 |
| ICB-02 | Target size | at least 48x48dp even when nested | F | components/icon-buttons/accessibility@2026-02-11 |
| ICB-03 | Icon contrast | at least 3:1 with surface | F | components/icon-buttons/accessibility@2026-02-11 |
| ICB-04 | Toggle cue | selected shown by filled icon or heavier weight plus color | F | components/icon-buttons/guidelines@2026-02-11 |
| ICB-05 | Emphasis order | filled > tonal > outlined > standard | C | components/icon-buttons/guidelines@2026-02-11 |
| ICB-06 | Accessible name | action label, not icon name; tooltip on web | F | components/icon-buttons/accessibility@2026-02-11 |

## Lists
**Use:** Vertical scannable items with text, media, and optional actions.
**Dimensions & shape:** Item height 56 (one line), 72 (two), 88dp (three). Padding 16dp, gap 12. Icon 24, avatar 40 (full), image 56x56, video 100x56. Divider 1dp; segmented gap 2dp, container corner large.
**Color roles:** surface container; label on-surface (body-large); supporting on-surface-variant (body-medium); trailing label-small; selected secondary-container/on-secondary-container; divider outline.
**Do / Don't:**
- Do keep visuals and text in the same position in every item.
- Do limit supporting text to 1-3 lines.
- Do use gaps for contained lists, dividers only if needed.
- Don't mix checkboxes into single-select or radios into multi-select; no nested actions there.
**Accessibility:**
- Selection needs a non-color cue.
- Arrow keys move (wrap); Space/Enter activates; selected item focused first.
- Web selectable list: listbox container, option items.
**Review checks:** heights from the set; consistent alignment; selection visible without color.
| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| LST-01 | Item height | 56 / 72 / 88dp for 1 / 2 / 3 lines | C | components/lists/specs@2026-05-18 |
| LST-02 | Type roles | label body-large; supporting body-medium; trailing label-small | C | components/lists/specs@2026-05-18 |
| LST-03 | Spacing | 16dp side padding; 12dp gap; media icon 24, avatar 40, image 56 | C | components/lists/specs@2026-05-18 |
| LST-04 | Selection cue | not color alone: radio/checkbox, icon, or non-color style | F | components/lists/accessibility@2026-05-18 |
| LST-05 | Control match | radio = single, checkbox/switch = multi | C | components/lists/guidelines@2026-05-18 |
| LST-06 | Separators | 2dp gaps if contained; 1dp dividers if uncontained | C | components/lists/specs@2026-05-18 |
| LST-07 | Keyboard | arrows navigate with wrap; Space/Enter activate | F | components/lists/accessibility@2026-05-18 |

## Loading indicator
**Use:** Expressive morphing-shape indicator for short waits (200ms-5s). Expressive only.
**Dimensions & shape:** Container 48x48dp, indicator 38dp; resizable 24-240dp, ratio fixed; seven-shape morph.
**Color roles:** default: indicator primary, no container; contained: primary-container with on-primary-container indicator.
**Do / Don't:**
- Do show the container over other content and with pull-to-refresh.
- Do center it on the loading element.
- Don't show under 200ms; use progress indicator over 5s.
- Don't morph it into a progress indicator.
**Accessibility:**
- Indicator at least 3:1 against background.
- Progress bar role with purpose label.
- Pull-to-refresh needs a non-gesture alternative.
**Review checks:** size 24-240dp; short waits only; label present.
| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| LDI-01 | Size | 48dp container, 38dp indicator; 24-240dp allowed | E | components/loading-indicator/specs@2026-02-05 |
| LDI-02 | Wait time | under 200ms none; 200ms-5s loading; over 5s progress indicator | C | components/loading-indicator/guidelines@2026-02-05 |
| LDI-03 | Contained colors | primary-container with on-primary-container | E | components/loading-indicator/specs@2026-02-05 |
| LDI-04 | Contrast | indicator at least 3:1 | F | components/loading-indicator/accessibility@2026-02-05 |
| LDI-05 | Label | progress bar role, names the process | F | components/loading-indicator/accessibility@2026-02-05 |

## Menus
**Use:** Temporary list of actions or choices from a trigger.
**Dimensions & shape:** Item height M3 48dp / Expressive 44dp; pad 16dp sides, icons 20, label-large; level2. M3 container corner extra-small, divider 1dp; Expressive corner large, gap 2dp.
**Color roles:** standard surface-container-low (M3 surface-container), label on-surface, icons on-surface-variant, selected tertiary-container/on-tertiary-container; vibrant tertiary-container with tertiary selected.
**Do / Don't:**
- Do group with a divider or 1-2 gaps; no gaps in scrolling menus.
- Do show unavailable items disabled, not removed.
- Don't put buttons or switches in items.
- Don't overuse vibrant.
**Accessibility:**
- Focus first item on open; Esc/outside/back closes.
- Selected items need 3:1 plus a cue like a check.
- Disabled items focusable; dividers not.
**Review checks:** selection cue; disabled not hidden; no nested buttons; stays on screen.
| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| MNU-01 | Item size | M3 48dp / Expressive 44dp; 16dp padding; icon 20; label-large | C | components/menus/specs@2026-05-18 |
| MNU-02 | Container | M3 corner 4dp; Expressive corner large; level2 | C | components/menus/specs@2026-05-18 |
| MNU-03 | Vibrant | tertiary mapping is high emphasis; use sparingly | E | components/menus/guidelines@2026-05-18 |
| MNU-04 | Selected cue | 3:1 color difference plus second cue | F | components/menus/accessibility@2026-05-18 |
| MNU-05 | Slots | targets at least 48dp; one action per item | F | components/menus/accessibility@2026-05-18 |
| MNU-06 | Focus | first item on open; Escape, outside tap or back closes; focus return and containment: A11-34 | F | components/menus/accessibility@2026-05-18 |

## Navigation bar
**Use:** Bottom switcher for 3-5 top-level destinations on compact and medium windows.
**Dimensions & shape:** Baseline M3: container 80dp, indicator 64x32dp pill, icon 24, label-medium, gap 4. Expressive flexible: container 64dp; vertical indicator 56x32dp (label gap 6); horizontal item indicator 40dp high, 16dp side padding. Full width, square corners, level2. Baseline bar not recommended in Expressive.
**Color roles:** container surface-container; indicator secondary-container; active icon on-secondary-container; inactive on-surface-variant; active label on-surface (baseline) or secondary (flexible); badge error.
**Do / Don't:**
- Do give each item an icon and 1-2 word label; filled icon plus bold label when active.
- Don't use for fewer than 3 or over 5 destinations.
- Don't swipe between destinations or hide on scroll with a screen reader.
- Don't use on expanded windows (use a rail).
**Accessibility:**
- Icons 3:1 against container.
- Full labels visible to 2x text size.
- Initial focus on first item.
**Review checks:** 3-5 items; one active; labels on all; heights match variant.
| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| NVB-01 | Count | 3-5 items, exactly one active | C | components/navigation-bar/guidelines@2026-05-18 |
| NVB-02 | Container height | M3 80dp; Expressive flexible 64dp | C | components/navigation-bar/specs@2026-05-18 |
| NVB-03 | Indicator | M3 64x32dp; flexible vertical 56x32dp; horizontal 40dp high | C | components/navigation-bar/specs@2026-05-18 |
| NVB-04 | Active vs inactive | filled icon + bold label vs outlined icon + medium label | C | components/navigation-bar/accessibility@2026-05-18 |
| NVB-05 | Icon contrast | at least 3:1 with container | F | components/navigation-bar/guidelines@2026-05-18 |
| NVB-06 | Window class | compact and medium only; vertical items compact, horizontal medium | C | components/navigation-bar/guidelines@2026-05-18 |
| NVB-07 | Text scaling | label fully visible to 2x | F | components/navigation-bar/accessibility@2026-05-18 |
| NVB-08 | No swipe between destinations | Swiping the screen does not move between navigation bar destinations; keep swipe for related items (carousel cards) or item actions (archive). Swiping between tab panels is a tabs behavior, not this | C | components/navigation-bar/guidelines@2026-05-18 |
| NVB-09 | Color roles | container surface-container; active indicator secondary-container; active icon on-secondary-container; inactive icon and label on-surface-variant; active label secondary (flexible, `md.comp.nav-bar`) or on-surface (baseline, `md.comp.navigation-bar`); focus indicator secondary (baseline token) | C | components/navigation-bar/specs@2026-05-18 |

## Navigation drawer
**Use:** Side destination list for 5+ destinations or deep hierarchy. Not recommended in Expressive (use expanded rail).
**Dimensions & shape:** Width 360dp, full height; modal corner large on end side; active indicator 336x56dp pill; icon 24; label-large; headline title-small. Start edge.
**Color roles:** standard surface (level0); modal surface-container-low (level1) with scrim; active indicator secondary-container, on-secondary-container content; inactive on-surface-variant; divider outline.
**Do / Don't:**
- Do use modal drawers on compact/medium, standard on expanded+.
- Don't combine with a navigation bar.
- Don't cut off labels; icons before text.
**Accessibility:**
- Scrim tap, item select, or swipe closes modal.
- Initial focus first item; arrows move.
- Filled icon marks selection.
**Review checks:** width 360; indicator 56 high; one active; scrim on modal.
| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| NVD-01 | Size | sheet 360dp wide; indicator 336x56dp | C | components/navigation-drawer/specs@2026-05-18 |
| NVD-02 | Variant | modal compact/medium; standard expanded and larger | C | components/navigation-drawer/guidelines@2026-05-18 |
| NVD-03 | Single primary nav | not combined with a navigation bar | C | components/navigation-drawer/guidelines@2026-05-18 |
| NVD-04 | Container color | modal surface-container-low; standard surface | C | components/navigation-drawer/specs@2026-05-18 |
| NVD-05 | Selected cue | filled icon plus indicator | F | components/navigation-drawer/accessibility@2026-05-18 |
| NVD-06 | Expressive | replaced by expanded navigation rail | E | components/navigation-drawer/guidelines@2026-05-18 |

## Navigation rail
**Use:** Vertical leading-edge navigation for medium and larger windows.
**Dimensions & shape:** Baseline M3: 80dp wide, indicator 32dp high (56 without label), icon 24. Expressive collapsed: 96dp wide (narrow 80), top space 44, items 64 (short 56), vertical indicator 56x32; expanded: 220-360dp, horizontal indicator 56dp high, 16dp padding, gap 8; modal corner large, level2.
**Color roles:** surface (modal surface-container); indicator secondary-container; active icon on-secondary-container; inactive on-surface-variant; active label on-surface (baseline) or secondary.
**Do / Don't:**
- Do put 3-7 destinations in the collapsed rail; menu and FAB top-aligned.
- Don't hide the collapsed rail or lay it out horizontally.
- Don't use on compact windows.
- Don't use a logo as the menu button.
**Accessibility:**
- Labels visible to 2x text size.
- Initial focus on first interactive item.
- Without fill, items need 3:1.
**Review checks:** leading edge; 3-7 items; one-word labels; one active.
| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| NVR-01 | Collapsed width | M3 80dp; Expressive 96dp (narrow 80) | C | components/navigation-rail/specs@2026-05-18 |
| NVR-02 | Expanded width | 220-360dp | E | components/navigation-rail/specs@2026-05-18 |
| NVR-03 | Indicator | M3 32dp high (56 no label); Expressive 56x32 vertical | C | components/navigation-rail/specs@2026-05-18 |
| NVR-04 | Items | 3-7 in collapsed rail; one-word label each | C | components/navigation-rail/guidelines@2026-05-18 |
| NVR-05 | Window class | medium and larger; compact uses bar | C | components/navigation-rail/guidelines@2026-05-18 |
| NVR-06 | Active state | filled icon plus indicator | C | components/navigation-rail/accessibility@2026-05-18 |
| NVR-07 | Text scaling | full label at 2x | F | components/navigation-rail/accessibility@2026-05-18 |

## Progress indicators
**Use:** Status of longer (over 5s) processes, linear or circular.
**Dimensions & shape:** Linear 4dp (thick 8); wavy 10 (thick 14), wave 3dp / 40dp. Circular 40dp (wavy 48, thick 52), stroke 4dp (thick 8), 24-240dp. Track gap 4dp; stop dot 4dp. Baseline circular 48dp. Linear host at least 40dp, 4dp end padding.
**Color roles:** indicator primary; track secondary-container (baseline surface-container-highest); stop dot primary.
**Do / Don't:**
- Do use one indicator for a group; same variant for the same process.
- Do switch to determinate when progress is known.
- Don't keep the track in buttons.
- Don't misstate determinate progress.
**Accessibility:**
- Indicator at least 3:1 against background.
- Stop dot required if track under 3:1.
- Progress bar role, label names process.
**Review checks:** thickness from set; stop dot where track faint; label present.
| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| PRG-01 | Linear | height 4dp (thick 8); wavy 10 (thick 14) | C | components/progress-indicators/specs@2026-02-27 |
| PRG-02 | Circular | 40dp (wavy 48, thick 52), stroke 4dp | C | components/progress-indicators/specs@2026-02-27 |
| PRG-03 | Stop dot | 4dp at end of linear determinate if track under 3:1 | F | components/progress-indicators/guidelines@2026-02-27 |
| PRG-04 | Contrast | indicator at least 3:1 | F | components/progress-indicators/accessibility@2026-02-27 |
| PRG-05 | Wait time | over 5s progress; 200ms-5s loading; under 200ms none | C | components/progress-indicators/guidelines@2026-02-27 |
| PRG-06 | In buttons | indicator in label color, no track | F | components/progress-indicators/accessibility@2026-02-27 |
| PRG-07 | Label | progress bar role with process and content | F | components/progress-indicators/accessibility@2026-02-27 |

## Radio button
**Use:** Choose exactly one option from five or fewer visible options.
**Dimensions & shape:** Icon 20dp, state layer 40dp, target at least 48x48dp; always an adjacent label.
**Color roles:** selected primary; unselected on-surface-variant; state layers primary or on-surface.
**Do / Don't:**
- Do stack vertically; click on label selects.
- Do offer a none option if opt-out is needed.
- Don't use for multi-select or nest.
- Don't apply density by default.
**Accessibility:**
- Tab enters at selected or first; arrows move and select; Space selects.
- Radio group role with title label.
- Targets at least 48x48 CSS px.
**Review checks:** visible label on each; max five; one selected or explicit none.
| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| RAD-01 | Geometry | icon 20dp, state layer 40dp, target 48dp | F | components/radio-button/specs@2026-02-16 |
| RAD-02 | Colors | selected primary; unselected on-surface-variant | C | components/radio-button/specs@2026-02-16 |
| RAD-03 | Label | each radio has adjacent text; label selects | F | components/radio-button/guidelines@2026-02-16 |
| RAD-04 | Count | five or fewer, vertical, single choice | C | components/radio-button/guidelines@2026-02-16 |
| RAD-05 | Keyboard | arrows move and select with wrap | F | components/radio-button/accessibility@2026-02-16 |
