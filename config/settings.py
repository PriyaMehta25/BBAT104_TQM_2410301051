from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / 'data'
DB_PATH = DATA_DIR / 'library.db'
BACKUP_DIR = DATA_DIR / 'backups'
ARTIFACTS_DIR = ROOT_DIR / 'artifacts'
APP_NAME = 'Library Management System'
QUALITY_GOAL = 'Q06 - Reduce Duplicate Entries'
VERSION = '2.0'

BACKUP_DIR.mkdir(parents=True, exist_ok=True)
