#!/usr/bin/env python3
"""
Automated design preflight for HTML artifacts.

Drives system Google Chrome over the DevTools Protocol (stdlib only) and checks
a set of pages for the defects that are invisible in source and obvious in a
render:

  layout        horizontal overflow at each viewport + the offending elements
  accessibility tap targets under 44px, WCAG AA contrast, heading order,
                H1 count, <img> without alt, SVG without an accessible name
  semantics     form controls present, internal links that do not resolve
  static        CSS classes defined but unused; page classes with no rule

Usage:
    python3 design_preflight.py ./pages --css tokens/globals.css
    python3 design_preflight.py ./pages --css tokens/globals.css \
        --viewport mobile:390 --viewport desktop:1440

Exits non-zero when any check fails.
"""
import argparse
import json
import os
import pathlib
import re
import subprocess
import sys
import time
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render_cdp import Chrome  # noqa: E402

# --------------------------------------------------------------------------
# In-page probes
# --------------------------------------------------------------------------
LAYOUT_JS = r"""
(() => {
  const out = {};
  out.docWidth   = document.documentElement.scrollWidth;
  out.innerWidth = window.innerWidth;
  out.overflowing = [...document.querySelectorAll('body *')]
    .filter(el => {
      const r = el.getBoundingClientRect();
      return r.width > 0 && (r.right > window.innerWidth + 1 || r.left < -1);
    })
    .slice(0, 12)
    .map(el => {
      const r = el.getBoundingClientRect();
      return el.tagName.toLowerCase() + '.' +
             (el.className || '').toString().split(' ')[0] +
             ' [right=' + Math.round(r.right) + ']';
    });

  out.smallTargets = [...document.querySelectorAll('a[href], button, summary')]
    .filter(el => {
      const r = el.getBoundingClientRect();
      if (r.width === 0 || r.height === 0) return false;
      // The design preflight's 44px floor applies to BOTH dimensions.
      // A 48px-high nav link can still have a 30px-wide hit area.
      return r.width < 44 || r.height < 44;
    })
    .slice(0, 15)
    .map(el => {
      const r = el.getBoundingClientRect();
      return el.tagName.toLowerCase() + ' "' +
             (el.textContent || '').trim().slice(0, 30) + '" ' +
             Math.round(r.width) + 'x' + Math.round(r.height);
    });

  out.headings = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(h => h.tagName);
  let jump = null, prev = 0;
  for (const h of out.headings) {
    const lvl = Number(h[1]);
    if (prev && lvl > prev + 1) { jump = h + ' after H' + prev; break; }
    prev = lvl;
  }
  out.headingJump = jump;
  out.h1Count = out.headings.filter(h => h === 'H1').length;

  out.imgsWithoutAlt = [...document.querySelectorAll('img')].filter(i => !i.hasAttribute('alt')).length;
  out.svgWithoutLabel = [...document.querySelectorAll('svg')].filter(s => {
    if (s.getAttribute('aria-hidden') === 'true') return false;
    return !s.getAttribute('aria-label') &&
           !s.querySelector('title') &&
           !s.getAttribute('aria-labelledby');
  }).length;

  out.forms = document.querySelectorAll(
    'form, input, textarea, select, button[type=submit]'
  ).length;

  out.internalLinks = [...document.querySelectorAll('a[href]')]
    .map(a => a.getAttribute('href'))
    .filter(h => h && !h.startsWith('http') && !h.startsWith('tel:') &&
                 !h.startsWith('#') && !h.startsWith('mailto:'));

  return out;
})()
"""

CONTRAST_JS = r"""
(() => {
  const lum = ([r,g,b]) => {
    const f = v => { v/=255; return v <= 0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4); };
    return 0.2126*f(r) + 0.7152*f(g) + 0.0722*f(b);
  };
  const parse = s => {
    const m = s.match(/rgba?\(([^)]+)\)/); if (!m) return null;
    const p = m[1].split(',').map(x => parseFloat(x));
    return [p[0], p[1], p[2], p[3] === undefined ? 1 : p[3]];
  };
  const ratio = (a,b) => {
    const L1 = lum(a), L2 = lum(b);
    return (Math.max(L1,L2) + 0.05) / (Math.min(L1,L2) + 0.05);
  };
  // Effective background: walk ancestors until an opaque background is found.
  const bgOf = el => {
    let e = el;
    while (e) {
      const cs = getComputedStyle(e);
      if (cs.backgroundImage && cs.backgroundImage !== 'none') return null; // unknowable
      const c = parse(cs.backgroundColor);
      if (c && c[3] > 0.95) return c.slice(0,3);
      e = e.parentElement;
    }
    return [255,255,255];
  };

  const out = [];
  const seen = new Set();
  for (const el of document.querySelectorAll('body *')) {
    // only elements that directly contain text
    const own = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    if (!own) continue;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none') continue;
    if (parseFloat(cs.opacity) < 0.1) continue;
    const fg = parse(cs.color); if (!fg) continue;
    if (fg[3] !== undefined && fg[3] < 0.95) continue;
    const bg = bgOf(el); if (!bg) continue;
    const size = parseFloat(cs.fontSize);
    const bold = parseInt(cs.fontWeight) >= 700;
    const large = size >= 24 || (size >= 18.66 && bold);
    const need = large ? 3.0 : 4.5;
    const r = ratio(fg.slice(0,3), bg);
    if (r >= need) continue;
    const key = cs.color + '|' + bg.join(',') + '|' + Math.round(size);
    if (seen.has(key)) continue;
    seen.add(key);
    out.push({
      tag: el.tagName.toLowerCase() + '.' +
           (el.className || '').toString().split(' ')[0],
      text: (el.textContent || '').trim().slice(0, 40),
      ratio: Math.round(r * 100) / 100,
      size, need,
      color: cs.color,
      bg: 'rgb(' + bg.map(Math.round).join(',') + ')',
    });
  }
  return out;
})()
"""


# --------------------------------------------------------------------------
# Raw-source markup validity
# --------------------------------------------------------------------------
# The browser SILENTLY REPAIRS structural errors: a duplicate <main> and a
# stray </footer> both disappear into a well-formed DOM. A DOM-level probe can
# therefore never see them. This check reads the file as served.
#
# Landmark tags whose open/close counts must balance. Chosen because each has
# a required-unique or single-instance semantic in a page shell.
LANDMARK_TAGS = ("main", "header", "footer", "nav", "section", "article", "aside")


def raw_markup_check(path):
    """Return a list of structural problems in the raw HTML source."""
    src = pathlib.Path(path).read_text(encoding="utf-8")
    # Strip regions whose contents would confuse tag counting.
    body = re.sub(r"<script\b.*?</script>", " ", src, flags=re.S | re.I)
    body = re.sub(r"<style\b.*?</style>", " ", body, flags=re.S | re.I)
    body = re.sub(r"<head\b.*?</head>", " ", body, flags=re.S | re.I)
    body = re.sub(r"<!--.*?-->", " ", body, flags=re.S)

    issues = []
    for tag in LANDMARK_TAGS:
        opens = len(re.findall(rf"<{tag}\b", body, re.I))
        closes = len(re.findall(rf"</{tag}\s*>", body, re.I))
        if opens != closes:
            issues.append(f"<{tag}> open {opens} / close {closes} (unbalanced)")
        if re.search(rf"</{tag}\s*>\s*</{tag}\s*>", body, re.I):
            issues.append(f"doubled </{tag}></{tag}>")

    ids = re.findall(r'\bid="([^"]+)"', body)
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        issues.append(f"duplicate id(s): {dupes}")
    return issues


# --------------------------------------------------------------------------
# Copy compliance
# --------------------------------------------------------------------------
# Optional, domain-specific: some briefs forbid guarantees, delivery
# timelines, outcome claims, testimonials, or any language implying a form or
# booking control. Configured from the command line.
COPY_JS = r"""
(() => (document.body.innerText || '').toLowerCase())()
"""


def parse_banned(specs):
    """Parse 'label=regex' specs into (label, compiled) pairs."""
    out = []
    for spec in specs:
        label, _, pattern = spec.partition("=")
        if not pattern:
            raise ValueError(f"--banned-claim needs 'label=regex', got {spec!r}")
        out.append((label, re.compile(pattern, re.I)))
    return out


# --------------------------------------------------------------------------
# Static CSS <-> HTML cross-check
# --------------------------------------------------------------------------
CSS_CLASS_RE = re.compile(r"\.(-?[_a-zA-Z][_a-zA-Z0-9-]*)")
HTML_CLASS_RE = re.compile(r'class="([^"]*)"')


def static_crosscheck(pages_dir, css_files):
    css_text = "\n".join(
        pathlib.Path(c).read_text(encoding="utf-8") for c in css_files
    )
    # strip comments before scanning
    css_text = re.sub(r"/\*.*?\*/", " ", css_text, flags=re.S)
    css_classes = set(CSS_CLASS_RE.findall(css_text))

    html_classes = set()
    for f in pages_dir.glob("*.html"):
        text = f.read_text(encoding="utf-8")
        for chunk in HTML_CLASS_RE.findall(text):
            for c in chunk.split():
                html_classes.add(c)

    unused = sorted(c for c in css_classes if c not in html_classes)
    unstyled = sorted(c for c in html_classes if c not in css_classes)
    return unused, unstyled


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pages", help="directory of HTML files to check")
    ap.add_argument("--css", action="append", default=[], help="CSS file(s) for the static cross-check")
    ap.add_argument("--viewport", action="append", default=[],
                    help="name:WIDTH (repeatable). Default: mobile:390 desktop:1440")
    ap.add_argument("--allow-forms", action="store_true",
                    help="do not fail when form controls are present")
    ap.add_argument("--banned-claim", action="append", default=[],
                    metavar="LABEL=REGEX",
                    help="fail when page text matches REGEX (repeatable). "
                         "Use for briefs that forbid guarantees, timelines, "
                         "outcomes, testimonials, or form/booking language.")
    args = ap.parse_args()

    banned = parse_banned(args.banned_claim)

    pages_dir = pathlib.Path(args.pages).resolve()
    files = sorted(pages_dir.glob("*.html"))
    if not files:
        print("No HTML files found", file=sys.stderr)
        return 1

    viewports = []
    for spec in (args.viewport or ["mobile:390", "desktop:1440"]):
        name, _, w = spec.partition(":")
        viewports.append((name, int(w)))

    failures = []
    chrome = Chrome(profile="/tmp/cdp-preflight-profile")
    try:
        for f in files:
            url = f.as_uri()
            print(f"\n=== {f.name} ===")

            # --- raw-source markup validity (browser cannot see these) ---
            issues = raw_markup_check(f)
            if issues:
                failures.append(f"{f.name}: raw markup — {'; '.join(issues)}")
            print(f"  [{'OK ' if not issues else 'FAIL'}] raw source markup: "
                  f"{'; '.join(issues) if issues else 'well-formed'}")

            for vp, width in viewports:
                chrome.cdp.call(
                    "Emulation.setDeviceMetricsOverride",
                    width=width, height=900, deviceScaleFactor=1,
                    mobile=(vp == "mobile"),
                )
                chrome.cdp.call("Page.navigate", url=url)
                time.sleep(1.2)
                d = chrome.cdp.evaluate(LAYOUT_JS)

                over = d["docWidth"] - d["innerWidth"]
                ok = over <= 0
                if not ok:
                    failures.append(f"{f.name}@{vp}: horizontal overflow {over}px")
                print(f"  [{'OK ' if ok else 'FAIL'}] {vp} overflow={over}px  "
                      f"offenders={d['overflowing'] or 'none'}")

                if vp == "mobile":
                    small = d["smallTargets"]
                    if small:
                        failures.append(f"{f.name}: tap targets <44px: {small}")
                    print(f"  [{'OK ' if not small else 'FAIL'}] "
                          f"tap targets <44px: {small or 'none'}")

                    h1ok = d["h1Count"] == 1
                    if not h1ok:
                        failures.append(f"{f.name}: h1 count {d['h1Count']}")
                    print(f"  [{'OK ' if h1ok else 'FAIL'}] h1 count={d['h1Count']}  "
                          f"heading jump={d['headingJump'] or 'none'}")

                    if d["headingJump"]:
                        failures.append(f"{f.name}: heading jump {d['headingJump']}")

                    if d["forms"] and not args.allow_forms:
                        failures.append(f"{f.name}: {d['forms']} form controls present")
                    print(f"  [{'OK ' if not d['forms'] else 'WARN'}] "
                          f"form controls={d['forms']}")

                    a11y = (d["imgsWithoutAlt"], d["svgWithoutLabel"])
                    if any(a11y):
                        failures.append(f"{f.name}: imgs missing alt={a11y[0]}, "
                                        f"svg missing label={a11y[1]}")
                    print(f"  [{'OK ' if not any(a11y) else 'FAIL'}] "
                          f"imgs missing alt={a11y[0]}  svg missing label={a11y[1]}")

                    print(f"  internal links: {sorted(set(d['internalLinks']))}")

                    # --- copy compliance (only if the brief configures it) ---
                    if banned:
                        text = chrome.cdp.evaluate(COPY_JS)
                        hits = [lab for lab, rx in banned if rx.search(text or "")]
                        if hits:
                            failures.append(f"{f.name}: banned claim language: {hits}")
                        print(f"  [{'OK ' if not hits else 'FAIL'}] "
                              f"banned claims: {hits or 'none'}")

                    # dead link check
                    for href in sorted(set(d["internalLinks"])):
                        target = (f.parent / href.split("#")[0]).resolve()
                        if not target.exists():
                            failures.append(f"{f.name}: dead link {href}")
                            print(f"  [FAIL] dead link: {href}")

            # contrast, measured at desktop width
            chrome.cdp.call(
                "Emulation.setDeviceMetricsOverride",
                width=1440, height=1000, deviceScaleFactor=1, mobile=False,
            )
            chrome.cdp.call("Page.navigate", url=url)
            time.sleep(1.2)
            rows = chrome.cdp.evaluate(CONTRAST_JS)
            print("  contrast failures:")
            if not rows:
                print("    (none)")
            for row in rows:
                failures.append(
                    f"{f.name}: contrast {row['tag']} "
                    f"\"{row['text']}\" = {row['ratio']} (need {row['need']})"
                )
                print(f"    [FAIL] {row['tag']:<28} {row['ratio']:>6} "
                      f"(need {row['need']})  {row['color']} on {row['bg']}")
    finally:
        chrome.close()

    if args.css:
        print("\n=== static CSS <-> HTML cross-check ===")
        unused, unstyled = static_crosscheck(pages_dir, args.css)
        if unused:
            print(f"  [WARN] CSS classes never used in markup ({len(unused)}): "
                  f"{unused[:20]}")
        if unstyled:
            print(f"  [WARN] markup classes with no CSS rule ({len(unstyled)}): "
                  f"{unstyled[:20]}")

    print("\n" + "=" * 62)
    if failures:
        print(f"FAILURES ({len(failures)}):")
        for x in failures:
            print("  -", x)
        return 1
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
