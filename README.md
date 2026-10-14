# BBAT104 TQM Project - Library Management System (Q06)

**Student:** Priya Mehta  
**Roll No.:** 2410301051  
**Branch / Section:** CSE / A  
**Session:** 2026-27  
**Quality Goal:** Q06 - Reduce Duplicate Entries

## Teacher-reference aligned architecture
The project follows the supplied reference discussion's separation of concerns:

`User -> UI -> Service -> Model/Database -> Reports/TQM`

- **UI:** screens and user interaction only; no SQL.
- **Services:** business rules, validation decisions and process control.
- **Models:** data objects representing books, members and issues.
- **Database:** SQLite persistence, schema, indexes and constraints.
- **Reports:** quality metrics and audit/defect summaries.
- **Utils:** validation, audit/error logging and backup.
- **TQM artefacts:** CTQ, SIPOC, FMEA, checksheet, Pareto, Fishbone and PDCA.

## Q06 controls implemented
1. Unique ISBN constraint
2. Unique member-code constraint
3. Pre-add validation
4. Search Before Add
5. Confirmation dialogs

## Run
```bash
python run.py

## Testing

To run the automated tests, open the VS Code terminal and type:

```bash
python -m unittest discover -s tests -v
```

## Folder map
```text
config/       settings
 database/    db, schema, migrations, seed
models/       book, member, issue
services/     business rules and process control
ui/           Dashboard, Books, Members, Issue/Return, Quality
reports/      TQM metrics
utils/        validators, logs, backup
artifacts/    TQM figures
 data/        SQLite database and backups
 docs/        project report and specification
tests/        validation tests
main.py       application entry point
run.py     launcher to start the application
```

## Viva line
**The UI never writes SQL; validation prevents bad data; audit/error logs provide evidence for TQM analysis; the logs feed Pareto, FMEA and PDCA improvement.**
