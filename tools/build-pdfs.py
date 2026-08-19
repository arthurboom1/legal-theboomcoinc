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
    "master-services-agreement": ("Boom-Logic-Master-Services-Agreement", "2026-07-01"),
    "service-attachment-managed-services": ("Boom-Logic-Service-Attachment-Managed-Services", "2026-07-01"),
    "service-attachment-compliance-services": ("Boom-Logic-Service-Attachment-Compliance-Services", "2026-07-01"),
    "schedule-of-services": ("Boom-Logic-Schedule-of-Services", "2026-07-01"),
    "schedule-of-third-party-services": ("Boom-Logic-Schedule-of-Third-Party-Services", "2026-07-01"),
    "data-processing-agreement": ("Boom-Logic-Data-Processing-Agreement", "2026-07-01"),
    "terms-of-service": ("Boom-Logic-BoomTalk-VoIP-Terms-of-Service", "2026-07-22"),
    "e911": ("Boom-Logic-911-E911-Notification-Disclosures", "2026-07-22"),
}

css_abs = (ROOT / "styles.css").as_uri()
for page_dir, (name, eff) in DOCS.items():
    src = ROOT / page_dir / "index.html"
    html = src.read_text(encoding="utf-8").replace('href="/styles.css"', f'href="{css_abs}"')
    dest = OUT / f"{name}-{eff}.pdf"
    HTML(string=html, base_url=str(src.parent)).write_pdf(str(dest))
    print(f"built {dest.relative_to(ROOT)} ({dest.stat().st_size//1024} KB)")
