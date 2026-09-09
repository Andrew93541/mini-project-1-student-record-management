"""
================================================================================
Student Record Management System
MCA Semester I – Python Programming & Relational Database

A robust, humanized console application demonstrating:
- Core Python 3 Programming (Conditionals, Loops, Functions, Data Structures)
- Real Relational Database Management using SQLite 3 and parameterized SQL
- Strict Data Integrity & SQL CHECK Constraints
- Complete CRUD Operations (Create, Read, Update, Delete)
- Defensive Input Validation Functions
- Automatic Academic Grade Evaluation
- Exception and Error Handling
- Persistent File I/O Activity Logging
================================================================================
"""

import os
import sqlite3
from datetime import datetime

# Database and log file configuration
DB_NAME = "student_records.db"
LOG_FILE = "activity_log.txt"


def connect_database(db_path=DB_NAME):
    """
    Establishes and returns a connection to the SQLite relational database.
    """
    return sqlite3.connect(db_path)


def create_database(db_path=DB_NAME):
    """
    Connects to the SQLite database and ensures the 'students' table exists
    with primary key, NOT NULL, and CHECK constraints.
    If a legacy table exists without CHECK constraints, it safely migrates
    existing data to the new schema.
    """
    conn = connect_database(db_path)
    cursor = conn.cursor()

    # Inspect current table schema in sqlite_master
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='students'")
    row = cursor.fetchone()

    if row is None:
        # Table does not exist, create it with all constraints
        cursor.execute(
            """
            CREATE TABLE students (
                student_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL CHECK(age BETWEEN 16 AND 100),
                course TEXT NOT NULL,
                semester INTEGER NOT NULL CHECK(semester BETWEEN 1 AND 6),
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                marks REAL NOT NULL CHECK(marks BETWEEN 0 AND 100),
                grade TEXT NOT NULL
            )
            """
        )
        conn.commit()
    else:
        existing_sql = row[0] or ""
        # Check if existing schema has the required CHECK constraints
        if "CHECK" not in existing_sql.upper() or "BETWEEN 16 AND 100" not in existing_sql.upper():
            # Legacy table detected: perform safe data migration
            cursor.execute("SELECT student_id, name, age, course, semester, email, phone, marks, grade FROM students")
            existing_records = cursor.fetchall()

            cursor.execute("DROP TABLE students")
            cursor.execute(
                """
                CREATE TABLE students (
                    student_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL CHECK(age BETWEEN 16 AND 100),
                    course TEXT NOT NULL,
                    semester INTEGER NOT NULL CHECK(semester BETWEEN 1 AND 6),
                    email TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    marks REAL NOT NULL CHECK(marks BETWEEN 0 AND 100),
                    grade TEXT NOT NULL
                )
                """
            )

            # Re-insert existing records safely
            for rec in existing_records:
                try:
                    cursor.execute(
                        """
                        INSERT INTO students (student_id, name, age, course, semester, email, phone, marks, grade)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        rec
                    )
                except sqlite3.Error:
                    pass  # Skip corrupt records violating new constraints

            conn.commit()

    return conn


def calculate_grade(marks):
    """
    Automatically calculates letter grade based on marks obtained:
    90 - 100 : A+
    80 - 89.9: A
    70 - 79.9: B
    60 - 69.9: C
    50 - 59.9: D
    Below 50 : F
    """
    if marks >= 90.0:
        return "A+"
    elif marks >= 80.0:
        return "A"
    elif marks >= 70.0:
        return "B"
    elif marks >= 60.0:
        return "C"
    elif marks >= 50.0:
        return "D"
    else:
        return "F"


def log_activity(student_id, action, log_path=LOG_FILE):
    """
    Demonstrates Python File I/O.
    Appends a timestamped log entry to activity_log.txt for write operations.
    """
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - {action.capitalize()} student {student_id}\n"
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except OSError as e:
        print(f"[Warning] Could not write to activity log: {e}")


# ==============================================================================
# STRICT INPUT VALIDATION HELPER FUNCTIONS
# ==============================================================================

def get_valid_student_id(prompt="Enter Student ID (e.g. STU001): "):
    """
    Validates Student ID format:
    - Must start with 'STU' followed by 3 to 6 numeric digits (e.g. STU001, STU2026).
    - Cannot be empty, contain spaces, or have special characters.
    """
    while True:
        raw = input(prompt).strip().upper()
        if not raw:
            print("Error: Student ID cannot be empty.")
            continue

        # Check pattern: STU + 3 to 6 digits
        if raw.startswith("STU") and len(raw) in range(6, 10) and raw[3:].isdigit():
            return raw

        print("Error: Invalid Student ID format. Must be 'STU' followed by 3-6 digits (e.g., STU001, STU2026).")


def get_valid_name(prompt="Enter Student Name: "):
    """
    Validates Student Name:
    - Between 2 and 50 characters.
    - Contains only letters and spaces (no numbers or special symbols).
    """
    while True:
        name = input(prompt).strip()
        if not name:
            print("Error: Name cannot be empty.")
            continue

        if len(name) < 2 or len(name) > 50:
            print("Error: Name must be between 2 and 50 characters long.")
            continue

        # Verify only letters, spaces, and optional dots for initials are present
        if all(c.isalpha() or c.isspace() or c == "." for c in name) and any(c.isalpha() for c in name):
            # Clean multiple internal spaces into a single space
            return " ".join(name.split())

        print("Error: Name must contain only letters, spaces, or dots for initials (no numbers or symbols).")


def get_valid_age(prompt="Enter Age (16-100): "):
    """
    Validates Student Age:
    - Integer between 16 and 100.
    """
    while True:
        raw_input = input(prompt).strip()
        try:
            age = int(raw_input)
            if 16 <= age <= 100:
                return age
            print("Error: Age must be between 16 and 100.")
        except ValueError:
            print("Error: Invalid input. Please enter a whole number for age.")


def get_valid_course(prompt="Enter Course (e.g. MCA, BCA): "):
    """
    Validates Course Name:
    - Non-empty, 2 to 30 characters, letters and spaces only.
    """
    while True:
        course = input(prompt).strip()
        if not course:
            print("Error: Course cannot be empty.")
            continue

        if len(course) < 2 or len(course) > 30:
            print("Error: Course name must be between 2 and 30 characters.")
            continue

        # Check for letters, spaces, dots or hyphens
        valid_chars = all(c.isalnum() or c.isspace() or c in ".-" for c in course)
        has_letters = any(c.isalpha() for c in course)
        if valid_chars and has_letters:
            return " ".join(course.split())

        print("Error: Course name must contain letters (e.g., MCA, BCA, Computer Science).")


def get_valid_semester(prompt="Enter Semester (1-6): "):
    """
    Validates Semester:
    - Integer between 1 and 6.
    """
    while True:
        raw_input = input(prompt).strip()
        try:
            sem = int(raw_input)
            if 1 <= sem <= 6:
                return sem
            print("Error: Semester must be between 1 and 6.")
        except ValueError:
            print("Error: Invalid input. Please enter a whole number between 1 and 6.")


def get_valid_email(prompt="Enter Email: "):
    """
    Validates Email:
    - Not empty.
    - Contains exactly one '@'.
    - Has text before '@' and domain with '.' after '@'.
    """
    while True:
        email = input(prompt).strip().lower()
        if not email:
            print("Error: Email cannot be empty.")
            continue

        if email.count("@") == 1:
            username, domain = email.split("@")
            if username and domain and "." in domain:
                domain_parts = domain.split(".")
                # Check domain parts are not empty (e.g., .com or a.b)
                if all(part for part in domain_parts) and len(domain_parts[-1]) >= 2:
                    return email

        print("Error: Invalid email format. Example: student@gmail.com or rahul@college.edu")


def get_valid_phone(prompt="Enter 10-digit Phone Number: "):
    """
    Validates Phone Number:
    - Exactly 10 numeric digits.
    - Starts with 6, 7, 8, or 9 (Indian mobile format).
    """
    while True:
        phone = input(prompt).strip()
        if not phone:
            print("Error: Phone number cannot be empty.")
            continue

        if len(phone) == 10 and phone.isdigit():
            if phone[0] in ("6", "7", "8", "9"):
                return phone
            print("Error: Mobile number must start with 6, 7, 8, or 9.")
            continue

        print("Error: Phone number must contain exactly 10 numeric digits.")


def get_valid_marks(prompt="Enter Marks (0-100): "):
    """
    Validates Marks:
    - Float between 0.0 and 100.0.
    """
    while True:
        raw_input = input(prompt).strip()
        try:
            marks = float(raw_input)
            if 0.0 <= marks <= 100.0:
                return round(marks, 2)
            print("Error: Marks must be between 0 and 100.")
        except ValueError:
            print("Error: Invalid input. Please enter a numeric value for marks.")


def display_student_card(student):
    """
    Displays complete student profile in a formatted ASCII box.
    Expects a tuple: (student_id, name, age, course, semester, email, phone, marks, grade)
    """
    student_id, name, age, course, semester, email, phone, marks, grade = student
    print("==================================================")
    print("              STUDENT INFORMATION")
    print("==================================================")
    print(f"Student ID : {student_id}")
    print(f"Name       : {name}")
    print(f"Age        : {age}")
    print(f"Course     : {course}")
    print(f"Semester   : {semester}")
    print(f"Email      : {email}")
    print(f"Phone      : {phone}")
    print(f"Marks      : {marks:.2f}")
    print(f"Grade      : {grade}")
    print("==================================================")


# ==============================================================================
# CRUD CONTROLLER FUNCTIONS
# ==============================================================================

def add_student(conn):
    """
    CREATE: Adds a new student record into SQLite.
    Demonstrates strict input validation, parameterized SQL INSERT,
    automatic grade calculation, and File I/O audit logging.
    """
    print("\n==================================================")
    print("                   ADD STUDENT")
    print("==================================================")

    student_id = get_valid_student_id("Enter Student ID (e.g. STU001): ")

    # Check if student ID already exists
    cursor = conn.cursor()
    cursor.execute("SELECT student_id FROM students WHERE student_id = ?", (student_id,))
    if cursor.fetchone():
        print("Student ID already exists. Please use a different ID.")
        return

    name = get_valid_name("Enter Student Name: ")
    age = get_valid_age("Enter Age (16-100): ")
    course = get_valid_course("Enter Course (e.g. MCA, BCA): ")
    semester = get_valid_semester("Enter Semester (1-6): ")
    email = get_valid_email("Enter Email: ")
    phone = get_valid_phone("Enter 10-digit Phone Number: ")
    marks = get_valid_marks("Enter Marks (0-100): ")

    # Calculate grade automatically
    grade = calculate_grade(marks)

    try:
        cursor.execute(
            """
            INSERT INTO students (student_id, name, age, course, semester, email, phone, marks, grade)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (student_id, name, age, course, semester, email, phone, marks, grade)
        )
        conn.commit()
        print("\nStudent added successfully!")
        log_activity(student_id, "added")
    except sqlite3.IntegrityError:
        print("Student ID already exists. Please use a different ID.")
    except sqlite3.Error as e:
        print(f"Database error while adding student: {e}")


def view_students(conn):
    """
    READ: Retrieves and displays all student records in an aligned ASCII table.
    Demonstrates SQL SELECT, loops, and formatted display.
    """
    print("\n==========================================================================================================")
    print("                                              ALL STUDENTS")
    print("==========================================================================================================")

    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT student_id, name, age, course, semester, email, phone, marks, grade
        FROM students
        ORDER BY student_id ASC
        """
    )
    records = cursor.fetchall()

    if not records:
        print("No student records found.")
        print("==========================================================================================================")
        return

    header = f"{'ID':<10} {'Name':<22} {'Age':<5} {'Course':<8} {'Sem':<5} {'Marks':<8} {'Grade':<6} {'Email':<26} {'Phone':<12}"
    print(header)
    print("-" * len(header))

    for row in records:
        s_id, s_name, s_age, s_course, s_sem, s_email, s_phone, s_marks, s_grade = row
        print(f"{s_id:<10} {s_name:<22} {s_age:<5} {s_course:<8} {s_sem:<5} {s_marks:<8.2f} {s_grade:<6} {s_email:<26} {s_phone:<12}")

    print("-" * len(header))
    print(f"Total Students: {len(records)}")
    print("==========================================================================================================")


def search_student(conn):
    """
    READ / SEARCH: Searches for student records by ID or Name.
    Demonstrates SQL parameterized queries and conditional results handling.
    """
    print("\n==================================================")
    print("                  SEARCH STUDENT")
    print("==================================================")

    query_str = input("Enter Student ID or Name: ").strip()
    if not query_str:
        print("Error: Search term cannot be empty.")
        return

    cursor = conn.cursor()

    # Search for exact ID match or case-insensitive partial Name match
    cursor.execute(
        """
        SELECT student_id, name, age, course, semester, email, phone, marks, grade
        FROM students
        WHERE student_id = ? OR LOWER(name) LIKE LOWER(?)
        ORDER BY student_id ASC
        """,
        (query_str.upper(), f"%{query_str}%")
    )
    results = cursor.fetchall()

    if not results:
        print("\nStudent record not found.")
        return

    print(f"\nFound {len(results)} matching record(s):")
    for student in results:
        display_student_card(student)


def update_student(conn):
    """
    UPDATE: Modifies a specific field of an existing student record.
    Ensures updated values adhere to strict validation, recalculates
    grades when marks change, and records modifications in activity_log.txt.
    """
    print("\n==================================================")
    print("                  UPDATE STUDENT")
    print("==================================================")

    student_id = input("Enter Student ID to update: ").strip().upper()
    if not student_id:
        print("Error: Student ID cannot be empty.")
        return

    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT student_id, name, age, course, semester, email, phone, marks, grade
        FROM students
        WHERE student_id = ?
        """,
        (student_id,)
    )
    student = cursor.fetchone()

    if not student:
        print("\nStudent record not found.")
        return

    print("\nCurrent Record:")
    display_student_card(student)

    print("\nSelect Field to Update:")
    print("1. Name")
    print("2. Age")
    print("3. Course")
    print("4. Semester")
    print("5. Email")
    print("6. Phone")
    print("7. Marks")
    print("8. Cancel")

    choice = input("\nEnter choice (1-8): ").strip()

    if choice == "1":
        new_name = get_valid_name("Enter New Name: ")
        cursor.execute("UPDATE students SET name = ? WHERE student_id = ?", (new_name, student_id))
    elif choice == "2":
        new_age = get_valid_age("Enter New Age (16-100): ")
        cursor.execute("UPDATE students SET age = ? WHERE student_id = ?", (new_age, student_id))
    elif choice == "3":
        new_course = get_valid_course("Enter New Course (e.g. MCA, BCA): ")
        cursor.execute("UPDATE students SET course = ? WHERE student_id = ?", (new_course, student_id))
    elif choice == "4":
        new_sem = get_valid_semester("Enter New Semester (1-6): ")
        cursor.execute("UPDATE students SET semester = ? WHERE student_id = ?", (new_sem, student_id))
    elif choice == "5":
        new_email = get_valid_email("Enter New Email: ")
        cursor.execute("UPDATE students SET email = ? WHERE student_id = ?", (new_email, student_id))
    elif choice == "6":
        new_phone = get_valid_phone("Enter New 10-digit Phone: ")
        cursor.execute("UPDATE students SET phone = ? WHERE student_id = ?", (new_phone, student_id))
    elif choice == "7":
        new_marks = get_valid_marks("Enter New Marks (0-100): ")
        new_grade = calculate_grade(new_marks)
        cursor.execute(
            "UPDATE students SET marks = ?, grade = ? WHERE student_id = ?",
            (new_marks, new_grade, student_id)
        )
    elif choice == "8":
        print("Update cancelled.")
        return
    else:
        print("Invalid choice. Update cancelled.")
        return

    try:
        conn.commit()
        print("\nStudent record updated successfully!")
        log_activity(student_id, "updated")
    except sqlite3.Error as e:
        print(f"Database error while updating student: {e}")


def delete_student(conn):
    """
    DELETE: Deletes an existing student record after user confirmation.
    Demonstrates SQL DELETE, confirmation safety, and File I/O logging.
    """
    print("\n==================================================")
    print("                  DELETE STUDENT")
    print("==================================================")

    student_id = input("Enter Student ID to delete: ").strip().upper()
    if not student_id:
        print("Error: Student ID cannot be empty.")
        return

    cursor = conn.cursor()
    cursor.execute(
        "SELECT student_id, name, course, semester FROM students WHERE student_id = ?",
        (student_id,)
    )
    student = cursor.fetchone()

    if not student:
        print("\nStudent record not found.")
        return

    s_id, s_name, s_course, s_sem = student
    print(f"\nFound Student: {s_id} - {s_name} (Course: {s_course}, Sem: {s_sem})")
    confirm = input("Are you sure you want to delete this student? (y/n): ").strip().lower()

    if confirm in ("y", "yes"):
        try:
            cursor.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
            conn.commit()
            print("\nStudent record deleted successfully.")
            log_activity(student_id, "deleted")
        except sqlite3.Error as e:
            print(f"Database error while deleting student: {e}")
    else:
        print("\nDeletion cancelled. Student record retained.")


# ==============================================================================
# MAIN APPLICATION CONTROLLER
# ==============================================================================

def main():
    """
    Main entry point of the application. Initializes database connection
    and manages the primary menu-driven execution loop.
    """
    conn = create_database(DB_NAME)

    while True:
        print("\n==================================================")
        print("           STUDENT RECORD MANAGEMENT")
        print("==================================================")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")
        print("--------------------------------------------------")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            add_student(conn)
        elif choice == "2":
            view_students(conn)
        elif choice == "3":
            search_student(conn)
        elif choice == "4":
            update_student(conn)
        elif choice == "5":
            delete_student(conn)
        elif choice == "6":
            print("\n==================================================")
            print("Thank you for using Student Record Management System.")
            print("Goodbye!")
            print("==================================================")
            break
        else:
            print("\nInvalid choice. Please select an option from the menu (1-6).")

    # Close database connection cleanly upon exit
    conn.close()


if __name__ == "__main__":
    main()
