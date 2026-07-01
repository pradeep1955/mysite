# Pleasure Web Site

A Django project with apps for home pages, ads, blog, events, livestream, news, polls, portfolio, shop, stocks, IoT data, and e-bike features.

## Requirements

- Python 3.11+ or Docker
- MySQL client build dependencies if installing `mysqlclient` locally
- API keys only for features that call external services

## Environment Setup

Create an environment file before running the project:

```bash
cp .env.example .env
```

Set `DJANGO_SECRET_KEY` to a real secret value. Optional API keys can be left blank, but features that depend on those services may not work until the keys are configured.

For local SQLite development, the values in `.env.example` are enough after replacing `DJANGO_SECRET_KEY`.

## Run Locally

Create and activate a virtual environment:

```bash
python3 -m venv django_venv
source django_venv/bin/activate
pip install -r requirements.txt
```

Apply database migrations:

```bash
python manage.py migrate
```

Start the Django development server:

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Run With Docker

Create a Docker environment file:

```bash
cp .env.example .env.test
```

Edit `.env.test` and use these database values:

```env
DB_ENGINE=django.db.backends.mysql
DB_NAME=testdb
DB_USER=root
DB_PASSWORD=testpass
DB_HOST=db
DB_PORT=3306
```

Build and start the containers:

```bash
docker compose up --build
```

In another terminal, apply migrations to the Docker database:

```bash
docker compose exec web python manage.py migrate
```

Open `http://localhost:8000/`.

To stop the containers:

```bash
docker compose down
```

## Deploy On PythonAnywhere

These steps replace an existing PythonAnywhere `mysite` project with the GitHub `master` branch.

Open a PythonAnywhere Bash console:

```bash
cd ~
mv mysite mysite_backup
git clone -b master https://github.com/pradeep1955/mysite.git mysite
cd mysite
```

Create or reuse a virtual environment:

```bash
python3.11 -m venv ~/.virtualenvs/mysite-venv
source ~/.virtualenvs/mysite-venv/bin/activate
pip install -r requirements.txt
```

Create the production environment file:

```bash
cp .env.example .env
```

Edit `.env` and set at least:

```env
DJANGO_SECRET_KEY=replace-this-with-a-real-secret
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourusername.pythonanywhere.com
```

If you use PythonAnywhere MySQL, also set the `DB_ENGINE`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, and `DB_PORT` values in `.env`. For SQLite, keep the SQLite defaults.

Apply migrations and collect static files:

```bash
python manage.py migrate
python manage.py collectstatic
```

In the PythonAnywhere Web tab:

- Set the source code directory to `/home/yourusername/mysite`
- Set the virtualenv to `/home/yourusername/.virtualenvs/mysite-venv`
- Set the WSGI file to import `/home/yourusername/mysite/mysite/wsgi.py`
- Add a static files mapping from `/static/` to `/home/yourusername/mysite/staticfiles`
- Reload the web app

## GitHub Commit Checklist

- Do not commit `.env`, `.env.test`, `.env.production`, local SQLite databases, media uploads, virtual environments, or collected static files.
- Keep `.env.example`, `Dockerfile`, `docker-compose.yml`, `requirements.txt`, migrations, templates, static source files, and application code committed.
- Run the Django check before committing:

```bash
python manage.py check
```

## Notes

- `mysite/github_settings.py` is ignored because it can contain GitHub OAuth secrets.
- A fresh Docker database will return errors on pages that query models until `python manage.py migrate` has been run inside the web container.
