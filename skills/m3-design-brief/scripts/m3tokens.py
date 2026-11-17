#!/usr/bin/env python3
"""m3tokens.py - Material 3 color scheme, contrast check and token export.

Standard library only, Python 3.8+, deterministic output.

Subcommands:
  scheme --seed "#RRGGBB" [--name NAME] [--variant tonal-spot] [--out FILE]
      Approximate M3 tonal-spot scheme (light, dark, tonal palettes) as JSON.
  check SCHEME.json [--format md|json] [--out FILE]
      WCAG 2.x contrast of the required role pairs. Exit 1 if a required pair fails.
  export [SCHEME.json] --format css|json|compose|flutter|tailwind [--tokens color|type|shape] [--out FILE]
      Color roles for a platform, or the type scale / shape scale as CSS custom properties.

Exit codes: 0 ok, 1 contrast failure (check), 2 bad input.
"""

import argparse
import decimal
import json
import math
import re
import sys

VERSION = "0.2.0"

# ---------------------------------------------------------------------------
# Color science: sRGB <-> XYZ (D65) <-> CIELAB <-> LCh(ab)
# ---------------------------------------------------------------------------

# D65 reference white (Y = 1)
WHITE = (0.95047, 1.0, 1.08883)

# sRGB (linear) to XYZ, IEC 61966-2-1
M_RGB_XYZ = (
    (0.4124564, 0.3575761, 0.1804375),
    (0.2126729, 0.7151522, 0.0721750),
    (0.0193339, 0.1191920, 0.9503041),
)
M_XYZ_RGB = (
    (3.2404542, -1.5371385, -0.4985314),
    (-0.9692660, 1.8760108, 0.0415560),
    (0.0556434, -0.2040259, 1.0572252),
)

EPS = 216.0 / 24389.0   # 0.008856
KAPPA = 24389.0 / 27.0  # 903.3


def _mul(m, v):
    return tuple(m[i][0] * v[0] + m[i][1] * v[1] + m[i][2] * v[2] for i in range(3))


def srgb_to_linear(c):
    """c in 0..1 (gamma-encoded) -> linear."""
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def linear_to_srgb(c):
    return 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055


def hex_to_rgb(h):
    """'#RRGGBB' or '#RGB' -> (r, g, b) ints. Raises ValueError."""
    s = h.strip()
    if s.startswith("#"):
        s = s[1:]
    if not re.fullmatch(r"[0-9a-fA-F]{3}|[0-9a-fA-F]{6}", s):
        raise ValueError("not a hex color: %r (use #RRGGBB)" % h)
    if len(s) == 3:
        s = "".join(ch * 2 for ch in s)
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#%02X%02X%02X" % tuple(rgb)


def rgb_to_xyz(rgb):
    lin = tuple(srgb_to_linear(c / 255.0) for c in rgb)
    return _mul(M_RGB_XYZ, lin)


def xyz_to_linear_rgb(xyz):
    return _mul(M_XYZ_RGB, xyz)


def _f(t):
    return t ** (1.0 / 3.0) if t > EPS else (KAPPA * t + 16.0) / 116.0


def _finv(t):
    t3 = t ** 3
    return t3 if t3 > EPS else (116.0 * t - 16.0) / KAPPA


def xyz_to_lab(xyz):
    fx, fy, fz = (_f(xyz[i] / WHITE[i]) for i in range(3))
    return (116.0 * fy - 16.0, 500.0 * (fx - fy), 200.0 * (fy - fz))


def lab_to_xyz(lab):
    L, a, b = lab
    fy = (L + 16.0) / 116.0
    fx = fy + a / 500.0
    fz = fy - b / 200.0
    return (WHITE[0] * _finv(fx), WHITE[1] * _finv(fy), WHITE[2] * _finv(fz))


def lab_to_lch(lab):
    L, a, b = lab
    c = math.hypot(a, b)
    h = math.degrees(math.atan2(b, a)) % 360.0 if c > 1e-3 else 0.0
    return (L, c, h)


def lch_to_lab(lch):
    L, c, h = lch
    r = math.radians(h)
    return (L, c * math.cos(r), c * math.sin(r))


def hex_to_lch(h):
    return lab_to_lch(xyz_to_lab(rgb_to_xyz(hex_to_rgb(h))))


def lch_to_linear_rgb(lch):
    return xyz_to_linear_rgb(lab_to_xyz(lch_to_lab(lch)))


def _in_gamut(lin, tol=1e-9):
    return all(-tol <= c <= 1.0 + tol for c in lin)


def _quantize(lin):
    out = []
    for c in lin:
        c = min(1.0, max(0.0, c))
        out.append(int(linear_to_srgb(c) * 255.0 + 0.5))
    return tuple(min(255, max(0, v)) for v in out)


def lch_to_hex_gamut(L, chroma, hue):
    """Color with CIE L* = L and the given hue; chroma reduced by binary search
    until the color fits sRGB. Returns (hex, used_chroma)."""
    L = min(100.0, max(0.0, float(L)))
    if L <= 0.0:
        return "#000000", 0.0
    if L >= 100.0:
        return "#FFFFFF", 0.0
    if _in_gamut(lch_to_linear_rgb((L, chroma, hue))):
        c_used = chroma
    else:
        lo, hi = 0.0, float(chroma)
        for _ in range(50):
            mid = (lo + hi) / 2.0
            if _in_gamut(lch_to_linear_rgb((L, mid, hue))):
                lo = mid
            else:
                hi = mid
        c_used = lo
    return rgb_to_hex(_quantize(lch_to_linear_rgb((L, c_used, hue)))), c_used


def relative_luminance(h):
    """WCAG 2.x relative luminance of a hex color."""
    r, g, b = (srgb_to_linear(c / 255.0) for c in hex_to_rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(fg, bg):
    l1, l2 = relative_luminance(fg), relative_luminance(bg)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def lstar(h):
    return hex_to_lch(h)[0]


# ---------------------------------------------------------------------------
# Scheme definition (material-color-utilities defaults, tonal-spot)
# ---------------------------------------------------------------------------

# Palette chroma (HCT/CAM16 units in M3, used here as CIE LCh(ab) chroma: an approximation).
PALETTE_SPECS = (
    # name, hue offset or fixed hue, chroma
    ("primary", ("seed", 0.0), 36.0),
    ("secondary", ("seed", 0.0), 16.0),
    ("tertiary", ("seed", 60.0), 24.0),
    ("neutral", ("seed", 0.0), 6.0),
    ("neutral-variant", ("seed", 0.0), 8.0),
    # M3 error: HCT hue 25, chroma 84. HCT hue 25 is about LCh(ab) hue 36 (the hue of the M3 baseline
    # error #BA1A1A), so the LCh hue 36 is used to keep error red rather than crimson.
    ("error", ("fixed", 36.0), 84.0),
)

STANDARD_TONES = (0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 98, 99, 100)


def _role_table():
    """(role, palette, light tone, dark tone) in output order."""
    rows = []
    for g, pal in (("primary", "primary"), ("secondary", "secondary"),
                   ("tertiary", "tertiary"), ("error", "error")):
        rows += [
            (g, pal, 40, 80),
            ("on-" + g, pal, 100, 20),
            (g + "-container", pal, 90, 30),
            ("on-" + g + "-container", pal, 30, 90),
        ]
    rows += [
        ("surface", "neutral", 98, 6),
        ("on-surface", "neutral", 10, 90),
        ("surface-variant", "neutral-variant", 90, 30),
        ("on-surface-variant", "neutral-variant", 30, 80),
        ("surface-container-lowest", "neutral", 100, 4),
        ("surface-container-low", "neutral", 96, 10),
        ("surface-container", "neutral", 94, 12),
        ("surface-container-high", "neutral", 92, 17),
        ("surface-container-highest", "neutral", 90, 22),
        ("surface-dim", "neutral", 87, 6),
        ("surface-bright", "neutral", 98, 24),
        ("inverse-surface", "neutral", 20, 90),
        ("inverse-on-surface", "neutral", 95, 20),
        ("inverse-primary", "primary", 80, 40),
        ("outline", "neutral-variant", 50, 60),
        ("outline-variant", "neutral-variant", 80, 30),
        ("shadow", "neutral", 0, 0),
        ("scrim", "neutral", 0, 0),
    ]
    for g in ("primary", "secondary", "tertiary"):
        rows += [
            (g + "-fixed", g, 90, 90),
            (g + "-fixed-dim", g, 80, 80),
            ("on-" + g + "-fixed", g, 10, 10),
            ("on-" + g + "-fixed-variant", g, 30, 30),
        ]
    return tuple(rows)


ROLE_TABLE = _role_table()
ROLES = tuple(r[0] for r in ROLE_TABLE)

METHOD = (
    "Approximation of the Material 3 tonal-spot scheme. The seed is converted to CIE LCh(ab) (sRGB, D65). "
    "HCT tone equals CIE L*, so each role color is built with L* = its tone and the palette's hue and chroma, "
    "reducing chroma by binary search until the color fits sRGB. Palettes: primary (seed hue, chroma 36), "
    "secondary (seed hue, 16), tertiary (seed hue + 60, 24), neutral (seed hue, 6), neutral-variant (seed hue, 8), "
    "error (HCT hue 25, chroma 84; applied as LCh hue 36, the LCh hue of the M3 baseline error #BA1A1A). The chroma numbers are HCT/CAM16 units in M3; using them as LCh(ab) chroma and "
    "LCh hue in place of CAM16 hue is an approximation. Role tones: material-color-utilities defaults."
)
NOTE = (
    "Approximate. Contrast between roles is preserved because luminance depends only on L* (= tone); hue and "
    "colorfulness differ slightly from the official tools. For exact values regenerate with Material Theme "
    "Builder or the material-color-utilities library."
)


def build_scheme(seed, name=None, variant="tonal-spot"):
    seed_hex = rgb_to_hex(hex_to_rgb(seed))
    L0, C0, H0 = hex_to_lch(seed_hex)
    pal_def = {}
    for pname, (kind, val), chroma in PALETTE_SPECS:
        hue = (H0 + val) % 360.0 if kind == "seed" else val
        pal_def[pname] = (hue, chroma)

    cache = {}

    def tone(pname, t):
        key = (pname, t)
        if key not in cache:
            hue, chroma = pal_def[pname]
            cache[key] = lch_to_hex_gamut(t, chroma, hue)[0]
        return cache[key]

    light, dark, role_meta = {}, {}, {}
    for role, pname, lt, dt in ROLE_TABLE:
        light[role] = tone(pname, lt)
        dark[role] = tone(pname, dt)
        role_meta[role] = {"palette": pname, "light": lt, "dark": dt}

    palettes = {}
    for pname, _, _ in PALETTE_SPECS:
        used = {t for (p, t) in cache if p == pname}
        tones = sorted(set(STANDARD_TONES) | used)
        palettes[pname] = {str(t): tone(pname, t) for t in tones}

    meta = {
        "generator": "m3tokens.py %s" % VERSION,
        "name": name or "",
        "seed": seed_hex,
        "seed_lch": {"l": round(L0, 2), "c": round(C0, 2), "h": round(H0, 2)},
        "variant": variant,
        "method": METHOD,
        "note": NOTE,
        "palette_specs": {p: {"hue": round(h, 2), "chroma": c} for p, (h, c) in pal_def.items()},
        "roles": role_meta,
    }
    return {"meta": meta, "light": light, "dark": dark, "palettes": palettes}


# ---------------------------------------------------------------------------
# Loading schemes (generated or hand-written brand palettes)
# ---------------------------------------------------------------------------

class InputError(Exception):
    pass


def normalize_role(key):
    k = key.strip()
    for prefix in ("--md-sys-color-", "md-sys-color-", "md.sys.color.", "md_sys_color_"):
        if k.lower().startswith(prefix):
            k = k[len(prefix):]
            break
    k = re.sub(r"(?<=[a-z0-9])([A-Z])", r"-\1", k)  # camelCase -> kebab
    k = k.replace("_", "-").replace(".", "-").replace(" ", "-").lower()
    return k


def load_scheme(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except OSError as e:
        raise InputError("cannot read %s: %s" % (path, e))
    except ValueError as e:
        raise InputError("invalid JSON in %s: %s" % (path, e))
    if not isinstance(data, dict):
        raise InputError("scheme must be a JSON object with 'light' and/or 'dark'")
    themes = {}
    for theme in ("light", "dark"):
        if theme not in data:
            continue
        roles = data[theme]
        if not isinstance(roles, dict):
            raise InputError("'%s' must be an object of role: hex" % theme)
        out = {}
        for k, v in roles.items():
            if isinstance(v, dict) and "$value" in v:
                v = v["$value"]
            if not isinstance(v, str):
                raise InputError("%s.%s: value must be a hex string" % (theme, k))
            try:
                out[normalize_role(k)] = rgb_to_hex(hex_to_rgb(v))
            except ValueError as e:
                raise InputError("%s.%s: %s" % (theme, k, e))
        themes[theme] = out
    if not themes:
        raise InputError("scheme has neither 'light' nor 'dark'")
    meta = data.get("meta") if isinstance(data.get("meta"), dict) else {}
    return {"meta": meta, "themes": themes}


# ---------------------------------------------------------------------------
# check
# ---------------------------------------------------------------------------

SURFACES = ("surface", "surface-dim", "surface-bright", "surface-container-lowest",
            "surface-container-low", "surface-container", "surface-container-high",
            "surface-container-highest", "surface-variant")


def required_pairs():
    """(foreground, background, minimum, kind). kind: text | non-text | decorative."""
    pairs = []
    for g in ("primary", "secondary", "tertiary", "error"):
        pairs.append(("on-" + g, g, 4.5, "text"))
        pairs.append(("on-" + g + "-container", g + "-container", 4.5, "text"))
    for g in ("primary", "secondary", "tertiary", "error"):
        pairs.append((g, "surface", 4.5, "text"))
    for g in ("primary", "secondary", "tertiary"):
        pairs.append(("on-" + g + "-fixed", g + "-fixed", 4.5, "text"))
        pairs.append(("on-" + g + "-fixed-variant", g + "-fixed", 4.5, "text"))
    for fg in ("on-surface", "on-surface-variant"):
        for bg in SURFACES:
            pairs.append((fg, bg, 4.5, "text"))
    pairs.append(("inverse-on-surface", "inverse-surface", 4.5, "text"))
    pairs.append(("inverse-primary", "inverse-surface", 4.5, "text"))
    pairs.append(("outline", "surface", 3.0, "non-text"))
    pairs.append(("outline-variant", "surface", None, "decorative"))
    return tuple(pairs)


def run_check(scheme):
    pairs = required_pairs()
    needed = sorted({p[0] for p in pairs} | {p[1] for p in pairs})
    result = {"themes": {}, "pass": True}
    for theme, roles in scheme["themes"].items():
        rows, missing = [], [r for r in ROLES if r not in roles]
        for fg, bg, minimum, kind in pairs:
            row = {"fg": fg, "bg": bg, "kind": kind, "min": minimum}
            if fg not in roles or bg not in roles:
                row.update({"ratio": None, "status": "skipped"})
            else:
                ratio = contrast_ratio(roles[fg], roles[bg])
                row["fg_hex"], row["bg_hex"] = roles[fg], roles[bg]
                row["ratio"] = math.floor(ratio * 100) / 100.0
                if minimum is None:
                    row["status"] = "info"
                elif ratio >= minimum:
                    row["status"] = "pass"
                else:
                    row["status"] = "fail"
                    result["pass"] = False
            rows.append(row)
        unknown = sorted(k for k in roles if k not in ROLES)
        checked = [r for r in rows if r["status"] in ("pass", "fail")]
        result["themes"][theme] = {
            "pairs": rows,
            "missing_roles": missing,
            "missing_for_check": [r for r in needed if r not in roles],
            "unknown_roles": unknown,
            "summary": {
                "required": len(checked),
                "passed": sum(1 for r in checked if r["status"] == "pass"),
                "failed": sum(1 for r in checked if r["status"] == "fail"),
                "skipped": sum(1 for r in rows if r["status"] == "skipped"),
            },
        }
    return result


def format_check_md(result, meta):
    out = ["# Contrast check (WCAG 2.x)", ""]
    if meta.get("seed"):
        out.append("Seed %s, variant %s. %s" % (meta.get("seed"), meta.get("variant", ""), meta.get("note", "")))
        out.append("")
    out.append("Text pairs need 4.5:1, outline on surface needs 3:1, outline-variant is decorative (reported only). "
               "Ratios are truncated to two decimals.")
    out.append("")
    for theme, t in result["themes"].items():
        s = t["summary"]
        out.append("## %s: %d/%d required pairs pass%s" % (
            theme, s["passed"], s["required"],
            (", %d skipped (missing roles)" % s["skipped"]) if s["skipped"] else ""))
        out.append("")
        out.append("| Foreground | Background | Colors | Ratio | Needs | Result |")
        out.append("| --- | --- | --- | --- | --- | --- |")
        for r in t["pairs"]:
            colors = "%s on %s" % (r["fg_hex"], r["bg_hex"]) if "fg_hex" in r else "-"
            ratio = "%.2f:1" % r["ratio"] if r["ratio"] is not None else "-"
            needs = "%g:1" % r["min"] if r["min"] else "decorative"
            out.append("| %s | %s | %s | %s | %s | %s |" % (r["fg"], r["bg"], colors, ratio, needs, r["status"]))
        out.append("")
        if t["missing_roles"]:
            out.append("Missing roles: " + ", ".join(t["missing_roles"]))
            out.append("")
        if t["unknown_roles"]:
            out.append("Unknown role names (ignored): " + ", ".join(t["unknown_roles"]))
            out.append("")
    out.append("Overall: %s" % ("PASS" if result["pass"] else "FAIL"))
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
# export: colors
# ---------------------------------------------------------------------------

def camel(role):
    parts = role.split("-")
    return parts[0] + "".join(p[:1].upper() + p[1:] for p in parts[1:])


def _header_lines(meta):
    lines = ["Material 3 color roles generated by m3tokens.py %s." % VERSION]
    if meta.get("seed"):
        lines.append("Seed %s, variant %s%s." % (meta["seed"], meta.get("variant", "tonal-spot"),
                                                 (", name " + meta["name"]) if meta.get("name") else ""))
    if meta.get("note"):
        lines.append(meta["note"])
    else:
        lines.append("Hand-written palette: run `m3tokens.py check` on it before use.")
    return lines


def _ordered(roles):
    known = [r for r in ROLES if r in roles]
    extra = sorted(r for r in roles if r not in ROLES)
    return known + extra


def export_css(scheme):
    meta, th = scheme["meta"], scheme["themes"]
    out = ["/*"] + [" * " + l for l in _header_lines(meta)] + [
        " * Light values on :root; dark values via prefers-color-scheme and [data-theme=\"dark\"].",
        " * Use the variables in components; never hardcode hex values.",
        " */"]

    def block(selector, roles, indent=""):
        lines = [indent + selector + " {"]
        for r in _ordered(roles):
            lines.append("%s  --md-sys-color-%s: %s;" % (indent, r, roles[r]))
        lines.append(indent + "}")
        return lines

    first = "light" if "light" in th else "dark"
    out += block(":root", th[first])
    if "light" in th and "dark" in th:
        out.append("")
        out.append("@media (prefers-color-scheme: dark) {")
        out += block(':root:not([data-theme="light"])', th["dark"], "  ")
        out.append("}")
        out.append("")
        out += block('[data-theme="dark"]', th["dark"])
        out.append("")
        out += block('[data-theme="light"]', th["light"])
    return "\n".join(out) + "\n"


def export_json(scheme):
    meta, th = scheme["meta"], scheme["themes"]
    doc = {"$description": " ".join(_header_lines(meta))}
    color = {}
    for theme in ("light", "dark"):
        if theme in th:
            color[theme] = {r: {"$type": "color", "$value": th[theme][r]} for r in _ordered(th[theme])}
    doc["md"] = {"sys": {"color": color}}
    return json.dumps(doc, indent=2, ensure_ascii=False) + "\n"


# Compose lightColorScheme/darkColorScheme parameters (androidx.compose.material3).
COMPOSE_PARAMS = (
    "primary", "on-primary", "primary-container", "on-primary-container", "inverse-primary",
    "secondary", "on-secondary", "secondary-container", "on-secondary-container",
    "tertiary", "on-tertiary", "tertiary-container", "on-tertiary-container",
    "surface", "on-surface", "surface-variant", "on-surface-variant",
    "inverse-surface", "inverse-on-surface",
    "error", "on-error", "error-container", "on-error-container",
    "outline", "outline-variant", "scrim",
    "surface-bright", "surface-container", "surface-container-high", "surface-container-highest",
    "surface-container-low", "surface-container-lowest", "surface-dim",
)


def _argb(hexv):
    return "0xFF" + hexv[1:].upper()


def export_compose(scheme):
    meta, th = scheme["meta"], scheme["themes"]
    out = ["// " + l for l in _header_lines(meta)]
    out += [
        "// Jetpack Compose Material 3: pass to MaterialTheme(colorScheme = ...).",
        "// background/onBackground mirror surface/onSurface; surfaceTint mirrors primary.",
        "// Roles without a lightColorScheme parameter (shadow, fixed roles) are emitted as separate",
        "// constants below; recent material3 versions also expose fixed roles on ColorScheme.",
        "",
        "import androidx.compose.material3.darkColorScheme",
        "import androidx.compose.material3.lightColorScheme",
        "import androidx.compose.ui.graphics.Color",
        "",
    ]
    for theme, fn, val in (("light", "lightColorScheme", "LightColorScheme"),
                           ("dark", "darkColorScheme", "DarkColorScheme")):
        if theme not in th:
            continue
        roles = th[theme]
        out.append("val %s = %s(" % (val, fn))
        for r in COMPOSE_PARAMS:
            if r in roles:
                out.append("    %s = Color(%s)," % (camel(r), _argb(roles[r])))
        if "surface" in roles:
            out.append("    background = Color(%s)," % _argb(roles["surface"]))
        if "on-surface" in roles:
            out.append("    onBackground = Color(%s)," % _argb(roles["on-surface"]))
        if "primary" in roles:
            out.append("    surfaceTint = Color(%s)," % _argb(roles["primary"]))
        out.append(")")
        out.append("")
        rest = [r for r in _ordered(roles) if r not in COMPOSE_PARAMS]
        if rest:
            prefix = "Light" if theme == "light" else "Dark"
            out.append("// %s theme roles without a lightColorScheme/darkColorScheme parameter" % theme)
            for r in rest:
                name = prefix + camel(r)[:1].upper() + camel(r)[1:]
                out.append("val %s = Color(%s)" % (name, _argb(roles[r])))
            out.append("")
    return "\n".join(out)


# Flutter ColorScheme properties (Flutter 3.22+). Key: role name, value: Flutter property.
FLUTTER_PROPS = (
    ("primary", "primary"), ("on-primary", "onPrimary"),
    ("primary-container", "primaryContainer"), ("on-primary-container", "onPrimaryContainer"),
    ("primary-fixed", "primaryFixed"), ("primary-fixed-dim", "primaryFixedDim"),
    ("on-primary-fixed", "onPrimaryFixed"), ("on-primary-fixed-variant", "onPrimaryFixedVariant"),
    ("secondary", "secondary"), ("on-secondary", "onSecondary"),
    ("secondary-container", "secondaryContainer"), ("on-secondary-container", "onSecondaryContainer"),
    ("secondary-fixed", "secondaryFixed"), ("secondary-fixed-dim", "secondaryFixedDim"),
    ("on-secondary-fixed", "onSecondaryFixed"), ("on-secondary-fixed-variant", "onSecondaryFixedVariant"),
    ("tertiary", "tertiary"), ("on-tertiary", "onTertiary"),
    ("tertiary-container", "tertiaryContainer"), ("on-tertiary-container", "onTertiaryContainer"),
    ("tertiary-fixed", "tertiaryFixed"), ("tertiary-fixed-dim", "tertiaryFixedDim"),
    ("on-tertiary-fixed", "onTertiaryFixed"), ("on-tertiary-fixed-variant", "onTertiaryFixedVariant"),
    ("error", "error"), ("on-error", "onError"),
    ("error-container", "errorContainer"), ("on-error-container", "onErrorContainer"),
    ("surface", "surface"), ("on-surface", "onSurface"),
    ("surface-dim", "surfaceDim"), ("surface-bright", "surfaceBright"),
    ("surface-container-lowest", "surfaceContainerLowest"), ("surface-container-low", "surfaceContainerLow"),
    ("surface-container", "surfaceContainer"), ("surface-container-high", "surfaceContainerHigh"),
    ("surface-container-highest", "surfaceContainerHighest"),
    ("on-surface-variant", "onSurfaceVariant"),
    ("outline", "outline"), ("outline-variant", "outlineVariant"),
    ("shadow", "shadow"), ("scrim", "scrim"),
    ("inverse-surface", "inverseSurface"), ("inverse-on-surface", "onInverseSurface"),
    ("inverse-primary", "inversePrimary"),
)
FLUTTER_REQUIRED = ("primary", "on-primary", "secondary", "on-secondary", "error", "on-error",
                    "surface", "on-surface")


def export_flutter(scheme):
    meta, th = scheme["meta"], scheme["themes"]
    mapped = {r for r, _ in FLUTTER_PROPS}
    out = ["// " + l for l in _header_lines(meta)]
    out += [
        "// Flutter Material 3 (Flutter 3.22+): ThemeData(useMaterial3: true, colorScheme: lightColorScheme).",
        "// Flutter names differ for some roles: inverse-on-surface -> onInverseSurface.",
        "// Left out: surface-variant (deprecated in Flutter; use surfaceContainerHighest for fills),",
        "// background/onBackground (deprecated; Flutter uses surface/onSurface).",
        "// surfaceTint mirrors primary.",
        "",
        "import 'package:flutter/material.dart';",
        "",
    ]
    for theme, brightness, val in (("light", "Brightness.light", "lightColorScheme"),
                                   ("dark", "Brightness.dark", "darkColorScheme")):
        if theme not in th:
            continue
        roles = th[theme]
        missing_req = [r for r in FLUTTER_REQUIRED if r not in roles]
        if missing_req:
            out.append("// %s: missing required ColorScheme roles: %s" % (theme, ", ".join(missing_req)))
        out.append("const ColorScheme %s = ColorScheme(" % val)
        out.append("  brightness: %s," % brightness)
        for r, prop in FLUTTER_PROPS:
            if r in roles:
                out.append("  %s: Color(%s)," % (prop, _argb(roles[r])))
        if "primary" in roles:
            out.append("  surfaceTint: Color(%s)," % _argb(roles["primary"]))
        out.append(");")
        out.append("")
        left = [r for r in _ordered(roles) if r not in mapped]
        if left:
            out.append("// %s roles not in Flutter ColorScheme: %s" % (
                theme, ", ".join("%s %s" % (r, roles[r]) for r in left)))
            out.append("")
    return "\n".join(out)


def export_tailwind(scheme):
    meta, th = scheme["meta"], scheme["themes"]
    base = th.get("light") or th.get("dark")
    out = ["// " + l for l in _header_lines(meta)]
    out += [
        "// Tailwind theme.extend.colors using M3 role names. Each color reads the CSS custom property",
        "// from `m3tokens.py export --format css` (load that CSS for light/dark switching); the hex is the",
        "// fallback (light theme). Example: bg-primary text-on-primary, bg-surface-container text-on-surface.",
        "module.exports = {",
        "  theme: {",
        "    extend: {",
        "      colors: {",
    ]
    for r in _ordered(base):
        out.append("        '%s': 'var(--md-sys-color-%s, %s)'," % (r, r, base[r]))
    out += ["      },", "    },", "  },", "};"]
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
# export: type and shape
# ---------------------------------------------------------------------------

# Baseline M3 type scale shipped by the Material 3 libraries:
# role: (size sp, line height sp, tracking sp, weight)
TYPE_SCALE = (
    ("display-large", 57, 64, -0.25, 400),
    ("display-medium", 45, 52, 0, 400),
    ("display-small", 36, 44, 0, 400),
    ("headline-large", 32, 40, 0, 400),
    ("headline-medium", 28, 36, 0, 400),
    ("headline-small", 24, 32, 0, 400),
    ("title-large", 22, 28, 0, 400),
    ("title-medium", 16, 24, 0.15, 500),
    ("title-small", 14, 20, 0.1, 500),
    ("body-large", 16, 24, 0.5, 400),
    ("body-medium", 14, 20, 0.25, 400),
    ("body-small", 12, 16, 0.4, 400),
    ("label-large", 14, 20, 0.1, 500),
    ("label-medium", 12, 16, 0.5, 500),
    ("label-small", 11, 16, 0.5, 500),
)
BRAND_FONT_ROLES = ("display", "headline")

# Shape scale: styles.md SHP-01 (styles/shape/corner-radius-scale@2026-05-06).
SHAPE_SCALE = (
    ("none", "0px"), ("extra-small", "4px"), ("small", "8px"), ("medium", "12px"),
    ("large", "16px"), ("large-increased", "20px"), ("extra-large", "28px"),
    ("extra-large-increased", "32px"), ("extra-extra-large", "48px"), ("full", "9999px"),
)


def _num(x, places=4):
    q = decimal.Decimal(repr(x)).quantize(decimal.Decimal(1).scaleb(-places), rounding=decimal.ROUND_HALF_UP)
    s = format(q, "f")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def export_type_css():
    out = [
        "/*",
        " * Material 3 baseline type scale (15 styles) as CSS custom properties, m3tokens.py %s." % VERSION,
        " * Values: baseline M3 type scale shipped by the Material 3 libraries. The docs",
        " * (styles/typography/type-scale-tokens@2026-05-06) name the tokens md.sys.typescale.<role>-<size>.",
        " * {font, size, line-height, tracking, weight} but show the numeric table only as an image.",
        " * Sizes in sp = CSS px; size and line height emitted in rem (px / 16); tracking in em (tracking / size).",
        " * Font: display and headline use the brand typeface, the rest the plain typeface",
        " * (M3 typography: brand face for large styles, plain face for small ones); change the two --md-ref-typeface-*",
        " * values to use a brand font. Emphasized styles are not included.",
        " */",
        ":root {",
        "  --md-ref-typeface-brand: Roboto, \"Noto Sans\", system-ui, sans-serif;",
        "  --md-ref-typeface-plain: Roboto, \"Noto Sans\", system-ui, sans-serif;",
    ]
    for role, size, lh, tr, wt in TYPE_SCALE:
        face = "brand" if role.split("-")[0] in BRAND_FONT_ROLES else "plain"
        p = "  --md-sys-typescale-" + role
        out.append("%s-font: var(--md-ref-typeface-%s);" % (p, face))
        out.append("%s-size: %srem; /* %dpx */" % (p, _num(size / 16.0), size))
        out.append("%s-line-height: %srem; /* %dpx */" % (p, _num(lh / 16.0), lh))
        out.append("%s-weight: %d;" % (p, wt))
        out.append("%s-tracking: %sem; /* %spx */" % (p, _num(tr / float(size)), _num(tr, 2)))
    out.append("}")
    return "\n".join(out) + "\n"


def export_shape_css():
    out = [
        "/*",
        " * Material 3 shape (corner radius) scale, m3tokens.py %s." % VERSION,
        " * Values: M3 rule SHP-01 (m3.material.io/styles/shape/corner-radius-scale, 2026-05-06), 1dp = 1 CSS px.",
        " * Token names follow md.sys.shape.corner.<step> (used in the component spec tables).",
        " * large-increased, extra-large-increased and extra-extra-large are M3 Expressive additions",
        " * (styles/shape/overview-principles@2026-05-06). full = fully rounded (pill), not 50%.",
        " */",
        ":root {",
    ]
    for step, val in SHAPE_SCALE:
        tag = " /* Expressive */" if step in ("large-increased", "extra-large-increased", "extra-extra-large") else ""
        out.append("  --md-sys-shape-corner-%s: %s;%s" % (step, val, tag))
    out.append("}")
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _emit(text, out_path):
    if out_path:
        try:
            with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(text)
        except OSError as e:
            raise InputError("cannot write %s: %s" % (out_path, e))
    else:
        sys.stdout.write(text)


def cmd_scheme(args):
    if args.variant != "tonal-spot":
        raise InputError("only --variant tonal-spot is supported")
    try:
        scheme = build_scheme(args.seed, args.name, args.variant)
    except ValueError as e:
        raise InputError(str(e))
    _emit(json.dumps(scheme, indent=2, ensure_ascii=False) + "\n", args.out)
    return 0


def cmd_check(args):
    scheme = load_scheme(args.scheme)
    result = run_check(scheme)
    if args.format == "json":
        text = json.dumps(result, indent=2) + "\n"
    else:
        text = format_check_md(result, scheme["meta"])
    _emit(text, args.out)
    return 0 if result["pass"] else 1


def cmd_export(args):
    if args.tokens in ("type", "shape"):
        if args.format != "css":
            raise InputError("--tokens %s supports --format css only" % args.tokens)
        _emit(export_type_css() if args.tokens == "type" else export_shape_css(), args.out)
        return 0
    if not args.scheme:
        raise InputError("export --tokens color needs a scheme JSON file")
    scheme = load_scheme(args.scheme)
    fn = {"css": export_css, "json": export_json, "compose": export_compose,
          "flutter": export_flutter, "tailwind": export_tailwind}[args.format]
    _emit(fn(scheme), args.out)
    return 0


class _Parser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        sys.stderr.write("%s: error: %s\n" % (self.prog, message))
        sys.exit(2)


def build_parser():
    p = _Parser(prog="m3tokens.py", description=__doc__.split("\n\n")[0],
                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--version", action="version", version="m3tokens.py " + VERSION)
    sub = p.add_subparsers(dest="cmd", parser_class=_Parser)

    s = sub.add_parser("scheme", help="generate an approximate M3 tonal-spot scheme from a seed color",
                       description="Generate light and dark M3 color roles and tonal palettes from a seed "
                                   "(approximation of tonal-spot in CIE LCh; see meta.method and meta.note).")
    s.add_argument("--seed", required=True, help='seed color, "#RRGGBB"')
    s.add_argument("--name", default=None, help="scheme name stored in meta.name")
    s.add_argument("--variant", default="tonal-spot", help="scheme variant (only tonal-spot)")
    s.add_argument("--out", default=None, help="write to FILE instead of stdout")
    s.set_defaults(func=cmd_scheme)

    c = sub.add_parser("check", help="check WCAG contrast of the required role pairs",
                       description="Contrast (WCAG 2.x) of required role pairs per theme: text pairs 4.5:1, "
                                   "outline on surface 3:1, outline-variant reported only. Works with any JSON "
                                   "{\"light\": {role: hex}, \"dark\": {...}}; missing roles are listed. "
                                   "Exit 1 if a required pair fails.")
    c.add_argument("scheme", help="scheme JSON (from `scheme` or hand-written)")
    c.add_argument("--format", choices=("md", "json"), default="md")
    c.add_argument("--out", default=None, help="write to FILE instead of stdout")
    c.set_defaults(func=cmd_check)

    e = sub.add_parser("export", help="export color roles, type scale or shape scale",
                       description="Export color roles (css, json DTCG, compose, flutter, tailwind) from a "
                                   "scheme JSON, or the M3 type / shape scale as CSS custom properties "
                                   "(--tokens type|shape --format css, no scheme needed).")
    e.add_argument("scheme", nargs="?", default=None, help="scheme JSON (needed for --tokens color)")
    e.add_argument("--format", required=True, choices=("css", "json", "compose", "flutter", "tailwind"))
    e.add_argument("--tokens", choices=("color", "type", "shape"), default="color")
    e.add_argument("--out", default=None, help="write to FILE instead of stdout")
    e.set_defaults(func=cmd_export)
    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "cmd", None):
        parser.print_help(sys.stderr)
        return 2
    try:
        return args.func(args)
    except InputError as e:
        sys.stderr.write("m3tokens.py: error: %s\n" % e)
        return 2


if __name__ == "__main__":
    sys.exit(main())
