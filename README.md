# 📝 Cover Letter Generator — HeadHunter + Gemini AI

Automatically generates personalized cover letters from HeadHunter vacancies using Google Gemini AI. Paste a vacancy URL or ID, get a ready-to-send cover letter copied to your clipboard in seconds.

---

## ✨ Features

- 🔍 Fetches vacancy details directly from the HeadHunter API
- 🤖 Generates a tailored cover letter via Google Gemini 2.5 Flash
- 📋 Copies the result to clipboard automatically
- 🌐 Opens the vacancy in your browser after generation
- 🔎 Includes a vacancy search script with filters (city, salary, experience, schedule)
- 🌍 Supports any language for the generated letter (Russian, English, etc.)

---

## 📁 Project Structure

```
├── cover_letter_generator.py   # Main script — fetch vacancy + generate letter
├── vacancy_search.py           # Search vacancies on HH with filters
├── config.py                   # Your personal info and API key
└── requirements.txt            # Python dependencies
```

---

## ⚙️ Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-username/cover-letter-generator.git
cd cover-letter-generator
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Get a Gemini API key

Go to [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey) and create a free key.

### 5. Configure `config.py`

```python
GEMINI_API_KEY  = "your_key_here"

YOUR_NAME       = "Your Full Name"
YOUR_POSITION   = "Target Job Title"
YOUR_SKILLS     = "Python, SQL, REST API, ..."
EXTRA_INFO      = "MSc Computer Science, certified in ..."

LETTER_LANGUAGE = "English"   # or "Russian", etc.
LETTER_TONE     = "professional"
LETTER_LENGTH   = "100-150 words"
```

---

## 🚀 Usage

### Generate a cover letter

```bash
python cover_letter_generator.py
```

Paste a HeadHunter vacancy URL or ID when prompted:

```
Paste HeadHunter vacancy URL or ID: https://hh.ru/vacancy/123456789
```

The generated letter is printed, copied to your clipboard, and the vacancy is opened in your browser.

### Search for vacancies

Edit the filters at the top of `vacancy_search.py`:

```python
TEXT       = "system analyst"
AREA       = 1          # 1=Moscow, 2=St.Petersburg, 99=Riga
SALARY     = 100000
EXPERIENCE = "between1And3"
SCHEDULE   = "remote"
```

Then run:

```bash
python vacancy_search.py
```

Copy any vacancy ID from the output and use it in the generator.

---

## 📦 Requirements

```
google-genai
requests
pyperclip
```

---

## 🔑 Environment Variables (optional)

Instead of hardcoding your API key in `config.py`, you can use an environment variable:

```bash
export GEMINI_API_KEY="your_key_here"
```

And update `config.py`:

```python
import os
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")
```

---

## ⚠️ Notes

- HeadHunter API is public and does not require authentication for vacancy lookups
- `pyperclip` requires a clipboard backend on Linux (e.g. `xclip` or `xsel`)
- This tool is intended for personal use only

---

## 📄 License

MIT
