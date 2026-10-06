# DjangoCelery

[![Tests](https://github.com/sanjarbek-ashurboyev/DjangoCelery/actions/workflows/tests.yml/badge.svg)](https://github.com/sanjarbek-ashurboyev/DjangoCelery/actions/workflows/tests.yml)

A small example of moving slow work out of the request cycle with Celery. The user enters
an email address, Django generates a one-time code, stores it in Redis and hands the
email off to a Celery worker, so the page responds immediately instead of waiting for
the SMTP server.

## How it works

```
browser ──► Django view ──► Redis (stores the code)
                │
                └──► Celery task queue (Redis broker) ──► worker ──► Gmail SMTP
```

## Tech stack

Python · Django · Celery · Redis · SMTP

## Running locally

Requirements: Python 3.12+ and a Redis server on `localhost:6379`.

```bash
git clone https://github.com/sanjarbek-ashurboyev/DjangoCelery.git
cd DjangoCelery
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# A Gmail address with an app password: https://myaccount.google.com/apppasswords
export EMAIL_HOST_USER=you@gmail.com
export EMAIL_HOST_PASSWORD=your-app-password

.venv/bin/celery -A email_otp.tasks worker --loglevel=info   # terminal 1
.venv/bin/python manage.py runserver                          # terminal 2
```

Open http://127.0.0.1:8000/email and enter an address.

## License

[MIT](LICENSE)
