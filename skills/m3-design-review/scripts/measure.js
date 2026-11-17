(function m3Measure(options) {
  /*
   * m3-design-review / scripts/measure.js
   * Read-only measurement of a rendered page for a Material Design 3 review.
   * Evaluate in the page context: Playwright page.evaluate(source[, options]), a browser-automation JS tool,
   * or DevTools: paste `(<file contents>)()` into the console.
   * Dependency-free. Sends nothing anywhere. Does not change the DOM or styles and does not scroll; the only side
   * effect is a transient element.focus() during the focus check, after which the previously focused element is restored.
   * Returns a JSON-serializable object. Field meanings and limits: references/measurement.md.
   */
  'use strict';
  var opts = options || {};
  var CAP = opts.maxItems || 40;            // max items per list
  var MAX_EL = opts.maxElements || 6000;    // max elements scanned
  var MAX_FOCUS = opts.maxFocus || 80;      // max elements focused in the focus check
  var TARGET = opts.minTarget || 48;        // CSS px (1dp = 1 CSS px on the web)
  var MIN_TEXT = opts.minTextPx || 12;      // CSS px
  var HIT_SCAN = opts.hitScan !== false;    // effective hit areas (::before/::after geometry and a hit-test probe)
  var MAX_PROBE = opts.maxProbe === undefined ? 300 : opts.maxProbe; // max targets probed with elementFromPoint
  var EXPECT_W = typeof opts.expectWidth === 'number' ? opts.expectWidth : null;
  var NON_TEXT_SEL = Array.isArray(opts.nonTextSelectors) ? opts.nonTextSelectors : [];
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
  function norm(s) { return String(s || '').toLowerCase().replace(/[^\p{L}\p{N}]+/gu, ' ').trim(); }
  function pxv(v) { var n = parseFloat(v); return isFinite(n) ? n : NaN; }
  // exposed to assistive tech and rendered (sr-only boxes count; display:none, visibility:hidden, aria-hidden do not)
  function exposed(el) {
    var cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || cs.visibility === 'collapse') return false;
    if (typeof el.checkVisibility === 'function' && !el.checkVisibility({ visibilityProperty: true })) return false;
    if (el.closest('[aria-hidden="true"]')) return false;
    return el.getClientRects().length > 0;
  }
  // visible text of a control: rendered text nodes, skipping icon-font glyphs and visually hidden text
  var ICON_RE = /(^|[\s_-])(icon|icons|material-symbols[\w-]*|material-icons[\w-]*|symbol)($|[\s_-])/i;
  function visibleTextOf(el) {
    var out = '', w = doc.createTreeWalker(el, NodeFilter.SHOW_TEXT, null), n, memo = new Map();
    function skip(p) {
      if (memo.has(p)) return memo.get(p);
      var r = false;
      for (var c = p; c && c !== el.parentElement; c = c.parentElement) {
        var cl = c.getAttribute('class') || '';
        var s = getComputedStyle(c);
        if (ICON_RE.test(cl) || /material (icons|symbols)/i.test(s.fontFamily) ||
            s.display === 'none' || s.visibility === 'hidden' || (c !== el && visuallyHidden(c, s))) { r = true; break; }
      }
      memo.set(p, r); return r;
    }
    while ((n = w.nextNode())) if (n.nodeValue.trim() && n.parentElement && !skip(n.parentElement)) out += ' ' + n.nodeValue;
    return out.replace(/\s+/g, ' ').trim();
  }

  // ---------- effective hit area ----------
  function rectOf(r) { return { l: r.left, t: r.top, r: r.right, b: r.bottom }; }
  function paddingBox(e, s) {
    var r = e.getBoundingClientRect();
    return {
      l: r.left + (pxv(s.borderLeftWidth) || 0) - e.scrollLeft, t: r.top + (pxv(s.borderTopWidth) || 0) - e.scrollTop,
      r: r.right - (pxv(s.borderRightWidth) || 0) - e.scrollLeft, b: r.bottom - (pxv(s.borderBottomWidth) || 0) - e.scrollTop,
      w: e.clientWidth, h: e.clientHeight
    };
  }
  function makesCB(s) { // establishes a containing block for absolutely positioned descendants
    return s.position !== 'static' || (s.transform && s.transform !== 'none') || (s.filter && s.filter !== 'none') ||
      (s.perspective && s.perspective !== 'none') || /\b(layout|paint|strict|content)\b/.test(s.contain || '') ||
      /\b(transform|filter|perspective)\b/.test(s.willChange || '') ||
      (s.containerType && s.containerType !== 'normal');
  }
  function containingBlock(el, s) {
    for (var cur = el, depth = 0; cur && cur.nodeType === 1 && depth < 60; depth++) {
      if (makesCB(s)) {
        var pb = paddingBox(cur, s);
        // clientWidth excludes scrollbars; inline boxes have clientWidth 0, keep the rect then
        if (pb.w > 0) pb.r = pb.l + pb.w;
        if (pb.h > 0) pb.b = pb.t + pb.h;
        return { el: cur, box: pb };
      }
      cur = cur.parentElement; if (cur) s = getComputedStyle(cur);
    }
    return { el: null, box: { l: -window.scrollX, t: -window.scrollY, r: -window.scrollX + root.clientWidth, b: -window.scrollY + root.clientHeight } };
  }
  function parseMatrix(t) {
    if (!t || t === 'none') return null;
    var m = t.match(/^matrix(3d)?\(([^)]+)\)$/); if (!m) return null;
    var v = m[2].split(',').map(parseFloat);
    return m[1] ? [v[0], v[1], v[4], v[5], v[12], v[13]] : v;
  }
  function pseudoRect(el, which, elCS) {
    var ps; try { ps = getComputedStyle(el, which); } catch (e) { return null; }
    if (!ps || !ps.content || ps.content === 'none' || ps.content === 'normal') return null;
    if (ps.display === 'none' || ps.visibility !== 'visible' || ps.pointerEvents === 'none') return null;
    if (ps.position !== 'absolute') return null; // in-flow pseudo-elements sit inside the box; fixed ones are skipped
    var cb = containingBlock(el, elCS);
    var W = pxv(ps.width), H = pxv(ps.height); if (!isFinite(W) || !isFinite(H)) return null;
    if (ps.boxSizing !== 'border-box') {
      W += (pxv(ps.paddingLeft) || 0) + (pxv(ps.paddingRight) || 0) + (pxv(ps.borderLeftWidth) || 0) + (pxv(ps.borderRightWidth) || 0);
      H += (pxv(ps.paddingTop) || 0) + (pxv(ps.paddingBottom) || 0) + (pxv(ps.borderTopWidth) || 0) + (pxv(ps.borderBottomWidth) || 0);
    }
    var L = pxv(ps.left), R = pxv(ps.right), T = pxv(ps.top), B = pxv(ps.bottom);
    var x1 = isFinite(L) ? cb.box.l + L + (pxv(ps.marginLeft) || 0) : (isFinite(R) ? cb.box.r - R - (pxv(ps.marginRight) || 0) - W : NaN);
    var y1 = isFinite(T) ? cb.box.t + T + (pxv(ps.marginTop) || 0) : (isFinite(B) ? cb.box.b - B - (pxv(ps.marginBottom) || 0) - H : NaN);
    if (!isFinite(x1) || !isFinite(y1)) return null;
    var r = { l: x1, t: y1, r: x1 + W, b: y1 + H };
    var m = parseMatrix(ps.transform);
    if (m) {
      var o = (ps.transformOrigin || '').split(' ').map(parseFloat), ox = r.l + (o[0] || 0), oy = r.t + (o[1] || 0);
      var xs = [], ys = [];
      [[r.l, r.t], [r.r, r.t], [r.l, r.b], [r.r, r.b]].forEach(function (p) {
        var dx = p[0] - ox, dy = p[1] - oy;
        xs.push(ox + m[0] * dx + m[2] * dy + m[4]); ys.push(oy + m[1] * dx + m[3] * dy + m[5]);
      });
      r = { l: Math.min.apply(null, xs), t: Math.min.apply(null, ys), r: Math.max.apply(null, xs), b: Math.max.apply(null, ys) };
    }
    // clipped by overflow on the containing block and its ancestors (body and html propagate to the viewport)
    for (var cur = cb.el, d = 0; cur && cur !== doc.body && cur !== root && d < 40; cur = cur.parentElement, d++) {
      var s = getComputedStyle(cur);
      if (s.overflowX === 'visible' && s.overflowY === 'visible') continue;
      var pb = paddingBox(cur, s); pb.l += cur.scrollLeft; pb.r += cur.scrollLeft; pb.t += cur.scrollTop; pb.b += cur.scrollTop;
      if (s.overflowX !== 'visible') { r.l = Math.max(r.l, pb.l); r.r = Math.min(r.r, pb.r); }
      if (s.overflowY !== 'visible') { r.t = Math.max(r.t, pb.t); r.b = Math.min(r.b, pb.b); }
    }
    if (r.r - r.l <= 0 || r.b - r.t <= 0) return null;
    return r;
  }
  function owns(el, n) {
    if (!n) return false;
    if (n === el || el.contains(n)) return true;
    if (el.labels) for (var i = 0; i < el.labels.length; i++) if (el.labels[i] === n || el.labels[i].contains(n)) return true;
    return false;
  }
  // Walks outward from each edge of the box along the center lines while elementFromPoint still hits the element.
  function probeHit(el, b) {
    var vw = root.clientWidth, vh = window.innerHeight;
    var cx = (b.l + b.r) / 2, cy = (b.t + b.b) / 2;
    if (cx < 0 || cy < 0 || cx >= vw || cy >= vh) return { status: 'offscreen' };
    if (!owns(el, doc.elementFromPoint(cx, cy))) return { status: 'covered' };
    var limited = false;
    function ext(dx, dy, x0, y0) {
      for (var d = 1; d <= TARGET; d++) {
        var x = x0 + dx * (d - 0.5), y = y0 + dy * (d - 0.5);
        if (x < 0 || y < 0 || x >= vw || y >= vh) { limited = true; return d - 1; }
        if (!owns(el, doc.elementFromPoint(x, y))) return d - 1;
      }
      return TARGET;
    }
    var w = (b.r - b.l) + ext(-1, 0, b.l, cy) + ext(1, 0, b.r, cy);
    var h = (b.b - b.t) + ext(0, -1, cx, b.t) + ext(0, 1, cx, b.b);
    return { status: limited ? 'limited' : 'ok', w: w, h: h };
  }

  // ---------- collect elements ----------
  var INTERACTIVE = 'a[href], button, input:not([type="hidden"]), select, textarea, summary, ' +
    '[role="button"], [role="link"], [role="checkbox"], [role="radio"], [role="switch"], [role="tab"], ' +
    '[role="menuitem"], [role="option"], [role="slider"], [role="spinbutton"], [role="combobox"], ' +
    '[tabindex]:not([tabindex="-1"]), [onclick], [contenteditable="true"]';
  var all = doc.body ? doc.body.getElementsByTagName('*') : [];
  var scanned = Math.min(all.length, MAX_EL);

  var out = {
    tool: 'm3-design-review/measure.js', version: '1.1.0',
    url: location.origin === 'null' ? location.protocol : location.origin + location.pathname,
    viewport: {
      innerWidth: window.innerWidth, innerHeight: window.innerHeight,
      clientWidth: root.clientWidth, devicePixelRatio: window.devicePixelRatio,
      prefersDark: window.matchMedia && matchMedia('(prefers-color-scheme: dark)').matches,
      prefersReducedMotion: window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches,
      rootFontSizePx: parseFloat(getComputedStyle(root).fontSize),
      metaViewport: null, expectWidth: EXPECT_W, mismatch: false
    },
    warnings: [],
    document: {},
    smallTargets: list(), smallText: list(), contrastFailures: list(), contrastUnresolved: list(),
    unnamedControls: list(), imagesWithoutAlt: list(), focusNotVisible: list(), focusWeak: list(),
    truncated: list(), nonTextContrast: list(), layoutOverflow: null, labelInName: list(), ariaConflicts: list(),
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
    h1Count: 0, h1CountAll: doc.querySelectorAll('h1').length, headingCount: 0, headingSkips: 0, headingOutline: [],
    mainCount: doc.querySelectorAll('main, [role="main"]').length
  };
  out.viewport.metaViewport = vmc;
  if (vm === null) out.warnings.push('viewport-meta-missing');
  if (EXPECT_W !== null && Math.abs(window.innerWidth - EXPECT_W) > 1) {
    out.viewport.mismatch = true; out.warnings.push('viewport-width-mismatch');
  }
  // headings exposed to assistive tech (hidden views do not count)
  var prevLevel = 0, hs = doc.querySelectorAll('h1, h2, h3, h4, h5, h6, [role="heading"]');
  for (var hi = 0; hi < hs.length && hi < MAX_EL; hi++) {
    var hEl = hs[hi];
    if (!exposed(hEl)) continue;
    var lvl = /^H[1-6]$/.test(hEl.tagName) && !hEl.getAttribute('role') ? +hEl.tagName[1] : (parseInt(hEl.getAttribute('aria-level'), 10) || 2);
    out.document.headingCount++;
    if (lvl === 1) out.document.h1Count++;
    if (prevLevel && lvl > prevLevel + 1) out.document.headingSkips++;
    prevLevel = lvl;
    if (out.document.headingOutline.length < CAP) out.document.headingOutline.push({ level: lvl, text: textOf(hEl, 40) });
  }

  var fontCount = {}, radiusCount = {}, animated = 0, transitioned = 0, textChecked = 0, exemptDisabled = 0;
  var interactive = [], targetCands = [];
  var overflowItems = { count: 0, truncated: false, items: [] };
  function ownTextOf(e) { var t = ''; for (var c = e.firstChild; c; c = c.nextSibling) if (c.nodeType === 3) t += c.nodeValue; return t.trim(); }
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
        targetCands.push({ el: el, cs: cs, rect: rect, w: w, h: h, via: via });
      }
    }

    // truncation and clipped overflow (only boxes that clip or clamp)
    if (!hidden && (cs.overflowX !== 'visible' || cs.overflowY !== 'visible')) {
      var clamp = cs.webkitLineClamp || cs.getPropertyValue('-webkit-line-clamp') || cs.getPropertyValue('line-clamp');
      var txtAll = (el.textContent || '').replace(/\s+/g, ' ').trim();
      var overX = el.clientWidth > 0 && el.scrollWidth > el.clientWidth + 1;
      var overY = el.clientHeight > 0 && el.scrollHeight > el.clientHeight + 1;
      var clipX = cs.overflowX === 'hidden' || cs.overflowX === 'clip';
      var clipY = cs.overflowY === 'hidden' || cs.overflowY === 'clip';
      var tvia = null;
      if (clamp && clamp !== 'none' && overY) tvia = 'line-clamp';
      else if (cs.textOverflow === 'ellipsis' && overX) tvia = 'ellipsis';
      else if (clipX && overX && ownTextOf(el) && /nowrap|pre/.test(cs.whiteSpace)) tvia = 'clip';
      if (tvia && txtAll) {
        var ctl = el.closest(INTERACTIVE) || el;
        var hidAnc = !!el.closest('[aria-hidden="true"]');
        push(out.truncated, {
          selector: sel(el), text: txtAll.slice(0, 60), via: tvia,
          hasTitle: !!(el.closest('[title]') && el.closest('[title]').getAttribute('title').trim()),
          nameHasFullText: !hidAnc && norm(accName(ctl)).indexOf(norm(txtAll)) >= 0
        });
      }
      if (txtAll && tvia !== 'ellipsis' && tvia !== 'line-clamp' && ((clipX && overX) || (clipY && overY))) {
        overflowItems.count++;
        if (overflowItems.items.length < CAP) {
          overflowItems.items.push({
            selector: sel(el), axis: clipX && overX ? (clipY && overY ? 'both' : 'x') : 'y',
            scrollWidth: el.scrollWidth, clientWidth: el.clientWidth, scrollHeight: el.scrollHeight, clientHeight: el.clientHeight
          });
        } else overflowItems.truncated = true;
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

  // ---------- small targets: effective hit area ----------
  var probed = 0, probeCovered = 0, probeOffscreen = 0;
  targetCands.forEach(function (c) {
    var el = c.el, b = rectOf(c.rect), hit = b, via = c.via || 'box';
    if (c.via === 'label') {
      el.labels && Array.prototype.forEach.call(el.labels, function (lb) {
        var lr = lb.getBoundingClientRect();
        if (lr.width * lr.height >= c.w * c.h - 0.5) hit = rectOf(lr);
      });
    }
    var hw = c.w, hh = c.h, covered, probeStatus;
    if (HIT_SCAN) {
      var u = { l: hit.l, t: hit.t, r: hit.r, b: hit.b }, grew = false;
      ['::before', '::after'].forEach(function (w) {
        var pr = pseudoRect(el, w, c.cs); if (!pr) return;
        var n = { l: Math.min(u.l, pr.l), t: Math.min(u.t, pr.t), r: Math.max(u.r, pr.r), b: Math.max(u.b, pr.b) };
        if (n.r - n.l > u.r - u.l + 0.5 || n.b - n.t > u.b - u.t + 0.5) grew = true;
        u = n;
      });
      hw = u.r - u.l; hh = u.b - u.t;
      if (grew) via = 'pseudo';
      if (probed < MAX_PROBE) {
        probed++;
        var p = probeHit(el, b);
        probeStatus = p.status;
        if (p.status === 'covered') { probeCovered++; covered = true; }
        else if (p.status === 'offscreen') probeOffscreen++;
        else if (p.status === 'ok' && (Math.abs(p.w - hw) > 1 || Math.abs(p.h - hh) > 1)) {
          if (Math.abs(p.w - hw) > 1) hw = p.w;
          if (Math.abs(p.h - hh) > 1) hh = p.h;
          via = 'probe';
        }
      }
    }
    if (hw < TARGET || hh < TARGET) {
      var inline = el.tagName === 'A' && c.cs.display === 'inline' && el.parentElement &&
        (el.parentElement.textContent || '').trim().length > (el.textContent || '').trim().length + 10;
      push(out.smallTargets, {
        selector: sel(el), text: textOf(el, 30), width: r1(hw), height: r1(hh),
        visualWidth: r1(c.rect.width), visualHeight: r1(c.rect.height), hitWidth: r1(hw), hitHeight: r1(hh),
        hitAreaVia: via, probe: probeStatus, covered: covered || undefined,
        inlineTextLink: inline || undefined, disabled: isDisabled(el) || undefined
      });
    }
  });
  if (HIT_SCAN && probeOffscreen) out.notes.push(probeOffscreen + ' small-target candidate(s) were outside the viewport: hit area from geometry only (no probe).');
  if (HIT_SCAN && targetCands.length > MAX_PROBE) out.notes.push('Hit-test probe limited to ' + MAX_PROBE + ' of ' + targetCands.length + ' candidates.');

  // ---------- non-text contrast (fields, outlined controls, nonTextSelectors) ----------
  var FIELD_TYPES = /^(|text|search|email|url|tel|password|number|date|datetime-local|month|week|time)$/;
  function isField(el) {
    var t = el.tagName, r = (el.getAttribute('role') || '').toLowerCase();
    if (t === 'TEXTAREA' || t === 'SELECT') return true;
    if (t === 'INPUT') return FIELD_TYPES.test((el.getAttribute('type') || '').toLowerCase());
    return /^(textbox|combobox|searchbox|spinbutton)$/.test(r) || el.getAttribute('contenteditable') === 'true';
  }
  var ntChecked = 0, ntUnresolved = 0;
  function sideBorders(cs, under) { // composited color of each drawn border side
    var res = [];
    ['Top', 'Right', 'Bottom', 'Left'].forEach(function (S) {
      var w = pxv(cs['border' + S + 'Width']), st = cs['border' + S + 'Style'], c = parseColor(cs['border' + S + 'Color']);
      if (!(w >= 0.5) || st === 'none' || st === 'hidden' || !c || c.a === 0) return;
      res.push(c.a < 1 ? over(c, under) : c);
    });
    return res;
  }
  var prevActiveEarly = doc.activeElement;
  interactive.forEach(function (el) {
    if (el === prevActiveEarly || isDisabled(el)) return;
    var cs = getComputedStyle(el);
    if (visuallyHidden(el, cs)) return;
    var t = el.tagName, type = (el.getAttribute('type') || '').toLowerCase();
    if (t === 'INPUT' && /^(checkbox|radio|range|color|file)$/.test(type) && cs.appearance !== 'none') return;
    var field = isField(el);
    var behind = effectiveBg(el.parentElement || el);
    if (!behind.color) { ntUnresolved++; return; }
    var bg = behind.color, fill = parseColor(cs.backgroundColor);
    var fillC = fill && fill.a > 0 ? over(fill, bg) : bg;
    var clipBorder = cs.backgroundClip === 'border-box' ? fillC : bg;
    var parts = [];
    sideBorders(cs, clipBorder).forEach(function (c) { parts.push({ part: 'border', c: c }); });
    if (cs.outlineStyle !== 'none' && cs.outlineStyle !== 'auto' && pxv(cs.outlineWidth) >= 0.5) {
      var oc = parseColor(cs.outlineColor);
      if (oc && oc.a > 0) parts.push({ part: 'outline', c: oc.a < 1 ? over(oc, bg) : oc });
    }
    if (!field && !parts.length) return; // filled or text-only controls: the label identifies them (see measurement.md)
    ntChecked++;
    // the component is identifiable if its fill or any drawn boundary reaches 3:1 against what is behind it
    var fillRatio = ratio(fillC, bg), strongest = null;
    parts.forEach(function (p) { p.ratio = ratio(p.c, bg); if (!strongest || p.ratio > strongest.ratio) strongest = p; });
    if (Math.max(fillRatio, strongest ? strongest.ratio : 0) < 3) {
      var best = strongest || { part: 'fill', ratio: fillRatio, c: fillC }; // report the boundary the design relies on
      push(out.nonTextContrast, {
        selector: sel(el), part: best.part, ratio: r2(best.ratio), required: 3, kind: field ? 'field' : 'control',
        color: hex(best.c), background: hex(bg), fillRatio: r2(fillRatio), note: behind.note || undefined
      });
    }
  });
  var ntPrev = new Map(), ntSeen = 0;
  NON_TEXT_SEL.forEach(function (q) {
    var nodes; try { nodes = doc.querySelectorAll(q); } catch (e) { out.notes.push('Invalid nonTextSelectors entry: ' + String(q).slice(0, 60)); return; }
    for (var k = 0; k < nodes.length && ntSeen < MAX_EL; k++, ntSeen++) {
      var el = nodes[k];
      if (!visible(el)) continue;
      var cs = getComputedStyle(el), c, svg = typeof SVGElement !== 'undefined' && el instanceof SVGElement;
      if (svg) {
        var f = cs.fill && cs.fill !== 'none' ? cs.fill : cs.stroke;
        c = /^url\(/.test(f || '') ? null : parseColor(f);
        if (c) c.a *= (parseFloat(cs.fill && cs.fill !== 'none' ? cs.fillOpacity : cs.strokeOpacity) || 1);
      } else c = parseColor(cs.backgroundColor);
      if (c) c.a *= parseFloat(cs.opacity) >= 0 ? parseFloat(cs.opacity) : 1;
      var behindS = effectiveBg(el.parentElement || el);
      if (!c || c.a === 0 || !behindS.color) { ntUnresolved++; continue; }
      ntChecked++;
      var cc = over(c, behindS.color), rr = ratio(cc, behindS.color);
      ntPrev.set(el, cc);
      if (rr < 3) {
        var prevEl = el.previousElementSibling;
        push(out.nonTextContrast, {
          selector: sel(el), part: 'fill', ratio: r2(rr), required: 3, kind: 'selector', color: hex(cc),
          background: hex(behindS.color), vsPrevious: prevEl && ntPrev.has(prevEl) ? r2(ratio(cc, ntPrev.get(prevEl))) : undefined,
          note: behindS.note || undefined
        });
      }
    }
  });

  // ---------- label in name (WCAG 2.5.3) ----------
  interactive.forEach(function (el) {
    if (el.getAttribute('aria-hidden') === 'true') return;
    var lb = el.getAttribute('aria-labelledby'), al = el.getAttribute('aria-label');
    if (!(lb && lb.trim()) && !(al && al.trim())) return;
    var vis = (el.labels && el.labels.length) ? Array.prototype.map.call(el.labels, visibleTextOf).join(' ') : visibleTextOf(el);
    var nv = norm(vis); if (!nv) return;
    var name = accName(el);
    if (norm(name).indexOf(nv) < 0) push(out.labelInName, { selector: sel(el), visibleText: vis.slice(0, 60), accessibleName: name.slice(0, 60) });
  });

  // ---------- ARIA conflicts ----------
  function rendered(el) { return getComputedStyle(el).display !== 'none' && el.getClientRects().length > 0; }
  function focusableIn(scope, skipNativeRadio) {
    return Array.prototype.filter.call(scope.querySelectorAll(INTERACTIVE), function (n) {
      if (skipNativeRadio && n.tagName === 'INPUT' && (n.type === 'radio')) return false;
      return n.tabIndex >= 0 && !isDisabled(n) && rendered(n);
    });
  }
  var ariaNodes = doc.body ? doc.body.querySelectorAll('[role], [aria-pressed], [aria-checked], [aria-selected], [aria-hidden="true"], button, a[href]') : [];
  var CHECKED_OK = /^(checkbox|radio|switch|menuitemcheckbox|menuitemradio|option|treeitem)$/;
  var SELECTED_OK = /^(option|tab|gridcell|row|columnheader|rowheader|treeitem)$/;
  for (var ak = 0; ak < ariaNodes.length && ak < MAX_EL; ak++) {
    var an = ariaNodes[ak];
    if (!rendered(an)) continue;
    var explicitRole = (an.getAttribute('role') || '').trim().split(/\s+/)[0].toLowerCase();
    var native = an.tagName === 'INPUT' || an.tagName === 'SELECT' || an.tagName === 'TEXTAREA';
    var role = explicitRole || (an.tagName === 'BUTTON' ? 'button' : (an.tagName === 'A' ? 'link' : ''));
    var issues = [];
    if (an.hasAttribute('aria-pressed') && role !== 'button') issues.push('aria-pressed on role=' + (role || an.tagName.toLowerCase()) + (role === 'radio' || role === 'tab' ? ' (use aria-' + (role === 'radio' ? 'checked' : 'selected') + ')' : ''));
    if (an.hasAttribute('aria-checked') && !native && !CHECKED_OK.test(role)) issues.push('aria-checked on ' + (explicitRole ? 'role=' + role : 'a ' + an.tagName.toLowerCase() + ' without a checkbox, radio or switch role'));
    if (an.hasAttribute('aria-selected') && !native && !SELECTED_OK.test(role)) issues.push('aria-selected on ' + (explicitRole ? 'role=' + role : 'a ' + an.tagName.toLowerCase() + ' without an option or tab role'));
    if (role === 'tab' && !an.hasAttribute('aria-selected')) issues.push('role=tab without aria-selected');
    if (role === 'tab' && !an.closest('[role="tablist"]')) issues.push('role=tab outside a tablist');
    if (!native && /^(radio|checkbox|switch)$/.test(explicitRole) && !an.hasAttribute('aria-checked')) issues.push('role=' + role + ' without aria-checked');
    if (!native && explicitRole === 'radio' && !an.closest('[role="radiogroup"]')) issues.push('role=radio outside a radiogroup');
    if (explicitRole === 'option' && !an.closest('[role="listbox"], [role="combobox"], [role="grid"], [role="tree"]')) issues.push('role=option outside a listbox');
    if (/^menuitem/.test(explicitRole) && !an.closest('[role="menu"], [role="menubar"], [role="group"]')) issues.push('role=' + explicitRole + ' outside a menu');
    if (/^(tablist|radiogroup|menu|menubar|listbox|toolbar|tree|grid)$/.test(explicitRole) && !an.hasAttribute('aria-activedescendant')) {
      var stops = focusableIn(an, true).length;
      if (stops > 1) issues.push('role=' + explicitRole + ' has ' + stops + ' tab stops (roving tabindex expected)');
    }
    if (an.getAttribute('aria-hidden') === 'true' && !(an.parentElement && an.parentElement.closest('[aria-hidden="true"]'))) {
      var selfF = an.matches(INTERACTIVE) && an.tabIndex >= 0 && !isDisabled(an);
      var inner = focusableIn(an, false).filter(function (n) { return n !== an; }).length;
      if (selfF) issues.push('aria-hidden on a focusable element');
      else if (inner) issues.push('aria-hidden subtree contains ' + inner + ' focusable element(s)');
    }
    if ((role === 'button' || role === 'link') && an.parentElement && an.parentElement.closest('a[href], button, [role="button"], [role="link"]')) issues.push('interactive element nested inside another button or link');
    issues.forEach(function (msg) { push(out.ariaConflicts, { selector: sel(an), issue: msg }); });
  }

  // ---------- layout overflow (for the 200% text recipe) ----------
  out.layoutOverflow = {
    documentScrollWidth: root.scrollWidth, clientWidth: root.clientWidth,
    horizontalScroll: root.scrollWidth > root.clientWidth + 1,
    count: overflowItems.count, truncated: overflowItems.truncated, items: overflowItems.items
  };

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
    hitScan: HIT_SCAN, targetCandidates: targetCands.length, hitProbed: probed, hitProbeCovered: probeCovered,
    hitProbeOffscreen: probeOffscreen, nonTextChecked: ntChecked, nonTextUnresolved: ntUnresolved,
    ms: Date.now() - t0
  };
  out.thresholds = { minTargetPx: TARGET, minTextPx: MIN_TEXT, contrastSmall: 4.5, contrastLarge: 3, nonText: 3, largeTextPx: 24, largeBoldTextPx: 18.66 };
  return JSON.parse(JSON.stringify(out));
})
