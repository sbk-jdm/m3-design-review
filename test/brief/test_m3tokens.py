"""Tests for skills/m3-design-brief/scripts/m3tokens.py (stdlib unittest).

Run from the repository root:  python3 -m unittest discover -s test/brief -v
"""

import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SCRIPT = os.path.join(ROOT, "skills", "m3-design-brief", "scripts", "m3tokens.py")
sys.dont_write_bytecode = True  # keep __pycache__ out of the skill folder
sys.path.insert(0, os.path.dirname(SCRIPT))

import m3tokens as m  # noqa: E402

SEEDS = {
    "blue": "#1E64D2",
    "red": "#D32F2F",
    "yellow": "#F5D000",
    "green": "#2E7D32",
    "grey": "#808080",
    "purple": "#6750A4",
}


def run_cli(*args):
    p = subprocess.run([sys.executable, SCRIPT] + list(args), capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def write_json(obj):
    fd, path = tempfile.mkstemp(suffix=".json")
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        json.dump(obj, fh)
    return path


class TestConversions(unittest.TestCase):
    def test_hex_roundtrip_through_lch(self):
        samples = ["#000000", "#FFFFFF", "#6750A4", "#FF0000", "#00FF00", "#0000FF",
                   "#808080", "#F5D000", "#123456", "#FEDCBA", "#010101"]
        for h in samples:
            L, c, hue = m.hex_to_lch(h)
            lin = m.lch_to_linear_rgb((L, c, hue))
            self.assertEqual(m.rgb_to_hex(m._quantize(lin)), h, h)

    def test_lab_xyz_roundtrip(self):
        for lab in [(50, 20, -30), (90, -5, 10), (10, 3, 3), (5, 0, 0)]:
            back = m.xyz_to_lab(m.lab_to_xyz(lab))
            for a, b in zip(lab, back):
                self.assertAlmostEqual(a, b, places=6)

    def test_known_values(self):
        self.assertAlmostEqual(m.hex_to_lch("#FFFFFF")[0], 100.0, places=2)
        self.assertAlmostEqual(m.hex_to_lch("#000000")[0], 0.0, places=4)
        self.assertAlmostEqual(m.relative_luminance("#FFFFFF"), 1.0, places=4)
        self.assertAlmostEqual(m.contrast_ratio("#000000", "#FFFFFF"), 21.0, places=2)
        self.assertAlmostEqual(m.contrast_ratio("#777777", "#FFFFFF"), 4.48, places=2)

    def test_gamut_mapping_keeps_lightness_and_hue(self):
        hexv, used = m.lch_to_hex_gamut(50, 200, 140)
        self.assertLess(used, 200)
        L, c, h = m.hex_to_lch(hexv)
        self.assertAlmostEqual(L, 50, delta=0.6)
        self.assertAlmostEqual(h, 140, delta=3)

    def test_bad_hex(self):
        for bad in ["#12345", "blue", "#GGGGGG", ""]:
            with self.assertRaises(ValueError):
                m.hex_to_rgb(bad)


class TestScheme(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schemes = {k: m.build_scheme(v) for k, v in SEEDS.items()}

    def test_every_role_in_both_themes(self):
        self.assertEqual(len(m.ROLES), 46)
        for name, s in self.schemes.items():
            for theme in ("light", "dark"):
                self.assertEqual(set(s[theme]), set(m.ROLES), "%s %s" % (name, theme))
                for v in s[theme].values():
                    self.assertRegex(v, r"^#[0-9A-F]{6}$")

    def test_tone_within_tolerance(self):
        for name, s in self.schemes.items():
            for role, pal, lt, dt in m.ROLE_TABLE:
                self.assertAlmostEqual(m.lstar(s["light"][role]), lt, delta=0.6, msg="%s light %s" % (name, role))
                self.assertAlmostEqual(m.lstar(s["dark"][role]), dt, delta=0.6, msg="%s dark %s" % (name, role))

    def test_palette_tones(self):
        s = self.schemes["purple"]
        self.assertEqual(set(s["palettes"]), {"primary", "secondary", "tertiary", "neutral",
                                              "neutral-variant", "error"})
        for pal in s["palettes"].values():
            for t in ("0", "10", "40", "90", "95", "98", "99", "100"):
                self.assertIn(t, pal)
            for t, v in pal.items():
                self.assertAlmostEqual(m.lstar(v), float(t), delta=0.6)

    def test_meta_states_approximation(self):
        meta = self.schemes["purple"]["meta"]
        self.assertIn("Approximat", meta["note"])
        self.assertIn("Material Theme Builder", meta["note"])
        self.assertIn("material-color-utilities", meta["note"])
        self.assertIn("LCh", meta["method"])
        self.assertEqual(meta["seed"], "#6750A4")
        self.assertEqual(meta["variant"], "tonal-spot")

    def test_deterministic(self):
        a = json.dumps(m.build_scheme("#6750A4"), sort_keys=True)
        b = json.dumps(m.build_scheme("#6750a4"), sort_keys=True)
        self.assertEqual(a, b)

    def test_tertiary_hue_shift(self):
        s = self.schemes["blue"]
        hp = m.hex_to_lch(s["light"]["primary"])[2]
        ht = m.hex_to_lch(s["light"]["tertiary"])[2]
        self.assertAlmostEqual((ht - hp) % 360, 60, delta=4)

    def test_fixed_roles_same_in_both_themes(self):
        s = self.schemes["green"]
        for r in m.ROLES:
            if "fixed" in r:
                self.assertEqual(s["light"][r], s["dark"][r], r)

    def test_check_passes_generated(self):
        for name, s in self.schemes.items():
            res = m.run_check({"meta": s["meta"], "themes": {"light": s["light"], "dark": s["dark"]}})
            self.assertTrue(res["pass"], name)
            for theme in ("light", "dark"):
                self.assertEqual(res["themes"][theme]["missing_roles"], [])
                self.assertEqual(res["themes"][theme]["summary"]["failed"], 0)


class TestCli(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        cls.paths = {}
        for name, seed in SEEDS.items():
            path = os.path.join(cls.tmp, name + ".json")
            code, out, err = run_cli("scheme", "--seed", seed, "--name", name, "--out", path)
            assert code == 0, err
            cls.paths[name] = path

    def test_scheme_stdout_is_json(self):
        code, out, err = run_cli("scheme", "--seed", "#6750A4")
        self.assertEqual(code, 0, err)
        d = json.loads(out)
        self.assertEqual(set(d), {"meta", "light", "dark", "palettes"})

    def test_check_passes_six_seeds(self):
        for name, path in self.paths.items():
            for fmt in ("md", "json"):
                code, out, err = run_cli("check", path, "--format", fmt)
                self.assertEqual(code, 0, "%s %s: %s" % (name, fmt, out))
            self.assertIn("Overall: PASS", run_cli("check", path)[1])

    def test_check_fails_bad_brand_palette(self):
        light = dict(json.load(open(self.paths["purple"]))["light"])
        light["primary"] = "#B39DDB"      # too light for white text
        light["on-primary"] = "#FFFFFF"
        path = write_json({"light": light})
        code, out, err = run_cli("check", path)
        self.assertEqual(code, 1, out)
        self.assertIn("fail", out)
        self.assertIn("Overall: FAIL", out)
        code, out, err = run_cli("check", path, "--format", "json")
        self.assertEqual(code, 1)
        self.assertFalse(json.loads(out)["pass"])

    def test_check_partial_brand_palette_lists_missing(self):
        brand = {"light": {"primary": "#1B5FAA", "onPrimary": "#FFFFFF",
                           "--md-sys-color-surface": "#FFFFFF", "on_surface": "#1F1F1F"}}
        path = write_json(brand)
        code, out, err = run_cli("check", path, "--format", "json")
        self.assertEqual(code, 0, out + err)
        d = json.loads(out)
        t = d["themes"]["light"]
        self.assertIn("outline", t["missing_roles"])
        self.assertGreater(t["summary"]["skipped"], 0)
        self.assertEqual(t["summary"]["failed"], 0)
        statuses = {(p["fg"], p["bg"]): p["status"] for p in t["pairs"]}
        self.assertEqual(statuses[("on-primary", "primary")], "pass")
        self.assertEqual(statuses[("on-surface", "surface")], "pass")

    def test_outline_variant_does_not_fail(self):
        light = dict(json.load(open(self.paths["blue"]))["light"])
        light["outline-variant"] = light["surface"]
        code, out, err = run_cli("check", write_json({"light": light}))
        self.assertEqual(code, 0, out)

    def test_outline_needs_3(self):
        light = dict(json.load(open(self.paths["blue"]))["light"])
        light["outline"] = "#D0D0D0"
        code, out, err = run_cli("check", write_json({"light": light}))
        self.assertEqual(code, 1, out)

    def test_exports_contain_every_role(self):
        path = self.paths["purple"]
        d = json.load(open(path))
        flutter_skip = {"surface-variant"}
        for fmt in ("css", "json", "compose", "flutter", "tailwind"):
            code, out, err = run_cli("export", path, "--format", fmt)
            self.assertEqual(code, 0, fmt + err)
            self.assertTrue(out.strip(), fmt)
            for role in m.ROLES:
                if fmt == "css":
                    needle = "--md-sys-color-%s:" % role
                elif fmt == "json":
                    needle = '"%s"' % role
                elif fmt == "tailwind":
                    needle = "'%s'" % role
                elif fmt == "compose":
                    needle = m.camel(role).lower()
                else:
                    if role in flutter_skip:
                        continue
                    needle = dict(m.FLUTTER_PROPS)[role] + ":"
                hay = out.lower() if fmt == "compose" else out
                self.assertIn(needle, hay, "%s missing %s" % (fmt, role))
            for role in ("primary", "surface"):
                self.assertIn(d["light"][role][1:].upper(), out.upper(), fmt)
            if fmt in ("css", "json", "compose", "flutter"):
                self.assertIn(d["dark"]["surface"][1:].upper(), out.upper(), fmt)

    def test_css_dark_blocks(self):
        out = run_cli("export", self.paths["red"], "--format", "css")[1]
        self.assertIn("@media (prefers-color-scheme: dark)", out)
        self.assertIn('[data-theme="dark"]', out)

    def test_json_export_is_dtcg(self):
        out = run_cli("export", self.paths["red"], "--format", "json")[1]
        d = json.loads(out)
        tok = d["md"]["sys"]["color"]["dark"]["primary"]
        self.assertEqual(tok["$type"], "color")
        self.assertRegex(tok["$value"], r"^#[0-9A-F]{6}$")

    def test_type_and_shape_exports(self):
        code, out, err = run_cli("export", "--tokens", "type", "--format", "css")
        self.assertEqual(code, 0, err)
        for role, size, lh, tr, wt in m.TYPE_SCALE:
            for prop in ("font", "size", "line-height", "weight", "tracking"):
                self.assertIn("--md-sys-typescale-%s-%s:" % (role, prop), out)
        self.assertIn("--md-sys-typescale-body-large-size: 1rem;", out)
        self.assertIn("--md-sys-typescale-display-large-size: 3.5625rem;", out)
        self.assertIn("--md-sys-typescale-label-large-weight: 500;", out)
        self.assertIn("--md-sys-typescale-body-large-tracking: 0.0313em;", out)
        self.assertIn("baseline M3 type scale shipped by the Material 3 libraries", out)
        code, out, err = run_cli("export", "--tokens", "shape", "--format", "css")
        self.assertEqual(code, 0, err)
        for step, val in (("none", "0px"), ("extra-small", "4px"), ("medium", "12px"),
                          ("extra-large", "28px"), ("extra-extra-large", "48px")):
            self.assertIn("--md-sys-shape-corner-%s: %s;" % (step, val), out)
        self.assertIn("--md-sys-shape-corner-full:", out)

    def test_out_option(self):
        target = os.path.join(self.tmp, "out.css")
        code, out, err = run_cli("export", self.paths["green"], "--format", "css", "--out", target)
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "")
        self.assertIn("--md-sys-color-primary", open(target).read())

    def test_exit_codes_bad_input(self):
        self.assertEqual(run_cli("scheme", "--seed", "purple")[0], 2)
        self.assertEqual(run_cli("scheme", "--seed", "#6750A4", "--variant", "vibrant")[0], 2)
        self.assertEqual(run_cli("scheme")[0], 2)
        self.assertEqual(run_cli()[0], 2)
        self.assertEqual(run_cli("check", os.path.join(self.tmp, "nope.json"))[0], 2)
        bad = os.path.join(self.tmp, "bad.json")
        with open(bad, "w") as fh:
            fh.write("{not json")
        self.assertEqual(run_cli("check", bad)[0], 2)
        self.assertEqual(run_cli("check", write_json({"foo": {}}))[0], 2)
        self.assertEqual(run_cli("check", write_json({"light": {"primary": "red"}}))[0], 2)
        self.assertEqual(run_cli("export", self.paths["red"], "--format", "xml")[0], 2)
        self.assertEqual(run_cli("export", "--format", "css")[0], 2)
        self.assertEqual(run_cli("export", "--tokens", "type", "--format", "compose")[0], 2)

    def test_help_for_each_subcommand(self):
        for sub in ("scheme", "check", "export"):
            code, out, err = run_cli(sub, "--help")
            self.assertEqual(code, 0)
            self.assertIn("usage", out.lower())


if __name__ == "__main__":
    unittest.main()
