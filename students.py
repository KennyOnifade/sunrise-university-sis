from database import get_connection, log_action

def insert_student(name, email, age, course, gpa, current_user):
    """
    Insert a new student into the database.

    Args:
        name (str): Student full name.
        email (str): Student email address.
        age (int): Student age.
        course (str): Enrolled course.
        gpa (float): Student GPA (0.0 - 4.0).
        current_user (dict): Logged in user performing the action.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO students (name, email, age, course, gpa)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (email) DO NOTHING;
        """, (name.strip().title(), email.lower(), 
              age, course, gpa))
        conn.commit()
        log_action(current_user["username"],
                  f"Added student: {name}")
        print(f"✅ Student '{name}' added successfully.")
    except Exception as e:
        print(f"❌ Error inserting student: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def get_all_students(current_user):
    """
    Retrieve all students from the database.

    Args:
        current_user (dict): Logged in user performing the action.

    Returns:
        list: List of all student records.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name, email, age, course, gpa
        FROM students
        ORDER BY name;
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    log_action(current_user["username"],
              "Viewed all student records")
    return rows

def filter_students_by_gpa(min_gpa, max_gpa, current_user):
    """
    Filter students by GPA range.

    Args:
        min_gpa (float): Minimum GPA.
        max_gpa (float): Maximum GPA.
        current_user (dict): Logged in user performing the action.

    Returns:
        list: Filtered student records.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT name, email, age, course, gpa
        FROM students
        WHERE gpa BETWEEN %s AND %s
        ORDER BY gpa DESC;
    """, (min_gpa, max_gpa))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    log_action(current_user["username"],
              f"Filtered students by GPA {min_gpa}-{max_gpa}")
    return rows

def get_course_counts(current_user):
    """
    Count students per course from real data.

    Args:
        current_user (dict): Logged in user performing the action.

    Returns:
        dict: Course names and their student counts.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT course, COUNT(*) as count
        FROM students
        GROUP BY course
        ORDER BY count DESC;
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    log_action(current_user["username"],
              "Viewed course enrollment analytics")
    return {row[0]: row[1] for row in rows}

def get_average_gpa_per_course(current_user):
    """
    Calculate average GPA per course from real data.

    Args:
        current_user (dict): Logged in user performing the action.

    Returns:
        dict: Course names and their average GPAs.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT course, ROUND(AVG(gpa), 2) as avg_gpa
        FROM students
        GROUP BY course
        ORDER BY avg_gpa DESC;
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    log_action(current_user["username"],
              "Viewed average GPA per course analytics")
    return {row[0]: float(row[1]) for row in rows}

def add_sample_students(current_user):
    """
    Add realistic sample students for demonstration.

    Args:
        current_user (dict): Logged in user performing the action.
    """
    sample_students = [
        ("James Carter",     "james.carter@university.edu",
         20, "Information Systems", 3.8),
        ("Maria Lopez",      "maria.lopez@university.edu",
         22, "Computer Science",    3.5),
        ("Robert Johnson",   "robert.johnson@university.edu",
         21, "Mathematics",         3.2),
        ("Emily Davis",      "emily.davis@university.edu",
         23, "Information Systems", 3.9),
        ("Michael Brown",    "michael.brown@university.edu",
         20, "Computer Science",    2.8),
        ("Sarah Wilson",     "sarah.wilson@university.edu",
         22, "Mathematics",         3.6),
        ("David Martinez",   "david.martinez@university.edu",
         21, "Information Systems", 3.1),
        ("Jennifer Taylor",  "jennifer.taylor@university.edu",
         24, "Computer Science",    3.7),
        ("William Anderson", "william.anderson@university.edu",
         20, "Mathematics",         2.9),
        ("Linda Thomas",     "linda.thomas@university.edu",
         23, "Information Systems", 3.4),
    ]
    print("Adding sample students...")
    for name, email, age, course, gpa in sample_students:
        insert_student(name, email, age, 
                      course, gpa, current_user)
    print("✅ Sample students added successfully!")

# Test when run directly
if __name__ == "__main__":
    from auth import login
    user = login("admin", "Admin1234!")
    if user:
        add_sample_students(user)
        print("\nAll Students:")
        students = get_all_students(user)
        for s in students:
            print(f"  {s[0]} | {s[3]} | GPA: {s[4]}")
        print("\nCourse Enrollment Counts:")
        counts = get_course_counts(user)
        for course, count in counts.items():
            print(f"  {course}: {count} students")
        print("\nAverage GPA Per Course:")
        averages = get_average_gpa_per_course(user)
        for course, avg in averages.items():
            print(f"  {course}: {avg}")