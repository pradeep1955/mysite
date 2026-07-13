# TinkerStack

A Django-powered personal site for IoT, electronics, and ML/AI project write-ups — with a
parts/kits store built directly from real Bills of Materials, and a lightweight rule-based
chat assistant that points visitors to the right components.

Live at: https://prdp1955.pythonanywhere.com/

---

## For Users — what's on the site

- **Home** (`/`) — the latest project story and blog post, with a signup form for updates.
- **Blog** (`/blog/`) — project write-ups and technical posts. Log in as an author to write,
  edit, or delete your own posts via `/blog/post/new/`.
- **Store** (`/store/`) — project kits with full parts lists (BOM), pricing, and affiliate
  links to where each part is actually sourced. Kits move through a lifecycle: coming soon →
  open for preorder → available. No payment gateway yet — preorder interest is captured and
  followed up manually.
- **Chat assistant** — the small chat button in the corner of every page answers common
  technical questions (e.g. "which pump for drip irrigation?") using a keyword-matched
  knowledge base, and links to relevant store products when it has a good answer. No account
  or login required to use it.
- **Privacy Policy** (`/privacy/`) — what data the site collects and why.

No account is required to browse the blog, store, or use the chat assistant. Logging in is
only needed to author blog posts.

---

## For Developers

### Project layout

| App | Purpose |
|---|---|
| `home` | Landing page, `SensorReading` model (IoT sensor data), email `Subscriber` capture, privacy policy page |
| `blog` | Posts (`Post` model), author pages, about page |
| `store` | `Category` / `Product` / `ProjectKit` / `KitComponent` (the BOM) / `PreorderInterest` |
| `assistant` | Keyword-matched chat widget — `Intent` (keywords → answer → linked products) and `ChatQuery` (every question asked, logged for content research) |

### Requirements

- Python 3.11+ or Docker
- MySQL client build dependencies if installing `mysqlclient` locally
- API keys only for features that call external services

### Environment Setup

```bash
cp .env.example .env
```

Set `DJANGO_SECRET_KEY` to a real secret value. For local SQLite development, the values in
`.env.example` are enough after replacing that one value.

### Run Locally

```bash
python3 -m venv django_venv
source django_venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

### Seed sample data (optional but recommended for a fresh clone)

The store and assistant apps come with management commands that populate real, structured
starter content instead of leaving you with empty tables:

```bash
python manage.py seed_solar_irrigation_kit   # Category, Product, and ProjectKit rows from the solar irrigation BOM
python manage.py seed_tools                  # a starter "Tools" category (all inactive by default — review before publishing)
python manage.py seed_starter_intents        # run AFTER seed_solar_irrigation_kit — chat assistant starter Q&A
```

All three are safe to re-run — they use `get_or_create`, so re-running won't create
duplicates or overwrite anything you've since edited in the admin.

### Run With Docker

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

```bash
docker compose up --build
```

In another terminal:

```bash
docker compose exec web python manage.py migrate
```

Open `http://localhost:8000/`. Stop with `docker compose down`.

### Deploy On PythonAnywhere

These steps replace an existing PythonAnywhere `mysite` project with the GitHub `master`
branch.

```bash
cd ~
mv mysite mysite_backup
git clone -b master https://github.com/pradeep1955/mysite.git mysite
cd mysite
python3.11 -m venv ~/.virtualenvs/mysite-venv
source ~/.virtualenvs/mysite-venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and set at least:

```env
DJANGO_SECRET_KEY=replace-this-with-a-real-secret
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourusername.pythonanywhere.com
```

If you use PythonAnywhere MySQL, also set `DB_ENGINE`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`,
`DB_HOST`, and `DB_PORT` in `.env`. For SQLite, keep the SQLite defaults.

```bash
python manage.py migrate
python manage.py collectstatic
```

In the PythonAnywhere **Web** tab:

- Source code directory: `/home/yourusername/mysite`
- Virtualenv: `/home/yourusername/.virtualenvs/mysite-venv`
- WSGI file imports `/home/yourusername/mysite/mysite/wsgi.py`
- Static files mapping: `/static/` → `/home/yourusername/mysite/staticfiles`
- **Reload** the web app

> **Every code or template change requires a Reload on the Web tab** — PythonAnywhere does
> not auto-detect file changes. This is the single most common source of "I pushed it but
> nothing changed" confusion.

> **Migrations must always be created on one consistent machine** (this project uses the
> developer's laptop) and committed to git from there. Running `makemigrations` directly on
> the server, outside of git, causes the server and repo to silently drift apart.

### GitHub Commit Checklist

- Do not commit `.env`, `.env.test`, `.env.production`, local SQLite databases, media
  uploads, virtual environments, or collected static files.
- **Do** commit `.env.example`, `Dockerfile`, `docker-compose.yml`, `requirements.txt`,
  migrations, templates, static source files, and application code.
- Run the Django check before committing:

```bash
python manage.py check
```

### Notes

- `mysite/github_settings.py` is ignored because it can contain GitHub OAuth secrets.
- A fresh Docker database will return errors on pages that query models until
  `python manage.py migrate` has been run inside the web container.
- See `AGENTS.md` for the Claude Code optimisation skill shipped with this repo.