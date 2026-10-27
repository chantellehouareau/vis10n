#!/usr/bin/env python3
"""Build the VIS10N website.

Reads src/site.html (the design, every section in one file) and src/posts.json
(the Insight articles), and writes one HTML file per page with its own title,
description, share preview, canonical address and structured data for Google:

    index.html                 /
    portfolio.html             /portfolio
    rayj-dennis.html           /rayj-dennis
    insight.html               /insight
    insight/<slug>.html        /insight/<slug>
    privacy.html, terms.html   /privacy, /terms
    404.html, sitemap.xml, robots.txt

Run it after any change to src/:   python3 build.py
Uses the Python standard library only.
"""
import datetime
import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "src"
BASE = "https://vis10nholdings.com"
TODAY = datetime.date.today().isoformat()

ORG_ID = BASE + "/#organization"
SITE_ID = BASE + "/#website"
PERSON_ID = BASE + "/rayj-dennis#person"

RAYJ_PROFILES = [
    "https://www.instagram.com/rayjdennis10/",
    "https://www.linkedin.com/in/rayj-dennis",
    "https://en.wikipedia.org/wiki/RayJ_Dennis",
]
VIS10N_PROFILES = [
    "https://www.linkedin.com/company/vis10n",
    "https://www.instagram.com/vis10nholdings",
]

ORG = {
    "@type": "Organization",
    "@id": ORG_ID,
    "name": "VIS10N Holdings",
    "alternateName": "VIS10N",
    "url": BASE + "/",
    "logo": {"@type": "ImageObject", "url": BASE + "/img/vis10n-logo-square.png", "width": 600, "height": 600},
    "description": "VIS10N Holdings is a global holding company that invests in, builds and partners with ventures across sport, media, marketing, technology and real estate.",
    "foundingDate": "2025",
    "founder": {"@id": PERSON_ID},
    "sameAs": VIS10N_PROFILES,
    "subOrganization": {"@type": "Organization", "name": "Vestrium Global", "url": "https://vestriumglobal.com"},
}
WEBSITE = {
    "@type": "WebSite",
    "@id": SITE_ID,
    "url": BASE + "/",
    "name": "VIS10N Holdings",
    "publisher": {"@id": ORG_ID},
    "inLanguage": "en",
}
PERSON = {
    "@type": "Person",
    "@id": PERSON_ID,
    "name": "RayJ Dennis",
    "alternateName": "Raymond Patterson Dennis",
    "url": BASE + "/rayj-dennis",
    "image": BASE + "/img/rayj-tunnel.jpg",
    "jobTitle": "Founder and CEO",
    "description": "RayJ Dennis is the Founder and CEO of VIS10N Holdings and a point guard for the Atlanta Hawks.",
    "worksFor": {"@id": ORG_ID},
    "affiliation": {"@type": "SportsTeam", "name": "Atlanta Hawks", "sport": "Basketball"},
    "alumniOf": [
        {"@type": "CollegeOrUniversity", "name": "Baylor University"},
        {"@type": "CollegeOrUniversity", "name": "University of Toledo"},
        {"@type": "CollegeOrUniversity", "name": "Boise State University"},
    ],
    "birthPlace": {"@type": "Place", "name": "Plainfield, Illinois"},
    "knowsAbout": ["Sports business", "Athlete ownership", "Venture investing", "Real estate", "Media and entertainment"],
    "sameAs": RAYJ_PROFILES,
}

PAGES = [
    # key, path, output file, title, description, og type, share image
    ("home", "/", "index.html",
     "VIS10N Holdings | Sport, Media and Real Estate Holding Company",
     "VIS10N Holdings, founded by RayJ Dennis, invests in, builds and partners with ventures across sport, media, marketing, technology and real estate.",
     "website", "og-vis10n.jpg"),
    ("portfolio", "/portfolio", "portfolio.html",
     "Portfolio | VIS10N Holdings",
     "The VIS10N Playbook: Healf, Augment, Atorie, Luxe Assist AI, Baselayer, Rorra and Ziggiz, ventures building at the intersection of sport, culture and scalable infrastructure.",
     "website", "og-vis10n.jpg"),
    ("founder", "/rayj-dennis", "rayj-dennis.html",
     "RayJ Dennis | Founder & CEO, VIS10N Holdings",
     "RayJ Dennis is the Founder and CEO of VIS10N Holdings and a point guard for the Atlanta Hawks. From Boise State, Toledo and Baylor to the NBA, he builds from within the sports economy.",
     "profile", "og-rayj-dennis.jpg"),
    ("insight", "/insight", "insight.html",
     "Insight | VIS10N Holdings",
     "Perspectives from VIS10N Holdings and RayJ Dennis on the sports economy: athlete ownership, sports infrastructure, media and emerging market opportunities.",
     "website", "og-vis10n.jpg"),
    ("privacy", "/privacy", "privacy.html",
     "Privacy Policy | VIS10N Holdings",
     "How VIS10N Holdings collects, uses and protects information submitted through vis10nholdings.com.",
     "website", "og-vis10n.jpg"),
    ("terms", "/terms", "terms.html",
     "Terms of Use | VIS10N Holdings",
     "The terms that govern use of the VIS10N Holdings website.",
     "website", "og-vis10n.jpg"),
]

MAIN_RE = re.compile(r'(?:<!-- =+ [A-Z ]+ =+ -->\n)?<main class="page" data-page="(\w+)">.*?</main>\n', re.S)


def esc(s):
    return html.escape(s, quote=True)


def md_to_html(md):
    out, ul = [], None
    for line in md.split("\n"):
        t = line.strip()
        if not t:
            continue
        if t.startswith("- "):
            ul = ul or []
            ul.append(f"<li>{t[2:]}</li>")
            continue
        if ul:
            out.append("<ul>" + "".join(ul) + "</ul>")
            ul = None
        out.append(f"<h2>{t[3:]}</h2>" if t.startswith("## ") else f"<p>{t}</p>")
    if ul:
        out.append("<ul>" + "".join(ul) + "</ul>")
    return "".join(out)


def fmt_date(d):
    return datetime.date.fromisoformat(d).strftime("%d %b %Y").upper()


def read_minutes(p):
    return max(2, round(len(p["body"].split()) / 230))


def companies(site):
    return re.findall(r'\{id:"(\w+)", n:"([^"]+)", s:"([^"]+)".*?d:"([^"]+)"', site)


def head_block(url, title, desc, og_type, image, graph, extra_meta="", robots="index,follow,max-image-preview:large"):
    img = f"{BASE}/img/{image}"
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    ld = ld.replace("</", "<\\/")
    return f"""<link rel="canonical" href="{url}">
<meta name="robots" content="{robots}">
<meta property="og:site_name" content="VIS10N Holdings">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{img}">
{extra_meta}<script type="application/ld+json">{ld}</script>
"""


def page_html(site, keep, title, desc, head, main_override=None):
    out = site
    out = re.sub(r"<title>.*?</title>", f"<title>{esc(title)}</title>", out, count=1, flags=re.S)
    out = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{esc(desc)}">', out, count=1)
    out = out.replace("</head>", head + "</head>", 1)
    out = out.replace('<html lang="en">', f'<html lang="en" data-page="{keep}">', 1)

    def repl(m):
        if main_override is not None:
            return ""
        if m.group(1) != keep:
            return ""
        return m.group(0).replace('<main class="page" ', '<main class="page active" ', 1)

    first = [True]

    def repl_with_override(m):
        if first[0]:
            first[0] = False
            return main_override
        return ""

    out = MAIN_RE.sub(repl_with_override if main_override is not None else repl, out)
    return out


def breadcrumb(items):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)],
    }


def build():
    site = (SRC / "site.html").read_text(encoding="utf-8")
    posts = json.loads((SRC / "posts.json").read_text(encoding="utf-8"))
    posts.sort(key=lambda p: p["date"], reverse=True)
    site = site.replace("/*POSTS_JSON*/[]", json.dumps(posts, ensure_ascii=False).replace("</", "<\\/"), 1)
    assert "/*POSTS_JSON*/" not in site
    cos = companies(site)

    written, sitemap = [], []

    for key, path, out, title, desc, og_type, image in PAGES:
        url = BASE + path if path != "/" else BASE + "/"
        page_type = {"founder": "ProfilePage", "portfolio": "CollectionPage", "insight": "CollectionPage"}.get(key, "WebPage")
        webpage = {
            "@type": page_type, "@id": url + "#webpage", "url": url, "name": title, "description": desc,
            "isPartOf": {"@id": SITE_ID}, "inLanguage": "en",
            "primaryImageOfPage": {"@type": "ImageObject", "url": f"{BASE}/img/{image}"},
        }
        graph = [ORG, WEBSITE, PERSON, webpage]
        if key == "home":
            webpage["about"] = {"@id": ORG_ID}
        if key == "founder":
            webpage["mainEntity"] = {"@id": PERSON_ID}
            webpage["about"] = {"@id": PERSON_ID}
        if key == "portfolio":
            webpage["mainEntity"] = {
                "@type": "ItemList", "name": "VIS10N Holdings portfolio",
                "itemListElement": [
                    {"@type": "ListItem", "position": i + 1,
                     "item": {"@type": "Organization", "name": n, "description": d}}
                    for i, (cid, n, s, d) in enumerate(cos)
                ],
            }
        if key == "insight":
            webpage["mainEntity"] = {
                "@type": "ItemList",
                "itemListElement": [
                    {"@type": "ListItem", "position": i + 1, "url": f"{BASE}/insight/{p['slug']}", "name": p["title"]}
                    for i, p in enumerate(posts)
                ],
            }
        if key != "home":
            graph.append(breadcrumb([("Home", BASE + "/"), (title.split(" | ")[0], url)]))
        head = head_block(url, title, desc, og_type, image, graph)
        (ROOT / out).write_text(page_html(site, key, title, desc, head), encoding="utf-8")
        written.append(out)
        sitemap.append((url, TODAY, {"home": "1.0", "founder": "0.9", "portfolio": "0.8", "insight": "0.8"}.get(key, "0.3")))

    # Insight articles: one file each, article text written into the page.
    (ROOT / "insight").mkdir(exist_ok=True)
    for i, p in enumerate(posts):
        url = f"{BASE}/insight/{p['slug']}"
        title = f"{p['title']} | VIS10N Insight"
        desc = p["excerpt"]
        others = [q for q in posts if q is not p][:3]
        article = {
            "@type": "BlogPosting", "@id": url + "#article", "headline": p["title"], "description": desc,
            "datePublished": p["date"], "dateModified": p.get("updated", p["date"]),
            "author": {"@id": PERSON_ID, "@type": "Person", "name": "RayJ Dennis", "url": BASE + "/rayj-dennis"},
            "publisher": {"@id": ORG_ID}, "mainEntityOfPage": {"@id": url + "#webpage"},
            "image": f"{BASE}/img/og-vis10n.jpg", "articleSection": p["cats"][0], "keywords": p["cats"],
            "wordCount": len(p["body"].split()), "inLanguage": "en",
        }
        webpage = {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title, "description": desc, "isPartOf": {"@id": SITE_ID}}
        graph = [ORG, WEBSITE, PERSON, webpage, article,
                 breadcrumb([("Home", BASE + "/"), ("Insight", BASE + "/insight"), (p["title"], url)])]
        extra = (f'<meta property="article:published_time" content="{p["date"]}">\n'
                 f'<meta property="article:author" content="{BASE}/rayj-dennis">\n'
                 + "".join(f'<meta property="article:tag" content="{esc(c)}">\n' for c in p["cats"]))
        head = head_block(url, title, desc, "article", "og-vis10n.jpg", graph, extra)
        page = page_html(site, "post", title, desc, head)
        meta = (f"<span>{fmt_date(p['date'])}</span><span>{esc(p['author'])}</span>"
                f"<span>{read_minutes(p)} min read</span><span>{esc(' · '.join(p['cats']))}</span>")
        more = "".join(
            f'<a class="irow" href="/insight/{q["slug"]}"><span class="dt">{fmt_date(q["date"])}</span><h3>{q["title"]}</h3>'
            f'<span class="tags">{esc(" · ".join(q["cats"][:2]))}</span><span class="go"></span></a>' for q in others)
        for a, b in [('<h1 id="pTitle"></h1>', f'<h1 id="pTitle">{p["title"]}</h1>'),
                     ('<div class="meta" id="pMeta"></div>', f'<div class="meta" id="pMeta">{meta}</div>'),
                     ('<p class="lede" id="pLede"></p>', f'<p class="lede" id="pLede">{esc(p["excerpt"])}</p>'),
                     ('<div class="body" id="pBody"></div>', f'<div class="body" id="pBody">{md_to_html(p["body"])}</div>'),
                     ('<div class="irows" id="moreRows"></div>', f'<div class="irows" id="moreRows">{more}</div>')]:
            assert page.count(a) == 1, a
            page = page.replace(a, b)
        (ROOT / "insight" / f"{p['slug']}.html").write_text(page, encoding="utf-8")
        written.append(f"insight/{p['slug']}.html")
        sitemap.append((url, p.get("updated", p["date"]), "0.7"))

    # 404
    nf = ('<main class="page active" data-page="notfound">\n  <section class="wrap phero">\n    <span class="label">404</span>\n'
          '    <h1><span class="ln"><span>Page not found</span></span></h1>\n    <div class="sub"><p>The page you are looking for has moved or no longer exists.</p>'
          '<div><a class="btn" href="/">Back to home</a></div></div>\n  </section>\n</main>\n')
    head = head_block(BASE + "/", "Page not found | VIS10N Holdings", "", "website", "og-vis10n.jpg", [ORG], robots="noindex")
    (ROOT / "404.html").write_text(page_html(site, "notfound", "Page not found | VIS10N Holdings", "", head, main_override=nf), encoding="utf-8")
    written.append("404.html")

    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, lm, pr in sitemap:
        sm.append(f"  <url><loc>{u}</loc><lastmod>{lm}</lastmod><priority>{pr}</priority></url>")
    sm.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(sm) + "\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")

    print("Built:", ", ".join(written + ["sitemap.xml", "robots.txt"]))


if __name__ == "__main__":
    build()
