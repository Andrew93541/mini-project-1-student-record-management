# Screenshots Directory
## Student Record Management System

This directory is prepared for storing console execution screenshots for academic project documentation and presentation.

### Required Screenshots List:

1. **`01-main-menu.png`**
   - **Description**: Main console menu displaying the banner and options 1 through 6.
   - **Sample Display**:
     ```text
     ==================================================
                STUDENT RECORD MANAGEMENT
     ==================================================
     1. Add Student
     2. View All Students
     3. Search Student
     4. Update Student
     5. Delete Student
     6. Exit
     --------------------------------------------------
     Enter your choice (1-6):
     ```

2. **`02-add-student.png`**
   - **Description**: Adding a new student record (prompts, strict validations, auto-grade computation, success message).
   - **Sample Display**:
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

3. **`03-view-students.png`**
   - **Description**: Viewing all students formatted in aligned ASCII table columns with total count.
   - **Sample Display**:
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

4. **`04-search-student.png`**
   - **Description**: Searching for a student by ID or Name (case-insensitive) and displaying the student profile card.
   - **Sample Display**:
     ```text
     ==================================================
                       SEARCH STUDENT
     ==================================================
     Enter Student ID or Name: Rahul

     Found 1 matching record(s):
     ==================================================
                   STUDENT INFORMATION
     ==================================================
     Student ID : STU001
     Name       : Rahul Sharma
     Age        : 22
     Course     : MCA
     Semester   : 1
     Email      : rahul.sharma@example.com
     Phone      : 9876543210
     Marks      : 82.50
     Grade      : A
     ==================================================
     ```

5. **`05-update-student.png`**
   - **Description**: Updating a specific field of an existing student (e.g., marks) and automatic grade recalculation.
   - **Sample Display**:
     ```text
     ==================================================
                       UPDATE STUDENT
     ==================================================
     Enter Student ID to update: STU001

     Current Record:
     ==================================================
                   STUDENT INFORMATION
     ==================================================
     Student ID : STU001
     Name       : Rahul Sharma
     Age        : 22
     Course     : MCA
     Semester   : 1
     Email      : rahul.sharma@example.com
     Phone      : 9876543210
     Marks      : 82.50
     Grade      : A
     ==================================================

     Select Field to Update:
     1. Name
     2. Age
     3. Course
     4. Semester
     5. Email
     6. Phone
     7. Marks
     8. Cancel

     Enter choice (1-8): 7
     Enter New Marks (0-100): 95.0

     Student record updated successfully!
     ```

6. **`06-delete-student.png`**
   - **Description**: Deleting a student record with confirmation prompt (`y/n`).
   - **Sample Display**:
     ```text
     ==================================================
                       DELETE STUDENT
     ==================================================
     Enter Student ID to delete: STU001

     Found Student: STU001 - Rahul Sharma (Course: MCA, Sem: 1)
     Are you sure you want to delete this student? (y/n): y

     Student record deleted successfully.
     ```

7. **`07-database-persistence.png`**
   - **Description**: Demonstrating data persistence after exiting and restarting the application or inspecting `student_records.db` with SQLite / Python.
