import matplotlib.pyplot as plt
from auth import login, register_user
from students import (get_all_students, filter_students_by_gpa,
                      get_course_counts, get_average_gpa_per_course,
                      insert_student)
from database import log_action

def get_gpa_range():
    """
    Get GPA range from user with input validation.

    Returns:
        tuple: (min_gpa, max_gpa) as floats.
    """
    while True:
        try:
            min_gpa = float(input("Enter minimum GPA (0.0 - 4.0): "))
            max_gpa = float(input("Enter maximum GPA (0.0 - 4.0): "))
            if not (0.0 <= min_gpa <= 4.0) or \
               not (0.0 <= max_gpa <= 4.0):
                print("❌ GPA must be between 0.0 and 4.0.")
                continue
            if min_gpa > max_gpa:
                print("❌ Minimum GPA cannot exceed maximum GPA.")
                continue
            return min_gpa, max_gpa
        except ValueError:
            print("❌ Please enter a valid GPA number.")

def visualize_data(course_counts, avg_gpa_per_course, students):
    """
    Create visualizations from real database data.

    Args:
        course_counts (dict): Real enrollment data from database.
        avg_gpa_per_course (dict): Real GPA averages from database.
        students (list): List of student records.
    """
    if not course_counts:
        print("❌ No data to visualize.")
        return

    # Bar chart — course enrollment counts
    plt.figure(figsize=(8, 6))
    plt.bar(course_counts.keys(),
            course_counts.values(), color="skyblue",
            edgecolor="black")
    plt.xlabel("Course")
    plt.ylabel("Number of Students")
    plt.title("Student Enrollment by Course")
    plt.tight_layout()
    plt.savefig("course_enrollment.png")
    plt.show()

    # Bar chart — average GPA per course
    plt.figure(figsize=(8, 6))
    plt.bar(avg_gpa_per_course.keys(),
            avg_gpa_per_course.values(),
            color="lightgreen", edgecolor="black")
    plt.xlabel("Course")
    plt.ylabel("Average GPA")
    plt.title("Average GPA by Course")
    plt.ylim(0, 4.0)
    plt.tight_layout()
    plt.savefig("average_gpa_per_course.png")
    plt.show()

    # Histogram — GPA distribution
    gpas = [s[4] for s in students]
    plt.figure(figsize=(8, 6))
    plt.hist(gpas, bins=5, color="lightcoral",
             edgecolor="black")
    plt.xlabel("GPA")
    plt.ylabel("Number of Students")
    plt.title("GPA Distribution of All Students")
    plt.tight_layout()
    plt.savefig("gpa_distribution.png")
    plt.show()

    # Pie chart — course enrollment
    plt.figure(figsize=(8, 6))
    plt.pie(course_counts.values(),
            labels=course_counts.keys(),
            autopct="%1.1f%%",
            colors=["lightblue", "lightgreen", "lightcoral"])
    plt.title("Course Enrollment Distribution")
    plt.tight_layout()
    plt.savefig("course_enrollment_pie.png")
    plt.show()

    print("✅ Visualizations saved and displayed!")

def add_new_student(current_user):
    """
    Prompt user to enter a new student's details.

    Args:
        current_user (dict): Logged in user.
    """
    print("\n--- Add New Student ---")
    name = input("Student full name: ")
    email = input("Student email: ")
    while True:
        try:
            age = int(input("Student age: "))
            if age < 0:
                print("❌ Age cannot be negative.")
                continue
            break
        except ValueError:
            print("❌ Please enter a valid age.")
    course = input("Enrolled course: ")
    while True:
        try:
            gpa = float(input("Student GPA (0.0 - 4.0): "))
            if not (0.0 <= gpa <= 4.0):
                print("❌ GPA must be between 0.0 and 4.0.")
                continue
            break
        except ValueError:
            print("❌ Please enter a valid GPA.")
    insert_student(name, email, age, course, gpa, current_user)

def generate_report(students, course_counts,
                   avg_gpa_per_course, current_user):
    """
    Save a student performance report to a text file.

    Args:
        students (list): All student records.
        course_counts (dict): Enrollment counts per course.
        avg_gpa_per_course (dict): Average GPA per course.
        current_user (dict): Logged in user.
    """
    filename = "student_performance_report.txt"
    try:
        with open(filename, "w") as f:
            f.write("="*50 + "\n")
            f.write("  STUDENT PERFORMANCE REPORT\n")
            f.write("  Sunrise University SIS\n")
            f.write("="*50 + "\n\n")
            f.write(f"Total Students: {len(students)}\n")
            mean_gpa = sum(s[4] for s in students) / len(students)
            f.write(f"Overall Mean GPA: {mean_gpa:.2f}\n\n")
            f.write("Course Enrollment:\n")
            for course, count in course_counts.items():
                f.write(f"  {course}: {count} students\n")
            f.write("\nAverage GPA Per Course:\n")
            for course, avg in avg_gpa_per_course.items():
                f.write(f"  {course}: {avg:.2f}\n")
            f.write("\nFull Student List:\n")
            f.write("-"*50 + "\n")
            for s in students:
                f.write(f"  {s[0]:<25} | {s[3]:<22}"
                       f" | GPA: {s[4]}\n")
        log_action(current_user["username"],
                  "Generated student performance report")
        print(f"✅ Report saved to '{filename}'")
    except IOError as e:
        print(f"❌ Error saving report: {e}")

def main():
    """Main SIS application with login and full menu."""
    print("\n" + "="*50)
    print("   Welcome to Sunrise University SIS")
    print("="*50)

    # --- LOGIN REQUIRED BEFORE ANYTHING ELSE ---
    current_user = None
    attempts = 0
    while current_user is None:
        if attempts >= 3:
            print("❌ Too many failed attempts. Exiting.")
            return
        print("\nPlease log in to continue.")
        username = input("Username: ")
        password = input("Password: ")
        current_user = login(username, password)
        if current_user is None:
            attempts += 1
            remaining = 3 - attempts
            if remaining > 0:
                print(f"  {remaining} attempt(s) remaining.")

    # --- MAIN MENU ---
    while True:
        print("\n" + "-"*50)
        print(f"  Logged in as: {current_user['username']}"
              f" ({current_user['role']})")
        print("-"*50)
        print("1. View all students")
        print("2. Filter students by GPA range")
        print("3. Add a new student")
        print("4. View analytics and visualizations")
        print("5. Generate performance report")
        print("6. Exit")
        print("-"*50)
        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            students = get_all_students(current_user)
            if students:
                print(f"\n{'Name':<25}{'Course':<25}"
                      f"{'Age':<6}{'GPA'}")
                print("-"*65)
                for s in students:
                    print(f"{s[0]:<25}{s[3]:<25}"
                          f"{s[2]:<6}{s[4]}")
            else:
                print("No students found in the database.")

        elif choice == "2":
            min_gpa, max_gpa = get_gpa_range()
            students = filter_students_by_gpa(
                min_gpa, max_gpa, current_user)
            if students:
                print(f"\nStudents with GPA "
                      f"{min_gpa:.1f} - {max_gpa:.1f}:")
                print(f"{'Name':<25}{'Course':<25}{'GPA'}")
                print("-"*55)
                for s in students:
                    print(f"{s[0]:<25}{s[3]:<25}{s[4]}")
            else:
                print(f"No students found with GPA "
                      f"between {min_gpa} and {max_gpa}.")

        elif choice == "3":
            add_new_student(current_user)

        elif choice == "4":
            students = get_all_students(current_user)
            course_counts = get_course_counts(current_user)
            avg_gpa = get_average_gpa_per_course(current_user)
            if not students:
                print("No data available to analyze.")
                continue
            mean_gpa = sum(s[4] for s in students) / len(students)
            print("\n--- Academic Analytics ---")
            print(f"Total Students : {len(students)}")
            print(f"Overall Mean GPA: {mean_gpa:.2f}")
            print("\nCourse Enrollment:")
            for course, count in course_counts.items():
                print(f"  {course}: {count} students")
            print("\nAverage GPA Per Course:")
            for course, avg in avg_gpa.items():
                print(f"  {course}: {avg:.2f}")

            # Recommendation based on real data
            lowest = min(avg_gpa.items(), key=lambda x: x[1])
            print(f"\n⚠️  Recommendation: '{lowest[0]}' has the "
                  f"lowest average GPA ({lowest[1]:.2f}). "
                  f"Consider additional academic support.")
            visualize_data(course_counts, avg_gpa, students)
            log_action(current_user["username"],
                      "Viewed full analytics and visualizations")

        elif choice == "5":
            students = get_all_students(current_user)
            course_counts = get_course_counts(current_user)
            avg_gpa = get_average_gpa_per_course(current_user)
            if not students:
                print("No data available for report.")
                continue
            generate_report(students, course_counts,
                          avg_gpa, current_user)

        elif choice == "6":
            log_action(current_user["username"],
                      "Logged out of the SIS system")
            print("\nGoodbye! Keep learning! 👋")
            break

        else:
            print("❌ Invalid choice. Please enter 1-6.")

if __name__ == "__main__":
    main()