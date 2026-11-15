# Material 3 components, part 3 (search to tooltips)

Snapshot date: 2026-05-21. Base URL: https://m3.material.io/
A source `path` maps to `https://m3.material.io/<path>` (use the page's `source_url` when in doubt).
Distilled from Material Design 3 documentation (Apache 2.0 / CC BY 4.0); see NOTICE.md.
On the web, 1dp is treated as 1 CSS px. Tiers: F = floor, C = core M3, E = Expressive-only/optional/platform-specific.
Corner tokens: extra-small 4dp, small 8dp, medium 12dp, large 16dp, extra-large 28dp (full = pill).

## Search
**Use:** Keyword entry with live suggestions/results (bar and view).
**Dimensions & shape:** Bar height 56dp, full (pill) corners, always the same shape focused or not. Margins: 24dp unfocused, 12dp focused. Baseline inner padding 16dp; Expressive contained 4dp (16dp with no actions). View header: 72dp full-screen, 56dp docked. Text body-large.
**Color roles:** Bar container surface-container-high, elevation level3 (baseline) or contained style; contained view background surface-container-low; input text and leading icon on-surface; hint and trailing icons on-surface-variant; divider (divided style) outline.
**Do / Don't:**
- Do use a short hint ("Search messages") and place it atop searched content.
- Do use full-screen results on compact, docked on larger windows.
- Don't put surface-container-high on a surface-container page.
- Don't exceed two trailing icons or reshape the bar on focus.
**Accessibility:**
- Hint is the accessible name; announce results as they appear.
**Review checks:** height 56 and pill; container role contrasts with page background; at most two trailing icons; hint present.

| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| SRC-01 | Search bar height and shape | 56dp, corner full | C | components/search/specs@2026-05-18 |
| SRC-02 | Container color role | surface-container-high, more than one step from page surface-container | C | components/search/guidelines@2026-05-18 |
| SRC-03 | Trailing icons | one or two; avatar plus at most one icon button | C | components/search/guidelines@2026-05-18 |
| SRC-04 | Focused layout by window | compact: full-screen; medium/expanded: docked with scrim | C | components/search/guidelines@2026-05-18 |
| SRC-05 | Margins | unfocused 24dp, focused 12dp (contained style) | E | components/search/guidelines@2026-05-18 |
| SRC-06 | Announce results to assistive tech; hint text is the label | required | F | components/search/accessibility@2026-05-18 |

## Segmented buttons (no longer recommended in Expressive; use connected button group)
**Use:** Choose among 2-5 short options (single-select) or filter with several on at once (multi-select).
**Dimensions & shape:** Height 40dp, outline 1dp, full corners, min side padding 12dp, 8dp between elements, icon 18dp, 48dp target. 2 to 5 segments. 
**Color roles:** outline `outline`; unselected label/icon on-surface; selected container secondary-container with on-secondary-container; state layers on-surface (unselected) or on-secondary-container (selected).
**Do / Don't:**
- Do show a check on selected segments.
- Do keep labels short, one line, one label type.
- Don't exceed five segments (use chips).
- Don't stretch to full width on large screens.
**Accessibility:**
- Outline 3:1; selection not color-only; behaves as radio group or checkboxes.
**Review checks:** 2-5 segments; 40dp tall; check mark on selected; outline contrast 3:1; no wrapped labels.

| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| SEG-01 | Segment count | 2 to 5 | C | components/segmented-buttons/guidelines@2026-05-18 |
| SEG-02 | Height and outline | 40dp tall, 1dp outline, full corners | C | components/segmented-buttons/specs@2026-05-18 |
| SEG-03 | Selected state | secondary-container fill, on-secondary-container content, check icon | C | components/segmented-buttons/specs@2026-05-18 |
| SEG-04 | Outline contrast vs surface | at least 3:1 | F | components/segmented-buttons/accessibility@2026-05-18 |
| SEG-05 | Selection not by color alone | check icon plus color change | F | components/segmented-buttons/accessibility@2026-05-18 |
| SEG-06 | Touch target | 48dp | F | components/segmented-buttons/specs@2026-05-18 |

## Side sheets
**Use:** Secondary content at a side edge; standard (medium/expanded) or modal (compact, blocks content).
**Dimensions & shape:** Default width 256dp, max width 400dp. Start/end padding 24dp (16dp start with icon), 12dp between top elements. Bottom actions area 72dp (16dp top, 24dp bottom padding). Detached margin 16dp. Corners: docked none; detached large (16dp).
**Color roles:** standard container surface; modal container surface-container-low; headline on-surface-variant; divider outline; action labels primary.
**Do / Don't:**
- Do include a close icon button.
- Do place on the right edge (left in RTL), scrolling vertically only.
- Don't scroll horizontally.
- Don't inset beyond 16dp.
**Accessibility:**
- Close affordance always present; role dialog.
**Review checks:** close button present; width at most 400dp; no horizontal scroll; modal has scrim.

| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| SSH-01 | Width | default 256dp, max 400dp | C | components/side-sheets/specs@2026-05-18 |
| SSH-02 | Close affordance always present | close icon button | F | components/side-sheets/accessibility@2026-05-18 |
| SSH-03 | Variant by window size | standard for medium/expanded; modal for compact | C | components/side-sheets/guidelines@2026-05-18 |
| SSH-04 | Padding | 24dp start/end, 12dp between top elements, actions area 72dp | C | components/side-sheets/specs@2026-05-18 |
| SSH-05 | Container color | standard surface; modal surface-container-low | C | components/side-sheets/specs@2026-05-18 |
| SSH-06 | No horizontal scrolling; inset at most 16dp | required | C | components/side-sheets/guidelines@2026-05-18 |

## Sliders
**Use:** Pick a value or range on a track, applied immediately; standard, centered, or range.
**Dimensions & shape:** Track height by size: XS 16, S 24, M 40, L 56, XL 96dp (active and inactive equal). Outer corner: XS/S 8, M 12, L 16, XL 28dp. Handle 4dp wide, height 44 (XS-S, M) / 68 (L) / 108dp (XL), full corners. Stop indicator 4dp circle. Inset icon 24dp (M, L) or 32dp (XL); icon padding 6 (8 for XL).
**Color roles:** active track and handle primary; inactive track secondary-container; active stop indicators on-primary; inactive stop indicators on-secondary-container.
**Do / Don't:**
- Do show the value while pressed; one at a time on range sliders.
- Do keep a linked text field in sync.
- Don't use inset icons on XS/S, centered, or range sliders.
- Don't use range sliders vertically or XL outside hero use.
**Accessibility:**
- Inactive-track end 3:1 vs background; arrows, Home/End work; role slider.
**Review checks:** track height; end of inactive track visible at 3:1.

| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| SLD-01 | Track height steps | XS 16, S 24, M 40, L 56, XL 96dp | E | components/sliders/specs@2026-05-08 |
| SLD-02 | Handle | 4dp wide, full corners, height 44dp (XS/S/M), 68 (L), 108 (XL); width narrows when pressed | C | components/sliders/specs@2026-05-08 |
| SLD-03 | Color roles | active primary; inactive secondary-container | C | components/sliders/specs@2026-05-08 |
| SLD-04 | Inactive-track end contrast | at least 3:1 with background | F | components/sliders/accessibility@2026-05-08 |
| SLD-05 | Inset icon only on standard M/L/XL | not on XS/S, centered, range | E | components/sliders/guidelines@2026-05-08 |
| SLD-06 | Keyboard | Tab to handle; arrows step; Home/End to ends | F | components/sliders/accessibility@2026-05-08 |

## Snackbar
**Use:** Short low-priority feedback at screen bottom; one at a time, one optional action.
**Dimensions & shape:** Height 48dp (one line) or 68dp (two lines); extra-small (4dp) corners; elevation level3; icon 24dp.
**Color roles:** container inverse-surface; text inverse-on-surface; action label inverse-primary (text button).
**Do / Don't:**
- Do show above FABs, clear of navigation.
- Do use one text action such as Undo.
- Don't stack or show several at once.
- Don't use filled buttons, icons, or links inside.
**Accessibility:**
- Actionable snackbars never auto-dismiss; polite announcement, no focus steal; Esc dismisses.
**Review checks:** container inverse-surface; single action; not covering nav/FAB.

| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| SNB-01 | Height and corners | 48dp one line, 68dp two lines; corner 4dp | C | components/snackbar/specs@2026-05-18 |
| SNB-02 | Colors | inverse-surface container, inverse-on-surface text, inverse-primary action | C | components/snackbar/specs@2026-05-18 |
| SNB-03 | One snackbar at a time; at most one action | required | C | components/snackbar/guidelines@2026-05-18 |
| SNB-04 | Auto-dismiss window | 4-10 s only without action; with action stays until acted on | F | components/snackbar/accessibility@2026-05-18 |
| SNB-05 | Focus and announcement | polite live region; do not move or trap focus | F | components/snackbar/accessibility@2026-05-18 |
| SNB-06 | Web auto-dismiss needs inline feedback | message also shown near trigger | F | components/snackbar/guidelines@2026-05-18 |

## Split button
**Use:** One main action plus a trailing menu of related actions (Expressive component).
**Dimensions & shape:** Container height XS 32, S 40 (default), M 56, L 96, XL 136dp. Gap between the two parts 2dp. Pill outer corners; inner corners extra-small, trailing button turns fully round (50%) when menu open. Trailing icon 22 (XS/S), 26 (M), 38 (L), 50dp (XL). Menu 4dp away.
**Color roles:** colors come from the button component: elevated, filled, tonal, or outlined.
**Do / Don't:**
- Do keep the label to one or two words.
- Do align the menu to the trailing button.
- Don't swap the trailing chevron icon.
- Don't lengthen the label or alter the menu.
**Accessibility:**
- 48dp targets; trailing button announces expanded/collapsed.
**Review checks:** height matches a size; 2dp gap; trailing chevron present and rotates; targets 48dp; menu 4dp away.

| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| SPB-01 | Height by size | XS 32, S 40, M 56, L 96, XL 136dp | E | components/split-button/specs@2026-02-05 |
| SPB-02 | Gap between parts | 2dp; inner corners extra-small; trailing 50% when selected | E | components/split-button/specs@2026-02-05 |
| SPB-03 | Touch target per part | at least 48x48dp | F | components/split-button/accessibility@2026-02-05 |
| SPB-04 | Trailing icon | expand/collapse, rotates 180 degrees on open | E | components/split-button/guidelines@2026-02-05 |
| SPB-05 | Menu offset | 4dp from the button, aligned to trailing edge when possible | E | components/split-button/guidelines@2026-02-05 |
| SPB-06 | Trailing label conveys menu state | expanded/collapsed announced | F | components/split-button/accessibility@2026-02-05 |

## Switch
**Use:** Immediate on/off toggle for one standalone option or setting.
**Dimensions & shape:** Track 52 x 32dp, 2dp outline (unselected), full corners. Handle: 16dp unselected, 24dp selected or with icon; grows when pressed. Icon 16dp. State layer 40dp; touch target 48dp.
**Color roles:** On: track primary, handle on-primary, icon primary. Off: track surface-container-highest, outline and handle outline, icon surface-container-highest.
**Do / Don't:**
- Do pair with an inline label; apply immediately.
- Do use clear binary handle icons only.
- Don't use for opposing choices or single-pick lists.
- Don't put text in the track.
**Accessibility:**
- 48dp target; state not color-only; Space/Enter toggles; adjacent label is the name.
**Review checks:** 52x32 track; label next to it; on/off differ by handle position; effect immediate.

| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| SWT-01 | Track size | 52 x 32dp; unselected outline 2dp | C | components/switch/specs@2026-01-06 |
| SWT-02 | Handle size | 16dp off, 24dp on or with icon | C | components/switch/specs@2026-01-06 |
| SWT-03 | Color roles | on: primary track, on-primary handle; off: surface-container-highest track, outline handle | C | components/switch/specs@2026-01-06 |
| SWT-04 | Touch target | 48dp; do not reduce via density | F | components/switch/accessibility@2026-01-06 |
| SWT-05 | Visible label next to every switch | describes the on state | F | components/switch/guidelines@2026-01-06 |
| SWT-06 | Binary and immediate only | no Save step, no opposing options | C | components/switch/guidelines@2026-01-06 |

## Tabs
**Use:** Switch between peer content groups (not sequential steps); primary under an app bar, secondary nested.
**Dimensions & shape:** Container 48dp (label only) or 64dp (icon and label), square corners, full window width, 1dp bottom divider. Icon 24dp, 8dp icon-to-text inline gap, 4dp text-to-badge. Active indicator: primary 3dp tall (top corners 3dp), secondary 2dp, min length 24dp. First scrollable tab offset 52dp from the leading edge. Badge up to four characters.
**Color roles:** container surface; active label/icon primary (primary tabs) or on-surface (secondary); inactive on-surface-variant; indicator primary; divider surface-variant.
**Do / Don't:**
- Do use icons on all tabs or none.
- Do put secondary tabs below primary.
- Don't use for sequential content.
- Don't truncate labels or loop scrolling.
**Accessibility:**
- 48dp targets; active tab not color-only; icon-only tabs need labels.
**Review checks:** heights 48/64; indicator 3dp or 2dp; at most four fixed tabs.

| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| TAB-01 | Container height | 48dp label-only; 64dp icon plus label | C | components/tabs/specs@2026-05-18 |
| TAB-02 | Active indicator | primary 3dp, secondary 2dp, color primary, min length 24dp | C | components/tabs/specs@2026-05-18 |
| TAB-03 | Active/inactive colors | active primary (secondary tabs on-surface); inactive on-surface-variant | C | components/tabs/specs@2026-05-18 |
| TAB-04 | Fixed tab count | at most four; use scrollable beyond | C | components/tabs/guidelines@2026-05-18 |
| TAB-05 | Scrollable tabs: first tab offset 52dp; badge max four characters | required | C | components/tabs/guidelines@2026-05-18 |
| TAB-06 | Icons on all tabs or none; icon-only needs accessible name | required | F | components/tabs/guidelines@2026-05-18 |

## Text fields
**Use:** Free-text entry; filled or outlined, same function.
**Dimensions & shape:** Container height 56dp (target 56dp). Padding 16dp sides (12dp with icons), 8dp top/bottom, 16dp icon-to-text, 4dp above supporting text. Icons 24dp. Filled: extra-small top corners, bottom indicator 1dp (2dp focused). Outlined: extra-small corners, outline 1dp (3dp focused).
**Color roles:** filled container surface-container-highest; outline `outline`; label/supporting on-surface-variant; input on-surface; focused label and stroke primary; error: label, stroke, supporting text, trailing icon all `error`.
**Do / Don't:**
- Do show a visible one-line label and an error icon with error text.
- Do mark required fields with an asterisk.
- Don't mix filled and outlined in one form.
- Don't use placeholder-only fields.
**Accessibility:**
- Edge contrast 3:1; label is the name; errors use alert role; icon buttons labeled by function.
**Review checks:** height 56; label always visible; error not color-only; one variant per form; focus state distinct.

| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| TXF-01 | Container height and padding | 56dp; 16dp sides (12dp with icons); 8dp top/bottom | C | components/text-fields/specs@2026-05-18 |
| TXF-02 | Stroke widths | filled indicator 1dp, focus 2dp; outlined 1dp, focus 3dp | C | components/text-fields/specs@2026-05-18 |
| TXF-03 | Error state | error role on label, stroke, supporting text, icon plus error icon | C | components/text-fields/specs@2026-05-18 |
| TXF-04 | Container/outline contrast with background | at least 3:1 | F | components/text-fields/accessibility@2026-05-18 |
| TXF-05 | Every field labeled; label visible, one line, not truncated | required | F | components/text-fields/guidelines@2026-05-18 |
| TXF-06 | One variant per region; fields not full-width on large screens | required | C | components/text-fields/guidelines@2026-05-18 |

## Time pickers
**Use:** Modal time entry; dial and input variants; not for fine precision.
**Dimensions & shape:** Container extra-large (28dp) corners, dynamic width. Dial 256dp, full shape; selector handle 48dp, center dot 8dp, track 2dp. Time selector fields 96 x 80dp (114dp wide in 24h vertical), small (8dp) corners. Period (AM/PM) selector 52 x 80dp vertical or 216 x 38dp horizontal, 1dp outline.
**Color roles:** container surface-container-high; dial surface-container-highest; selected field primary-container / on-primary-container; unselected field surface-container-highest / on-surface; selected period tertiary-container; handle and track primary; selected dial label on-primary; headline on-surface-variant.
**Do / Don't:**
- Do offer the keyboard/clock toggle.
- Do use a scrim; switch variant instead of scrolling.
- Don't apply density to the dial.
- Don't show AM/PM in 24-hour mode.
**Accessibility:**
- Dial targets 48dp; manual entry reachable; dial announces e.g. "Hour 7 of 12".
**Review checks:** scrim and 28dp container; dial 256dp; toggle icon present; Cancel/OK present.

| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| TMP-01 | Container | surface-container-high, 28dp corners, modal over scrim | C | components/time-pickers/specs@2026-02-05 |
| TMP-02 | Dial and field sizes | dial 256dp; fields 96x80dp; period 52x80 (vertical) or 216x38 (horizontal) | C | components/time-pickers/specs@2026-02-05 |
| TMP-03 | Manual input available from dial via keyboard icon | required | F | components/time-pickers/accessibility@2026-02-05 |
| TMP-04 | Dial touch targets | at least 48x48dp | F | components/time-pickers/accessibility@2026-02-05 |
| TMP-05 | Selected colors | field primary-container; period tertiary-container; handle primary | C | components/time-pickers/specs@2026-02-05 |
| TMP-06 | No scrolling; fall back to input variant in short viewports | required | C | components/time-pickers/guidelines@2026-02-05 |

## Toolbars
**Use:** Frequent page actions; docked (global, bottom) or floating (contextual); Expressive, replaces bottom app bar.
**Dimensions & shape:** Docked height 64dp, square corners, 16dp edge padding, 4-32dp spacing between items. Floating 64dp tall (or 64dp wide vertical), pill corners, 4dp between items, elevation level3. Margins: horizontal 16dp, vertical 24dp. FAB beside it: 56dp expanded or 80dp collapsed, 8dp gap.
**Color roles:** docked and standard floating surface-container; vibrant floating primary-container; standard icons on-surface-variant, selected on-secondary-container.
**Do / Don't:**
- Do move overflow actions into a menu.
- Do emphasize one action only.
- Don't round the docked container.
- Don't use square buttons in floating toolbars.
**Accessibility:**
- 48dp targets; Tab/arrows move; web role toolbar.
**Review checks:** 64dp height; corners per variant; no nav bar alongside; one emphasized action.

| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| TLB-01 | Height / width | docked 64dp tall; floating 64dp tall (horizontal) or wide (vertical) | E | components/toolbars/specs@2026-05-18 |
| TLB-02 | Corners | docked none; floating full | E | components/toolbars/specs@2026-05-18 |
| TLB-03 | Window margin for floating | 16dp horizontal, 24dp vertical minimum | E | components/toolbars/guidelines@2026-05-18 |
| TLB-04 | Never shown with a navigation bar | docked at bottom only | C | components/toolbars/guidelines@2026-05-18 |
| TLB-05 | Emphasize one action only | one filled/primary control or FAB | E | components/toolbars/guidelines@2026-05-18 |
| TLB-06 | Every control touch target | at least 48x48dp | F | components/toolbars/guidelines@2026-05-18 |

## Tooltips
**Use:** Plain labels icon-only elements; rich explains with optional subhead, link, up to two text buttons.
**Dimensions & shape:** Plain: 24dp height, 8dp padding, extra-small (4dp) corners. Rich: medium (12dp) corners, padding 16dp sides, 12dp top, 8dp bottom. Plain sits 4dp from a bounded target (8dp for text baselines); rich shifts in 8dp steps to stay on screen.
**Color roles:** plain container inverse-surface, text inverse-on-surface; rich container surface-container, subhead and text on-surface-variant, action labels primary.
**Do / Don't:**
- Do use plain tooltips on icon-only buttons.
- Do give auto-shown rich tooltips a subhead.
- Don't tooltip elements that have a visible label.
- Don't hide critical information in tooltips.
**Accessibility:**
- Show on focus as well as hover; no focus trap; tooltip role.
**Review checks:** colors match variant; 4dp gap; target uncovered.

| ID | Rule | Value / criterion | Tier | Source |
| --- | --- | --- | --- | --- |
| TIP-01 | Plain tooltip colors and shape | inverse-surface, inverse-on-surface, 4dp corners | C | components/tooltips/specs@2026-01-30 |
| TIP-02 | Rich tooltip shape and padding | 12dp corners, 16dp sides, 12 top, 8 bottom | C | components/tooltips/specs@2026-01-30 |
| TIP-03 | Offset from target | 4dp (bounded) or 8dp (text) | C | components/tooltips/guidelines@2026-01-30 |
| TIP-04 | Appear on keyboard focus as well as hover | required | F | components/tooltips/accessibility@2026-01-30 |
| TIP-05 | Do not trap focus or hide required info | required | F | components/tooltips/accessibility@2026-01-30 |
| TIP-06 | One tooltip at a time; hide 1.5 s after leaving; rich max two buttons | required | C | components/tooltips/guidelines@2026-01-30 |
