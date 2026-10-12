from datetime import datetime
import shutil
from config.settings import DB_PATH, BACKUP_DIR
from utils.logger import audit


def create_backup():
    if not DB_PATH.exists():
        raise FileNotFoundError('Database file not found.')
    target = BACKUP_DIR / f"library_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    shutil.copy2(DB_PATH, target)
    audit('BACKUP', 'DATABASE', None, target.name)
    return target
