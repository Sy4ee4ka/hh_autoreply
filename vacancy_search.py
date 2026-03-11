#!/usr/bin/env python3
"""
HeadHunter Vacancy Search
Searches vacancies with filters and prints results with IDs
ready to paste into cover_letter_generator.py

Requirements:
    pip install requests

Usage:
    1. Set filters below or in the prompt
    2. Run:  python vacancy_search.py
"""

import sys
import requests

# ══════════════════════════════════════════════════════════════
#  FILTERS  —  edit before running
# ══════════════════════════════════════════════════════════════

TEXT       = "system analyst"   # search query
AREA       = 1                  # 1=Moscow, 2=St.Petersburg, 99=Riga, 88=Minsk
SALARY     = None               # e.g. 100000 — or None to skip
CURRENCY   = "RUR"              # RUR, EUR, USD
EXPERIENCE = "noExperience"     # None | "noExperience" | "between1And3" | "between3And6" | "moreThan6"
EMPLOYMENT = None               # None | "full" | "part" | "project" | "volunteer"
SCHEDULE   = None               # None | "remote" | "fullDay" | "flexible" | "shift"
PER_PAGE   = 20                 # results to fetch (max 100)

# ══════════════════════════════════════════════════════════════

HH_API = "https://api.hh.ru"
AREAS  = {
    1: "Moscow", 2: "St. Petersburg", 99: "Riga", 88: "Minsk",
    113: "Russia", 16: "Novosibirsk", 54: "Yekaterinburg",
}


def search_vacancies(params: dict) -> list:
    headers = {"User-Agent": "VacancySearch/1.0 (personal use)"}
    resp    = requests.get(f"{HH_API}/vacancies", params=params, headers=headers, timeout=15)
    resp.raise_for_status()
    return resp.json()


def format_salary(salary: dict | None) -> str:
    if not salary:
        return "salary not specified"
    lo, hi, cur = salary.get("from"), salary.get("to"), salary.get("currency", "")
    parts = []
    if lo: parts.append(f"from {lo:,}")
    if hi: parts.append(f"to {hi:,}")
    return " ".join(parts) + f" {cur}" if parts else "salary not specified"


def main():
    print("=" * 60)
    print("  HeadHunter Vacancy Search")
    print("=" * 60)

    params = {
        "text":     TEXT,
        "area":     AREA,
        "per_page": PER_PAGE,
        "page":     0,
    }
    if SALARY:
        params["salary"]   = SALARY
        params["currency"] = CURRENCY
        params["only_with_salary"] = "true"
    if EXPERIENCE:
        params["experience"] = EXPERIENCE
    if EMPLOYMENT:
        params["employment"] = EMPLOYMENT
    if SCHEDULE:
        params["schedule"] = SCHEDULE

    area_name = AREAS.get(AREA, f"area {AREA}")
    print(f"\n🔍  Searching: \"{TEXT}\" in {area_name}")
    if SALARY:
        print(f"    Salary: from {SALARY:,} {CURRENCY}")
    if EXPERIENCE:
        print(f"    Experience: {EXPERIENCE}")
    if SCHEDULE:
        print(f"    Schedule: {SCHEDULE}")

    try:
        data = search_vacancies(params)
    except requests.HTTPError as e:
        print(f"HTTP error: {e}")
        sys.exit(1)

    items = data.get("items", [])
    total = data.get("found", 0)

    print(f"\n📋  Found {total} vacancies total, showing {len(items)}:\n")
    print("─" * 60)

    ids = []
    for i, v in enumerate(items, 1):
        vid        = v["id"]
        title      = v["name"]
        company    = v.get("employer", {}).get("name", "N/A")
        area       = v.get("area", {}).get("name", "")
        salary_str = format_salary(v.get("salary"))
        url        = v.get("alternate_url", "")
        ids.append(vid)

        print(f"  [{i:02d}]  {title}")
        print(f"        🏢  {company}  |  📍 {area}")
        print(f"        💰  {salary_str}")
        print(f"        🔗  {url}")
        print(f"        ID: {vid}")
        print()

    print("─" * 60)
    print("\n📌  All IDs (copy-paste into cover_letter_generator.py):")
    print("\n".join(ids))
    print()


if __name__ == "__main__":
    main()
