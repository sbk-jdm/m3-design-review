# Adapter protocol

How the review connects to a specific project without the skill knowing anything about it. The adapter has four
parts: project guidelines (including an optional review setup), a decisions ledger, a project conventions list, and a
change-list format. All are optional.

## 1. Find project guidelines

Look, in this order, and stop at the first that gives design guidance:

1. What the user said in this conversation (named file, pasted rules, "we follow X").
2. Instruction files already in context: `CLAUDE.md`, `AGENTS.md`, `.github/copilot-instructions.md`, project
   instructions or project documents attached to the session.
3. Files in the repository, if one is available (search names case-insensitively, read only the relevant ones):
   - `DESIGN.md`, `design-guidelines.md`, `docs/design/**`, `docs/ui/**`, `style-guide.md`, `STYLEGUIDE.md`
   - design tokens: `tokens.json`, `*.tokens.json`, `theme.(css|scss|ts|js|dart|kt)`, CSS custom properties on `:root`
   - component library docs or Storybook stories, if present
4. If nothing is found, ask once: "Do you have project design guidelines or recorded design decisions I should
   respect? If not, I will review against M3 only." Continue without them if there is no answer.

From the guidelines, extract only what changes the review:
- explicit deviations from M3 (brand shapes, a custom type scale, a palette that is not role-based)
- the tolerance, if stated
- target platforms, form factors, themes, and any mandatory accessibility level
- privacy rules (for example amounts or names that must be hidden in a privacy mode)
- the review setup (below), if stated
- project rules that are not M3 rules (ARIA patterns, wording, interaction conventions): breaches of these go to
  "Project and WCAG notes" in the report, citing the guideline file and section

Floor rules (tier F) still apply even if the guidelines say otherwise.

### Review setup (optional)

The guidelines may state how a review must be run. When they do, use these values instead of the defaults in
SKILL.md Step 3; when they do not, use the defaults and say so in the report header.

```
## Review setup
Widths to test: 360, 390, 1280            # CSS px; each becomes a measure.js run with expectWidth
Themes to test: light, dark
Text-size settings to test: browser 200%; app setting "Text size" = Large   # each runs the "text at 200%" recipe
Viewport meta in production: width=device-width, initial-scale=1           # inject it if the test harness omits it
Privacy state to review: <how to switch on a demo or privacy mode>
Minimum text size: 12                       # CSS px; may raise the A11-30 threshold, never lower it
```

- Widths to test: drive the viewport and `expectWidth` of each run; a run that warns about the viewport is redone.
- Text-size settings to test: list the browser zoom level and any in-app text-size setting with the values to try;
  results are labelled `measured-simulation`.
- Every field is optional. Values that would weaken a tier F rule (a lower minimum text size, a smaller target) are
  ignored.

## 2. Decisions ledger

A plain Markdown file that records accepted deviations so they are not reported again.

Location: use the one the guidelines name. Otherwise look for `design-decisions.md`, `docs/design-decisions.md` or
`DECISIONS.md` with a section titled "Design deviations". If none exists, propose `docs/design-decisions.md` and create
it only after the user agrees. In a session without a filesystem, output the entries for the user to save.

Format: one table, newest entries at the bottom; append only, never rewrite past entries.

```
## Design deviations (M3)

| Date | Rule ID | Scope | Decision | Rationale | Finding |
| --- | --- | --- | --- | --- | --- |
| 2026-01-15 | SHP-02 | all buttons | deviation | Brand uses 8dp corners on every button | F-07 (review 2026-01-15) |
```

- Date: ISO date of the decision.
- Rule ID: exactly as in the references (several IDs separated by commas).
- Scope: selector, component or screen the deviation covers; keep it as narrow as the user stated.
- Decision: `deviation` (accepted difference from a tier C or E rule), `accepted risk` (a tier F finding or a WCAG
  note the user chose not to fix), or `revoked` in a new row to cancel an earlier entry.
- Rationale: one line in the user's words.
- Never store screenshots, page text, personal data or measured values from private screens in the ledger.

Tier F rules can only be recorded as `accepted risk`, never as `deviation`:

```
| 2026-01-20 | A11-01 | `.legend-dot` buttons | accepted risk | Redesign planned next quarter | F-03 (review 2026-01-20) |
```

Using the ledger in a review: a `deviation` entry suppresses findings with the same rule ID inside its scope. Report
the number suppressed in the header. If the current evidence shows the deviation now harms usability (for example a
new contrast failure), report it again as tier F regardless of the entry. An `accepted risk` entry suppresses nothing:
the finding is still reported, marked "accepted risk (ledger, <date>)", and counted in the summary line.

## 3. Project conventions list

Decision candidates with Rule ID `none (project convention)` are project choices that M3 does not address (a custom
affordance, a project-specific color meaning). They are not M3 deviations, so they do not go to the ledger.

Location: the conventions section the guidelines name. Otherwise a separate section in the same decisions file:

```
## Project conventions (not covered by M3)

| Date | Convention | Scope | Rationale | Candidate |
| --- | --- | --- | --- | --- |
| 2026-01-15 | A chevron next to a value opens a bottom sheet with the options | value pickers | Consistent across screens | D-2 (review 2026-01-15) |
```

A recorded convention removes the matching decision candidate from later reviews. It never overrides a tier F rule:
if the convention breaks one, the F finding is still reported. Create the section only after the user agrees, as for
the ledger.

## 4. Change-list format

Use the format the project already uses for tasks (a pending-changes document, an issue template, a checklist in a
named file). If none is known, use this default:

```
## Accepted changes from M3 review <date>

- [ ] <file or component>: <change> (<token or value>). Rule <RULE-ID or source>. Effort <S|M|L>. From F-nn / N-nn.
```

Group items by file or component when there are more than ten. Keep each item actionable in one step. Do not apply
the changes unless the user asks.

## 5. What the adapter must never do

- Copy project-specific names, data or decisions into the skill's own files.
- Store screenshots or page data anywhere.
- Override a tier F rule.
