"""Run scripts/measure.js on test/seeded-violations.html in headless Chromium and check test/EXPECTED.md.

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
    flat = json.dumps(d)
    for ok_id in ["ok-button", "ok-disabled", "ok-large", "ok-decorative", "ok-sronly", "ok-checkbox"]:
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
        data = page.evaluate(SRC)
        after = page.evaluate("document.documentElement.outerHTML")
        active = page.evaluate("document.activeElement === document.body")
        again = page.evaluate("(" + SRC + ")()")  # DevTools-style invocation
        browser.close()
    if "--dump" in sys.argv:
        print(json.dumps(data, indent=1))
    results = checks(data)
    results.append(("M1", before == after, "DOM unchanged by the script"))
    results.append(("M2", active, "focus restored to <body>"))
    results.append(("M3", again["contrastFailures"]["count"] == data["contrastFailures"]["count"], "second run gives the same result"))
    failed = 0
    for vid, ok, what in results:
        print(("PASS " if ok else "FAIL ") + vid.ljust(16) + what)
        failed += not ok
    print("%d checks, %d failed" % (len(results), failed))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
