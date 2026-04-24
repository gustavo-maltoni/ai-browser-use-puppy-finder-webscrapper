import os
from config import DATABASE_FILENAME
from contextlib import contextmanager
from tinydb import TinyDB

@contextmanager
def db_session():
    # Create database connection
    db = TinyDB(
        DATABASE_FILENAME,
        ensure_ascii=False,
        indent=4,
        sort_keys=True,
        separators=(',', ': ')
    )

    try:
        # Yield database to session context
        yield db
    
    finally:
        # Close database connection when context is terminated
        db.close()

def create_tables() -> None:
    if os.path.exists(DATABASE_FILENAME):
        return;

    with db_session() as db:
        db.table('AD_PARSED_LINK', persist_empty=True) # Already visited links
        db.table('AD_FAILED_LINK', persist_empty=True) # Links that failed