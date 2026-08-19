# Boom Logic Legal Portal — legal.theboomcoinc.com

Static HTML legal portal for The Boom Company, Inc. (dba Boom Logic).
This repository is the source of truth for the site and deploys to Plesk via the Plesk Git extension.

## Structure

| Path | Document | Effective |
|---|---|---|
| `/` | Legal Hub (index) | — |
| `/master-services-agreement/` | Master Services Agreement | July 1, 2026 |
| `/service-attachment-managed-services/` | Service Attachment for Managed Services | July 1, 2026 |
| `/service-attachment-compliance-services/` | Service Attachment for Managed Compliance Services | July 1, 2026 |
| `/schedule-of-services/` | Schedule of Services | July 1, 2026 |
| `/schedule-of-third-party-services/` | Schedule of Third-Party Services | July 1, 2026 |
| `/data-processing-agreement/` | Data Processing Agreement | July 1, 2026 |
| `/third-party-access-authorization/` | Third-Party Administrative Access Authorization & Release (client form) | August 19, 2026 |
| `styles.css` | Shared stylesheet | — |

| `/terms-of-service/` | BoomTalk™ VoIP Terms of Service (imported verbatim from production) | July 22, 2026 |
| `/e911/` | 911/E911 Notification & Disclosures (imported verbatim from production) | July 22, 2026 |

This repository is now the **complete** source of truth for the site.

## PDFs

Date-stamped PDF copies of every document live in `/pdf/` and are linked from the hub
and each document page. Regenerate after any document change with
`python3 tools/build-pdfs.py` (requires `pip install weasyprint`), updating the
effective-date stamp in that script first. Never delete outgoing PDFs — prior
versions remain in `/pdf/` as the archive.

## Versioning policy (important)

When a legal document is updated:
1. **Never overwrite in place silently.** Commit the new version with a message like
   `MSA: new version effective YYYY-MM-DD`.
2. Move the outgoing version to an archive URL (e.g. `/master-services-agreement/2026-07-01/`)
   and add a row to the version-history table on the document page.
3. Update the effective-date banner and the hub listing.

The commit history of this repo is independent evidence of what terms were posted on any
given date. Do not force-push or rewrite history on `main`.

## Deployment

Plesk → Websites & Domains → legal.theboomcoinc.com → Git → pulls from this repo's `main`
branch and deploys to the domain's document root. Pushes to `main` deploy automatically
via webhook.
