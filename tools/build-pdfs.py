#!/usr/bin/env python3
"""Render each legal document page to a date-stamped PDF in /pdf/.

Run from the repo root:  python3 tools/build-pdfs.py
Requires: pip install weasyprint

When a document is revised, update its effective date in DOCS below and re-run.
Do not delete outgoing PDFs — prior versions stay in /pdf/ as the archive.
"""
import pathlib, sys

try:
    from weasyprint import HTML
except ImportError:
    sys.exit("weasyprint is required: pip install weasyprint")

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "pdf"
OUT.mkdir(exist_ok=True)

# page dir -> (output basename, effective date stamp)
DOCS = {
    "master-services-agreement": ("Boom-Logic-Master-Services-Agreement", "2026-11-02"),
    "service-attachment-managed-services": ("Boom-Logic-Service-Attachment-Managed-Services", "2026-11-02"),
    "service-attachment-compliance-services": ("Boom-Logic-Service-Attachment-Compliance-Services", "2026-11-02"),
    "service-attachment-boomtalk-live": ("Boom-Logic-Service-Attachment-BoomTalk-Live", "2026-11-02"),
    "schedule-of-services": ("Boom-Logic-Schedule-of-Services", "2026-11-02"),
    "schedule-of-third-party-services": ("Boom-Logic-Schedule-of-Third-Party-Services", "2026-11-02"),
    "business-associate-agreement": ("Boom-Logic-Business-Associate-Agreement", "2026-11-02"),
    "service-level-schedule": ("Boom-Logic-Service-Level-Schedule", "2026-11-02"),
    "data-processing-agreement": ("Boom-Logic-Data-Processing-Agreement", "2026-11-02"),
    "third-party-access-authorization": ("Boom-Logic-Third-Party-Access-Authorization", "2026-08-19"),
    "mutual-nda": ("Boom-Logic-Mutual-NDA", "2026-10-08"),
    "terms-of-service": ("Boom-Logic-BoomTalk-VoIP-Terms-of-Service", "2026-09-22"),
    "e911": ("Boom-Logic-911-E911-Notification-Disclosures", "2026-09-22"),
}

css_abs = (ROOT / "styles.css").as_uri()
for page_dir, (name, eff) in DOCS.items():
    src = ROOT / page_dir / "index.html"
    html = src.read_text(encoding="utf-8").replace('href="/styles.css"', f'href="{css_abs}"')
    dest = OUT / f"{name}-{eff}.pdf"
    if dest.exists():
        print(f"skip {dest.name} (published PDFs are never rebuilt)")
        continue
    HTML(string=html, base_url=str(src.parent)).write_pdf(str(dest))
    print(f"built {dest.relative_to(ROOT)} ({dest.stat().st_size//1024} KB)")

import hashlib
lines = [f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}" for p in sorted(OUT.glob("*.pdf"))]
(OUT / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n")
print(f"wrote pdf/SHA256SUMS.txt ({len(lines)} files)")

# ---------------------------------------------------------------------------
# Contract-document manifest for the quote composer: /contract-documents.json
# Lists the CURRENT version of every document an Order can incorporate, with
# its authoritative PDF URL and SHA-256. Update RELEASE and APPLIES when a new
# legal release is published.
import json
RELEASE = "2026-11-02"
BASE = "https://legal.theboomcoinc.com"
APPLIES = {  # page dir -> (title, when the quote composer should list it)
    "master-services-agreement": ("Master Services Agreement", "always"),
    "service-attachment-managed-services": ("Service Attachment for Managed Services", "service:managed"),
    "service-level-schedule": ("Service Level Schedule", "always"),
    "schedule-of-services": ("Schedule of Services", "always"),
    "schedule-of-third-party-services": ("Schedule of Third-Party Services", "always"),
    "business-associate-agreement": ("Business Associate Agreement", "hipaa"),
    "data-processing-agreement": ("Data Processing Agreement", "always"),
    "service-attachment-compliance-services": ("Service Attachment for Managed Compliance Services", "service:compliance"),
    "service-attachment-boomtalk-live": ("Service Attachment for BoomTalk™ Live", "service:boomtalk-live"),
    "terms-of-service": ("BoomTalk™ VoIP Terms of Service", "service:boomtalk-voip"),
    "e911": ("911/E911 Notification and Disclosures", "service:boomtalk-voip"),
}
from datetime import date
docs = []
for page_dir, (title, applies) in APPLIES.items():
    name, eff = DOCS[page_dir]
    pdf = OUT / f"{name}-{eff}.pdf"
    d = date.fromisoformat(eff)
    docs.append({
        "title": title,
        "effective": eff,
        "effective_display": f"{d.strftime('%B')} {d.day}, {d.year}",
        "applies": applies,
        "page_url": f"{BASE}/{page_dir}/",
        "pdf_url": f"{BASE}/pdf/{pdf.name}",
        "sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
    })
manifest = {
    "release": RELEASE,
    "provider": "The Boom Company (dba Boom Logic)",
    "applies_values": {
        "always": "List on every Order.",
        "hipaa": "List on every Order; applies when Client is a HIPAA covered entity or business associate (MSA 13.2).",
        "service:managed": "List when the Order includes managed IT, security, backup, or network services.",
        "service:compliance": "List when the Order includes managed compliance services.",
        "service:boomtalk-live": "List when the Order includes BoomTalk Live.",
        "service:boomtalk-voip": "List when the Order includes BoomTalk VoIP.",
    },
    "documents": docs,
}
(ROOT / "contract-documents.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
print(f"wrote contract-documents.json ({len(docs)} documents)")
