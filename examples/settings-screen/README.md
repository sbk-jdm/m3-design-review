# Example: Settings screen, brief to implementation to review

A complete round trip with invented data, used to test both skills on 2026-11-17.

1. `brief.md`: written with m3-design-brief in `screen` mode from a one-paragraph request (habit-tracking PWA,
   seed color #2E7D32, compact window, light and dark, plain HTML/CSS/JS).
2. `implementation.html`: built by a different model that had only `brief.md`, not the skills, following the
   brief's handoff prompt. One self-contained file; open it in a browser.
3. `review.md`: m3-design-review run on the implementation with the brief as project guidelines. Result: 34 of 37
   acceptance criteria pass; the 3 failures (focus ring opacity, a 41 px hit area, overlap at 200% text) are real
   and are listed as findings.

The brief and review are kept as produced, including the issues the round trip revealed; the fixes went into the
skills (see CHANGELOG.md, m3-design-brief 0.1.0 and m3-design-review 0.3.0).

Screenshots at 390 px (DPR 2): `settings-light.png`, `settings-dark.png`.
