from storage.database import Database
from storage.initializer import DatabaseInitializer
from services.quiz_service import QuizService

def main():
    db = Database("quiz.db")
    db.connect()
    DatabaseInitializer(db).initialize()
    service = QuizService(db)

    while True:
        print("\n--- Quiz Application ---")
        print("1. Create Quiz")
        print("2. View All Quizzes")
        print("3. Add Question to Quiz")
        print("4. Take Quiz")
        print("5. View Results for Quiz")
        print("6. Delete Quiz")
        print("7. Exit")
        choice = input("Choose: ").strip()

        try:
            if choice == "1":
                title = input("Quiz title: ")
                description = input("Description (optional): ")
                quiz = service.create_quiz(title, description)
                print(f"Created quiz with ID {quiz.id}")
            elif choice == "2":
                quizzes = service.get_all_quizzes()
                if not quizzes:
                    print("No quizzes available.")
                else:
                    for q in quizzes:
                        print(f"{q.id}: {q.title}")
            elif choice == "3":
                quiz_id = int(input("Quiz ID: "))
                text = input("Question text: ")
                print("Enter 4 options:")
                options = []
                for i in range(4):
                    options.append(input(f"Option {i+1}: "))
                correct = int(input("Correct option number (1-4): ")) - 1
                q = service.add_question(quiz_id, text, options, correct)
                print(f"Added question with ID {q.id}")
            elif choice == "4":
                quiz_id = int(input("Quiz ID to take: "))
                service.take_quiz(quiz_id)
            elif choice == "5":
                quiz_id = int(input("Quiz ID: "))
                results = service.get_results_for_quiz(quiz_id)
                if not results:
                    print("No results for this quiz.")
                else:
                    for r in results:
                        print(f"{r.taken_at} - Score: {r.score}/{r.total_questions}")
            elif choice == "6":
                quiz_id = int(input("Quiz ID to delete: "))
                service.delete_quiz(quiz_id)
                print("Quiz deleted.")
            elif choice == "7":
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