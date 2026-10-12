from database.db import execute


def audit(action, entity, entity_id=None, details='', user_name='student'):
    execute(
        'INSERT INTO audit_logs(action, entity, entity_id, details, user_name) VALUES(?,?,?,?,?)',
        (action, entity, entity_id, details, user_name),
    )


def log_error(code, category, message, user_name='student'):
    execute(
        'INSERT INTO error_logs(error_code, category, message, user_name) VALUES(?,?,?,?)',
        (code, category, message, user_name),
    )
