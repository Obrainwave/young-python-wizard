# Online Quiz Platform

A web application for creating and taking multiple-choice quizzes. Admins can build quizzes with questions and options, while users can take quizzes, get instant scoring with detailed feedback, and view leaderboards. Built with Flask and SQLite, this project follows a clean layered architecture with separated models, services, storage, and web layers.

This project is part of the **Young Python Wizard** Module 9 series.

---

## Features

### For Admins

- ➕ Create, edit, and delete quizzes.
- ❓ Add multiple-choice questions (four options, one correct answer).
- ✏️ Edit and delete individual questions.
- 📊 View all quizzes with their question counts from a single dashboard.

### For Users

- 📝 Browse all available quizzes.
- 🎯 Take quizzes by entering a name and selecting answers.
- ✅ Receive instant scoring with per-question feedback (correct/incorrect and the right answer).
- 🏆 View a leaderboard of top attempts for each quiz.
- 📅 See when each attempt was made.

### Technical

- 💾 Persistent storage using SQLite.
- 🧱 Layered architecture (models, services, storage, web).
- 🎨 Modern Bootstrap 5 UI with custom CSS.
- 🔀 Separate blueprints for public and admin routes.

---

## Project Structure

```
quiz_platform/
├── models/
│   ├── __init__.py
│   ├── quiz.py
│   ├── question.py
│   ├── option.py
│   └── attempt.py
├── services/
│   ├── __init__.py
│   ├── quiz_service.py
│   └── attempt_service.py
├── storage/
│   ├── __init__.py
│   ├── database.py
│   ├── initializer.py
│   ├── quiz_repository.py
│   ├── question_repository.py
│   ├── option_repository.py
│   └── attempt_repository.py
├── webapp/
│   ├── __init__.py
│   ├── routes.py
│   ├── admin_routes.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── quiz_list.html
│   │   ├── take_quiz.html
│   │   ├── quiz_result.html
│   │   ├── leaderboard.html
│   │   ├── admin_dashboard.html
│   │   ├── quiz_form.html
│   │   ├── question_list.html
│   │   └── question_form.html
│   └── static/
│       └── style.css
├── main.py
└── requirements.txt
```

- **`models/`** – Data classes (`Quiz`, `Question`, `Option`, `Attempt`).
- **`services/`** – Business logic and validation (`QuizService`, `AttemptService`).
- **`storage/`** – Database connection, initialization, and repositories.
- **`webapp/`** – Flask app factory, blueprints, templates, and static assets.
- **`main.py`** – Entry point that runs the Flask app.

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Install dependencies:

```bash
pip install -r requirements.txt
```

### Running the Application

```bash
python main.py
```

Open `http://127.0.0.1:5002` in your browser.

The database (`quiz.db`) and its tables are created automatically on the first run.

---

## Usage

### Admin Panel

Navigate to `/admin` to access the dashboard.

1. Click **+ Add Quiz** to create a new quiz (title and optional description).
2. From the dashboard, click **Questions** next to a quiz to manage its questions.
3. Click **+ Add Question** to add a multiple-choice question:
   - Enter the question text.
   - Fill in four options.
   - Select the radio button next to the correct option.
4. Use **Edit** and **Delete** to modify existing content.

### Taking a Quiz

1. Navigate to `/quizzes` to see all available quizzes.
2. Click **Take Quiz** on any quiz with at least one question.
3. Enter your name and answer each question by selecting a radio button.
4. Click **Submit Answers** to see your score and detailed feedback.
5. View the leaderboard for that quiz to see how you compare.

### Leaderboard

- Accessible from the quiz list or the results page.
- Shows the top 10 attempts, sorted by score (highest first), then by submission time (earliest first).

---

## How It Works

### Database Schema

The SQLite database contains five tables with proper foreign-key relationships:

- **quizzes** – quiz metadata.
- **questions** – belongs to a quiz; stores order via `position`.
- **options** – belongs to a question; stores `is_correct` flag.
- **attempts** – one record per quiz submission (user name, score, total, timestamp).
- **attempt_answers** – stores the chosen option for each question in an attempt. This enables detailed post-submission feedback.

### Layered Architecture

- **Repositories** (in `storage/`) handle all SQL. Each method opens its own connection to keep Flask's multi-threaded dev server safe.
- **Services** (in `services/`) contain business logic: validation, scoring, hydration of nested models, and orchestration across repositories.
- **Models** (in `models/`) are simple data containers.
- **Routes** (in `webapp/`) are split into two blueprints: `main` for public pages and `admin` for management.

### Scoring and Feedback

When a user submits a quiz:

1. `AttemptService.submit_attempt` iterates over every question in the quiz.
2. For each question, it validates that the chosen option belongs to that question and checks `is_correct`.
3. Each answer (including unanswered questions) is stored in `attempt_answers`.
4. The attempt's score is the count of correct answers.

The results page uses `get_detailed_results` to display each question, the user's answer, and the correct answer.

---

## Extending the Project

Here are ideas to enhance the platform:

- **Admin authentication** – protect `/admin` with Flask-Login or HTTP basic auth.
- **Timed quizzes** – add a countdown and auto-submit on timeout.
- **Shuffle questions and options** – randomize order per attempt.
- **Question categories** – tag quizzes and filter the list.
- **User accounts** – store attempts per user and show personal history.
- **Export results** – generate a CSV of all attempts for a quiz.
- **Multiple correct answers** – support multi-select questions.
- **REST API** – expose `/api/quizzes` and `/api/attempts` for mobile clients.
- **Unit tests** – cover services and repositories with `pytest`.

---

## License

This project is part of the **Young Python Wizard** learning repository and is free to use for personal and educational purposes.

Happy quizzing! 🧠🐍