from database.db import connect


def run_migrations():
    # Versioned migration hook kept intentionally simple for this academic project.
    con = connect()
    con.execute('CREATE TABLE IF NOT EXISTS schema_version(version INTEGER PRIMARY KEY)')
    con.execute('INSERT OR IGNORE INTO schema_version(version) VALUES (1)')
    con.commit()
    con.close()
