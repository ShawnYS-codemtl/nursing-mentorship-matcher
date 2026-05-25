# Nursing Mentorship Matcher

A web tool for McGill's nursing programs that pairs mentors and mentees from Google Form CSV exports using a scored matching algorithm. Administrators upload CSVs, review auto-detected column mappings, run the algorithm, and manage results through a dashboard.

---

## Features

- **Two-step CSV import** — upload mentor and mentee CSVs, preview and correct auto-detected column mappings before committing
- **Duplicate mapping detection** — highlights conflicting column assignments in real time before import
- **Scored matching algorithm** — three-phase pipeline: locked matches → explicit preferences → min-cost max-flow optimization
- **Scoring breakdown** — each match shows a score out of 100 across program alignment, specialty alignment, and identity/extracurricular factors; hard constraints (year seniority, language) are enforced
- **Dashboard** — stats panel, sortable matches table with expandable score breakdown per match
- **Lock matches** — lock individual pairs so algorithm re-runs don't overwrite them
- **Manual matching** — browse unmatched mentors and mentees side-by-side with live score preview; sort lists by name, program, or year
- **CSV export** — download all matches as a spreadsheet
- **Reset database** — clear all data and start fresh

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite, TypeScript, Tailwind CSS |
| Backend | Python, Flask, SQLAlchemy |
| Database | SQLite (local) / PostgreSQL via Supabase (production) |
| Matching | networkx `max_flow_min_cost` |
| Hosting | Vercel (frontend) + Render (backend) |

---

## Local Development

### Prerequisites
- Python 3.10+
- Node.js 18+

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py                  # http://127.0.0.1:5000
```

Utility scripts (run from `backend/`):
```bash
python scripts/reset_db.py          # drop and recreate all tables
python scripts/insert_test_data.py  # populate with synthetic data
python -m tests.test_matching_manual  # run scoring tests
```

### Frontend

```bash
cd frontend
npm install
npm run dev    # http://localhost:5173
npm run build  # type-check + production build
npm run lint   # ESLint
```

No environment variables are needed for local development. The frontend defaults to `http://127.0.0.1:5000` and the backend uses SQLite automatically.

---

## Deployment

Production stack: **Vercel** (frontend) + **Render** (backend) + **Supabase** (PostgreSQL).

### 1. Supabase

Create a free project. Go to **Project Settings → Database → Connection pooling** and copy the **Transaction mode** URL (port **6543**). This is your `DATABASE_URL`.

> **Important:** Use the pooler URL (port 6543), not the direct connection (port 5432). Render's free tier is IPv4-only; the direct Supabase hostname resolves to IPv6 and will fail.

If your database password contains special characters (`@ # % / : ? & = +`), percent-encode it:
```bash
python3 -c "import urllib.parse; print(urllib.parse.quote('your-password', safe=''))"
```

### 2. Render

Connect your GitHub repo. Set root directory to `backend/`. Add environment variables:

| Variable | Value |
|---|---|
| `DATABASE_URL` | Supabase pooler URL (port 6543) |
| `ALLOWED_ORIGINS` | Your Vercel URL, e.g. `https://your-app.vercel.app` |
| `FLASK_ENV` | `production` |

Build command: `pip install -r requirements.txt`  
Start command: `python run.py`

### 3. Vercel

Import your GitHub repo. Set root directory to `frontend/`. Add environment variable:

| Variable | Value |
|---|---|
| `VITE_API_URL` | Your Render URL, e.g. `https://your-app.onrender.com` |

Both services auto-deploy on push to main.

---

## Architecture

### Import Pipeline (`backend/app/services/importing/`)

1. **Preview** (`mapping.py`) — normalizes CSV column names and matches them to canonical fields via alias dictionaries (`aliases.py`)
2. **Normalize** (`normalization.py`) — converts raw CSV values to typed canonical fields (year integers, JSON arrays, normalized strings)
3. **Validate** (`validation.py`) — checks required fields are present and correctly typed; returns structured per-row errors
4. **Persist** (`import_service.py`) — builds ORM objects, deduplicates by email, resolves explicit preference names to database IDs

### Matching Pipeline (`backend/app/services/matching/`)

Three phases run in sequence on `POST /run-matching`:

1. **Locked matches** — excluded from subsequent phases; their consumed capacity is reserved
2. **Explicit matching** — mutual preferences first, then mentor-driven, then mentee-driven
3. **Flow matching** — builds a weighted directed graph and solves `max_flow_min_cost` to maximize total score subject to per-mentor capacity constraints

### Scoring (`backend/app/services/matching/scoring.py`)

`calculate_match_score(mentor, mentee)` returns `(score: int, breakdown: dict)`.

Hard constraints — year seniority (`mentor.year > mentee.year`) and language — return score 0 if violated, but `potential_score` is still computed for display.

| Component | Max pts |
|---|---|
| Program alignment | 35 |
| Specialty alignment | 35 |
| Identity / extracurricular | 30 |

---

## Project Structure

```
nursing-mentorship-matcher/
├── backend/
│   ├── run.py                        # app entry point
│   ├── requirements.txt
│   ├── render.yaml                   # Render deployment config
│   └── app/
│       ├── models/                   # SQLAlchemy ORM: Mentor, Mentee, Match
│       ├── routes/                   # Flask blueprints (one file per endpoint group)
│       └── services/
│           ├── importing/            # CSV import pipeline
│           │   ├── aliases.py        # fuzzy-match vocabulary
│           │   ├── mapping.py        # auto-detect column mappings
│           │   ├── normalization.py  # type conversion
│           │   ├── validation.py     # required field checks
│           │   └── import_service.py # orchestration + persistence
│           └── matching/
│               ├── scoring.py        # calculate_match_score()
│               ├── explicit_matcher.py
│               ├── flow_matching.py  # max_flow_min_cost
│               └── locked_matches.py
└── frontend/
    └── src/
        ├── components/
│       │   ├── dashboard/            # StatsPanel, MatchesTable, UnmatchedPanel
│       │   └── controls/             # ImportPanel, ImportMappingTable, ControlPanel
        ├── hooks/                    # useMatches, useStats, useUnmatched, useMatchScore
        ├── services/api.ts           # all fetch calls
        ├── types.ts                  # shared TypeScript interfaces
        └── constants/importFields.ts # canonical field lists for dropdowns
```
