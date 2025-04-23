# Testopia

> **Web & Telegram Quiz Generator**

Testopia is a Django‑powered application that lets educators create and administer quizzes by simply uploading an Excel file of questions. Students can then take these quizzes either via a web interface or interactively through a Telegram bot.

---

## 🚀 Highlights

- **Excel‑based Quiz Creation**: Upload `.xlsx` files containing questions, options, correct answers, and point values; Testopia parses and stores them automatically.
- **Django Backend**: Robust data models for Tests, Questions, Choices, User Answers, and User Test sessions.
- **Web Interface**: Simple upload form (`/upload/`) to create quizzes, plus web view to render and submit tests (prototype stage).
- **Telegram Bot**: Interactive quiz delivery via inline buttons using **pyTelegramBotAPI**. Commands:
  - `/start` — Register and welcome message
  - `/tests` — List available quizzes
  - Inline buttons to answer, skip, or finish a quiz
- **Automated Test Generation**: `utils/TestGenerator` reads your Excel sheet, randomizes questions/variants, dumps JSON for both web and bot consumption.
- **Persistence & Analytics**: Tracks user answers, computes scores, and logs results in `UserTest` records.

---

## 📂 Project Structure

```
├── TGBOT/             # Telegram bot handlers and Test session classes
├── data/              # Django app: models, forms, views, tests for web quiz interface
├── core/              # Django core: settings, URLs, user model extensions
├── utils/             # TestGenerator: parses Excel & builds quiz JSON
├── templates/         # HTML templates: upload form, success page, quiz view
├── static/            # CSS/JS assets for web interface
├── .github/workflows/ # CI pipeline for linting & testing
├── manage.py          # Django CLI
├── requirements.txt   # Python dependencies
└── README.md          # This documentation
```

---

## 🔧 Installation & Quickstart

1. **Clone the repo**
   ```bash
   git clone https://github.com/habiboffdev/testopia.git
   cd testopia
   ```
2. **Create & activate an environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate    # Windows: `venv\\Scripts\\activate`
   pip install -r requirements.txt
   ```
3. **Configure environment variables**
   - Copy `.env.example` to `.env` and set:
     ```ini
     SECRET_KEY=your_django_secret_key
     TELEGRAM_BOT_TOKEN=your_telegram_token
     DEBUG=True
     ALLOWED_HOSTS=localhost,127.0.0.1
     DATABASE_URL=sqlite:///db.sqlite3
     ```
4. **Apply migrations**
   ```bash
   python manage.py migrate
   ```
5. **Run Django server**
   ```bash
   python manage.py runserver
   ```
6. **Start the Telegram Bot** (in a separate terminal)
   ```bash
   python TGBOT/main.py
   ```

---

## 🛠 Usage

1. **Create a Quiz**:
   - Visit `http://localhost:8000/upload/`
   - Fill in title, description, number of variants, and upload your Excel file (columns: `question`, `A`, `B`, `C`, `D`, `point`).
2. **View Quiz Data**:
   - After upload, view parsed data on the success page.
3. **Take Quiz via Web** (Prototype):
   - Browse to `/solve/<test_id>/` to see questions rendered and submit answers.
4. **Take Quiz via Telegram**:
   - Message your bot on Telegram:
     - `/start` to register
     - `/tests` to list quizzes
     - Tap inline buttons to select answers, skip, or finish. Score is sent at end.

---

## 📚 Data Models

| Model         | Purpose                                             |
|---------------|-----------------------------------------------------|
| **TestModel** | Metadata for each quiz (title, description, variants) |
| **Question**  | Each question text, point value, order, multiple-choice flag |
| **Choice**    | Options for questions; flags correct answers         |
| **UserAnswer**| Tracks raw answer selections per user & quiz         |
| **UserTest**  | Summarizes a user’s quiz session: correct, incorrect, total points |

---

## 📈 Next Steps & Maintenance

- **Web UI Completion**: Finish the `/solve/` and `/submit/` endpoints and add styled templates.
- **Error Handling**: Improve exception logging and user feedback on upload/view pages.
- **CI Pipeline**: Expand GitHub Actions to run `pytest`, `flake8`, and code coverage checks.
- **Deployment**: Containerize with Docker and deploy on Heroku or DigitalOcean.

---

## 📜 License

MIT License. See [LICENSE](LICENSE) for details.

_Last updated: April 23, 2025_

