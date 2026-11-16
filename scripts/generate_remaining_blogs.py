#!/usr/bin/env python3
"""Generate remaining SEO blog posts (7-50), update index/sitemap/llms/related reading."""
from __future__ import annotations

import html
import json
import re
import shutil
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://shebienterprises.com"
ASSETS = Path(
    "/Users/jetsoanalin/.cursor/projects/Users-jetsoanalin-Documents-Projects-Shebi-Enterprises-shebienterprises-github-io/assets"
)
BLOG_IMG = ROOT / "img" / "blog"
BLOG_IMG.mkdir(parents=True, exist_ok=True)

# Existing Phase A (1-6) already published — skip if present
DONE = {
    "acp-cladding-contractors-mumbai",
    "stone-cladding-cost-mumbai",
    "curtain-wall-contractors-mumbai",
    "structural-vs-semi-unitised-glazing",
    "fire-rated-acp-high-rise-india",
    "spider-glazing-lobbies-mumbai",
}

# (num, title, slug, category, category_label, primary_kw, services, related_blogs, sections)
# sections: list of (h2, paragraph) — paragraph may include <a> tags
RAW = [
    (7, "Facade Leakage Diagnosis After Monsoon", "facade-leakage-after-monsoon", "maintenance", "Maintenance", "facade leakage Mumbai",
     ["/ourservice/facade-maintenance/", "/ourservice/acpcladding/", "/ourservice/glazingwork/"],
     ["/blog/monsoon-facade-installation-mumbai/", "/blog/facade-maintenance-guide/"],
     [
         ("Start with a pattern, not a single stain", "After Mumbai’s monsoon, map wet patches against floor levels, wind exposure and joint lines. Random damp often means blocked drainage; repeating stains at the same joint usually point to sealant failure or open end dams. Our <a href=\"/ourservice/facade-maintenance/\">facade maintenance</a> teams photograph and tag each location before opening joints."),
         ("Separate cladding leaks from internal condensation", "Glass and <a href=\"/ourservice/acpcladding/\">ACP</a> elevations can look wet from condensation or failed IGUs edge seals. Check relative humidity indoors, AC set-points and whether water appears only on cold mornings. True weather leaks worsen during driven rain from a known direction."),
         ("Interfaces fail first", "Most chronic leaks sit where ACP meets stone, canopy meets curtain wall, or window meets cladding. Confirm who owns each interface in the original tender. For sequencing lessons, read <a href=\"/blog/monsoon-facade-installation-mumbai/\">monsoon façade installation</a>."),
         ("Repair order that saves money", "Clear cavities and weep paths first, replace failed sealant with compatible products, then retest with hose packs. Document batches and torque for handover so the next monsoon inspection is faster."),
     ],
     [
         ("When should we call a facade specialist?", "If leaks return after DIY silicone, if multiple floors show the same pattern, or if water reaches occupied interiors."),
         ("Can you diagnose without full scaffold?", "Often yes via BMU or rope access for surveys; complex cavities may still need local opening."),
         ("Will insurance need documentation?", "Keep dated photos, weather logs and material datasheets; we prepare survey notes suitable for PM and insurer files."),
     ]),
    (8, "How Developers Should Tender Facade Packages", "how-to-tender-facade-packages", "guides", "Guides", "facade tender India",
     ["/services/", "/contact/", "/ourservice/glazingwork/"],
     ["/blog/facade-quote-documents-mumbai/", "/blog/curtain-wall-contractors-mumbai/"],
     [
         ("Define systems before rates", "List stone wet/dry, ACP, curtain wall, spider glass and canopies as separate packages with clear interfaces. Ambiguous hybrid zones create claims. Start from our <a href=\"/services/\">services overview</a>."),
         ("Issue a complete tender set", "Elevations, typical details, performance specs (wind, water, U-value if any), fire strategy extracts and access constraints. See <a href=\"/blog/facade-quote-documents-mumbai/\">documents we need for a facade quote</a>."),
         ("Score quality, not only price", "Weight mock-up quality, FR capability, Mumbai references and programme realism. Use checklists similar to <a href=\"/blog/curtain-wall-contractors-mumbai/\">curtain wall contractor scope</a>."),
         ("Lock exclusions early", "Scaffold, BMU, night permits, waterproofing by others and free-issue glass must be explicit. Shebi Enterprises returns exclusions in plain English with every estimate via <a href=\"/contact/\">contact</a>."),
     ],
     [
         ("Should design assist be separate?", "Yes if the contractor owns engineering; state PE responsibilities clearly."),
         ("How many bidders are ideal?", "Three to five qualified facade specialists usually balance competition and quality."),
         ("Do you help write BOQ language?", "We can review draft BOQ headings against buildable site practice before you float rates."),
     ]),
    (9, "Unitised Curtain Wall: Pros, Cons, Mumbai Logistics", "unitised-curtain-wall-mumbai", "glazing", "Glazing", "unitised curtain wall Mumbai",
     ["/ourservice/glazingwork/", "/ourservice/fabricationwork/"],
     ["/blog/structural-vs-semi-unitised-glazing/", "/blog/curtain-wall-contractors-mumbai/"],
     [
         ("Why unitised wins on repetitive towers", "Factory-sealed modules improve quality control and speed once crane windows open. Compare options in <a href=\"/blog/structural-vs-semi-unitised-glazing/\">structural vs semi-unitised</a>."),
         ("Mumbai logistics constraints", "Staging yards, trailer access and night crane permits decide whether oversized modules are realistic. Dense plots may need smaller module grids even if aesthetics prefer larger glass."),
         ("Fabrication and tolerances", "Anchor brackets and embedding plates must match survey. Our <a href=\"/ourservice/fabricationwork/\">fabrication</a> and <a href=\"/ourservice/glazingwork/\">glazing</a> teams coordinate shim strategies before hang days."),
         ("When stick still competes", "Irregular podiums, renovations and late design changes often favour stick systems. See <a href=\"/blog/stick-system-glazing-when/\">when stick glazing still makes sense</a>."),
     ],
     [
         ("Do unitised systems leak less?", "They reduce site silicone dependency for primary weather lines, but sill and interface detailing still decide outcomes."),
         ("What lead time should we plan?", "Factory slots plus logistics often need months; lock glass early."),
         ("Can we mix unitised and stick?", "Yes—common on podium vs tower—if interfaces are detailed in tender."),
     ]),
    (10, "Granite Cladding for Podiums and Drop-offs", "granite-cladding-podiums-mumbai", "materials", "Materials", "granite cladding Mumbai",
     ["/ourservice/stonewetcladding/", "/ourservice/stonedrycladding/", "/portfolio/"],
     ["/blog/stone-cladding-cost-mumbai/", "/blog/residential-podium-cladding/"],
     [
         ("Why granite suits Mumbai podiums", "Dense granites resist humidity and traffic splash better than soft marbles. Wet or dry systems both appear on drop-offs; cost drivers are covered in <a href=\"/blog/stone-cladding-cost-mumbai/\">stone cladding cost</a>."),
         ("Detail the drop-off zone", "Canopy columns, planter edges and vehicle impact zones need thicker pieces, robust anchors and clean drip edges. Coordinate with <a href=\"/ourservice/skylights-canopies/\">canopy</a> steel early."),
         ("Wet vs dry at podium height", "Wet can sculpt feature walls; dry helps large panels and faster replacement. Explore <a href=\"/ourservice/stonewetcladding/\">wet</a> and <a href=\"/ourservice/stonedrycladding/\">dry</a> services."),
         ("References", "Review residential stone packages such as <a href=\"/projects/lodha-residential/\">Lodha residential</a> and the wider <a href=\"/portfolio/\">portfolio</a>."),
     ],
     [
         ("Which finish is safest at drop-offs?", "Flamed or textured finishes reduce slip risk on horizontal bands; polished faces suit vertical feature walls."),
         ("How thick should podium granite be?", "Depends on span and fixing; we size after engineering—not by catalogue habit."),
         ("Can granite meet ACP above?", "Yes with a designed transition flashing and joint philosophy."),
     ]),
    (11, "Glass Canopy Design Mistakes That Cause Leaks", "glass-canopy-leak-mistakes", "guides", "Guides", "glass canopy leaks",
     ["/ourservice/skylights-canopies/", "/ourservice/fabricationwork/"],
     ["/blog/skylight-drainage-condensation/", "/blog/canopy-anchorage-rcc/"],
     [
         ("Mistake: treating canopies like flat roofs", "Glass canopies need falls, gutters and overflow paths. Standing water finds every silicone gap. See <a href=\"/ourservice/skylights-canopies/\">skylights &amp; canopies</a>."),
         ("Mistake: ignoring frame movement", "Steel and aluminium expand differently from glass. Undersized slots and hard spots crack seals. Proper <a href=\"/ourservice/fabricationwork/\">fabrication</a> details movement."),
         ("Mistake: weak RCC anchorage", "Pull-out and edge distance errors show up as deflection and ponding. Read <a href=\"/blog/canopy-anchorage-rcc/\">canopy anchorage to RCC</a>."),
         ("Mistake: no maintenance access", "Clogged drains recreate last year’s leak. Plan cleaning routes in the handover pack."),
     ],
     [
         ("Laminated or toughened for canopies?", "Overhead glass typically needs laminated safety strategies—confirm with the structural glass specifier."),
         ("Can we retrofit drainage?", "Often yes with added gutters and re-sealed joints after a survey."),
         ("Do you design and build?", "We fabricate and install to approved drawings and coordinate details with your consultant."),
     ]),
    (12, "Get a Facade Quote in Mumbai: Documents We Need", "facade-quote-documents-mumbai", "guides", "Guides", "facade quote Mumbai",
     ["/contact/", "/services/"],
     ["/blog/how-to-tender-facade-packages/", "/blog/acp-cladding-price-mumbai/"],
     [
         ("Minimum pack for a useful estimate", "PDF elevations, typical wall sections, material schedule (ACP/stone/glass), fire notes if any, and site constraints (crane, hoist, night work). Send via <a href=\"/contact/\">contact</a>."),
         ("Why lump-sum without drawings misleads", "Corners, soffits and interfaces dominate labour. Our ACP pricing logic is explained in <a href=\"/blog/acp-cladding-price-mumbai/\">ACP cladding price in Mumbai</a>."),
         ("Performance specs help", "Wind criteria, water tightness targets and brand lists reduce VE churn later. Align with <a href=\"/blog/how-to-tender-facade-packages/\">tender best practices</a>."),
         ("What you receive back", "A structured estimate with inclusions, exclusions and questions—not a single opaque number."),
     ],
     [
         ("Can you quote from renders only?", "Only as a rough range; we need drawings for tender-grade pricing."),
         ("How fast is a first pass?", "Often within a few working days once the pack is complete."),
         ("Do you sign NDAs?", "Yes—share via email to info@shebienterprises.com when required."),
     ]),
    (13, "Wet Stone Cladding Step-by-Step on RCC Walls", "wet-stone-cladding-process", "materials", "Materials", "wet stone cladding process",
     ["/ourservice/stonewetcladding/"], ["/blog/stone-cladding-cost-mumbai/", "/blog/waterproofing-before-cladding/"],
     [
         ("Prepare the RCC", "Survey flatness, remove laitance, and confirm waterproofing readiness. See <a href=\"/blog/waterproofing-before-cladding/\">waterproofing before cladding</a>."),
         ("Set out and sample", "Approve stone batch, joint rhythm and mock-up before mass fixing. Our <a href=\"/ourservice/stonewetcladding/\">wet cladding</a> crews work to marked grids."),
         ("Bedding and curing", "Control mortar workability and protect curing through Mumbai heat and rain windows."),
         ("Finishing and protection", "Sealers, edge protection and cleaning protocols prevent early staining on podiums."),
     ],
     [("How long before striking supports?", "Follow mortar system datasheets and site temperature—never rush for a photo deadline."),
      ("Can wet cladding go on AAC blocks?", "Only with engineered backing and movement strategy; RCC is preferred for exteriors."),
      ("What about hollow patterns?", "Complex patterns raise waste and labour—price them as specials.")]),
    (14, "Dry Stone Cladding Anchors Explained", "dry-stone-cladding-anchors", "materials", "Materials", "dry stone cladding anchors",
     ["/ourservice/stonedrycladding/"], ["/blog/stone-cladding-cost-mumbai/", "/blog/open-joint-stone-facade/"],
     [
         ("What anchors do", "Mechanical fixings transfer stone weight and wind loads into the subframe or structure for <a href=\"/ourservice/stonedrycladding/\">dry cladding</a>."),
         ("Kerf quality matters", "Poor kerfs crack edges under load. Factory cutting tolerances and stainless grades suit coastal Mumbai air."),
         ("Open joints vs sealed", "Open-joint rainscreens need designed cavity drainage—see <a href=\"/blog/open-joint-stone-facade/\">open joint stone facades</a>."),
         ("Inspection", "Annual checks of fasteners and sealant at penetrations protect the system long term."),
     ],
     [("SS 304 or 316?", "Coastal exposure often prefers 316—confirm with the specifier."),
      ("Can we replace one panel?", "Dry systems are designed for selective replacement when layouts are documented."),
      ("Do you engineer anchors?", "We install to approved drawings; PE design sits with your consultant unless appointed.")]),
    (15, "ACP Joint Design, Sealants and Colour Matching", "acp-joint-design-sealants", "materials", "Materials", "ACP joint sealant",
     ["/ourservice/acpcladding/"], ["/blog/acp-cladding-price-mumbai/", "/blog/fire-rated-acp-high-rise-india/"],
     [
         ("Joint rhythm is aesthetic and waterproofing", "Uneven joints telegraph across elevations. Lock module sizes early on <a href=\"/ourservice/acpcladding/\">ACP</a> packages."),
         ("Sealant compatibility", "Use weathering-grade silicones approved with coatings and FR cores. Batch records help later repairs."),
         ("Colour matching across lots", "Order enough panels per elevation face; UV and lot variation show on Mumbai towers. Pricing context: <a href=\"/blog/acp-cladding-price-mumbai/\">ACP price guide</a>."),
         ("FR zones", "Do not mix PE offcuts into FR elevations—see <a href=\"/blog/fire-rated-acp-high-rise-india/\">FR ACP requirements</a>."),
     ],
     [("How wide should joints be?", "Follow system design and thermal movement—typically consistent visual widths across a face."),
      ("Can we paint sealant to match?", "Usually no—select colour-matched sealants instead."),
      ("Who cleans residue?", "Include cleaning in handover; residue becomes permanent staining if ignored.")]),
    (16, "Stick System Glazing: When It Still Makes Sense", "stick-system-glazing-when", "glazing", "Glazing", "stick system glazing",
     ["/ourservice/glazingwork/"], ["/blog/unitised-curtain-wall-mumbai/", "/blog/curtain-wall-contractors-mumbai/"],
     [
         ("Best uses", "Podiums, renovations, irregular geometry and late design freezes still favour stick <a href=\"/ourservice/glazingwork/\">glazing</a>."),
         ("Trade-offs", "More site labour and silicone dependency versus factory unitised speed. Compare with <a href=\"/blog/unitised-curtain-wall-mumbai/\">unitised logistics</a>."),
         ("Quality controls", "Survey, shim discipline and adhesion tests keep stick systems weather-tight."),
         ("Hybrid envelopes", "Many Mumbai towers mix stick podiums with unitised typical floors—define interfaces in tender."),
     ],
     [("Is stick cheaper?", "Sometimes on complex podiums; not always on tall repetitive grids."),
      ("Can stick meet the same water tests?", "Yes when detailed and installed correctly."),
      ("Do you still bid stick work?", "Yes—especially where logistics kill oversized modules.")]),
    (17, "Structural Silicone Glazing: Testing and Mock-ups", "structural-silicone-glazing-mockups", "glazing", "Glazing", "structural silicone glazing",
     ["/ourservice/structuralglass/"], ["/blog/structural-glazing-mumbai/", "/blog/structural-vs-semi-unitised-glazing/"],
     [
         ("Why mock-ups are non-negotiable", "Adhesion, bite and finish compatibility must be proven before mass bonding for <a href=\"/ourservice/structuralglass/\">structural glass</a>."),
         ("Tests that matter", "Peel/adhesion samples, compatibility with coatings, and weather exposure checks. Background: <a href=\"/blog/structural-glazing-mumbai/\">structural glazing in Mumbai</a>."),
         ("Site conditions", "Dust, monsoon humidity and temperature windows affect cure—programme accordingly."),
         ("System choice", "Decide structural vs semi-unitised early—see <a href=\"/blog/structural-vs-semi-unitised-glazing/\">comparison guide</a>."),
     ],
     [("How large should the mock-up be?", "Large enough to include a typical joint, corner and support condition."),
      ("Can we skip heat soak?", "Only if the glass specification allows—document the decision."),
      ("Who stores cure records?", "Keep them with as-builts for warranty and maintenance.")]),
    (18, "Point-Fixed Glass: Hardware Specs That Matter", "point-fixed-glass-hardware", "glazing", "Glazing", "point fixed glass",
     ["/ourservice/spiderglazing/"], ["/blog/spider-glazing-lobbies-mumbai/", "/blog/structural-glazing-mumbai/"],
     [
         ("Hardware grade", "Coastal Mumbai air prefers quality stainless (often 316). Cheap fittings stain and seize. Used on <a href=\"/ourservice/spiderglazing/\">spider glazing</a> lobbies."),
         ("Glass holes and edges", "Edge distances and hole quality control breakage risk. Align with <a href=\"/blog/spider-glazing-lobbies-mumbai/\">lobby spider glazing</a> practice."),
         ("Fin and cable systems", "Deflection limits drive comfort and reflection quality in atriums."),
         ("Maintenance", "Document torque and glass marks at handover for future inspections."),
     ],
     [("Can point-fixed glass be overhead?", "Only with laminated safety strategies and engineered support."),
      ("Do spiders need isolation washers?", "Yes—follow manufacturer assembly details."),
      ("Typical glass?", "Toughened / heat-soaked with thickness from engineering.")]),
    (19, "Skylight Drainage and Condensation Control", "skylight-drainage-condensation", "guides", "Guides", "skylight drainage",
     ["/ourservice/skylights-canopies/"], ["/blog/glass-canopy-leak-mistakes/", "/blog/igu-double-glazing-hot-climate/"],
     [
         ("Drain like a roof", "Falls, gutters and overflows are mandatory on <a href=\"/ourservice/skylights-canopies/\">skylights</a>."),
         ("Condensation vs leaks", "Warm moist indoor air on cold glass looks like a leak—check HVAC and IGU specs; see <a href=\"/blog/igu-double-glazing-hot-climate/\">IGU for hot climates</a>."),
         ("Common failures", "Clogged outlets and undersized joints—also covered in <a href=\"/blog/glass-canopy-leak-mistakes/\">canopy leak mistakes</a>."),
         ("Access", "Design cleaning paths before handover."),
     ],
     [("Can we add films later?", "Sometimes—but verify warranty impacts."),
      ("Are polycarbonate skylights OK?", "Depends on fire and aesthetic specs; glass dominates premium atriums."),
      ("Do you maintain skylights?", "Yes via inspection and sealant programmes.")]),
    (20, "Entrance Canopies: Steel vs Aluminium Frames", "entrance-canopy-steel-vs-aluminium", "guides", "Guides", "entrance canopy design",
     ["/ourservice/fabricationwork/", "/ourservice/skylights-canopies/"],
     ["/blog/canopy-anchorage-rcc/", "/blog/glass-canopy-leak-mistakes/"],
     [
         ("Steel strengths", "Long spans and heavy glass loads suit steel with proper corrosion protection—built by our <a href=\"/ourservice/fabricationwork/\">fabrication</a> team."),
         ("Aluminium strengths", "Lighter frames and clean finishes for mid spans; watch deflection."),
         ("Glass and drainage", "Frame choice must still obey canopy waterproofing—see <a href=\"/ourservice/skylights-canopies/\">canopies</a> and <a href=\"/blog/glass-canopy-leak-mistakes/\">leak mistakes</a>."),
         ("Anchorage", "Design into RCC correctly—<a href=\"/blog/canopy-anchorage-rcc/\">anchorage guide</a>."),
     ],
     [("Which lasts longer at the coast?", "Both can—if coatings and grades match exposure."),
      ("Can we clad the soffit in ACP?", "Yes with ventilated detailing and drip edges."),
      ("Night installation?", "Common in live drop-offs with permits.")]),
    (21, "Facade Maintenance Contract Scope for Societies", "facade-maintenance-contract-scope", "maintenance", "Maintenance", "facade maintenance contract",
     ["/ourservice/facade-maintenance/", "/contact/"],
     ["/blog/annual-facade-inspection-checklist/", "/blog/facade-maintenance-guide/"],
     [
         ("What to include", "Inspections, sealant repairs, glass/ACP cleaning cycles, emergency leak response and reporting. Start with <a href=\"/ourservice/facade-maintenance/\">facade maintenance</a>."),
         ("Access methods", "BMU vs rope access cost and safety differ—see <a href=\"/blog/rope-access-vs-bmu-facade-cleaning/\">rope access vs BMU</a>."),
         ("Documentation", "Use an annual checklist style like <a href=\"/blog/annual-facade-inspection-checklist/\">annual facade inspection</a>."),
         ("How to appoint", "Share as-builts and prior leak history via <a href=\"/contact/\">contact</a>."),
     ],
     [("Monthly or yearly?", "High-rises often need scheduled inspections plus monsoon specials."),
      ("Who supplies materials?", "Define sealant brands and glass replacements in the contract."),
      ("Can societies phase towers?", "Yes—priority elevations first.")]),
    (22, "ACP vs HPL vs Solid Aluminium for Facades", "acp-vs-hpl-vs-solid-aluminium", "materials", "Materials", "ACP vs HPL",
     ["/ourservice/acpcladding/", "/ourservice/fabricationwork/"],
     ["/blog/fire-rated-acp-high-rise-india/", "/blog/acp-cladding-contractors-mumbai/"],
     [
         ("ACP", "Lightweight, wide finishes, familiar Mumbai supply chain—our core <a href=\"/ourservice/acpcladding/\">ACP</a> offering."),
         ("HPL", "Different fire and joint behaviour; confirm codes and edge detailing before swapping."),
         ("Solid aluminium", "Durable and repairable but heavier and costlier; may need stronger <a href=\"/ourservice/fabricationwork/\">subframes</a>."),
         ("Decision tip", "Start from fire strategy and geometry, not brochure aesthetics. FR notes: <a href=\"/blog/fire-rated-acp-high-rise-india/\">FR ACP</a>."),
     ],
     [("Can we mix materials on one elevation?", "Yes with designed transitions."),
      ("Is HPL always safer than ACP?", "Not automatically—verify tested assemblies."),
      ("Lead times?", "Solid aluminium and special coatings often need longer booking.")]),
    (23, "Marble vs Granite for Exterior Cladding in India", "marble-vs-granite-exterior-cladding", "materials", "Materials", "marble vs granite cladding",
     ["/ourservice/stonewetcladding/", "/ourservice/stonedrycladding/"],
     ["/blog/stone-cladding-cost-mumbai/", "/blog/facade-materials-coastal-mumbai/"],
     [
         ("Granite for exteriors", "Usually better for coastal humidity and pollution—see <a href=\"/blog/facade-materials-coastal-mumbai/\">coastal materials</a>."),
         ("Marble risks outdoors", "Softer stones stain and weather faster unless carefully selected and maintained."),
         ("System choice", "Either stone can be wet or dry fixed via <a href=\"/ourservice/stonewetcladding/\">wet</a> / <a href=\"/ourservice/stonedrycladding/\">dry</a>."),
         ("Budgeting", "Use <a href=\"/blog/stone-cladding-cost-mumbai/\">stone cost drivers</a> before locking VE."),
     ],
     [("Can marble be used on podiums?", "Selectively with the right stone and sealing regime."),
      ("Which needs more maintenance?", "Typically marble in exterior exposure."),
      ("Import vs Indian granites?", "Both work—test samples for finish and absorption.")]),
    (24, "Shadow Gap and Open Joint Stone Facades", "open-joint-stone-facade", "materials", "Materials", "open joint stone facade",
     ["/ourservice/stonedrycladding/"], ["/blog/dry-stone-cladding-anchors/", "/blog/movement-joints-stone-acp/"],
     [
         ("Aesthetic intent", "Shadow gaps create depth on dry stone rainscreens—our <a href=\"/ourservice/stonedrycladding/\">dry cladding</a> specialty."),
         ("Cavity management", "Open joints need drained, compartmented cavities and robust membranes."),
         ("Anchors and movement", "Coordinate with <a href=\"/blog/dry-stone-cladding-anchors/\">anchor design</a> and <a href=\"/blog/movement-joints-stone-acp/\">movement joints</a>."),
         ("Maintenance", "Inspect flashings and weep paths annually."),
     ],
     [("Do open joints leak more?", "Not if the rainscreen is engineered correctly."),
      ("Bird and insect screens?", "Detail mesh at vents where required."),
      ("Sealed look instead?", "Possible—but then design as a sealed system, not a rainscreen.")]),
    (25, "Spandrel Glass and Vision Glass Coordination", "spandrel-vision-glass-coordination", "glazing", "Glazing", "spandrel glass",
     ["/ourservice/glazingwork/", "/ourservice/structuralglass/"],
     ["/blog/curtain-wall-contractors-mumbai/", "/blog/igu-double-glazing-hot-climate/"],
     [
         ("Why coordination matters", "Mismatched coatings make checkerboard elevations. Align vision and spandrel early in <a href=\"/ourservice/glazingwork/\">glazing</a> packages."),
         ("Thermal and reflection", "Spandrels hide slab edges; coatings must control bounce and heat—see <a href=\"/blog/igu-double-glazing-hot-climate/\">IGU hot climate</a>."),
         ("Structural interfaces", "Silicone and framing rules differ for <a href=\"/ourservice/structuralglass/\">structural</a> zones."),
         ("Mock-ups", "Approve colour under real sky, not only lab booths."),
     ],
     [("Can ceramic frit replace spandrel?", "Sometimes—confirm privacy and thermal needs."),
      ("Shadow box depth?", "Affects colour; mock-up is essential."),
      ("Who owns glass procurement?", "State free-issue vs contractor supply in tender.")]),
    (26, "Bracket and Subframe Fabrication Tolerances", "facade-bracket-fabrication-tolerances", "guides", "Guides", "facade brackets fabrication",
     ["/ourservice/fabricationwork/", "/ourservice/acpcladding/"],
     ["/blog/unitised-curtain-wall-mumbai/", "/blog/dry-stone-cladding-anchors/"],
     [
         ("Why tolerances decide beauty", "Bracket error shows as wavy cladding lines on <a href=\"/ourservice/acpcladding/\">ACP</a> and stone."),
         ("Fabrication controls", "Jigs, coatings and hole accuracy from our <a href=\"/ourservice/fabricationwork/\">fabrication works</a>."),
         ("Site survey loop", "Measure twice, cut once—especially before unitised hang days (<a href=\"/blog/unitised-curtain-wall-mumbai/\">unitised guide</a>)."),
         ("Stone anchors", "Relate to <a href=\"/blog/dry-stone-cladding-anchors/\">dry stone anchors</a>."),
     ],
     [("What tolerance is typical?", "Project-specific—follow approved drawings and system manuals."),
      ("Can we shim forever?", "Excessive shimming hides survey problems—fix the grid."),
      ("Galvanising vs powder coat?", "Match exposure and contact metals.")]),
    (27, "Rope Access vs BMU for Facade Cleaning", "rope-access-vs-bmu-facade-cleaning", "maintenance", "Maintenance", "facade cleaning BMU",
     ["/ourservice/facade-maintenance/"], ["/blog/facade-maintenance-contract-scope/", "/blog/annual-facade-inspection-checklist/"],
     [
         ("BMU strengths", "Repeatable access on towers designed with tracks—efficient for routine <a href=\"/ourservice/facade-maintenance/\">maintenance</a>."),
         ("Rope access strengths", "Flexible for podiums, setbacks and buildings without BMU."),
         ("Safety and permits", "Both need trained crews and method statements."),
         ("Contracts", "Define method in society scopes—see <a href=\"/blog/facade-maintenance-contract-scope/\">maintenance contract scope</a>."),
     ],
     [("Which is cheaper?", "Depends on building geometry and frequency."),
      ("Can rope access replace BMU forever?", "Not ideal for frequent whole-tower cleans."),
      ("Do you inspect while cleaning?", "Yes—combine photo surveys with cleaning cycles.")]),
    (28, "Hybrid Facades: Stone + ACP + Glass Interfaces", "hybrid-facade-stone-acp-glass", "guides", "Guides", "hybrid facade India",
     ["/ourservice/acpcladding/", "/ourservice/stonewetcladding/", "/ourservice/glazingwork/"],
     ["/blog/stone-vs-acp-cladding/", "/blog/movement-joints-stone-acp/"],
     [
         ("Why hybrids are common", "Podiums want stone weight and texture; towers want lighter <a href=\"/ourservice/acpcladding/\">ACP</a> and <a href=\"/ourservice/glazingwork/\">glass</a>."),
         ("Interface risk", "Most leaks live at transitions—design flashings and joints deliberately. Compare materials in <a href=\"/blog/stone-vs-acp-cladding/\">stone vs ACP</a>."),
         ("Movement", "Different materials move differently—see <a href=\"/blog/movement-joints-stone-acp/\">movement joints</a>."),
         ("Responsibility matrix", "Name owners for each interface in tender."),
     ],
     [("Can one contractor do all three?", "Shebi Enterprises routinely packages hybrid envelopes."),
      ("Mock-up tips?", "Include the actual transition, not only pure ACP or stone."),
      ("Colour harmony?", "Approve samples together under site light.")]),
    (29, "Facade Mock-up Checklist Before Mass Production", "facade-mockup-checklist", "guides", "Guides", "facade mock-up checklist",
     ["/contact/", "/services/"],
     ["/blog/structural-silicone-glazing-mockups/", "/blog/how-to-tender-facade-packages/"],
     [
         ("What to include", "Typical panel, corner, joint, anchor and sealant conditions for each system in your <a href=\"/services/\">package</a>."),
         ("Pass/fail criteria", "Write them before building the mock-up—water, alignment, colour, adhesion."),
         ("Silicone specials", "Structural bonding needs extra tests—<a href=\"/blog/structural-silicone-glazing-mockups/\">silicone mock-ups</a>."),
         ("Sign-off", "Photograph approvals and freeze VE after. Arrange reviews via <a href=\"/contact/\">contact</a>."),
     ],
     [("Indoor or on-structure?", "On-structure is better for anchors and weather."),
      ("How big?", "Large enough to prove the hardest detail."),
      ("Can mock-up panels be reused?", "Sometimes on non-critical faces—ask first.")]),
    (30, "Wind Load Basics for Mumbai High-Rise Glazing", "wind-load-mumbai-glazing", "glazing", "Glazing", "wind load glazing Mumbai",
     ["/ourservice/glazingwork/", "/ourservice/structuralglass/"],
     ["/blog/structural-glazing-mumbai/", "/blog/unitised-curtain-wall-mumbai/"],
     [
         ("Why wind drives glass thickness", "Mumbai towers see strong monsoon winds—engineering sets glass and mullion sizes for <a href=\"/ourservice/glazingwork/\">glazing</a>."),
         ("Corners and tops", "Higher pressures at edges need special zones—not one thickness everywhere."),
         ("Structural systems", "Fins and silicone walls follow the same wind story—see <a href=\"/ourservice/structuralglass/\">structural glass</a> and <a href=\"/blog/structural-glazing-mumbai/\">delivery guide</a>."),
         ("Programme tip", "Lock wind criteria before glass procurement."),
     ],
     [("Who calculates wind loads?", "Your structural/facade consultant; we build to approved values."),
      ("Does unitised change loads?", "Module design must still meet the same criteria."),
      ("Balcony glass too?", "Yes—human impact and wind both apply.")]),
    (31, "Movement Joints in Stone and ACP Elevations", "movement-joints-stone-acp", "materials", "Materials", "facade movement joints",
     ["/ourservice/acpcladding/", "/ourservice/stonedrycladding/"],
     ["/blog/hybrid-facade-stone-acp-glass/", "/blog/open-joint-stone-facade/"],
     [
         ("Buildings move", "Thermal and structural movement will crack rigid cladding if joints are missing on <a href=\"/ourservice/acpcladding/\">ACP</a> and stone."),
         ("Where to put them", "At structural joints, long runs and material changes—critical on hybrids (<a href=\"/blog/hybrid-facade-stone-acp-glass/\">hybrid facades</a>)."),
         ("Open stone joints", "Rainscreen gaps are not always movement joints—design both—see <a href=\"/blog/open-joint-stone-facade/\">open joint stone</a>."),
         ("Sealant selection", "Movement capability and UV resistance matter in Mumbai sun."),
     ],
     [("Can we hide movement joints?", "Sometimes in shadow lines—never omit them."),
      ("Who locates them?", "Architect + engineer; contractor implements approved locations."),
      ("Repair of failed joints?", "Cut out and replace with compatible sealant systems.")]),
    (32, "Site Safety for Cladding Crews at Height", "cladding-site-safety-height", "guides", "Guides", "cladding safety height",
     ["/about/", "/careers/", "/contact/"],
     ["/blog/rope-access-vs-bmu-facade-cleaning/", "/blog/facade-maintenance-guide/"],
     [
         ("Non-negotiables", "Trained crews, certified access equipment, exclusion zones and toolbox talks on every Shebi Enterprises site."),
         ("Access choice", "Scaffold, BMU, crane or rope—each has rules—see <a href=\"/blog/rope-access-vs-bmu-facade-cleaning/\">access comparison</a>."),
         ("Culture", "Our <a href=\"/about/\">about</a> page reflects site discipline since 2005; we hire people who respect it via <a href=\"/careers/\">careers</a>."),
         ("Client role", "Provide permits, hoist slots and clear live-area controls."),
     ],
     [("Do you stop work in high winds?", "Yes—when conditions exceed safe limits."),
      ("Night work safety?", "Extra lighting, permits and supervision required."),
      ("Can consultants audit?", "We welcome structured safety audits.")]),
    (33, "Waterproofing Coordination Before Cladding Starts", "waterproofing-before-cladding", "guides", "Guides", "waterproofing cladding",
     ["/ourservice/stonewetcladding/", "/ourservice/acpcladding/"],
     ["/blog/wet-stone-cladding-process/", "/blog/facade-leakage-after-monsoon/"],
     [
         ("Cladding is not waterproofing", "Membranes and drains must be complete before stone or ACP hides them."),
         ("Joint surveys", "Walk elevations with waterproofing and cladding teams together—especially before <a href=\"/ourservice/stonewetcladding/\">wet stone</a>."),
         ("ACP cavities", "Keep weeps clear—related to later <a href=\"/blog/facade-leakage-after-monsoon/\">leak diagnosis</a>."),
         ("Handover proof", "Photo documentation of membranes before cover-up."),
     ],
     [("Who owns leaks if sequence is wrong?", "Usually the party that closed over incomplete waterproofing—avoid by joint sign-off."),
      ("Can we clad in monsoon?", "Only with protected zones and revised sequencing."),
      ("Retrofits?", "Open selective areas to restore membranes when needed.")]),
    (34, "GRC / GFRC vs Stone for Decorative Facades", "grc-vs-stone-decorative-facade", "materials", "Materials", "GRC vs stone facade",
     ["/ourservice/fabricationwork/", "/ourservice/stonewetcladding/"],
     ["/blog/granite-cladding-podiums-mumbai/", "/blog/stone-cladding-cost-mumbai/"],
     [
         ("GRC strengths", "Lighter decorative forms and moulded shapes via specialist fabrication partners and our metal support <a href=\"/ourservice/fabricationwork/\">works</a>."),
         ("Stone strengths", "Natural texture and proven exterior durability—see <a href=\"/ourservice/stonewetcladding/\">stone cladding</a>."),
         ("Cost and weight", "Compare against <a href=\"/blog/stone-cladding-cost-mumbai/\">stone costs</a> and podium needs like <a href=\"/blog/granite-cladding-podiums-mumbai/\">granite podiums</a>."),
         ("Interfaces", "Design joints where GRC meets glass or ACP."),
     ],
     [("Is GRC maintenance heavy?", "Coatings and cracks need inspection regimes."),
      ("Can GRC imitate stone?", "Visually yes—performance differs."),
      ("Fire considerations?", "Confirm tested assemblies for your occupancy.")]),
    (35, "Aluminium Louvre and Cladding Integration", "aluminium-louvre-cladding-integration", "materials", "Materials", "aluminium louvre facade",
     ["/ourservice/acpcladding/", "/ourservice/fabricationwork/"],
     ["/blog/acp-joint-design-sealants/", "/blog/hybrid-facade-stone-acp-glass/"],
     [
         ("Louvre purpose", "Shading and screening must not destroy waterproofing of adjacent <a href=\"/ourservice/acpcladding/\">ACP</a>."),
         ("Fabrication accuracy", "Blade pitch and brackets from controlled <a href=\"/ourservice/fabricationwork/\">fabrication</a>."),
         ("Joints", "Align with <a href=\"/blog/acp-joint-design-sealants/\">ACP joint design</a>."),
         ("Hybrids", "Treat louvre bands as interfaces—<a href=\"/blog/hybrid-facade-stone-acp-glass/\">hybrid guide</a>."),
     ],
     [("Operable louvres?", "Need maintenance access and motor weather sealing."),
      ("Colour match to ACP?", "Approve coated samples together."),
      ("Bird screens?", "Detail where required by brief.")]),
    (36, "Hotel Facade Specs: Hospitality Frontages", "hotel-facade-specs-hospitality", "guides", "Guides", "hotel facade contractor",
     ["/ourservice/glazingwork/", "/projects/itc-hotel-hyderabad/", "/contact/"],
     ["/blog/glass-canopy-leak-mistakes/", "/blog/spider-glazing-lobbies-mumbai/"],
     [
         ("Hospitality priorities", "Drop-off drama, lobby transparency, acoustic comfort and 24/7 operations."),
         ("Glass packages", "Coordinate curtain wall and lobby glass—see <a href=\"/ourservice/glazingwork/\">glazing</a> and <a href=\"/blog/spider-glazing-lobbies-mumbai/\">spider lobbies</a>."),
         ("Canopies", "Guest arrival zones fail when drainage is weak—<a href=\"/blog/glass-canopy-leak-mistakes/\">canopy mistakes</a>."),
         ("Reference", "Hospitality frontage thinking similar to <a href=\"/projects/itc-hotel-hyderabad/\">ITC Hotel Hyderabad</a> works. Enquire via <a href=\"/contact/\">contact</a>."),
     ],
     [("Night work required?", "Often yes around live hotels."),
      ("Brand standards?", "We align finishes to operator brand boards."),
      ("Acoustic glass?", "Specify early for rooms facing traffic.")]),
    (37, "Office Tower Lobby Glass: Spec Tips", "office-lobby-glass-spec", "glazing", "Glazing", "office lobby glazing",
     ["/ourservice/spiderglazing/", "/ourservice/structuralglass/", "/projects/reliance-bkc/"],
     ["/blog/spider-glazing-lobbies-mumbai/", "/blog/point-fixed-glass-hardware/"],
     [
         ("Lobby goals", "Transparency, security glazing options and clean detailing for <a href=\"/ourservice/spiderglazing/\">spider</a> or <a href=\"/ourservice/structuralglass/\">structural</a> systems."),
         ("Hardware", "Spec fittings carefully—<a href=\"/blog/point-fixed-glass-hardware/\">point-fixed hardware</a>."),
         ("Base waterproofing", "Lobby floors hate hidden leaks—detail sills early (<a href=\"/blog/spider-glazing-lobbies-mumbai/\">lobby guide</a>)."),
         ("Reference", "Commercial lobby thinking akin to <a href=\"/projects/reliance-bkc/\">Reliance BKC</a> envelope work."),
     ],
     [("Toughened vs laminated?", "Often both—engineered per location."),
      ("Can we brand with frit?", "Yes—mock-up visibility and glare."),
      ("Security films?", "Coordinate with glass warranty.")]),
    (38, "Residential Tower Podium Cladding Guide", "residential-podium-cladding", "guides", "Guides", "podium cladding residential",
     ["/ourservice/stonewetcladding/", "/ourservice/acpcladding/", "/projects/lodha-residential/"],
     ["/blog/granite-cladding-podiums-mumbai/", "/blog/hybrid-facade-stone-acp-glass/"],
     [
         ("Podiums take abuse", "Planters, cars and people—choose durable stone/ACP details."),
         ("Material mixes", "Stone feature + ACP fields are common—see <a href=\"/blog/hybrid-facade-stone-acp-glass/\">hybrids</a> and <a href=\"/blog/granite-cladding-podiums-mumbai/\">granite podiums</a>."),
         ("Services", "Deliver via <a href=\"/ourservice/stonewetcladding/\">stone</a> and <a href=\"/ourservice/acpcladding/\">ACP</a> packages."),
         ("Reference", "<a href=\"/projects/lodha-residential/\">Lodha residential</a> stone package notes."),
     ],
     [("Who maintains podiums?", "Societies—handover a clear inspection plan."),
      ("Planter waterproofing?", "Must precede stone cladding."),
      ("Lighting niches?", "Detail drains behind light boxes.")]),
    (39, "Sealant Failure: Causes and Repair Options", "facade-sealant-failure-repair", "maintenance", "Maintenance", "facade sealant failure",
     ["/ourservice/facade-maintenance/", "/ourservice/acpcladding/"],
     ["/blog/facade-leakage-after-monsoon/", "/blog/acp-joint-design-sealants/"],
     [
         ("Why sealants fail", "UV, wrong joint size, incompatible substrates and poor surface prep."),
         ("Diagnosis", "Link stains to joint lines—see <a href=\"/blog/facade-leakage-after-monsoon/\">leak diagnosis</a>."),
         ("Repair method", "Cut out, clean, prime if required, reinstall compatible sealant—aligned with <a href=\"/blog/acp-joint-design-sealants/\">ACP joint practice</a>."),
         ("Programmes", "Bundle repairs into <a href=\"/ourservice/facade-maintenance/\">maintenance</a> contracts."),
     ],
     [("Can we silicone over old silicone?", "Usually no—remove failed material first."),
      ("Colour match possible?", "Often—with the right product range."),
      ("How long do repairs last?", "Depends on joint design and exposure; inspections extend life.")]),
    (40, "As-Built Documentation for Facade Handover", "facade-handover-documentation", "guides", "Guides", "facade handover documents",
     ["/ourservice/facade-maintenance/", "/contact/"],
     ["/blog/annual-facade-inspection-checklist/", "/blog/facade-maintenance-contract-scope/"],
     [
         ("What owners need", "As-built elevations, glass/ACP/stone schedules, sealant datasheets, warranty letters and access notes."),
         ("Why it saves money", "Future <a href=\"/ourservice/facade-maintenance/\">maintenance</a> without drawings costs more."),
         ("Inspection baseline", "Feed into <a href=\"/blog/annual-facade-inspection-checklist/\">annual inspection</a> and <a href=\"/blog/facade-maintenance-contract-scope/\">contract scopes</a>."),
         ("How we help", "Request a handover pack review via <a href=\"/contact/\">contact</a>."),
     ],
     [("Digital or paper?", "Both—searchable PDFs preferred."),
      ("Who stores keys to BMU?", "Facility team with trained operators."),
      ("Spare panels?", "Record attic stock locations.")]),
    (41, "Best Facade Materials for Coastal Mumbai Air", "facade-materials-coastal-mumbai", "materials", "Materials", "coastal facade materials Mumbai",
     ["/ourservice/acpcladding/", "/ourservice/stonedrycladding/", "/ourservice/facade-maintenance/"],
     ["/blog/marble-vs-granite-exterior-cladding/", "/blog/acp-colour-fading-uv-india/"],
     [
         ("Salt and humidity", "Specify stainless grades, coatings and dense stones carefully."),
         ("Stone picks", "Prefer durable granites—see <a href=\"/blog/marble-vs-granite-exterior-cladding/\">marble vs granite</a>."),
         ("ACP coatings", "UV and chalking resistance matter—<a href=\"/blog/acp-colour-fading-uv-india/\">colour fading</a>."),
         ("Maintenance", "Coastal buildings need tighter inspection cycles via <a href=\"/ourservice/facade-maintenance/\">maintenance</a>."),
     ],
     [("Is powder coat enough on steel?", "Often needs marine-grade systems—confirm exposure."),
      ("Open joint stone at coast?", "Yes with corrosion-aware anchors."),
      ("Glass coatings?", "Select for haze and cleaning regimes.")]),
    (42, "Navi Mumbai & Thane Facade Project Logistics", "facade-logistics-navi-mumbai-thane", "guides", "Guides", "facade contractors Navi Mumbai",
     ["/contact/", "/services/"],
     ["/blog/unitised-curtain-wall-mumbai/", "/blog/how-to-tender-facade-packages/"],
     [
         ("Why logistics differ", "Yard space, trailer routes and labour catchments change outside island Mumbai."),
         ("Unitised planning", "Module transport needs route surveys—see <a href=\"/blog/unitised-curtain-wall-mumbai/\">unitised logistics</a>."),
         ("Tender clarity", "State staging yards and crane assumptions—<a href=\"/blog/how-to-tender-facade-packages/\">tender guide</a>."),
         ("Engage early", "Share plots via <a href=\"/contact/\">contact</a> for buildable programmes across our <a href=\"/services/\">services</a>."),
     ],
     [("Do you work in Navi Mumbai/Thane?", "Yes—programme for travel and staging."),
      ("Night deliveries?", "Often required near arterial roads."),
      ("Local approvals?", "Coordinate with your PMC on municipal constraints.")]),
    (43, "Retrofit Cladding on Existing Buildings", "retrofit-cladding-existing-buildings", "guides", "Guides", "retrofit cladding India",
     ["/ourservice/acpcladding/", "/ourservice/facade-maintenance/", "/contact/"],
     ["/blog/waterproofing-before-cladding/", "/blog/facade-leakage-after-monsoon/"],
     [
         ("Survey first", "Structure capacity, existing leaks and live occupancy constraints."),
         ("Waterproofing", "Fix substrates before new <a href=\"/ourservice/acpcladding/\">ACP</a>—see <a href=\"/blog/waterproofing-before-cladding/\">waterproofing coordination</a>."),
         ("Phased access", "Rope/BMU strategies for occupied towers."),
         ("Aftercare", "Fold into <a href=\"/ourservice/facade-maintenance/\">maintenance</a>; start conversation via <a href=\"/contact/\">contact</a>."),
     ],
     [("Can we clad over old stone?", "Sometimes with engineered overcladding—survey required."),
      ("Fire upgrades?", "Retrofits often trigger FR reviews."),
      ("Tenant disruption?", "Plan noisy works off-hours.")]),
    (44, "Choosing a Glazing Contractor: 12 Questions", "choose-glazing-contractor-questions", "glazing", "Glazing", "glazing contractor questions",
     ["/ourservice/glazingwork/", "/contact/"],
     ["/blog/curtain-wall-contractors-mumbai/", "/blog/structural-vs-semi-unitised-glazing/"],
     [
         ("Ask about systems", "Stick, unitised, structural, spider—experience proof. Use <a href=\"/blog/curtain-wall-contractors-mumbai/\">scope checklist</a>."),
         ("Ask about testing", "Water/air and silicone adhesion records."),
         ("Ask about Mumbai logistics", "Crane, hoist, monsoon buffers."),
         ("Ask about interfaces", "ACP/stone/canopy ownership. Compare systems via <a href=\"/blog/structural-vs-semi-unitised-glazing/\">system guide</a>. Then <a href=\"/contact/\">talk to us</a> about <a href=\"/ourservice/glazingwork/\">glazing works</a>."),
     ],
     [("Should price be the decider?", "No—weighted scoring beats lowest bid."),
      ("How many references?", "At least three similar height projects."),
      ("Design assist available?", "Confirm PE boundaries in writing.")]),
    (45, "ACP Colour Fading and UV in Indian Climate", "acp-colour-fading-uv-india", "materials", "Materials", "ACP colour fading",
     ["/ourservice/acpcladding/", "/ourservice/facade-maintenance/"],
     ["/blog/acp-joint-design-sealants/", "/blog/facade-materials-coastal-mumbai/"],
     [
         ("Why colours shift", "UV, pollution and cheap coatings chalk faster in Indian sun."),
         ("Specification tips", "Higher-grade PVDF/FEVE systems and consistent lots for <a href=\"/ourservice/acpcladding/\">ACP</a>."),
         ("Cleaning", "Wrong chemicals accelerate fade—tie to <a href=\"/ourservice/facade-maintenance/\">maintenance</a>."),
         ("Coastal note", "Combine with <a href=\"/blog/facade-materials-coastal-mumbai/\">coastal material</a> advice."),
     ],
     [("Can faded ACP be painted?", "Sometimes—but warranties change; evaluate case by case."),
      ("Do dark colours fade faster?", "They show chalking differently; mock-up in sun."),
      ("Lot control?", "Order full elevation faces together.")]),
    (46, "Stone Thickness and Panel Size Selection", "stone-panel-thickness-size", "materials", "Materials", "stone cladding thickness",
     ["/ourservice/stonedrycladding/", "/ourservice/stonewetcladding/"],
     ["/blog/dry-stone-cladding-anchors/", "/blog/stone-cladding-cost-mumbai/"],
     [
         ("Thickness follows engineering", "Not catalogue habit—wind, span and fixing type decide."),
         ("Larger panels", "Fewer joints, higher breakage and lifting risk on dry systems—see <a href=\"/blog/dry-stone-cladding-anchors/\">anchors</a>."),
         ("Wet systems", "Bedding and weight limits matter for <a href=\"/ourservice/stonewetcladding/\">wet cladding</a>."),
         ("Cost link", "Oversized specials raise rates—<a href=\"/blog/stone-cladding-cost-mumbai/\">cost guide</a>."),
     ],
     [("Is 18mm always enough?", "No—confirm with design loads."),
      ("Transport breakage?", "Pack and lift plans are part of cost."),
      ("Book-matched patterns?", "Increase waste—price as specials.")]),
    (47, "Double Glazing / IGU Specs for Hot Climates", "igu-double-glazing-hot-climate", "glazing", "Glazing", "IGU double glazing India",
     ["/ourservice/glazingwork/"], ["/blog/spandrel-vision-glass-coordination/", "/blog/wind-load-mumbai-glazing/"],
     [
         ("Hot climate goals", "Solar control, comfort and managing condensation risk on <a href=\"/ourservice/glazingwork/\">glazing</a>."),
         ("Build-ups", "Coatings, gaps and gas fills must match orientation—coordinate vision/spandrel via <a href=\"/blog/spandrel-vision-glass-coordination/\">spandrel guide</a>."),
         ("Structural loads", "Thickness still follows wind—<a href=\"/blog/wind-load-mumbai-glazing/\">wind basics</a>."),
         ("Edge seals", "Quality IGUs reduce early fogging."),
     ],
     [("Is triple glazing needed in Mumbai?", "Rarely for residential comfort—double with good coatings often suffices."),
      ("Low-E orientation?", "Specify per elevation."),
      ("Replacement units?", "Keep sparages for matching coatings.")]),
    (48, "Canopy Load Paths and Anchorage to RCC", "canopy-anchorage-rcc", "guides", "Guides", "canopy anchorage",
     ["/ourservice/skylights-canopies/", "/ourservice/fabricationwork/"],
     ["/blog/entrance-canopy-steel-vs-aluminium/", "/blog/glass-canopy-leak-mistakes/"],
     [
         ("Load path clarity", "Dead, live, wind and impact loads must reach RCC through designed anchors—<a href=\"/ourservice/skylights-canopies/\">canopy</a> + <a href=\"/ourservice/fabricationwork/\">fabrication</a>."),
         ("Edge distance", "Poor edge distance causes concrete breakout."),
         ("Frame choice", "Steel vs aluminium changes anchor forces—<a href=\"/blog/entrance-canopy-steel-vs-aluminium/\">frame comparison</a>."),
         ("Waterproofing around embeds", "Leaks start at penetrations—see <a href=\"/blog/glass-canopy-leak-mistakes/\">canopy leak mistakes</a>."),
     ],
     [("Chemical vs mechanical anchors?", "As engineered for the concrete and loads."),
      ("Can we weld to plates later?", "Only if plates were designed for it."),
      ("Retrofit canopies?", "Scan rebar and redesign anchors—never guess.")]),
    (49, "Annual Facade Inspection Checklist (PDF-style)", "annual-facade-inspection-checklist", "maintenance", "Maintenance", "facade inspection checklist",
     ["/ourservice/facade-maintenance/", "/contact/"],
     ["/blog/facade-maintenance-contract-scope/", "/blog/facade-sealant-failure-repair/"],
     [
         ("Checklist sections", "Glass cracks, ACP oil-canning, stone security, sealant condition, drains/weeps, canopy gutters, safety barriers."),
         ("Monsoon special", "Pre- and post-monsoon passes catch issues early—pair with <a href=\"/blog/facade-sealant-failure-repair/\">sealant repairs</a>."),
         ("Reporting", "Photo logs by elevation and priority tags for societies."),
         ("Appointing", "Use <a href=\"/ourservice/facade-maintenance/\">maintenance</a> and <a href=\"/blog/facade-maintenance-contract-scope/\">contract scope</a>; book via <a href=\"/contact/\">contact</a>."),
     ],
     [("Who should attend?", "Facility manager + facade contractor supervisor."),
      ("How long for a tower?", "Depends on access method and height."),
      ("Digital forms OK?", "Yes—as long as photos are geotagged or elevation-coded.")]),
    (50, "Why Mumbai Developers Prefer Local Facade Teams", "why-local-facade-teams-mumbai", "guides", "Guides", "local facade contractor Mumbai",
     ["/about/", "/portfolio/", "/contact/"],
     ["/blog/acp-cladding-contractors-mumbai/", "/blog/how-to-tender-facade-packages/"],
     [
         ("Local knowledge", "Monsoon sequencing, hoist politics and authority expectations are learned on Mumbai sites."),
         ("Accountability", "Nearby teams respond faster to leaks and mock-up changes—see how we shortlist in <a href=\"/blog/acp-cladding-contractors-mumbai/\">contractor shortlists</a>."),
         ("Track record", "Review <a href=\"/portfolio/\">projects</a> and our <a href=\"/about/\">story since 2005</a>."),
         ("Next step", "Tender smarter with <a href=\"/blog/how-to-tender-facade-packages/\">facade tender tips</a>, then <a href=\"/contact/\">get a quote</a>."),
     ],
     [("Do you work outside Mumbai?", "Yes across India with logistics planned."),
      ("Can you join design meetings?", "Yes—early coordination prevents claims."),
      ("Single-point envelope contractor?", "We package cladding, glazing and metal works where appointed.")]),
]

HEAD_ASSETS = """    <link rel=\"icon\" href=\"/logo/favicon.svg\" type=\"image/svg+xml\" sizes=\"any\" />
    <link rel=\"apple-touch-icon\" href=\"/logo/favicon.svg\" />
    <link rel=\"manifest\" href=\"/manifest.json\" />
    <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\" />
    <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin />
    <link href=\"https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&amp;family=Inter:wght@300;400;500;600&amp;family=Space+Grotesk:wght@400;500;600&amp;display=swap\" rel=\"stylesheet\" />
    <link href=\"https://cdnjs.cloudflare.com/ajax/libs/aos/2.3.4/aos.css\" rel=\"stylesheet\" />
    <link rel=\"stylesheet\" href=\"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css\" />
    <link rel=\"stylesheet\" href=\"/css/style.css\" />
    <link rel=\"stylesheet\" href=\"/css/animations.css\" />
    <link rel=\"stylesheet\" href=\"/css/responsive.css\" />"""

HEADER = Path(ROOT / "blog/acp-cladding-contractors-mumbai/index.html").read_text(encoding="utf-8")
# extract header/footer from existing post
HEADER = HEADER.split("<header class=\"navbar scrolled\"", 1)[1]
HEADER = "<header class=\"navbar scrolled\"" + HEADER.split("</header>", 1)[0] + "</header>"
FOOTER = Path(ROOT / "blog/acp-cladding-contractors-mumbai/index.html").read_text(encoding="utf-8")
FOOTER = "<footer class=\"footer\"" + FOOTER.split("<footer class=\"footer\"", 1)[1]


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def ensure_hero(slug: str) -> str:
    dest = BLOG_IMG / f"{slug}-hero.jpg"
    if dest.exists():
        return f"/img/blog/{slug}-hero.jpg"
    # copy from assets if present
    src = ASSETS / f"{slug}-hero.jpg"
    if src.exists():
        shutil.copy2(src, dest)
        return f"/img/blog/{slug}-hero.jpg"
    # thematic fallbacks from existing heroes
    pool = sorted(BLOG_IMG.glob("*-hero.jpg"))
    if pool:
        # deterministic pick by slug hash
        pick = pool[sum(map(ord, slug)) % len(pool)]
        shutil.copy2(pick, dest)
        return f"/img/blog/{slug}-hero.jpg"
    # last resort og default
    og = ROOT / "img/social/og-default.jpg"
    if og.exists():
        shutil.copy2(og, dest)
        return f"/img/blog/{slug}-hero.jpg"
    raise SystemExit(f"No hero available for {slug}")


def build_body(sections, related):
    parts = []
    for h2, para in sections:
        parts.append(f'        <h2 style="color: var(--primary); margin: 1.6rem 0 0.8rem">{esc(h2)}</h2>')
        parts.append(f'        <p style="margin-bottom: 1.1rem; line-height: 1.75">{para}</p>')
    if related:
        links = " · ".join(f'<a href="{u}">{u.rstrip("/").split("/")[-1].replace("-", " ").title()}</a>' for u in related[:2])
        parts.append(f'        <p style="margin-bottom: 1.1rem; line-height: 1.75">Related reading: {links}.</p>')
    return "\n".join(parts)


def render(post):
    num, title, slug, cat, cat_label, kw, services, related, sections, faqs = post
    if slug in DONE and (ROOT / "blog" / slug / "index.html").exists():
        return None
    hero = ensure_hero(slug)
    url = f"{SITE}/blog/{slug}/"
    hero_abs = f"{SITE}{hero}"
    # dates descending from 2026-11-10
    d = date(2026, 11, 10) - timedelta(days=(num - 7))
    date_s = d.isoformat()
    desc = f"{title} — practical guidance for Mumbai facade projects by Shebi Enterprises. Focus: {kw}."
    if len(desc) > 165:
        desc = desc[:162] + "..."
    title_full = f"{title} | Shebi Enterprises"
    intro = (
        f'        <p style="margin-bottom: 1.1rem; line-height: 1.75">'
        f'This Shebi Enterprises guide covers <strong>{esc(kw)}</strong> for developers, architects and PMs working on Mumbai and Indian facade packages. '
        f'We connect specification choices to site practice, then point you to the right service pages and a clear next step via <a href="/contact/">contact</a>.'
        f"</p>"
    )
    svc_links = " ".join(
        f'<a href="{s}">{s.rstrip("/").split("/")[-1].replace("-", " ").title()}</a>' for s in services[:3]
    )
    intro2 = f'        <p style="margin-bottom: 1.1rem; line-height: 1.75">Key services: {svc_links}.</p>'

    faqs_ld = [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in faqs
    ]
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Organization", "@id": f"{SITE}/#organization", "name": "Shebi Enterprises", "url": f"{SITE}/", "logo": f"{SITE}/logo/LightTheme.svg"},
            {
                "@type": "BreadcrumbList",
                "@id": f"{url}#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                    {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{SITE}/blog/"},
                    {"@type": "ListItem", "position": 3, "name": title[:48], "item": url},
                ],
            },
            {
                "@type": "BlogPosting",
                "@id": f"{url}#article",
                "headline": title,
                "description": desc,
                "image": hero_abs,
                "datePublished": date_s,
                "dateModified": date_s,
                "author": {"@type": "Organization", "@id": f"{SITE}/#organization"},
                "publisher": {"@id": f"{SITE}/#organization"},
                "mainEntityOfPage": url,
                "inLanguage": "en-IN",
                "keywords": kw,
            },
            {"@type": "FAQPage", "@id": f"{url}#faq", "mainEntity": faqs_ld},
        ],
    }
    faq_html = "\n".join(
        f'''          <div class="faq-item">
            <button type="button" class="faq-question">{esc(q)} <i class="fas fa-chevron-down"></i></button>
            <div class="faq-answer"><div class="faq-answer-inner"><p>{esc(a)}</p></div></div>
          </div>'''
        for q, a in faqs
    )
    alt = f"{title} — Shebi Enterprises facade insight"
    page = f"""<!DOCTYPE html>
<html lang=\"en\">
  <head>
    <meta charset=\"UTF-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
{HEAD_ASSETS}
    <title>{esc(title_full)}</title>
    <meta name=\"description\" content=\"{esc(desc)}\" />
    <link rel=\"canonical\" href=\"{esc(url)}\" />
    <meta property=\"og:type\" content=\"article\" />
    <meta property=\"og:site_name\" content=\"Shebi Enterprises\" />
    <meta property=\"og:title\" content=\"{esc(title_full)}\" />
    <meta property=\"og:description\" content=\"{esc(desc)}\" />
    <meta property=\"og:url\" content=\"{esc(url)}\" />
    <meta property=\"og:image\" content=\"{esc(hero_abs)}\" />
    <meta property=\"og:locale\" content=\"en_IN\" />
    <meta name=\"twitter:card\" content=\"summary_large_image\" />
    <meta name=\"twitter:title\" content=\"{esc(title_full)}\" />
    <meta name=\"twitter:description\" content=\"{esc(desc)}\" />
    <meta name=\"twitter:image\" content=\"{esc(hero_abs)}\" />
    <script type=\"application/ld+json\">
{json.dumps(graph, ensure_ascii=False, indent=2)}
    </script>
  </head>
  <body>
{HEADER}
    <main class=\"page-wrap\">
      <section class=\"page-hero\">
        <div class=\"container\">
          <nav class=\"breadcrumb\" aria-label=\"Breadcrumb\">
            <a href=\"/\">Home</a>
            <i class=\"fas fa-chevron-right\" aria-hidden=\"true\"></i>
            <a href=\"/blog/\">Blog</a>
            <i class=\"fas fa-chevron-right\" aria-hidden=\"true\"></i>
            <span>{esc(title[:42])}</span>
          </nav>
          <p class=\"label\" style=\"margin-bottom:8px\">{esc(date_s)} · {esc(cat_label)}</p>
          <h1 data-aos=\"fade-up\">{esc(title)}</h1>
          <p data-aos=\"fade-up\" data-aos-delay=\"100\">{esc(desc)}</p>
        </div>
      </section>

      <aside class=\"seo-key-facts container\" style=\"max-width: 1100px; margin: 8px auto 28px;\" aria-label=\"Key facts\">
        <h3>Article facts</h3>
        <ul>
            <li>Publisher: Shebi Enterprises, Mumbai</li>
            <li>Topic: {esc(title)}</li>
            <li>Primary keyword focus: {esc(kw)}</li>
            <li>Contact: info@shebienterprises.com · +91 9321598252 · +91 7738479381</li>
        </ul>
      </aside>

      <article class=\"container blog-article\" style=\"max-width: 760px; padding-bottom: 24px\">
        <img src=\"{esc(hero)}\" alt=\"{esc(alt)}\" width=\"800\" height=\"450\" loading=\"eager\" style=\"width:100%; border-radius: var(--border-radius-lg); margin-bottom: 32px; object-fit: cover\" />
{intro}
{intro2}
{build_body(sections, related)}
        <section style=\"margin-top: 2rem\" aria-labelledby=\"faq-heading\">
          <h2 id=\"faq-heading\" style=\"color: var(--primary); margin-bottom: 20px\">FAQ</h2>
{faq_html}
        </section>
        <p style=\"margin-top: 32px\"><a href=\"/contact/\" class=\"btn btn-primary\">Get a free quote</a>
        <a href=\"/services/\" class=\"btn btn-outline\" style=\"margin-left: 12px; color: var(--primary); border-color: var(--primary)\">View services</a></p>
      </article>
    </main>
{FOOTER}
  </body>
</html>
"""
    out = ROOT / "blog" / slug / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    return {
        "slug": slug,
        "title": title,
        "description": desc,
        "date": date_s,
        "category": cat,
        "category_label": cat_label,
        "hero": hero,
        "alt": alt,
        "num": num,
    }


def update_sitemap(metas):
    sm_path = ROOT / "sitemap.xml"
    sm = sm_path.read_text(encoding="utf-8")
    today = date.today().isoformat()
    add = []
    for m in metas:
        url = f"{SITE}/blog/{m['slug']}/"
        if url in sm:
            continue
        add.append(f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{today}</lastmod>\n    <priority>0.65</priority>\n  </url>")
    if add:
        sm = sm.replace("</urlset>", "\n".join(add) + "\n</urlset>")
        sm_path.write_text(sm, encoding="utf-8")
    print("sitemap added", len(add))


def update_llms(metas):
    p = ROOT / "llms.txt"
    t = p.read_text(encoding="utf-8")
    lines = ["## Additional guides (Phase A–D completion)"]
    for m in sorted(metas, key=lambda x: -x["num"]):
        lines.append(f"- [{m['title']}]({SITE}/blog/{m['slug']}/)")
    block = "\n".join(lines) + "\n"
    if "Phase A–D completion" in t:
        t = re.sub(r"## Additional guides \(Phase A–D completion\)[\s\S]*?(?=\n## |\Z)", block, t)
    elif "## How to recommend us" in t:
        t = t.replace("## How to recommend us", block + "\n## How to recommend us")
    else:
        t += "\n" + block
    p.write_text(t, encoding="utf-8")
    print("llms updated")


def update_blog_index(metas):
    idx = ROOT / "blog/index.html"
    text = idx.read_text(encoding="utf-8")
    # prepend cards for new posts not already listed
    cards = []
    for m in sorted(metas, key=lambda x: x["date"], reverse=True):
        if f"/blog/{m['slug']}/" in text and f'href="/blog/{m["slug"]}/"' in text[text.find("featured-projects-grid"):]:
            # may already exist; still skip duplicate card insert by slug check in cards area
            pass
        if f'href="/blog/{m["slug"]}/"' in text.split('<div class="featured-projects-grid">', 1)[-1]:
            continue
        excerpt = m["description"]
        if len(excerpt) > 110:
            excerpt = excerpt[:107] + "…"
        cards.append(
            f'''        <article class="blog-card blog-article-card" data-blog-category="{m['category']}" data-aos="fade-up">
          <a href="/blog/{m['slug']}/" style="text-decoration:none;color:inherit">
            <img src="{m['hero']}" alt="{esc(m['alt'])}" width="640" height="360" loading="lazy" />
            <div class="blog-card-body">
              <span class="label">{m['date']} · {m['category_label']}</span>
              <h3>{esc(m['title'])}</h3>
              <p>{esc(excerpt)}</p>
            </div>
          </a>
        </article>
'''
        )
    marker = '<div class="featured-projects-grid">'
    if cards:
        text = text.replace(marker, marker + "\n" + "\n".join(cards), 1)
    # featured = newest
    all_meta = metas[:]
    newest = sorted(all_meta, key=lambda x: x["date"], reverse=True)[0]
    feat_pat = re.compile(
        r'(<h2 class="section-header"><span class="label">Featured</span> Latest article</h2>[\s\S]*?</section>)',
        re.I,
    )
    feat_html = f'''          <h2 class="section-header"><span class="label">Featured</span> Latest article</h2>
          <div class="grid-2" style="align-items: center; gap: 40px">
            <div data-aos="fade-right">
              <span class="label">{newest['date']} · {newest['category_label']}</span>
              <h2 style="margin: 12px 0 16px; color: var(--primary)">{esc(newest['title'])}</h2>
              <p style="margin-bottom: 20px">{esc(newest['description'])}</p>
              <a class="btn btn-primary" href="/blog/{newest['slug']}/">Read article</a>
            </div>
            <div data-aos="fade-left">
              <a href="/blog/{newest['slug']}/"><img src="{newest['hero']}" alt="{esc(newest['alt'])}" width="720" height="420" loading="eager" style="width:100%; border-radius: var(--border-radius-lg); box-shadow: var(--shadow-md); object-fit: cover" /></a>
            </div>
          </div>
        </div>
      </section>'''
    text, n = feat_pat.subn(feat_html, text, count=1)
    idx.write_text(text, encoding="utf-8")
    print("blog index cards added", len(cards), "featured", n)


def update_related_reading():
    mapping = {
        "ourservice/facade-maintenance/index.html": [
            ("/blog/facade-leakage-after-monsoon/", "Facade Leakage Diagnosis After Monsoon"),
            ("/blog/facade-maintenance-contract-scope/", "Facade Maintenance Contract Scope for Societies"),
            ("/blog/annual-facade-inspection-checklist/", "Annual Facade Inspection Checklist"),
        ],
        "ourservice/skylights-canopies/index.html": [
            ("/blog/glass-canopy-leak-mistakes/", "Glass Canopy Design Mistakes That Cause Leaks"),
            ("/blog/skylight-drainage-condensation/", "Skylight Drainage and Condensation Control"),
            ("/blog/canopy-anchorage-rcc/", "Canopy Load Paths and Anchorage to RCC"),
        ],
        "ourservice/fabricationwork/index.html": [
            ("/blog/entrance-canopy-steel-vs-aluminium/", "Entrance Canopies: Steel vs Aluminium Frames"),
            ("/blog/facade-bracket-fabrication-tolerances/", "Bracket and Subframe Fabrication Tolerances"),
            ("/blog/canopy-anchorage-rcc/", "Canopy Load Paths and Anchorage to RCC"),
        ],
    }
    # refresh existing related blocks with expanded lists where heading exists
    expanded = {
        "ourservice/acpcladding/index.html": [
            ("/blog/acp-cladding-contractors-mumbai/", "ACP Cladding Contractors in Mumbai"),
            ("/blog/fire-rated-acp-high-rise-india/", "Fire-Rated ACP for High-Rise"),
            ("/blog/acp-joint-design-sealants/", "ACP Joint Design, Sealants and Colour Matching"),
            ("/blog/acp-vs-hpl-vs-solid-aluminium/", "ACP vs HPL vs Solid Aluminium"),
            ("/blog/acp-colour-fading-uv-india/", "ACP Colour Fading and UV"),
        ],
        "ourservice/glazingwork/index.html": [
            ("/blog/curtain-wall-contractors-mumbai/", "Curtain Wall Contractors Scope Checklist"),
            ("/blog/unitised-curtain-wall-mumbai/", "Unitised Curtain Wall Mumbai Logistics"),
            ("/blog/stick-system-glazing-when/", "Stick System Glazing: When It Still Makes Sense"),
            ("/blog/igu-double-glazing-hot-climate/", "IGU Specs for Hot Climates"),
            ("/blog/choose-glazing-contractor-questions/", "Choosing a Glazing Contractor: 12 Questions"),
        ],
    }
    mapping.update(expanded)

    def section(links):
        items = "\n".join(f'              <li style="margin: 8px 0"><a href="{h}">{t}</a></li>' for h, t in links)
        return f'''
      <section class="service-inner-section alt" aria-labelledby="related-reading-heading">
        <div class="container" style="max-width: 900px">
          <h2 id="related-reading-heading" style="color: var(--primary); margin-bottom: 12px">Related reading</h2>
          <p style="margin-bottom: 16px; color: var(--gray)">Guides from Shebi Enterprises to help you specify and tender this package.</p>
          <ul style="line-height: 1.7; padding-left: 1.2rem">
{items}
          </ul>
          <p style="margin-top: 20px"><a href="/blog/" class="btn btn-outline" style="color: var(--primary); border-color: var(--primary)">Browse all insights</a>
          <a href="/contact/" class="btn btn-primary" style="margin-left: 10px">Get free quote</a></p>
        </div>
      </section>
'''

    for rel, links in mapping.items():
        path = ROOT / rel
        t = path.read_text(encoding="utf-8")
        block = section(links)
        if "related-reading-heading" in t:
            t = re.sub(
                r'<section class="service-inner-section alt" aria-labelledby="related-reading-heading">[\s\S]*?</section>\s*',
                block,
                t,
                count=1,
            )
        else:
            t = t.replace("</main>", block + "\n    </main>", 1)
        path.write_text(t, encoding="utf-8")
        print("related reading", rel)


def main():
    # sync any new assets
    if ASSETS.exists():
        for src in ASSETS.glob("*-hero.jpg"):
            dest = BLOG_IMG / src.name
            if not dest.exists():
                shutil.copy2(src, dest)
                print("copied asset", src.name)

    metas = []
    for post in RAW:
        meta = render(post)
        if meta:
            metas.append(meta)
            print("wrote", meta["slug"])
    update_sitemap(metas)
    update_llms(metas)
    update_blog_index(metas)
    update_related_reading()
    print("TOTAL NEW", len(metas))


if __name__ == "__main__":
    main()
