# Local backend setup

[Back to the README](../README.md)

## Environment

Install the pinned [requirements](../requirements.txt) in a Python 3.11/3.12 virtual environment. Copy the example file:

```powershell
# Windows
Copy-Item .env.example .env
```

```bash
# macOS / Linux
cp .env.example .env
```

| Variable | Purpose |
| --- | --- |
| `EMAIL_HOST_USER` | SMTP account used by registration and password-recovery emails |
| `EMAIL_HOST_PASSWORD` | SMTP password/app password for that account |
| `FIREBASE_CREDENTIALS_PATH` | Firebase service-account JSON path; defaults to `serviceAccountKey.json` |

The email server is configured in [settings.py](../config/settings.py) as Gmail SMTP with TLS on port 587. Use your own account and credentials. Firebase credentials are loaded by [notifications/apps.py](../notifications/apps.py); absent credentials produce a startup warning and push delivery will not work.

**The current settings do not read `SECRET_KEY`, `DEBUG`, or database connection values from `.env`.** Adding those variables alone does not change behavior. Update the settings implementation when preparing a deployment.

## Use a clean database

A database snapshot is tracked in the repository. For development, change the SQLite `NAME` in `config/settings.py` from `BASE_DIR / 'db.sqlite3'` to `BASE_DIR / 'db.local.sqlite3'`. This creates a separate database without overwriting the snapshot.

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py check
python manage.py runserver
```

Use the admin to create a small synthetic category/product dataset. An empty catalog is expected until you add records. Do not copy real customer or prescription data into demos.

Registration creates inactive users until the email OTP is verified. An admin account created by `createsuperuser` is active.

## Connect the Flutter app

The API prefix is `/api/`. For an Android emulator, point the client to `http://10.0.2.2:8000/api/`. For a physical device, use the development computer's LAN address, bind Django to `0.0.0.0:8000`, and add that address to `ALLOWED_HOSTS`.

The app's media origin must also point to this backend. Use the same Firebase project on client and server when testing push messages.

## Troubleshooting

| Problem | Likely next check |
| --- | --- |
| Firebase credentials warning | Set the credential path to your own service-account JSON, or accept that push delivery is unavailable locally |
| OTP email does not arrive | SMTP credentials, account authorization, and mail delivery |
| HTTP 401 | Access token, account activation, and refresh flow |
| HTTP 429 | Configured anonymous/user/OTP throttle limits |
| Empty product list | Create active products and categories in the clean database |
| Broken media URLs | Development media serving and the client's media origin |

## Before deployment

Replace the source-defined secret, disable debug mode, restrict allowed hosts and CORS, and configure static/media serving, HTTPS, backups, and upload access controls. Review authorization on every exposed endpoint and test complete registration/order/prescription flows.

If credentials have ever been committed, revoke or rotate them with the provider. Removing a file in a new commit does not erase earlier Git history. Keep local credentials and service-account JSON outside version control.
