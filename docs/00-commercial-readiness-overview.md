# Commercial Readiness Overview

CutFlow is a Django-based ERP for aluminium/uPVC window and door fabrication. It covers customer/project capture, site measurements, quotation generation, production job creation, profile cut calculation, hardware BOQ generation, bar optimization, and reusable offcut tracking.

This documentation pack turns the repository from a developer project into a commercially operable product package. Each document focuses on one aspect of running, selling, maintaining, or deploying the system.

## Commercial Readiness Definition

CutFlow should be considered commercially ready only when these conditions are met:

- The production environment runs with `DEBUG=False`, a private `SECRET_KEY`, real domain names in `ALLOWED_HOSTS`, HTTPS, database backups, and monitored logs.
- MySQL 8.0 or another approved production database is configured, backed up, and tested for restore.
- Every business role has a documented access policy and at least one trained user.
- Quotation, tax, payment term, company profile, and PDF output settings have been validated by the business owner.
- Catalog formulas, profile costs, glass rates, hardware rules, wastage, fabrication, and margin settings have been reviewed against real production data.
- A release checklist is followed for migrations, seed data, static files, smoke tests, and rollback.
- Security controls for authentication, CSRF, session cookies, admin access, backups, and sensitive data handling are implemented and reviewed.

## Documentation Map

| Document | Purpose |
| --- | --- |
| `01-product-scope-and-workflows.md` | Explains what the product does and the end-to-end commercial workflow. |
| `02-roles-and-access-control.md` | Defines user roles, permissions, and operational controls. |
| `03-data-model-and-records.md` | Documents core records, ownership, and retention expectations. |
| `04-catalog-pricing-and-formulas.md` | Covers catalog setup, formulas, pricing inputs, and validation. |
| `05-commercial-documents-and-pdfs.md` | Defines quotation and production document expectations. |
| `06-production-and-optimization.md` | Explains production jobs, cut generation, optimization, and offcuts. |
| `07-deployment-runbook.md` | Provides a production deployment and release process. |
| `08-security-and-compliance.md` | Lists security controls required before commercial launch. |
| `09-operations-and-maintenance.md` | Covers backups, monitoring, support, maintenance, and incident response. |
| `10-testing-and-acceptance.md` | Defines tests and acceptance criteria before launch. |
| `11-customer-onboarding-and-training.md` | Gives a rollout and training plan for customer teams. |
| `12-commercial-gap-report.md` | Lists current gaps found in the repository and recommended next steps. |

## Current App Modules

- `accounts`: login, user profiles, roles, and activity log model.
- `catalog`: brands, colors, systems, profiles, formulas, glass, hardware, rules, and company settings.
- `projects`: customers, projects, measurement items, status history, lock workflow.
- `quotations`: quotation records, line items, pricing calculations, PDF generation.
- `production`: production jobs, generated items, cut items, hardware requirements, optimization runs, offcuts.
- `core`: dashboard, formula engine, optimizer, role middleware, seed command.

## Recommended Commercial Launch Sequence

1. Complete the items in `12-commercial-gap-report.md`.
2. Configure a staging environment that mirrors production.
3. Import real catalog and formula data for at least one full product line.
4. Run acceptance tests from `10-testing-and-acceptance.md`.
5. Train one admin, one sales user, and one production user.
6. Run two pilot projects from customer creation through optimized production output.
7. Freeze the first commercial release and tag it in Git.
8. Deploy production using `07-deployment-runbook.md`.
9. Monitor the first live week daily.

