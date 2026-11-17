# Report template

Use this layout for every review. Keep section order. Omit a section only when it would be empty, and then write one
line saying so (for example "No decision candidates."). Write the prose in the user's language; keep IDs, tokens and
sources as they are.

---

## Header

```
# M3 design review: <surface name>

Surface: <what was reviewed: screens / files / URL>, <platform>, <form factor / window size class>
Viewports and themes: <e.g. 390 x 844 CSS px, DPR 3, light and dark; text 200% simulated at 195 px>
Tolerance: <strict | inspired> (<"default" | "set by user" | "set by project guidelines">)
References snapshot: <oldest snapshot date of the files loaded> <freshness note if older than 6 months>
Project guidelines: <found at <path> | not found>   Decisions ledger: <found, N entries | not found>
Evidence: measured-rendered <n>, measured-code <n>, measured-simulation <n>, estimated <n>. <K> findings suppressed by recorded decisions.
Privacy: <"no personal data visible" | "personal data visible: suggest reviewing a redacted state">
```

- Evidence counts cover findings and notes together; each item counts once, under its label.
- Freshness note when the snapshot is more than 6 months old: "References are older than 6 months: refresh them
  before implementing tier C changes; tier F findings stand."
- If a measurement run reported setup warnings (`viewport-meta-missing`, `viewport-width-mismatch`), say here how the
  setup was fixed. Never report results from a run that still had them.

## Summary

Two to four lines: overall state, the most important problem, and the count by tier and kind.

```
Issues: F <n>, C <n>. Suggestions: C <n>, E <n>. Notes: <n>. Not reviewed: <out of scope, e.g. motion, RTL>.
```

If there are few or no findings, say so here and keep the findings section short. No filler praise.

## Brief acceptance criteria

Only when a design brief with acceptance criteria (`AC-nn`, for example from m3-design-brief) was given or found.
Otherwise omit the section without a line. In the header, name the brief as the project guidelines
(`Project guidelines: brief "<title>" (<date>)`). One row per AC, in the brief's order:

```
Brief: <title>, <mode>, <date>. Result: pass <n>, fail <n>, not checked <n>.

| AC | Criterion (short) | Result | Evidence |
| --- | --- | --- | --- |
| AC-01 | <criterion in a few words> | pass | <evidence label>: <selector or region> - <value> |
| AC-02 | <criterion> | fail | see F-03 |
| AC-03 | <criterion> | not checked | <why, and the step that would check it> |
```

- Result is exactly `pass`, `fail` or `not checked`. Never mark `pass` without evidence; label it as for findings.
- A failed AC that breaks a rule ID, a WCAG criterion or a project guideline is also reported as a finding or note;
  its row says "see F-nn" (or N-nn) instead of repeating the evidence. A failed AC with no such rule (a brief value
  not met, for example a pane width) keeps its evidence in the row and is not repeated elsewhere.
- Brief decisions (`B-nn`) are recorded decisions within the brief's scope: they are not findings or decision
  candidates, except when they break a tier F rule (then the F finding is reported and cites the decision).
- Brief open questions (`Q-nn`) that are still open: list them in one line after the table.

## Findings

Sorted by impact (tier F issues first). One block per finding:

```
### F-01 <short title>
Area: <component or foundation>   Tier: <F | C | E>   Kind: <issue | suggestion>   Effort: <S | M | L>
Evidence (<measured-rendered | measured-code | measured-simulation | estimated>): <selector or image region> - <value(s)>; <count> occurrences
Rule: <RULE-ID> (<path@lastmod | WCAG 2.2 SC x.y.z | WAI-ARIA APG <pattern> | heuristic>)
Why it matters: <one line, user impact first>
Proposed change: <concrete token, role or value>
Decision: [ ] accept  [ ] reject  [ ] deviation   Note: ______
```

Rules for blocks:
- `F-nn` is a running finding number, independent of the tier.
- Evidence names at most three examples and gives the total count. If the control was classified by function
  (CMP-01), say which classification was used ("judged as a segmented button").
- One rule per finding; if several apply, cite the most specific one and list the others after it ("also A11-01").
- The proposed change is something an implementer can do without asking back.
- Effort: S = one property or token; M = one component or a few files; L = structural or cross-screen.
- A tier F finding cannot be a deviation: if the user will not fix it, record `accepted risk` (see
  `adapter-protocol.md`) and keep it in the summary line.

Grouping: when the same problem appears in several places or comes from a shared component, class or token, report
it once with all occurrences (or three examples and the total), so a single decision covers it. Put it in the area
where the fix lives. Do not report it again under another area or as a note.

## Project and WCAG notes

Items that are not M3 rules: breaches of the project's own guidelines, and WCAG 2.2 success criteria that no rule ID
in the references covers. Tier is not used here. Put accessibility failures first. One short block per item:

```
### N-01 <short title>
Area: <component or foundation>   Effort: <S | M | L>
Source: <project guideline: <file>, <section> | WCAG 2.2 SC x.y.z <name>>
Evidence (<measured-rendered | measured-code | measured-simulation | estimated>): <selector or region> - <value(s)>; <count> occurrences
Proposed change: <concrete change>
Decision: [ ] accept  [ ] reject   Note: ______
```

- `N-nn` is a running number, separate from `F-nn`.
- If a rule ID in the references covers the problem, it is a finding, not a note.
- A rejected WCAG note is recorded as `accepted risk`, like a tier F finding.

## Decision candidates

Conflicts between project guidelines (or established project patterns) and tier C or E rules, plus project choices
that M3 does not address but that a reviewer would otherwise question. Not violations. List each once, and skip any
already recorded in the ledger or the conventions list:

```
| # | Project choice | M3 rule | Rule ID (source) | Options |
| --- | --- | --- | --- | --- |
| D-1 | <what the project does> | <what M3 says> | <ID (path@lastmod)> | record as deviation / align with M3 |
| D-2 | <what the project does> | no M3 rule | none (project convention) | record as project convention / change it |
```

Rows with `none (project convention)` are recorded in the project's conventions list, not in the M3 deviation ledger
(`adapter-protocol.md`, section 3). Tier F rules never appear here; they are findings.

## Not covered

One or two lines: what could not be checked and why (no rendered page, state styles not visible, motion not
observable, focus flow not exercised, a reference file missing). Offer the step that would cover it.

## Next step

One line asking for decisions, for example: "Mark each finding and note accept, reject or deviation (ranges are fine:
'accept F-01..F-06, N-01'). I will record deviations in the ledger and give you the change list."

---

## After decisions

Reply with up to three blocks, then list open items (findings and notes with no decision).

```
Ledger entries added (<path>):
<entries in the ledger format of adapter-protocol.md, including any accepted risk>

Project conventions added (<path>):
<entries for decision candidates recorded as project conventions>

Change list (<format name>):
<items in the project's change-list format, or the default format>
```
