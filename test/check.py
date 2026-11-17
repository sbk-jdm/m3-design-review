"""Run scripts/measure.js on test/seeded-violations.html (and test/no-viewport.html) in headless Chromium and check
test/EXPECTED.md.

Usage: python3 test/check.py [--chrome /path/to/chrome] [--dump]
Requires Python Playwright. Uses only local files; no network access.
"""
import json
import pathlib
import sys

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = (ROOT / "skills/m3-design-review/scripts/measure.js").read_text(encoding="utf-8")
PAGE = (ROOT / "test/seeded-violations.html").as_uri()
NO_VIEWPORT = (ROOT / "test/no-viewport.html").as_uri()
OPTS = {"expectWidth": 390, "nonTextSelectors": [".bar > i"]}


def item(d, key, selector):
    return next((i for i in d[key]["items"] if i["selector"] == selector), None)


def sels(d, key):
    return [i["selector"] for i in d[key]["items"]]


def checks(d):
    c = []
    add = lambda vid, ok, what: c.append((vid, bool(ok), what))
    add("V01", d["document"]["lang"] is None, "document.lang is null")
    add("V02", d["document"]["zoomDisabled"], "document.zoomDisabled is true")
    add("V03", any(i["selector"] == "button#v03" and i["height"] < 48 for i in d["smallTargets"]["items"]), "smallTargets has button#v03 (32 px tall)")
    add("V04", any(i["selector"] == "button#v04" and i["iconOnly"] for i in d["unnamedControls"]["items"]), "unnamedControls has button#v04 with iconOnly")
    add("V05", "img#v05" in sels(d, "imagesWithoutAlt"), "imagesWithoutAlt has img#v05")
    add("V06", any(i["selector"] == "p#v06" and i["fontSizePx"] == 10 for i in d["smallText"]["items"]), "smallText has p#v06 at 10 px")
    add("V07", any(i["selector"] == "p#v07" and 2.8 <= i["ratio"] <= 2.9 and i["required"] == 4.5 for i in d["contrastFailures"]["items"]), "contrastFailures has p#v07 ~2.85 (needs 4.5)")
    add("V08", any(i["selector"] == "p#v08" and i["large"] and i["required"] == 3 for i in d["contrastFailures"]["items"]), "contrastFailures has p#v08 as large text (needs 3)")
    add("V09", any(i["selector"] == "p#v09" and "gradient" in i["reason"] for i in d["contrastUnresolved"]["items"]), "contrastUnresolved has p#v09 (gradient)")
    add("V10", "button#v10" in sels(d, "focusNotVisible"), "focusNotVisible has button#v10")
    add("V11", d["motion"]["reducedMotionQueryFound"] is False and d["motion"]["elementsWithAnimation"] >= 1, "no reduced-motion query while an animation runs")
    add("V12", any(h["value"] == "7px" for h in d["radiusHistogram"]), "radiusHistogram contains 7px")
    add("V13", any("Comic Sans MS" in f["family"] for f in d["fontFamilies"]), "fontFamilies lists the decorative face")
    add("V14", any(i["selector"] == "p#v14" and i["ratio"] < 4.5 for i in d["contrastFailures"]["items"]), "contrastFailures has p#v14 (alpha composited)")
    add("V15", "input#v15" in sels(d, "unnamedControls") and "input#v15" in sels(d, "smallTargets"), "input#v15 unnamed and under 48 px")
    add("V16", any(i["selector"] == "p#v16" and i["ratio"] < 4.5 for i in d["contrastFailures"]["items"]), "contrastFailures has p#v16 (color-mix parsed)")
    add("P1", d["customProperties"]["count"] == 4 and d["customProperties"]["mdSysCount"] == 2, "4 :root custom properties, 2 --md-sys-*")
    t = item(d, "smallTargets", "button#v17")
    add("V17", t and t["visualHeight"] == 36 and 45.5 <= t["hitHeight"] <= 46.5 and t["hitAreaVia"] in ("pseudo", "probe"),
        "smallTargets has button#v17: visual 36 px, effective ~46 px via pseudo/probe")
    t = item(d, "truncated", "div#v18")
    add("V18", t and t["via"] == "ellipsis" and t["hasTitle"] is False and t["nameHasFullText"], "truncated has div#v18 (ellipsis, no title)")
    t = item(d, "nonTextContrast", "input#v19")
    add("V19", t and t["part"] == "fill" and 1.05 <= t["ratio"] <= 1.2 and t["kind"] == "field", "nonTextContrast has input#v19 fill ~1.1:1")
    t = item(d, "labelInName", "button#v20")
    add("V20", t and t["visibleText"] == "Send now" and t["accessibleName"] == "Submit form", "labelInName has button#v20")
    add("V21", any(i["selector"] == "button#v21" and "aria-pressed" in i["issue"] for i in d["ariaConflicts"]["items"]), "ariaConflicts has button#v21 (role=radio with aria-pressed)")
    doc = d["document"]
    add("V22", doc["h1Count"] == 1 and doc["h1CountAll"] == 2 and doc["headingCount"] == 2, "hidden h1 not counted (h1Count 1, headingCount 2)")
    t = item(d["layoutOverflow"] and d, "layoutOverflow", "div#v23")
    add("V23", t and t["scrollWidth"] >= 320 and t["clientWidth"] == 200 and d["layoutOverflow"]["horizontalScroll"] is False,
        "layoutOverflow has div#v23 (320 in 200), no page scroll")
    t = item(d, "nonTextContrast", "i#v24")
    add("V24", t and t["kind"] == "selector" and 1.0 <= t["ratio"] <= 1.1, "nonTextContrast has i#v24 (~1.05:1) via nonTextSelectors")
    add("W1", d["warnings"] == [] and d["viewport"]["mismatch"] is False and d["viewport"]["expectWidth"] == 390, "no setup warnings at 390 px")
    t = item(d, "smallTargets", "button#ok-child-hit")
    add("P2", t and t["probe"] == "offscreen" and t["hitAreaVia"] == "box", "below the fold: ok-child-hit measured from geometry only (probe offscreen)")
    flat = json.dumps({k: v for k, v in d.items() if k != "radiusHistogram"})  # inventory examples are not reports
    for ok_id in ["ok-button", "ok-disabled", "ok-large", "ok-decorative", "ok-sronly", "ok-checkbox", "ok-chip-pseudo",
                  "ok-icon-centered", "ok-fits", "ok-field", "ok-labelname", "ok-radio", "ok-seg"]:
        add("N:" + ok_id, ("#" + ok_id + '"') not in flat, ok_id + " not reported")
    add("N:ok-inline", all(i.get("inlineTextLink") for i in d["smallTargets"]["items"] if i["selector"] == "a#ok-inline"), "inline link marked inlineTextLink")
    return c


def main():
    chrome = sys.argv[sys.argv.index("--chrome") + 1] if "--chrome" in sys.argv else None
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(executable_path=chrome) if chrome else p.chromium.launch()
        except Exception:
            browser = p.chromium.launch(executable_path="/usr/bin/google-chrome")
        page = browser.new_page(viewport={"width": 390, "height": 844})
        page.goto(PAGE)
        before = page.evaluate("document.documentElement.outerHTML")
        scroll = page.evaluate("[scrollX, scrollY]")
        data = page.evaluate(SRC, OPTS)
        after = page.evaluate("document.documentElement.outerHTML")
        active = page.evaluate("document.activeElement === document.body")
        scroll_after = page.evaluate("[scrollX, scrollY]")
        again = page.evaluate("(" + SRC + ")()")  # DevTools-style invocation, no options
        legacy = page.evaluate(SRC, {"hitScan": False})
        page.evaluate("document.getElementById('v17').scrollIntoView({block: 'center'})")  # the harness scrolls, not the script
        inview = page.evaluate(SRC, OPTS)
        mctx = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
        mpage = mctx.new_page()
        mpage.goto(NO_VIEWPORT)
        nov = mpage.evaluate(SRC, {"expectWidth": 390})
        mpage.goto(PAGE)
        mob = mpage.evaluate(SRC, {"expectWidth": 390})
        browser.close()
    if "--dump" in sys.argv:
        print(json.dumps(data, indent=1))
    results = checks(data)
    results.append(("M1", before == after, "DOM unchanged by the script"))
    results.append(("M2", active, "focus restored to <body>"))
    results.append(("M3", again["contrastFailures"]["count"] == data["contrastFailures"]["count"], "second run gives the same result"))
    results.append(("M4", scroll == scroll_after, "scroll position unchanged"))
    results.append(("H1", item(legacy, "smallTargets", "button#ok-chip-pseudo") is not None and item(data, "smallTargets", "button#ok-chip-pseudo") is None,
                    "hitScan:false keeps the v0.1 box-only result (ok-chip-pseudo reported only then)"))
    t = item(inview, "smallTargets", "button#v17")
    results.append(("P3", t and t["probe"] == "ok" and 45.5 <= t["hitHeight"] <= 46.5 and t["hitAreaVia"] == "pseudo",
                    "in view: the probe confirms the 46 px pseudo band of v17"))
    results.append(("P4", item(inview, "smallTargets", "button#ok-chip-pseudo") is None and item(inview, "smallTargets", "button#ok-child-hit") is None,
                    "in view: ok-chip-pseudo and ok-child-hit (probe) not reported"))
    results.append(("W2", "viewport-meta-missing" in nov["warnings"] and "viewport-width-mismatch" in nov["warnings"] and nov["viewport"]["innerWidth"] == 980,
                    "no viewport meta in a mobile context: both warnings, 980 px layout"))
    results.append(("W3", mob["warnings"] == [] and mob["viewport"]["innerWidth"] == 390, "seeded page in the mobile context: no warnings"))
    failed = 0
    for vid, ok, what in results:
        print(("PASS " if ok else "FAIL ") + vid.ljust(20) + what)
        failed += not ok
    print("%d checks, %d failed" % (len(results), failed))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
