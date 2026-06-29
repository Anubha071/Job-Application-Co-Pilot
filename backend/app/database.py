from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import DATABASE_URL

# Create the SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} 
)


def ensure_sqlite_schema():
    """Ensure SQLite tables have the expected columns when models change."""
    # BROKEN CODE: existing databases may still have the legacy drafts schema.
    # Run migrate_drafts_schema.py once to rename coveR_letter to cover_letter
    # and add missing ats_score if needed.
    if not DATABASE_URL.startswith("sqlite"):
        return

    with engine.begin() as conn:
        existing = conn.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' AND name='applications'")
        ).fetchone()
        if not existing:
            return

        existing_columns = [row[1] for row in conn.execute(text("PRAGMA table_info(applications)")).fetchall()]
        expected_columns = {
            "company_name": "VARCHAR",
            "job_title": "VARCHAR",
            "status": "VARCHAR",
            "job_description": "TEXT",
            "resume_text": "TEXT",
            "resume_filename": "VARCHAR"
        }

        for column_name, column_type in expected_columns.items():
            if column_name not in existing_columns:
                conn.execute(
                    text(f"ALTER TABLE applications ADD COLUMN {column_name} {column_type}")
                )

        # Ensure the drafts table matches the Draft model when the app evolves.
        existing = conn.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' AND name='drafts'")
        ).fetchone()
        if existing:
            draft_columns = [row[1] for row in conn.execute(text("PRAGMA table_info(drafts)")).fetchall()]
            # BROKEN CODE: legacy schema used the incorrect drafts column name coveR_letter.
            # Migrate any old data to cover_letter and remove the bad column if possible.
            legacy_column = "coveR_letter"
            if "cover_letter" not in draft_columns:
                if legacy_column in draft_columns:
                    try:
                        conn.execute(text("ALTER TABLE drafts RENAME COLUMN coveR_letter TO cover_letter"))
                        draft_columns.remove(legacy_column)
                        draft_columns.append("cover_letter")
                    except Exception:
                        conn.execute(text("ALTER TABLE drafts ADD COLUMN cover_letter TEXT"))
                        conn.execute(text("UPDATE drafts SET cover_letter = coveR_letter"))
                else:
                    conn.execute(text("ALTER TABLE drafts ADD COLUMN cover_letter TEXT"))

            if legacy_column in draft_columns:
                try:
                    conn.execute(text("ALTER TABLE drafts DROP COLUMN coveR_letter"))
                except Exception:
                    # Some SQLite versions do not support DROP COLUMN.
                    pass

            if "ats_score" not in draft_columns:
                conn.execute(text("ALTER TABLE drafts ADD COLUMN ats_score TEXT"))

# SessionLocal class will be used to create database sessions
SessionLocal = sessionmaker(
    autocommit=False,   # We want to control when transactions are committed
    autoflush = False,  # We want to control when changes are flushed to the database
    bind = engine   # Bind the session to our engine
)

# Base class for our models
Base = declarative_base()

# Dependency function to get a database session
def get_db():
    db = SessionLocal() # Create a new database session
    try:
        yield db  # Yield the session to be used in the request
    finally:
        db.close()  # Ensure the session is closed after the request is done