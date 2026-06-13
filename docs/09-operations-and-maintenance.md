# Operations and Maintenance

## Daily Operations

- Review failed logins or access errors.
- Confirm new quotations and production jobs are visible.
- Check whether any production items have diagnostics.
- Verify backups completed.
- Review disk space for media/PDF storage.

## Weekly Operations

- Review catalog rate changes.
- Review reusable offcut records against physical stock.
- Export or archive key reports if required by management.
- Check app logs for recurring errors.
- Test one backup restore in a non-production environment on a scheduled basis.

## Monthly Operations

- Review user access and deactivate old accounts.
- Review quotation terms, tax rates, and company settings.
- Reconcile profile, glass, and hardware costs with supplier price lists.
- Review production optimization results for material waste trends.
- Patch operating system and dependencies.

## Backup Plan

Back up:

- MySQL database.
- Media uploads.
- Environment configuration, stored securely.
- Deployed Git version or release artifact.

Minimum recommendation:

- Daily database backups.
- Daily media backup or object storage versioning.
- Monthly restore test.
- Offsite backup copy.

## Monitoring

Monitor:

- Application uptime.
- HTTP 500 errors.
- Database connection failures.
- Disk space.
- Backup success/failure.
- Gunicorn or service restart loops.
- Slow requests for PDF generation and optimization.

## Support Process

For every support issue, record:

- Reporter.
- Time reported.
- Affected project/quotation/job.
- Screenshots or PDF.
- Steps to reproduce.
- Business impact.
- Fix owner.
- Resolution and release version.

## Incident Response

Severity examples:

- Critical: app unavailable, data loss, incorrect accepted quotations, security incident.
- High: production cannot generate cutting list, PDFs broken, login unavailable for a team.
- Medium: individual project issue, catalog correction needed.
- Low: cosmetic issue or training question.

For critical incidents:

1. Stop the harmful workflow if needed.
2. Preserve logs and affected records.
3. Notify business owner.
4. Restore service or rollback.
5. Verify affected commercial documents.
6. Write a short incident report.

