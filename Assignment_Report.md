# ACADEMIC PROJECT REPORT

## Mini Project 1: Student Record Management System

---

### Academic Submission Details

- **Student Name**: Pritesh Gupta
- **Roll Number**: MCA - 08
- **Course**: Master of Computer Applications (MCA)
- **Semester**: Semester I
- **Subject**: Python Programming & Relational Database
- **Project Title**: Student Record Management System
- **Academic Year**: 2026 – 2027

---

## 1. Title Page & Certificate of Originality

```text
========================================================================================
                               ACADEMIC MINI PROJECT REPORT
                                            ON
                          STUDENT RECORD MANAGEMENT SYSTEM

                    Submitted in partial fulfillment of the requirements
                          for the degree of Master of Computer Applications
                                       (MCA - Semester I)

                 Course: Python Programming & Relational Database
========================================================================================
```

---

## 2. Introduction
In modern educational administration, maintaining accurate, secure, and accessible student academic records is critical. Traditional manual record-keeping methods and flat, unstructured text files suffer from data redundancy, lack of data validation, difficulty in querying, and risk of data loss.

The **Student Record Management System** is an interactive, menu-driven console application engineered using **Python 3** and an embedded **SQLite 3** relational database. It provides an efficient platform for faculty and administrators to perform comprehensive CRUD (Create, Read, Update, Delete) operations, automatic academic grade evaluations, strict multi-layer input validation, SQL `CHECK` constraints, and persistent file-based activity logging.

---

## 3. Problem Statement
Educational institutions often struggle with managing student academic information using ad-hoc flat files or spreadsheets. Key issues include:
1. **Duplicate Entries**: Inability to enforce unique student identification numbers.
2. **Data Inconsistency**: Absence of input validation leading to corrupt marks or invalid numeric values.
3. **Manual Grade Computation**: Errors in manual letter grade assignment from aggregate marks.
4. **Lack of Relational Storage**: Storing data in non-relational formats prevents structured querying using standard SQL.
5. **No Audit Trail**: Lack of persistent tracking of write, update, and delete actions.

This project directly resolves these challenges by building a structured relational application backed by SQLite, database constraints, defensive validation, and standard File I/O.

---

## 4. Objectives
- To design and implement a menu-driven console application using procedural Python 3.
- To demonstrate practical implementation of relational database principles using SQLite and parameterized SQL.
- To enforce data integrity using Primary Key and SQL `CHECK` constraints (Age 16–100, Semester 1–6, Marks 0–100).
- To implement defensive input validation helper functions (Student ID format `STUxxx`, Name, 10-digit Phone, Email).
- To automate academic letter grade calculation according to predefined institutional grade scales.
- To demonstrate Python File I/O operations through persistent activity logging in a separate text file.
- To implement comprehensive exception handling to ensure application stability during runtime.

---

## 5. Scope
The scope of this mini-project encompasses:
- Managing core student demographic and academic data (ID, Name, Age, Course, Semester, Email, Phone, Marks, Grade).
- Supporting essential database operations: Insert, Select (All & Search), Update, and Delete.
- Single-user console terminal execution with zero external library dependencies.
- Persistent local SQLite database storage and text-based activity auditing.

---

## 6. Technologies Used
- **Python 3.10+**: Core programming language utilizing standard procedural paradigms, structured control flow, and data structures.
- **SQLite 3**: Lightweight, zero-configuration, serverless relational database engine embedded directly inside Python.
- **`sqlite3` Module**: Python standard library interface for executing SQL queries and managing database transactions.
- **Python File I/O (`open()`)**: Built-in file streaming used in append mode (`"a"`) for audit logging.
- **`datetime` Module**: Standard library module for generating precise timestamps.

---

## 7. System Requirements

### Hardware Requirements
- **Processor**: Intel Core i3 or equivalent AMD processor (2.0 GHz or higher).
- **RAM**: 2 GB minimum (4 GB recommended).
- **Hard Disk Space**: 50 MB of free storage space.
- **Display**: Standard console / terminal monitor (80x24 characters minimum).

### Software Requirements
- **Operating System**: Windows 10/11, Linux (Ubuntu/Debian/Fedora), or macOS.
- **Runtime Environment**: Python 3.10 or higher.
- **Dependencies**: Python Standard Library only (no third-party packages required).

---

## 8. Functional Requirements
1. **Database Initialization**: The system must automatically connect to `student_records.db` and create the `students` table if it does not already exist.
2. **Student Registration (Add)**: The system must accept student details, validate each field strictly, compute letter grades, prevent duplicate IDs, and insert the record via SQL.
3. **Record Viewing (View All)**: The system must display all records in a formatted ASCII table with aligned columns and record counts.
4. **Search Mechanism**: The system must allow searching by exact Student ID or case-insensitive partial Student Name.
5. **Record Modification (Update)**: The system must allow field-by-field updates without re-entering unchanged data. Marks updates must automatically trigger grade recalculation.
6. **Record Removal (Delete)**: The system must require confirmation (`y/n`) prior to removing a record from the database.
7. **Audit Logging**: The system must log every successful Add, Update, and Delete operation to `activity_log.txt` with a timestamp.

---

## 9. Application Workflow
```text
+-------------------------------------------------------------+
|                      Start Application                      |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|           Initialize Database (student_records.db)          |
|      Create 'students' table with CHECK constraints         |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|                     Display Main Menu                       |
|   1. Add  2. View  3. Search  4. Update  5. Delete  6. Exit |
+-------------------------------------------------------------+
                              |
       +----------------------+----------------------+
       |                      |                      |
       v                      v                      v
[1. Add Student]       [2. View All]         [3. Search]
- Input Validations    - SQL SELECT *        - Enter ID / Name
- Auto Calculate Grade - Render ASCII Table  - Display Profile Card
- SQL INSERT           |                     |
- Log to File          |                     |
       |                      |                      |
       +----------------------+----------------------+
       |                      |                      |
       v                      v                      v
[4. Update Student]    [5. Delete Student]    [6. Exit]
- Enter ID             - Enter ID             - Display Goodbye
- Select Field         - Confirm (y/n)        - Close Connection
- SQL UPDATE           - SQL DELETE           - Terminate Cleanly
- Recompute Grade      - Log to File
- Log to File          |
       |               |
       +---------------+
               |
               v
  (Return to Main Menu Loop)
```

---

## 10. Basic System Architecture
The application is structured into four distinct logical layers:
1. **User Interface (UI) Layer**: Handles console input/output, formatted tables, menus, and user prompts.
2. **Validation & Business Logic Layer**: Enforces strict constraints (ID format, phone digits, email structure, numerical bounds, grade evaluation).
3. **Database Access Layer**: Executes parameterized SQL statements via Python's `sqlite3` cursor and manages transactions.
4. **Storage Layer**: Physical storage consisting of `student_records.db` (relational table) and `activity_log.txt` (flat text log).

---

## 11. Database Design & Schema
The application uses a normalized single-table design with embedded SQL `CHECK` constraints suitable for an MCA Semester-I mini project.

```text
+-----------------------------------------------------------------------------------------+
|                                        students                                         |
+--------------------+--------------+-----------------------------------------------------+
| Column Name        | Type         | Constraints                                         |
+--------------------+--------------+-----------------------------------------------------+
| student_id         | TEXT         | PRIMARY KEY, NOT NULL                               |
| name               | TEXT         | NOT NULL                                            |
| age                | INTEGER      | NOT NULL, CHECK(age BETWEEN 16 AND 100)             |
| course             | TEXT         | NOT NULL                                            |
| semester           | INTEGER      | NOT NULL, CHECK(semester BETWEEN 1 AND 6)           |
| email              | TEXT         | NOT NULL                                            |
| phone              | TEXT         | NOT NULL                                            |
| marks              | REAL         | NOT NULL, CHECK(marks BETWEEN 0 AND 100)            |
| grade              | TEXT         | NOT NULL                                            |
+--------------------+--------------+-----------------------------------------------------+
```

---

## 12. Primary Key
`student_id` is designated as the **Primary Key**.
- It guarantees that each student has a distinct, non-null identifier.
- SQLite creates a unique B-tree index on `student_id`, making record lookup and search operations fast.
- Duplicate primary key entries are blocked at the database engine level (`sqlite3.IntegrityError`).

---

## 13. SQL Operations
The project uses standard ANSI SQL statements executed via Python's cursor:

### Table Creation (DDL)
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

### Data Manipulation (DML)
- **Insert**:
  ```sql
  INSERT INTO students (student_id, name, age, course, semester, email, phone, marks, grade)
  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
  ```
- **Select (All)**:
  ```sql
  SELECT student_id, name, age, course, semester, email, phone, marks, grade 
  FROM students 
  ORDER BY student_id ASC;
  ```
- **Select (Search)**:
  ```sql
  SELECT student_id, name, age, course, semester, email, phone, marks, grade 
  FROM students 
  WHERE student_id = ? OR LOWER(name) LIKE LOWER(?);
  ```
- **Update**:
  ```sql
  UPDATE students SET marks = ?, grade = ? WHERE student_id = ?;
  ```
- **Delete**:
  ```sql
  DELETE FROM students WHERE student_id = ?;
  ```

---

## 14. Mapping of CRUD to Application Functions

| CRUD Action | SQL Operation | Python Function | Responsibility |
|---|---|---|---|
| **Create** | `INSERT` | `add_student(conn)` | Captures inputs, calculates grade, inserts record, logs to file. |
| **Read** | `SELECT` | `view_students(conn)` | Queries all records and formats into an aligned table. |
| **Read** | `SELECT` | `search_student(conn)` | Queries matching records by ID or Name and displays profile. |
| **Update** | `UPDATE` | `update_student(conn)` | Updates a chosen attribute and recalculates grade if marks change. |
| **Delete** | `DELETE` | `delete_student(conn)` | Confirms deletion and removes record from database. |

---

## 15. Python Concepts Used
1. **Data Types & Variables**: `str` for text, `int` for age/semester, `float` for marks, `tuple` for query parameters, `list` for query result collections.
2. **Conditionals**: `if-elif-else` branches for menu selection, input boundary checking, search results evaluation, and grade calculation.
3. **Loops**: `while` loops for the continuous main application loop and input re-prompting; `for` loops for iterating through database query tuples.
4. **Functions**: Modular code organization with clear parameter passing and single responsibilities.
5. **Context Managers**: `with open(...) as f:` ensuring automatic closing of file descriptors.
6. **Exception Handling**: Catching `ValueError`, `sqlite3.IntegrityError`, `sqlite3.Error`, and `OSError` to maintain program resilience.

---

## 16. File I/O Implementation
In addition to relational database storage, the project demonstrates Python File I/O by appending operational activity logs to `activity_log.txt`:
- **Mode**: Append (`"a"`)
- **Format**: `YYYY-MM-DD HH:MM:SS - <Action> student <ID>`
- **Example Log**:
  ```text
  2026-09-09 20:15:10 - Added student STU001
  2026-09-09 20:16:22 - Updated student STU001
  2026-09-09 20:17:05 - Deleted student STU001
  ```

---

## 17. Function Descriptions

### 17.1 `create_database(db_path)`
Establishes a connection to the SQLite database file and executes the `CREATE TABLE IF NOT EXISTS` DDL statement with `CHECK` constraints. Returns the active connection object.

### 17.2 `calculate_grade(marks)`
Accepts numeric marks (float) and returns the corresponding letter grade according to the academic scale:
- 90.0 – 100.0: `A+`
- 80.0 – 89.9: `A`
- 70.0 – 79.9: `B`
- 60.0 – 69.9: `C`
- 50.0 – 59.9: `D`
- Below 50.0: `F`

### 17.3 `log_activity(student_id, action, log_path)`
Formats current timestamp using `datetime.now()` and writes an audit entry to `activity_log.txt`.

### 17.4 `get_valid_student_id(prompt)`
Ensures Student ID follows the standard format `STU` followed by 3 to 6 digits (e.g., `STU001`, `STU2026`).

### 17.5 `get_valid_name(prompt)`
Validates that the name consists of letters and spaces between 2 and 50 characters, allowing dots for initials.

### 17.6 `get_valid_age(prompt)`
Validates that user input can be converted to an integer and falls within the required range `[16, 100]`.

### 17.7 `get_valid_course(prompt)`
Validates that course names are non-empty and alphabetic between 2 and 30 characters.

### 17.8 `get_valid_semester(prompt)`
Validates that semester numbers are integers within `[1, 6]`.

### 17.9 `get_valid_email(prompt)`
Validates that the email has username, `@`, and a valid domain containing `.`.

### 17.10 `get_valid_phone(prompt)`
Validates that the phone number contains exactly 10 digits starting with 6, 7, 8, or 9.

### 17.11 `get_valid_marks(prompt)`
Validates that marks entered are a valid float between `0.0` and `100.0`.

### 17.12 `display_student_card(student)`
Formats a single student tuple into a clear ASCII information card.

### 17.13 `add_student(conn)`
Collects all student attributes, validates duplicate keys, calculates grade, executes SQL `INSERT`, commits the transaction, and logs the operation.

### 17.14 `view_students(conn)`
Executes `SELECT * FROM students`, formats all records into an aligned table, and displays total count.

### 17.15 `search_student(conn)`
Queries students by exact ID match or case-insensitive partial Name match (`LIKE %query%`) and displays matching profile cards.

### 17.16 `update_student(conn)`
Provides a field-specific menu to update individual student attributes with strict validation. Recalculates grade if marks are changed.

### 17.17 `delete_student(conn)`
Locates the student record, presents a confirmation prompt (`y/n`), and executes SQL `DELETE` upon confirmation.

### 17.18 `main()`
Entry point coordinating the application startup, main loop, menu routing, and clean shutdown.

---

## 18. Input Validation & Defensive Design
The application incorporates strict input validation loops:
- Format validation for Student ID (`STU` + 3-6 digits).
- Alphabetic validation for Name and Course.
- Range validation for Age (`16` to `100`) and Semester (`1` to `6`).
- Standard email format verification.
- 10-digit Indian phone number verification.
- Strict floating-point range validation for Marks (`0.0` to `100.0`).
- Duplicate Primary Key validation prior to SQL execution.

---

## 19. Exception Handling
- **`ValueError`**: Caught during type casting (`int()`, `float()`), prompting the user to re-enter a valid number instead of crashing.
- **`sqlite3.IntegrityError`**: Handled gracefully if duplicate Primary Keys or SQL `CHECK` constraint violations occur.
- **`sqlite3.Error`**: Catches general SQLite operational exceptions.
- **`OSError`**: Catches file writing issues when appending to the activity log.

---

## 20. Sample Input and Output

### Adding a Student
```text
==================================================
                   ADD STUDENT
==================================================
Enter Student ID (e.g. STU001): STU001
Enter Student Name: Rahul Sharma
Enter Age (16-100): 22
Enter Course (e.g. MCA, BCA): MCA
Enter Semester (1-6): 1
Enter Email: rahul.sharma@example.com
Enter 10-digit Phone Number: 9876543210
Enter Marks (0-100): 82.5

Student added successfully!
```

### Viewing All Students
```text
==========================================================================================================
                                              ALL STUDENTS
==========================================================================================================
ID         Name                   Age   Course   Sem   Marks    Grade  Email                      Phone       
--------------------------------------------------------------------------------------------------------------
STU001     Rahul Sharma           22    MCA      1     82.50    A      rahul.sharma@example.com   9876543210  
STU002     Priya Patil            21    MCA      1     91.00    A+     priya.patil@example.com    9823456781  
STU003     Pritesh Gupta          22    MCA      1     88.50    A      pritesh.gupta@itm.edu      9812345678  
STU004     Amit Shah              23    MCA      1     74.00    B      amit.shah@example.com      9890123456  
STU005     Sneha Kulkarni         22    MCA      1     65.50    C      sneha.k@example.com        9871234560  
--------------------------------------------------------------------------------------------------------------
Total Students: 5
==========================================================================================================
```

---

## 21. Test Cases and Verification Results

All 19 unit and integration test cases were executed against the application using the automated test suite `test_student_management.py`:

| Test # | Test Scenario | Input Data | Expected Output | Status |
|---|---|---|---|---|
| **TC-01** | Student ID Validation | `STU001`, `abc`, `123`, `STU@001` | Accepts `STU001`, rejects invalid formats | **PASS** |
| **TC-02** | Name Validation | `Rahul Sharma`, `12345`, `@@Rahul` | Accepts alphabetic names, rejects symbols/digits | **PASS** |
| **TC-03** | Age Validation | `22`, `abc`, `15`, `105` | Accepts 16–100, rejects out-of-range/text | **PASS** |
| **TC-04** | Course Validation | `MCA`, `12345`, `@@@` | Accepts valid course, rejects symbols/digits | **PASS** |
| **TC-05** | Semester Validation | `1` to `6`, `0`, `7`, `abc` | Accepts 1–6, rejects out-of-range/text | **PASS** |
| **TC-06** | Email Validation | `student@gmail.com`, `invalid@` | Accepts standard email, rejects invalid domain | **PASS** |
| **TC-07** | Phone Validation | `9876543210`, `12345`, `abc` | Accepts 10-digit mobile, rejects invalid length | **PASS** |
| **TC-08** | Marks Validation | `85.0`, `-10`, `105`, `abc` | Accepts 0.0–100.0, rejects out-of-range/text | **PASS** |
| **TC-09** | Grade Calculation Boundaries | `100, 90, 80, 70, 60, 50, 49` | Computes `A+, A, B, C, D, F` correctly | **PASS** |
| **TC-10** | Add Student (Create) | `STU001`, Rahul, 22, MCA, 1, 82.5 | Record inserted into SQLite; Grade = `A` | **PASS** |
| **TC-11** | Duplicate Student ID Rejection | `STU001` (already exists) | `Student ID already exists.` message | **PASS** |
| **TC-12** | View All Students (Read) | Option `2` | Aligned ASCII table with record count | **PASS** |
| **TC-13** | Search Student | `STU001`, `rahul`, `rah`, `NONE` | Exact ID, partial name matches found | **PASS** |
| **TC-14** | Update Student & Grade Recalc | `STU001` -> Marks `95.0` | Marks updated; Grade becomes `A+` | **PASS** |
| **TC-15** | Delete Student Confirmation | `STU001`, `n` (keep), `y` (delete) | Cancels on `n`, deletes on `y` | **PASS** |
| **TC-16** | Database Persistence | Close connection, Reopen | All records persist in `student_records.db` | **PASS** |
| **TC-17** | SQL CHECK Constraints | Invalid Age/Sem/Marks direct SQL | Database engine raises `IntegrityError` | **PASS** |
| **TC-18** | Activity Log File I/O | Add/Update/Delete actions | Entries recorded in `activity_log.txt` | **PASS** |
| **TC-19** | Automatic Schema Migration | Legacy unconstrained table | Safely migrates table to CHECK schema & preserves data | **PASS** |

---

## 22. Advantages of the System
- **Lightweight & Fast**: Built-in SQLite requires zero configuration or external database server setup.
- **Zero Dependencies**: Runs out of the box on any standard Python 3.10+ environment.
- **Relational Integrity**: Enforces uniqueness via Primary Keys and boundaries via SQL `CHECK` constraints.
- **User-Friendly Console UI**: Clear menus, formatted tables, and forgiving input validation.
- **Audit Logging**: Maintains a separate File I/O audit log of all database mutations.

---

## 23. Limitations
- **Single-User Environment**: Designed as a standalone console tool; does not support concurrent multi-user access over a network.
- **Single-Table Schema**: Does not normalize courses, semesters, or individual subject marks into separate relational tables.
- **Terminal Interface**: Lacks graphical UI or web frontend.

---

## 24. Future Enhancements
- **Multi-Table Relational Normalization**: Adding tables for `courses`, `subjects`, `attendance`, and `fee_payments` with foreign keys.
- **Graphical / Web User Interface**: Developing a desktop GUI using Tkinter or a web portal using Flask.
- **Report Generation**: Exporting student marksheets to PDF or CSV format.
- **Role-Based Authentication**: Adding faculty and student login credentials.

---

## 25. Conclusion
The **Student Record Management System** successfully satisfies all requirements of the MCA Semester-I curriculum. It demonstrates a solid understanding of fundamental Python programming (control flow, functions, exception handling, and file operations) combined with practical relational database management using SQLite, parameterized SQL, and database constraints. The application is robust, easy to navigate, defensively programmed, and fully documented for academic evaluation.
