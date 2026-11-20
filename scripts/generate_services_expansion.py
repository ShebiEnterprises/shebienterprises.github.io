#!/usr/bin/env python3
"""Generate enriched SEO service pages (24), hub, nav/footer, sitemap, llms."""
from __future__ import annotations

import html
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://shebienterprises.com"
ASSETS = Path(
    "/Users/jetsoanalin/.cursor/projects/Users-jetsoanalin-Documents-Projects-Shebi-Enterprises-shebienterprises-github-io/assets"
)
IMG = ROOT / "img" / "services"
IMG.mkdir(parents=True, exist_ok=True)

GROUPS = [
    (
        "Cladding",
        [
            "stonewetcladding",
            "stonedrycladding",
            "acpcladding",
            "hpl-solid-aluminium-cladding",
            "grc-gfrc-decorative-facade",
            "open-joint-stone-rainscreen",
            "retrofit-recladding",
        ],
    ),
    (
        "Glazing",
        [
            "glazingwork",
            "unitised-curtain-wall",
            "structuralglass",
            "spiderglazing",
            "spandrel-shadow-box-glass",
            "aluminium-windows-doors",
            "balcony-terrace-glass-enclosures",
        ],
    ),
    (
        "Metalwork",
        [
            "fabricationwork",
            "aluminium-louvres-sunscreens",
            "entrance-portals-metalwork",
            "glass-railings-balustrades",
            "canopy-dropoff-packages",
            "skylights-canopies",
        ],
    ),
    (
        "Lifecycle",
        [
            "facade-maintenance",
            "sealant-joint-rehabilitation-amc",
            "facade-survey-leak-diagnosis",
            "acp-cladding-cleaning-restoration",
        ],
    ),
    (
        "Design-assist",
        [
            "facade-design-assist",
            "facade-mockups-sample-walls",
            "fire-rated-facade-systems",
        ],
    ),
]

# slug -> card image filename (under /img/services/)
CARD_IMG = {
    "stonewetcladding": "service-stone-wet-cladding.jpg",
    "stonedrycladding": "service-stone-dry-cladding.jpg",
    "acpcladding": "service-acp-cladding.jpg",
    "glazingwork": "service-glazing-works.jpg",
    "structuralglass": "service-structural-glass.jpg",
    "fabricationwork": "service-fabrication-works.jpg",
    "spiderglazing": "service-spider-glazing.jpg",
    "skylights-canopies": "service-skylights-canopies.jpg",
    "facade-maintenance": "service-facade-maintenance.jpg",
    "aluminium-louvres-sunscreens": "service-aluminium-louvres-sunscreens.jpg",
    "hpl-solid-aluminium-cladding": "service-hpl-solid-aluminium-cladding.jpg",
    "grc-gfrc-decorative-facade": "service-grc-gfrc-decorative-facade.jpg",
    "retrofit-recladding": "service-retrofit-recladding.jpg",
    "glass-railings-balustrades": "service-glass-railings-balustrades.jpg",
    "entrance-portals-metalwork": "service-entrance-portals-metalwork.jpg",
    "sealant-joint-rehabilitation-amc": "service-sealant-joint-rehabilitation-amc.jpg",
    "unitised-curtain-wall": "service-unitised-curtain-wall.jpg",
    "open-joint-stone-rainscreen": "service-open-joint-stone-rainscreen.jpg",
    "spandrel-shadow-box-glass": "service-spandrel-shadow-box-glass.jpg",
    "canopy-dropoff-packages": "service-canopy-dropoff-packages.jpg",
    "facade-survey-leak-diagnosis": "service-facade-survey-leak-diagnosis.jpg",
    "facade-design-assist": "service-facade-design-assist.jpg",
    "facade-mockups-sample-walls": "service-facade-mockups-sample-walls.jpg",
    "fire-rated-facade-systems": "service-fire-rated-facade-systems.jpg",
    "aluminium-windows-doors": "service-aluminium-windows-doors.jpg",
    "balcony-terrace-glass-enclosures": "service-balcony-terrace-glass-enclosures.jpg",
    "acp-cladding-cleaning-restoration": "service-acp-cladding-cleaning-restoration.jpg",
}

DETAIL_BY_GROUP = {
    "Cladding": ("service-detail-stone.jpg", "service-detail-install.jpg"),
    "Glazing": ("service-detail-glass.jpg", "service-detail-install.jpg"),
    "Metalwork": ("service-detail-metal.jpg", "service-detail-install.jpg"),
    "Lifecycle": ("service-sealant-joint-rehabilitation-amc.jpg", "service-detail-install.jpg"),
    "Design-assist": ("service-facade-mockups-sample-walls.jpg", "service-detail-metal.jpg"),
}

PROJECTS = [
    ("/projects/lodha-residential/", "Lodha Residential", "/img/works/drywetino%20stone%20cladding%20Lodha%20Project.jpg", "Stone & cladding"),
    ("/projects/itc-hotel-hyderabad/", "ITC Hotel Hyderabad", "/img/works/ITC%20hotel%20Hyderabad.jpg", "Hospitality facade"),
    ("/projects/reliance-bkc/", "Reliance BKC", "/img/works/IMG20180216114240.jpg", "Commercial envelope"),
    ("/projects/lt-construction/", "L&T Construction", "/img/works/granite%20cladding%20L%20%26T%20Project.jpg", "Granite cladding"),
    ("/projects/oberoi-commercial/", "Oberoi Commercial", "/img/works/IMG20170911113814.jpg", "Commercial facade"),
    ("/projects/piramal-residential/", "Piramal Residential", "/img/works/IMG20170222134133.jpg", "Residential cladding"),
    ("/projects/sunteck-bandra/", "Sunteck Bandra", "/img/works/sunteck%20bandra.jpg", "Facade works"),
    ("/projects/suraj-estate/", "Suraj Estate", "/img/works/suraj%20estate%201.jpg", "Facade works"),
    ("/projects/orbit-bkc/", "Orbit BKC", "/img/works/Orbit%20BKC.jpg", "Facade works"),
]


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def group_of(slug: str) -> str:
    for g, slugs in GROUPS:
        if slug in slugs:
            return g
    return "Cladding"


# Compact service definitions: expand into full pages
# Fields: title, short, desc_meta, tagline, what (list paras), needs, caps, variants[(name,blurb)], materials[(name,blurb)], faqs[(q,a)], blogs[(href,title)], related_services[slugs], cta, cta_blog, projects idxs, usp_line
RAW: dict[str, dict] = {}


def S(slug, **kw):
    RAW[slug] = kw


S(
    "stonewetcladding",
    title="Stone Wet Cladding",
    short="wet stone cladding",
    desc_meta="Wet stone cladding contractors in Mumbai - mortar-fixed natural stone for podiums and feature walls by Shebi Enterprises.",
    tagline="Mortar-fixed natural stone for podiums, feature walls and prestige elevations across Mumbai.",
    what=[
        "Wet stone cladding beds natural stone onto a prepared RCC or masonry substrate with mortar, creating continuous feature walls and podium skins that read as solid architecture. It suits sculpted patterns, curved walls and drop-offs where dry-fix module grids feel too mechanical.",
        "Shebi Enterprises has delivered wet stone packages since 2005 for Mumbai developers who need predictable joint rhythm, monsoon-aware curing and clean interfaces with canopies, ACP and glass above.",
    ],
    needs=[
        "Approved stone samples, finish and joint width",
        "Elevations and typical wall sections with waterproofing notes",
        "Substrate readiness and curing windows in the programme",
        "Interface drawings where stone meets ACP, glass or canopy steel",
        "Access strategy (scaffold / BMU) and live-area constraints",
    ],
    caps=[
        "Podium, drop-off and feature-wall wet fixing",
        "Stone batch control and mock-up approval",
        "Movement and drainage coordination with waterproofing",
        "Transitions to dry stone, ACP and glazing",
        "Protection, cleaning and handover documentation",
    ],
    variants=[
        ("Granite wet cladding", "Dense stones for coastal humidity and traffic splash."),
        ("Marble / feature stone", "Selective use with sealing regimes for interiors or sheltered faces."),
        ("Patterned feature walls", "Custom joint layouts for lobbies and drop-offs."),
        ("Sculpted and curved walls", "Where wet bedding follows complex geometry."),
    ],
    materials=[
        ("Indian & imported granites", "Selected for absorption, finish and thickness."),
        ("Bedding mortars", "Matched to stone and site temperature."),
        ("Sealers & cleaners", "As approved for the specified finish."),
    ],
    faqs=[
        ("When is wet cladding better than dry?", "On sculpted podiums, complex patterns and many feature walls where mechanical anchors are less practical."),
        ("What drawings do you need to quote?", "Elevations, sections, stone schedule and interface notes - see our contact form or email info@shebienterprises.com."),
        ("How do you manage monsoon curing?", "We programme protected curing windows and avoid rushing strike times for photo deadlines."),
        ("Can wet stone meet ACP above?", "Yes - with a designed transition flashing and joint philosophy."),
        ("Do you supply stone?", "We can supply or install free-issue stone as tendered."),
    ],
    blogs=[
        ("/blog/stone-cladding-cost-mumbai/", "Stone Cladding Cost in Mumbai"),
        ("/blog/wet-stone-cladding-process/", "Wet Stone Cladding Process"),
        ("/blog/waterproofing-before-cladding/", "Waterproofing Before Cladding"),
    ],
    related=["stonedrycladding", "canopy-dropoff-packages", "retrofit-recladding"],
    cta="Specify wet stone with confidence",
    cta_sub="Share elevations for a buildable estimate.",
    usp="Wet stone crews who understand Mumbai curing and height safety.",
    card_blurb="Mortar-fixed natural stone for podiums, feature walls and facades.",
)

S(
    "stonedrycladding",
    title="Stone Dry Cladding",
    short="dry stone cladding",
    desc_meta="Dry stone cladding contractors in Mumbai - mechanically anchored stone rainscreens by Shebi Enterprises.",
    tagline="Mechanically anchored stone for high-rise wind loads, serviceability and selective panel replacement.",
    what=[
        "Dry stone cladding uses stainless anchors and subframes to carry stone weight and wind loads into the structure. Open or sealed joints, cavity drainage and kerf quality decide long-term performance on Mumbai towers.",
        "Our teams install dry systems on podiums and typical floors where engineers demand replaceable panels and documented fixing.",
    ],
    needs=[
        "Stone engineering drawings and anchor schedule",
        "Wind criteria and panel size / thickness assumptions",
        "Open-joint vs sealed joint decision",
        "Survey of structure / embed plates",
        "Access and crane or BMU constraints",
    ],
    caps=[
        "Kerf cutting coordination and stainless anchors",
        "Open-joint rainscreen and sealed elevations",
        "High-rise wind-load installations",
        "Selective panel replacement strategies",
        "Interface flashings with ACP and glass",
    ],
    variants=[
        ("Open-joint rainscreen", "Shadow gaps with drained cavities."),
        ("Sealed dry stone", "Weathered silicone lines where specified."),
        ("Large-format panels", "Engineered thickness and fixing centres."),
        ("Podium feature bands", "Heavier pieces at drop-offs."),
    ],
    materials=[
        ("Granite & engineered stone", "Per approved samples."),
        ("SS 304 / 316 anchors", "Coastal exposure often prefers 316."),
        ("Aluminium / MS subframes", "Coated for exposure."),
    ],
    faqs=[
        ("SS 304 or 316?", "Coastal Mumbai often prefers 316 - confirm with the specifier."),
        ("Can we replace one panel?", "Dry systems are designed for selective replacement when layouts are documented."),
        ("Do you engineer anchors?", "We install to approved drawings; PE design sits with your consultant unless appointed for design-assist."),
        ("Open joints - do they leak more?", "Not if the rainscreen cavity and flashings are engineered correctly."),
        ("Lead time for stone?", "Factory cutting and logistics often need months - lock samples early."),
    ],
    blogs=[
        ("/blog/dry-stone-cladding-anchors/", "Dry Stone Cladding Anchors"),
        ("/blog/open-joint-stone-facade/", "Open Joint Stone Facades"),
        ("/blog/stone-cladding-cost-mumbai/", "Stone Cladding Cost"),
    ],
    related=["stonewetcladding", "open-joint-stone-rainscreen", "fabricationwork"],
    cta="Anchor stone the right way",
    cta_sub="Send drawings for a dry cladding package review.",
    usp="Mechanical stone fixing with monsoon-aware cavity detailing.",
    card_blurb="Mechanically anchored stone for high-rise wind loads and serviceability.",
)

S(
    "acpcladding",
    title="ACP Cladding",
    short="ACP cladding",
    desc_meta="ACP cladding contractors in Mumbai - FR and standard aluminium composite panels by Shebi Enterprises.",
    tagline="Lightweight composite panels for contemporary towers - standard, FR and premium finishes.",
    what=[
        "Aluminium Composite Panel (ACP) cladding is the most widely specified modern facade finish in India. Two aluminium skins bonded to a polyethylene or mineral core deliver colour range, speed and manageable weight on tall elevations.",
        "Shebi Enterprises installs branded systems with fire classification where NBC and local authorities demand FR cores, plus flashings, joints and colour control across lots.",
    ],
    needs=[
        "Elevations, typical details and fire strategy extracts",
        "Brand / core grade list (FR vs standard)",
        "Colour schedule per elevation face",
        "Interface drawings at stone, glass and canopy junctions",
        "Access, crane and night-work constraints",
    ],
    caps=[
        "Grid layout and expansion joint planning",
        "FR-grade and standard ACP systems",
        "Flashings, copings and sealant geometry",
        "Colour-matched trims and soffits",
        "Retrofit recladding on existing buildings",
    ],
    variants=[
        ("Standard ACP", "Cost-effective for many mid-rise packages."),
        ("FR (fire retardant) grade", "High-rise and assembly occupancy zones."),
        ("Metallic & solid colours", "Lot-matched for whole faces."),
        ("Wood, stone & digital print", "Feature bands and podiums."),
    ],
    materials=[
        ("Specifier brand lists", "Alucobond-class and approved equivalents."),
        ("Subframes & brackets", "Fabricated to survey."),
        ("Weathering silicones", "Compatible with coatings."),
    ],
    faqs=[
        ("Is FR ACP mandatory?", "Many high-rise and assembly occupancies require FR core; we confirm with your architect and approvals."),
        ("How do you handle panel replacement?", "Accessible fixing and recorded layouts speed swaps after damage."),
        ("What brands do you recommend?", "We match the specifier list and can propose VE equivalents with written approval."),
        ("How wide should joints be?", "Follow system design and thermal movement - keep visual widths consistent."),
        ("Lead time?", "Special colours and FR stock need early booking."),
    ],
    blogs=[
        ("/blog/acp-cladding-contractors-mumbai/", "ACP Cladding Contractors in Mumbai"),
        ("/blog/fire-rated-acp-high-rise-india/", "Fire-Rated ACP for High-Rise"),
        ("/blog/acp-cladding-price-mumbai/", "ACP Price Guide"),
        ("/blog/acp-vs-hpl-vs-solid-aluminium/", "ACP vs HPL vs Solid Aluminium"),
    ],
    related=["fire-rated-facade-systems", "hpl-solid-aluminium-cladding", "retrofit-recladding"],
    cta="Upgrade your elevation with ACP",
    cta_sub="Share drawings for a structured estimate and timeline.",
    usp="FR-aware ACP packages with lot-matched colour control.",
    card_blurb="FR and standard ACP in metallic, solid, wood and digital print finishes.",
)

# Continue remaining services in a second write via exec append - keep file growing
# Glazing and rest defined below for completeness

S(
    "glazingwork",
    title="Glazing Works",
    short="curtain wall and glazing",
    desc_meta="Curtain wall and glazing contractors in Mumbai - stick, semi-unitised and envelope glazing by Shebi Enterprises.",
    tagline="Curtain wall, stick and unitised-ready envelopes for Mumbai wind and monsoon exposure.",
    what=[
        "Glazing works cover stick curtain wall, semi-unitised systems, windows and envelope glass that define the thermal and visual performance of a tower. Correct survey, shim discipline and sealant adhesion decide whether the elevation stays dry through monsoon.",
        "We coordinate glass procurement, aluminium systems and interfaces with stone and ACP so the building reads as one envelope.",
    ],
    needs=[
        "Elevations, typical mullion details and glass schedule",
        "Wind criteria and performance specs",
        "Vision vs spandrel coordination",
        "Free-issue vs contractor glass decision",
        "Crane, hoist and night permit assumptions",
    ],
    caps=[
        "Stick and hybrid curtain wall install",
        "IGU coordination for hot climates",
        "Spandrel and vision alignment",
        "Site adhesion and water tests",
        "Interface flashings with cladding",
    ],
    variants=[
        ("Stick curtain wall", "Podiums, renovations and irregular geometry."),
        ("Semi-unitised", "Factory prep with site assembly."),
        ("Unitised packages", "See our unitised curtain wall service."),
        ("Partitions & decorative glass", "Interior and lobby packages."),
    ],
    materials=[
        ("Aluminium systems", "Thermal break where specified."),
        ("IGU / toughened / laminated", "Per engineering."),
        ("Structural & weathering silicones", "Mock-up tested."),
    ],
    faqs=[
        ("Stick or unitised?", "Repetitive towers often favour unitised; irregular podiums may stay stick."),
        ("Who buys glass?", "State free-issue vs contractor supply in tender."),
        ("Do you mock up?", "Yes - typical joint, corner and support conditions."),
        ("Monsoon installation?", "Possible with protection and sequenced elevations."),
        ("Spandrel colour mismatch?", "Approve vision and spandrel together under real sky."),
    ],
    blogs=[
        ("/blog/curtain-wall-contractors-mumbai/", "Curtain Wall Contractors Mumbai"),
        ("/blog/unitised-curtain-wall-mumbai/", "Unitised Curtain Wall Mumbai"),
        ("/blog/wind-load-mumbai-glazing/", "Wind Load Basics"),
    ],
    related=["unitised-curtain-wall", "structuralglass", "spandrel-shadow-box-glass"],
    cta="Glaze for Mumbai wind",
    cta_sub="Send the glazing package for a buildable quote.",
    usp="Envelope glazing with monsoon sequencing and site QA.",
    card_blurb="Curtain wall, stick and unitised systems, semi-structural and double-skin envelope glazing.",
)

S(
    "structuralglass",
    title="Structural Glass",
    short="structural glass",
    desc_meta="Structural glass contractors in Mumbai - silicone-bonded fins and walls by Shebi Enterprises.",
    tagline="Silicone-bonded glass fins and walls for lobbies, atriums and flagship retail.",
    what=[
        "Structural glass systems use glass as a load-bearing or fin-supported element with structural silicone bonding. Mock-ups, adhesion tests and cure records are non-negotiable before mass bonding.",
        "We deliver lobby and atrium packages where transparency and reflection quality matter as much as strength.",
    ],
    needs=[
        "Structural glass engineering and silicone specs",
        "Glass thickness, heat soak and laminate strategy",
        "Mock-up pass/fail criteria",
        "Site dust and humidity programme constraints",
        "Maintenance access for future inspection",
    ],
    caps=[
        "Fin walls and silicone-bonded facades",
        "Adhesion and compatibility testing",
        "Lobby and atrium installs",
        "Coordination with spider and point-fixed zones",
        "Handover cure records",
    ],
    variants=[
        ("Glass fin walls", "Lobby and atrium transparency."),
        ("Structural silicone glazing", "Bonded vision systems."),
        ("Hybrid with spider fittings", "Point-fixed feature zones."),
        ("Overhead laminated strategies", "Where safety glass is required."),
    ],
    materials=[
        ("Toughened / heat-soaked glass", "Per engineering."),
        ("Structural silicones", "Brand-locked after mock-up."),
        ("Stainless hardware", "Coastal grades as specified."),
    ],
    faqs=[
        ("How large should the mock-up be?", "Large enough for a typical joint, corner and support."),
        ("Can we skip heat soak?", "Only if the glass specification allows - document it."),
        ("Who stores cure records?", "Keep them with as-builts for warranty."),
        ("Indoor bonding conditions?", "Dust and humidity windows affect cure - we programme accordingly."),
        ("Maintenance?", "Document torque and glass marks at handover."),
    ],
    blogs=[
        ("/blog/structural-glazing-mumbai/", "Structural Glazing Mumbai"),
        ("/blog/structural-silicone-glazing-mockups/", "Structural Silicone Mock-ups"),
        ("/blog/structural-vs-semi-unitised-glazing/", "Structural vs Semi-Unitised"),
    ],
    related=["spiderglazing", "glazingwork", "facade-mockups-sample-walls"],
    cta="Bond glass with proven mock-ups",
    cta_sub="Share structural glass drawings for review.",
    usp="Structural silicone discipline from mock-up to cure records.",
    card_blurb="Silicone-bonded glass fins and walls for lobbies and flagship retail.",
)

S(
    "fabricationwork",
    title="Fabrication Works",
    short="metal fabrication",
    desc_meta="Facade fabrication works in Mumbai - MS, SS and aluminium brackets, canopies and subframes by Shebi Enterprises.",
    tagline="Precision metal fabrication for subframes, canopies, portals and balustrades.",
    what=[
        "Facade performance fails when brackets and subframes are out of tolerance. Our fabrication works produce MS, SS and aluminium components with coatings matched to coastal exposure and surveyed hole positions.",
        "From canopy steel to ACP brackets, fabrication is the backbone of every envelope package we install.",
    ],
    needs=[
        "Approved shop drawings and material grades",
        "Coating specification (galvanise / powder / paint)",
        "Site survey before final hole cutting",
        "Delivery and staging plan",
        "Interface with free-issue glass or stone",
    ],
    caps=[
        "Bracket and subframe fabrication",
        "Canopy and portal steelwork",
        "Balustrade and railing frames",
        "Tolerance control and jigs",
        "Site survey feedback loops",
    ],
    variants=[
        ("ACP / stone subframes", "Grid accuracy for cladding lines."),
        ("Canopy frames", "Steel or aluminium spans."),
        ("Entrance portals", "Feature metalwork packages."),
        ("Balustrade frames", "Glass railing support."),
    ],
    materials=[
        ("MS / SS / aluminium", "Per exposure and load."),
        ("Powder coat & galvanising", "Matched to contact metals."),
        ("Fasteners", "Isolation washers where required."),
    ],
    faqs=[
        ("What tolerance is typical?", "Project-specific - follow approved drawings and system manuals."),
        ("Can we shim forever?", "Excessive shimming hides survey problems - fix the grid."),
        ("Galvanising vs powder coat?", "Match exposure and dissimilar metal contact."),
        ("Do you install what you fabricate?", "Yes - fabrication and site teams stay coordinated."),
        ("Lead time?", "Depends on tonnage and coating slots."),
    ],
    blogs=[
        ("/blog/facade-bracket-fabrication-tolerances/", "Bracket Fabrication Tolerances"),
        ("/blog/entrance-canopy-steel-vs-aluminium/", "Canopy Steel vs Aluminium"),
        ("/blog/canopy-anchorage-rcc/", "Canopy Anchorage to RCC"),
    ],
    related=["entrance-portals-metalwork", "canopy-dropoff-packages", "aluminium-louvres-sunscreens"],
    cta="Fabricate to survey, not guesswork",
    cta_sub="Send shop drawings for fabrication planning.",
    usp="In-house facade metalwork tied to site survey.",
    card_blurb="MS, SS and aluminium structures, canopies and balustrades.",
)

S(
    "spiderglazing",
    title="Spider Glazing",
    short="spider glazing",
    desc_meta="Spider glazing contractors in Mumbai - point-fixed all-glass facades by Shebi Enterprises.",
    tagline="Point-supported all-glass walls for maximum lobby and atrium transparency.",
    what=[
        "Spider glazing uses stainless point fittings to support glass with minimal framing, delivering the clear lobby look clients expect on premium towers. Hardware grade, hole quality and fin or cable design control safety and reflection quality.",
        "We install spider systems for Mumbai lobbies with coastal-grade stainless and documented torque at handover.",
    ],
    needs=[
        "Point-fixed engineering and glass hole schedule",
        "Hardware grade (often SS 316 at coast)",
        "Fin / cable deflection limits",
        "Laminate strategy for overhead or high-risk zones",
        "Maintenance access notes",
    ],
    caps=[
        "Lobby and atrium spider walls",
        "Stainless spider fittings install",
        "Coordination with structural glass fins",
        "Edge distance and hole quality control",
        "Handover torque documentation",
    ],
    variants=[
        ("Four-arm spiders", "Classic lobby grids."),
        ("Fin-supported systems", "Larger spans."),
        ("Cable / rod systems", "Lightweight atriums."),
        ("Hybrid with silicone walls", "Feature zones."),
    ],
    materials=[
        ("Toughened / laminated glass", "Per engineering."),
        ("SS spider hardware", "Coastal grades."),
        ("Isolation washers", "Per manufacturer details."),
    ],
    faqs=[
        ("Can spider glass be overhead?", "Only with laminated safety strategies and engineered support."),
        ("Do spiders need isolation washers?", "Yes - follow manufacturer assembly details."),
        ("Typical glass?", "Toughened / heat-soaked with thickness from engineering."),
        ("Staining of fittings?", "Cheap hardware stains at the coast - specify grade early."),
        ("Maintenance?", "Inspect fittings and glass marks on AMC cycles."),
    ],
    blogs=[
        ("/blog/spider-glazing-lobbies-mumbai/", "Spider Glazing for Lobbies"),
        ("/blog/point-fixed-glass-hardware/", "Point-Fixed Glass Hardware"),
        ("/blog/office-lobby-glass-spec/", "Office Lobby Glass Spec"),
    ],
    related=["structuralglass", "glazingwork", "glass-railings-balustrades"],
    cta="Specify spider glazing that lasts at the coast",
    cta_sub="Share lobby drawings for a point-fixed package review.",
    usp="Coastal-grade spider hardware with lobby finish quality.",
    card_blurb="Point-supported all-glass walls for maximum transparency.",
)

S(
    "skylights-canopies",
    title="Skylights & Canopies",
    short="skylights and canopies",
    desc_meta="Skylight and glass canopy contractors in Mumbai - drainage-aware entrance canopies by Shebi Enterprises.",
    tagline="Daylighting and entrance canopies engineered for Mumbai wind and monsoon rain.",
    what=[
        "Skylights and glass canopies fail when treated like flat roofs. Falls, gutters, overflows and frame movement detailing keep water off occupied spaces below.",
        "We design and install canopy and skylight packages with fabrication and glazing under one responsibility matrix.",
    ],
    needs=[
        "Plan, section and drainage intent",
        "Glass safety strategy (typically laminated overhead)",
        "RCC anchorage and edge distances",
        "Frame material (steel vs aluminium)",
        "Cleaning and maintenance access",
    ],
    caps=[
        "Entrance canopy design-build",
        "Skylight drainage and condensation control",
        "Steel and aluminium frames",
        "RCC anchorage coordination",
        "Soffit cladding interfaces",
    ],
    variants=[
        ("Entrance canopies", "Drop-off weather protection."),
        ("Atrium skylights", "Daylighting with drains."),
        ("Walkway covers", "Link bridges and podiums."),
        ("Full drop-off packages", "See canopy & drop-off packages."),
    ],
    materials=[
        ("Laminated safety glass", "Overhead default."),
        ("MS / aluminium frames", "Corrosion protection as specified."),
        ("Gutters & sealants", "Sized for monsoon intensity."),
    ],
    faqs=[
        ("Laminated or toughened overhead?", "Overhead glass typically needs laminated safety strategies."),
        ("Can we retrofit drainage?", "Often yes after a survey."),
        ("Steel or aluminium frames?", "Spans and deflection decide - both can work at the coast with right coatings."),
        ("Night installation?", "Common in live drop-offs with permits."),
        ("Maintenance?", "Clogged drains recreate last year's leak - plan cleaning routes."),
    ],
    blogs=[
        ("/blog/glass-canopy-leak-mistakes/", "Glass Canopy Leak Mistakes"),
        ("/blog/skylight-drainage-condensation/", "Skylight Drainage"),
        ("/blog/canopy-anchorage-rcc/", "Canopy Anchorage"),
    ],
    related=["canopy-dropoff-packages", "fabricationwork", "entrance-portals-metalwork"],
    cta="Keep canopies dry through monsoon",
    cta_sub="Share canopy drawings for a drainage-aware quote.",
    usp="Canopy packages that treat drainage as primary structure.",
    card_blurb="Daylighting solutions and entrance canopies engineered for Mumbai wind.",
)

S(
    "facade-maintenance",
    title="Facade Maintenance",
    short="facade maintenance",
    desc_meta="Facade maintenance contractors in Mumbai - inspection, cleaning and sealant renewal by Shebi Enterprises.",
    tagline="Inspection, cleaning, sealant renewal and restorative repairs after handover.",
    what=[
        "Facades need planned maintenance: sealant life, drainage paths, glass and ACP cleaning, and post-monsoon leak response. Societies and facility teams that wait for visible failure pay more.",
        "Shebi Enterprises offers inspection-led maintenance with BMU or rope access methods matched to the building.",
    ],
    needs=[
        "As-built drawings or previous survey notes if available",
        "Access method (BMU tracks vs rope access)",
        "Known leak history and monsoon priority elevations",
        "Material brand preferences for sealant / glass",
        "Society or FM approval process",
    ],
    caps=[
        "Annual and monsoon inspections",
        "Sealant cut-out and renewal",
        "Glass and ACP cleaning cycles",
        "Emergency leak response",
        "Photo-documented reporting",
    ],
    variants=[
        ("Inspection AMC", "Scheduled surveys with reports."),
        ("Cleaning cycles", "BMU or rope access."),
        ("Sealant rehabilitation", "Focused joint programmes."),
        ("Restorative repairs", "Local panel and glass swaps."),
    ],
    materials=[
        ("Weathering silicones", "Compatible with existing systems."),
        ("Glass replacements", "Matched to original specs where possible."),
        ("ACP / stone spares", "From documented layouts."),
    ],
    faqs=[
        ("Monthly or yearly?", "High-rises often need scheduled inspections plus monsoon specials."),
        ("BMU or rope access?", "Depends on geometry and frequency - we advise after a site look."),
        ("Can societies phase towers?", "Yes - priority elevations first."),
        ("Do you inspect while cleaning?", "Yes - combine photo surveys with cleaning cycles."),
        ("Insurance documentation?", "We prepare dated survey notes suitable for PM files."),
    ],
    blogs=[
        ("/blog/facade-maintenance-guide/", "Facade Maintenance Guide"),
        ("/blog/facade-maintenance-contract-scope/", "Maintenance Contract Scope"),
        ("/blog/annual-facade-inspection-checklist/", "Annual Inspection Checklist"),
        ("/blog/rope-access-vs-bmu-facade-cleaning/", "Rope Access vs BMU"),
    ],
    related=["sealant-joint-rehabilitation-amc", "facade-survey-leak-diagnosis", "retrofit-recladding"],
    cta="Protect the envelope you already paid for",
    cta_sub="Book an inspection or AMC discussion.",
    usp="Maintenance led by facade installers, not generic cleaners only.",
    card_blurb="Inspection, cleaning, sealant renewal and restorative repairs post-handover.",
)

# --- Strong fit (7) ---
S(
    "aluminium-louvres-sunscreens",
    title="Aluminium Louvres & Sunscreens",
    short="aluminium louvres",
    desc_meta="Aluminium louvre and sunscreen contractors in Mumbai - facade-integrated sun control by Shebi Enterprises.",
    tagline="Facade-integrated aluminium louvres and sunscreens coordinated with ACP and glazing.",
    what=[
        "Aluminium louvres and sunscreens cut solar gain, add depth to elevations and conceal plant screens without looking like an afterthought. They must share subframe logic, movement joints and cleaning access with the cladding around them.",
        "We fabricate and install louvre blades and screens as part of hybrid ACP and glass envelopes.",
    ],
    needs=["Blade profile and pitch intent", "Structural loads and bracket locations", "Finish and colour match to ACP", "Access for cleaning", "Fire and smoke strategy notes if screening shafts"],
    caps=["Horizontal and vertical louvre banks", "Plant and AC screens", "Integration with ACP and curtain wall", "Powder-coated finishes", "Fabrication of brackets and frames"],
    variants=[("Aerofoil louvres", "Architectural sun control."), ("Z / C blade screens", "Plant concealment."), ("Operable screens", "Where specified."), ("Feature fins", "Vertical accent blades.")],
    materials=[("Extruded aluminium", "Alloy per spec."), ("Powder coat", "UV-stable colours."), ("SS fasteners", "Isolation as required.")],
    faqs=[
        ("Can louvres match ACP colour?", "Often yes with controlled powder-coat batches."),
        ("Do they need separate engineering?", "Yes - wind and self-weight into the structure."),
        ("Cleaning access?", "Design walkways or BMU reach at tender."),
        ("Noise / vibration?", "Detail fixings to avoid rattle in monsoon winds."),
        ("Lead time?", "Extrusion and coating slots need booking."),
    ],
    blogs=[("/blog/aluminium-louvre-cladding-integration/", "Aluminium Louvre Integration"), ("/blog/acp-cladding-contractors-mumbai/", "ACP Contractors")],
    related=["acpcladding", "fabricationwork", "glazingwork"],
    cta="Integrate louvres into the facade, not as a bolt-on",
    cta_sub="Share sunscreen drawings for a coordinated quote.",
    usp="Louvre packages tied to ACP and glazing interfaces.",
    card_blurb="Facade-integrated aluminium louvres, fins and plant screens.",
)

S(
    "hpl-solid-aluminium-cladding",
    title="HPL & Solid Aluminium Cladding",
    short="HPL and solid aluminium cladding",
    desc_meta="HPL and solid aluminium cladding in Mumbai - durable panel alternatives to ACP by Shebi Enterprises.",
    tagline="HPL and solid aluminium panel systems when the brief needs different fire or durability behaviour than ACP.",
    what=[
        "HPL and solid aluminium are specified when architects want different edge detailing, impact resistance or fire assemblies than standard ACP. They are heavier and need stronger subframes, but can be the right answer for feature bands and high-abuse zones.",
        "We help teams compare options against ACP and install to approved systems.",
    ],
    needs=["Panel brand and thickness", "Fire assembly certificates", "Subframe capacity check", "Joint and edge detailing", "Sample approval under site light"],
    caps=["HPL rainscreen install", "Solid aluminium cassette systems", "Subframe upgrades", "Transitions to ACP and stone", "Sample and mock-up walls"],
    variants=[("HPL rainscreen", "Open or sealed joints per system."), ("Solid aluminium cassettes", "Repairable metal faces."), ("Mixed elevations", "ACP + HPL/solid transitions."), ("Feature soffits", "Canopy and portal linings.")],
    materials=[("Specifier HPL brands", "Per fire docs."), ("Solid aluminium sheet", "Alloy and coating."), ("Heavier subframes", "Fabricated in-house.")],
    faqs=[
        ("Is HPL always safer than ACP?", "Not automatically - verify tested assemblies."),
        ("Why is solid aluminium costlier?", "Material weight, subframe and finish labour."),
        ("Can we mix with ACP?", "Yes with designed transitions."),
        ("Lead times?", "Often longer than commodity ACP."),
        ("Maintenance?", "Solid aluminium can be more repairable locally."),
    ],
    blogs=[("/blog/acp-vs-hpl-vs-solid-aluminium/", "ACP vs HPL vs Solid Aluminium"), ("/blog/fire-rated-acp-high-rise-india/", "FR ACP Guide")],
    related=["acpcladding", "fire-rated-facade-systems", "fabricationwork"],
    cta="Choose the panel system that matches the fire brief",
    cta_sub="Send the material schedule for a comparison install quote.",
    usp="Panel alternatives installed with the same site discipline as ACP.",
    card_blurb="HPL and solid aluminium systems for feature and high-performance zones.",
)

S(
    "grc-gfrc-decorative-facade",
    title="GRC / GFRC Decorative Facades",
    short="GRC decorative facade",
    desc_meta="GRC GFRC decorative facade contractors in Mumbai - ornamental panels with stone and cladding packages by Shebi Enterprises.",
    tagline="Decorative GRC / GFRC elements coordinated with stone and cladding on podiums and feature elevations.",
    what=[
        "GRC and GFRC deliver ornate or geometric facade elements that are difficult in natural stone alone. Weight, fixing and joint movement still need envelope thinking - not pure decoration.",
        "We coordinate GRC with stone wet/dry and ACP so junctions stay weather-tight.",
    ],
    needs=["GRC shop drawings and weights", "Fixing and embed details", "Finish samples", "Interface with stone/ACP", "Lifting and access plan"],
    caps=["Decorative podium panels", "Cornices and feature motifs", "Coordination with stone cladding", "Fixing and alignment QA", "Protection during finishing trades"],
    variants=[("Ornamental GRC", "Classical motifs."), ("Geometric GFRC", "Modern screens."), ("Painted finishes", "As specified."), ("Hybrid with stone", "Feature bands.")],
    materials=[("GRC / GFRC units", "From approved fabricators."), ("SS / MS fixings", "Per engineering."), ("Joint sealants", "Movement-capable.")],
    faqs=[
        ("Is GRC lighter than stone?", "Often yes - still needs engineered fixing."),
        ("Can it look like stone?", "Finishes vary - approve samples on site."),
        ("Who engineers fixings?", "Your consultant; we install to approved details."),
        ("Damage risk?", "Protect during subsequent trades."),
        ("Maintenance?", "Inspect joints and coatings on AMC cycles."),
    ],
    blogs=[("/blog/grc-vs-stone-decorative-facade/", "GRC vs Stone"), ("/blog/granite-cladding-podiums-mumbai/", "Granite Podiums")],
    related=["stonewetcladding", "stonedrycladding", "fabricationwork"],
    cta="Add decorative depth without losing weather performance",
    cta_sub="Share GRC drawings for a coordinated install quote.",
    usp="Decorative GRC tied into real cladding interfaces.",
    card_blurb="Decorative GRC / GFRC panels coordinated with stone and cladding.",
)

S(
    "retrofit-recladding",
    title="Retrofit & Recladding",
    short="facade retrofit recladding",
    desc_meta="Facade retrofit and recladding contractors in Mumbai - overclad and strip-and-reclad packages by Shebi Enterprises.",
    tagline="Overclad and reclad packages for ageing towers, societies and commercial upgrades.",
    what=[
        "Retrofit cladding upgrades tired elevations, improves weather performance and can address FR or maintenance issues without a full rebuild. Surveys of the existing structure, live-building constraints and phased access decide success.",
        "We deliver ACP, stone and hybrid retrofit packages for Mumbai societies and commercial owners.",
    ],
    needs=["Existing facade survey / photos", "Structural capacity notes if available", "Occupied-building work rules", "Phasing and noise constraints", "Target system (ACP / stone / hybrid)"],
    caps=["Strip-and-reclad programmes", "Overclad where structure allows", "Society-friendly phasing", "Sealant and drainage upgrades", "As-built documentation for handover"],
    variants=[("ACP reclad", "Fast visual upgrade."), ("Stone podium refresh", "Drop-off prestige."), ("Hybrid reclad", "Stone + ACP + glass interfaces."), ("Partial elevation pilots", "Prove quality before full tower.")],
    materials=[("FR ACP where required", "High-rise upgrades."), ("New subframes", "Surveyed to existing RCC."), ("Sealants & flashings", "Modern weather lines.")],
    faqs=[
        ("Can we reclad while occupied?", "Often yes with phasing, protection and permits."),
        ("Overclad or strip first?", "Depends on existing build-up and weight - survey decides."),
        ("Do societies need full drawings?", "Yes for tender-grade pricing - we can help scope."),
        ("Fire upgrades?", "FR strategy must be explicit on high-rises."),
        ("Warranty?", "Document existing conditions and new system limits clearly."),
    ],
    blogs=[("/blog/retrofit-cladding-existing-buildings/", "Retrofit Cladding"), ("/blog/facade-maintenance-guide/", "Maintenance Guide")],
    related=["acpcladding", "facade-maintenance", "facade-survey-leak-diagnosis"],
    cta="Refresh the elevation without guessing the build-up",
    cta_sub="Book a retrofit survey discussion.",
    usp="Reclad programmes run by teams who also build new envelopes.",
    card_blurb="Overclad and reclad packages for existing towers and societies.",
)

S(
    "glass-railings-balustrades",
    title="Glass Railings & Balustrades",
    short="glass railings balustrades",
    desc_meta="Glass railing and balustrade contractors in Mumbai - podium and terrace glazing by Shebi Enterprises.",
    tagline="Glass railings and balustrades for podiums, terraces and drop-offs with engineered fixing.",
    what=[
        "Glass balustrades combine safety loads with clean sightlines on podiums and terraces. Base channels, spigots or structural glass edges must be detailed for human impact and coastal corrosion.",
        "We fabricate and install railing packages alongside canopy and stone podium works.",
    ],
    needs=["Handrail / balustrade drawings", "Load and height requirements", "Glass type (toughened / laminated)", "Base fixing into RCC or steel", "Finish schedule for metal parts"],
    caps=["Spigot and channel systems", "Structural glass balustrades", "Podium and terrace installs", "SS / aluminium handrails", "Coordination with canopy drop-offs"],
    variants=[("Frameless glass", "Minimal metal."), ("Post and glass", "Classic decks."), ("Hybrid with steel handrail", "High-traffic zones."), ("Staircase balustrades", "Interior/exterior.")],
    materials=[("Toughened / laminated glass", "Per code and engineering."), ("SS 304 / 316", "Coastal preference."), ("Aluminium channels", "Powder coated.")],
    faqs=[
        ("Laminated or toughened?", "Many podium edges prefer laminated strategies - follow the specifier."),
        ("Can we match lobby spider glass?", "Hardware grades can align for a family look."),
        ("Corrosion at coast?", "Specify stainless grade and drainage at bases."),
        ("Retrofit on existing parapets?", "Survey edge distances and embeds first."),
        ("Lead time?", "Glass processing dominates the programme."),
    ],
    blogs=[("/blog/office-lobby-glass-spec/", "Lobby Glass Spec"), ("/blog/point-fixed-glass-hardware/", "Point-Fixed Hardware")],
    related=["fabricationwork", "spiderglazing", "canopy-dropoff-packages"],
    cta="Specify railings that survive coastal air",
    cta_sub="Share balustrade drawings for fabrication and install pricing.",
    usp="Glass railings fabricated and installed with facade-grade stainless.",
    card_blurb="Podium and terrace glass railings with engineered metalwork.",
)

S(
    "entrance-portals-metalwork",
    title="Entrance Portals & Feature Metalwork",
    short="entrance portals metalwork",
    desc_meta="Entrance portal and feature metalwork in Mumbai - steel and aluminium feature frames by Shebi Enterprises.",
    tagline="Entrance portals, feature frames and architectural metalwork for drop-offs and lobbies.",
    what=[
        "Entrance portals set the first impression of a development. Steel or aluminium frames, cladding wraps and lighting coordination must land true on survey and survive monsoon splash at the drop-off.",
        "Our fabrication and install teams deliver portals as part of canopy and podium packages.",
    ],
    needs=["Portal GA and connection details", "Cladding wrap material", "Lighting / signage interfaces", "RCC embeds", "Live drop-off work windows"],
    caps=["Feature portal frames", "Clad portal wraps (ACP / aluminium)", "Coordination with canopies", "Precision fabrication", "Night installs with permits"],
    variants=[("Steel portals", "Long spans."), ("Aluminium feature frames", "Lighter mid spans."), ("Clad portals", "ACP or solid aluminium skins."), ("Lobby portals", "Interior feature frames.")],
    materials=[("MS / aluminium", "Coatings for coast."), ("ACP / solid Al wraps", "As designed."), ("Fasteners & embeds", "Per structural notes.")],
    faqs=[
        ("Can portals include canopy loads?", "Sometimes - engineering must confirm."),
        ("Night work?", "Common for live lobbies."),
        ("Who owns cladding wrap?", "Often the same facade contractor - reduces interface risk."),
        ("Tolerance?", "Survey before final fabrication."),
        ("Maintenance?", "Inspect coatings and sealants annually."),
    ],
    blogs=[("/blog/entrance-canopy-steel-vs-aluminium/", "Canopy Frames"), ("/blog/hotel-facade-specs-hospitality/", "Hotel Facade Specs")],
    related=["fabricationwork", "canopy-dropoff-packages", "acpcladding"],
    cta="Make the entrance a designed package",
    cta_sub="Send portal drawings for fabrication planning.",
    usp="Feature metalwork built by the same team that clads the elevation.",
    card_blurb="Entrance portals and architectural metal frames for lobbies and drop-offs.",
)

S(
    "sealant-joint-rehabilitation-amc",
    title="Sealant & Joint Rehabilitation (AMC)",
    short="sealant joint rehabilitation",
    desc_meta="Facade sealant and joint rehabilitation AMC in Mumbai - cut-out and reseal programmes by Shebi Enterprises.",
    tagline="Focused sealant cut-out, joint redesign and AMC programmes for ageing envelopes.",
    what=[
        "Failed silicone is the most common monsoon complaint on glass and ACP towers. Cut-out, substrate prep and compatible reseal - not a thin smear over failed joints - restores the weather line.",
        "We run elevation-phased sealant AMCs for societies and commercial FM teams.",
    ],
    needs=["Leak map or elevation priorities", "Existing sealant brand if known", "Access method", "Occupied-floor constraints", "Colour match requirements"],
    caps=["Failed joint diagnosis", "Cut-out and reseal", "Compatible silicone selection", "Photo reports per elevation", "Tie-in to wider maintenance AMC"],
    variants=[("Monsoon special programmes", "Priority faces first."), ("Full-tower AMC", "Multi-year contracts."), ("ACP joint rehab", "Colour-matched sealants."), ("Glass curtain wall rehab", "Mullion and cap seals.")],
    materials=[("Weathering silicones", "Movement-capable."), ("Primers", "Per datasheet."), ("Backer rods", "Correct depth.")],
    faqs=[
        ("Why not just add more silicone?", "Over failed joints it peels - cut-out is required."),
        ("How long does silicone last?", "Depends on UV, movement and original install - inspections catch early failure."),
        ("Colour match?", "Select sealant colour; painting sealant usually fails."),
        ("Can this run under AMC?", "Yes - annual or monsoon-triggered."),
        ("Do you test adhesion?", "On critical elevations we sample before mass work."),
    ],
    blogs=[("/blog/facade-sealant-failure-repair/", "Sealant Failure Repair"), ("/blog/facade-leakage-after-monsoon/", "Leakage After Monsoon"), ("/blog/acp-joint-design-sealants/", "ACP Joint Sealants")],
    related=["facade-maintenance", "facade-survey-leak-diagnosis", "acpcladding"],
    cta="Fix the weather line, not just the stain",
    cta_sub="Request a sealant rehabilitation survey.",
    usp="Sealant programmes run by facade installers who know system joints.",
    card_blurb="Cut-out, reseal and joint AMC programmes for glass and ACP towers.",
)

# --- Good fit (5) ---
S(
    "unitised-curtain-wall",
    title="Unitised Curtain Wall",
    short="unitised curtain wall",
    desc_meta="Unitised curtain wall contractors in Mumbai - factory-sealed modules and logistics by Shebi Enterprises.",
    tagline="Factory-sealed unitised modules for repetitive towers with Mumbai logistics planning.",
    what=[
        "Unitised curtain wall improves quality control by sealing modules in the factory and hanging them on site. Crane windows, trailer access and staging yards decide whether oversized modules are realistic in dense Mumbai plots.",
        "We coordinate fabrication partners, glass procurement and site hang sequences with clear interface ownership.",
    ],
    needs=["Module grid and elevations", "Factory slot and glass lead times", "Crane / trailer access study", "Anchor and embed survey", "Stick vs unitised podium decision"],
    caps=["Unitised hang programmes", "Hybrid stick podium + unitised tower", "Logistics planning", "Interface detailing", "Site QA on hang days"],
    variants=[("Full unitised towers", "Repetitive grids."), ("Hybrid envelopes", "Stick podium + unitised typical floors."), ("Smaller modules", "Tight urban logistics."), ("Design-assist unitised", "Early engineering engagement.")],
    materials=[("Factory aluminium modules", "System brands as specified."), ("IGUs", "Locked early."), ("Anchors & brackets", "Surveyed.")],
    faqs=[
        ("Do unitised systems leak less?", "They reduce site silicone dependency for primary lines - interfaces still matter."),
        ("Lead time?", "Factory slots plus glass often need months."),
        ("Can we mix with stick?", "Yes - common on podium vs tower."),
        ("Night crane?", "Often required in dense plots."),
        ("Who owns PE?", "State clearly in tender."),
    ],
    blogs=[("/blog/unitised-curtain-wall-mumbai/", "Unitised Curtain Wall Mumbai"), ("/blog/structural-vs-semi-unitised-glazing/", "Structural vs Semi-Unitised"), ("/blog/facade-logistics-navi-mumbai-thane/", "Facade Logistics")],
    related=["glazingwork", "facade-design-assist", "fabricationwork"],
    cta="Plan unitised logistics before you freeze the grid",
    cta_sub="Share tower elevations for a unitised feasibility review.",
    usp="Unitised delivery with Mumbai crane and staging realism.",
    card_blurb="Factory-sealed unitised curtain wall with logistics-aware install.",
)

S(
    "open-joint-stone-rainscreen",
    title="Open-Joint Stone Rainscreen",
    short="open joint stone rainscreen",
    desc_meta="Open-joint stone rainscreen contractors in Mumbai - shadow-gap dry stone by Shebi Enterprises.",
    tagline="Shadow-gap open-joint stone rainscreens with drained, compartmented cavities.",
    what=[
        "Open-joint stone rainscreens create depth through shadow gaps while managing water in the cavity behind. They are not simply dry stone with missing sealant - membranes, weeps and compartmentation are part of the system.",
        "We install open-joint packages as a premium dry stone offering for commercial and residential towers.",
    ],
    needs=["Open-joint design intent", "Cavity drainage and membrane notes", "Anchor engineering", "Panel size and thickness", "Maintenance inspection access"],
    caps=["Shadow-gap dry stone", "Cavity drainage detailing", "Stainless anchor install", "Interface with sealed zones", "Annual inspection support"],
    variants=[("Full open-joint faces", "Architectural rainscreens."), ("Mixed sealed / open", "Feature bands only."), ("Large-format panels", "Engineered fixings."), ("Podium rainscreens", "Impact-aware thicknesses.")],
    materials=[("Granite / engineered stone", "Approved samples."), ("SS anchors", "Coastal grades."), ("Membranes & flashings", "Cavity management.")],
    faqs=[
        ("Do open joints leak more?", "Not if the rainscreen is engineered correctly."),
        ("Bird / insect screens?", "Detail mesh at vents where required."),
        ("Sealed look instead?", "Possible - but design as a sealed system, not a rainscreen."),
        ("Movement joints?", "Still required - rainscreen gaps are not always movement joints."),
        ("Cleaning?", "Plan access without forcing closed-joint habits."),
    ],
    blogs=[("/blog/open-joint-stone-facade/", "Open Joint Stone"), ("/blog/dry-stone-cladding-anchors/", "Dry Stone Anchors"), ("/blog/movement-joints-stone-acp/", "Movement Joints")],
    related=["stonedrycladding", "stonewetcladding", "movement-joints-stone-acp"],
    cta="Specify shadow gaps with real cavity design",
    cta_sub="Send open-joint details for an install review.",
    usp="Open-joint stone with rainscreen thinking, not missing sealant.",
    card_blurb="Shadow-gap open-joint stone rainscreens with drained cavities.",
)

# fix related that pointed to blog slug - use real services only
RAW["open-joint-stone-rainscreen"]["related"] = ["stonedrycladding", "stonewetcladding", "facade-maintenance"]

S(
    "spandrel-shadow-box-glass",
    title="Spandrel & Shadow-Box Glass",
    short="spandrel and shadow box glass",
    desc_meta="Spandrel and shadow-box glass coordination in Mumbai - vision and opaque bands by Shebi Enterprises.",
    tagline="Vision and spandrel coordination so office towers avoid checkerboard elevations.",
    what=[
        "Spandrel and shadow-box glass hide slab edges and services while vision glass admits light. Mismatched coatings create checkerboard elevations that no amount of cleaning will fix.",
        "We coordinate glass procurement, frits and shadow-box depth with the curtain wall package.",
    ],
    needs=["Vision and spandrel glass schedule", "Coating / frit intent", "Shadow-box depth", "Mock-up under real sky", "Thermal and privacy targets"],
    caps=["Spandrel glass install", "Shadow-box assemblies", "Vision/spandrel mock-ups", "Curtain wall coordination", "Replacement logistics"],
    variants=[("Opaque spandrel IGU", "Standard office towers."), ("Ceramic frit", "Privacy and solar control."), ("Shadow boxes", "Depth-driven colour."), ("Metal back pans", "Where specified.")],
    materials=[("Coated IGUs", "Hot-climate performance."), ("Fritted glass", "As designed."), ("Insulation / pans", "Shadow-box build-ups.")],
    faqs=[
        ("Can frit replace spandrel?", "Sometimes - confirm privacy and thermal needs."),
        ("Why mock up outdoors?", "Lab booths miss real sky reflection."),
        ("Who buys glass?", "State free-issue vs contractor supply."),
        ("Colour change over time?", "Coatings and lot control matter - lock early."),
        ("Repair strategy?", "Document glass marks and spares."),
    ],
    blogs=[("/blog/spandrel-vision-glass-coordination/", "Spandrel & Vision Coordination"), ("/blog/igu-double-glazing-hot-climate/", "IGU Hot Climate")],
    related=["glazingwork", "unitised-curtain-wall", "structuralglass"],
    cta="Align vision and spandrel before glass is ordered",
    cta_sub="Share the glass schedule for coordination review.",
    usp="Spandrel coordination that protects the elevation's first impression.",
    card_blurb="Vision and spandrel / shadow-box glass coordination for office towers.",
)

S(
    "canopy-dropoff-packages",
    title="Entrance Canopy & Drop-off Packages",
    short="canopy drop-off package",
    desc_meta="Entrance canopy and drop-off packages in Mumbai - steel, glass, stone and ACP soffits by Shebi Enterprises.",
    tagline="Single-responsibility drop-off packages: structure, glass, drainage and podium cladding interfaces.",
    what=[
        "Drop-offs fail when steel, glass, stone and ACP each arrive as separate claims. A canopy & drop-off package puts drainage, anchorage, soffit cladding and podium stone under one sequence.",
        "Ideal for residential and hospitality projects where the first 20 metres of arrival matter.",
    ],
    needs=["Canopy GA and drainage", "Podium stone / ACP finishes", "Lighting and signage interfaces", "Live traffic management plan", "Anchorage into RCC"],
    caps=["Steel / aluminium canopy frames", "Laminated glass roofs", "Stone / ACP soffits and columns", "Drainage and overflows", "Night install sequencing"],
    variants=[("Glass canopy packages", "Transparent arrival."), ("Clad canopy packages", "ACP / aluminium soffits."), ("Hospitality drop-offs", "Hotel porte-cochere."), ("Residential drop-offs", "Tower arrival courts.")],
    materials=[("Structural steel / aluminium", "Coatings for coast."), ("Laminated glass", "Overhead safety."), ("Stone / ACP", "Podium finishes.")],
    faqs=[
        ("Why a package vs separate trades?", "Interfaces cause most leaks and claims."),
        ("Can you work at night?", "Yes with permits."),
        ("Stone columns included?", "Often - scope explicitly."),
        ("Who designs drainage?", "We implement approved drainage; design-assist available."),
        ("Maintenance?", "Include gutter cleaning in handover."),
    ],
    blogs=[("/blog/glass-canopy-leak-mistakes/", "Canopy Leak Mistakes"), ("/blog/residential-podium-cladding/", "Residential Podium Cladding"), ("/blog/hotel-facade-specs-hospitality/", "Hotel Facade Specs")],
    related=["skylights-canopies", "stonewetcladding", "entrance-portals-metalwork"],
    cta="Deliver the arrival experience as one package",
    cta_sub="Share drop-off drawings for a combined quote.",
    usp="Drop-offs where structure, glass and cladding share one programme.",
    card_blurb="Full canopy and drop-off packages with stone, ACP and glass interfaces.",
)

S(
    "facade-survey-leak-diagnosis",
    title="Facade Survey & Leak Diagnosis",
    short="facade survey leak diagnosis",
    desc_meta="Facade survey and leak diagnosis in Mumbai - monsoon leak mapping by Shebi Enterprises.",
    tagline="Photo-documented facade surveys and leak diagnosis that feed repair scopes.",
    what=[
        "Guessing the leak source wastes silicone and scaffold money. Pattern mapping against wind direction, joint lines and interfaces finds whether you have sealant failure, blocked weeps or condensation.",
        "Our surveys produce actionable notes for societies, PMs and insurers - then feed maintenance or retrofit packages.",
    ],
    needs=["Building access permissions", "Known wet patch locations", "As-builts if available", "Preferred access method", "Reporting format needs"],
    caps=["Visual and photo surveys", "Leak pattern mapping", "Hose-pack retests after repair", "BMU / rope access surveys", "Repair scope recommendations"],
    variants=[("Monsoon post-storm surveys", "Priority response."), ("Pre-purchase surveys", "Asset due diligence."), ("AMC baseline surveys", "Year-zero documentation."), ("High-rise BMU surveys", "Track-equipped towers.")],
    materials=[("Survey tools & cameras", "Documented elevations."), ("Compatible sealants", "For follow-on repairs."), ("Temporary protections", "As needed.")],
    faqs=[
        ("Can you diagnose without full scaffold?", "Often yes via BMU or rope access; complex cavities may need local opening."),
        ("Will insurance need documentation?", "We prepare dated photos and notes suitable for claims files."),
        ("Do surveys include quotes?", "We can attach a repair estimate after diagnosis."),
        ("Condensation vs leak?", "We separate internal moisture patterns from weather leaks."),
        ("How fast after monsoon?", "Book early - queues build after heavy spells."),
    ],
    blogs=[("/blog/facade-leakage-after-monsoon/", "Leakage After Monsoon"), ("/blog/facade-sealant-failure-repair/", "Sealant Failure"), ("/blog/annual-facade-inspection-checklist/", "Inspection Checklist")],
    related=["sealant-joint-rehabilitation-amc", "facade-maintenance", "retrofit-recladding"],
    cta="Diagnose before you reseal the whole elevation",
    cta_sub="Request a facade survey slot.",
    usp="Leak diagnosis by teams who also repair and reclad.",
    card_blurb="Photo-documented surveys and monsoon leak diagnosis for towers and societies.",
)

# --- Stretch (3) ---
S(
    "facade-design-assist",
    title="Facade Design-Assist",
    short="facade design assist",
    desc_meta="Facade design-assist in Mumbai - buildable detailing and shop-drawing support by Shebi Enterprises.",
    tagline="Early design-assist so tenders reflect buildable Mumbai site practice.",
    what=[
        "Design-assist sits between architect intent and contractor execution: interface matrices, typical details, BOQ language and logistics reality. It reduces VE churn and claims once the job is live.",
        "Shebi Enterprises supports developers and architects with practical envelope detailing - PE stamping remains with your appointed engineer unless separately contracted.",
    ],
    needs=["Concept elevations", "Performance targets", "Fire strategy extracts", "Programme and logistics constraints", "Clarity on PE responsibility"],
    caps=["Interface matrices", "Typical detail workshops", "Tender BOQ language review", "Mock-up planning", "Logistics feasibility notes"],
    variants=[("Pre-tender design-assist", "Before floating rates."), ("Post-award detailing", "Shop-drawing support."), ("Hybrid system advice", "Stone + ACP + glass."), ("Hospitality drop-off packages", "Arrival sequencing.")],
    materials=[("Sample boards", "As required."), ("Reference system data", "Manufacturer inputs."), ("Draft details", "For consultant approval.")],
    faqs=[
        ("Are you the PE?", "Design-assist supports buildability; structural/facade PE remains as appointed unless scoped otherwise."),
        ("When to engage?", "Before tender freeze is ideal."),
        ("Does it delay design?", "It usually saves time by preventing rework."),
        ("Can you write BOQ headings?", "We review language against site practice."),
        ("Fee model?", "Discuss via contact - often tied to package size."),
    ],
    blogs=[("/blog/how-to-tender-facade-packages/", "How to Tender Facade Packages"), ("/blog/facade-quote-documents-mumbai/", "Documents for a Quote"), ("/blog/choose-glazing-contractor-questions/", "Questions for Glazing Contractors")],
    related=["facade-mockups-sample-walls", "unitised-curtain-wall", "hybrid-facade-stone-acp-glass"],
    cta="Make the tender buildable before rates go out",
    cta_sub="Book a design-assist conversation.",
    usp="Design-assist grounded in two decades of Mumbai site delivery.",
    card_blurb="Buildable detailing, interface matrices and tender support for facade packages.",
)
RAW["facade-design-assist"]["related"] = ["facade-mockups-sample-walls", "unitised-curtain-wall", "acpcladding"]

S(
    "facade-mockups-sample-walls",
    title="Facade Mock-ups & Sample Walls",
    short="facade mock-ups",
    desc_meta="Facade mock-up and sample wall contractors in Mumbai - visual and performance mock-ups by Shebi Enterprises.",
    tagline="On-structure and sample-bay mock-ups that freeze aesthetics and performance before mass production.",
    what=[
        "Mock-ups prove colour, joint rhythm, anchors and water performance before thousands of square metres are committed. Write pass/fail criteria before building the bay.",
        "We build mock-ups for ACP, stone, silicone bonding and hybrid transitions.",
    ],
    needs=["Pass/fail criteria in writing", "Systems to include (panel, corner, joint, anchor)", "On-structure vs freestanding decision", "Sign-off attendees list", "Programme slot before mass order"],
    caps=["Visual sample walls", "Performance mock-ups", "Structural silicone mock-ups", "Hybrid transition bays", "Documented sign-off photography"],
    variants=[("Freestanding sample walls", "Early aesthetic approval."), ("On-structure mock-ups", "Anchors and weather."), ("Silicone bonding mock-ups", "Adhesion tests."), ("Hybrid interface mock-ups", "Stone-ACP-glass junctions.")],
    materials=[("Project materials", "Same lots as intended."), ("Sealants & anchors", "Final system."), ("Temporary structures", "As required.")],
    faqs=[
        ("Indoor or on-structure?", "On-structure is better for anchors and weather."),
        ("How big?", "Large enough to prove the hardest detail."),
        ("Can mock-up panels be reused?", "Sometimes on non-critical faces - ask first."),
        ("Who attends sign-off?", "Architect, client and contractor - record decisions."),
        ("VE after mock-up?", "Freeze VE after approval to protect the elevation."),
    ],
    blogs=[("/blog/facade-mockup-checklist/", "Mock-up Checklist"), ("/blog/structural-silicone-glazing-mockups/", "Silicone Mock-ups")],
    related=["facade-design-assist", "acpcladding", "structuralglass"],
    cta="Approve the bay before you approve the tonnes",
    cta_sub="Plan a mock-up into your programme.",
    usp="Mock-ups that include the hard interfaces, not only clean panels.",
    card_blurb="Visual and performance mock-up bays before mass facade production.",
)

S(
    "fire-rated-facade-systems",
    title="Fire-Rated Facade Systems",
    short="fire-rated facade systems",
    desc_meta="Fire-rated facade systems in Mumbai - FR ACP zones and cavity barrier coordination by Shebi Enterprises.",
    tagline="FR ACP zones, cavity barriers and material control for high-rise fire strategies.",
    what=[
        "High-rise fire strategies increasingly control combustible cladding, cavity barriers and compartmentation at the facade. Mixing PE offcuts into FR elevations is a common site failure mode.",
        "We install FR-grade ACP systems and coordinate cavity detailing with the project's fire consultant - we do not replace statutory fire engineering.",
    ],
    needs=["Fire strategy extracts", "FR brand and core grade list", "Cavity barrier details", "Zone drawings (FR vs non-FR)", "Inspection and documentation requirements"],
    caps=["FR ACP installation", "Material control on site", "Cavity barrier coordination", "Documentation for approvals", "Training toolbox talks on FR zones"],
    variants=[("Full FR elevations", "High-rise compliance zones."), ("Partial FR bands", "Specific floors / faces."), ("Hospitality / assembly", "Stricter occupancy rules."), ("Retrofit FR upgrades", "With survey of existing build-up.")],
    materials=[("FR mineral-core ACP", "Brand-locked."), ("Cavity barriers", "As fire consultant details."), ("Non-combustible trims", "Where required.")],
    faqs=[
        ("Do you certify the fire design?", "Fire engineering remains with the appointed consultant; we install and document to approved details."),
        ("Can PE and FR mix on one face?", "Only as the strategy allows - never by accident on site."),
        ("Documentation?", "Batch records and photos support approvals."),
        ("Retrofit FR?", "Possible with survey and strategy update."),
        ("Cost premium?", "FR cores and detailing cost more - budget explicitly."),
    ],
    blogs=[("/blog/fire-rated-acp-high-rise-india/", "Fire-Rated ACP High-Rise"), ("/blog/acp-cladding-contractors-mumbai/", "ACP Contractors"), ("/blog/acp-fire-safety-core-grades/", "ACP Core Grades") if False else ("/blog/fire-rated-acp-high-rise-india/", "Fire-Rated ACP")],
    related=["acpcladding", "hpl-solid-aluminium-cladding", "facade-design-assist"],
    cta="Keep FR zones real on site, not only on drawings",
    cta_sub="Share fire strategy extracts for an FR install discussion.",
    usp="FR ACP install with material discipline and documentation.",
    card_blurb="FR ACP zones and cavity-barrier coordination for high-rise fire strategies.",
)

# fix fire blogs list cleanly
RAW["fire-rated-facade-systems"]["blogs"] = [
    ("/blog/fire-rated-acp-high-rise-india/", "Fire-Rated ACP for High-Rise"),
    ("/blog/acp-vs-hpl-vs-solid-aluminium/", "ACP vs HPL vs Solid Aluminium"),
    ("/blog/acp-cladding-contractors-mumbai/", "ACP Contractors Mumbai"),
]

S(
    "aluminium-windows-doors",
    title="Aluminium Windows & Doors",
    short="aluminium windows and doors",
    desc_meta="Aluminium window and door systems in Mumbai - thermal-break frames with facade-coordinated install by Shebi Enterprises.",
    tagline="Aluminium window and door systems coordinated with curtain wall, ACP and stone interfaces.",
    what=[
        "Aluminium windows and doors sit at every weather interface on a tower. Frame type, glass build-up, thresholds and flashings decide whether floors stay dry and comfortable through Mumbai monsoon and heat.",
        "Shebi Enterprises supplies and installs aluminium window and door packages as part of the wider envelope - so openings align with cladding grids, sill details and maintenance access.",
    ],
    needs=[
        "Window and door schedule with sizes and openable types",
        "Glass and hardware specification",
        "Thermal / acoustic performance targets if any",
        "Interface details with ACP, stone and curtain wall",
        "Access strategy for upper floors",
    ],
    caps=[
        "Casement, sliding and tilt-turn systems",
        "Entrance and terrace door sets",
        "Thermal-break frames where specified",
        "Coordination with cladding reveals",
        "Site survey, fixing and weather sealing",
    ],
    variants=[
        ("Casement windows", "Outward / inward openers for ventilation."),
        ("Sliding systems", "Wide openings on residences."),
        ("Tilt-turn", "European-style multipoint hardware."),
        ("Terrace / balcony doors", "Thresholds detailed for monsoon."),
    ],
    materials=[
        ("Aluminium profiles", "System brands as specified."),
        ("IGU / toughened glass", "Per schedule."),
        ("Hardware & seals", "Coastal-grade where required."),
    ],
    faqs=[
        ("Do you coordinate with ACP reveals?", "Yes - openings and cladding should share one grid logic."),
        ("Thermal break required?", "Follow the project spec and comfort targets."),
        ("Can you match curtain wall sightlines?", "Often with system selection and detail workshops."),
        ("Monsoon thresholds?", "We detail drains and seals for driven rain."),
        ("Retrofit windows?", "Possible after survey of existing openings."),
    ],
    blogs=[
        ("/blog/curtain-wall-contractors-mumbai/", "Curtain Wall Contractors"),
        ("/blog/igu-double-glazing-hot-climate/", "IGU for Hot Climates"),
        ("/blog/stick-system-glazing-when/", "When Stick Glazing Makes Sense"),
    ],
    related=["glazingwork", "balcony-terrace-glass-enclosures", "acpcladding"],
    cta="Specify openings with the facade, not after it",
    cta_sub="Share the window schedule for a coordinated quote.",
    usp="Window and door packages installed by facade teams who own the weather line.",
    card_blurb="Aluminium window and door systems coordinated with cladding and curtain wall.",
)

S(
    "balcony-terrace-glass-enclosures",
    title="Balcony & Terrace Glass Enclosures",
    short="balcony terrace glass enclosures",
    desc_meta="Balcony and terrace glass enclosure contractors in Mumbai - sliding and framed systems by Shebi Enterprises.",
    tagline="Glass enclosures for balconies and terraces that respect wind, drainage and railing loads.",
    what=[
        "Balcony and terrace glass enclosures extend usable space while controlling wind and rain. They must respect structural edge loads, railing codes, drainage and the look of the elevation from the street.",
        "We design-install framed and sliding enclosure packages alongside glass railings and aluminium openings so the tower elevation stays coherent.",
    ],
    needs=[
        "Balcony / terrace GA and railing drawings",
        "Openable vs fixed enclosure intent",
        "Wind and human-impact criteria",
        "Drainage and waterproofing notes at slab edge",
        "Society or developer approval constraints",
    ],
    caps=[
        "Sliding and stacking glass systems",
        "Framed enclosure bays",
        "Integration with glass railings",
        "Threshold and drain detailing",
        "High-rise install with method statements",
    ],
    variants=[
        ("Full-height sliding enclosures", "Seasonal open/close living."),
        ("Partial wind screens", "Upper-rail glass only."),
        ("Terrace rooms", "Larger framed enclosures."),
        ("Retrofit enclosures", "On existing parapets after survey."),
    ],
    materials=[
        ("Toughened / laminated glass", "Per safety strategy."),
        ("Aluminium frames & tracks", "Powder-coated."),
        ("SS fixings", "Coastal grades as needed."),
    ],
    faqs=[
        ("Will society allow enclosures?", "Many require prior approval - we can support drawings for submission."),
        ("Does it affect facade drainage?", "Thresholds and weep paths must be designed, not improvised."),
        ("Can it match railing glass?", "Yes - hardware and glass families can align."),
        ("Wind noise?", "System choice and seals matter on high floors."),
        ("Maintenance?", "Tracks and seals need periodic cleaning - include in AMC if desired."),
    ],
    blogs=[
        ("/blog/office-lobby-glass-spec/", "Lobby Glass Spec Tips"),
        ("/blog/point-fixed-glass-hardware/", "Point-Fixed Hardware"),
        ("/blog/residential-podium-cladding/", "Residential Podium Cladding"),
    ],
    related=["glass-railings-balustrades", "aluminium-windows-doors", "glazingwork"],
    cta="Enclose balconies without fighting the elevation",
    cta_sub="Share balcony drawings for an enclosure package review.",
    usp="Enclosure systems detailed with railing, drainage and facade finish in mind.",
    card_blurb="Sliding and framed glass enclosures for residential balconies and terraces.",
)

S(
    "acp-cladding-cleaning-restoration",
    title="ACP Cladding Cleaning & Restoration",
    short="ACP cladding cleaning restoration",
    desc_meta="ACP cladding cleaning and restoration in Mumbai - panel wash, polish and local repair by Shebi Enterprises.",
    tagline="Scheduled ACP cleaning, stain removal and local panel restoration for societies and commercial towers.",
    what=[
        "ACP elevations lose gloss and pick up monsoon stains, sealant residue and pollution film. Cleaning alone is not enough when joints have failed or panels are dented - restoration pairs wash cycles with sealant and panel repairs.",
        "Shebi Enterprises runs ACP cleaning and restoration programmes using BMU or rope access, with the same crews who understand FR cores, joint design and colour matching.",
    ],
    needs=[
        "Elevation photos and priority faces",
        "Access method (BMU tracks vs rope access)",
        "Known stains, dents or open joints",
        "Colour / finish notes for replacement panels",
        "Occupied-building work windows",
    ],
    caps=[
        "Soft-wash and panel-safe cleaning",
        "Sealant residue and staining treatment",
        "Local panel replacement",
        "Joint touch-up and reseal",
        "Photo reports before / after",
    ],
    variants=[
        ("Annual cleaning cycles", "Whole-tower or priority faces."),
        ("Monsoon recovery cleans", "Post-storm stain programmes."),
        ("Panel restoration", "Dents, scratches, replacements."),
        ("Combined AMC", "Cleaning + sealant + inspection."),
    ],
    materials=[
        ("Panel-safe cleaners", "Matched to coating type."),
        ("Colour-matched sealants", "For joint touch-ups."),
        ("Replacement ACP", "Same brand / lot where possible."),
    ],
    faqs=[
        ("Will pressure washing damage ACP?", "Aggressive pressure can harm coatings - we use controlled methods."),
        ("Can faded colour be restored?", "Cleaning helps; severe UV fade may need panel replacement."),
        ("Do you clean glass too?", "Yes as part of facade maintenance packages."),
        ("FR panels - any special care?", "Yes - no solvents that attack coatings; document FR zones."),
        ("Society AMC?", "We can combine cleaning with sealant and inspection contracts."),
    ],
    blogs=[
        ("/blog/facade-maintenance-guide/", "Facade Maintenance Guide"),
        ("/blog/acp-colour-fading-uv-india/", "ACP Colour Fading and UV"),
        ("/blog/rope-access-vs-bmu-facade-cleaning/", "Rope Access vs BMU"),
        ("/blog/acp-joint-design-sealants/", "ACP Joint Sealants"),
    ],
    related=["facade-maintenance", "sealant-joint-rehabilitation-amc", "acpcladding"],
    cta="Restore ACP elevations without guessing the coating",
    cta_sub="Request a cleaning and restoration survey.",
    usp="ACP cleaning by facade installers who also reseal and replace panels.",
    card_blurb="ACP washing, stain treatment and local panel restoration for towers and societies.",
)


def title_of(slug: str) -> str:
    return RAW[slug]["title"]


def nav_dropdown_html() -> str:
    parts = ['            <div class="dropdown-menu dropdown-menu-grouped">']
    for gname, slugs in GROUPS:
        parts.append(f'              <div class="dropdown-group"><span class="dropdown-group-label">{esc(gname)}</span>')
        for slug in slugs:
            parts.append(f'                <a href="/ourservice/{slug}/">{esc(title_of(slug))}</a>')
        parts.append("              </div>")
    parts.append("            </div>")
    return "\n".join(parts)


def footer_services_html() -> str:
    # Compact: link to hub groups + key services to avoid huge footers
    lines = [
        '                <li><a href="/services/">All services</a></li>',
        '                <li><a href="/ourservice/acpcladding/">ACP Cladding</a></li>',
        '                <li><a href="/ourservice/glazingwork/">Glazing Works</a></li>',
        '                <li><a href="/ourservice/stonewetcladding/">Stone Cladding</a></li>',
        '                <li><a href="/ourservice/unitised-curtain-wall/">Unitised Curtain Wall</a></li>',
        '                <li><a href="/ourservice/retrofit-recladding/">Retrofit &amp; Recladding</a></li>',
        '                <li><a href="/ourservice/facade-maintenance/">Facade Maintenance</a></li>',
        '                <li><a href="/ourservice/facade-design-assist/">Design-Assist</a></li>',
    ]
    return "\n".join(lines)


def sync_images():
    if ASSETS.exists():
        for src in ASSETS.glob("service-*.jpg"):
            dest = IMG / src.name
            if not dest.exists() or src.stat().st_mtime > dest.stat().st_mtime:
                shutil.copy2(src, dest)


def render_service(slug: str) -> None:
    d = RAW[slug]
    title = d["title"]
    card = CARD_IMG[slug]
    g = group_of(slug)
    detail, install = DETAIL_BY_GROUP[g]
    img1 = f"/img/services/{card}"
    img2 = f"/img/services/{detail}"
    img3 = f"/img/services/{install}"
    url = f"{SITE}/ourservice/{slug}/"
    faqs = d["faqs"]
    faq_schema = [
        {
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        }
        for q, a in faqs
    ]
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
                "name": f"{title} Mumbai | Shebi Enterprises",
                "description": d["desc_meta"],
                "isPartOf": {"@id": f"{SITE}/#organization"},
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{url}#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                    {"@type": "ListItem", "position": 2, "name": "Services", "item": f"{SITE}/services/"},
                    {"@type": "ListItem", "position": 3, "name": title, "item": url},
                ],
            },
            {
                "@type": "Service",
                "@id": f"{url}#service",
                "name": title,
                "serviceType": d["short"],
                "description": d["desc_meta"],
                "provider": {"@id": f"{SITE}/#organization"},
                "areaServed": [
                    {"@type": "City", "name": "Mumbai"},
                    {"@type": "State", "name": "Maharashtra"},
                    {"@type": "Country", "name": "India"},
                ],
                "url": url,
            },
            {"@type": "FAQPage", "@id": f"{url}#faq", "mainEntity": faq_schema},
        ],
    }

    what_html = "\n".join(f"            <p>{esc(p)}</p>" for p in d["what"])
    needs_html = "\n".join(f"              <li><i class=\"fas fa-check\"></i><span>{esc(n)}</span></li>" for n in d["needs"])
    caps_html = "\n".join(f"              <li><i class=\"fas fa-check\"></i><span>{esc(c)}</span></li>" for c in d["caps"])
    var_html = "\n".join(
        f'            <div class="variant-card"><strong>{esc(n)}</strong><p style="margin:8px 0 0;font-size:0.9rem;color:var(--gray)">{esc(b)}</p></div>'
        for n, b in d["variants"]
    )
    mat_html = "\n".join(
        f'            <div class="material-tag" style="display:block;padding:16px"><strong>{esc(n)}</strong><br /><span style="font-size:0.85rem;font-weight:400">{esc(b)}</span></div>'
        for n, b in d["materials"]
    )
    faq_html = "\n".join(
        f'''          <div class="faq-item">
            <button type="button" class="faq-question">{esc(q)} <i class="fas fa-chevron-down"></i></button>
            <div class="faq-answer"><div class="faq-answer-inner"><p>{esc(a)}</p></div></div>
          </div>'''
        for q, a in faqs
    )
    blogs_html = "\n".join(
        f'              <li style="margin: 8px 0"><a href="{h}">{esc(t)}</a></li>' for h, t in d["blogs"]
    )
    rel_html = "\n".join(
        f'              <li style="margin: 8px 0"><a href="/ourservice/{rs}/">{esc(title_of(rs))}</a></li>'
        for rs in d["related"]
        if rs in RAW
    )
    # related projects - pick 3 based on hash
    idxs = [sum(map(ord, slug)) % len(PROJECTS), (sum(map(ord, slug)) + 2) % len(PROJECTS), (sum(map(ord, slug)) + 4) % len(PROJECTS)]
    proj_cards = []
    for i in idxs:
        href, name, img, blurb = PROJECTS[i]
        proj_cards.append(
            f'''            <a href="{href}" class="card" style="text-decoration: none; color: inherit">
              <img src="{img}" alt="{esc(name)}" loading="lazy" width="400" height="260" />
              <div style="padding: 16px"><h4>{esc(name)}</h4><p>{esc(blurb)}</p></div>
            </a>'''
        )
    proj_html = "\n".join(proj_cards)

    page = f'''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="icon" href="/logo/favicon.svg" type="image/svg+xml" sizes="any" />
    <link rel="apple-touch-icon" href="/logo/favicon.svg" />
    <link rel="manifest" href="/manifest.json" />
    <title>{esc(title)} Mumbai | Shebi Enterprises</title>
    <meta name="description" content="{esc(d['desc_meta'])}" />
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
    <meta property="og:title" content="{esc(title)} Mumbai | Shebi Enterprises" />
    <meta property="og:description" content="{esc(d['desc_meta'])}" />
    <meta property="og:url" content="{url}" />
    <meta property="og:image" content="{SITE}/img/social/og-default.jpg" />
    <meta property="og:locale" content="en_IN" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{esc(title)} Mumbai | Shebi Enterprises" />
    <meta name="twitter:description" content="{esc(d['desc_meta'])}" />
    <meta name="twitter:image" content="{SITE}/img/social/og-default.jpg" />
    <script type="application/ld+json">
{json.dumps(schema, indent=2)}
    </script>
  </head>
  <body>
    <header class="navbar scrolled" id="navbar">
      <div class="container navbar-inner">
        <a href="/" class="navbar-logo">
          <img src="/logo/LightTheme.svg" alt="Shebi Enterprises Logo" class="logo-dark" height="50" width="180" />
          <img src="/logo/DarkTheme.svg" alt="Shebi Enterprises Logo" class="logo-light" height="50" width="180" />
        </a>
        <nav class="navbar-links">
          <a href="/">Home</a>
          <div class="nav-dropdown">
            <a href="/services/">Services <i class="fas fa-chevron-down"></i></a>
{nav_dropdown_html()}
          </div>
          <a href="/portfolio/">Projects</a>
          <a href="/about/">About</a>
          <a href="/blog/">Blog</a>
          <a href="/contact/">Contact</a>
        </nav>
        <div class="navbar-actions">
          <a href="/contact/" class="btn btn-primary navbar-cta">Get Free Quote</a>
          <button class="hamburger" id="hamburger" type="button" aria-label="Menu"><span></span><span></span><span></span></button>
        </div>
      </div>
      <div class="mobile-menu" id="mobileMenu">
        <div class="mobile-menu-inner">
          <a href="/">Home</a>
          <a href="/services/">Services</a>
          <a href="/portfolio/">Projects</a>
          <a href="/about/">About</a>
          <a href="/blog/">Blog</a>
          <a href="/contact/">Contact</a>
          <a href="/contact/" class="btn btn-primary">Get Free Quote</a>
        </div>
      </div>
    </header>

    <main class="page-wrap">
      <section class="page-hero">
        <div class="container">
          <nav class="breadcrumb" aria-label="Breadcrumb">
            <a href="/">Home</a>
            <i class="fas fa-chevron-right" aria-hidden="true"></i>
            <a href="/services/">Services</a>
            <i class="fas fa-chevron-right" aria-hidden="true"></i>
            <span>{esc(title)}</span>
          </nav>
          <h1 data-aos="fade-up">{esc(title)}</h1>
          <p data-aos="fade-up" data-aos-delay="100">{esc(d['tagline'])}</p>
        </div>
      </section>

      <section class="service-inner-section">
        <div class="container why-grid">
          <div data-aos="fade-right">
            <img src="{img1}" alt="{esc(title)} - Shebi Enterprises" class="why-img" width="700" height="520" loading="lazy" />
          </div>
          <div data-aos="fade-left">
            <span class="label" style="color: var(--secondary); font-family: var(--font-accent); letter-spacing: 2px; text-transform: uppercase; font-size: 0.8rem">What is it?</span>
            <h2 style="color: var(--primary); margin: 12px 0">{esc(title)}</h2>
{what_html}
          </div>
        </div>
      </section>

      <section class="service-inner-section alt">
        <div class="container" style="display:grid;grid-template-columns:1.1fr 0.9fr;gap:40px;align-items:center">
          <div>
            <h2 style="color: var(--primary); margin-bottom: 16px">What the client needs</h2>
            <p style="margin-bottom: 16px; color: var(--gray)">A complete pack produces a buildable estimate and fewer site claims. Share what you have via <a href="/contact/">contact</a> - we will list gaps plainly.</p>
            <ul class="capabilities-list" style="display:grid;gap:12px">
{needs_html}
            </ul>
          </div>
          <div>
            <img src="{img2}" alt="{esc(title)} detail - Shebi Enterprises" width="640" height="480" loading="lazy" style="width:100%;border-radius:var(--border-radius-lg);object-fit:cover" />
          </div>
        </div>
      </section>

      <section class="service-inner-section">
        <div class="container">
          <h2 class="section-header" style="text-align: left"><span class="label">Capabilities</span></h2>
          <ul class="capabilities-list grid-2" style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px">
{caps_html}
          </ul>
        </div>
      </section>

      <section class="service-inner-section alt">
        <div class="container">
          <h2 style="color: var(--primary); margin-bottom: 12px">Types &amp; variants</h2>
          <p style="margin-bottom: 24px; color: var(--gray); max-width: 720px">Choose the variant that matches performance, aesthetics and logistics - not brochure habit.</p>
          <div class="variant-grid">
{var_html}
          </div>
        </div>
      </section>

      <section class="service-inner-section">
        <div class="container">
          <h2 style="color: var(--primary); margin-bottom: 12px">Materials we work with</h2>
          <p style="margin-bottom: 24px; color: var(--gray); max-width: 720px">Final brands follow the approved specification and fire strategy.</p>
          <div class="material-grid">
{mat_html}
          </div>
        </div>
      </section>

      <section class="service-inner-section alt">
        <div class="container" style="display:grid;grid-template-columns:0.9fr 1.1fr;gap:40px;align-items:center">
          <div>
            <img src="{img3}" alt="{esc(title)} installation - Shebi Enterprises" width="640" height="480" loading="lazy" style="width:100%;border-radius:var(--border-radius-lg);object-fit:cover" />
          </div>
          <div>
            <h2 style="color: var(--primary); margin-bottom: 16px">How we deliver</h2>
            <ol style="line-height:1.8;padding-left:1.2rem;color:var(--text-dark)">
              <li><strong>Survey &amp; pack review</strong> - drawings, access and interfaces.</li>
              <li><strong>Shop drawings / coordination</strong> - freeze details with your consultant.</li>
              <li><strong>Mock-up where required</strong> - visual and performance checks.</li>
              <li><strong>Fabrication &amp; procurement</strong> - brackets, panels, glass as scoped.</li>
              <li><strong>Install &amp; QA</strong> - monsoon-aware sequencing and documented sign-off.</li>
              <li><strong>Handover</strong> - as-builts, batches and maintenance notes.</li>
            </ol>
          </div>
        </div>
      </section>

      <section class="service-inner-section">
        <div class="container">
          <h2 style="text-align: center; margin-bottom: 32px; color: var(--primary)">Why choose Shebi?</h2>
          <div class="usp-grid-3">
            <div class="usp-box"><h4>20+ years on site</h4><p>{esc(d['usp'])}</p></div>
            <div class="usp-box"><h4>Developer-grade QA</h4><p>Mock-ups, documented sign-off and clear exclusions.</p></div>
            <div class="usp-box"><h4>Monsoon-ready details</h4><p>Weep paths, flashings and sealant specs matched to exposure.</p></div>
          </div>
        </div>
      </section>

      <section class="service-inner-section alt">
        <div class="container">
          <h2 style="color: var(--primary); margin-bottom: 24px">Related projects</h2>
          <div class="related-projects-grid">
{proj_html}
          </div>
        </div>
      </section>

      <section class="service-inner-section">
        <div class="container" style="max-width: 800px">
          <h2 style="color: var(--primary); margin-bottom: 20px">FAQ</h2>
{faq_html}
        </div>
      </section>

      <section class="cta-banner">
        <div class="container">
          <h2>{esc(d['cta'])}</h2>
          <p>{esc(d['cta_sub'])}</p>
          <div class="cta-actions">
            <a href="/contact/" class="btn btn-primary">Get Free Quote</a>
            <a href="/services/" class="btn btn-outline">All services</a>
          </div>
        </div>
      </section>

      <section class="service-inner-section alt" aria-labelledby="related-reading-heading">
        <div class="container" style="max-width: 900px">
          <h2 id="related-reading-heading" style="color: var(--primary); margin-bottom: 12px">Related reading</h2>
          <p style="margin-bottom: 16px; color: var(--gray)">Guides from Shebi Enterprises to help you specify and tender this package.</p>
          <ul style="line-height: 1.7; padding-left: 1.2rem">
{blogs_html}
          </ul>
          <h2 style="color: var(--primary); margin: 28px 0 12px; font-size:1.35rem">Related services</h2>
          <ul style="line-height: 1.7; padding-left: 1.2rem">
{rel_html}
          </ul>
          <p style="margin-top: 20px"><a href="/blog/" class="btn btn-outline" style="color: var(--primary); border-color: var(--primary)">Browse all insights</a>
          <a href="/contact/" class="btn btn-primary" style="margin-left: 10px">Get free quote</a></p>
        </div>
      </section>
    </main>

    <footer class="footer">
      <div class="footer-main">
        <div class="container">
          <div class="footer-grid">
            <div class="footer-col footer-brand">
              <img src="/logo/DarkTheme.svg" alt="Shebi Enterprises" height="50" width="180" loading="lazy" />
              <p>Mumbai's most trusted cladding and glazing contractor since 2005.</p>
              <div class="footer-social">
                <a href="https://www.facebook.com/shebienterprises" target="_blank" rel="noopener noreferrer" aria-label="Facebook"><i class="fab fa-facebook-f"></i></a>
                <a href="https://www.instagram.com/shebi.enterprises" target="_blank" rel="noopener noreferrer" aria-label="Instagram"><i class="fab fa-instagram"></i></a>
                <a href="https://www.linkedin.com/company/shebienterprises" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn"><i class="fab fa-linkedin-in"></i></a>
                <a href="https://wa.me/917738479381" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp"><i class="fab fa-whatsapp"></i></a>
              </div>
            </div>
            <div class="footer-col">
              <h4>Our Services</h4>
              <ul>
{footer_services_html()}
              </ul>
            </div>
            <div class="footer-col">
              <h4>Quick Links</h4>
              <ul>
                <li><a href="/">Home</a></li>
                <li><a href="/about/">About Us</a></li>
                <li><a href="/portfolio/">Our Projects</a></li>
                <li><a href="/blog/">Blog</a></li>
                <li><a href="/careers/">Careers</a></li>
                <li><a href="/contact/">Contact Us</a></li>
              </ul>
            </div>
            <div class="footer-col">
              <h4>Contact Us</h4>
              <div class="footer-contact">
                <div class="contact-item"><i class="fas fa-phone"></i><div><a href="tel:+919321598252">+91 9321598252</a><br /><a href="tel:+917738479381">+91 7738479381</a></div></div>
                <div class="contact-item"><i class="fas fa-envelope"></i><a href="mailto:info@shebienterprises.com">info@shebienterprises.com</a></div>
                <div class="contact-item"><i class="fab fa-whatsapp"></i><a href="https://wa.me/917738479381" target="_blank" rel="noopener noreferrer">WhatsApp</a></div>
                <div class="contact-item"><i class="fas fa-map-marker-alt"></i><span>Mumbai, Maharashtra, India</span></div>
              </div>
              <a href="/contact/" class="btn btn-primary" style="margin-top: 20px; width: 100%; justify-content: center">Get Free Quote</a>
            </div>
          </div>
        </div>
      </div>
      <div class="footer-bottom">
        <div class="container">
          <p>© 2026 Shebi Enterprises. All Rights Reserved. Founded by Jerald Francis.</p>
          <p><a href="/">Home</a> | <a href="/services/">Services</a> | <a href="/portfolio/">Projects</a> | <a href="/contact/">Contact</a></p>
        </div>
      </div>
    </footer>

    <a href="https://wa.me/917738479381?text=Hi%20Shebi%20Enterprises%2C%20I%20would%20like%20to%20request%20a%20free%20quote." class="whatsapp-float" target="_blank" rel="noopener noreferrer" aria-label="Chat on WhatsApp"><i class="fab fa-whatsapp"></i><span class="whatsapp-tooltip">Get Free Quote</span></a>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/aos/2.3.4/aos.js"></script>
    <script src="/js/main.js"></script>
    <script>
      AOS.init({{ duration: 700, easing: "ease-out-cubic", once: true, offset: 80 }});
    </script>
  </body>
</html>
'''
    # fix double braces from AOS - we used {{ so they become {
    out_dir = ROOT / "ourservice" / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "index.html").write_text(page, encoding="utf-8")

    redirect = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="robots" content="noindex" />
  <link rel="canonical" href="{url}" />
  <meta http-equiv="refresh" content="0; url=/ourservice/{slug}/" />
  <title>Redirecting…</title>
  <script>location.replace("/ourservice/{slug}/");</script>
</head>
<body><p>Redirecting to <a href="/ourservice/{slug}/">{esc(title)}</a>…</p></body>
</html>
'''
    (ROOT / "ourservice" / f"{slug}.html").write_text(redirect, encoding="utf-8")
    print("service", slug)


def update_sitewide_nav_footer():
    dropdown = nav_dropdown_html()
    footer_ul = footer_services_html()
    # Match old flat dropdown
    old_dropdown_re = re.compile(
        r'<div class="dropdown-menu">\s*(?:<a href="/ourservice/[^"]+/">[^<]+</a>\s*)+</div>',
        re.M,
    )
    old_grouped_re = re.compile(
        r'<div class="dropdown-menu dropdown-menu-grouped">[\s\S]*?</div>\s*</div>\s*</div>',
        re.M,
    )
    # Simpler: replace from dropdown-menu open to closing before nav-dropdown close
    dropdown_block_re = re.compile(
        r'<div class="dropdown-menu(?: dropdown-menu-grouped)?">[\s\S]*?</div>\n(\s*)</div>\n(\s*)<a href="/portfolio/"',
        re.M,
    )

    footer_services_re = re.compile(
        r'(<div class="footer-col">\s*<h4>Our Services</h4>\s*<ul>)[\s\S]*?(</ul>\s*</div>)',
        re.M,
    )

    for path in ROOT.rglob("*.html"):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        orig = text
        text, n1 = dropdown_block_re.subn(
            dropdown + "\n\\1</div>\n\\2<a href=\"/portfolio/\"",
            text,
            count=1,
        )
        # If nested groups already, dropdown_block_re may fail due to multiple </div>
        if n1 == 0 and 'dropdown-menu' in text:
            text2, n2 = re.subn(
                r'<div class="dropdown-menu(?: dropdown-menu-grouped)?">[\s\S]*?</div>(?=\s*</div>\s*<a href="/portfolio/")',
                dropdown.strip(),
                text,
                count=1,
            )
            if n2:
                text = text2
                n1 = n2
        text, nf = footer_services_re.subn(r"\1\n" + footer_ul + r"\n              \2", text, count=1)
        if text != orig:
            path.write_text(text, encoding="utf-8")
            print("nav/footer", path.relative_to(ROOT), "dd", n1, "ft", nf)


def build_services_hub():
    cards = []
    for gname, slugs in GROUPS:
        cards.append(f'        <h2 class="services-group-title" data-aos="fade-up">{esc(gname)}</h2>')
        cards.append('        <div class="services-grid services-page-grid">')
        for i, slug in enumerate(slugs):
            d = RAW[slug]
            img = CARD_IMG[slug]
            delay = (i % 4) * 80
            cards.append(
                f'''          <a href="/ourservice/{slug}/" class="service-card" data-aos="fade-up" data-aos-delay="{delay}">
            <div class="service-card-media">
              <img src="/img/services/{img}" alt="{esc(d['title'])}" width="640" height="480" loading="lazy" />
            </div>
            <h3>{esc(d['title'])}</h3>
            <p>{esc(d.get('card_blurb', d['tagline']))}</p>
            <span class="learn-more">Details <i class="fas fa-arrow-right"></i></span>
          </a>'''
            )
        cards.append("        </div>")
    grid = "\n".join(cards)

    # Read existing hub and replace services section
    path = ROOT / "services" / "index.html"
    text = path.read_text(encoding="utf-8")
    # Remove hub key-facts block
    text = re.sub(
        r'\s*<aside class="seo-key-facts[\s\S]*?</aside>\s*',
        "\n\n",
        text,
        count=1,
    )
    text = re.sub(
        r'<section class="services-section services-page">[\s\S]*?</section>',
        f'''<section class="services-section services-page">
      <div class="container">
{grid}
        <div style="text-align: center; margin-top: 48px" data-aos="fade-up">
          <a href="/portfolio/" class="btn btn-dark">See project photos <i class="fas fa-images"></i></a>
          <a href="/contact/" class="btn btn-primary" style="margin-left: 12px">Request quote</a>
        </div>
      </div>
    </section>''',
        text,
        count=1,
    )
    # hero copy
    text = text.replace(
        "Design-assist, supply and installation for curtain wall, ACP, stone, structural glazing and allied metalwork used on premium projects across India.",
        "Design-assist, supply and installation across cladding, glazing, metalwork, lifecycle maintenance and fire-rated facade systems for premium projects across India.",
    )
    path.write_text(text, encoding="utf-8")
    print("hub updated")


def update_home_services():
    """Curated 8 cards on home + view all (FR systems only on /services/)."""
    curated = [
        "acpcladding",
        "glazingwork",
        "stonewetcladding",
        "unitised-curtain-wall",
        "spiderglazing",
        "retrofit-recladding",
        "canopy-dropoff-packages",
        "facade-maintenance",
    ]
    cards = ['        <div class="services-grid">']
    for i, slug in enumerate(curated):
        d = RAW[slug]
        img = CARD_IMG[slug]
        delay = (i % 4) * 100
        cards.append(
            f'''          <a href="/ourservice/{slug}/" class="service-card" data-aos="fade-up" data-aos-delay="{delay}">
            <div class="service-card-media">
              <img src="/img/services/{img}" alt="{esc(d['title'])}" width="640" height="480" loading="lazy" />
            </div>
            <h3>{esc(d['title'])}</h3>
            <p>{esc(d.get('card_blurb', d['tagline']))}</p>
            <span class="learn-more">Learn More <i class="fas fa-arrow-right"></i></span>
          </a>'''
        )
    cards.append("        </div>")
    grid = "\n".join(cards)
    path = ROOT / "index.html"
    text = path.read_text(encoding="utf-8")
    text = re.sub(
        r'(<section class="services-section">\s*<div class="container">\s*<div class="section-header" data-aos="fade-up">[\s\S]*?</div>\s*)<div class="services-grid">[\s\S]*?</div>\s*<div style="text-align: center; margin-top: 48px"',
        r"\1" + grid + '\n        <div style="text-align: center; margin-top: 48px"',
        text,
        count=1,
    )
    path.write_text(text, encoding="utf-8")
    print("home services updated")


def update_sitemap_llms():
    sm = ROOT / "sitemap.xml"
    text = sm.read_text(encoding="utf-8")
    for slug in RAW:
        url = f"{SITE}/ourservice/{slug}/"
        if url not in text:
            entry = f"""  <url>
    <loc>{url}</loc>
    <lastmod>2026-11-16</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.75</priority>
  </url>
"""
            text = text.replace("</urlset>", entry + "</urlset>")
    sm.write_text(text, encoding="utf-8")

    llms = ROOT / "llms.txt"
    lt = llms.read_text(encoding="utf-8")
    block_lines = ["## Services", ""]
    for gname, slugs in GROUPS:
        block_lines.append(f"### {gname}")
        for slug in slugs:
            block_lines.append(f"- [{title_of(slug)}]({SITE}/ourservice/{slug}/)")
        block_lines.append("")
    block_lines.append(f"- [Full service list]({SITE}/services/)")
    block = "\n".join(block_lines)
    if "## Services" in lt:
        lt = re.sub(r"## Services[\s\S]*?(?=\n## |\Z)", block + "\n", lt, count=1)
    else:
        lt += "\n" + block + "\n"
    llms.write_text(lt, encoding="utf-8")
    print("sitemap/llms updated")


def main():
    assert len(RAW) == 27, f"expected 27 services, got {len(RAW)}"
    sync_images()
    for slug in RAW:
        assert slug in CARD_IMG, slug
        render_service(slug)
    build_services_hub()
    update_home_services()
    update_sitemap_llms()
    update_sitewide_nav_footer()
    print("DONE services", len(RAW))


if __name__ == "__main__":
    main()
