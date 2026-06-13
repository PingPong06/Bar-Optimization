# Commercial Gap Report

This report is based on the current repository structure and code inspection. It separates documentation-ready items from gaps that should be fixed before real commercial deployment.

## Strengths Already Present

- Django app is organized into clear business modules.
- Core sales-to-production workflow exists.
- Role model exists with admin, salesman, production, and viewer.
- Formula engine rejects unsafe Python syntax.
- Catalog supports systems, profiles, glass, hardware, and company settings.
- Quotation pricing model supports taxes, discounts, installation, freight, and lifting charges.
- Production service generates cut items and hardware requirements.
- Optimizer supports kerf, end waste, reusable offcuts, and profile grouping.
- README contains setup instructions and business flow.

## Critical Gaps Before Commercial Launch

1. Production security settings must be verified in the real hosting environment.
   - Secure cookie, HTTPS, HSTS, and deploy-specific settings have been added to settings.
   - Run `python manage.py check --deploy` in staging with the real domain and HTTPS proxy.

2. Access control needs a full URL-by-URL audit.
   - Confirm every create/edit/delete/download/optimize action has server-side role enforcement.
   - Do not rely only on hidden UI buttons.

3. Activity logging model exists but needs systematic usage.
   - Log quotation, production, catalog, and settings changes.

4. Accepted quotations are not protected enough as commercial records.
   - Add workflow rules for accepted/revised/expired states.
   - Prevent silent changes to accepted quote pricing.

5. Production database backup and restore must be implemented in the hosting environment.
   - Deployment configuration has been documented.
   - Test restore before go-live.

## High-Priority Gaps

- Add automated tests for formula engine, pricing, optimizer, and permissions.
- Add staging smoke test script.
- Keep `.env.production.example` aligned with hosting requirements.
- Review PDF layouts for long tables, page breaks, and official terms.
- Add catalog import/export process for supplier price updates.
- Add explicit status transition rules for projects, quotations, and production jobs.
- Add diagnostics blocking rules before final optimization.
- Add error pages for production.

## Medium-Priority Gaps

- Add user-facing help text for formula setup and production diagnostics.
- Add audit views or reports for admin users.
- Expand structured logging for file or hosted log aggregation.
- Monitor the `/healthz/` endpoint in production.
- Add data retention/export policy.
- Add support for restoring archived PDFs if the database changes.
- Add visual regression checks for PDFs if documents are legally important.

## Recommended Next Engineering Sprint

1. Add permission tests and close role enforcement gaps.
2. Add audit logging service and call it from high-value workflows.
3. Add automated tests for formula/pricing/optimizer.
4. Add quote acceptance rules and immutable accepted totals.
5. Run a staging pilot with real catalog data.

## Commercial Go/No-Go

Current status: not yet ready for unsupervised commercial production use.

Recommended status: ready for controlled pilot after deployment hardening, access-control audit, and formula/pricing validation.
