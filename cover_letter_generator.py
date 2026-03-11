#!/usr/bin/env python3
"""
Cover Letter Generator
Fetches vacancy info from HeadHunter and generates a cover letter using Google Gemini.

Requirements:
    pip install google-genai requests

Usage:
    1. Edit config.py with your API key and personal info
    2. Run:  python cover_letter_generator.py
"""

import re
import sys
import requests
import webbrowser
import pyperclip # type: ignore
from google import genai

try:
    import config
except ModuleNotFoundError:
    print("❌  config.py not found. Make sure it's in the same folder as this script.")
    sys.exit(1)

HH_API_BASE = "https://api.hh.ru"


def extract_vacancy_id(url_or_id: str) -> str:
    match = re.search(r"/vacancy/(\d+)", url_or_id)
    if match:
        return match.group(1)
    if url_or_id.strip().isdigit():
        return url_or_id.strip()
    raise ValueError(f"Cannot extract vacancy ID from: {url_or_id!r}")


def fetch_vacancy(vacancy_id: str) -> dict:
    url     = f"{HH_API_BASE}/vacancies/{vacancy_id}"
    headers = {"User-Agent": "CoverLetterBot/1.0 (personal use)"}
    resp    = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()
    return resp.json()


def parse_vacancy(data: dict) -> dict:
    def strip_html(text: str) -> str:
        return re.sub(r"<[^>]+>", " ", text or "").strip()

    salary  = data.get("salary")
    sal_str = ""
    if salary:
        lo, hi, cur = salary.get("from"), salary.get("to"), salary.get("currency", "")
        parts = []
        if lo: parts.append(f"from {lo:,}")
        if hi: parts.append(f"to {hi:,}")
        sal_str = " ".join(parts) + f" {cur}"

    return {
        "employer":    data.get("employer", {}).get("name", "N/A"),
        "title":       data.get("name", "N/A"),
        "area":        data.get("area", {}).get("name", ""),
        "salary":      sal_str,
        "experience":  data.get("experience", {}).get("name", ""),
        "employment":  data.get("employment", {}).get("name", ""),
        "schedule":    data.get("schedule", {}).get("name", ""),
        "key_skills":  ", ".join(s["name"] for s in data.get("key_skills", [])),
        "description": strip_html(data.get("description", ""))[:4000],
    }


def build_prompt(vacancy: dict) -> str:
    return f"""
You are an expert career coach and professional writer.

Write a compelling, personalized cover letter in {config.LETTER_LANGUAGE} for the following job vacancy.
Tone: {config.LETTER_TONE}. Target length: {config.LETTER_LENGTH}.

## Vacancy Details
- **Company:**    {vacancy['employer']}
- **Position:**   {vacancy['title']}
- **Location:**   {vacancy['area']}
- **Salary:**     {vacancy['salary'] or 'Not specified'}
- **Experience:** {vacancy['experience']}
- **Employment:** {vacancy['employment']}
- **Schedule:**   {vacancy['schedule']}
- **Key Skills:** {vacancy['key_skills']}

### Job Description (excerpt)
{vacancy['description']}

## Applicant Profile
- **Name:**        {config.YOUR_NAME}
- **Target role:** {config.YOUR_POSITION}
- **Key skills:**  {config.YOUR_SKILLS}
- **Additional:**  {config.EXTRA_INFO or 'N/A'}

## Instructions
1. Start with a strong opening that mentions the exact company and position.
2. Connect the applicant's skills directly to the vacancy requirements.
3. Highlight 2-3 specific strengths with measurable impact where possible.
4. Show genuine enthusiasm for the company and role.
5. End with a clear call-to-action.
6. Do NOT use generic openers like "I am writing to express my interest…".

Return ONLY the cover letter text — no preamble or explanation.
""".strip()


def generate_cover_letter(prompt: str) -> str:
    client   = genai.Client(api_key=config.GEMINI_API_KEY)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text.strip()


def save_letter(letter: str, vacancy: dict) -> str:
    safe_company = re.sub(r"[^\w\-]", "_", vacancy["employer"])[:30]
    safe_title   = re.sub(r"[^\w\-]", "_", vacancy["title"])[:30]
    filename     = f"cover_letter_{safe_company}_{safe_title}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("Cover Letter\n")
        f.write(f"Company:  {vacancy['employer']}\n")
        f.write(f"Position: {vacancy['title']}\n")
        f.write("=" * 60 + "\n\n")
        f.write(letter)
    return filename


def main():
    print("=" * 60)
    print("  Cover Letter Generator  |  HeadHunter + Gemini")
    print("=" * 60)

    if config.GEMINI_API_KEY == "YOUR_GEMINI_API_KEY":
        print("\n⚠  Open config.py and set your GEMINI_API_KEY first.\n")
        sys.exit(1)

    raw = input("\nPaste HeadHunter vacancy URL or ID: ").strip()
    if not raw:
        print("No input provided. Exiting.")
        sys.exit(1)

    try:
        vacancy_id = extract_vacancy_id(raw)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"\n🔍  Fetching vacancy #{vacancy_id} from HeadHunter…")
    try:
        data    = fetch_vacancy(vacancy_id)
        vacancy = parse_vacancy(data)
    except requests.HTTPError as e:
        print(f"HTTP error: {e}")
        sys.exit(1)

    print(f"✅  Found: {vacancy['title']} at {vacancy['employer']}")
    if vacancy["key_skills"]:
        print(f"    Skills: {vacancy['key_skills']}")

    print("\n✍️   Generating cover letter with Gemini…")
    try:
        letter = generate_cover_letter(build_prompt(vacancy))
    except Exception as e:
        print(f"Gemini error: {e}")
        sys.exit(1)

    print("\n" + "=" * 60)
    print(letter)
    print("=" * 60)

    pyperclip.copy(letter)
    print("📋  Cover letter copied to clipboard!")

    ##filename = save_letter(letter, vacancy)
    ##print(f"\n💾  Saved to: {filename}")

    vacancy_url = f"https://hh.ru/vacancy/{vacancy_id}"
    #open_link = input("\n🌐  Open vacancy in browser? (y/n): ").strip().lower()
    #if open_link == "y":
    webbrowser.open(vacancy_url)
    print(f"✅  Opened: {vacancy_url}")


if __name__ == "__main__":
    main()
