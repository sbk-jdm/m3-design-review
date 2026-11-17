# Brief method: how to decide

How to make the design decisions of a brief. Every decision cites a rule ID from the shared references (layout,
color, styles, components, expressive files), a project guideline, or becomes a decision `B-nn` with a one-line
reason. Values in the brief are copied from the cited rule rows, never typed from memory. Precedence: tier F >
project > tier C > tier E.

## 1. Start from user tasks

1. List the users and their 1-3 main tasks for the surface, with frequency and context (on the move, at a desk,
   one hand). Unknown: assume, and record as `B-nn`.
2. Pick one primary task per screen (LAY-48). It gets the most prominent control: one filled button (BTN-07) or one
   FAB for a constructive primary action (FAB-03; never destructive). Secondary tasks are discoverable but quieter
   (tonal, outlined, text buttons; ICB-05 for icon buttons).
3. Content inventory: for each task, the data and controls it needs, in priority order. This order is the reading
   order and the focus order (A11-06, A11-19). Drop anything no task needs.
4. Success: what the user sees when the task is done (result in place, snackbar, new view). It becomes an AC.

## 2. Navigation

Choose by the number of top-level destinations and by window size class (LAY-08, LAY-11):

| Situation | Compact (< 600) | Medium (600-839) | Expanded and up (840+) |
| --- | --- | --- | --- |
| 3-5 top-level destinations | Navigation bar (NVB-01, NVB-06, LAY-37) | Navigation rail (NVR-05), or bar with two panes (LAY-08) | Navigation rail, collapsed or expanded (LAY-08, LAY-09) |
| 6 or more destinations, or deep hierarchy | Modal navigation drawer or modal expanded rail (NVD-02, LAY-08) | Modal drawer or rail (NVD-02, NVR-04: 3-7 items) | Standard drawer or expanded rail (NVD-02) |
| 2 or more peer views inside one destination | Tabs (TAB-04: up to 4 fixed, scrollable beyond) | Tabs | Tabs |
| Single task or detail view | Top app bar with back and 1-2 actions (LAY-36, APB-05) | Same | Same, or detail pane of list-detail (LAY-43) |

- Only one primary navigation component per window class (NVD-03); swap only equivalent components across classes
  (bar to rail, LAY-11). No toolbar together with a navigation bar (TLB-04).
- No swiping between navigation bar destinations (NVB-08); top-level changes use a quick fade (MOT-11).
- Exactly one active destination with a visible indicator (INT-18, NVB-03, NVR-03); labels on every item (ICO-07).
- Focus after a destination change: A11-33. Back from a detail view returns focus to the item that opened it.

## 3. Components by function

Classify by what the control does (CMP-01), then take the component's specs from its rule rows (size, shape, color
roles, type role, target). Do not choose by look.

| Need | Component | Key rules |
| --- | --- | --- |
| Trigger the primary action | Filled button (one per screen), or FAB / extended FAB | BTN-01..BTN-07, FAB-03, FAB-06, EFB-03, EFB-05 |
| Secondary or repeated actions | Tonal, outlined or text button; icon button; app bar actions | BTN-04, ICB-05, APB-05 |
| A main action with alternatives | Split button | SPB-01..SPB-06 |
| Switch view or sort, 2-5 options, single select | Segmented button (connected button group in Expressive) | SEG-01, SEG-05, CMP-01, BGR-04 |
| Filter a collection | Filter chips | CHP-05, CHP-06, CHP-04 |
| Swap content panels | Tabs | TAB-01..TAB-06, A11-32 |
| Binary setting that applies immediately | Switch with a visible label | SWT-05, SWT-06 |
| One of up to 5 options | Radio buttons | RAD-04 |
| Several options, or a parent with children | Checkboxes | CHK-04, LST-05 |
| One of many options, or actions on an item | Menu | MNU-01..MNU-06, A11-34 |
| Enter text | Text field, one variant per region | TXF-03, TXF-05, TXF-06 |
| Pick a date or time | Date picker, time picker (typed entry always available) | DTP-05, TMP-03 |
| Pick a value in a range | Slider | SLD-02, SLD-03, SLD-06 |
| A homogeneous collection | List | LST-01..LST-07 |
| Heterogeneous items, each a unit | Cards (actionable card holds no buttons) | CRD-01, CRD-06 |
| Browse a few visual items | Carousel with a show-all path | CAR-01 |
| Confirm, decide, or enter a short form | Dialog; full-screen dialog at compact only | DLG-01, DLG-03, DLG-05, DLG-06, LAY-10 |
| Supplemental options or content | Bottom sheet at compact; menu or side sheet at medium and up | LAY-10, LAY-45, SSH-03, BSH-06 |
| Brief feedback after an action | Snackbar (one at a time, at most one action) | SNB-03..SNB-06 |
| Wait for a result | Loading indicator 200 ms-5 s, progress indicator over 5 s, nothing under 200 ms | LDI-02, PRG-05 |
| Search | Search bar and view | SRC-04, SRC-06 |
| Group content | Space first, dividers when needed | LAY-33, DIV-02 |

If the project already ships a custom component for the function, keep it (mark `project`) and specify the M3 rules
it must still meet (tier F always, tier C as far as the guidelines allow).

## 4. Layout per window size class

For each window class in scope, specify a row from the layout rules; values come from the cited rows:

| Item | Rule IDs |
| --- | --- |
| Window margins (16dp compact; 24dp medium and up) | LAY-16 |
| Pane count, spacer (24dp) and pane widths (fixed pane 360dp expanded, 412dp large and up) | LAY-03, LAY-17, LAY-18, LAY-19, LAY-21 |
| Canonical layout: feed, list-detail or supporting pane | LAY-40..LAY-44 |
| Navigation component (section 2) | LAY-08 |
| Line length of body text 40-60 characters | LAY-07 |
| Dialogs and supplemental selection | LAY-10 |
| Reflow on resize, rotate and unfold without reload | LAY-12 |
| Reachability of essential actions; safe areas | LAY-13, LAY-38 |
| Text fields not full width on large screens | TXF-06 |
| RTL, if the product ships right-to-left languages | LAY-50..LAY-56 |

Describe each layout as an ordered list of regions (app bar, navigation, panes, bottom elements); a text wireframe is
optional. Say what moves, hides or changes between classes (LAY-26, LAY-46) and which layout an undesigned class uses.

## 5. Foundations to specify

- Color: every element gets a role, never a raw hex (COL-01); foreground uses the `on-*` pair of its fill (COL-02);
  page on `surface`, navigation area on `surface-container` (COL-17); nested containers follow the container order
  (COL-18); dividers `outline-variant` (COL-20); interactive borders `outline` (COL-22). Both themes from one role
  set (COL-28). Extra semantic colors (success, warning) as static roles with four parts (COL-32, COL-34).
- Type: every text element gets a role and size (TYP-01; buttons label-large, app bar titles per APB-02). Changing
  or aligned numbers use tabular figures (TYP-12). Web sizes in rem (TYP-13).
- Shape: each component maps to one step of the scale (SHP-01, SHP-02), as its component rows state (buttons full,
  dialogs 28dp per DLG-01).
- Elevation: resting levels 0-3 and tonal separation by default (ELV-02, ELV-03, ELV-05); scrim for modals (ELV-09).
- Spacing: 8dp scale, padding and gaps on the parent (SPC-01, SPC-03); unchanged at 200% text (SPC-05).
- Icons: 24dp default, one style (ICO-01, ICO-02); 48dp target (ICO-04).

## 6. States

Specify a state table for every interactive element and every data view. A state that does not apply is written
`n/a` with the reason (for example FAB-05: a FAB is never disabled; INT-08 lists components without a disabled state).

Interactive elements:

| State | What to specify | Rules |
| --- | --- | --- |
| Default (enabled) | Container and content roles, shape, size | component rows |
| Hover (pointer) | State layer 8% of the content color | INT-03, INT-04, INT-09 |
| Focus (keyboard) | State layer 10% plus a visible focus ring | INT-03, INT-12, A11-05 |
| Pressed | State layer 10%, ripple | INT-03, INT-13 |
| Disabled | Content on-surface 38%, container on-surface 10% (for buttons, BTN-05); not focusable | INT-06, INT-07 |
| Selected / activated | At least two cues (color plus check, icon fill, weight or indicator) | INT-01, INT-17, ICB-04 |
| Dragged, if draggable | State layer 16%, single-pointer alternative | INT-03, INT-15, CRD-05, BSH-05 |

Data views (lists, feeds, charts, detail panes, forms):

| State | What to specify | Rules |
| --- | --- | --- |
| Loading | Skeleton or indicator by expected wait; no layout jump when content arrives | LDI-02, PRG-05, MOT-10 |
| Empty | What the user sees and the action that fills it; empty detail pane shows a placeholder | LAY-43, heuristic |
| Error | Message near the cause, a recovery action; field errors with the error role and supporting text | TXF-03, SNB-06 |
| Offline, if the product works offline or syncs | What stays available, what is queued, how sync status is shown | heuristic |
| Long content | Wrap or truncate with a reveal path; 200% text without loss | WRT-07, A11-09, A11-08 |
| Partial or stale data, if relevant | How it is marked (text, not color alone) | A11-29 |

## 7. Content and copy

- Write the actual strings in a copy table (ID, text, notes) in the product's language; no lorem ipsum.
- Buttons 1-3 words, sentence case, one line (BTN-06); chip labels at most 20 characters (CHP-04); navigation
  rail labels one word (NVR-04); dialog headlines brief, no apologies or "Are you sure?" (DLG-07).
- Every field has a visible label (TXF-05); hint text is the search label (SRC-06).
- Link and button text says what it does; no repeated generic "Learn more" (A11-23); alt text up to 125 characters
  (A11-27); decorative images hidden (A11-25).
- Error and empty messages say what happened and what to do next (heuristic); keep terminology consistent with the
  project's glossary (`project`).
- Plan for longer translations and 200% text: wrap where critical (WRT-07), never lose content (WRT-06).

## 8. Accessibility floor as acceptance criteria

Every brief turns the floor into ACs for its scope (format: brief-template.md, "Acceptance criteria rules"):

| AC topic | Rules |
| --- | --- |
| Hit area at least 48 x 48dp (44 for pointer-only surfaces), 8dp between targets | A11-01, A11-02, A11-16, A11-17, LAY-28 |
| Text contrast 4.5:1 (3:1 large); non-text and interactive boundaries 3:1 | A11-03, COL-05, COL-06, COL-08, BTN-08 |
| States with two cues; color never the only cue in data and status | A11-04, A11-29 |
| Visible focus, logical order, full keyboard operation, arrows in composite widgets | A11-05, A11-06, A11-10, A11-32 |
| Focus into and back from dialogs, sheets, menus; after view changes | A11-11, A11-33, A11-34 |
| Labels, label in name, headings, landmarks | A11-07, A11-31, A11-35, A11-20 |
| 200% text without loss; content text at least 12 CSS px | A11-08, A11-30 |
| Reduced motion honored | A11-15 |

Add the component-specific tier F rows of the chosen components (for example DLG-06, SNB-04, SNB-05, TXF-05,
CHP-03). A project may raise a threshold (adapter review setup), never lower it.

## 9. Motion

Specify motion only where it helps a task (orientation, feedback, continuity). For each: trigger, property, easing
and duration tokens (MOT-02, MOT-03; exit shorter than enter, MOT-04), pattern (MOT-11..MOT-16), and the
reduced-motion fallback: a short fade or no animation (MOT-06, A11-15). A motion without a fallback is not allowed.

## 10. Expressive (tier E)

Default to baseline M3. Use Expressive only when the user asks or the project guidelines adopt it. Then: check
platform availability (EXP-01..EXP-05; web has no official Expressive components), pick one motion scheme (EXP-30,
MOT-08), keep hero moments rare (EXP-15), do not mix baseline and Expressive sizes within a component family (EXP-41),
and take replacements for parts no longer recommended from EXP-40. Floors still apply.

## 11. Decisions and questions

- `B-nn` decision: an assumption or a choice the brief makes so the implementer need not ask (window classes,
  seed color, a departure from tier C in `inspired` mode). One line: what, and why.
- `Q-nn` question: only what the user or project must decide and the brief cannot assume. Mark affected sections
  "pending Q-nn" and give the default that applies until answered.
- Never resolve a tier F conflict with a decision: specify the compliant value and ask (`Q-nn`).
