---
name: m3-design-brief
description: Writes Material Design 3 design briefs (project guidelines, screen specs, change specs) that any AI or developer can implement. Design only, no code changes.
---

# Material Design 3 design brief

Write a self-contained Markdown design brief that a person or any AI assistant can follow to design or implement an
interface in Material Design 3 (M3), without this skill installed. The brief carries the actual values inline (hex,
dp or px, type roles and sizes, component specs) and keeps rule IDs so m3-design-review can validate the result.

## When to use / not to use

Use when the user asks to:
- "write design guidelines / a design system brief for this project, based on Material 3"
- "spec this screen / flow / feature / component in M3 so another AI or a developer can build it"
- "turn these review findings (or this list of UI changes) into an implementation-ready spec"
- choose M3 components, navigation, layout per window size class, states and copy before building

Do not use when:
- the user wants code written or edited, or UI rendered: this skill writes the brief only. Do not change code,
  even small fixes; offer the handoff prompt instead
- the user wants an existing UI checked against M3: that is m3-design-review (run it first, then use mode `change`)
- the target design system is explicitly not Material, or the question is a single lookup ("FAB height?"): answer
  from the reference files directly

## Modes

| Mode | Output | Pick it when |
| --- | --- | --- |
| `system` | Project design guidelines: foundations, tokens, component rules, exceptions, do/don't, accessibility floor | The user asks for guidelines, a design system, a theme, or rules every screen must follow; or no guidelines exist and several screens will be designed |
| `screen` | Brief for one screen, flow, feature or component | The user names one screen, flow, feature or component to design or build |
| `change` | Change spec: per change where, before, after (exact values), rule, verify, effort | The input is an m3-design-review report with decisions, or a list of changes to an existing UI |

If the request fits two modes, pick the narrower one and say so in one line. If a `screen` brief is requested and no
project guidelines exist, write the screen brief and offer a `system` brief afterwards; do not write both unasked.

## Layers and precedence

Same order as m3-design-review. A higher layer wins over a lower one.

1. Floor rules, tier F: accessibility and usability minimums. Never negotiable; the brief never specifies a value that
   breaks one, even when asked. Record the conflict as an open question (`Q-nn`) and specify the compliant value.
2. Project guidelines, recorded deviations (decisions ledger) and project conventions, found through the adapter
   protocol. They win over tier C and E: use the project's value and mark it `project`.
3. M3 core, tier C: roles, tokens, type and shape scales, component specs. The default for every value.
4. M3 Expressive and optional items, tier E: only on request or when the project guidelines adopt them.

Tolerance (`strict` or `inspired`, default `inspired`) is recorded in the brief header for the later review. In
`strict`, do not depart from a tier C rule by your own decision: propose the departure as `Q-nn`. In `inspired`, a
departure is allowed as a decision `B-nn` with a one-line reason, never on tier F.

## Workflow

### Step 0. Scope and mode

Determine the mode (table above), the surface (product area, screen, flow or component), the platform and stack
(web with CSS or Tailwind, Jetpack Compose, Flutter, other), and the window size classes to cover: compact (< 600dp),
medium (600-839), expanded (840-1199), large (1200-1599), extra-large (1600 and up) (LAY-01). Default: compact and
expanded for web and Android, compact only for phone-only apps; state the default as a decision.

### Step 1. Load the adapter

Follow `references/adapter-protocol.md`, sections 1 to 3 (shared with m3-design-review): find project design
guidelines, a decisions ledger and a conventions list. Use from them: deviations from M3, tolerance, platforms, window
classes, themes, accessibility level, privacy rules, review setup and existing tokens. Project guidelines and recorded
deviations win over tier C and E, never over tier F. If nothing is found, do not ask separately: fold it into Step 2.

### Step 2. Gather inputs

Collect: the request; users and their main tasks; platform and window size classes; themes (light, dark, contrast
levels); existing tokens or brand colors; existing UI, if any (screenshots, code, a review report); content and data
the screen shows; constraints (libraries in use, components that must stay).

Ask at most 3 short questions, in one message, and only when the answer changes the brief (for example: no brand
color and no tokens; unknown platform; unclear primary task). For everything else, make a reasonable assumption and
record it as a decision `B-nn` ("B-02 Window classes: compact and expanded; medium uses the compact layout"). If the
user does not answer, continue with the assumptions and keep the questions as `Q-nn`.

### Step 3. Tokens

In this order:
1. Project tokens exist: reuse them. Map custom names to M3 roles (`references/color.md`, section 6). If they can be
   written as a role JSON, run `python3 scripts/m3tokens.py check <file>`; failing pairs become tier F items of the
   brief (fix value as `B-nn`, or `Q-nn` if the project must decide).
2. A brand or seed color exists: generate a scheme, check it, export it in the target stack's format:
   ```
   python3 scripts/m3tokens.py scheme --seed "#RRGGBB" --name <name> --out scheme.json
   python3 scripts/m3tokens.py check scheme.json
   python3 scripts/m3tokens.py export scheme.json --format css|compose|flutter|tailwind|json
   python3 scripts/m3tokens.py export --tokens type --format css
   python3 scripts/m3tokens.py export --tokens shape --format css
   ```
   The scheme is an approximation of M3 tonal-spot (luminance and therefore contrast match; hue and chroma may differ
   slightly). Say so in the brief, with the note from `meta.note`, and keep the seed so exact values can be
   regenerated with Material Theme Builder or the material-color-utilities library. See `references/color-scheme.md`.
3. No color at all: ask (it counts as one of the 3 questions); without an answer, choose a seed as `B-nn`.

Always paste the export inline in the brief (section "Tokens"), so the implementer does not need the script. Use the
names of `references/platform-mapping.md` for the stack. Without code execution, do not compute hex values by hand:
reuse project tokens, or specify the seed and a generator (Flutter `ColorScheme.fromSeed`, Material Theme Builder
or material-color-utilities elsewhere) and add an AC that the generated pairs pass the contrast check. Type sizes: use the export; for any value it omits,
name the role token (for example body-large) and the platform's M3 default typography as the source; never guess.

### Step 4. Decide

Follow `references/brief-method.md`: start from user tasks; choose navigation by destinations and window size class;
choose components by function (CMP-01); set layout and panes per window class; specify states for every interactive
element and data view; write the copy; turn the accessibility floor into acceptance criteria; add motion only with a
reduced-motion fallback; use Expressive (tier E) only on request or when the adapter says so.

Load only the rule references the brief needs (progressive disclosure; list headings with `grep -n '^## ' <file>`
and read only those sections):

| Brief involves | Load |
| --- | --- |
| Always | `references/layout-interaction-a11y.md` ("Accessibility floor", breakpoints, margins and panes, states, "Cross-component rules") |
| Color roles, themes, tokens | `references/color.md`, `references/color-scheme.md` |
| Type, shape, elevation, spacing, motion, icons | `references/styles.md` |
| App bars, badges, bottom sheets, button groups, buttons, cards, carousel, checkbox, chips, date pickers, dialogs, divider | `references/components-1.md` |
| Extended FAB, FAB menu, FAB, icon buttons, lists, loading indicator, menus, navigation bar / drawer / rail, progress indicators, radio button | `references/components-2.md` |
| Search, segmented buttons, side sheets, sliders, snackbar, split button, switch, tabs, text fields, time pickers, toolbars, tooltips | `references/components-3.md` |
| Expressive requested or adopted by the project | `references/expressive.md` |
| Token names for the stack | `references/platform-mapping.md` |

If a reference file is missing, say so and continue; do not invent rules or values to fill the gap.

### Step 5. Write

Use `references/brief-template.md`: the template of the mode, the "Handoff prompt" block at the top, then the body,
"Decisions" (`B-01`...), "Acceptance criteria" (`AC-01`...), "Open questions" (`Q-01`...) and "Validation". Follow
"Acceptance criteria rules" in the same file. In mode `change`, take only accepted findings and notes from the review
(deviations go to the ledger, rejected items are left out), and group changes that share a component or token.

### Step 6. Self-check

Before presenting, check and fix:
- Every value (color, size, radius, spacing, type, elevation, duration, copy rule) is marked `M3 <RULE-ID>`,
  `project` or `decision B-nn`; nothing is unmarked or invented.
- Every AC is testable: a condition, where and when (width, theme, state) and how to check it, plus its source.
- No value or decision breaks a tier F rule; each tier F rule in scope has an AC.
- Every interactive element and data view has its states; every motion has a reduced-motion fallback.
- Focus order and reading order stated in the brief match the order of elements in the layout you specify; no
  section contradicts another (for example "focus goes to the title, then Tab reaches Back" with Back placed first).
- Every measurement in an AC names its reference point (which element, which edge, which state).
- The brief is self-contained: no links to this skill's files, all values inline, the token export pasted.
- Privacy (below) holds.

### Step 7. Hand off

- Present the brief. If a filesystem is available, propose a path and write it only after the user agrees:
  `system` briefs where the adapter protocol looks for guidelines (`docs/design-guidelines.md` or `DESIGN.md`), so
  later briefs and reviews find them; `screen` and `change` briefs under `docs/design/briefs/<date>-<slug>.md`.
  Otherwise output the brief in the reply for the user to save.
- Point to the handoff prompt: the user pastes it with the brief into any AI tool or gives both to a developer.
- Validation: after implementation, run m3-design-review with the brief as project guidelines; it reports each AC
  as pass, fail or not checked. Without that skill, follow the brief's "Validation" section by hand.
- System briefs that record exceptions: offer to append them to the decisions ledger (adapter protocol, section 2).

## Output discipline

- Self-contained: values inline, rule IDs kept for traceability, no references to this skill's files or scripts
  (except in "Validation", where m3-design-review is named as an option).
- Written in the user's language. Keep rule IDs, token names, code and sources unchanged.
- No images required: describe layouts with region lists, tables and, if useful, a small text wireframe.
- Mark every value: `M3 <RULE-ID>` (for example `M3 BTN-01`), `project`, or `decision B-nn`. Acceptance criteria
  cite a rule ID, `project` or `WCAG 2.2 SC x.y.z`.
- Units: dp in specs; on the web 1dp = 1 CSS px and type sizes in rem (px / 16, TYP-13). Colors as role names with
  their hex for each theme.
- Concrete and implementable: "filled button, height 40dp, corner full, primary / on-primary", never "make it pop".
- Plain, professional text. No decorative icons or emoji. Tables where the template uses them.
- Header shows the references snapshot date (the oldest "Snapshot date" of the files loaded). If it is more than 6
  months before today, say so and recommend checking tier C values against https://m3.material.io/.
- Specify only what the brief needs; do not pad it with M3 rules that do not apply to the surface.

## Privacy

- The brief will be pasted into other tools: never include personal data, credentials, internal URLs with tokens,
  or real customer content. Use realistic placeholder content ("Account ending 1234", "Sample User").
- If screenshots or code show personal data, say so, describe elements by role, and quote only the minimum text.
- Carry project privacy rules into the brief (for example a mode that hides amounts) as `project` requirements and ACs.
- Do not store screenshots or page data in files, memory or the ledger.

## Files

- `references/brief-method.md`: how to decide navigation, components, layout, states, copy, accessibility, motion.
- `references/brief-template.md`: templates `system`, `screen`, `change`, the handoff prompt, acceptance criteria rules.
- `references/color-scheme.md`: color roles, tone mapping used by the script, using a brand palette.
- `references/platform-mapping.md`: token and component names for CSS, Jetpack Compose, Flutter and other stacks.
- `references/adapter-protocol.md`: project guidelines, decisions ledger, conventions (shared with m3-design-review).
- `scripts/m3tokens.py`: stdlib Python CLI: `scheme` (scheme from a seed), `check` (contrast of role pairs), `export`
  (css, json, compose, flutter, tailwind; `--tokens type|shape`). Run with `--help` per subcommand.
- The other `references/*.md` files: distilled M3 rules (shared with m3-design-review), each with an ID, a tier and a
  source `path@lastmod` (maps to `https://m3.material.io/<path>`), `WCAG 2.2 SC x.y.z`, `WAI-ARIA APG <pattern>` or
  `heuristic`.
