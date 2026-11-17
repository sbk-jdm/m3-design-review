# Design brief: Settings screen (habit-tracking PWA)

Mode: screen   Date: 2026-11-17   Status: draft
Platform and stack: web (PWA), plain HTML, CSS custom properties and vanilla JavaScript, no framework
Window size classes: compact (< 600dp), designed for 360-412dp; medium and wider reuse the compact layout in a centered column (B-01)
Themes: light and dark; contrast level standard   Tolerance: inspired (set by user)
Sources: Material Design 3 references, snapshot 2026-05-21 (rule IDs cite https://m3.material.io/<path> as path@lastmod)
  Project guidelines: none   Decisions ledger: none
Color scheme: generated from seed #2E7D32, approximate tonal-spot; exact values can be regenerated from the seed with
  Material Theme Builder or material-color-utilities (B-02)

Units: dp in specs; on the web 1dp = 1 CSS px. Type sizes and line heights in rem (px / 16, M3 TYP-13); spacing,
sizes and radii in px so they do not grow with text (M3 SPC-05). Every value carries its source: `M3 <RULE-ID>`,
`decision B-nn`, or `WCAG 2.2 SC x.y.z`.

## Handoff prompt

```
Implement the design brief below exactly. Scope: the Settings screen (route /settings) and the app-wide theme and
text-size mechanism it controls (CSS tokens in "10. Tokens", the data-theme attribute, the text-scale variable).
Stack: plain HTML, CSS custom properties and vanilla JavaScript, no framework, installable PWA.
1. Use only the values in this brief: the tokens in "Tokens" (names and values as given), the component specs,
   the copy table. Do not invent colors, sizes, radii, spacing, type styles, durations or texts. If you need a value
   the brief does not give, stop and ask.
2. Keep every acceptance criterion (AC-nn) true. Accessibility criteria are mandatory: never trade them for looks.
3. Values marked "project" come from the existing codebase or guidelines: reuse the existing token or component
   instead of redefining it.
4. If the brief conflicts with the existing code, a library default or another AC, do not choose silently: report
   it as a question quoting the AC-nn, C-nn or section.
5. Do not change behavior, data, text or styles outside the scope.
6. When done, reply with: the files you changed; for each AC, how you checked it (or "not checked" and why); any
   deviation from the brief, and open questions.
```

## 1. Purpose

Users: people tracking daily habits on their phone, usually one-handed and in short sessions (decision B-03).

Primary task: change a preference and see it take effect immediately (no Save step, M3 SWT-06). The screen has no
single primary action, so it has no filled button or FAB (M3 LAY-48, BTN-07).

Secondary tasks: turn the daily reminder on or off and set its time; choose theme, text size and first day of the
week; export data as CSV; delete all habit data after a confirmation; see which account is signed in and sign out.

Success: the changed value is visible in its control at once and persists after reload and offline (theme and text
size repaint the whole app immediately); export ends with a downloaded file plus inline and snackbar confirmation;
deletion ends with a snackbar and the data rows showing the empty state.

Scope in: the Settings screen, its two dialogs (delete confirmation, sign-out with unsynced changes), its snackbar,
offline and permission states, the app-wide theme and text-size tokens.
Scope out: sign-in screen, profile editing (name and email are display-only, B-04), notification delivery
(push service), the content of the CSV beyond its file name, layouts designed for medium and wider windows.

## 2. Content inventory

Order = reading order = focus order (M3 A11-06, A11-19). Sample content uses placeholders only.

| # | Item | Type | Priority | Data source and sample | Notes |
| --- | --- | --- | --- | --- | --- |
| 1 | Back | control | high | n/a | Icon button in the app bar |
| 2 | Title "Settings" | text | high | static | Page heading, h1 |
| 3 | Offline status | text | conditional | `navigator.onLine` and sync queue | Only while offline (B-14) |
| 4 | Section heading "Account" | text | medium | static | h2 |
| 5 | Account summary: avatar initials, name, email | data | medium | Cached profile: "Sample User", "sample.user@example.com", initials "SU" | Not interactive (B-04) |
| 6 | Sign out | control | medium | n/a | List row action |
| 7 | Section heading "Reminders" | text | medium | static | h2 |
| 8 | Daily reminder | control | high | Setting `reminder.enabled`, default off (B-05); `Notification.permission` | Switch row |
| 9 | Reminder time | control | high | Setting `reminder.time`, default 20:00 (B-05) | Outlined text field, native time input (B-06) |
| 10 | Section heading "Appearance" | text | medium | static | h2 |
| 11 | Theme: System default, Light, Dark | control | high | Setting `theme`, default System default (B-05) | Radio group (B-07) |
| 12 | Text size: Small, Medium, Large | control | high | Setting `textSize`, default Medium (B-05) | Radio group (B-07, B-08) |
| 13 | Section heading "Calendar" | text | medium | static | h2 (B-09) |
| 14 | Week starts on: Monday, Sunday | control | medium | Setting `weekStart`, default Monday (B-05) | Radio group (B-07) |
| 15 | Section heading "Data" | text | medium | static | h2; focus target after deletion (section 6) |
| 16 | Export data | control | medium | Local habits and check-ins; last export time | List row action; file `habits-YYYY-MM-DD.csv` |
| 17 | Delete all data | control | low | Local and account data | Destructive list row; opens dialog (B-12) |
| 18 | Snackbar | text, control | conditional | n/a | Bottom of window, one at a time |

## 3. Layout

### Compact (< 600dp), designed at 360, 390 and 412dp

Ordered regions:
1. Top app bar, small: full window width, height 64dp (M3 APB-01), corner none (M3 APB-04), leading space 4dp
   (M3 APB, dimensions), leading Back icon button, title "Settings". No trailing actions (M3 APB-05). Sticks to the
   top while content scrolls (decision B-10). Sits below the status bar (M3 LAY-38).
2. Main content: one scrolling column on `surface` (M3 COL-17), sections in inventory order. Rows span the full
   window width with 16dp inner side padding, which gives the 16dp compact margin (M3 LAY-16, LST-03). Bottom
   padding 16dp plus `env(safe-area-inset-bottom)` (M3 LAY-38; 16dp is decision B-10).
3. Snackbar (when shown): fixed at the bottom, 16dp from each side and 16dp above the bottom safe area
   (decision B-15).
4. Dialogs (when open): centered over a scrim (section 4).

No navigation bar on this screen: Settings is a secondary screen opened from the app's main screen and left with
Back (decision B-03, M3 LAY-36). Vertical scroll only, never horizontal (M3 WRT-04).

Spacing inside the column (all on the 8dp scale, M3 SPC-01; values decision B-09):
- Section heading: padding 16dp top, 8dp bottom, 16dp sides.
- Group legend (Theme, Text size, Week starts on): padding 8dp top, 8dp bottom, 16dp sides.
- List rows: 16dp side padding, 12dp gap between leading element, text and trailing element (M3 LST-03).
- Reminder time field: 16dp side margins, 8dp above and 16dp below (decision B-09).
- No dividers: sections are grouped by their headings and spacing (M3 LAY-33, DIV-02).

Text wireframe at 390dp (light theme, reminder on, online):

```
+------------------------------------------+
| [<-]  Settings                           |  top app bar 64dp
+------------------------------------------+
| Account                                  |  section heading
| (SU) Sample User                         |  72dp row, not interactive
|      sample.user@example.com             |
| Sign out                                 |  56dp row
| Reminders                                |
| Daily reminder                    [==o]  |  72dp switch row
| Get a notification to check in...        |
|  +- Reminder time -------------------+   |  outlined field 56dp
|  | 8:00 PM                           |   |
|  +-----------------------------------+   |
|  Every day, in this device's time zone   |
| Appearance                               |
| Theme                                    |  legend
| (o) System default                       |  56dp radio rows
| ( ) Light                                |
| ( ) Dark                                 |
| Text size                                |
| ( ) Small                                |
| (o) Medium                               |
| ( ) Large                                |
| Calendar                                 |
| Week starts on                           |
| (o) Monday                               |
| ( ) Sunday                               |
| Data                                     |
| Export data                              |  72dp row
| Download your habits and check-ins...    |
| Delete all data                          |  72dp row, error label
| Permanently delete your habits and...    |
+------------------------------------------+
```

### Medium, expanded and wider (600dp and up)

Not designed (B-01). Until a wider layout is specified, the compact layout applies unchanged, with the app bar at full
window width and the content column limited to 600dp wide and centered (decision B-01). The layout must reflow on
resize and rotation without reload (M3 LAY-12).

## 4. Components

```
Back: standard icon button, small (container 40dp, icon 24dp)   Function: return to the previous screen (CMP-01)
Container: none at rest; state layer circle 40dp, corner full   Source: M3 ICB-01, ICB-05, LAY-32
Content: icon arrow_back, Material Symbols Outlined, 24dp, on-surface #171D16 / #DCE5DB (M3 APB color roles)
Target: 48 x 48dp   Source: M3 ICB-02
Behavior: history back; with no in-app history (deep link), go to the app's main screen (B-03)
Label / accessible name: "Back" (TXT-02); plain tooltip "Back" on hover and focus (M3 ICB-06, TIP-04)
```

```
App bar title: text in the small top app bar   Function: page title, the page's only h1 (M3 A11-22)
Container: surface #F3FCF2 / #0E150C at rest; surface-container #E8F0E6 / #1B211A once the content is scrolled,
  no shadow (elevation level0 to level2 shown tonally)   Source: M3 APB-06, ELV-05
Content: "Settings", title-large 1.375rem / 1.75rem, weight 400, on-surface; one line, never truncated
  Source: M3 APB-02, APB (do / don't)
Text scale: the title ignores the in-app text-size setting and uses the baseline size (M3 WRT-05); browser text
  size still scales it (rem)
```

```
Offline status: non-interactive status row (B-14)   Function: tell the user changes are kept locally
Container: surface-container-high #E2EAE1 / #252C24, corner medium 12dp, margin 8dp top and 16dp sides, padding 16dp
  Source: decision B-14 (role per M3 COL-18, corner per M3 SHP-01)
Content: icon cloud_off 24dp on-surface-variant #40493F / #BECABD, hidden from assistive tech (M3 A11-25);
  text TXT-32 body-medium 0.875rem / 1.25rem on-surface #171D16 / #DCE5DB; gap 12dp   Source: decision B-14
Behavior: shown while offline; removed when back online. role="status" (M3 A11-07)
```

```
Section heading (Account, Reminders, Appearance, Calendar, Data): h2   Function: group label (M3 A11-35)
Content: title-small 0.875rem / 1.25rem, weight 500, tracking 0.0071em, primary #396937 / #A0D49B on surface
  Source: M3 TYP-01 (title role for section headers); primary color decision B-09
```

```
Account summary: list item, two lines (72dp), not interactive   Function: show who is signed in (B-04)
Container: surface, no state layers (not interactive)   Source: M3 LST-01, LST-03
Leading: avatar 40dp, corner full, primary-container #BBF0B6 / #205121 with initials "SU" in on-primary-container
  #205121 / #BBF0B6, title-medium 1rem / 1.5rem weight 500; hidden from assistive tech (initials repeat the name)
  Source: M3 LST-03 (avatar 40dp); colors and type decision B-04
Content: name body-large 1rem / 1.5rem on-surface; email body-medium 0.875rem / 1.25rem on-surface-variant
  #40493F / #BECABD; both wrap (overflow-wrap: anywhere), never truncated   Source: M3 LST-02, WRT-07, A11-09
```

```
List action row (Sign out, Export data, Delete all data): list item as a native <button>, full width
  Function: run an action (CMP-01)
Container: surface; min-height 56dp (one line: Sign out) or 72dp (two lines: Export, Delete); grows with text
  Source: M3 LST-01, WRT-04
Content: label body-large on-surface (Delete all data: label in error #C00013 / #FFB4A5, B-12); supporting text
  body-medium on-surface-variant; text left aligned at 16dp; no leading icons   Source: M3 LST-02, LST-03; B-09
Trailing (Export only, while busy): indeterminate circular progress indicator 24dp, stroke 4dp, primary
  #396937 / #A0D49B, role="progressbar", aria-label "Exporting data"   Source: M3 PRG-02, PRG-04, PRG-07; B-13
Target: the whole row, at least 48dp tall (rows are 56 or 72dp)   Source: M3 A11-01
Behavior: section 6. Accessible name = label text; supporting text via aria-describedby (M3 A11-31)
```

```
Daily reminder: switch in a two-line list row (72dp)   Function: binary setting applied immediately (M3 SWT-05, SWT-06)
Row: native <label> wrapping text and <input type="checkbox" role="switch">; the whole row is the target
  Source: M3 SWT-04, SWT-05; whole-row target decision B-07
Content: label TXT-07 body-large on-surface; supporting TXT-08 body-medium on-surface-variant   Source: M3 LST-02
Switch: track 52 x 32dp, corner full; handle 16dp off, 24dp on; no handle icons   Source: M3 SWT-01, SWT-02
  On: track primary #396937 / #A0D49B, handle on-primary #FFFFFF / #03390B   Source: M3 SWT-03
  Off: track surface-container-highest #DCE5DB / #30372F, 2dp outline and handle outline #707A6E / #899487
  Source: M3 SWT-01, SWT-03
Trailing padding 16dp; gap text to switch 12dp   Source: M3 LST-03
Behavior: section 6 (permission flow)
```

```
Reminder time: outlined text field wrapping a native <input type="time"> (B-06)
  Function: enter the reminder time (typed entry always available, M3 TMP-03)
Container: height 56dp, corner extra-small 4dp, outline 1dp outline #707A6E / #899487 (3dp primary when
  focused), padding 16dp sides, 8dp top and bottom, 4dp above supporting text   Source: M3 TXF-01, TXF-02, TXF (dimensions)
Content: visible label TXT-11 (on-surface-variant; primary when focused), value body-large on-surface in the
  device locale's time format with tabular figures (font-variant-numeric: tabular-nums), supporting text TXT-12
  body-small 0.75rem / 1rem on-surface-variant   Source: M3 TXF-05, TYP-12; label and supporting type roles B-06
Width: full column width minus 16dp margins (328dp at 360dp)   Source: M3 LAY-16; B-06
Error: label, outline and supporting text in error #C00013 / #FFB4A5, trailing icon error 24dp, text TXT-13
  Source: M3 TXF-03
Behavior: section 6. Disabled while Daily reminder is off (section 5)
```

```
Radio groups (Theme, Text size, Week starts on): <fieldset> with <legend>, one list row per option   (B-07)
  Function: choose one of 2-3 options, applied immediately (M3 RAD-04, LST-05)
Legend: label-large 0.875rem / 1.25rem weight 500, on-surface-variant #40493F / #BECABD   Source: decision B-09
Row: native <label> with <input type="radio">, min-height 56dp, the whole row is the target and carries the state
  layer (M3 INT-05); radio icon 20dp in a 24dp leading slot at 16dp start padding, 12dp gap to the label
  Source: M3 RAD-01, LST-01, LST-03; slot decision B-07
Colors: selected radio primary #396937 / #A0D49B; unselected on-surface-variant #40493F / #BECABD; label body-large
  on-surface   Source: M3 RAD-02, LST-02
Behavior: section 6
```

```
Delete confirmation: basic dialog, native <dialog> opened with showModal(), role="alertdialog"
  Function: confirm a destructive, irreversible action (M3 DLG-01..DLG-07)
Container: surface-container-high #E2EAE1 / #252C24, corner extra-large 28dp, padding 24dp, no shadow (level3 shown
  by tone and scrim, B-11); width min(560dp, 100vw - 48dp)   Source: M3 DLG-01, DLG-02; width decision B-11
Scrim: scrim #000000 at 32% opacity, both themes (::backdrop)   Source: M3 ELV-09, DLG-04
Content: headline TXT-27 headline-small 1.5rem / 2rem on-surface; 16dp gap; body TXT-28 body-medium on-surface-variant;
  inline error (when shown) TXT-30 body-medium error, role="alert"   Source: M3 DLG-02, DLG (color roles); type B-11
Actions: two text buttons, small (height 40dp, 16dp side padding, label-large, corner full), trailing aligned,
  8dp apart, 24dp above them: "Cancel" in primary #396937 / #A0D49B, then "Delete" nearest the edge in error
  #C00013 / #FFB4A5 (B-12)   Source: M3 BTN-01, BTN-02, BTN-03, DLG-02, DLG-03
Target: each button 48dp tall hit area   Source: M3 BTN-09
Label / accessible name: aria-labelledby the headline, aria-describedby the body (M3 DLG accessibility)
```

```
Sign-out confirmation (only with unsynced changes): basic dialog, same spec as Delete confirmation   (B-16)
Content: headline TXT-33a, body TXT-33b; actions "Cancel" (primary) and "Sign out" (primary)
```

```
Snackbar: single-line or two-line snackbar   Function: brief feedback after export or deletion (M3 SNB-03)
Container: inverse-surface #2C322B / #DCE5DB, corner extra-small 4dp, min-height 48dp (68dp two lines), padding
  16dp sides, no shadow   Source: M3 SNB-01, SNB-02; padding and no-shadow decision B-15
Content: text body-medium inverse-on-surface #EAF3E9 / #2C322B   Source: M3 SNB-02; type role B-15
Action: none on this screen (B-15)
Behavior: role="status" polite live region; never takes focus; auto-dismiss after 6 s; Escape dismisses
  Source: M3 SNB-04, SNB-05; 6 s decision B-15
```

## 5. States

State layers use the content color of the element (M3 INT-04) at hover 8%, focus 10%, pressed 10% (M3 INT-03), one
at a time (M3 INT-05). Focus ring on every focusable element: 3dp solid secondary #50644D / #B6CDB3, offset 2dp
around icon buttons, buttons and the text field; inset (offset -3dp) on full-width rows, following the element's
corner shape (decision B-17). Disabled: content on-surface at 38%, not focusable, no state layers (M3 INT-06,
BTN-05); disabled content is exempt from contrast (M3 INT-07).

| Element | Default | Hover | Focus | Pressed | Disabled | Selected | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Back | icon on-surface, no container | on-surface 8% circle 40dp | on-surface 10% circle plus ring | on-surface 10% plus ripple | n/a: always available | n/a | M3 INT-03, INT-13, LAY-32; B-17 |
| Action rows (Sign out, Export) | surface, text on-surface / on-surface-variant | on-surface 8% over row | on-surface 10% plus inset ring | on-surface 10% plus ripple | label on-surface 38%; supporting text that says why stays on-surface-variant at 100% (TXT-25, TXT-26) | n/a | M3 INT-03, INT-06; B-13 |
| Export, busy | supporting text TXT-20, trailing progress indicator, aria-busy="true", not activatable | none | ring stays | none | n/a | n/a | M3 PRG-05; B-13 |
| Delete all data row | label error, supporting on-surface-variant | on-surface 8% | on-surface 10% plus inset ring | on-surface 10% plus ripple | as action rows (no data: TXT-25; offline: TXT-26) | n/a | M3 INT-03; B-12 |
| Daily reminder row | switch off or on per SWT-03 | on-surface 8% over row | on-surface 10% plus inset ring | on-surface 10%; handle grows (M3 Switch dimensions) | unsupported browser: label and switch 38%, supporting TXT-10 at 100% | on: handle 24dp at end, track primary (position, size and color: three cues) | M3 SWT-01..SWT-03, INT-01 |
| Reminder time field | outline 1dp outline, label on-surface-variant | outline on-surface (decision B-06) | outline 3dp primary, label primary, plus ring | n/a: text input | reminder off: label, value, outline and supporting text on-surface 38%, outline on-surface 10% (B-06) | n/a | M3 TXF-02, INT-06 |
| Reminder time field, error | label, outline, supporting text error, trailing error icon, text TXT-13 | same | 3dp error outline plus ring | n/a | n/a | n/a | M3 TXF-03 |
| Radio row | unselected: ring icon on-surface-variant | on-surface 8% over row | on-surface 10% plus inset ring | on-surface 10% plus ripple | n/a: always enabled | radio filled with inner dot, primary (shape plus color) | M3 RAD-02, INT-01, LST-04 |
| Dialog text buttons | label primary or error, no container | label color 8% | label color 10% plus ring | label color 10% plus ripple | while deleting: on-surface 38% | n/a | M3 BTN-05, INT-03 |

| View | Loading | Empty | Error | Offline | Long content | Source |
| --- | --- | --- | --- | --- | --- | --- |
| Settings values | none: read synchronously from localStorage before first paint (B-18) | n/a: defaults always exist (B-05) | corrupt stored value: use the default silently | edits saved locally, synced later; status row shown (B-14) | radio and row labels wrap; rows grow | M3 LDI-02, WRT-07 |
| Account summary | profile not cached yet and fetch over 200 ms: two skeleton bars (surface-container-highest, corner full, 12dp tall, 160dp and 200dp wide) in a 72dp row, no layout jump | n/a: screen only reachable when signed in | fetch fails: name hidden, supporting text TXT-34 | cached profile shown; nothing cached: TXT-34 | long name or email wraps, never ellipsis | M3 MOT-10, A11-09; B-13 |
| Export | under 200 ms: no indicator; over 200 ms: busy state above | no habits: row disabled, TXT-25 | supporting text TXT-22 in error, row enabled to retry | works offline from local data | file name in snackbar wraps to two lines (68dp) | M3 LDI-02, PRG-05, SNB-01; B-13 |
| Delete | dialog busy: "Delete" label becomes TXT-29c with a 20dp indeterminate circular indicator in the label color, no track; both buttons disabled; Escape ignored | no habits: row disabled, TXT-25 | dialog stays open, TXT-30 shown, buttons enabled again | row disabled, TXT-26 | dialog body scrolls inside the dialog between pinned headline and actions | M3 PRG-06, DLG (do: pin title and buttons); B-12 |
| Reminder permission | permission prompt open: switch shows off until granted | n/a | permission denied: switch off, supporting text becomes TXT-09 | switch and time still editable; saved locally | n/a | B-19 |

## 6. Interactions and navigation

| Trigger | Result | Focus after | Keyboard | Source |
| --- | --- | --- | --- | --- |
| Screen opens (from main screen or deep link /settings) | Settings shown with stored values | h1 "Settings" (tabindex="-1") | Tab then reaches Back | M3 A11-33, INT-30 |
| Back | Previous screen; deep link with no history: main screen | The control that opened Settings on the previous screen | Enter or Space on Back; browser and Android back do the same | M3 A11-33; B-03 |
| Activate Sign out, all changes synced | Sign out and go to the sign-in screen | Sign-in screen title (out of scope) | Enter or Space | M3 A11-33; B-16 |
| Activate Sign out, unsynced changes | Sign-out dialog opens | "Cancel" (first control) | Tab cycles inside; Escape = Cancel | M3 DLG-06, A11-11; B-16 |
| Toggle Daily reminder on, permission "default" | Browser permission prompt; granted: switch on, time field enabled; denied: switch off, TXT-09 | Stays on the switch row | Space or Enter toggles | M3 SWT-06, A11-11; B-19 |
| Toggle Daily reminder on, permission "denied" | Switch stays off; supporting text TXT-09 | Stays on the switch row | Space or Enter | B-19 |
| Toggle Daily reminder off | Switch off; time field disabled; stored time kept | Stays on the switch row | Space or Enter | M3 SWT-06 |
| Change reminder time (input "change" event) | Saved immediately if valid; empty value shows error TXT-13 and keeps the last valid time stored | Stays in the field | Native time input keys; Android opens the system picker on tap | M3 TMP-03, TXF-03; B-06 |
| Select a theme option | Theme applies at once: System default removes `data-theme`; Light sets `data-theme="light"`; Dark sets `data-theme="dark"` on `<html>`; `<meta name="theme-color">` updated to the surface value of the active theme | Stays on the radio | Arrow keys move and select within the group; Tab leaves the group | M3 RAD-05, A11-32; B-18 |
| Select a text size option | `--app-text-scale` on `<html>` becomes 0.875, 1 or 1.25; every scaled type style updates at once | Stays on the radio (scrolled into view if the reflow moved it) | Arrow keys; Tab leaves | M3 RAD-05; B-08 |
| Select week start | Saved; calendars elsewhere in the app use it | Stays on the radio | Arrow keys; Tab leaves | M3 RAD-05 |
| Activate Export data | Build CSV from local data, download `habits-YYYY-MM-DD.csv`; on success supporting text becomes TXT-21 and snackbar TXT-23 | Stays on the Export row | Enter or Space | M3 SNB-06; B-13 |
| Activate Delete all data | Delete dialog opens | "Cancel" | Tab cycles; Escape = Cancel | M3 DLG-06, A11-11 |
| Dialog "Cancel" or Escape | Dialog closes, nothing changes | The row that opened it | Escape, Enter, Space | M3 A11-11, A11-34 |
| Dialog "Delete" | Busy state; success: dialog closes, data removed, snackbar TXT-31, Export and Delete rows show TXT-25 | Success: h2 "Data" (tabindex="-1"), because the Delete row is now disabled; failure: stays on "Delete" | Enter or Space | M3 A11-33, A11-11; B-12 |
| Snackbar shown | Announced politely, dismissed after 6 s | Unchanged | Escape dismisses it when no dialog is open | M3 SNB-04, SNB-05; B-15 |

What persists: every setting in localStorage (key `settings`, JSON) and in the account when online; scroll position
is not restored when the screen is reopened (decision B-18).

## 7. Motion

Durations and easings come from the M3 token set (M3 MOT-01..MOT-04). Reduced motion =
`@media (prefers-reduced-motion: reduce)` (M3 A11-15, MOT-06).

| Transition | Pattern | Easing and duration | Reduced motion | Source |
| --- | --- | --- | --- | --- |
| Settings screen enters | fade in (opacity 0 to 1) | standard decelerate `cubic-bezier(0, 0, 0, 1)`, 250ms | no animation | M3 MOT-02, MOT-13 |
| Settings screen exits (Back) | fade out | standard accelerate `cubic-bezier(0.3, 0, 1, 1)`, 200ms | no animation | M3 MOT-02, MOT-04 |
| Dialog and scrim open | fade in, enter and exit pattern | standard decelerate, 250ms | no animation | M3 MOT-02, MOT-09 |
| Dialog and scrim close | fade out | standard accelerate, 200ms | no animation | M3 MOT-04 |
| Switch handle moves and resizes; track color | position, size, color | standard `cubic-bezier(0.2, 0, 0, 1)`, short4 200ms | no animation (instant) | M3 MOT-05, MOT-03 |
| App bar fill on scroll | background color | standard, short4 200ms | no animation | M3 APB-06, MOT-03 |
| State layers (hover, focus, press) | opacity | standard, short2 100ms | unchanged (opacity only) | M3 MOT-03 |
| Snackbar enters | slides up 16dp from the bottom edge plus fade | standard decelerate, 250ms | fade only, 250ms | M3 MOT-16, MOT-06; B-15 |
| Snackbar exits | fade out | standard accelerate, 200ms | fade only | M3 MOT-04 |
| Progress indicator | continuous rotation | linear rotation is the indicator itself | indicator hidden; the text (TXT-20, TXT-29c) carries the busy state | M3 MOT-06; B-13 |
| Theme or text-size change | none: repaint at once | n/a | n/a | B-18 |

## 8. Copy

English (US), sentence case (M3 BTN-06). Times follow the device locale via `Intl.DateTimeFormat` (decision B-20).

| ID | Text | Where | Notes (max length, casing, variables) |
| --- | --- | --- | --- |
| TXT-01 | Settings | App bar title, h1, document title | |
| TXT-02 | Back | Back icon button name and tooltip | |
| TXT-03 | Account | Section heading | |
| TXT-04 | Reminders | Section heading | |
| TXT-05 | Appearance | Section heading | |
| TXT-06 | Calendar | Section heading | |
| TXT-06b | Data | Section heading | |
| TXT-07 | Daily reminder | Switch row label (describes the on state, M3 SWT-05) | |
| TXT-08 | Get a notification to check in on your habits | Switch row supporting text | |
| TXT-09 | Notifications are blocked. Allow them for this site in your browser settings. | Switch row supporting text, permission denied | Replaces TXT-08 |
| TXT-10 | Reminders aren't available in this browser. | Switch row supporting text, no Notification API | Replaces TXT-08 |
| TXT-11 | Reminder time | Text field label | |
| TXT-12 | Every day, in this device's time zone | Text field supporting text | |
| TXT-13 | Enter a time | Text field error | |
| TXT-14 | Theme | Legend | Options: "System default", "Light", "Dark" |
| TXT-15 | Text size | Legend | Options: "Small", "Medium", "Large" |
| TXT-16 | Week starts on | Legend | Options: "Monday", "Sunday" |
| TXT-17 | Sign out | Action row label; sign-out dialog confirm button | |
| TXT-18 | Export data | Action row label | |
| TXT-19 | Download your habits and check-ins as a CSV file | Export supporting text, idle and never exported | |
| TXT-20 | Preparing your file… | Export supporting text, busy | |
| TXT-21 | Last export: {date}, {time} | Export supporting text after success | {date} "today" or locale short date; {time} locale time |
| TXT-22 | Export failed. Try again. | Export supporting text after failure, error role | |
| TXT-23 | Export ready: {filename} | Snackbar | {filename} = `habits-YYYY-MM-DD.csv` |
| TXT-24 | Delete all data | Action row label | |
| TXT-24b | Permanently delete your habits and check-in history | Delete supporting text | |
| TXT-25 | No habit data yet | Export and Delete supporting text when there is no data | |
| TXT-26 | Connect to the internet to delete your data | Delete supporting text while offline | |
| TXT-27 | Delete all data? | Delete dialog headline | No "Are you sure?" (M3 DLG-07) |
| TXT-28 | This permanently deletes your habits and check-in history on this device and in your account. You can't undo this. To keep a copy, export your data first. | Delete dialog body | |
| TXT-29a | Cancel | Dialog dismiss button | |
| TXT-29b | Delete | Delete dialog confirm button | Specific verb (M3 DLG, do) |
| TXT-29c | Deleting | Confirm button label while busy | |
| TXT-30 | Couldn't delete your data. Check your connection and try again. | Delete dialog inline error | |
| TXT-31 | All habit data deleted | Snackbar | |
| TXT-32 | You're offline. Changes are saved on this device and sync when you reconnect. | Offline status row | |
| TXT-33a | Sign out? | Sign-out dialog headline | |
| TXT-33b | Some changes haven't synced yet. If you sign out now, they'll be lost. | Sign-out dialog body | |
| TXT-34 | Account details aren't available offline | Account row text when no profile is cached | |
| TXT-35 | Exporting data / Deleting data | Accessible names of the progress indicators | Not visible |

## 9. Accessibility

- Landmarks: `<header>` (banner) holds the app bar; `<main>` holds the content (M3 A11-20). The screen has no
  footer, so no contentinfo.
- Headings: h1 "Settings"; h2 for each section; radio groups use `<fieldset>` and `<legend>` (M3 A11-35, A11-22).
- Focus order: Back, (offline status is not focusable), Sign out, Daily reminder, Reminder time, Theme group, Text
  size group, Week starts on group, Export data, Delete all data. DOM order equals visual order (M3 A11-06, A11-19).
- Native controls only: `<button>`, `<input type="checkbox" role="switch">`, `<input type="radio">`,
  `<input type="time">`, `<dialog>` (M3 A11-12, A11-26). Enter also toggles the switch (script), Space natively.
- Names: every control's accessible name contains its visible label (M3 A11-31); Back has "Back" (M3 ICB-06); the
  avatar and decorative icons are `aria-hidden="true"` (M3 A11-25).
- Announcements: snackbar and offline row are `role="status"`; text-field error and dialog error are announced
  (`aria-describedby` on the field, `role="alert"` in the dialog) (M3 SNB-05, TXF accessibility).
- Composite widgets: radio groups use native arrow-key behavior; one Tab stop per group (M3 A11-32, RAD-05).
- Dialogs: `showModal()` makes the page inert; Escape closes (except while deleting); focus returns to the trigger
  (M3 A11-11, A11-34, DLG-06).
- Text scaling: all type in rem through the scaled tokens; rows, fields and dialogs use min-height and grow; no fixed
  heights on text containers (M3 A11-08, WRT-04). Viewport meta `width=device-width, initial-scale=1` with pinch zoom
  allowed (no `user-scalable=no`, no `maximum-scale`) (M3 A11-08).
- Minimum text size: no content text below 12 CSS px at any in-app text size (M3 A11-30, B-08).

## 10. Tokens

Tokens used by this screen (values from the generated scheme; full exports below):

| Token | Light | Dark | Used by | Source |
| --- | --- | --- | --- | --- |
| --md-sys-color-surface | #F3FCF2 | #0E150C | Page, app bar at rest, rows; `theme-color` meta | M3 COL-17 |
| --md-sys-color-on-surface | #171D16 | #DCE5DB | Titles, labels, values, state layers, disabled content (38%) | M3 COL-02 |
| --md-sys-color-on-surface-variant | #40493F | #BECABD | Supporting text, legends, unselected radios, field label, icons | M3 COL-02 |
| --md-sys-color-surface-container | #E8F0E6 | #1B211A | App bar when scrolled | M3 APB-06 |
| --md-sys-color-surface-container-high | #E2EAE1 | #252C24 | Dialogs, offline status row | M3 DLG-01; B-14 |
| --md-sys-color-surface-container-highest | #DCE5DB | #30372F | Switch track off, skeleton bars | M3 SWT-03 |
| --md-sys-color-primary | #396937 | #A0D49B | Section headings, switch track on, selected radio, focused field, Cancel, progress | M3 COL-12 |
| --md-sys-color-on-primary | #FFFFFF | #03390B | Switch handle on | M3 SWT-03 |
| --md-sys-color-primary-container | #BBF0B6 | #205121 | Avatar | B-04 |
| --md-sys-color-on-primary-container | #205121 | #BBF0B6 | Avatar initials | B-04 |
| --md-sys-color-secondary | #50644D | #B6CDB3 | Focus ring | B-17 |
| --md-sys-color-outline | #707A6E | #899487 | Text field outline, switch outline and handle off | M3 TXF-04, SWT-03 |
| --md-sys-color-error | #C00013 | #FFB4A5 | Delete label and button, field error, export and dialog errors | M3 COL-16, TXF-03; B-12 |
| --md-sys-color-inverse-surface | #2C322B | #DCE5DB | Snackbar container | M3 SNB-02 |
| --md-sys-color-inverse-on-surface | #EAF3E9 | #2C322B | Snackbar text | M3 SNB-02 |
| --md-sys-color-scrim | #000000 | #000000 | Dialog scrim at 32% | M3 ELV-09 |

Contrast check of the generated scheme (WCAG 2.x): light 39/39 and dark 39/39 required pairs pass. Pairs specific to
this screen, checked on the same values: error on surface 6.15:1 / 10.89:1; error on surface-container-high
5.25:1 / 8.41:1; primary on surface-container-high 5.25:1 / 8.45:1; on-surface-variant on surface-container-high
7.62:1 / 8.44:1; secondary (focus ring) on surface 6.11:1 / 10.93:1 and on surface-container-high 5.22:1 / 8.44:1;
outline on surface 4.26:1 / 5.87:1; outline on surface-container-highest (switch off) 3.46:1 / 3.88:1. All meet 4.5:1 for text and 3:1 for non-text.

Scheme note: approximate. Contrast between roles is preserved because luminance depends only on L* (= tone); hue
and colorfulness differ slightly from the official tools. For exact values regenerate with Material Theme Builder or
the material-color-utilities library from seed #2E7D32 (tonal-spot) and re-run the contrast check (AC-29).

App tokens added by this brief (decisions; put them after the exports):

```css
/* Text size setting (B-08). Small 0.875, Medium 1 (default), Large 1.25. */
:root { --app-text-scale: 1; }
:root[data-text-size="small"] { --app-text-scale: 0.875; }
:root[data-text-size="large"] { --app-text-scale: 1.25; }

/* Scaled type: every text style used in content applies size and line height through these, never the raw
   tokens. Floor 0.75rem (12px at default browser size) for size, 1rem for line height (A11-30, B-08).
   Pattern, repeated for each style the app uses (body-large shown): */
:root {
  --app-type-body-large-size: max(0.75rem, calc(var(--md-sys-typescale-body-large-size) * var(--app-text-scale)));
  --app-type-body-large-line-height: max(1rem, calc(var(--md-sys-typescale-body-large-line-height) * var(--app-text-scale)));
}
/* The app bar title (title-large) uses the raw tokens, unscaled (WRT-05). */

/* Focus ring (B-17) */
:root {
  --app-focus-ring-width: 3px;
  --app-focus-ring-color: var(--md-sys-color-secondary);
  --app-focus-ring-offset: 2px;       /* rows use -3px (inset) */
}

/* State layer opacities (M3 INT-03) and disabled values (M3 BTN-05, INT-06) */
:root {
  --app-state-hover: 0.08;
  --app-state-focus: 0.10;
  --app-state-pressed: 0.10;
  --app-disabled-content: 0.38;
  --app-disabled-container: 0.10;
  --app-scrim-opacity: 0.32;          /* M3 ELV-09 */
}

/* Motion (M3 MOT-02, MOT-03) */
:root {
  --md-sys-motion-easing-standard: cubic-bezier(0.2, 0, 0, 1);
  --md-sys-motion-easing-standard-decelerate: cubic-bezier(0, 0, 0, 1);
  --md-sys-motion-easing-standard-accelerate: cubic-bezier(0.3, 0, 1, 1);
  --md-sys-motion-duration-short2: 100ms;
  --md-sys-motion-duration-short4: 200ms;
  --md-sys-motion-duration-medium1: 250ms;
}
```

Theme switching uses the selectors the color export already contains: no attribute = follow the system
(`prefers-color-scheme`), `data-theme="light"` and `data-theme="dark"` on `<html>` force a theme. Also set
`color-scheme: light dark` on `:root` (and `light` or `dark` with the forced attribute) so native controls (time
input, scrollbars) match (decision B-18).

Color roles, CSS (full set, generated from seed #2E7D32):

```css
/*
 * Material 3 color roles generated by m3tokens.py 0.1.0.
 * Seed #2E7D32, variant tonal-spot, name habit.
 * Approximate. Contrast between roles is preserved because luminance depends only on L* (= tone); hue and colorfulness differ slightly from the official tools. For exact values regenerate with Material Theme Builder or the material-color-utilities library.
 * Light values on :root; dark values via prefers-color-scheme and [data-theme="dark"].
 * Use the variables in components; never hardcode hex values.
 */
:root {
  --md-sys-color-primary: #396937;
  --md-sys-color-on-primary: #FFFFFF;
  --md-sys-color-primary-container: #BBF0B6;
  --md-sys-color-on-primary-container: #205121;
  --md-sys-color-secondary: #50644D;
  --md-sys-color-on-secondary: #FFFFFF;
  --md-sys-color-secondary-container: #D2E9CF;
  --md-sys-color-on-secondary-container: #384C36;
  --md-sys-color-tertiary: #14696B;
  --md-sys-color-on-tertiary: #FFFFFF;
  --md-sys-color-tertiary-container: #A4EFF1;
  --md-sys-color-on-tertiary-container: #004F52;
  --md-sys-color-error: #C00013;
  --md-sys-color-on-error: #FFFFFF;
  --md-sys-color-error-container: #FFDAD3;
  --md-sys-color-on-error-container: #93000C;
  --md-sys-color-surface: #F3FCF2;
  --md-sys-color-on-surface: #171D16;
  --md-sys-color-surface-variant: #DAE6D8;
  --md-sys-color-on-surface-variant: #40493F;
  --md-sys-color-surface-container-lowest: #FFFFFF;
  --md-sys-color-surface-container-low: #EDF6EC;
  --md-sys-color-surface-container: #E8F0E6;
  --md-sys-color-surface-container-high: #E2EAE1;
  --md-sys-color-surface-container-highest: #DCE5DB;
  --md-sys-color-surface-dim: #D4DCD3;
  --md-sys-color-surface-bright: #F3FCF2;
  --md-sys-color-inverse-surface: #2C322B;
  --md-sys-color-inverse-on-surface: #EAF3E9;
  --md-sys-color-inverse-primary: #A0D49B;
  --md-sys-color-outline: #707A6E;
  --md-sys-color-outline-variant: #BECABD;
  --md-sys-color-shadow: #000000;
  --md-sys-color-scrim: #000000;
  --md-sys-color-primary-fixed: #BBF0B6;
  --md-sys-color-primary-fixed-dim: #A0D49B;
  --md-sys-color-on-primary-fixed: #062100;
  --md-sys-color-on-primary-fixed-variant: #205121;
  --md-sys-color-secondary-fixed: #D2E9CF;
  --md-sys-color-secondary-fixed-dim: #B6CDB3;
  --md-sys-color-on-secondary-fixed: #0F1F0B;
  --md-sys-color-on-secondary-fixed-variant: #384C36;
  --md-sys-color-tertiary-fixed: #A4EFF1;
  --md-sys-color-tertiary-fixed-dim: #89D3D5;
  --md-sys-color-on-tertiary-fixed: #002021;
  --md-sys-color-on-tertiary-fixed-variant: #004F52;
}

@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --md-sys-color-primary: #A0D49B;
    --md-sys-color-on-primary: #03390B;
    --md-sys-color-primary-container: #205121;
    --md-sys-color-on-primary-container: #BBF0B6;
    --md-sys-color-secondary: #B6CDB3;
    --md-sys-color-on-secondary: #233521;
    --md-sys-color-secondary-container: #384C36;
    --md-sys-color-on-secondary-container: #D2E9CF;
    --md-sys-color-tertiary: #89D3D5;
    --md-sys-color-on-tertiary: #003738;
    --md-sys-color-tertiary-container: #004F52;
    --md-sys-color-on-tertiary-container: #A4EFF1;
    --md-sys-color-error: #FFB4A5;
    --md-sys-color-on-error: #690001;
    --md-sys-color-error-container: #93000C;
    --md-sys-color-on-error-container: #FFDAD3;
    --md-sys-color-surface: #0E150C;
    --md-sys-color-on-surface: #DCE5DB;
    --md-sys-color-surface-variant: #40493F;
    --md-sys-color-on-surface-variant: #BECABD;
    --md-sys-color-surface-container-lowest: #071105;
    --md-sys-color-surface-container-low: #171D16;
    --md-sys-color-surface-container: #1B211A;
    --md-sys-color-surface-container-high: #252C24;
    --md-sys-color-surface-container-highest: #30372F;
    --md-sys-color-surface-dim: #0E150C;
    --md-sys-color-surface-bright: #343B33;
    --md-sys-color-inverse-surface: #DCE5DB;
    --md-sys-color-inverse-on-surface: #2C322B;
    --md-sys-color-inverse-primary: #396937;
    --md-sys-color-outline: #899487;
    --md-sys-color-outline-variant: #40493F;
    --md-sys-color-shadow: #000000;
    --md-sys-color-scrim: #000000;
    --md-sys-color-primary-fixed: #BBF0B6;
    --md-sys-color-primary-fixed-dim: #A0D49B;
    --md-sys-color-on-primary-fixed: #062100;
    --md-sys-color-on-primary-fixed-variant: #205121;
    --md-sys-color-secondary-fixed: #D2E9CF;
    --md-sys-color-secondary-fixed-dim: #B6CDB3;
    --md-sys-color-on-secondary-fixed: #0F1F0B;
    --md-sys-color-on-secondary-fixed-variant: #384C36;
    --md-sys-color-tertiary-fixed: #A4EFF1;
    --md-sys-color-tertiary-fixed-dim: #89D3D5;
    --md-sys-color-on-tertiary-fixed: #002021;
    --md-sys-color-on-tertiary-fixed-variant: #004F52;
  }
}

[data-theme="dark"] {
  --md-sys-color-primary: #A0D49B;
  --md-sys-color-on-primary: #03390B;
  --md-sys-color-primary-container: #205121;
  --md-sys-color-on-primary-container: #BBF0B6;
  --md-sys-color-secondary: #B6CDB3;
  --md-sys-color-on-secondary: #233521;
  --md-sys-color-secondary-container: #384C36;
  --md-sys-color-on-secondary-container: #D2E9CF;
  --md-sys-color-tertiary: #89D3D5;
  --md-sys-color-on-tertiary: #003738;
  --md-sys-color-tertiary-container: #004F52;
  --md-sys-color-on-tertiary-container: #A4EFF1;
  --md-sys-color-error: #FFB4A5;
  --md-sys-color-on-error: #690001;
  --md-sys-color-error-container: #93000C;
  --md-sys-color-on-error-container: #FFDAD3;
  --md-sys-color-surface: #0E150C;
  --md-sys-color-on-surface: #DCE5DB;
  --md-sys-color-surface-variant: #40493F;
  --md-sys-color-on-surface-variant: #BECABD;
  --md-sys-color-surface-container-lowest: #071105;
  --md-sys-color-surface-container-low: #171D16;
  --md-sys-color-surface-container: #1B211A;
  --md-sys-color-surface-container-high: #252C24;
  --md-sys-color-surface-container-highest: #30372F;
  --md-sys-color-surface-dim: #0E150C;
  --md-sys-color-surface-bright: #343B33;
  --md-sys-color-inverse-surface: #DCE5DB;
  --md-sys-color-inverse-on-surface: #2C322B;
  --md-sys-color-inverse-primary: #396937;
  --md-sys-color-outline: #899487;
  --md-sys-color-outline-variant: #40493F;
  --md-sys-color-shadow: #000000;
  --md-sys-color-scrim: #000000;
  --md-sys-color-primary-fixed: #BBF0B6;
  --md-sys-color-primary-fixed-dim: #A0D49B;
  --md-sys-color-on-primary-fixed: #062100;
  --md-sys-color-on-primary-fixed-variant: #205121;
  --md-sys-color-secondary-fixed: #D2E9CF;
  --md-sys-color-secondary-fixed-dim: #B6CDB3;
  --md-sys-color-on-secondary-fixed: #0F1F0B;
  --md-sys-color-on-secondary-fixed-variant: #384C36;
  --md-sys-color-tertiary-fixed: #A4EFF1;
  --md-sys-color-tertiary-fixed-dim: #89D3D5;
  --md-sys-color-on-tertiary-fixed: #002021;
  --md-sys-color-on-tertiary-fixed-variant: #004F52;
}

[data-theme="light"] {
  --md-sys-color-primary: #396937;
  --md-sys-color-on-primary: #FFFFFF;
  --md-sys-color-primary-container: #BBF0B6;
  --md-sys-color-on-primary-container: #205121;
  --md-sys-color-secondary: #50644D;
  --md-sys-color-on-secondary: #FFFFFF;
  --md-sys-color-secondary-container: #D2E9CF;
  --md-sys-color-on-secondary-container: #384C36;
  --md-sys-color-tertiary: #14696B;
  --md-sys-color-on-tertiary: #FFFFFF;
  --md-sys-color-tertiary-container: #A4EFF1;
  --md-sys-color-on-tertiary-container: #004F52;
  --md-sys-color-error: #C00013;
  --md-sys-color-on-error: #FFFFFF;
  --md-sys-color-error-container: #FFDAD3;
  --md-sys-color-on-error-container: #93000C;
  --md-sys-color-surface: #F3FCF2;
  --md-sys-color-on-surface: #171D16;
  --md-sys-color-surface-variant: #DAE6D8;
  --md-sys-color-on-surface-variant: #40493F;
  --md-sys-color-surface-container-lowest: #FFFFFF;
  --md-sys-color-surface-container-low: #EDF6EC;
  --md-sys-color-surface-container: #E8F0E6;
  --md-sys-color-surface-container-high: #E2EAE1;
  --md-sys-color-surface-container-highest: #DCE5DB;
  --md-sys-color-surface-dim: #D4DCD3;
  --md-sys-color-surface-bright: #F3FCF2;
  --md-sys-color-inverse-surface: #2C322B;
  --md-sys-color-inverse-on-surface: #EAF3E9;
  --md-sys-color-inverse-primary: #A0D49B;
  --md-sys-color-outline: #707A6E;
  --md-sys-color-outline-variant: #BECABD;
  --md-sys-color-shadow: #000000;
  --md-sys-color-scrim: #000000;
  --md-sys-color-primary-fixed: #BBF0B6;
  --md-sys-color-primary-fixed-dim: #A0D49B;
  --md-sys-color-on-primary-fixed: #062100;
  --md-sys-color-on-primary-fixed-variant: #205121;
  --md-sys-color-secondary-fixed: #D2E9CF;
  --md-sys-color-secondary-fixed-dim: #B6CDB3;
  --md-sys-color-on-secondary-fixed: #0F1F0B;
  --md-sys-color-on-secondary-fixed-variant: #384C36;
  --md-sys-color-tertiary-fixed: #A4EFF1;
  --md-sys-color-tertiary-fixed-dim: #89D3D5;
  --md-sys-color-on-tertiary-fixed: #002021;
  --md-sys-color-on-tertiary-fixed-variant: #004F52;
}
```

Type scale, CSS (baseline M3 type scale; content text applies size and line height through the scaled `--app-type-*` variables above):

```css
/*
 * Material 3 baseline type scale (15 styles) as CSS custom properties, m3tokens.py 0.1.0.
 * Values: baseline M3 type scale shipped by the Material 3 libraries. The docs
 * (styles/typography/type-scale-tokens@2026-05-06) name the tokens md.sys.typescale.<role>-<size>.
 * {font, size, line-height, tracking, weight} but show the numeric table only as an image.
 * Sizes in sp = CSS px; size and line height emitted in rem (px / 16); tracking in em (tracking / size).
 * Font: display and headline use the brand typeface, the rest the plain typeface
 * (M3 typography: brand face for large styles, plain face for small ones); change the two --md-ref-typeface-*
 * values to use a brand font. Emphasized styles are not included.
 */
:root {
  --md-ref-typeface-brand: Roboto, "Noto Sans", system-ui, sans-serif;
  --md-ref-typeface-plain: Roboto, "Noto Sans", system-ui, sans-serif;
  --md-sys-typescale-display-large-font: var(--md-ref-typeface-brand);
  --md-sys-typescale-display-large-size: 3.5625rem; /* 57px */
  --md-sys-typescale-display-large-line-height: 4rem; /* 64px */
  --md-sys-typescale-display-large-weight: 400;
  --md-sys-typescale-display-large-tracking: -0.0044em; /* -0.25px */
  --md-sys-typescale-display-medium-font: var(--md-ref-typeface-brand);
  --md-sys-typescale-display-medium-size: 2.8125rem; /* 45px */
  --md-sys-typescale-display-medium-line-height: 3.25rem; /* 52px */
  --md-sys-typescale-display-medium-weight: 400;
  --md-sys-typescale-display-medium-tracking: 0em; /* 0px */
  --md-sys-typescale-display-small-font: var(--md-ref-typeface-brand);
  --md-sys-typescale-display-small-size: 2.25rem; /* 36px */
  --md-sys-typescale-display-small-line-height: 2.75rem; /* 44px */
  --md-sys-typescale-display-small-weight: 400;
  --md-sys-typescale-display-small-tracking: 0em; /* 0px */
  --md-sys-typescale-headline-large-font: var(--md-ref-typeface-brand);
  --md-sys-typescale-headline-large-size: 2rem; /* 32px */
  --md-sys-typescale-headline-large-line-height: 2.5rem; /* 40px */
  --md-sys-typescale-headline-large-weight: 400;
  --md-sys-typescale-headline-large-tracking: 0em; /* 0px */
  --md-sys-typescale-headline-medium-font: var(--md-ref-typeface-brand);
  --md-sys-typescale-headline-medium-size: 1.75rem; /* 28px */
  --md-sys-typescale-headline-medium-line-height: 2.25rem; /* 36px */
  --md-sys-typescale-headline-medium-weight: 400;
  --md-sys-typescale-headline-medium-tracking: 0em; /* 0px */
  --md-sys-typescale-headline-small-font: var(--md-ref-typeface-brand);
  --md-sys-typescale-headline-small-size: 1.5rem; /* 24px */
  --md-sys-typescale-headline-small-line-height: 2rem; /* 32px */
  --md-sys-typescale-headline-small-weight: 400;
  --md-sys-typescale-headline-small-tracking: 0em; /* 0px */
  --md-sys-typescale-title-large-font: var(--md-ref-typeface-plain);
  --md-sys-typescale-title-large-size: 1.375rem; /* 22px */
  --md-sys-typescale-title-large-line-height: 1.75rem; /* 28px */
  --md-sys-typescale-title-large-weight: 400;
  --md-sys-typescale-title-large-tracking: 0em; /* 0px */
  --md-sys-typescale-title-medium-font: var(--md-ref-typeface-plain);
  --md-sys-typescale-title-medium-size: 1rem; /* 16px */
  --md-sys-typescale-title-medium-line-height: 1.5rem; /* 24px */
  --md-sys-typescale-title-medium-weight: 500;
  --md-sys-typescale-title-medium-tracking: 0.0094em; /* 0.15px */
  --md-sys-typescale-title-small-font: var(--md-ref-typeface-plain);
  --md-sys-typescale-title-small-size: 0.875rem; /* 14px */
  --md-sys-typescale-title-small-line-height: 1.25rem; /* 20px */
  --md-sys-typescale-title-small-weight: 500;
  --md-sys-typescale-title-small-tracking: 0.0071em; /* 0.1px */
  --md-sys-typescale-body-large-font: var(--md-ref-typeface-plain);
  --md-sys-typescale-body-large-size: 1rem; /* 16px */
  --md-sys-typescale-body-large-line-height: 1.5rem; /* 24px */
  --md-sys-typescale-body-large-weight: 400;
  --md-sys-typescale-body-large-tracking: 0.0313em; /* 0.5px */
  --md-sys-typescale-body-medium-font: var(--md-ref-typeface-plain);
  --md-sys-typescale-body-medium-size: 0.875rem; /* 14px */
  --md-sys-typescale-body-medium-line-height: 1.25rem; /* 20px */
  --md-sys-typescale-body-medium-weight: 400;
  --md-sys-typescale-body-medium-tracking: 0.0179em; /* 0.25px */
  --md-sys-typescale-body-small-font: var(--md-ref-typeface-plain);
  --md-sys-typescale-body-small-size: 0.75rem; /* 12px */
  --md-sys-typescale-body-small-line-height: 1rem; /* 16px */
  --md-sys-typescale-body-small-weight: 400;
  --md-sys-typescale-body-small-tracking: 0.0333em; /* 0.4px */
  --md-sys-typescale-label-large-font: var(--md-ref-typeface-plain);
  --md-sys-typescale-label-large-size: 0.875rem; /* 14px */
  --md-sys-typescale-label-large-line-height: 1.25rem; /* 20px */
  --md-sys-typescale-label-large-weight: 500;
  --md-sys-typescale-label-large-tracking: 0.0071em; /* 0.1px */
  --md-sys-typescale-label-medium-font: var(--md-ref-typeface-plain);
  --md-sys-typescale-label-medium-size: 0.75rem; /* 12px */
  --md-sys-typescale-label-medium-line-height: 1rem; /* 16px */
  --md-sys-typescale-label-medium-weight: 500;
  --md-sys-typescale-label-medium-tracking: 0.0417em; /* 0.5px */
  --md-sys-typescale-label-small-font: var(--md-ref-typeface-plain);
  --md-sys-typescale-label-small-size: 0.6875rem; /* 11px */
  --md-sys-typescale-label-small-line-height: 1rem; /* 16px */
  --md-sys-typescale-label-small-weight: 500;
  --md-sys-typescale-label-small-tracking: 0.0455em; /* 0.5px */
}
```

Shape scale, CSS (this screen uses none, extra-small, medium, extra-large and full; the large-increased, extra-large-increased and extra-extra-large steps are M3 Expressive and not used):

```css
/*
 * Material 3 shape (corner radius) scale, m3tokens.py 0.1.0.
 * Values: M3 SHP-01 (styles/shape/corner-radius-scale@2026-05-06), 1dp = 1 CSS px.
 * Token names follow md.sys.shape.corner.<step> (used in the component spec tables).
 * large-increased, extra-large-increased and extra-extra-large are M3 Expressive additions
 * (styles/shape/overview-principles@2026-05-06). full = fully rounded (pill), not 50%.
 */
:root {
  --md-sys-shape-corner-none: 0px;
  --md-sys-shape-corner-extra-small: 4px;
  --md-sys-shape-corner-small: 8px;
  --md-sys-shape-corner-medium: 12px;
  --md-sys-shape-corner-large: 16px;
  --md-sys-shape-corner-large-increased: 20px;
  --md-sys-shape-corner-extra-large: 28px;
  --md-sys-shape-corner-extra-large-increased: 32px;
  --md-sys-shape-corner-extra-extra-large: 48px;
  --md-sys-shape-corner-full: 9999px;
}
```

## Decisions

- B-01 Window classes: only compact is designed (360-412dp, as requested). Medium and wider reuse the compact layout,
  app bar full width, content column max 600dp centered. Reason: the request targets phones; a centered column keeps
  labels next to their switches and radios on wide windows. Affects: section 3, AC-03.
- B-02 Color scheme generated from seed #2E7D32 (tonal-spot, approximate; see "Scheme note"). Reason: brand seed
  given, no project tokens. Affects: section 10, AC-29.
- B-03 Settings is a secondary screen opened from the app's main screen and left with Back; no navigation bar or
  rail on it. Users are phone users in short, often one-handed sessions. Reason: no app navigation was described;
  M3 LAY-36 fits a single-task screen. Affects: sections 1, 3, 6.
- B-04 Account summary is display-only (no profile editing); avatar shows initials on primary-container /
  on-primary-container, title-medium. Reason: the request lists name and email only; editing is out of scope.
  Affects: sections 2, 4, 5.
- B-05 Defaults: reminder off, reminder time 20:00, theme System default, text size Medium, week starts Monday.
  Reason: neutral defaults; System default respects the device theme. Affects: sections 2, 5.
- B-06 Reminder time is an inline outlined text field wrapping a native `<input type="time">`, not the M3 time
  picker dialog (inspired departure from M3 TMP-01 and TMP-02). Reason: no framework; the native input gives the
  locale's 12 or 24-hour format, typed entry (TMP-03) and the system picker on Android with one tap less. Field label
  type: body-large at rest and body-small when floated; supporting text body-small; hover outline on-surface;
  disabled outline on-surface 10% (aligned with M3 BTN-05). Affects: sections 4, 5, 6, AC-08, AC-17.
- B-07 Single-choice settings (Theme, Text size, Week starts on) are inline radio groups, not segmented buttons or
  list-row-plus-dialog. Each option row is a native `<label>` and the whole 56dp row is the target and carries the
  state layer; the radio icon sits in a 24dp leading slot. The switch row works the same way. Reason: all options
  stay visible and apply in one tap; labels can wrap at 200% text, which segmented buttons cannot (M3 SEG, review
  checks). Affects: sections 4, 5.
- B-08 Text size scale: Small 0.875, Medium 1, Large 1.25, applied as `--app-text-scale` to every content type
  style, with a floor of 0.75rem (12px) for size and 1rem for line height. Reason: "Small" must never take content
  text below 12px (M3 A11-30); the floor keeps it compliant. Pending Q-01 for the exact multipliers. Affects:
  sections 6, 10, AC-23, AC-24.
- B-09 Section structure and type: five sections (Account, Reminders, Appearance, Calendar, Data; "Week starts on"
  goes under Calendar). Section headings title-small in primary; legends label-large in on-surface-variant; no
  leading icons in rows; no dividers. Spacing: heading 16dp top / 8dp bottom; legend 8dp / 8dp; time field 8dp above,
  16dp below. Reason: settings lists scan by headings; space groups better than lines (M3 DIV-02). Affects: section 3, 4.
- B-10 App bar sticks to the top while content scrolls; bottom padding 16dp plus safe area. Reason: Back stays
  reachable. Affects: section 3.
- B-11 Dialogs: no shadow (level3 shown by surface-container-high and the scrim); width min(560dp, 100vw - 48dp);
  headline headline-small, body body-medium. Below a 328dp window (only at high zoom) the width drops under the
  280dp minimum of M3 DLG-02 (inspired departure). Reason: no horizontal scrolling at 200% zoom (M3 A11-08 wins).
  Affects: section 4, AC-14.
- B-12 Destructive styling: "Delete all data" row label and the dialog's "Delete" button use the error role instead
  of primary (inspired departure from M3 BTN-04 for text buttons). Delete removes habits and check-in history on the
  device and in the account; the account and settings stay. It needs a connection (offline: row disabled, TXT-26).
  Reason: signal the irreversible action by color plus wording; scope pending Q-02. Affects: sections 4, 5, 6.
- B-13 Short waits use the baseline indeterminate circular progress indicator (24dp in the Export row, 20dp in the
  dialog button), not the Expressive loading indicator (M3 LDI-01 is tier E). Under 200 ms nothing is shown
  (M3 LDI-02). Under reduced motion the indicator is hidden and the text carries the state. Account skeleton: two
  bars 12dp tall, 160dp and 200dp wide, surface-container-highest, corner full. Affects: sections 4, 5, 7.
- B-14 Offline status row at the top of the content while offline (surface-container-high, corner medium 12dp,
  padding 16dp, cloud_off icon). Reason: a PWA keeps working offline; the user must know edits are queued.
  Affects: sections 4, 5.
- B-15 Snackbar: no action on this screen, auto-dismiss after 6 s (within M3 SNB-04), 16dp side padding, 16dp from
  the window sides and above the safe area, body-medium text, no shadow; enters with a 16dp upward slide. Success is also shown inline (TXT-21) as
  M3 SNB-06 requires on the web. Affects: sections 4, 6.
- B-16 Sign out is immediate when everything is synced; a confirmation dialog appears only when unsynced changes
  would be lost. Reason: avoid friction on a reversible action, protect data when it is not. Affects: section 6.
- B-17 Focus ring: 3dp solid secondary, offset 2dp (inset -3dp on full-width rows), following the element's shape.
  Reason: M3 INT-12 requires a ring but the references give no size; secondary meets 3:1 on every surface used.
  Affects: section 5, AC-25.
- B-18 Persistence and theming: settings in localStorage (key `settings`) and synced to the account; a small inline
  script in `<head>` applies `data-theme`, `data-text-size` and the `theme-color` meta (#F3FCF2 light, #0E150C dark)
  before first paint; `color-scheme` set to match; theme and text-size changes repaint without animation; scroll
  position not restored. Affects: sections 5, 6, 7, AC-21, AC-22.
- B-19 Reminder permission: turning the switch on requests `Notification` permission; the switch shows on only after
  permission is granted; denied keeps it off with TXT-09; no Notification API disables the row with TXT-10.
  Affects: sections 5, 6.
- B-20 Copy in US English, sentence case; times and dates formatted with `Intl.DateTimeFormat` in the device locale.
  Affects: section 8.

## Acceptance criteria

Layout
- [ ] AC-01 [LAY-16] At 360, 390 and 412 px, row text starts 16 px from the left window edge and trailing controls
  end 16 px from the right edge. Check: measure in browser developer tools.
- [ ] AC-02 [APB-01] At 390 px, the top app bar is 64 px tall, full width, square corners, shows Back and "Settings"
  and no other actions. Check: measure the header element.
- [ ] AC-03 [project, B-01] At 1024 px, the content column is 600 px wide and centered; the app bar spans the window.
  Check: resize to 1024 px and measure.
- [ ] AC-04 [WRT-04] At 360 px with browser text size 200% and in-app text size Large, the page scrolls only
  vertically: `document.documentElement.scrollWidth` equals the viewport width. Check: run in the console.
- [ ] AC-05 [APB-06] After scrolling the content by any amount, the app bar fill changes from surface to
  surface-container (#E8F0E6 light, #1B211A dark) with no box-shadow. Check: computed styles before and after scroll.

Components
- [ ] AC-06 [LST-01] Sign out and each radio row are at least 56 px tall; account, Daily reminder, Export and Delete
  rows at least 72 px. Check: measure each row at 390 px.
- [ ] AC-07 [SWT-01] The switch track is 52 x 32 px; the handle is 16 px when off and 24 px when on. Check: measure
  in both states.
- [ ] AC-08 [TXF-05] The Reminder time field shows the visible label "Reminder time" in every state, including when
  filled. Check: visual inspection with and without a value.
- [ ] AC-09 [TXF-04] The Reminder time field outline contrasts at least 3:1 with the page (#707A6E on #F3FCF2 light,
  #899487 on #0E150C dark). Check: contrast checker on the computed colors.
- [ ] AC-10 [RAD-04] Theme, Text size and Week starts on are each a `<fieldset>` with a `<legend>` and 3, 3 and 2
  vertically stacked radio options with visible labels. Check: inspect the DOM.
- [ ] AC-11 [project, B-12] The "Delete all data" label and the dialog "Delete" button render in error (#C00013
  light, #FFB4A5 dark). Check: computed color in both themes.
- [ ] AC-12 [DLG-01] The delete dialog container is surface-container-high (#E2EAE1 / #252C24) with 28 px corners
  over a scrim of #000000 at 32%. Check: computed styles of `dialog` and `::backdrop`.
- [ ] AC-13 [DLG-03] The delete dialog has exactly two actions, trailing aligned, "Delete" nearest the right edge.
  Check: visual inspection at 390 px.
- [ ] AC-14 [project, B-11] At 390 px the dialog is 342 px wide; at 1024 px it is 560 px wide. Check: measure.
- [ ] AC-15 [SNB-02] The snackbar uses inverse-surface (#2C322B / #DCE5DB) with inverse-on-surface text and 4 px
  corners, and shows only one at a time. Check: export twice quickly; inspect computed styles and count snackbars.

States
- [ ] AC-16 [INT-01] The selected radio, the switch on state and the focused field each differ from their unselected
  or idle state by at least two visual cues (radio: inner dot plus color; switch: handle position plus size plus
  color; field: 3 px outline plus label color). Check: compare in grayscale (developer tools color-vision emulation).
- [ ] AC-17 [INT-06] With Daily reminder off, the Reminder time field renders at 38% on-surface and is skipped by Tab.
  Check: switch off, then Tab through the screen.
- [ ] AC-18 [TXF-03] Clearing the time value shows "Enter a time" in error with an error icon, and the stored time
  is unchanged after reload. Check: clear the field, blur, reload.
- [ ] AC-19 [LDI-02] When the CSV export takes over 200 ms (throttle to slow 3G or add a test delay), the Export row
  shows "Preparing your file…" and a progress indicator named "Exporting data"; under 200 ms no indicator flashes.
  Check: run both cases and watch the row and the accessibility tree.
- [ ] AC-20 [project, B-14] With the network offline (developer tools), the offline status row TXT-32 appears at the
  top of the content and Delete all data is disabled with TXT-26, while Export still works. Check: toggle offline.

Interaction
- [ ] AC-21 [project, B-18] Selecting Dark sets `data-theme="dark"` on `<html>` and repaints at once; after reload no
  light frame appears before the dark theme. Check: select Dark, reload with a performance recording, inspect frames.
- [ ] AC-22 [project, B-18] With System default selected, switching the OS or emulated `prefers-color-scheme` between
  light and dark changes the theme without reload, and `theme-color` follows (#F3FCF2 / #0E150C). Check: developer
  tools rendering emulation.
- [ ] AC-23 [project, B-08] Selecting Large makes body-large text 20 px; selecting Small makes it 14 px; Medium 16 px.
  Check: computed font-size of a row label for each option.
- [ ] AC-24 [A11-30] With in-app text size Small, no content text on the screen computes below 12 px. Check: script
  over all text nodes comparing computed font-size.
- [ ] AC-25 [A11-05] Every focusable element shows a 3 px secondary focus ring (#50644D light, #B6CDB3 dark) when
  reached with Tab. Check: tab through the whole screen in both themes.
- [ ] AC-26 [A11-11] Opening the delete dialog puts focus on "Cancel"; Tab cycles only inside the dialog; Escape
  closes it and focus returns to "Delete all data". Check: keyboard only.
- [ ] AC-27 [A11-33] After a successful deletion, focus is on the "Data" heading, the snackbar "All habit data
  deleted" is announced, and Export and Delete show "No habit data yet". Check: keyboard and a screen reader.
- [ ] AC-28 [SNB-05] The snackbar is announced politely, never receives focus, and disappears after 6 s. Check:
  screen reader and a timer; `document.activeElement` unchanged.

Accessibility and tokens
- [ ] AC-29 [A11-03] All text pairs listed in "10. Tokens" meet 4.5:1 and non-text pairs 3:1 in both themes, also
  after any regeneration of the scheme. Check: contrast checker on computed colors, or re-run the scheme check.
- [ ] AC-30 [A11-01] At 390 px every interactive element has a hit area of at least 48 x 48 px (Back, dialog buttons,
  rows, field). Check: measure each bounding box.
- [ ] AC-31 [A11-02] The 48 x 48 px minimum hit area of each control is at least 8 px from the next one: dialog buttons
  are 8 px apart, and contiguous 56 px rows leave at least 4 px above and below a centered 48 px area. Check: measure
  at 390 px.
- [ ] AC-32 [A11-31] The accessible name of each control contains its visible label (for example the switch is named
  "Daily reminder"); Back is named "Back". Check: accessibility tree in developer tools.
- [ ] AC-33 [A11-32] In each radio group, arrow keys move and select, and Tab enters and leaves the group in one
  stop. Check: keyboard only.
- [ ] AC-34 [A11-10] Every task in section 1 (toggle reminder, set time, change theme, text size and week start,
  export, delete, sign out) can be completed with Tab, arrows, Enter, Space and Escape only. Check: keyboard only.
- [ ] AC-35 [A11-35] The screen exposes one h1 "Settings" and an h2 for each of the five sections. Check: screen
  reader heading list.
- [ ] AC-36 [A11-08] At 390 px with browser text size 200% and in-app Large, no text is clipped, overlapped or
  ellipsized; all rows, field and dialog content remain readable and operable. Check: visual pass top to bottom with
  the delete dialog open and closed.
- [ ] AC-37 [A11-15] With `prefers-reduced-motion: reduce`, the screen, dialog and switch change without movement,
  the snackbar only fades and no progress indicator spins. Check: developer tools rendering emulation.

## Open questions

- Q-01 Text size multipliers: are Small 0.875, Medium 1 and Large 1.25 right, and should "Large" go further (for
  example 1.5)? Whatever the values, content text never goes below 12 px (M3 A11-30). Default until answered: B-08.
  Blocks: none.
- Q-02 Scope of "Delete all data": habits and check-in history only (account and settings kept), or also delete the
  account? Default until answered: habits and history only (B-12). Blocks: TXT-28 wording, section 6.

## Validation

1. With m3-design-review: "Review the Settings screen against Material 3 with this brief as project guidelines", at
   360, 390 and 412 px, plus 1024 px for AC-03 and AC-14, in light and dark themes, with in-app text size Small,
   Medium and Large, browser text size 200%, and with the network offline. The report's "Brief acceptance criteria"
   section lists every AC as pass, fail or not checked.
2. By hand: go through the AC checklist at each width and theme; measure hit areas and contrast with browser
   developer tools; tab through the screen and both dialogs; set text to 200% with in-app Large; turn on reduced
   motion; emulate offline and a denied notification permission.
