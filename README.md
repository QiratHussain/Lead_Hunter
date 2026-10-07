# LeadHunter

LeadHunter is a beginner-friendly Python/Flask portfolio project that searches for public business websites and extracts publicly visible contact information.

## What it demonstrates

- Python
- Flask
- HTML
- CSS
- Bootstrap
- Requests
- BeautifulSoup
- Regular expressions
- SQLite
- CSV export
- Basic web scraping
- Git/GitHub-ready project structure

## Project structure

```text
lead_hunter/
│
├── app.py
├── scraper.py
├── database.py
├── requirements.txt
├── README.md
│
├── templates/
│   ├── base.html
│   └── index.html
│
└── static/
    └── style.css
```

## How to run

Create a virtual environment if you want one:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install packages:

```bash
pip install -r requirements.txt
```

Run:

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Example search

Try:

```text
Business type: dental clinic
Location: Lahore
```

The app searches DuckDuckGo's HTML results, visits the resulting public websites, and tries to find:

- Business name
- Website
- Email
- Phone number

The results are stored in SQLite and can be exported as CSV.

## Important

This is a portfolio/learning project. Websites can block automated requests, change their HTML structure, or prohibit scraping in their terms. Use public information responsibly, respect robots.txt and website terms, keep request rates low, and do not collect private information.

## Future upgrades

Good next versions could add:

1. Search history
2. Lead scoring
3. Better phone-number detection
4. Pagination
5. Loading/progress indicator
6. Database filters
7. Delete leads
8. Google Sheets export
9. Scheduled searches
10. Login/authentication
11. Deployment
12. A client-facing API
