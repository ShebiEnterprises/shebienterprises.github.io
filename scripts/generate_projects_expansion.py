#!/usr/bin/env python3
"""Deepen 6 project pages, add 5 new, wire portfolio CTAs, update sitemap/llms."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://shebienterprises.com"


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def img_url(name: str) -> str:
    return "/img/works/" + quote(name)


# Shared chrome snippets read from an existing service page after generation
def nav_footer_from_template() -> tuple[str, str]:
    sample = (ROOT / "ourservice" / "acpcladding" / "index.html").read_text(encoding="utf-8")
    header = re.search(r"<header class=\"navbar[\s\S]*?</header>", sample).group(0)
    footer = re.search(r"<footer class=\"footer\">[\s\S]*?</footer>", sample).group(0)
    wa = re.search(r'<a href="https://wa\.me/917738479381[\s\S]*?</a>\s*<script src="https://cdnjs', sample)
    # get whatsapp float only
    wa_float = re.search(
        r'<a href="https://wa\.me/917738479381\?text=[^"]+" class="whatsapp-float"[\s\S]*?</a>',
        sample,
    ).group(0)
    return header, footer + "\n\n    " + wa_float


PROJECTS = [
    {
        "slug": "lodha-residential",
        "title": "Lodha Residential Tower",
        "nav": "Lodha Residential",
        "location": "Mumbai Metropolitan Region, Maharashtra",
        "typology": "High-rise residential",
        "client": "Lodha Group (developer project)",
        "desc_meta": "Stone cladding facade package for a Lodha residential tower in Mumbai by Shebi Enterprises - podium and typical floors.",
        "tagline": "Stone facade package for a high-rise residential development in the Mumbai region.",
        "overview": "Shebi Enterprises delivered stone cladding works on a Lodha residential tower where podium prestige and typical-floor cycles had to stay aligned with monsoon windows. The package focused on joint rhythm, drip edges and clean interfaces with windows and waterproofing.",
        "scope": [
            "Podium and typical-floor stone cladding",
            "Movement joints aligned to the structural grid",
            "Coordination with waterproofing and drip edges",
            "Window and cladding interface detailing",
            "Protection, cleaning and handover notes",
        ],
        "challenges": "Monsoon sequencing, tight floor cycles and shared hoist access with other trades. We resolved this with protected curing windows, buffer days in the programme and clear interface ownership with waterproofing and fenestration teams.",
        "materials": "Natural stone (granite / specified finishes), bedding and fixing systems per approved details, weathering sealants at interfaces.",
        "services": [
            ("/ourservice/stonewetcladding/", "Stone Wet Cladding"),
            ("/ourservice/stonedrycladding/", "Stone Dry Cladding"),
            ("/ourservice/canopy-dropoff-packages/", "Canopy & Drop-off Packages"),
        ],
        "hero": "drywetino stone cladding Lodha Project.jpg",
        "gallery": [
            "drywetino stone cladding Lodha Project.jpg",
            "drywetino stone cladding Lodha Project 2.jpg",
            "Lodha Aqua.jpg",
            "Lodha Exeles Fountain Cladding.jpg",
        ],
        "og": "drywetino stone cladding Lodha Project.jpg",
    },
    {
        "slug": "itc-hotel-hyderabad",
        "title": "ITC Hotel Hyderabad",
        "nav": "ITC Hotel Hyderabad",
        "location": "Hyderabad, Telangana",
        "typology": "Hospitality / hotel facade",
        "client": "ITC Hotels (project delivery)",
        "desc_meta": "Hospitality facade works for ITC Hotel Hyderabad by Shebi Enterprises - cladding coordinated for guest arrival and elevations.",
        "tagline": "Hospitality facade delivery with finish quality suited to a flagship hotel elevation.",
        "overview": "Hotel facades demand arrival-grade finishes, careful night-work coordination and details that survive continuous operations. On the ITC Hotel Hyderabad package, Shebi Enterprises focused on cladding quality, joint consistency and interfaces that stay presentable under guest-facing scrutiny.",
        "scope": [
            "Facade cladding package for hospitality elevations",
            "Joint and finish quality for arrival-facing zones",
            "Coordination with other envelope trades",
            "Protection during finishing and soft opening windows",
            "Documentation for handover",
        ],
        "challenges": "Live-site discipline, finish protection and sequencing around other hotel trades. We planned access and protection so cladding edges and corners stayed clean through the finishing period.",
        "materials": "Specified cladding systems and sealants matched to hospitality exposure and cleaning regimes.",
        "services": [
            ("/ourservice/acpcladding/", "ACP Cladding"),
            ("/ourservice/stonewetcladding/", "Stone Wet Cladding"),
            ("/ourservice/entrance-portals-metalwork/", "Entrance Portals"),
        ],
        "hero": "ITC hotel Hyderabad.jpg",
        "gallery": ["ITC hotel Hyderabad.jpg"],
        "og": "ITC hotel Hyderabad.jpg",
        "extra_gallery_note": True,
    },
    {
        "slug": "reliance-bkc",
        "title": "Reliance BKC",
        "nav": "Reliance BKC",
        "location": "Bandra Kurla Complex, Mumbai",
        "typology": "Commercial / corporate campus",
        "client": "Reliance Industries (project context)",
        "desc_meta": "Commercial facade works at Reliance BKC Mumbai by Shebi Enterprises - envelope cladding for a corporate campus setting.",
        "tagline": "Commercial envelope cladding delivered in a dense BKC campus environment.",
        "overview": "BKC sites demand logistics realism: limited staging, security gates and coordinated crane or hoist windows. Shebi Enterprises executed facade cladding works with survey-driven brackets and elevation finishes suited to a corporate campus.",
        "scope": [
            "Facade cladding on commercial elevations",
            "Bracket and subframe coordination",
            "Interface detailing with glazing where present",
            "Site logistics within campus constraints",
            "QA and handover documentation",
        ],
        "challenges": "Dense urban logistics and multi-trade coordination. Staging and delivery were planned around campus access rules so hang and cladding days stayed productive.",
        "materials": "ACP / metal cladding systems as specified, fabricated brackets, weathering sealants.",
        "services": [
            ("/ourservice/acpcladding/", "ACP Cladding"),
            ("/ourservice/fabricationwork/", "Fabrication Works"),
            ("/ourservice/glazingwork/", "Glazing Works"),
        ],
        "hero": "IMG20180216114240.jpg",
        "gallery": ["IMG20180216114240.jpg", "american bank bkc 3.jpg", "Orbit BKC.jpg"],
        "og": "IMG20180216114240.jpg",
    },
    {
        "slug": "lt-construction",
        "title": "L&T Construction Project",
        "nav": "L&T Construction",
        "location": "India (L&T project site)",
        "typology": "Institutional / commercial granite cladding",
        "client": "Larsen & Toubro (construction project)",
        "desc_meta": "Granite cladding works on an L&T construction project by Shebi Enterprises - durable stone elevations.",
        "tagline": "Granite cladding delivered to the standards of a major construction programme.",
        "overview": "Working within an L&T construction programme means aligning stone delivery, fixing quality and safety culture with a large multi-trade site. Shebi Enterprises executed granite cladding with attention to panel alignment, anchors and joint consistency.",
        "scope": [
            "Granite cladding supply/install as tendered",
            "Mechanical or wet fixing per approved details",
            "Alignment and joint quality control",
            "Safety at height and method statements",
            "Coordination with main contractor programme",
        ],
        "challenges": "Programme pressure and interface with main contractor logistics. Clear method statements and staged deliveries kept stone quality intact through peak site activity.",
        "materials": "Granite panels, stainless / specified anchors, sealants and flashings.",
        "services": [
            ("/ourservice/stonedrycladding/", "Stone Dry Cladding"),
            ("/ourservice/stonewetcladding/", "Stone Wet Cladding"),
            ("/ourservice/fabricationwork/", "Fabrication Works"),
        ],
        "hero": "granite cladding L &T Project.jpg",
        "gallery": [
            "granite cladding L &T Project.jpg",
            "granite cladding L &T Project 2.jpg",
        ],
        "og": "granite cladding L &T Project.jpg",
    },
    {
        "slug": "oberoi-commercial",
        "title": "Oberoi Commercial",
        "nav": "Oberoi Commercial",
        "location": "Mumbai, Maharashtra",
        "typology": "Commercial facade",
        "client": "Oberoi Realty (project context)",
        "desc_meta": "Commercial facade cladding for an Oberoi project in Mumbai by Shebi Enterprises.",
        "tagline": "Commercial facade finishes aligned to a premium developer elevation brief.",
        "overview": "Premium commercial elevations need consistent panel lines, clean corners and reliable weather detailing. Shebi Enterprises delivered cladding works with developer-grade QA expectations on an Oberoi commercial context project.",
        "scope": [
            "Facade cladding package",
            "Corner and joint quality",
            "Weather detailing at interfaces",
            "Site QA and mock-up support where required",
            "Handover documentation",
        ],
        "challenges": "Finish expectations and trade interfaces on a live commercial programme. We locked samples early and protected completed faces during subsequent works.",
        "materials": "Specified cladding panels, subframes and sealants.",
        "services": [
            ("/ourservice/acpcladding/", "ACP Cladding"),
            ("/ourservice/glazingwork/", "Glazing Works"),
            ("/ourservice/facade-mockups-sample-walls/", "Facade Mock-ups"),
        ],
        "hero": "IMG20170911113814.jpg",
        "gallery": ["IMG20170911113814.jpg", "IMG20170222134133.jpg", "IMG20180301130204.jpg"],
        "og": "IMG20170911113814.jpg",
    },
    {
        "slug": "piramal-residential",
        "title": "Piramal Residential",
        "nav": "Piramal Residential",
        "location": "Mumbai, Maharashtra",
        "typology": "Residential tower cladding",
        "client": "Piramal Realty (project context)",
        "desc_meta": "Residential facade cladding for a Piramal project in Mumbai by Shebi Enterprises.",
        "tagline": "Residential cladding focused on podium presence and typical-floor consistency.",
        "overview": "Residential towers balance podium feature quality with repetitive typical-floor production. Shebi Enterprises delivered cladding works for a Piramal residential context with attention to movement joints, monsoon detailing and drop-off facing finishes.",
        "scope": [
            "Residential facade cladding",
            "Podium feature zones",
            "Movement and weather joints",
            "Coordination with fenestration",
            "Cleaning and protection before handover",
        ],
        "challenges": "Occupancy-adjacent works and finish protection. Sequencing and temporary protection kept completed elevations presentable through the final stretch.",
        "materials": "Stone / ACP as specified for the elevation, sealants and flashings.",
        "services": [
            ("/ourservice/stonewetcladding/", "Stone Wet Cladding"),
            ("/ourservice/acpcladding/", "ACP Cladding"),
            ("/ourservice/residential-podium-cladding/", "Residential Podium") if False else ("/ourservice/canopy-dropoff-packages/", "Drop-off Packages"),
        ],
        "hero": "IMG20170222134133.jpg",
        "gallery": ["IMG20170222134133.jpg", "IMG20170911113814.jpg", "drywetino stone cladding Lodha Project.jpg"],
        "og": "IMG20170222134133.jpg",
    },
    {
        "slug": "sunteck-bandra",
        "title": "Sunteck Bandra",
        "nav": "Sunteck Bandra",
        "location": "Bandra, Mumbai",
        "typology": "Residential / mixed facade works",
        "client": "Sunteck Realty (project context)",
        "desc_meta": "Facade works at Sunteck Bandra Mumbai by Shebi Enterprises - cladding for a premium western suburb elevation.",
        "tagline": "Facade cladding delivered for a Sunteck development in Bandra.",
        "overview": "Sunteck Bandra elevations required careful cladding alignment and coastal-air awareness. Shebi Enterprises executed facade works with attention to panel lines, joints and interfaces visible from the street and arrival court.",
        "scope": [
            "Facade cladding package",
            "Joint and sealant quality",
            "Arrival-facing finish zones",
            "Coordination with other envelope trades",
            "Handover documentation",
        ],
        "challenges": "Urban site constraints in Bandra and finish expectations on street-facing elevations. Deliveries and protection were planned around limited staging.",
        "materials": "Specified cladding systems, subframes, sealants suited to coastal humidity.",
        "services": [
            ("/ourservice/acpcladding/", "ACP Cladding"),
            ("/ourservice/glazingwork/", "Glazing Works"),
            ("/ourservice/facade-maintenance/", "Facade Maintenance"),
        ],
        "hero": "sunteck bandra.jpg",
        "gallery": ["sunteck bandra.jpg", "sunteck bandra 2.jpg", "sunteck bandra 3.jpg", "sunteck city 1.jpg"],
        "og": "sunteck bandra.jpg",
    },
    {
        "slug": "suraj-estate",
        "title": "Suraj Estate",
        "nav": "Suraj Estate",
        "location": "Mumbai (incl. Dadar context works)",
        "typology": "Residential facade works",
        "client": "Suraj Estate (project context)",
        "desc_meta": "Facade works for Suraj Estate projects in Mumbai by Shebi Enterprises.",
        "tagline": "Residential facade cladding across Suraj Estate project elevations.",
        "overview": "Suraj Estate packages called for consistent residential cladding with practical site sequencing. Shebi Enterprises delivered facade works including elevations documented across Suraj Estate and Dadar-context photography in our portfolio.",
        "scope": [
            "Residential facade cladding",
            "Elevation consistency across faces",
            "Weather detailing",
            "Site QA",
            "Handover support",
        ],
        "challenges": "Multi-elevation coordination and occupied-neighbour constraints typical of dense Mumbai plots. Method statements kept work predictable for the client team.",
        "materials": "Specified stone / ACP systems and compatible sealants.",
        "services": [
            ("/ourservice/acpcladding/", "ACP Cladding"),
            ("/ourservice/stonewetcladding/", "Stone Wet Cladding"),
            ("/ourservice/retrofit-recladding/", "Retrofit & Recladding"),
        ],
        "hero": "suraj estate 1.jpg",
        "gallery": [
            "suraj estate 1.jpg",
            "suraj estate 3.jpg",
            "suraj estate 4.jpg",
            "suraj estate 5.jpg",
            "suraj estate dadar 2.jpg",
        ],
        "og": "suraj estate 1.jpg",
    },
    {
        "slug": "orbit-bkc",
        "title": "Orbit BKC",
        "nav": "Orbit BKC",
        "location": "Bandra Kurla Complex, Mumbai",
        "typology": "Commercial facade",
        "client": "Orbit (BKC project context)",
        "desc_meta": "Facade works at Orbit BKC Mumbai by Shebi Enterprises - commercial envelope cladding.",
        "tagline": "Commercial facade delivery in the BKC business district.",
        "overview": "Orbit BKC required commercial-grade cladding finishes in a high-visibility BKC setting. Shebi Enterprises executed facade works with survey accuracy and weather detailing suited to Mumbai monsoon exposure.",
        "scope": [
            "Commercial facade cladding",
            "Subframe and panel installation",
            "Joint sealant quality",
            "Campus logistics coordination",
            "QA documentation",
        ],
        "challenges": "BKC access control and multi-contractor sequencing. We aligned deliveries with site permits so cladding progress stayed continuous.",
        "materials": "Specified cladding panels, brackets and sealants.",
        "services": [
            ("/ourservice/acpcladding/", "ACP Cladding"),
            ("/ourservice/fabricationwork/", "Fabrication Works"),
            ("/ourservice/glazingwork/", "Glazing Works"),
        ],
        "hero": "Orbit BKC.jpg",
        "gallery": ["Orbit BKC.jpg", "Orbit BKC 2.jpg"],
        "og": "Orbit BKC.jpg",
    },
    {
        "slug": "adani-bungalows",
        "title": "Adani Bungalows",
        "nav": "Adani Bungalows",
        "location": "India (bungalow / villa facade package)",
        "typology": "Premium bungalow cladding",
        "client": "Adani (builder bungalow context)",
        "desc_meta": "Premium bungalow facade cladding for an Adani builder package by Shebi Enterprises.",
        "tagline": "Bespoke bungalow cladding where finish quality is inspected at close range.",
        "overview": "Bungalow and villa facades are judged at arm's length: stone or cladding edges, corners and junctions with canopies must be flawless. Shebi Enterprises delivered facade works on an Adani builder bungalow package with that level of finish care.",
        "scope": [
            "Bungalow facade cladding",
            "Feature walls and external finishes",
            "Interface with canopies and openings",
            "Close-range finish QA",
            "Protection through handover",
        ],
        "challenges": "High visual scrutiny and coordination with landscape and interior handover dates. Protection and cleaning protocols were enforced until client walkthrough.",
        "materials": "Specified stone / cladding finishes and sealants for external exposure.",
        "services": [
            ("/ourservice/stonewetcladding/", "Stone Wet Cladding"),
            ("/ourservice/acpcladding/", "ACP Cladding"),
            ("/ourservice/skylights-canopies/", "Skylights & Canopies"),
        ],
        "hero": "adani builder 5 bungalow 1.jpg",
        "gallery": ["adani builder 5 bungalow 1.jpg", "adani builder 5 bungalow 2.jpg"],
        "og": "adani builder 5 bungalow 1.jpg",
    },
    {
        "slug": "american-bank-bkc",
        "title": "American Bank BKC",
        "nav": "American Bank BKC",
        "location": "Bandra Kurla Complex, Mumbai",
        "typology": "Commercial / banking facade",
        "client": "American Bank BKC (project context)",
        "desc_meta": "Facade works at American Bank BKC Mumbai by Shebi Enterprises - commercial envelope finishes.",
        "tagline": "Commercial facade works for a banking facility elevation in BKC.",
        "overview": "Banking and commercial facilities in BKC need discreet, durable envelope finishes and disciplined site behaviour. Shebi Enterprises delivered facade works documented across multiple American Bank BKC progress photographs in our portfolio.",
        "scope": [
            "Commercial facade cladding",
            "Elevation consistency",
            "Weather and joint detailing",
            "Secure-site logistics",
            "QA and handover",
        ],
        "challenges": "Secure campus access and limited working windows. Permits and delivery slots were planned with the site team to avoid idle labour.",
        "materials": "Specified cladding systems, fabricated supports and sealants.",
        "services": [
            ("/ourservice/acpcladding/", "ACP Cladding"),
            ("/ourservice/fabricationwork/", "Fabrication Works"),
            ("/ourservice/facade-maintenance/", "Facade Maintenance"),
        ],
        "hero": "american bank bkc 3.jpg",
        "gallery": [
            "american bank bkc 1.jpg",
            "american bank bkc 2.jpg",
            "american bank bkc 3.jpg",
            "american bank bkc 4.jpg",
            "american bank bkc 5.jpg",
            "american bank bkc 6.jpg",
        ],
        "og": "american bank bkc 3.jpg",
    },
]

# fix piramal services list
for p in PROJECTS:
    if p["slug"] == "piramal-residential":
        p["services"] = [
            ("/ourservice/stonewetcladding/", "Stone Wet Cladding"),
            ("/ourservice/acpcladding/", "ACP Cladding"),
            ("/ourservice/canopy-dropoff-packages/", "Drop-off Packages"),
        ]


def render_project(p: dict, header: str, footer_block: str) -> None:
    slug = p["slug"]
    url = f"{SITE}/projects/{slug}/"
    og = f"{SITE}{img_url(p['og'])}"
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "@id": f"{SITE}/#organization",
                "name": "Shebi Enterprises",
                "url": f"{SITE}/",
                "logo": f"{SITE}/logo/LightTheme.svg",
            },
            {
                "@type": "WebPage",
                "@id": f"{url}#webpage",
                "url": url,
                "name": f"{p['title']} | Shebi Enterprises",
                "description": p["desc_meta"],
                "primaryImageOfPage": {"@type": "ImageObject", "url": og},
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{url}#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                    {"@type": "ListItem", "position": 2, "name": "Projects", "item": f"{SITE}/portfolio/"},
                    {"@type": "ListItem", "position": 3, "name": p["title"], "item": url},
                ],
            },
            {
                "@type": "CreativeWork",
                "@id": f"{url}#project",
                "name": p["title"],
                "description": p["desc_meta"],
                "url": url,
                "image": og,
                "creator": {"@id": f"{SITE}/#organization"},
                "contentLocation": {
                    "@type": "Place",
                    "name": p["location"],
                    "address": {"@type": "PostalAddress", "addressCountry": "IN"},
                },
            },
        ],
    }
    scope = "\n".join(f"              <li><i class=\"fas fa-check\"></i><span>{esc(s)}</span></li>" for s in p["scope"])
    services = "\n".join(f'              <li style="margin:8px 0"><a href="{h}">{esc(t)}</a></li>' for h, t in p["services"])
    gallery = "\n".join(
        f'            <img src="{img_url(g)}" alt="{esc(p["title"])} - facade photo" loading="lazy" width="400" height="300" style="border-radius: var(--border-radius); object-fit: cover; width: 100%; height: 220px" />'
        for g in p["gallery"]
    )
    # related projects
    others = [x for x in PROJECTS if x["slug"] != slug][:3]
    related = "\n".join(
        f'''            <a href="/projects/{o['slug']}/" class="card" style="text-decoration:none;color:inherit">
              <img src="{img_url(o['hero'])}" alt="{esc(o['title'])}" loading="lazy" width="400" height="260" />
              <div style="padding:16px"><h4>{esc(o['title'])}</h4><p>{esc(o['typology'])}</p></div>
            </a>'''
        for o in others
    )

    page = f'''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="icon" href="/logo/favicon.svg" type="image/svg+xml" sizes="any" />
    <link rel="apple-touch-icon" href="/logo/favicon.svg" />
    <link rel="manifest" href="/manifest.json" />
    <title>{esc(p['title'])} | Shebi Enterprises</title>
    <meta name="description" content="{esc(p['desc_meta'])}" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&amp;family=Inter:wght@300;400;500;600&amp;family=Space+Grotesk:wght@400;500;600&amp;display=swap" rel="stylesheet" />
    <link href="https://cdnjs.cloudflare.com/ajax/libs/aos/2.3.4/aos.css" rel="stylesheet" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" />
    <link rel="stylesheet" href="/css/style.css" />
    <link rel="stylesheet" href="/css/animations.css" />
    <link rel="stylesheet" href="/css/responsive.css" />
    <link rel="canonical" href="{url}" />
    <meta property="og:type" content="website" />
    <meta property="og:site_name" content="Shebi Enterprises" />
    <meta property="og:title" content="{esc(p['title'])} | Shebi Enterprises" />
    <meta property="og:description" content="{esc(p['desc_meta'])}" />
    <meta property="og:url" content="{url}" />
    <meta property="og:image" content="{og}" />
    <meta property="og:locale" content="en_IN" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{esc(p['title'])} | Shebi Enterprises" />
    <meta name="twitter:description" content="{esc(p['desc_meta'])}" />
    <meta name="twitter:image" content="{og}" />
    <script type="application/ld+json">
{json.dumps(schema, indent=2)}
    </script>
  </head>
  <body>
{header}

    <main class="page-wrap">
      <section class="page-hero">
        <div class="container">
          <nav class="breadcrumb" aria-label="Breadcrumb">
            <a href="/">Home</a>
            <i class="fas fa-chevron-right" aria-hidden="true"></i>
            <a href="/portfolio/">Projects</a>
            <i class="fas fa-chevron-right" aria-hidden="true"></i>
            <span>{esc(p['nav'])}</span>
          </nav>
          <h1 data-aos="fade-up">{esc(p['title'])}</h1>
          <p data-aos="fade-up" data-aos-delay="100">{esc(p['tagline'])}</p>
        </div>
      </section>

      <aside class="seo-key-facts container" style="max-width: 1100px; margin: 8px auto 28px;" aria-label="Key facts">
        <h3>Project facts</h3>
        <ul>
            <li>Location: {esc(p['location'])}</li>
            <li>Typology: {esc(p['typology'])}</li>
            <li>Contractor: Shebi Enterprises, Mumbai</li>
            <li>Contact: info@shebienterprises.com · +91 9321598252</li>
        </ul>
      </aside>

      <section class="service-inner-section">
        <div class="container why-grid">
          <div data-aos="fade-right">
            <img src="{img_url(p['hero'])}" alt="{esc(p['title'])} facade" class="why-img" width="700" height="520" loading="lazy" />
          </div>
          <div data-aos="fade-left">
            <span class="label" style="color: var(--secondary); font-family: var(--font-accent); letter-spacing: 2px; text-transform: uppercase; font-size: 0.8rem">Overview</span>
            <h2 style="color: var(--primary); margin: 12px 0">{esc(p['title'])}</h2>
            <p>{esc(p['overview'])}</p>
            <p style="margin-top:12px"><strong>Client context:</strong> {esc(p['client'])}</p>
          </div>
        </div>
      </section>

      <section class="service-inner-section alt">
        <div class="container grid-2">
          <div>
            <h2 style="color: var(--primary); margin-bottom: 16px">Scope of works</h2>
            <ul class="capabilities-list" style="display:grid;gap:12px">
{scope}
            </ul>
          </div>
          <div>
            <h2 style="color: var(--primary); margin-bottom: 16px">Challenges &amp; solutions</h2>
            <p>{esc(p['challenges'])}</p>
            <h3 style="margin-top: 24px; color: var(--accent)">Materials &amp; systems</h3>
            <p>{esc(p['materials'])}</p>
          </div>
        </div>
      </section>

      <section class="service-inner-section">
        <div class="container">
          <h2 style="color: var(--primary); margin-bottom: 16px">Services used</h2>
          <p style="margin-bottom:16px;color:var(--gray)">Related Shebi Enterprises packages for similar briefs.</p>
          <ul style="line-height:1.7;padding-left:1.2rem">
{services}
          </ul>
        </div>
      </section>

      <section class="service-inner-section alt">
        <div class="container">
          <h2 style="color: var(--primary); margin-bottom: 24px">Gallery</h2>
          <div class="featured-projects-grid">
{gallery}
          </div>
        </div>
      </section>

      <section class="service-inner-section">
        <div class="container">
          <h2 style="color: var(--primary); margin-bottom: 24px">Related projects</h2>
          <div class="related-projects-grid">
{related}
          </div>
        </div>
      </section>

      <section class="cta-banner">
        <div class="container">
          <h2>Planning a similar facade?</h2>
          <p>Share your drawings for a structured quote from Shebi Enterprises.</p>
          <div class="cta-actions">
            <a href="/contact/" class="btn btn-primary">Get Free Quote</a>
            <a href="/portfolio/" class="btn btn-outline">More projects</a>
          </div>
        </div>
      </section>
    </main>

{footer_block}

    <script src="https://cdnjs.cloudflare.com/ajax/libs/aos/2.3.4/aos.js"></script>
    <script src="/js/main.js"></script>
    <script>
      AOS.init({{ duration: 700, easing: "ease-out-cubic", once: true, offset: 80 }});
    </script>
  </body>
</html>
'''
    out = ROOT / "projects" / slug
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(page, encoding="utf-8")
    redirect = f'''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8" /><meta name="robots" content="noindex" />
<link rel="canonical" href="{url}" />
<meta http-equiv="refresh" content="0; url=/projects/{slug}/" />
<title>Redirecting…</title>
<script>location.replace("/projects/{slug}/");</script>
</head><body><p>Redirecting to <a href="/projects/{slug}/">{esc(p['title'])}</a>…</p></body></html>
'''
    (ROOT / "projects" / f"{slug}.html").write_text(redirect, encoding="utf-8")
    print("project", slug)


def wire_portfolio():
    path = ROOT / "portfolio" / "index.html"
    text = path.read_text(encoding="utf-8")
    # Map label substrings / image paths to project slugs
    mappings = [
        ("Lodha", "lodha-residential"),
        ("ITC hotel Hyderabad", "itc-hotel-hyderabad"),
        ("ITC Hotel", "itc-hotel-hyderabad"),
        ("sunteck bandra", "sunteck-bandra"),
        ("Sunteck Bandra", "sunteck-bandra"),
        ("suraj estate", "suraj-estate"),
        ("Suraj Estate", "suraj-estate"),
        ("Orbit BKC", "orbit-bkc"),
        ("adani builder", "adani-bungalows"),
        ("Adani", "adani-bungalows"),
        ("american bank bkc", "american-bank-bkc"),
        ("American Bank", "american-bank-bkc"),
        ("granite cladding L", "lt-construction"),
        ("L &amp;T", "lt-construction"),
        ("L&amp;T", "lt-construction"),
        ("Reliance", "reliance-bkc"),
        ("Oberoi", "oberoi-commercial"),
        ("Piramal", "piramal-residential"),
        ("drywetino stone cladding Lodha", "lodha-residential"),
    ]

    # Replace "Request similar" CTA inside cards that match - inject View project link
    # Strategy: for each article.project-card, if content matches, change CTA
    def repl_card(m):
        block = m.group(0)
        slug = None
        for key, s in mappings:
            if key.lower() in block.lower():
                slug = s
                break
        if not slug:
            return block
        if f"/projects/{slug}/" in block:
            return block
        # Replace primary CTA
        new_cta = (
            f'<a href="/projects/{slug}/" class="btn btn-primary project-card-cta">View project</a>'
            f'<a href="/contact/" class="btn btn-outline project-card-cta" style="margin-left:8px">Request similar</a>'
        )
        block2 = re.sub(
            r'<a href="/contact/" class="btn btn-primary project-card-cta">Request similar</a>',
            new_cta,
            block,
            count=1,
        )
        return block2

    text2 = re.sub(r"<article class=\"project-card\">[\s\S]*?</article>", repl_card, text)
    path.write_text(text2, encoding="utf-8")
    print("portfolio wired")


def update_sitemap_llms():
    sm = ROOT / "sitemap.xml"
    text = sm.read_text(encoding="utf-8")
    for p in PROJECTS:
        url = f"{SITE}/projects/{p['slug']}/"
        if url not in text:
            entry = f"""  <url>
    <loc>{url}</loc>
    <lastmod>2026-11-16</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
"""
            text = text.replace("</urlset>", entry + "</urlset>")
    sm.write_text(text, encoding="utf-8")

    llms = ROOT / "llms.txt"
    lt = llms.read_text(encoding="utf-8")
    lines = ["## Projects", ""]
    for p in PROJECTS:
        lines.append(f"- [{p['title']}]({SITE}/projects/{p['slug']}/)")
    lines.append(f"- [Full portfolio]({SITE}/portfolio/)")
    block = "\n".join(lines) + "\n"
    if "## Projects" in lt:
        lt = re.sub(r"## Projects[\s\S]*?(?=\n## |\Z)", block, lt, count=1)
    else:
        lt += "\n" + block
    llms.write_text(lt, encoding="utf-8")
    print("sitemap/llms projects updated")


def main():
    header, footer_block = nav_footer_from_template()
    for p in PROJECTS:
        render_project(p, header, footer_block)
    wire_portfolio()
    update_sitemap_llms()
    print("DONE projects", len(PROJECTS))


if __name__ == "__main__":
    main()
