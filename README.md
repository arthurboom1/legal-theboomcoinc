# Boom Logic Legal Portal — legal.theboomcoinc.com

Static HTML legal portal for The Boom Company, Inc. (dba Boom Logic).
This repository is the source of truth for the site and deploys to Plesk via the Plesk Git extension.

## Structure

| Path | Document | Effective |
|---|---|---|
| `/` | Legal Hub (index) | — |
| `/master-services-agreement/` | Master Services Agreement | July 1, 2026 |
| `/service-attachment-managed-services/` | Service Attachment for Managed Services | June 4, 2023 |
| `/service-attachment-compliance-services/` | Service Attachment for Managed Compliance Services | June 4, 2023 |
| `/schedule-of-services/` | Schedule of Services | June 4, 2023 |
| `/schedule-of-third-party-services/` | Schedule of Third-Party Services | June 26, 2024 |
| `/data-processing-agreement/` | Data Processing Agreement | December 1, 2023 |
| `styles.css` | Shared stylesheet | — |

`/terms-of-service/` (BoomTalk VoIP ToS) and `/e911/` (911/E911 Notification & Disclosures)
are live on the server but **not yet in this repository** — copy them in from Plesk before
enabling any deploy mode that removes files not present in the repo.

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
