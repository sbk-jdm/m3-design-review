# Platform mapping: tokens, roles and components

How M3 names in a brief map to code. Role and token names are the same across stacks; only the spelling changes
(kebab-case in CSS, camelCase in Kotlin and Dart). Generate the values with `scripts/m3tokens.py export`.
Library API names below are the current Jetpack Compose Material 3 (androidx.compose.material3) and Flutter
(material library) names; check them against the version the project uses.

## Values and their sources

- Color roles: generated per project (`scheme`, `check`, `export`); see color-scheme.md.
- Type scale: baseline M3 type scale shipped by the Material 3 libraries. The docs
  (styles/typography/type-scale-tokens@2026-05-06) name the tokens but give the numbers only as an image.
- Shape scale: styles.md SHP-01 (styles/shape/corner-radius-scale@2026-05-06). Token form
  `md.sys.shape.corner.<step>`, as used in the component spec tables.

| Type style | Size / line height (sp = CSS px) | Tracking | Weight |
| --- | --- | --- | --- |
| display-large / medium / small | 57/64, 45/52, 36/44 | -0.25, 0, 0 | 400 |
| headline-large / medium / small | 32/40, 28/36, 24/32 | 0 | 400 |
| title-large / medium / small | 22/28, 16/24, 14/20 | 0, 0.15, 0.1 | 400, 500, 500 |
| body-large / medium / small | 16/24, 14/20, 12/16 | 0.5, 0.25, 0.4 | 400 |
| label-large / medium / small | 14/20, 12/16, 11/16 | 0.1, 0.5, 0.5 | 500 |

Shape steps: none 0, extra-small 4, small 8, medium 12, large 16, large-increased 20, extra-large 28,
extra-large-increased 32, extra-extra-large 48 (dp), full = fully rounded. The three Expressive steps
(large-increased, extra-large-increased, extra-extra-large) may be missing from older libraries.

## CSS custom properties (web)

| Token | CSS |
| --- | --- |
| Color role | `--md-sys-color-<role>`, e.g. `--md-sys-color-on-primary-container` |
| Type style | `--md-sys-typescale-<role>-<size>-<prop>`, prop = `font`, `size`, `line-height`, `weight`, `tracking` |
| Shape | `--md-sys-shape-corner-<step>`, e.g. `--md-sys-shape-corner-medium`; full = `9999px` (pill, not 50%) |

- `export --format css` writes light values on `:root`, dark values under `@media (prefers-color-scheme: dark)` and
  `[data-theme="dark"]`. `export --tokens type|shape --format css` writes the type and shape variables.
- Sizes in rem (px / 16) so text follows the user's font size; tracking in em (tracking / size).
- Components use `var(--md-sys-color-*)` etc. only. Material Web components read the same variable names.
- Tailwind: `export --format tailwind` maps role names to the CSS variables (`bg-primary text-on-primary`).

## Jetpack Compose

| Token | Compose |
| --- | --- |
| Theme | `MaterialTheme(colorScheme = ..., typography = ..., shapes = ...) { ... }` |
| Color role | `MaterialTheme.colorScheme.<camelCase>`: `primary`, `onPrimaryContainer`, `surfaceContainerHigh`, `inverseOnSurface`, `outlineVariant` |
| Scheme | `lightColorScheme(...)`, `darkColorScheme(...)` (`export --format compose`); dynamic color on Android 12+: `dynamicLightColorScheme(context)`, `dynamicDarkColorScheme(context)` |
| Type style | `MaterialTheme.typography.<camelCase>`: `displayLarge` ... `labelSmall` (15 `TextStyle`s in `Typography(...)`) |
| Shape | `MaterialTheme.shapes.extraSmall`, `small`, `medium`, `large`, `extraLarge` (`Shapes(...)`); none = `RectangleShape`, full = `CircleShape` |

- Text sizes in `sp` (`fontSize = 16.sp, lineHeight = 24.sp, letterSpacing = 0.5.sp`); dimensions in `dp`.
- Content color: `contentColorFor(background)` returns the matching `on-*` role.
- `background`/`onBackground` mirror `surface`/`onSurface`. Roles without a `lightColorScheme` parameter in the
  project's version (fixed roles, shadow) are exported as separate constants.

## Flutter

| Token | Flutter |
| --- | --- |
| Theme | `ThemeData(useMaterial3: true, colorScheme: ..., textTheme: ...)` (Material 3 is the default since Flutter 3.16) |
| Color role | `Theme.of(context).colorScheme.<camelCase>`: `primary`, `onPrimaryContainer`, `surfaceContainerHigh`, `outlineVariant` |
| Scheme | `ColorScheme(brightness: ..., ...)` (`export --format flutter`) or `ColorScheme.fromSeed(seedColor: ..., brightness: ...)` |
| Type style | `Theme.of(context).textTheme.<camelCase>`: `displayLarge` ... `labelSmall` (same 15 names) |
| Shape | No theme-wide shape scale: set `RoundedRectangleBorder(borderRadius: BorderRadius.circular(12))` in component themes (`cardTheme`, `dialogTheme`, ...); full = `StadiumBorder()` |

- Name differences: `inverse-on-surface` is `onInverseSurface`. `surfaceVariant` and `background` are deprecated in
  Flutter: use `surfaceContainerHighest` for fills and `surface` for backgrounds. Fixed roles need Flutter 3.22+.
- Sizes in logical pixels: `TextStyle(fontSize: 16, height: 24 / 16, letterSpacing: 0.5)` (`height` is a ratio).

## Other stacks

- Put the role names in the stack's theme object (SwiftUI asset catalog or environment values, React Native or
  React theme providers, design-tool variables) and keep the M3 names (`primary`, `on-primary`, ...) as keys.
- Export JSON tokens (`export --format json`, W3C DTCG) for token pipelines such as Style Dictionary.
- Never hardcode hex values in components; every color comes from a role, every text style from the type scale,
  every corner from the shape scale. A component that needs a color without a role gets a documented custom role
  (palette + tone per theme + contrast check), not a literal.
- Libraries that only look like M3 may use other role names or shape defaults: map them explicitly in the brief.

## Components: usual names in Compose and Flutter

| M3 component | Jetpack Compose | Flutter |
| --- | --- | --- |
| Filled / tonal / outlined / text / elevated button | `Button`, `FilledTonalButton`, `OutlinedButton`, `TextButton`, `ElevatedButton` | `FilledButton`, `FilledButton.tonal`, `OutlinedButton`, `TextButton`, `ElevatedButton` |
| Icon button (standard, filled, tonal, outlined) | `IconButton`, `FilledIconButton`, `FilledTonalIconButton`, `OutlinedIconButton` | `IconButton`, `IconButton.filled`, `IconButton.filledTonal`, `IconButton.outlined` |
| FAB, small, large, extended | `FloatingActionButton`, `SmallFloatingActionButton`, `LargeFloatingActionButton`, `ExtendedFloatingActionButton` | `FloatingActionButton`, `.small`, `.large`, `.extended` |
| Segmented button | `SegmentedButton` inside `SingleChoiceSegmentedButtonRow` or `MultiChoiceSegmentedButtonRow` | `SegmentedButton` with `ButtonSegment`s |
| Chips: assist, filter, input, suggestion | `AssistChip`, `FilterChip`, `InputChip`, `SuggestionChip` | `ActionChip` (assist and suggestion), `FilterChip`, `InputChip`; `ChoiceChip` for single choice |
| Top app bar (small, center-aligned, medium, large) | `TopAppBar`, `CenterAlignedTopAppBar`, `MediumTopAppBar`, `LargeTopAppBar` | `AppBar` (`centerTitle`), `SliverAppBar.medium`, `SliverAppBar.large` |
| Bottom app bar | `BottomAppBar` | `BottomAppBar` |
| Navigation bar | `NavigationBar` + `NavigationBarItem` | `NavigationBar` + `NavigationDestination` |
| Navigation rail | `NavigationRail` + `NavigationRailItem` | `NavigationRail` + `NavigationRailDestination` |
| Navigation drawer (modal) | `ModalNavigationDrawer` + `ModalDrawerSheet` + `NavigationDrawerItem` | `NavigationDrawer` + `NavigationDrawerDestination` (in `Scaffold.drawer`) |
| Bottom sheet (modal / standard) | `ModalBottomSheet` / `BottomSheetScaffold` | `showModalBottomSheet` / `Scaffold.bottomSheet` or `showBottomSheet` |
| Dialog (basic / full-screen) | `AlertDialog` / `Dialog` with full-screen content | `AlertDialog` via `showDialog` / `Dialog.fullscreen` |
| Snackbar | `Snackbar` via `SnackbarHost` and `SnackbarHostState` | `SnackBar` via `ScaffoldMessenger.of(context).showSnackBar` |
| Card (elevated, filled, outlined) | `ElevatedCard`, `Card`, `OutlinedCard` | `Card`, `Card.filled`, `Card.outlined` |
| List item | `ListItem` | `ListTile` |
| Divider | `HorizontalDivider`, `VerticalDivider` | `Divider`, `VerticalDivider` |
| Text field (filled / outlined) | `TextField` / `OutlinedTextField` | `TextField` with `InputDecoration(filled: true)` / with `OutlineInputBorder` |
| Checkbox, radio button, switch | `Checkbox`, `RadioButton`, `Switch` | `Checkbox`, `Radio`, `Switch` |
| Slider (single, range) | `Slider`, `RangeSlider` | `Slider`, `RangeSlider` |
| Progress indicators | `LinearProgressIndicator`, `CircularProgressIndicator` | `LinearProgressIndicator`, `CircularProgressIndicator` |
| Menu | `DropdownMenu` + `DropdownMenuItem`; `ExposedDropdownMenuBox` for a select field | `MenuAnchor` + `MenuItemButton`; `DropdownMenu` for a select field |
| Tabs (primary / secondary) | `PrimaryTabRow` / `SecondaryTabRow` + `Tab` | `TabBar` / `TabBar.secondary` + `Tab` |
| Badge | `Badge` inside `BadgedBox` | `Badge` |
| Tooltip (plain / rich) | `PlainTooltip` / `RichTooltip` inside `TooltipBox` | `Tooltip` (no built-in rich tooltip with actions) |
| Search | `SearchBar`, `DockedSearchBar` | `SearchBar`, `SearchAnchor` |
| Date / time picker | `DatePicker`, `DatePickerDialog` / `TimePicker` | `showDatePicker` / `showTimePicker` |
| Carousel | `HorizontalMultiBrowseCarousel`, `HorizontalUncontainedCarousel` | `CarouselView` |

M3 Expressive components (button groups, split buttons, FAB menu, toolbars, loading indicator, shape morph) are
newer: Compose exposes them in recent material3 versions, often as experimental APIs; Flutter's core library may not
have them. In a brief, describe them by M3 name and spec (styles.md, expressive.md) and let the implementer pick
the API, or build them from the standard components with the same tokens.
