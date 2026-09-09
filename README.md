# Student Record Management System

**Course**: MCA Semester I – Python Programming & Relational Database  
**Subject Focus**: Python Programming & Relational Database Management with SQLite 3

---

## Project Description

The **Student Record Management System** is a robust, humanized, console-based application designed to manage student academic records. It integrates core **Python 3** programming concepts with an embedded **SQLite 3 relational database**, strict **SQL CHECK constraints**, defensive **input validation**, and **File I/O activity logging**.

The application is driven by a clean, menu-based terminal interface that allows users to perform full CRUD operations (Create, Read, Update, Delete) on student records. The system guarantees relational integrity, catches invalid input gracefully, automatically evaluates letter grades from numeric marks, and maintains an audit log of all database write operations.

---

## Key Features

- **Add Student (Create)**: Prompts for Student ID (`STU` + 3-6 digits), Name, Age (16-100), Course, Semester (1-6), Email, 10-digit Phone Number, and Marks (0-100). Enforces unique primary key constraint on Student ID.
- **View All Students (Read)**: Displays all stored student records in an aligned, readable ASCII tabular format with total student count.
- **Search Student (Read)**: Look up students by unique Student ID (exact match) or Student Name (case-insensitive substring search) and display a detailed student profile card.
- **Update Student (Update)**: Modify specific fields of an existing student with inline validation. If marks are modified, the letter grade is automatically recalculated.
- **Delete Student (Delete)**: Safely removes student records with an explicit `(y/n)` confirmation prompt.
- **Automatic Grade Calculation**: Computes letter grades (`A+`, `A`, `B`, `C`, `D`, `F`) based on aggregate marks (0.0 to 100.0).
- **Relational Storage (SQLite)**: Stores all records permanently in an embedded `student_records.db` database with table-level `CHECK` constraints.
- **File I/O Activity Logging**: Demonstrates Python File I/O by appending timestamped records of write operations (add, update, delete) to `activity_log.txt`.
- **Strict Input Validation**: Defensive validation for Student ID formats, names, numerical age/semester ranges, email formats, and 10-digit Indian phone numbers.
- **Zero External Dependencies**: Developed exclusively using the Python Standard Library.

---

## Technologies Used

- **Python 3.10+**: Core language for application logic, validation, and control flow.
- **SQLite 3**: Embedded serverless relational database engine.
- **`sqlite3` Module**: Python's standard library module for executing SQL queries and managing database transactions.
- **SQL (Structured Query Language)**: Standard relational database language used for `CREATE TABLE`, `INSERT`, `SELECT`, `UPDATE`, and `DELETE`.
- **Python File Handling**: Standard library `open()` with append mode (`"a"`) for audit logging.
- **`datetime` Module**: Generates timestamps for file logging.

---

## Database Architecture

- **Database File**: `student_records.db`
- **Table Name**: `students`
- **Primary Key**: `student_id` (enforces uniqueness for every student record)

### Database Schema (DDL)
```sql
CREATE TABLE IF NOT EXISTS students (
    student_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL CHECK(age BETWEEN 16 AND 100),
    course TEXT NOT NULL,
    semester INTEGER NOT NULL CHECK(semester BETWEEN 1 AND 6),
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    marks REAL NOT NULL CHECK(marks BETWEEN 0 AND 100),
    grade TEXT NOT NULL
);
```

---

## Strict Input Validation Rules

| Field | Rule / Format | Valid Example | Invalid Example |
|---|---|---|---|
| **Student ID** | Must start with `STU` followed by 3–6 digits | `STU001`, `STU2026` | `123`, `abc`, `STU@001` |
| **Name** | 2–50 chars, letters, spaces, optional initials | `Rahul Sharma`, `Pritesh Gupta` | `12345`, `Rahul123`, `@@Rahul` |
| **Age** | Integer between 16 and 100 | `22`, `18` | `abc`, `-5`, `150` |
| **Course** | 2–30 chars, letters & spaces | `MCA`, `BCA`, `Computer Science` | `12345`, `@@@` |
| **Semester** | Integer between 1 and 6 | `1`, `6` | `0`, `7`, `abc` |
| **Email** | Valid email with `@` and valid domain dot | `student@gmail.com` | `student`, `@gmail.com` |
| **Phone** | Exactly 10 digits, starts with 6, 7, 8, or 9 | `9876543210`, `8123456789` | `12345`, `1234567890`, `abc` |
| **Marks** | Float between 0.0 and 100.0 | `85.5`, `100.0` | `-10`, `105`, `abc` |

---

## File I/O Demonstration

To satisfy the academic requirement for **File I/O**, the application maintains an activity audit log in:

```text
activity_log.txt
```

Every successful `ADD`, `UPDATE`, or `DELETE` operation is appended to this text file with an accurate timestamp.

**Sample Log Entries**:
```text
2026-09-09 20:15:10 - Added student STU001
2026-09-09 20:16:22 - Updated student STU001
2026-09-09 20:17:05 - Deleted student STU001
```

---

## Grade Calculation System

Grades are evaluated automatically based on the following scale:

| Marks Range | Grade | Description |
|---|---|---|
| **90.0 – 100.0** | `A+` | Outstanding |
| **80.0 – 89.9** | `A` | Excellent |
| **70.0 – 79.9** | `B` | Very Good |
| **60.0 – 69.9** | `C` | Good |
| **50.0 – 59.9** | `D` | Pass |
| **Below 50.0** | `F` | Fail |

---

## How to Run

### Prerequisites
- Python 3.10 or higher installed.
- Zero third-party packages or virtual environment installations required.

### Execution Steps
1. Open a terminal or command prompt.
2. Navigate to the project directory:
   ```bash
   cd "e:\ITM\Assignment\Python with relation database\mini project 1"
   ```
3. Run the application:
   ```bash
   python student_management.py
   ```
4. To execute the automated test suite:
   ```bash
   python test_student_management.py
   ```

---

## Project Structure

```text
student-record-management/
│
├── student_management.py         # Main application source code
├── test_student_management.py    # Automated test suite (19 unit & integration tests)
├── student_records.db            # Persistent SQLite database file
├── activity_log.txt              # File I/O audit log file
│
├── README.md                     # GitHub-ready project README
├── Assignment_Report.md          # Full academic project report for MCA Semester I
├── requirements.txt              # Zero-dependency declaration
│
├── Doc/                          # Project Reference Documents
│   ├── 01_PRD.md                 # Product Requirements Document
│   ├── 02_TRD.md                 # Technical Requirements Document
│   ├── 03_UI_UX_Design.md        # UI/UX Console Design Specification
│   └── 04_Backend_Schema.md      # Database Schema & CRUD Mapping Document
│
└── screenshots/                  # Application execution screenshots
    ├── README.md                 # Screenshot descriptions & visual representations
    ├── 01-main-menu.png
    ├── 02-add-student.png
    ├── 03-view-students.png
    ├── 04-search-student.png
    ├── 05-update-student.png
    ├── 06-delete-student.png
    └── 07-database-persistence.png
```

---

## Screenshots

Screenshots illustrating console interactions are stored in the [screenshots/](screenshots/) directory:
- `01-main-menu.png`: Main menu navigation.
- `02-add-student.png`: Add student form and confirmation.
- `03-view-students.png`: Formatted tabular display of student records.
- `04-search-student.png`: Student profile card lookup.
- `05-update-student.png`: Updating record and auto-recalculated grade.
- `06-delete-student.png`: Confirmation-based deletion.
- `07-database-persistence.png`: Persistence verification across restarts.

---

## GitHub Repository
GitHub Repository: https://github.com/Andrew93541/mini-project-1-student-record-management
