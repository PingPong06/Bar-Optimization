# Deployment Runbook

## Production Requirements

- Python 3.10 or newer.
- MySQL 8.0 or managed MySQL-compatible database.
- Linux server or managed app platform.
- HTTPS domain.
- SMTP account for production email.
- Persistent storage for media uploads.
- Backup system for database and media.

## Environment Variables

Production must set:

```env
SECRET_KEY=replace-with-long-random-secret
DEBUG=False
ALLOWED_HOSTS=example.com,www.example.com
CSRF_TRUSTED_ORIGINS=https://example.com,https://www.example.com
USE_SQLITE=False
DB_FALLBACK_TO_SQLITE=False

DB_NAME=cutflow_db
DB_USER=cutflow_user
DB_PASSWORD=replace-with-strong-password
DB_HOST=localhost
DB_PORT=3306

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=notifications@example.com
EMAIL_HOST_PASSWORD=replace-with-app-password
DEFAULT_FROM_EMAIL=CutFlow <notifications@example.com>

COMPANY_NAME=Your Company Name
```

Use `.env.production.example` as the starting template for live deployments.

## First Deployment

1. Create the production database and user.
2. Create a Python virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure environment variables.
5. Run Django checks:

```bash
python manage.py check --deploy
```

Also verify the health endpoint after the app starts:

```bash
curl https://example.com/healthz/
```

6. Apply migrations:

```bash
python manage.py migrate
```

7. Create the first superuser:

```bash
python manage.py createsuperuser
```

8. Assign the superuser profile role as `admin`.
9. Seed initial catalog data if starting from the packaged catalog:

```bash
python manage.py seed_data
```

10. Collect static files:

```bash
python manage.py collectstatic --noinput
```

11. Start the app with Gunicorn behind Nginx or an equivalent production server.

## Release Process

For every release:

1. Announce maintenance window if needed.
2. Backup database and media.
3. Pull or deploy the approved Git commit.
4. Install changed dependencies.
5. Run migrations.
6. Collect static files.
7. Restart the application service.
8. Run smoke tests.
9. Monitor logs.
10. Record the release version and timestamp.

## Smoke Tests

After deployment:

- Login page loads.
- Admin login works.
- Dashboard loads.
- Customer list loads.
- Project creation works.
- Measurement creation works.
- Quotation generation works.
- Quotation PDF downloads.
- Production job creation works.
- Production item generation works.
- Optimization works for a known sample project.

## Rollback Plan

- Keep the previous deploy artifact or Git tag available.
- Restore the database backup if migrations are not backward compatible.
- Restart the previous app version.
- Confirm login and dashboard.
- Record the rollback cause.
