# Color scheme: roles, tone mapping, brand palettes

How `scripts/m3tokens.py` builds and checks an M3 color scheme, and how to use it with a brand palette.
Source paths map to `https://m3.material.io/<path>`; `@date` is the page's lastmod in the 2026-11-17 snapshot.

## Roles and what each one is for

From styles/color/roles@2026-07-27 unless noted. The docs count 26 standard roles in six groups (primary, secondary,
tertiary, error, surface, outline) plus optional add-on roles (fixed accents, surface dim/bright). The script emits
46 roles: the standard and add-on roles below, plus `surface-variant`, `shadow` and `scrim` that the libraries keep.

| Role | Use |
| --- | --- |
| primary | High-emphasis fills, text and icons against surface (FAB, high-emphasis buttons, active states) |
| on-primary | Text and icons on primary |
| primary-container | Standout fill against surface for key components such as the FAB |
| on-primary-container | Text and icons on primary-container |
| secondary | Less prominent fills, text and icons against surface (filter chips) |
| on-secondary | Text and icons on secondary |
| secondary-container | Less prominent fill for recessive components such as tonal buttons |
| on-secondary-container | Text and icons on secondary-container |
| tertiary | Complementary fills, text and icons against surface |
| on-tertiary | Text and icons on tertiary |
| tertiary-container | Complementary container color, for components like input fields |
| on-tertiary-container | Text and icons on tertiary-container |
| error | Attention-grabbing color for fills, icons and text that signal urgency; stays red in dynamic schemes |
| on-error | Text and icons on error |
| error-container | Attention-grabbing fill against surface |
| on-error-container | Text and icons on error-container |
| surface | Default background |
| on-surface | Text and icons on any surface or surface container |
| on-surface-variant | Lower-emphasis text and icons on any surface or surface container |
| surface-container-lowest | Lowest-emphasis container |
| surface-container-low | Low-emphasis container |
| surface-container | Default container (for example the navigation area next to a surface body) |
| surface-container-high | High-emphasis container |
| surface-container-highest | Highest-emphasis container |
| surface-dim | Dimmest surface in both themes (add-on) |
| surface-bright | Brightest surface in both themes (add-on) |
| inverse-surface | Fill for elements that contrast with surface (snackbar) |
| inverse-on-surface | Text and icons on inverse-surface (the docs write "inverse on surface") |
| inverse-primary | Actionable elements, such as a text button, on inverse-surface |
| outline | Important boundaries, such as a text field outline (3:1 against surface) |
| outline-variant | Decorative elements such as dividers, and borders of targets whose content already has 4.5:1 |
| primary-fixed, secondary-fixed, tertiary-fixed | Fills with the same tone in light and dark (add-on; contrast risk) |
| primary-fixed-dim, ... | Stronger tone of the fixed color, same fixed behavior |
| on-primary-fixed, ... | Text and icons on the fixed color |
| on-primary-fixed-variant, ... | Lower-emphasis text and icons on the fixed color |
| surface-variant | Library role (not described on the roles page); kept for older components and stacks |
| shadow, scrim | Library roles for elevation shadows and modal scrims (black) |

Pair only as intended: foreground `on-X` on fill `X`, `on-surface` / `on-surface-variant` on surfaces and containers.
Containers are fills, not text colors (styles/color/roles@2026-07-27).

## Tone mapping used by the script

Source: material-color-utilities defaults; the docs show this mapping only as an image. Verified against the docs
text where possible: primary40 for primary and primary100 for on-primary
(styles/color/system/how-the-system-works@2026-07-23); light surface tone 98 (changed from 99) and neutral chroma 6
(changed from 4) (styles/color/system/overview@2026-07-23); tonal palettes run 0 to 100 in steps of 10 plus 95, 98
and 99 (how-the-system-works@2026-07-23).

| Role (X = primary, secondary, tertiary, error) | Palette | Light | Dark |
| --- | --- | --- | --- |
| X | X | 40 | 80 |
| on-X | X | 100 | 20 |
| X-container | X | 90 | 30 |
| on-X-container | X | 30 (older versions used 10) | 90 |
| surface | neutral | 98 | 6 |
| on-surface | neutral | 10 | 90 |
| surface-variant | neutral-variant | 90 | 30 |
| on-surface-variant | neutral-variant | 30 | 80 |
| surface-container-lowest / low / (default) / high / highest | neutral | 100 / 96 / 94 / 92 / 90 | 4 / 10 / 12 / 17 / 22 |
| surface-dim / surface-bright | neutral | 87 / 98 | 6 / 24 |
| inverse-surface / inverse-on-surface | neutral | 20 / 95 | 90 / 20 |
| inverse-primary | primary | 80 | 40 |
| outline / outline-variant | neutral-variant | 50 / 80 | 60 / 30 |
| shadow, scrim | neutral | 0 | 0 |
| X-fixed / X-fixed-dim / on-X-fixed / on-X-fixed-variant (X without error) | X | 90 / 80 / 10 / 30 | same as light |

Palettes (tonal-spot): primary = seed hue, chroma 36; secondary = seed hue, 16; tertiary = seed hue + 60, 24;
neutral = seed hue, 6; neutral-variant = seed hue, 8; error = hue 25, chroma 84 (HCT; applied as CIE LCh hue 36,
the LCh hue of the M3 baseline error #BA1A1A, so error stays red).

## Commands

```
python3 scripts/m3tokens.py scheme --seed "#6750A4" --name app --out scheme.json
python3 scripts/m3tokens.py check scheme.json            # Markdown table; --format json; exit 1 on a failure
python3 scripts/m3tokens.py export scheme.json --format css|json|compose|flutter|tailwind
python3 scripts/m3tokens.py export --tokens type --format css
python3 scripts/m3tokens.py export --tokens shape --format css
```

`check` pairs: every `on-X` on `X` and `on-X-container` on `X-container` (X = primary, secondary, tertiary, error);
primary, secondary, tertiary and error as text on surface; on fixed and on fixed variant on each fixed color;
on-surface and on-surface-variant on surface, surface-dim, surface-bright, each surface container and surface-variant;
inverse-on-surface and inverse-primary on inverse-surface: all 4.5:1. outline on surface: 3:1. outline-variant on
surface: reported, never fails (decorative). Contrast uses the WCAG 2.x relative luminance formula; ratios are
truncated to two decimals. Large text (3:1) is not separated: the check applies the stricter 4.5:1 to every text pair.

## Using a brand palette instead of a seed

When the brand gives exact colors (a static custom-brand scheme, styles/color/static/custom-brand@2026-02-11):

1. Write the role hex values by hand into the same JSON shape, one object per theme. Missing roles are allowed and
   listed; role keys may be kebab-case (`on-primary`), camelCase (`onPrimary`), snake_case or prefixed
   (`--md-sys-color-on-primary`, `md.sys.color.on-primary`); DTCG `{"$value": "#..."}` values are accepted.
   ```json
   {
     "light": { "primary": "#1B5FAA", "on-primary": "#FFFFFF", "surface": "#FCFCFF", "on-surface": "#1A1C1E" },
     "dark":  { "primary": "#A4C8FF", "on-primary": "#00315E", "surface": "#111318", "on-surface": "#E2E2E6" }
   }
   ```
2. Optional starting point: generate a scheme from the brand's main color, then overwrite the roles the brand fixes
   (usually primary and sometimes primary-container). Keep the generated `on-*` roles only if `check` still passes.
3. Run `check`. Fix every `fail` by moving the tone of the fill or of its `on-*` color, not by inventing new pairs.
4. Run `export` for the stack. Components reference roles, never hex values.
5. For an exact scheme from a brand color, use Material Theme Builder (it exports Compose, Views, Flutter, Web and
   JSON) and run `check` on the result.

## Limits of the approximation

- M3 builds palettes in HCT (CAM16 hue and chroma, CIE L* tone). The script keeps L* exact, so contrast between
  roles matches the official tools within rounding (tone error below 0.6 L* after 8-bit rounding), but it uses CIE
  LCh(ab) hue and chroma in place of CAM16, so hue and colorfulness differ slightly. For #6750A4 it gives primary
  #66558F where the libraries give about #65558F; error #C00013 where the baseline is #BA1A1A.
- Only the tonal-spot variant and the standard contrast level. No vibrant, expressive, fidelity or content variants,
  no medium or high contrast schemes, no dynamic color from wallpaper or images.
- Gamut mapping lowers chroma at fixed L* and hue; very saturated seeds lose colorfulness at the light and dark ends,
  as in M3.
- Near-grey seeds (chroma below 0.001) get hue 0.
- For exact values regenerate with Material Theme Builder or the material-color-utilities library; `meta.method`
  and `meta.note` in every generated scheme say the same.
