# Brief templates

Use the template of the mode exactly: keep section order and headings (translated into the user's language; IDs,
tokens and code unchanged). Omit a section only when it cannot apply, and then write one line saying why. Replace
every `<...>` placeholder; never leave one in a delivered brief. Every brief has, in this order: header, Handoff
prompt, the mode's body, Decisions, Acceptance criteria, Open questions, Validation.

Value marks, used in every table and spec line: `M3 <RULE-ID>` (value taken from that rule row), `project` (from the
project guidelines, tokens or ledger; name the file once in the header), `decision B-nn`. IDs: decisions `B-01`...,
acceptance criteria `AC-01`..., open questions `Q-01`..., changes `C-01`... (mode `change`), groups `G-1`....

## Common header

```
# Design brief: <title>

Mode: <system | screen | change>   Date: <YYYY-MM-DD>   Status: draft
Platform and stack: <web, CSS custom properties | web, Tailwind | Android, Jetpack Compose | Flutter | other: ...>
Window size classes: <e.g. compact (< 600dp), expanded (840-1199dp); medium uses the compact layout (B-01)>
Themes: <light and dark; contrast level standard>   Tolerance: <inspired | strict> (<default | set by user | project>)
Sources: Material Design 3 references, snapshot <date> (rule IDs cite https://m3.material.io/<path> as path@lastmod)
  Project guidelines: <path and sections used | none>   Decisions ledger: <path, N deviations applied | none>
  <change mode only> Review: <report title and date>; decisions: <e.g. accept F-01..F-06, N-01>
Color scheme: <project tokens | generated from seed #RRGGBB, approximate tonal-spot; exact values can be regenerated
  from the seed with Material Theme Builder or material-color-utilities | pending Q-nn>
```

If the snapshot is more than 6 months older than the brief date, add: "References are older than 6 months: check
tier C values against https://m3.material.io/ before implementing; floor criteria stand."

## Handoff prompt

Put this block right after the header, in the user's language, filled in for the mode. It must work pasted alone
with the brief into any AI tool, without this skill.

```
Implement the design brief below exactly. <screen/change: Scope: <screens, components or files>.> Stack: <stack>.
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

Mode `system`: replace the first line with "Apply these design guidelines to every screen you design or build in
this project. When a screen brief exists, it adds to these guidelines; if they conflict, ask." and step 6 with
"Before delivering a screen, check it against the acceptance criteria and list any you could not meet."

## Template: system

````
<header>

## Handoff prompt
<block>

## 1. Product context
Users and main tasks; platforms; window size classes supported; themes; accessibility level; privacy rules.

## 2. Foundations
### Color
Scheme source (project tokens or seed and method). Role table, both themes:
| Role | Light | Dark | Use in this product | Source |
| --- | --- | --- | --- | --- |
| primary / on-primary | #...... / #...... | #...... / #...... | Primary action, active states | M3 COL-12 |
Extra semantic or brand roles (four parts each, both themes, contrast checked; COL-32, COL-34). Contrast check result
(pairs checked, failures and how they were fixed).
### Typography
Font families and fallback chain (TYP-16). Role map: | Role | Size / line height / weight / tracking | Used for | Source |
### Shape
| Component or group | Corner step | Value | Source |
### Elevation
Levels used and where (ELV-01..ELV-03), tonal separation, scrim.
### Spacing
Scale and standard values: window margins, pane spacer, card padding, list insets, gaps (SPC-01, LAY-16, LAY-17).
### Icons
Set, style, sizes, fill for selected state (ICO-01, ICO-02, ICO-08).
### Motion
Scheme (baseline easing and duration, or Expressive springs if adopted), tokens per transition type, reduced-motion
fallback (MOT-06).

## 3. Layout
Per window class: margins, panes and widths, navigation component, canonical layouts used. Reflow rules.

## 4. Component rules
| Function | Component and variant | Size | Shape | Color roles | Notes | Source |
One row per component the product uses; project defaults (for example "all dialogs basic, never full-screen at
expanded"). Rules for choosing between similar components (CMP-01).

## 5. Patterns
States (state layers, focus ring, disabled, selected), loading, empty, error, offline if relevant, forms and
validation, feedback (snackbar, inline), confirmation and destructive actions, dialogs and sheets per window class.

## 6. Content and copy
Voice, casing, terminology table, number, date and currency formats, error and empty message patterns.

## 7. Project exceptions
Deviations from M3 the project keeps (ledger format, so they can be appended to the decisions ledger):
| Date | Rule ID | Scope | Decision | Rationale | Finding |
| <date> | SHP-02 | all buttons | deviation | <reason> | B-03 |
Project conventions M3 does not address: | Date | Convention | Scope | Rationale | Candidate |

## 8. Do and don't
Short paired list, each item with its source.

## 9. Tokens
Token export pasted inline, one code block per format the project uses (color, then type and shape).

## 10. Review setup
```
## Review setup
Widths to test: <e.g. 360, 390, 1280>
Themes to test: <light, dark>
Text-size settings to test: <browser 200%; in-app setting values>
Privacy state to review: <how to switch on a demo or privacy mode | none>
Minimum text size: <12 or higher>
```

## Decisions
## Acceptance criteria
## Open questions
## Validation
````

## Template: screen

````
<header>

## Handoff prompt
<block>

## 1. Purpose
Users, primary task (one), secondary tasks, what success looks like. Scope: in / out.

## 2. Content inventory
| # | Item | Type (data, control, text) | Priority | Data source and sample | Notes |
Order = reading and focus order.

## 3. Layout
### Compact (< 600dp)
Ordered regions: <top app bar: title, actions>, <content: ...>, <navigation bar>, <FAB>. Margins, gaps, scroll.
### Expanded (840-1199dp)
Navigation rail, panes (count, widths, spacer), what moves or changes. <Repeat for each class in scope; for classes
not designed, say which layout applies.>
Optional text wireframe.

## 4. Components
One block per component:
```
<Name in this screen>: <M3 component, variant, size>   Function: <what it does> (CMP-01)
Container: <role> <hex light / hex dark>, <shape step and value>, <elevation level>   Source: <M3 ID | project | B-nn>
Content: <label role and type role>, <icon name and size>   Target: <hit area>   Source: <...>
Behavior: <on activate ...>   Label / accessible name: <text>
```

## 5. States
Per interactive element: | Element | Default | Hover | Focus | Pressed | Disabled | Selected | Source |
Per data view: | View | Loading | Empty | Error | Offline (if relevant) | Long content | Source |
Write the actual cues and values (for example "state layer on-surface 10% plus 2dp focus ring, primary").

## 6. Interactions and navigation
| Trigger | Result | Focus after | Keyboard | Source |
Back behavior, deep links, what persists (selection, scroll position, unread state).

## 7. Motion
| Transition | Pattern | Easing and duration | Reduced motion | Source |

## 8. Copy
| ID | Text | Where | Notes (max length, casing, variables) |

## 9. Accessibility
Headings and landmarks, focus order, labels for icon-only controls and images, announcements (live regions),
composite widgets and their keys, text scaling behavior.

## 10. Tokens
Tokens used by this screen: | Token | Light | Dark | Used by | Source |, then the export code block(s) in the
target stack's format (only the tokens this screen needs if project tokens exist; the full set if they do not).

## Decisions
## Acceptance criteria
## Open questions
## Validation
````

## Template: change

Input: an m3-design-review report with the user's decisions, or a list of UI changes. Take only accepted findings
(`F-nn`) and notes (`N-nn`). Deviations go to the decisions ledger, not here; rejected and undecided items are listed
under "Not included". A plain list of changes gets the same treatment, with Rule `project` or the rule found.

Grouping: changes that share a component, class, token or file form one group, so one edit fixes all occurrences.
Order groups: tier F first, then shared tokens before the components that use them, then by reach.

````
<header>

## Handoff prompt
<block, scope = the files or components in the groups>

## 1. Summary
<n> changes in <k> groups from <review or list>; effort S <n>, M <n>, L <n>. Expected result after implementation.

## 2. Changes
### G-1 <shared component, token or file> (fixes F-01, F-04, N-02)
#### C-01 <short title> (from F-01)
Location: <file, component or selector; every occurrence or the count plus examples>
Before: <exact current values, e.g. `height: 32px; border-radius: 6px`, color #...... (role if known)>
After: <exact new values, e.g. `min-height: 48px; border-radius: var(--md-sys-shape-corner-full)`, role and hex
  per theme>
Rule: <RULE-ID (path@lastmod) | WCAG 2.2 SC x.y.z | project (<file>, <section>)>
Verify: <how to check and the expected result, e.g. "at 390 px, measure.js smallTargets has none of .chip">
Effort: <S | M | L>   Depends on: <C-nn | none>

## 3. Not included
Recorded as deviations (ledger): <F-nn, rule, scope>. Rejected: <F-nn>. Undecided: <F-nn>. Accepted risk: <F-nn>.

## 4. Tokens
Only when a change adds or changes tokens: the new values and the export code block.

## Decisions
## Acceptance criteria
One AC per change or group, worded as the change's expected result, plus the floor ACs the changes touch.
## Open questions
## Validation
Re-run m3-design-review on the same surface with this change spec as the brief: the fixed F-nn must not reappear.
````

## Closing sections (all modes)

````
## Decisions
- B-01 <decision>. Reason: <one line>. Affects: <sections or AC-nn>.

## Acceptance criteria
- [ ] AC-01 [<RULE-ID | project | WCAG 2.2 SC x.y.z>] <condition>, at <width, theme, state>. Check: <method>.

## Open questions
- Q-01 <question>. Default until answered: <what the brief assumes>. Blocks: <sections or none>.
(or "No open questions.")

## Validation
1. With m3-design-review: "Review <surface> against Material 3 with this brief as project guidelines", at <widths>,
   <themes>. The report's "Brief acceptance criteria" section lists every AC as pass, fail or not checked.
2. By hand: go through the AC checklist at each width and theme; measure hit areas and contrast with browser
   developer tools or the platform's accessibility scanner; tab through the screen; set text to 200%; turn on
   reduced motion.
````

## Acceptance criteria rules

- Testable: each AC states an observable condition with a value or a yes/no result, where and when it holds
  (window class or width, theme, state, text size) and how to check it (measurement, keyboard sequence, screen
  reader, setting to switch, visual comparison with the brief's values).
- Sourced: each AC ends its tag with exactly one primary source: a rule ID from the references (`A11-01`), `project`
  (a project guideline or a decision of this brief: name the `B-nn`), or `WCAG 2.2 SC x.y.z`.
- One condition per AC; split "and" into two ACs unless they are checked together.
- Name the reference of every measurement ("text of rows without a leading element starts 16 px from the screen
  edge", not "row text starts 16 px").
- Text scaling is two different tests; write separate ACs and say which: page zoom to 200% (content reflows with
  no horizontal scroll, as a 320 CSS px window; WCAG 2.2 SC 1.4.10) and text-only enlargement to 200% (browser or OS
  font size; nothing clipped or overlapping; WCAG 2.2 SC 1.4.4). A product text-size setting is a third case.
- Coverage, at least: the accessibility floor for the scope (brief-method, section 8); every tier F rule of the
  chosen components; navigation and pane layout per window class; the primary action; every data-view state;
  both themes when both are in scope; the privacy rules of the project.
- Forbidden words without a measurable meaning: "intuitive", "clean", "consistent", "modern", "looks good",
  "appropriate". Replace with the value or behavior.
- Number ACs in the order a tester would check them: layout, components, states, interaction, accessibility.

Examples:

```
Good: AC-04 [A11-01] At 390 px, every interactive element has a hit area of at least 48 x 48 px. Check: measure
      the hit area of each control (browser tools or a measurement script); none smaller.
Good: AC-09 [A11-33] After opening an item from the list at compact width, focus is on the detail title; Back
      returns focus to the same list item. Check: keyboard and a screen reader.
Good: AC-12 [LAY-19] At 1024 px (expanded), the list pane is a fixed 360 px wide and the detail pane takes the rest.
      Check: measure pane widths at 1024 px and 1180 px.
Good: AC-15 [project, B-04] With "Hide amounts" on, no amount appears on screen, in tooltips or in accessible names.
      Check: switch the setting on and inspect the screen and the accessibility tree.
Bad:  AC-xx The screen is accessible and looks consistent with Material 3.
```
