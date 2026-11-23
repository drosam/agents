#!/usr/bin/env python3
"""Check hand-written SVG engineering diagrams against the engineering-diagrams rules.

Usage: check_svg.py FILE.svg [FILE.svg ...]

Prints one JSON object per file with "errors", "warnings" and "stats".
Exits 1 when any file has errors, 2 on bad usage. Standard library only (Python 3.8+).
Text widths are estimates; treat fit and overlap findings as prompts for the visual check.
"""
import json
import re
import sys
import xml.etree.ElementTree as ET

SKIP_CONTAINERS = {"defs", "marker", "pattern", "clipPath", "mask", "symbol", "linearGradient", "radialGradient"}
FRAME_ROLES = {"frame", "zone", "note", "legend", "background", "icon"}
MIN_FONT = 9.0
SMALL_FONT = 11.0
CURVE_MAX = 16.0
NODE_BUDGET = 12


def local(tag):
    return tag.split("}", 1)[-1] if isinstance(tag, str) else ""


def num(value, default=None):
    if value is None:
        return default
    m = re.match(r"\s*(-?\d*\.?\d+(?:e-?\d+)?)", str(value))
    return float(m.group(1)) if m else default


def style_map(el):
    out = {}
    for part in (el.get("style") or "").split(";"):
        if ":" in part:
            k, v = part.split(":", 1)
            out[k.strip()] = v.strip()
    return out


INHERITED = ("font-size", "font-family", "font-weight", "letter-spacing", "text-anchor", "stroke", "fill",
             "data-allow-diagonal", "data-role")


def class_rules(root):
    """Collect simple `.class { prop: value }` rules from <style> elements."""
    rules = {}
    for el in root.iter():
        if local(el.tag) != "style" or not el.text:
            continue
        for selectors, body in re.findall(r"([^{}]+)\{([^}]*)\}", el.text):
            props = {}
            for part in body.split(";"):
                if ":" in part:
                    k, v = part.split(":", 1)
                    props[k.strip()] = v.strip()
            for sel in selectors.split(","):
                m = re.fullmatch(r"\s*(?:[a-zA-Z]+)?\.([\w-]+)\s*", sel)
                if m:
                    rules.setdefault(m.group(1), {}).update(props)
    return rules


def walk(el, inherited, ancestors, out, rules):
    attrs = dict(inherited)
    from_class = {}
    for cls in (el.get("class") or "").split():
        from_class.update(rules.get(cls, {}))
    st = style_map(el)
    for key in INHERITED:
        val = st.get(key, from_class.get(key, el.get(key)))
        if val is not None:
            attrs[key] = val
    tag = local(el.tag)
    out.append((el, tag, attrs, ancestors))
    for child in el:
        walk(child, attrs, ancestors + [tag], out, rules)


# Helvetica advance widths (1/1000 em) for ASCII 32-126; Inter and SF run a few percent wider.
HELVETICA = [int(w) for w in (
    "278 278 355 556 556 889 667 191 333 333 389 584 278 333 278 278 556 556 556 556 556 556 556 556 "
    "556 556 278 278 584 584 584 556 1015 667 667 722 722 667 611 778 722 278 500 667 556 833 722 778 "
    "667 778 722 667 611 722 667 944 667 667 611 278 278 278 469 556 333 556 556 500 556 556 278 556 "
    "556 222 222 500 222 833 556 556 556 556 333 500 278 556 500 722 500 500 500 334 260 334 584").split()]


def text_width(s, fs, attrs):
    family = (attrs.get("font-family") or "").lower()
    weight = str(attrs.get("font-weight") or "400")
    bold = weight in ("bold", "bolder") or num(weight, 400) >= 600
    ls_raw = str(attrs.get("letter-spacing") or "0")
    ls = num(ls_raw, 0.0) * (fs if "em" in ls_raw else 1.0)
    if any(k in family for k in ("mono", "menlo", "courier", "consolas")):
        return len(s) * (fs * 0.6 + ls)
    units = sum(HELVETICA[ord(c) - 32] if 32 <= ord(c) <= 126 else 556 for c in s)
    serif = any(k in family for k in ("serif", "georgia", "iowan")) and "sans" not in family
    factor = 0.95 if serif else 1.10 if bold else 1.05
    return units / 1000.0 * fs * factor + len(s) * ls


def bbox_text(x, y, w, fs, anchor):
    x0 = x - w / 2 if anchor == "middle" else x - w if anchor == "end" else x
    return (x0, y - 0.78 * fs, x0 + w, y + 0.22 * fs)


def overlap(a, b):
    w = min(a[2], b[2]) - max(a[0], b[0])
    h = min(a[3], b[3]) - max(a[1], b[1])
    return w * h if w > 0 and h > 0 else 0.0


def path_segments(d):
    tokens = re.findall(r"[MmLlHhVvQqCcSsTtAaZz]|-?\d*\.?\d+(?:e-?\d+)?", d or "")
    segs, i, cmd = [], 0, None
    cx = cy = sx = sy = 0.0

    def take(n):
        nonlocal i
        vals = [float(t) for t in tokens[i:i + n]]
        i += n
        return vals

    sizes = {"M": 2, "L": 2, "H": 1, "V": 1, "Q": 4, "C": 6, "S": 4, "T": 2, "A": 7}
    while i < len(tokens):
        if re.match(r"[A-Za-z]", tokens[i]):
            cmd = tokens[i]
            i += 1
            if cmd in "Zz":
                segs.append(("line", (cx, cy), (sx, sy)))
                cx, cy = sx, sy
                continue
        if cmd is None or cmd in "Zz":
            break
        up = cmd.upper()
        if i + sizes[up] > len(tokens):
            break
        v = take(sizes[up])
        rel = cmd.islower()
        if up == "M":
            nx, ny = (cx + v[0], cy + v[1]) if rel else (v[0], v[1])
            cx, cy, sx, sy = nx, ny, nx, ny
            cmd = "l" if rel else "L"
            continue
        if up == "H":
            end = (cx + v[0] if rel else v[0], cy)
        elif up == "V":
            end = (cx, cy + v[0] if rel else v[0])
        else:
            end = (cx + v[-2], cy + v[-1]) if rel else (v[-2], v[-1])
        kind = "line" if up in "LHV" else "curve"
        segs.append((kind, (cx, cy), end))
        cx, cy = end
    return segs


def describe(el, tag):
    if el.get("id"):
        return "%s#%s" % (tag, el.get("id"))
    if tag == "text":
        return 'text "%s"' % "".join(el.itertext()).strip()[:40]
    keys = ("x", "y", "width", "height", "x1", "y1", "cx", "cy")
    coords = ",".join("%s=%s" % (k, el.get(k)) for k in keys if el.get(k) is not None)
    return "%s(%s)" % (tag, coords) if coords else tag


def check(path):
    errors, warnings = [], []
    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, OSError) as exc:
        return {"file": path, "errors": ["xml: %s" % exc], "warnings": [], "stats": {}}
    if local(root.tag) != "svg":
        errors.append("root: root element is not <svg>")

    vb = [num(p) for p in re.split(r"[\s,]+", (root.get("viewBox") or "").strip()) if p]
    if len(vb) != 4:
        errors.append("viewbox: missing or invalid viewBox")
        vb = [0, 0, num(root.get("width"), 0), num(root.get("height"), 0)]
    vx, vy, vw, vh = vb
    if num(root.get("width")) != vw or num(root.get("height")) != vh:
        warnings.append("viewbox: width/height attributes should equal viewBox size %gx%g" % (vw, vh))

    # Accessibility contract.
    if root.get("role") != "img":
        errors.append('a11y: <svg> needs role="img"')
    children = [c for c in root if isinstance(c.tag, str)]
    title = next((c for c in children if local(c.tag) == "title"), None)
    desc = next((c for c in children if local(c.tag) == "desc"), None)
    if not children or local(children[0].tag) != "title":
        errors.append("a11y: <title> must be the first child of <svg>")
    if title is None or not "".join(title.itertext()).strip():
        errors.append("a11y: missing <title> text")
    elif len("".join(title.itertext()).strip()) > 80:
        warnings.append("a11y: <title> longer than 80 characters")
    if desc is None or not "".join(desc.itertext()).strip():
        errors.append("a11y: missing <desc> with a one or two sentence summary")
    labelled = (root.get("aria-labelledby") or "").split()
    ids = {el.get("id") for el in root.iter() if el.get("id")}
    if not labelled:
        errors.append("a11y: <svg> needs aria-labelledby pointing at the title and desc ids")
    for ref in labelled:
        if ref not in ids:
            errors.append("a11y: aria-labelledby references missing id %r" % ref)

    nodes = []
    walk(root, {}, [], nodes, class_rules(root))

    # Safety and self-containment.
    for el, tag, attrs, anc in nodes:
        if tag in ("script", "foreignObject", "image"):
            errors.append("embed: <%s> is not allowed; keep diagrams self-contained" % tag)
        for key, val in el.attrib.items():
            if local(key) == "href" and not str(val).startswith("#"):
                errors.append("embed: external href %r" % val)
            if key.startswith("on"):
                errors.append("embed: event handler attribute %s" % key)
            for ref in re.findall(r"url\(#([^)]+)\)", str(val)):
                if ref not in ids:
                    errors.append("ref: url(#%s) points at a missing id (%s)" % (ref, describe(el, tag)))
        if tag == "style" and re.search(r"@import|url\((?!#)", el.text or ""):
            errors.append("embed: <style> loads external resources")

    drawable = [n for n in nodes if not (set(n[3]) & SKIP_CONTAINERS) and n[1] not in SKIP_CONTAINERS]

    # Rectangles.
    rects, background = [], None
    for el, tag, attrs, anc in drawable:
        if tag != "rect":
            continue
        x, y = num(el.get("x"), 0.0), num(el.get("y"), 0.0)
        w, h = num(el.get("width"), 0.0), num(el.get("height"), 0.0)
        fill = (attrs.get("fill") or "#000").strip()
        r = {"el": el, "x": x, "y": y, "w": w, "h": h, "x2": x + w, "y2": y + h,
             "stroked": (attrs.get("stroke") or "none") not in ("none", "transparent"),
             "role": el.get("data-role") or attrs.get("data-role"), "fill": fill}
        if w >= vw - 1 and h >= vh - 1 and x <= vx + 1 and y <= vy + 1:
            if fill not in ("none", "transparent") and not fill.startswith("url("):
                background = r
            continue
        if fill.startswith("url("):
            continue
        rects.append(r)
        if x < vx - 1 or y < vy - 1 or r["x2"] > vx + vw + 1 or r["y2"] > vy + vh + 1:
            errors.append("bounds: %s extends outside the viewBox" % describe(el, tag))
    if background is None:
        warnings.append("background: add an opaque full-size background rect; transparent SVGs break on dark pages")

    if not any(el.get("id") == "legend" or el.get("data-role") == "legend" for el, *_ in nodes):
        errors.append('legend: add <g id="legend"> explaining every color, tag, line style and arrowhead used')

    # Text items.
    texts = []
    for el, tag, attrs, anc in drawable:
        if tag != "text":
            continue
        spans = [c for c in el if local(c.tag) == "tspan" and (c.get("x") or c.get("y") or c.get("dy"))]
        items = []
        if spans:
            y_cursor = num(el.get("y"), 0.0)
            for sp in spans:
                sp_attrs = dict(attrs)
                for key in INHERITED:
                    if sp.get(key) is not None:
                        sp_attrs[key] = sp.get(key)
                y_cursor = num(sp.get("y"), y_cursor) + num(sp.get("dy"), 0.0)
                items.append(("".join(sp.itertext()), num(sp.get("x"), num(el.get("x"), 0.0)), y_cursor, sp_attrs))
        else:
            items.append(("".join(el.itertext()), num(el.get("x"), 0.0), num(el.get("y"), 0.0), attrs))
        for s, x, y, a in items:
            s = s.strip()
            if not s:
                continue
            fs = num(a.get("font-size"), 16.0)
            anchor = a.get("text-anchor") or "start"
            box = bbox_text(x, y, text_width(s, fs, a), fs, anchor)
            texts.append({"s": s, "fs": fs, "box": box, "x": x, "y": y, "el": el})
            if fs < MIN_FONT:
                errors.append('font: %gpx below the %gpx minimum ("%s")' % (fs, MIN_FONT, s[:30]))
            elif fs < SMALL_FONT and not s.isupper():
                warnings.append('font: %gpx sentence-case text is hard to read; use >= %gpx ("%s")' % (fs, SMALL_FONT, s[:30]))
            if box[0] < vx - 1 or box[2] > vx + vw + 1 or box[1] < vy - 1 or box[3] > vy + vh + 1:
                errors.append('bounds: text likely runs outside the viewBox ("%s")' % s[:40])

    # Text fit inside the smallest containing rect.
    for t in texts:
        holders = [r for r in rects if r["x"] <= t["x"] <= r["x2"] and r["y"] <= t["y"] <= r["y2"]]
        if not holders:
            continue
        r = min(holders, key=lambda q: q["w"] * q["h"])
        bx0, _, bx1, _ = t["box"]
        if r["stroked"] and (bx1 > r["x2"] or bx0 < r["x"]):
            errors.append('fit: text likely overflows its box %s ("%s"); widen the box or wrap' % (describe(r["el"], "rect"), t["s"][:40]))
        elif r["stroked"] and (bx1 > r["x2"] - 8 or bx0 < r["x"] + 4):
            warnings.append('fit: text is tight against its box edge ("%s"); keep >= 12px padding' % t["s"][:40])
        elif not r["stroked"] and (bx1 > r["x2"] + 2 or bx0 < r["x"] - 2):
            warnings.append('mask: label wider than its mask ("%s")' % t["s"][:40])

    for i, a in enumerate(texts):
        for b in texts[i + 1:]:
            area = overlap(a["box"], b["box"])
            smaller = min((a["box"][2] - a["box"][0]) * (a["box"][3] - a["box"][1]),
                          (b["box"][2] - b["box"][0]) * (b["box"][3] - b["box"][1])) or 1
            if area / smaller > 0.2:
                warnings.append('overlap: texts "%s" and "%s" may overlap' % (a["s"][:25], b["s"][:25]))

    # Connectors.
    connectors = 0
    obstacles = [r for r in rects if r["stroked"] and r["w"] >= 40 and r["h"] >= 24 and r["role"] not in FRAME_ROLES]
    for el, tag, attrs, anc in drawable:
        if tag not in ("path", "line", "polyline"):
            continue
        if (attrs.get("stroke") or "none") == "none":
            continue
        is_connector = (attrs.get("fill") or "none") in ("none", "transparent") or tag == "line"
        if tag == "line":
            segs = [("line", (num(el.get("x1"), 0.0), num(el.get("y1"), 0.0)), (num(el.get("x2"), 0.0), num(el.get("y2"), 0.0)))]
        elif tag == "polyline":
            pts = [float(p) for p in re.findall(r"-?\d*\.?\d+", el.get("points") or "")]
            pairs = list(zip(pts[0::2], pts[1::2]))
            segs = [("line", pairs[k], pairs[k + 1]) for k in range(len(pairs) - 1)]
        else:
            segs = path_segments(el.get("d"))
        if not is_connector or (el.get("data-role") or attrs.get("data-role")) == "shape":
            continue
        connectors += 1
        allow_diag = attrs.get("data-allow-diagonal") is not None
        for kind, (x1, y1), (x2, y2) in segs:
            dx, dy = abs(x2 - x1), abs(y2 - y1)
            if kind == "line" and dx > 0.5 and dy > 0.5 and not allow_diag:
                errors.append("route: diagonal segment (%g,%g)->(%g,%g) in %s; use orthogonal routing" % (x1, y1, x2, y2, describe(el, tag)))
            if kind == "curve" and max(dx, dy) > CURVE_MAX:
                warnings.append("route: curve spans %gpx in %s; use straight runs with r=8 elbows" % (max(dx, dy), describe(el, tag)))
            if kind != "line" or (dx > 0.5 and dy > 0.5):
                continue
            for r in obstacles:
                ix0, iy0, ix1, iy1 = r["x"] + 3, r["y"] + 3, r["x2"] - 3, r["y2"] - 3
                sx0, sx1 = sorted((x1, x2))
                sy0, sy1 = sorted((y1, y2))
                inside = r["x"] - 1 <= sx0 and sx1 <= r["x2"] + 1 and r["y"] - 1 <= sy0 and sy1 <= r["y2"] + 1
                if inside:  # divider or decoration inside the box
                    continue
                if sx1 > ix0 and sx0 < ix1 and sy1 > iy0 and sy0 < iy1:
                    warnings.append("route: %s crosses box %s; route around it or mark the box data-role=frame" % (describe(el, tag), describe(r["el"], "rect")))
                    break

    node_like = [r for r in obstacles if r["w"] >= 80 and r["h"] >= 40]
    if len(node_like) > NODE_BUDGET:
        warnings.append("budget: %d boxes; aim for <= 9 and split above %d" % (len(node_like), NODE_BUDGET))

    return {"file": path, "errors": sorted(set(errors), key=errors.index),
            "warnings": sorted(set(warnings), key=warnings.index),
            "stats": {"texts": len(texts), "boxes": len(node_like), "connectors": connectors, "viewBox": [vx, vy, vw, vh]}}


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 2
    failed = False
    for path in argv:
        result = check(path)
        failed = failed or bool(result["errors"])
        print(json.dumps(result, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
