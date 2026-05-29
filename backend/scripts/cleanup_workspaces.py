"""
Cleanup stale workspaces from the database.

Lists all workspaces with their row counts and last activity date.
Deletes workspaces that have been inactive for longer than --days (default 90).

Usage:
  cd backend
  source venv/bin/activate

  # List all workspaces
  python scripts/cleanup_workspaces.py --list

  # Preview what would be deleted (inactive > 90 days) — dry run by default
  python scripts/cleanup_workspaces.py --days 90

  # Actually delete stale workspaces
  python scripts/cleanup_workspaces.py --days 90 --confirm

  # Delete a specific workspace regardless of age
  python scripts/cleanup_workspaces.py --session my-workspace --confirm
"""

import os
import sys
import argparse
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from app.database import engine


def get_workspaces(conn):
    """Return a list of dicts with stats per workspace."""
    rows = conn.execute(text("""
        SELECT
            session_id,
            SUM(mentor_count)  AS mentors,
            SUM(mentee_count)  AS mentees,
            SUM(match_count)   AS matches,
            MAX(last_activity) AS last_activity
        FROM (
            SELECT session_id,
                   COUNT(*)  AS mentor_count,
                   0         AS mentee_count,
                   0         AS match_count,
                   MAX(created_at) AS last_activity
            FROM mentors GROUP BY session_id

            UNION ALL

            SELECT session_id,
                   0, COUNT(*), 0,
                   MAX(created_at)
            FROM mentees GROUP BY session_id

            UNION ALL

            SELECT session_id,
                   0, 0, COUNT(*),
                   MAX(created_at)
            FROM matches GROUP BY session_id
        ) combined
        GROUP BY session_id
        ORDER BY last_activity DESC
    """)).fetchall()

    workspaces = []
    for row in rows:
        last_activity = row.last_activity
        if isinstance(last_activity, str):
            last_activity = datetime.fromisoformat(last_activity)
        if last_activity and last_activity.tzinfo is None:
            last_activity = last_activity.replace(tzinfo=timezone.utc)

        workspaces.append({
            "session_id":    row.session_id,
            "mentors":       int(row.mentors  or 0),
            "mentees":       int(row.mentees  or 0),
            "matches":       int(row.matches  or 0),
            "last_activity": last_activity,
        })

    return workspaces


def delete_workspace(conn, session_id):
    conn.execute(text("DELETE FROM matches WHERE session_id = :sid"), {"sid": session_id})
    conn.execute(text("DELETE FROM mentees  WHERE session_id = :sid"), {"sid": session_id})
    conn.execute(text("DELETE FROM mentors  WHERE session_id = :sid"), {"sid": session_id})


def print_table(workspaces, cutoff=None):
    now = datetime.now(timezone.utc)
    header = f"{'WORKSPACE':<30} {'MENTORS':>7} {'MENTEES':>7} {'MATCHES':>7}  {'LAST ACTIVE':<20}  STATUS"
    print(header)
    print("-" * len(header))
    for w in workspaces:
        age = (now - w["last_activity"]).days if w["last_activity"] else "?"
        age_str = f"{age}d ago" if isinstance(age, int) else "unknown"
        stale = cutoff and w["last_activity"] and w["last_activity"] < cutoff
        status = "STALE" if stale else "ok"
        print(
            f"{w['session_id']:<30} {w['mentors']:>7} {w['mentees']:>7} {w['matches']:>7}"
            f"  {age_str:<20}  {status}"
        )


def main():
    parser = argparse.ArgumentParser(description="Clean up stale workspaces.")
    parser.add_argument("--list",    action="store_true", help="List all workspaces and exit.")
    parser.add_argument("--days",    type=int, default=90, help="Inactivity threshold in days (default: 90).")
    parser.add_argument("--session", type=str, help="Delete a specific workspace by code.")
    parser.add_argument("--confirm", action="store_true", help="Actually perform the deletion (default is dry run).")
    args = parser.parse_args()

    with engine.connect() as conn:
        workspaces = get_workspaces(conn)

        if not workspaces:
            print("No workspaces found.")
            return

        if args.list:
            print_table(workspaces)
            print(f"\nTotal workspaces: {len(workspaces)}")
            return

        # --- Target selection ---
        now = datetime.now(timezone.utc)

        if args.session:
            targets = [w for w in workspaces if w["session_id"] == args.session]
            if not targets:
                print(f"Workspace '{args.session}' not found.")
                sys.exit(1)
        else:
            cutoff = now - timedelta(days=args.days)
            targets = [w for w in workspaces if w["last_activity"] and w["last_activity"] < cutoff]

        cutoff_display = now - timedelta(days=args.days)
        print_table(workspaces, cutoff=cutoff_display if not args.session else None)
        print()

        if not targets:
            print(f"No workspaces inactive for more than {args.days} days. Nothing to delete.")
            return

        total_rows = sum(w["mentors"] + w["mentees"] + w["matches"] for w in targets)
        print(f"{'Would delete' if not args.confirm else 'Deleting'} {len(targets)} workspace(s) "
              f"({total_rows} total rows):")
        for w in targets:
            print(f"  • {w['session_id']}  ({w['mentors']} mentors, {w['mentees']} mentees, {w['matches']} matches)")

        if not args.confirm:
            print("\nDry run — pass --confirm to actually delete.")
            return

        print()
        for w in targets:
            delete_workspace(conn, w["session_id"])
            print(f"  Deleted: {w['session_id']}")

        conn.commit()
        print(f"\nDone. {len(targets)} workspace(s) removed.")


if __name__ == "__main__":
    main()
