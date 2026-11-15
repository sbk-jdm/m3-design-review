(function m3Measure(options) {
  /*
   * m3-design-review / scripts/measure.js
   * Read-only measurement of a rendered page for a Material Design 3 review.
   * Evaluate in the page context: Playwright page.evaluate(source[, options]), a browser-automation JS tool,
   * or DevTools: paste `(<file contents>)()` into the console.
   * Dependency-free. Sends nothing anywhere. Does not change the DOM or styles; the only side effect is a transient
   * element.focus() during the focus check, after which the previously focused element is restored.
   * Returns a JSON-serializable object. Field meanings and limits: references/measurement.md.
   */
  'use strict';
  var opts = options || {};
  var CAP = opts.maxItems || 40;            // max items per list
  var MAX_EL = opts.maxElements || 6000;    // max elements scanned
  var MAX_FOCUS = opts.maxFocus || 80;      // max elements focused in the focus check
  var TARGET = opts.minTarget || 48;        // CSS px (1dp = 1 CSS px on the web)
  var MIN_TEXT = opts.minTextPx || 12;      // CSS px
  var t0 = Date.now();
  var doc = document;
  var root = doc.documentElement;

  // ---------- helpers ----------
  function list() { return { count: 0, truncated: false, items: [] }; }
  function push(l, item) { l.count++; if (l.items.length < CAP) l.items.push(item); else l.truncated = true; }
  function r1(n) { return Math.round(n * 10) / 10; }
  function r2(n) { return Math.round(n * 100) / 100; }

  function cssEsc(s) {
    return (window.CSS && CSS.escape) ? CSS.escape(s) : String(s).replace(/[^a-zA-Z0-9_-]/g, '\\$&');
  }
  function part(el) {
    var s = el.tagName.toLowerCase();
    if (el.id) return s + '#' + cssEsc(el.id);
    var cls = (typeof el.className === 'string' ? el.className : (el.getAttribute('class') || ''))
      .trim().split(/\s+/).filter(Boolean).slice(0, 2);
    if (cls.length) s += '.' + cls.map(cssEsc).join('.');
    var p = el.parentElement;
    if (p) {
      var same = 0, idx = 0;
      for (var i = 0; i < p.children.length; i++) {
        if (p.children[i].tagName === el.tagName) { same++; if (p.children[i] === el) idx = same; }
      }
      if (same > 1) s += ':nth-of-type(' + idx + ')';
    }
    return s;
  }
  function sel(el) {
    var parts = [], cur = el, depth = 0;
    while (cur && cur.nodeType === 1 && depth < 4) {
      parts.unshift(part(cur));
      if (cur.id) break;
      cur = cur.parentElement; depth++;
      if (cur === root || cur === doc.body) break;
    }
    return parts.join(' > ');
  }
  function textOf(el, n) {
    var t = (el.innerText || el.textContent || '').replace(/\s+/g, ' ').trim();
    return t.length > (n || 40) ? t.slice(0, n || 40) + '...' : t;
  }

  function visible(el, cs) {
    cs = cs || getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || cs.visibility === 'collapse') return false;
    if (typeof el.checkVisibility === 'function' &&
        !el.checkVisibility({ opacityProperty: true, visibilityProperty: true })) return false;
    var r = el.getBoundingClientRect();
    return r.width > 1 && r.height > 1;
  }
  function visuallyHidden(el, cs) {
    // common "sr-only" patterns: clipped 1px boxes
    var r = el.getBoundingClientRect();
    if (r.width <= 1 || r.height <= 1) return true;
    if (cs.clip && cs.clip !== 'auto' && /rect\(\s*0(px)?[ ,]+0(px)?[ ,]+0(px)?[ ,]+0(px)?\s*\)/.test(cs.clip)) return true;
    if (cs.clipPath && /inset\(\s*50%/.test(cs.clipPath)) return true;
    return false;
  }

  // ---------- color ----------
  var cvs = null, ctx = null;
  function canvasColor(str) {
    try {
      if (!cvs) {
        cvs = doc.createElement('canvas'); cvs.width = 1; cvs.height = 1; // detached, never inserted
        ctx = cvs.getContext('2d', { willReadFrequently: true });
      }
      ctx.clearRect(0, 0, 1, 1);
      ctx.fillStyle = '#000'; ctx.fillStyle = str;
      ctx.fillRect(0, 0, 1, 1);
      var d = ctx.getImageData(0, 0, 1, 1).data;
      return { r: d[0], g: d[1], b: d[2], a: d[3] / 255 };
    } catch (e) { return null; }
  }
  function parseColor(str) {
    if (!str) return null;
    if (str === 'transparent') return { r: 0, g: 0, b: 0, a: 0 };
    var m = str.match(/^rgba?\(\s*([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)(?:\s*[,/]\s*([\d.]+%?))?\s*\)$/);
    if (m) {
      var a = m[4] === undefined ? 1 : (m[4].slice(-1) === '%' ? parseFloat(m[4]) / 100 : parseFloat(m[4]));
      return { r: +m[1], g: +m[2], b: +m[3], a: a };
    }
    return canvasColor(str); // color(), oklch(), color-mix() and other formats
  }
  function over(fg, bg) { // composite fg over opaque bg
    var a = fg.a;
    return { r: fg.r * a + bg.r * (1 - a), g: fg.g * a + bg.g * (1 - a), b: fg.b * a + bg.b * (1 - a), a: 1 };
  }
  function lum(c) {
    function ch(v) { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }
    return 0.2126 * ch(c.r) + 0.7152 * ch(c.g) + 0.0722 * ch(c.b);
  }
  function ratio(a, b) { var x = lum(a), y = lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); }
  function hex(c) {
    function h(v) { v = Math.round(v); return (v < 16 ? '0' : '') + v.toString(16); }
    return '#' + h(c.r) + h(c.g) + h(c.b);
  }
  // Effective background by walking ancestors and compositing their background colors.
  function effectiveBg(el) {
    var layers = [], cur = el, note = null;
    while (cur && cur.nodeType === 1) {
      var cs = getComputedStyle(cur);
      if (cs.backgroundImage && cs.backgroundImage !== 'none') {
        note = /gradient/.test(cs.backgroundImage) ? 'gradient' : 'image';
        return { color: null, note: note + ' on ' + part(cur) };
      }
      if (parseFloat(cs.opacity) < 1 && cur !== el) note = 'ancestor opacity < 1 ignored';
      var c = parseColor(cs.backgroundColor);
      if (c && c.a > 0) { layers.push(c); if (c.a >= 1) break; }
      cur = cur.parentElement;
    }
    var base = { r: 255, g: 255, b: 255, a: 1 };
    var top = layers.length ? layers[layers.length - 1] : null;
    if (!top || top.a < 1) note = (note ? note + '; ' : '') + 'no opaque background found; white canvas assumed';
    else base = top;
    for (var i = layers.length - 1; i >= 0; i--) if (layers[i] !== base) base = over(layers[i], base);
    return { color: base, note: note };
  }

  function isDisabled(el) {
    for (var cur = el; cur && cur.nodeType === 1; cur = cur.parentElement) {
      if (cur.disabled === true || cur.getAttribute('aria-disabled') === 'true') return true;
      if (cur.tagName === 'FIELDSET' && cur.disabled) return true;
    }
    return false;
  }

  // ---------- accessible name (simplified) ----------
  function idsText(ids) {
    return ids.split(/\s+/).map(function (id) {
      var n = doc.getElementById(id); return n ? (n.textContent || '').trim() : '';
    }).join(' ').trim();
  }
  function accName(el) {
    var v = el.getAttribute('aria-labelledby'); if (v) { v = idsText(v); if (v) return v; }
    v = el.getAttribute('aria-label'); if (v && v.trim()) return v.trim();
    var tag = el.tagName;
    if (tag === 'INPUT' || tag === 'SELECT' || tag === 'TEXTAREA') {
      var type = (el.getAttribute('type') || '').toLowerCase();
      if (/^(submit|reset|button)$/.test(type) && el.value) return el.value;
      if (type === 'image') return el.getAttribute('alt') || '';
      if (el.labels && el.labels.length) {
        var lt = Array.prototype.map.call(el.labels, function (l) { return (l.textContent || '').trim(); }).join(' ').trim();
        if (lt) return lt;
      }
      v = el.getAttribute('title'); if (v) return v.trim();
      v = el.getAttribute('placeholder'); if (v) return v.trim();  // weak name, still counted
      return '';
    }
    if (tag === 'IMG') return (el.getAttribute('alt') || el.getAttribute('title') || '').trim();
    var txt = '';
    var walker = doc.createTreeWalker(el, NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT, null);
    var n = walker.currentNode;
    while (n) {
      if (n.nodeType === 3) txt += n.nodeValue;
      else if (n !== el && n.nodeType === 1) {
        if (n.getAttribute('aria-hidden') === 'true') { n = nextSkip(walker, n); continue; }
        if (n.tagName === 'IMG' && n.getAttribute('alt')) txt += ' ' + n.getAttribute('alt');
        if (n.tagName === 'svg' || n.tagName === 'SVG') {
          var tl = n.querySelector('title'); if (tl) txt += ' ' + tl.textContent;
          var al = n.getAttribute('aria-label'); if (al) txt += ' ' + al;
          n = nextSkip(walker, n); continue;
        }
      }
      n = walker.nextNode();
    }
    txt = txt.replace(/\s+/g, ' ').trim();
    if (txt) return txt;
    v = el.getAttribute('title'); return v ? v.trim() : '';
  }
  function nextSkip(walker, n) { // advance past n's subtree
    walker.currentNode = n;
    var s = walker.nextSibling();
    while (!s) { var p = walker.parentNode(); if (!p) return null; s = walker.nextSibling(); }
    return s;
  }
  function srcHint(src) {
    if (/^data:/i.test(src)) return src.slice(0, src.indexOf(',') > 0 ? Math.min(src.indexOf(','), 30) : 30) + ',...';
    return src.split(/[?#]/)[0].split('/').pop().slice(-60);
  }
  function looksIconOnly(el) {
    var t = (el.textContent || '').replace(/\s+/g, '');
    var hasGlyph = !!el.querySelector('svg, img, i, [class*="icon" i], [class*="material-symbols" i]');
    return hasGlyph && t.length <= 30 && !/\s/.test((el.textContent || '').trim());
  }

  // ---------- collect elements ----------
  var INTERACTIVE = 'a[href], button, input:not([type="hidden"]), select, textarea, summary, ' +
    '[role="button"], [role="link"], [role="checkbox"], [role="radio"], [role="switch"], [role="tab"], ' +
    '[role="menuitem"], [role="option"], [role="slider"], [role="spinbutton"], [role="combobox"], ' +
    '[tabindex]:not([tabindex="-1"]), [onclick], [contenteditable="true"]';
  var all = doc.body ? doc.body.getElementsByTagName('*') : [];
  var scanned = Math.min(all.length, MAX_EL);

  var out = {
    tool: 'm3-design-review/measure.js', version: '1.0.0',
    url: location.origin === 'null' ? location.protocol : location.origin + location.pathname,
    viewport: {
      innerWidth: window.innerWidth, innerHeight: window.innerHeight,
      clientWidth: root.clientWidth, devicePixelRatio: window.devicePixelRatio,
      prefersDark: window.matchMedia && matchMedia('(prefers-color-scheme: dark)').matches,
      prefersReducedMotion: window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches,
      rootFontSizePx: parseFloat(getComputedStyle(root).fontSize)
    },
    document: {},
    smallTargets: list(), smallText: list(), contrastFailures: list(), contrastUnresolved: list(),
    unnamedControls: list(), imagesWithoutAlt: list(), focusNotVisible: list(), focusWeak: list(),
    customProperties: { count: 0, truncated: false, items: [] },
    fontFamilies: [], radiusHistogram: [], motion: {}, stats: {}, notes: []
  };

  // document-level
  var vm = doc.querySelector('meta[name="viewport"]');
  var vmc = vm ? (vm.getAttribute('content') || '') : null;
  out.document = {
    lang: root.getAttribute('lang') || null,
    dir: root.getAttribute('dir') || getComputedStyle(root).direction,
    title: !!(doc.title && doc.title.trim()),
    viewportMeta: vmc,
    viewportMetaMissing: vm === null,
    zoomDisabled: vmc !== null && (/user-scalable\s*=\s*(no|0)/i.test(vmc) ||
      /maximum-scale\s*=\s*(0?\.\d+|1(\.0+)?)(?![\d.])/i.test(vmc)),
    colorSchemeMeta: (doc.querySelector('meta[name="color-scheme"]') || { getAttribute: function () { return null; } }).getAttribute('content'),
    h1Count: doc.querySelectorAll('h1').length,
    mainCount: doc.querySelectorAll('main, [role="main"]').length
  };

  var fontCount = {}, radiusCount = {}, animated = 0, transitioned = 0, textChecked = 0, exemptDisabled = 0;
  var interactive = [];
  var interactiveSet = new Set(doc.body ? doc.body.querySelectorAll(INTERACTIVE) : []);

  for (var i = 0; i < scanned; i++) {
    var el = all[i];
    if (el.tagName === 'SCRIPT' || el.tagName === 'STYLE' || el.tagName === 'TEMPLATE' || el.tagName === 'NOSCRIPT') continue;
    var cs = getComputedStyle(el);
    if (!visible(el, cs)) continue;
    var rect = el.getBoundingClientRect();
    var hidden = visuallyHidden(el, cs);

    // motion inventory
    if (cs.animationName && cs.animationName !== 'none') animated++;
    if (cs.transitionDuration && cs.transitionDuration.split(',').some(function (d) { return parseFloat(d) > 0; })) transitioned++;

    // radius histogram
    var rad = [cs.borderTopLeftRadius, cs.borderTopRightRadius, cs.borderBottomRightRadius, cs.borderBottomLeftRadius];
    if (rad.some(function (x) { return parseFloat(x) > 0; })) {
      var px = rad.map(function (x) { return x.indexOf('%') >= 0 ? x : r1(parseFloat(x)) + 'px'; });
      var key = px.every(function (x) { return x === px[0]; }) ? px[0] : px.join(' ');
      var minSide = Math.min(rect.width, rect.height);
      if (rad.every(function (x) { return x.indexOf('%') < 0 && parseFloat(x) >= minSide / 2 - 0.5; })) key += ' (pill/full)';
      var rc = radiusCount[key] || (radiusCount[key] = { value: key, count: 0, examples: [] });
      rc.count++; if (rc.examples.length < 3) rc.examples.push(sel(el));
    }

    // interactive targets
    if (interactiveSet.has(el)) {
      interactive.push(el);
      var w = rect.width, h = rect.height, via = null;
      // a wrapping or associated label enlarges the hit area of native inputs
      if (el.labels && el.labels.length) {
        for (var li = 0; li < el.labels.length; li++) {
          var lr = el.labels[li].getBoundingClientRect();
          if (lr.width * lr.height > w * h) { w = lr.width; h = lr.height; via = 'label'; }
        }
      }
      if (!hidden && (w < TARGET || h < TARGET)) {
        var inline = el.tagName === 'A' && cs.display === 'inline' && el.parentElement &&
          (el.parentElement.textContent || '').trim().length > (el.textContent || '').trim().length + 10;
        push(out.smallTargets, {
          selector: sel(el), text: textOf(el, 30), width: r1(w), height: r1(h),
          hitAreaVia: via, inlineTextLink: inline || undefined, disabled: isDisabled(el) || undefined
        });
      }
    }

    // text checks: elements with their own non-empty text nodes
    var ownText = '';
    for (var c = el.firstChild; c; c = c.nextSibling) if (c.nodeType === 3) ownText += c.nodeValue;
    ownText = ownText.replace(/\s+/g, ' ').trim();
    if (ownText && !hidden) {
      textChecked++;
      var fam = cs.fontFamily;
      fontCount[fam] = (fontCount[fam] || 0) + 1;
      var fs = parseFloat(cs.fontSize), fw = parseInt(cs.fontWeight, 10) || 400;
      if (fs < MIN_TEXT) push(out.smallText, { selector: sel(el), text: ownText.slice(0, 30), fontSizePx: r2(fs) });

      var fg = parseColor(cs.color);
      if (isDisabled(el)) { exemptDisabled++; }
      else if (fg) {
        var bg = effectiveBg(el);
        var large = fs >= 24 || (fs >= 18.66 && fw >= 700);
        var need = large ? 3 : 4.5;
        if (!bg.color) {
          push(out.contrastUnresolved, { selector: sel(el), text: ownText.slice(0, 30), color: hex(fg), reason: bg.note });
        } else {
          var fgO = fg.a < 1 ? over(fg, bg.color) : fg;
          if (parseFloat(cs.opacity) < 1) fgO = over({ r: fgO.r, g: fgO.g, b: fgO.b, a: parseFloat(cs.opacity) }, bg.color);
          var cr = ratio(fgO, bg.color);
          if (cr < need) {
            push(out.contrastFailures, {
              selector: sel(el), text: ownText.slice(0, 30), ratio: r2(cr), required: need, large: large,
              fontSizePx: r2(fs), fontWeight: fw, color: hex(fgO), background: hex(bg.color),
              note: bg.note || undefined
            });
          }
        }
      }
    }

    // images without alt
    if (!hidden) {
      if (el.tagName === 'IMG' && !el.hasAttribute('alt') && el.getAttribute('aria-hidden') !== 'true' &&
          el.getAttribute('role') !== 'presentation' && el.getAttribute('role') !== 'none' &&
          !el.getAttribute('aria-label') && !el.getAttribute('aria-labelledby')) {
        push(out.imagesWithoutAlt, { selector: sel(el), src: srcHint(el.getAttribute('src') || ''), width: r1(rect.width), height: r1(rect.height) });
      } else if (el.getAttribute('role') === 'img' && !accName(el)) {
        push(out.imagesWithoutAlt, { selector: sel(el), role: 'img', width: r1(rect.width), height: r1(rect.height) });
      }
    }
  }
  if (all.length > MAX_EL) out.notes.push('Scanned the first ' + MAX_EL + ' of ' + all.length + ' elements.');

  // unnamed controls
  interactive.forEach(function (el) {
    if (el.getAttribute('aria-hidden') === 'true') return;
    if (!accName(el)) {
      push(out.unnamedControls, { selector: sel(el), tag: el.tagName.toLowerCase(), role: el.getAttribute('role') || undefined, iconOnly: looksIconOnly(el) });
    }
  });

  // ---------- focus visibility ----------
  function focusSnap(el) {
    var s = getComputedStyle(el);
    return {
      outline: s.outlineStyle + '|' + s.outlineWidth + '|' + s.outlineColor + '|' + s.outlineOffset,
      outlineOn: s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) > 0 && (parseColor(s.outlineColor) || { a: 1 }).a > 0,
      shadow: s.boxShadow, border: s.borderTopColor + s.borderBottomColor + s.borderTopWidth,
      bg: s.backgroundColor, color: s.color, deco: s.textDecorationLine,
      transition: s.transitionDuration.split(',').some(function (d) { return parseFloat(d) > 0; })
    };
  }
  var prevActive = doc.activeElement;
  var focusables = interactive.filter(function (el) {
    return !isDisabled(el) && !visuallyHidden(el, getComputedStyle(el)) && el.tabIndex >= 0 && typeof el.focus === 'function';
  }).slice(0, MAX_FOCUS);
  var focusChecked = 0, focusVisibleMatched = 0;
  focusables.forEach(function (el) {
    try {
      var before = focusSnap(el);
      var pBefore = el.parentElement ? focusSnap(el.parentElement) : null;
      el.focus({ preventScroll: true, focusVisible: true });
      if (doc.activeElement !== el) return;
      focusChecked++;
      var fv = false; try { fv = el.matches(':focus-visible'); } catch (e) {}
      if (fv) focusVisibleMatched++;
      var after = focusSnap(el);
      var pAfter = el.parentElement ? focusSnap(el.parentElement) : null;
      var ring = (after.outlineOn && after.outline !== before.outline) || (after.outlineOn && before.outlineOn) ||
        (after.shadow !== before.shadow && after.shadow !== 'none') ||
        (pAfter && ((pAfter.outlineOn && pAfter.outline !== pBefore.outline) || (pAfter.shadow !== pBefore.shadow && pAfter.shadow !== 'none')));
      var other = after.border !== before.border || after.bg !== before.bg || after.color !== before.color || after.deco !== before.deco;
      var item = { selector: sel(el), text: textOf(el, 30), focusVisibleMatched: fv, hasTransition: after.transition || undefined };
      if (!ring && !other) push(out.focusNotVisible, item);
      else if (!ring) { item.changes = ['border', 'bg', 'color', 'deco'].filter(function (k) { return after[k] !== before[k]; }); push(out.focusWeak, item); }
    } catch (e) { /* ignore element */ }
  });
  try {
    if (prevActive && prevActive !== doc.body && typeof prevActive.focus === 'function') prevActive.focus({ preventScroll: true });
    else if (doc.activeElement && doc.activeElement.blur) doc.activeElement.blur();
  } catch (e) {}
  if (interactive.length > MAX_FOCUS) out.notes.push('Focus check limited to ' + MAX_FOCUS + ' of ' + interactive.length + ' interactive elements.');
  if (focusChecked && !focusVisibleMatched) out.notes.push('No element matched :focus-visible after focus(); :focus-visible-only styles may be missed (see measurement.md).');

  // ---------- stylesheets: custom properties and reduced motion ----------
  var rmFound = false, rmRules = 0, sheetsTotal = 0, sheetsBlocked = 0, propNames = new Set();
  var rootCS = getComputedStyle(root);
  function walkRules(rules) {
    for (var k = 0; k < rules.length; k++) {
      var rule = rules[k];
      if (rule.media && rule.conditionText === undefined && rule.media.mediaText && /prefers-reduced-motion/.test(rule.media.mediaText)) { rmFound = true; rmRules++; }
      if (rule.conditionText && /prefers-reduced-motion/.test(rule.conditionText)) { rmFound = true; rmRules++; }
      if (rule.selectorText && /(^|,)\s*(:root|html)\s*(,|$)/.test(rule.selectorText) && rule.style) {
        for (var p = 0; p < rule.style.length; p++) if (rule.style[p].indexOf('--') === 0) propNames.add(rule.style[p]);
      }
      if (rule.cssRules) walkRules(rule.cssRules);
      if (rule.styleSheet) { try { sheetsTotal++; walkRules(rule.styleSheet.cssRules); } catch (e) { sheetsBlocked++; } }
    }
  }
  for (var si = 0; si < doc.styleSheets.length; si++) {
    var sh = doc.styleSheets[si]; sheetsTotal++;
    if (sh.media && sh.media.mediaText && /prefers-reduced-motion/.test(sh.media.mediaText)) { rmFound = true; rmRules++; }
    try { walkRules(sh.cssRules); } catch (e) { sheetsBlocked++; }
  }
  if (doc.adoptedStyleSheets) {
    for (var ai = 0; ai < doc.adoptedStyleSheets.length; ai++) { sheetsTotal++; try { walkRules(doc.adoptedStyleSheets[ai].cssRules); } catch (e) { sheetsBlocked++; } }
  }
  for (var ip = 0; ip < root.style.length; ip++) if (root.style[ip].indexOf('--') === 0) propNames.add(root.style[ip]);
  propNames.forEach(function (name) {
    out.customProperties.count++;
    if (out.customProperties.items.length < (opts.maxProperties || 200)) {
      out.customProperties.items.push({ name: name, value: rootCS.getPropertyValue(name).trim().slice(0, 120) });
    } else out.customProperties.truncated = true;
  });
  var mdSys = 0; propNames.forEach(function (n) { if (/^--md-sys-/.test(n)) mdSys++; });
  out.customProperties.mdSysCount = mdSys;

  out.motion = {
    reducedMotionQueryFound: rmFound, reducedMotionRules: rmRules,
    stylesheets: sheetsTotal, stylesheetsUnreadable: sheetsBlocked,
    elementsWithAnimation: animated, elementsWithTransition: transitioned
  };
  if (sheetsBlocked) out.notes.push(sheetsBlocked + ' stylesheet(s) unreadable (cross-origin): custom properties and reduced-motion queries in them were not seen.');

  out.fontFamilies = Object.keys(fontCount).map(function (k) { return { family: k, textElements: fontCount[k] }; })
    .sort(function (a, b) { return b.textElements - a.textElements; }).slice(0, 15);
  out.radiusHistogram = Object.keys(radiusCount).map(function (k) { return radiusCount[k]; })
    .sort(function (a, b) { return b.count - a.count; }).slice(0, 30);

  out.stats = {
    elementsScanned: scanned, interactive: interactive.length, textElementsChecked: textChecked,
    contrastExemptDisabled: exemptDisabled, focusChecked: focusChecked, focusVisibleMatched: focusVisibleMatched,
    ms: Date.now() - t0
  };
  out.thresholds = { minTargetPx: TARGET, minTextPx: MIN_TEXT, contrastSmall: 4.5, contrastLarge: 3, largeTextPx: 24, largeBoldTextPx: 18.66 };
  return JSON.parse(JSON.stringify(out));
})
