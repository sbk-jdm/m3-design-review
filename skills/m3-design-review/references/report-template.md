# Report template

Use this layout for every review. Keep section order. Omit a section only when it would be empty, and then write one
line saying so (for example "No decision candidates."). Write the prose in the user's language; keep IDs, tokens and
sources as they are.

---

## Header

```
# M3 design review: <surface name>

Surface: <what was reviewed: screens / files / URL>, <platform>, <form factor / window size class>
Viewports and themes: <e.g. 390 x 844 CSS px, DPR 3, light and dark>
Tolerance: <strict | inspired> (<"default" | "set by user" | "set by project guidelines">)
References snapshot: <date from the reference file headers> <freshness note if older than 6 months>
Project guidelines: <found at <path> | not found>   Decisions ledger: <found, N entries | not found>
Evidence: <N measured, M estimated>. <K> findings suppressed by recorded decisions.
Privacy: <"no personal data visible" | "personal data visible: suggest reviewing a redacted state">
```

## Summary

Two to four lines: overall state, the most important problem, and the count by tier and kind.

```
Issues: F <n>, C <n>. Suggestions: C <n>, E <n>. Not reviewed: <out of scope, e.g. motion, RTL>.
```

If there are few or no findings, say so here and keep the findings section short. No filler praise.

## Findings

Sorted by impact (tier F issues first). One block per finding:

```
### F-01 <short title>
Area: <component or foundation>   Tier: <F | C | E>   Kind: <issue | suggestion>   Effort: <S | M | L>
Evidence (<measured | estimated>): <selector or image region> - <value(s)>; <count> occurrences
Rule: <RULE-ID> (<path@lastmod>)
Why it matters: <one line, user impact first>
Proposed change: <concrete token, role or value>
Decision: [ ] accept  [ ] reject  [ ] deviation   Note: ______
```

Rules for blocks:
- `F-nn` is a running finding number, independent of the tier.
- Evidence names at most three examples and gives the total count.
- One rule per finding; if two apply, cite the stricter and mention the other in the evidence line.
- The proposed change is something an implementer can do without asking back.
- Effort: S = one property or token; M = one component or a few files; L = structural or cross-screen.

## Decision candidates

Conflicts between project guidelines (or established project patterns) and tier C or E rules. Not violations.
List each once, and skip any already recorded in the ledger:

```
| # | Project choice | M3 rule | Rule ID (source) | Options |
| --- | --- | --- | --- | --- |
| D-1 | <what the project does> | <what M3 says> | <ID (path@lastmod)> | record as deviation / align with M3 |
```

## Not covered

One or two lines: what could not be checked and why (no rendered page, state styles not visible, motion not
observable, a reference file missing). Offer the step that would cover it.

## Next step

One line asking for decisions, for example: "Mark each finding accept, reject or deviation (ranges are fine:
'accept F-01..F-06'). I will record deviations in the ledger and give you the change list."

---

## After decisions

Reply with two blocks, then list open items (findings with no decision).

```
Ledger entries added (<path>):
<entries in the ledger format of adapter-protocol.md>

Change list (<format name>):
<items in the project's change-list format, or the default format>
```
