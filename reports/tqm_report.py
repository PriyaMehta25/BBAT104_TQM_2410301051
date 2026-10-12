from database.db import fetchall, fetchone


def dashboard_metrics():
    books = fetchone('SELECT COUNT(*) FROM books')[0]
    members = fetchone('SELECT COUNT(*) FROM members')[0]
    active_issues = fetchone("SELECT COUNT(*) FROM issues WHERE status='Issued'")[0]
    duplicate_defects = fetchone("SELECT COUNT(*) FROM error_logs WHERE category='Duplicate Prevention'")[0]
    validation_defects = fetchone("SELECT COUNT(*) FROM error_logs WHERE category='Validation'")[0]
    return {
        'books': books,
        'members': members,
        'active_issues': active_issues,
        'duplicate_defects': duplicate_defects,
        'validation_defects': validation_defects,
    }


def defect_summary():
    return fetchall('SELECT category, COUNT(*) FROM error_logs GROUP BY category ORDER BY COUNT(*) DESC')


def recent_audit(limit=8):
    return fetchall('SELECT action,entity,details,log_time FROM audit_logs ORDER BY log_id DESC LIMIT ?', (limit,))
