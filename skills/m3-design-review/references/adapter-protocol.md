# Adapter protocol

How the review connects to a specific project without the skill knowing anything about it. The adapter has three
parts: project guidelines, a decisions ledger, and a change-list format. All three are optional.

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

Floor rules (tier F) still apply even if the guidelines say otherwise.

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
- Decision: `deviation` (accepted difference). Use `revoked` in a new row to cancel an earlier deviation.
- Rationale: one line in the user's words.
- Never store screenshots, page text, personal data or measured values from private screens in the ledger.

Using the ledger in a review: an entry suppresses findings with the same rule ID inside its scope. Report the number
suppressed in the header. If the current evidence shows the deviation now harms usability (for example a new
contrast failure), report it again as tier F regardless of the entry. Tier F rules cannot be ledgered as deviations;
if the user asks, record the decision as `accepted risk` and keep reporting it in the summary line.

## 3. Change-list format

Use the format the project already uses for tasks (a pending-changes document, an issue template, a checklist in a
named file). If none is known, use this default:

```
## Accepted changes from M3 review <date>

- [ ] <file or component>: <change> (<token or value>). Rule <RULE-ID>. Effort <S|M|L>. From F-nn.
```

Group items by file or component when there are more than ten. Keep each item actionable in one step. Do not apply
the changes unless the user asks.

## 4. What the adapter must never do

- Copy project-specific names, data or decisions into the skill's own files.
- Store screenshots or page data anywhere.
- Override a tier F rule.
