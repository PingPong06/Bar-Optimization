# Security and Compliance

## Production Security Baseline

Before commercial use:

- Set `DEBUG=False`.
- Use a private, random `SECRET_KEY`.
- Set `ALLOWED_HOSTS` to real domains only.
- Use HTTPS.
- Use secure cookies.
- Protect the database with a strong password and restricted network access.
- Keep `.env` out of Git.
- Restrict Django admin access to admin users.
- Back up the database and media files.
- Use a monitored production logging setup.

## Recommended Django Settings Additions

For production, configure:

```python
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
```

These should be enabled only when HTTPS is correctly configured.

## Sensitive Data

CutFlow may store:

- Customer names.
- Phone numbers.
- Email addresses.
- Billing and site addresses.
- Project notes.
- Commercial rates, costs, margins, and quotations.
- Uploaded company logos and user avatars.

## Access Control Requirements

- All write actions need server-side role checks.
- All PDF downloads should require authentication.
- Catalog, pricing, and company settings should be admin-only.
- Production optimization should be production/admin-only.
- Inactive users should not access operational screens.

## Audit Requirements

Activity logging should record:

- User login failures if practical.
- Customer/project creation and edits.
- Project lock/unlock.
- Quotation creation, revision, sent, accepted, rejected.
- Catalog cost/formula changes.
- Company settings changes.
- Production item generation.
- Optimization runs.
- Offcut creation and use.

## Compliance Notes

This project is not a substitute for legal, tax, or privacy advice. For commercial rollout, the business owner should review:

- Quotation terms and conditions.
- Payment terms.
- Tax treatment.
- Privacy notice for customer data.
- Data retention rules.
- Employee access policy.

