import sqlite3
from pathlib import Path
from datetime import datetime

DB=Path("data/academy.db")
DB.parent.mkdir(exist_ok=True)

def con():
    c=sqlite3.connect(DB)
    c.row_factory=sqlite3.Row
    c.execute("CREATE TABLE IF NOT EXISTS progress(k TEXT PRIMARY KEY, done INTEGER DEFAULT 0, updated_at TEXT)")
    # Migration from older DBs.
    cols=[r[1] for r in c.execute("PRAGMA table_info(progress)").fetchall()]
    if "updated_at" not in cols:
        c.execute("ALTER TABLE progress ADD COLUMN updated_at TEXT")
    c.execute("CREATE TABLE IF NOT EXISTS notes(k TEXT PRIMARY KEY, txt TEXT DEFAULT '')")
    c.execute("CREATE TABLE IF NOT EXISTS cache(k TEXT PRIMARY KEY, txt TEXT DEFAULT '')")
    c.execute("""CREATE TABLE IF NOT EXISTS completion_events(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_key TEXT NOT NULL,
        completed_at TEXT NOT NULL,
        completed_date TEXT NOT NULL
    )""")
    c.execute("CREATE INDEX IF NOT EXISTS idx_events_date ON completion_events(completed_date)")
    c.commit(); return c

def done(k):
    c=con(); r=c.execute("SELECT done FROM progress WHERE k=?",(k,)).fetchone(); c.close()
    return bool(r[0]) if r else False

def set_done(k,v):
    c=con()
    old=c.execute("SELECT done FROM progress WHERE k=?",(k,)).fetchone()
    oldv=bool(old[0]) if old else False
    now=datetime.now().astimezone()
    c.execute("INSERT INTO progress(k,done,updated_at) VALUES(?,?,?) ON CONFLICT(k) DO UPDATE SET done=excluded.done, updated_at=excluded.updated_at",(k,int(v),now.isoformat(timespec="seconds")))
    # Record the day only when an item changes from incomplete -> complete.
    if v and not oldv:
        c.execute("INSERT INTO completion_events(item_key,completed_at,completed_date) VALUES(?,?,?)",(k,now.isoformat(timespec="seconds"),now.date().isoformat()))
    c.commit(); c.close()

def note(k):
    c=con(); r=c.execute("SELECT txt FROM notes WHERE k=?",(k,)).fetchone(); c.close(); return r[0] if r else ""

def set_note(k,v):
    c=con(); c.execute("INSERT INTO notes VALUES(?,?) ON CONFLICT(k) DO UPDATE SET txt=excluded.txt",(k,v)); c.commit(); c.close()

def cache(k):
    c=con(); r=c.execute("SELECT txt FROM cache WHERE k=?",(k,)).fetchone(); c.close(); return r[0] if r else ""

def set_cache(k,v):
    c=con(); c.execute("INSERT INTO cache VALUES(?,?) ON CONFLICT(k) DO UPDATE SET txt=excluded.txt",(k,v)); c.commit(); c.close()

def events_on(day):
    day=day.isoformat() if hasattr(day,"isoformat") else str(day)
    c=con(); rows=c.execute("SELECT item_key,completed_at FROM completion_events WHERE completed_date=? ORDER BY completed_at",(day,)).fetchall(); c.close()
    return [dict(r) for r in rows]

def completed_dates():
    c=con(); rows=c.execute("SELECT completed_date,COUNT(*) n FROM completion_events GROUP BY completed_date ORDER BY completed_date DESC").fetchall(); c.close()
    return {r["completed_date"]:r["n"] for r in rows}
