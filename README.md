# CallHub — Institutional Phone Directory System

A centralized contact management system built for IIT Gandhinagar to securely store, search, and manage member contact information with role-based access control, SQL indexing optimization, and security audit logging.

> **Team project (5 members).** The work was divided into equal modules. See [Team & Contributions](#team--contributions).

## Team & Contributions

| Member | Module |
|--------|--------|
| **Lokesh** | **Database (SQL): schema design, sample data, index design and benchmarking** |
| **Jaya Rama Krishna**| _e.g. Authentication and JWT sessions_ |
| **Thushar** | _e.g. Role-based access control and audit logging_ |
| **Sanjay** | _e.g. Backend APIs (members, departments)_ |
| **Komal** | _e.g. Frontend and analytics_ |

### My contribution (Database / SQL)
- Designed and wrote the relational schema (`sql/schema.sql`): members, contacts, departments, roles, permissions, and log tables.
- Prepared sample data for testing (`sql/Sample_Data.sql`).
- Designed 9 indexes (`sql/indexes.sql`) on frequently searched and joined columns (member name, email, department, role mapping, log tables).
- Benchmarked queries before and after indexing using MySQL profiling and a Python script (`scripts/benchmark.py`, results in `benchmark_results.txt`).

**Benchmark findings** (dataset of 5,020 members):
- Name search with JOINs: about 43% faster (Python timing) and about 60% faster (MySQL profiling).
- Department filter: about 16% faster.
- Email search: no meaningful change (-0.9%).
- Note: the `LIKE '%text%'` name search still scans the whole `Member` table, because a leading wildcard cannot use a normal B-tree index. Most of the gain came from the index on the `Member_Role` join column.

## Tech Stack

- **Backend:** Python 3, Flask
- **Database:** MySQL (also runs on XAMPP's MariaDB)
- **Auth:** JWT (JSON Web Tokens)
- **Frontend:** HTML, CSS, JavaScript

## Project Structure

```
├── app/
│   ├── app.py              # Main Flask app + page routes
│   ├── auth.py             # JWT login/logout/session
│   ├── rbac.py             # Role-based access decorators
│   ├── db.py               # MySQL connection (DB_CONFIG)
│   ├── routes/
│   │   ├── members.py      # Member CRUD APIs
│   │   ├── departments.py  # Department CRUD APIs
│   │   └── analytics.py    # Search, interactions, analytics
│   ├── templates/          # HTML pages
│   └── static/             # CSS + JS
├── sql/
│   ├── schema.sql          # Database schema
│   ├── dump_file.sql       # Database structure dump
│   ├── Sample_Data.sql     # Sample data (20 members)
│   ├── indexes.sql         # SQL indexes
│   └── benchmark_queries.sql  # Queries used for benchmarking
├── scripts/
│   └── benchmark.py        # Benchmarking script
├── logs/
│   └── audit.log           # Audit log file
├── benchmark_results.txt   # Benchmark output
├── report.ipynb            # Jupyter notebook report
├── requirements.txt
└── README.md
```

## Setup Instructions (Windows + VS Code)

### 1. Get the code
```bash
git clone https://github.com/gellajayaramakrishna/callhub.git
cd callhub
```
Or open the project folder in VS Code.

### 2. Start MySQL
Install **XAMPP**, open the XAMPP Control Panel and click **Start** next to **MySQL**.
(Any MySQL server works. The default `root` user with an empty password is assumed.)

### 3. Create the database and load data
From the VS Code terminal in the project folder:
```bash
cmd /c "C:\xampp\mysql\bin\mysql.exe -u root < sql\dump_file.sql"
cmd /c "C:\xampp\mysql\bin\mysql.exe -u root CallHub < sql\Sample_Data.sql"
```
Check it worked:
```bash
C:\xampp\mysql\bin\mysql.exe -u root -e "USE CallHub; SELECT COUNT(*) FROM Member;"
```
It should print `20`.

On Mac/Linux with `mysql` on your PATH, use `mysql -u root -p < sql/dump_file.sql`, and the same pattern for `Sample_Data.sql`.

### 4. Create virtual environment and install dependencies
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
(Mac/Linux: `python3 -m venv venv` and `source venv/bin/activate`.)

### 5. Database credentials
`app/db.py` reads settings from environment variables and falls back to these defaults:
```python
DB_CONFIG = {
    "host": "localhost",      # CALLHUB_DB_HOST
    "user": "root",           # CALLHUB_DB_USER
    "password": "",           # CALLHUB_DB_PASSWORD
    "database": "CallHub",    # CALLHUB_DB_NAME
}
```
If your MySQL root user has a password, set `CALLHUB_DB_PASSWORD` or edit the default.

### 6. Run the app
```bash
cd app
python app.py
```
Visit: `http://127.0.0.1:5000`

## Test Login Credentials

| Name | Email | Password | Role |
|------|-------|----------|------|
| Rohit Das | rohit@org.in | 9000000009 | Director (Admin) |
| Pooja Singh | pooja@org.in | 9000000008 | HOD (Admin) |
| Amit Sharma | amit@org.in | 9000000001 | Student (Regular) |

> Password = Primary phone number

## API Endpoints

| Endpoint | Method | Access | Description |
|----------|--------|--------|-------------|
| `/login` | POST | Public | Login and get JWT token |
| `/isAuth` | GET | Public | Verify session token |
| `/logout` | POST | Public | Logout |
| `/members` | GET | Login | Get all members |
| `/members/<id>` | GET | Login | Get single member |
| `/members` | POST | Admin | Add new member |
| `/members/<id>` | PUT | Admin | Update member |
| `/members/<id>` | DELETE | Admin | Soft-delete member |
| `/departments` | GET | Login | Get all departments |
| `/departments` | POST | Admin | Add department |
| `/departments/<id>` | PUT | Admin | Update department |
| `/departments/<id>` | DELETE | Admin | Delete department |
| `/search` | POST | Login | Search directory |
| `/analytics` | GET | Admin | Get analytics |
| `/login-history` | GET | Admin | Get login history |

## RBAC Roles

**Admin roles:** Director, HOD, Dean, Admin Staff, HR Manager
- Full CRUD on members and departments
- View analytics and audit logs

**Regular users:** Student, Professor, etc.
- Read-only access to directory
- Search and view profiles only

## Security

- JWT tokens expire after 2 hours
- All unauthorized access attempts logged to `logs/audit.log`
- Login history tracked with IP address and timestamps
- Input validation on all endpoints
