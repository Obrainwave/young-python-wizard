from storage.database import Database
from storage.initializer import DatabaseInitializer
from services.grade_service import GradeService

def main():
    db = Database("gradebook.db")
    db.connect()

    # Initialize database (only creates tables if they don't exist)
    DatabaseInitializer(db).initialize()

    service = GradeService(db)

    while True:
        print("\n--- Grade Calculator ---")
        print("1. Add Student")
        print("2. View Students")
        print("3. Add Course")
        print("4. View Courses")
        print("5. Add Assignment to Course")
        print("6. Record Score")
        print("7. Student Report")
        print("8. Exit")
        choice = input("Choose: ").strip()

        try:
            if choice == "1":
                name = input("Student name: ")
                student = service.add_student(name)
                print(f"Added student with ID {student.id}")
            elif choice == "2":
                students = service.get_all_students()
                for s in students:
                    print(f"{s.id}: {s.name}")
            elif choice == "3":
                name = input("Course name: ")
                course = service.add_course(name)
                print(f"Added course with ID {course.id}")
            elif choice == "4":
                courses = service.get_all_courses()
                for c in courses:
                    print(f"{c.id}: {c.name}")
            elif choice == "5":
                course_id = int(input("Course ID: "))
                name = input("Assignment name: ")
                max_score = float(input("Max score: "))
                weight = float(input("Weight (0-1): "))
                assignment = service.add_assignment(course_id, name, max_score, weight)
                print(f"Added assignment with ID {assignment.id}")
            elif choice == "6":
                student_id = int(input("Student ID: "))
                assignment_id = int(input("Assignment ID: "))
                score = float(input("Score: "))
                service.record_score(student_id, assignment_id, score)
                print("Score recorded.")
            elif choice == "7":
                student_id = int(input("Student ID: "))
                service.student_report(student_id)
            elif choice == "8":
                print("Goodbye!")
                break
            else:
                print("Invalid option.")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    db.close()

if __name__ == "__main__":
    main()