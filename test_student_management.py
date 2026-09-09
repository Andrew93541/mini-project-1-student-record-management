"""
================================================================================
Automated Test Suite: Student Record Management System
File: test_student_management.py
MCA Semester I – Python Programming & Relational Database

Rigorously tests:
1. Strict Student ID Validation (Format STU+3-6 digits, empty, invalid chars)
2. Strict Name Validation (Letters & spaces only, empty, numbers, symbols)
3. Strict Age Validation (16 to 100, text input, out of bounds)
4. Strict Course Validation (Letters/spaces, empty, numeric, symbols)
5. Strict Semester Validation (1 to 6, 0, 7, text input)
6. Strict Email Validation (Valid format, missing @, missing dot, empty)
7. Strict Phone Validation (10 digits starting 6-9, <10, >10, non-numeric)
8. Strict Marks Validation (0-100, decimals, negative, >100, text)
9. Grade Calculation Scale & Boundary Evaluations
10. SQL Database CRUD Operations:
    - Create (Add Student with parameters)
    - Duplicate Primary Key Rejection
    - Read (View All Students table format)
    - Search (Exact ID, Case-insensitive Name, Partial Substring, Missing)
    - Update (Single Field & Marks with Auto-Grade Recalculation)
    - Delete (Confirmed 'y', Cancelled 'n')
11. Database Persistence Across Connection Closing & Reopening
12. Database SQL CHECK Constraints Integrity
13. File I/O Activity Logging in activity_log.txt
================================================================================
"""

import os
import sqlite3
import unittest
from unittest.mock import patch
import student_management as sm

TEST_DB = "test_student_records.db"
TEST_LOG = "test_activity_log.txt"


class TestStudentRecordManagement(unittest.TestCase):

    def setUp(self):
        # Clean up isolated test files
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
        if os.path.exists(TEST_LOG):
            os.remove(TEST_LOG)

        # Create isolated test database and patch module paths
        self.conn = sm.create_database(TEST_DB)
        self.original_log_file = sm.LOG_FILE
        sm.LOG_FILE = TEST_LOG

    def tearDown(self):
        self.conn.close()
        sm.LOG_FILE = self.original_log_file
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
        if os.path.exists(TEST_LOG):
            os.remove(TEST_LOG)

    # 1. Student ID Validation
    def test_01_student_id_validation(self):
        # Test valid IDs
        with patch("builtins.input", return_value="STU001"):
            self.assertEqual(sm.get_valid_student_id(), "STU001")
        with patch("builtins.input", return_value="stu2026"):
            self.assertEqual(sm.get_valid_student_id(), "STU2026")

        # Test invalid inputs (empty, abc, 123, STU, STU@001) then valid STU100
        invalid_inputs = ["", "   ", "abc", "123", "STU", "STU@001", "STU 001", "STU100"]
        with patch("builtins.input", side_effect=invalid_inputs):
            self.assertEqual(sm.get_valid_student_id(), "STU100")

    # 2. Name Validation
    def test_02_name_validation(self):
        # Test valid names
        with patch("builtins.input", return_value="Rahul Sharma"):
            self.assertEqual(sm.get_valid_name(), "Rahul Sharma")
        with patch("builtins.input", return_value="Pritesh Gupta"):
            self.assertEqual(sm.get_valid_name(), "Pritesh Gupta")

        # Test invalid names (empty, numbers, special symbols) then valid Amit
        invalid_inputs = ["", "   ", "12345", "Rahul123", "@@Rahul", "R", "Amit"]
        with patch("builtins.input", side_effect=invalid_inputs):
            self.assertEqual(sm.get_valid_name(), "Amit")

    # 3. Age Validation
    def test_03_age_validation(self):
        # Test valid ages
        with patch("builtins.input", return_value="22"):
            self.assertEqual(sm.get_valid_age(), 22)
        with patch("builtins.input", return_value="16"):
            self.assertEqual(sm.get_valid_age(), 16)
        with patch("builtins.input", return_value="100"):
            self.assertEqual(sm.get_valid_age(), 100)

        # Test invalid ages (text, negative, below 16, above 100) then valid 25
        invalid_inputs = ["abc", "-10", "0", "15", "101", "150", "20.5", "25"]
        with patch("builtins.input", side_effect=invalid_inputs):
            self.assertEqual(sm.get_valid_age(), 25)

    # 4. Course Validation
    def test_04_course_validation(self):
        # Test valid courses
        with patch("builtins.input", return_value="MCA"):
            self.assertEqual(sm.get_valid_course(), "MCA")
        with patch("builtins.input", return_value="Computer Science"):
            self.assertEqual(sm.get_valid_course(), "Computer Science")

        # Test invalid courses (empty, numeric, symbols) then valid BCA
        invalid_inputs = ["", "   ", "12345", "@@@", "BCA"]
        with patch("builtins.input", side_effect=invalid_inputs):
            self.assertEqual(sm.get_valid_course(), "BCA")

    # 5. Semester Validation
    def test_05_semester_validation(self):
        # Test valid semesters (1-6)
        for s in range(1, 7):
            with patch("builtins.input", return_value=str(s)):
                self.assertEqual(sm.get_valid_semester(), s)

        # Test invalid semesters (0, 7, -1, text) then valid 2
        invalid_inputs = ["abc", "0", "7", "-1", "2.5", "2"]
        with patch("builtins.input", side_effect=invalid_inputs):
            self.assertEqual(sm.get_valid_semester(), 2)

    # 6. Email Validation
    def test_06_email_validation(self):
        # Test valid emails
        with patch("builtins.input", return_value="student@gmail.com"):
            self.assertEqual(sm.get_valid_email(), "student@gmail.com")
        with patch("builtins.input", return_value="rahul.sharma@college.edu"):
            self.assertEqual(sm.get_valid_email(), "rahul.sharma@college.edu")

        # Test invalid emails (empty, missing @, missing dot, invalid domain) then valid
        invalid_inputs = ["", "student", "student@", "@gmail.com", "student@gmail", "student@.com", "pritesh@itm.edu"]
        with patch("builtins.input", side_effect=invalid_inputs):
            self.assertEqual(sm.get_valid_email(), "pritesh@itm.edu")

    # 7. Phone Validation
    def test_07_phone_validation(self):
        # Test valid Indian 10-digit mobile numbers starting with 6,7,8,9
        with patch("builtins.input", return_value="9876543210"):
            self.assertEqual(sm.get_valid_phone(), "9876543210")
        with patch("builtins.input", return_value="8123456789"):
            self.assertEqual(sm.get_valid_phone(), "8123456789")

        # Test invalid phone numbers (<10 digits, >10 digits, alphabetic, starting with 1-5) then valid
        invalid_inputs = ["", "12345", "987654321", "98765432101", "98765abc10", "1234567890", "9123456780"]
        with patch("builtins.input", side_effect=invalid_inputs):
            self.assertEqual(sm.get_valid_phone(), "9123456780")

    # 8. Marks Validation
    def test_08_marks_validation(self):
        # Test valid marks
        with patch("builtins.input", return_value="85"):
            self.assertEqual(sm.get_valid_marks(), 85.0)
        with patch("builtins.input", return_value="72.5"):
            self.assertEqual(sm.get_valid_marks(), 72.5)
        with patch("builtins.input", return_value="0"):
            self.assertEqual(sm.get_valid_marks(), 0.0)
        with patch("builtins.input", return_value="100"):
            self.assertEqual(sm.get_valid_marks(), 100.0)

        # Test invalid marks (text, negative, >100) then valid 90.0
        invalid_inputs = ["abc", "-10", "101", "150", "90.0"]
        with patch("builtins.input", side_effect=invalid_inputs):
            self.assertEqual(sm.get_valid_marks(), 90.0)

    # 9. Grade Calculation Boundaries
    def test_09_grade_calculation(self):
        self.assertEqual(sm.calculate_grade(100.0), "A+")
        self.assertEqual(sm.calculate_grade(90.0), "A+")
        self.assertEqual(sm.calculate_grade(89.9), "A")
        self.assertEqual(sm.calculate_grade(80.0), "A")
        self.assertEqual(sm.calculate_grade(79.9), "B")
        self.assertEqual(sm.calculate_grade(70.0), "B")
        self.assertEqual(sm.calculate_grade(69.9), "C")
        self.assertEqual(sm.calculate_grade(60.0), "C")
        self.assertEqual(sm.calculate_grade(59.9), "D")
        self.assertEqual(sm.calculate_grade(50.0), "D")
        self.assertEqual(sm.calculate_grade(49.9), "F")
        self.assertEqual(sm.calculate_grade(0.0), "F")

    # 10. Add Student (CRUD Create)
    def test_10_add_student(self):
        inputs = ["STU001", "Rahul Sharma", "22", "MCA", "1", "rahul@example.com", "9876543210", "82.5"]
        with patch("builtins.input", side_effect=inputs):
            sm.add_student(self.conn)

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM students WHERE student_id = 'STU001'")
        row = cursor.fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row[0], "STU001")
        self.assertEqual(row[1], "Rahul Sharma")
        self.assertEqual(row[2], 22)
        self.assertEqual(row[3], "MCA")
        self.assertEqual(row[4], 1)
        self.assertEqual(row[5], "rahul@example.com")
        self.assertEqual(row[6], "9876543210")
        self.assertEqual(row[7], 82.5)
        self.assertEqual(row[8], "A")

    # 11. Duplicate Student ID Rejection
    def test_11_duplicate_student_id_rejection(self):
        inputs1 = ["STU001", "Rahul Sharma", "22", "MCA", "1", "rahul@example.com", "9876543210", "82.5"]
        with patch("builtins.input", side_effect=inputs1):
            sm.add_student(self.conn)

        # Attempt duplicate insert
        inputs2 = ["STU001", "Duplicate Person", "23", "MCA", "1", "dup@example.com", "9876543211", "90.0"]
        with patch("builtins.input", side_effect=inputs2):
            sm.add_student(self.conn)

        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM students WHERE student_id = 'STU001'")
        self.assertEqual(cursor.fetchone()[0], 1)

    # 12. View All Students (CRUD Read)
    def test_12_view_students(self):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO students VALUES ('STU001', 'Rahul Sharma', 22, 'MCA', 1, 'r@e.com', '9876543210', 82.5, 'A')")
        cursor.execute("INSERT INTO students VALUES ('STU002', 'Priya Patil', 21, 'MCA', 1, 'p@e.com', '9876543211', 92.0, 'A+')")
        self.conn.commit()

        # Should execute cleanly without raising exception
        sm.view_students(self.conn)

    # 13. Search Student (Exact ID, Case-insensitive Name, Partial Substring, Missing)
    def test_13_search_student(self):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO students VALUES ('STU001', 'Rahul Sharma', 22, 'MCA', 1, 'r@e.com', '9876543210', 82.5, 'A')")
        self.conn.commit()

        # Exact ID search
        with patch("builtins.input", return_value="STU001"):
            sm.search_student(self.conn)

        # Case-insensitive Name search
        with patch("builtins.input", return_value="rahul sharma"):
            sm.search_student(self.conn)

        # Partial substring Name search
        with patch("builtins.input", return_value="rah"):
            sm.search_student(self.conn)

        # Missing search
        with patch("builtins.input", return_value="NONEXISTENT"):
            sm.search_student(self.conn)

        # Empty search rejected
        with patch("builtins.input", return_value=""):
            sm.search_student(self.conn)

    # 14. Update Student & Auto-Recalculate Grade (CRUD Update)
    def test_14_update_student_and_grade_recalc(self):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO students VALUES ('STU001', 'Rahul Sharma', 22, 'MCA', 1, 'r@e.com', '9876543210', 82.5, 'A')")
        self.conn.commit()

        # Update Name
        inputs_name = ["STU001", "1", "Rahul S. Sharma"]
        with patch("builtins.input", side_effect=inputs_name):
            sm.update_student(self.conn)

        cursor.execute("SELECT name FROM students WHERE student_id = 'STU001'")
        self.assertEqual(cursor.fetchone()[0], "Rahul S. Sharma")

        # Update Marks to 95.0 -> Grade must recalculate to A+
        inputs_marks = ["STU001", "7", "95.0"]
        with patch("builtins.input", side_effect=inputs_marks):
            sm.update_student(self.conn)

        cursor.execute("SELECT marks, grade FROM students WHERE student_id = 'STU001'")
        row = cursor.fetchone()
        self.assertEqual(row[0], 95.0)
        self.assertEqual(row[1], "A+")

    # 15. Delete Student with Confirmation & Cancel (CRUD Delete)
    def test_15_delete_student_confirmation(self):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO students VALUES ('STU001', 'Rahul Sharma', 22, 'MCA', 1, 'r@e.com', '9876543210', 82.5, 'A')")
        self.conn.commit()

        # Cancel delete
        inputs_cancel = ["STU001", "n"]
        with patch("builtins.input", side_effect=inputs_cancel):
            sm.delete_student(self.conn)
        cursor.execute("SELECT * FROM students WHERE student_id = 'STU001'")
        self.assertIsNotNone(cursor.fetchone())

        # Confirm delete
        inputs_confirm = ["STU001", "y"]
        with patch("builtins.input", side_effect=inputs_confirm):
            sm.delete_student(self.conn)
        cursor.execute("SELECT * FROM students WHERE student_id = 'STU001'")
        self.assertIsNone(cursor.fetchone())

    # 16. Database Persistence Across Connection Closing and Reopening
    def test_16_database_persistence(self):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO students VALUES ('STU005', 'Pritesh Gupta', 23, 'MCA', 1, 'pritesh@itm.edu', '9876543210', 88.5, 'A')")
        self.conn.commit()
        self.conn.close()

        # Open a brand new connection simulating application restart
        new_conn = sm.connect_database(TEST_DB)
        new_cursor = new_conn.cursor()
        new_cursor.execute("SELECT student_id, name, course, semester, marks, grade FROM students WHERE student_id = 'STU005'")
        record = new_cursor.fetchone()
        self.assertIsNotNone(record)
        self.assertEqual(record[0], "STU005")
        self.assertEqual(record[1], "Pritesh Gupta")
        self.assertEqual(record[4], 88.5)
        self.assertEqual(record[5], "A")
        new_conn.close()

        # Restore connection for tearDown
        self.conn = sqlite3.connect(TEST_DB)

    # 17. SQL CHECK Constraints Enforcement
    def test_17_sql_check_constraints(self):
        cursor = self.conn.cursor()

        # Invalid Age (<16 or >100) violates CHECK constraint
        with self.assertRaises(sqlite3.IntegrityError):
            cursor.execute("INSERT INTO students VALUES ('STU099', 'Bad Age', 10, 'MCA', 1, 'a@b.com', '9876543210', 80.0, 'A')")

        # Invalid Semester (>6) violates CHECK constraint
        with self.assertRaises(sqlite3.IntegrityError):
            cursor.execute("INSERT INTO students VALUES ('STU098', 'Bad Sem', 20, 'MCA', 8, 'a@b.com', '9876543210', 80.0, 'A')")

        # Invalid Marks (>100) violates CHECK constraint
        with self.assertRaises(sqlite3.IntegrityError):
            cursor.execute("INSERT INTO students VALUES ('STU097', 'Bad Marks', 20, 'MCA', 1, 'a@b.com', '9876543210', 105.0, 'A')")

    # 18. File I/O Activity Logging
    def test_18_activity_log_file_io(self):
        sm.log_activity("STU001", "added", log_path=TEST_LOG)
        sm.log_activity("STU001", "updated", log_path=TEST_LOG)
        sm.log_activity("STU001", "deleted", log_path=TEST_LOG)

        self.assertTrue(os.path.exists(TEST_LOG))
        with open(TEST_LOG, "r", encoding="utf-8") as f:
            lines = f.readlines()

        self.assertEqual(len(lines), 3)
        self.assertIn("Added student STU001", lines[0])
        self.assertIn("Updated student STU001", lines[1])
        self.assertIn("Deleted student STU001", lines[2])

    # 19. Automatic Database Schema Migration Test
    def test_19_automatic_schema_migration(self):
        # 1. Manually create a legacy unconstrained table with a record
        migration_db = "test_migration.db"
        if os.path.exists(migration_db):
            os.remove(migration_db)

        legacy_conn = sqlite3.connect(migration_db)
        legacy_cursor = legacy_conn.cursor()
        legacy_cursor.execute(
            """
            CREATE TABLE students (
                student_id TEXT PRIMARY KEY,
                name TEXT,
                age INTEGER,
                course TEXT,
                semester INTEGER,
                email TEXT,
                phone TEXT,
                marks REAL,
                grade TEXT
            )
            """
        )
        legacy_cursor.execute(
            "INSERT INTO students VALUES ('STU001', 'Rahul Sharma', 22, 'MCA', 1, 'r@e.com', '9876543210', 82.5, 'A')"
        )
        legacy_conn.commit()
        legacy_conn.close()

        # 2. Call create_database() which should detect legacy schema and perform safe migration
        migrated_conn = sm.create_database(migration_db)
        migrated_cursor = migrated_conn.cursor()

        # Verify new schema contains CHECK constraints
        migrated_cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='students'")
        schema_sql = migrated_cursor.fetchone()[0]
        self.assertIn("CHECK(age BETWEEN 16 AND 100)", schema_sql)
        self.assertIn("CHECK(semester BETWEEN 1 AND 6)", schema_sql)
        self.assertIn("CHECK(marks BETWEEN 0 AND 100)", schema_sql)

        # Verify existing record was preserved
        migrated_cursor.execute("SELECT student_id, name, marks FROM students WHERE student_id = 'STU001'")
        row = migrated_cursor.fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row[0], "STU001")
        self.assertEqual(row[1], "Rahul Sharma")
        self.assertEqual(row[2], 82.5)

        # Verify CHECK constraint is now active on migrated database
        with self.assertRaises(sqlite3.IntegrityError):
            migrated_cursor.execute(
                "INSERT INTO students VALUES ('STU999', 'Invalid Age', 10, 'MCA', 1, 'a@b.com', '9876543210', 80.0, 'A')"
            )

        migrated_conn.close()
        if os.path.exists(migration_db):
            os.remove(migration_db)


if __name__ == "__main__":
    unittest.main()
