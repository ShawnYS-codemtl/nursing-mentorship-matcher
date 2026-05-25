# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A nursing mentorship matching tool for McGill's nursing programs. Administrators upload CSVs (exported from Google Forms) of mentors and mentees, preview/adjust column mappings, then trigger an algorithm that produces optimal mentor–mentee pairings. Results are displayed in a dashboard where matches can be locked, manually overridden, and exported.

## Development Commands

### Backend (Flask)

```bash
cd backend

# First-time setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run the server (http://127.0.0.1:5000)
python run.py

# Reset the database
python scripts/reset_db.py

# Insert synthetic test data
python scripts/insert_test_data.py

# Run manual scoring tests (no test runner required)
cd .. && python -m backend.tests.test_matching_manual
# or from inside backend/
python -m tests.test_matching_manual
```

### Frontend (Vite + React)

```bash
cd frontend

npm install
npm run dev      # http://localhost:5173
npm run build    # type-check + production build
npm run lint     # ESLint
```

## Architecture

### Backend (`backend/`)

**Entry point:** `run.py` — creates the Flask app, initializes the SQLite DB, and starts the server.

**Database:** SQLite at `backend/app/data/database.db` via SQLAlchemy. Schema is in `app/models/` (`Mentor`, `Mentee`, `Match`). `init_db()` in `app/database.py` creates tables via `Base.metadata.create_all`.

**API routes** (all Blueprints registered in `app/routes/__init__.py`):

| Route | File | Purpose |
|---|---|---|
| `POST /import/preview` | `import_routes.py` | Upload CSVs, auto-detect column→canonical field mapping |
| `POST /import/confirm` | `import_routes.py` | Accept confirmed mapping, normalize, validate, persist |
| `POST /run-matching` | `matching.py` | Execute full matching pipeline, persist results |
| `GET /matches` | `matches.py` | Fetch all matches with mentor/mentee detail |
| `POST /matches/override` | `matches.py` | Manually assign a mentee to a different mentor |
| `DELETE /matches/<id>` | `matches.py` | Remove a match |
| `PATCH /matches/<id>/lock` | `matches.py` | Lock/unlock a match so re-runs don't overwrite it |
| `GET /stats` | `stats.py` | Aggregate stats for dashboard |
| `GET /unmatched` | `unmatched.py` | List unmatched mentees + available mentors |
| `GET /export` | `export.py` | Download matches as CSV |
| `POST /match-score` | `score_preview.py` | Preview score for a hypothetical pair |

**Import pipeline** (`app/services/importing/`):
1. `mapping.py` — `detect_mapping()` normalizes CSV column names and matches them to canonical fields via exact then containment matching against `aliases.py` dictionaries.
2. `normalization.py` — `normalize_rows()` remaps CSV rows from original column names to canonical field names using the confirmed mapping.
3. `validation.py` — checks that required canonical fields are present and non-empty.
4. `import_service.py` — calls `form_processors.py` to build ORM objects, deduplicates by email, then calls `resolve.py` to resolve preferred-mentor/mentee names to database IDs.

**Canonical fields** are defined in `app/services/importing/schema.py` (`MENTOR_FIELDS`, `MENTEE_FIELDS`). Aliases (the fuzzy-match vocabulary) live in `app/services/importing/aliases.py`.

**Matching pipeline** (`app/services/matching/`):

Three-phase pipeline triggered by `POST /run-matching`:

1. **Locked matches** (`locked_matches.py`) — pull already-locked matches from DB; those pairs and their consumed capacity are excluded from subsequent phases.
2. **Explicit matching** (`explicit_matcher.py`) — runs three sub-phases in order: mutual (both sides named each other), mentor-driven, then mentee-driven explicit preference matches.
3. **Flow matching** (`flow_matching.py`) — builds a directed graph (networkx `DiGraph`) with source→mentor→mentee→sink edges weighted by negative match score, then solves `max_flow_min_cost` to maximise total score while respecting per-mentor capacity. `run_flow_matching_v1` is the active version.

**Scoring** (`scoring.py` — `calculate_match_score(mentor, mentee)`):

Returns `(total_score: int, breakdown: dict)`. Hard constraints (year, language) return score 0 if violated. Scoring components and their max weights:

- Program alignment: 35 pts (full if same program, 17.5 for related programs)
- Specialty alignment: 35 pts (bonus for 2+ shared specialties, −5 penalty for mismatch)
- Identity/extracurricular: 30 pts (heritage language 6 pts/lang, race/ethnicity 8 pts, LGBTQ+ 4 pts, shared interests 3 pts/interest; each capped)

### Frontend (`frontend/src/`)

Single-page app — `App.tsx` renders only `DashboardPage`.

**State management:** No global store. `DashboardPage` owns a `refreshKey` integer that it increments to trigger re-fetches. All server state lives in custom hooks (`useMatches`, `useStats`, `useUnmatched`, `useMatchScore`).

**API layer:** All fetch calls are in `services/api.ts`. The base URL is read from the `VITE_API_URL` environment variable at build time, falling back to `http://127.0.0.1:5000` for local development.

**Import flow (two-step):**
1. User picks mentor + mentee CSVs → `POST /import/preview` → backend returns detected mappings → `ImportMappingTable` renders editable dropdowns for each CSV column.
2. User confirms (or edits) mappings → `POST /import/confirm` with files + mappings as `multipart/form-data`.

**Key component relationships:**
- `DashboardLayout` → sidebar (`Sidebar`) + header (`Header`) + main content slot
- `DashboardPage` composes `StatsPanel`, `MatchesTable`, `UnmatchedPanel`, `ControlPanel`
- `MatchesTable` → `MatchRow` (expandable) → `MatchBreakdown` (score breakdown detail)
- `UnmatchedPanel` uses `useSelectionController` to coordinate mentor/mentee selection for manual override

## Deployment

### Production Stack

| Layer | Service |
|---|---|
| Frontend | Vercel |
| Backend | Render (free web service) |
| Database | Supabase (PostgreSQL) |

### Environment Variables

**Render (backend):**

| Variable | Value |
|---|---|
| `DATABASE_URL` | Supabase connection pooler URL (see below) |
| `ALLOWED_ORIGINS` | Vercel frontend URL, e.g. `https://your-app.vercel.app` |
| `FLASK_ENV` | `production` |

**Vercel (frontend):**

| Variable | Value |
|---|---|
| `VITE_API_URL` | Render backend URL, e.g. `https://your-app.onrender.com` |

### Supabase + Render Networking Note

Render's free tier is **IPv4-only**. Supabase's direct connection string (`db.<project>.supabase.co:5432`) resolves to an IPv6 address and will fail with `Network is unreachable`.

**Always use the connection pooler URL** from Supabase:
- Location: Project Settings → Database → Connection pooling → Transaction mode
- Port: **6543** (not 5432)
- Format: `postgresql://postgres.PROJECT_ID:PASSWORD@aws-0-REGION.pooler.supabase.com:6543/postgres`

### Local Development

When `DATABASE_URL` is not set, `database.py` automatically falls back to SQLite at `backend/app/data/database.db`. No environment variables needed for local dev.

## Key Data Conventions

- **Year in program** is stored as an integer (0–6) mapped from string labels like `"U1 (Undergraduate Year 1)"` by `YEAR_MAPPING` in `form_processors.py`. Matching requires `mentor.year_in_program > mentee.year_in_program`.
- **List fields** (specialties, languages, race_ethnicity, extracurricular_interests) are stored as JSON arrays. `parse_checkbox_field()` splits comma-delimited form values.
- **Normalized values** (specialties, extracurriculars, race/ethnicity, lgbtq_status) are lowercased and space-replaced with underscores before storage and scoring. Raw languages are stored as-is.
- **Email** is the deduplication key for both mentors and mentees.
- **`match_reason`** column on `Match` stores the full `breakdown` dict as JSON.

## Workflow Orchestration

### 1. Plan Mode Default
- Enter plan mode for ANY non-trivial task (3+ steps or architectural decisions)
- If something goes sideways, STOP and re-plan immediately – don't keep pushing
- Use plan mode for verification steps, not just building
- Write detailed specs upfront to reduce ambiguity

### 2. Subagent Strategy
- Use subagents liberally to keep main context window clean
- Offload research, exploration, and parallel analysis to subagents
- For complex problems, throw more compute at it via subagents
- One task per subagent for focused execution

### 3. Self-Improvement Loop
- After ANY correction from the user: update `tasks/lessons.md` with the pattern
- Write rules for yourself that prevent the same mistake
- Ruthlessly iterate on these lessons until mistake rate drops
- Review lessons at session start for relevant project

### 4. Verification Before Done
- Never mark a task complete without proving it works
- Diff behavior between main and your changes when relevant
- Ask yourself: "Would a staff engineer approve this?"
- Run tests, check logs, demonstrate correctness

### 5. Demand Elegance (Balanced)
- For non-trivial changes: pause and ask "is there a more elegant way?"
- If a fix feels hacky: "Knowing everything I know now, implement the elegant solution"
- Skip this for simple, obvious fixes – don't over-engineer
- Challenge your own work before presenting it

### 6. Autonomous Bug Fixing
- When given a bug report: just fix it. Don't ask for hand-holding
- Point at logs, errors, failing tests – then resolve them
- Zero context switching required from the user
- Go fix failing CI tests without being told how

## Task Management

1. **Plan First**: Write plan to `tasks/todo.md` with checkable items
2. **Verify Plan**: Check in before starting implementation
3. **Track Progress**: Mark items complete as you go
4. **Explain Changes**: High-level summary at each step
5. **Document Results**: Add review section to `tasks/todo.md`
6. **Capture Lessons**: Update `tasks/lessons.md` after corrections

## Core Principles

- **Simplicity First**: Make every change as simple as possible. Impact minimal code.
- **No Laziness**: Find root causes. No temporary fixes. Senior developer standards.
- **Minimal Impact**: Changes should only touch what's necessary. Avoid introducing bugs.
