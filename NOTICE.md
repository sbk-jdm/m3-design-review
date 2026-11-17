# Notice

## Material Design 3 documentation

The files named `color.md`, `styles.md`, `layout-interaction-a11y.md`, `components-1.md`, `components-2.md`,
`components-3.md` and `expressive.md` in `skills/m3-design-review/references/` (and their identical copies in
`skills/m3-design-brief/references/`) are distilled from the Material Design 3 documentation at
https://m3.material.io/. `color-scheme.md` and `platform-mapping.md` in the brief skill summarize role names, tone
mappings and token names from the same documentation and from the public Material 3 libraries' naming. The documentation site states that its content is available under the
Apache License 2.0 or the Creative Commons Attribution 4.0 International License (CC BY 4.0).

- Source: Material Design 3, https://m3.material.io/ (each rule cites its page as `path@lastmod`, where `path` maps
  to `https://m3.material.io/<path>`).
- Changes: the content was condensed, reworded and reorganized into rule tables with IDs and tiers (floor, core,
  expressive/optional); numbers, token names and values were kept; review checks were added. Prose was not copied
  beyond short phrases.
- Not included: images, videos, illustrations and code samples from the documentation.
- License texts: Apache 2.0 at https://www.apache.org/licenses/LICENSE-2.0 and CC BY 4.0 at
  https://creativecommons.org/licenses/by/4.0/.

## WCAG 2.2 and WAI-ARIA Authoring Practices

Some rules cite the W3C Web Content Accessibility Guidelines (WCAG) 2.2 as `WCAG 2.2 SC x.y.z`, or the WAI-ARIA
Authoring Practices Guide (APG) as `WAI-ARIA APG <pattern>`, where Material Design 3 does not state the requirement.
These documents are cited by reference only: success-criterion numbers and pattern names are used to identify them,
and no text from them is copied. See https://www.w3.org/TR/WCAG22/ and https://www.w3.org/WAI/ARIA/apg/.

## No affiliation

This project is not affiliated with, endorsed by, or sponsored by Google. Material Design is a design system by
Google; its name is used here only to identify the guidelines the skills are based on.

## Everything else

Both `SKILL.md` files, `report-template.md`, `adapter-protocol.md`, `measurement.md`, `brief-method.md`,
`brief-template.md`, `scripts/measure.js`, `scripts/m3tokens.py`, the tests and the maintenance scripts are original
work released under the MIT License (see `LICENSE`). Color schemes produced by `m3tokens.py` are an approximation
of the Material 3 tonal-spot method, computed independently; they are not output of Google's tools.
