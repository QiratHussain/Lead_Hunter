import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urljoin, urlparse


HEADERS = {
    "User-Agent": "LeadHunter/1.0 (portfolio project)"
}

TIMEOUT = 8


def search_web(keyword, location):
    """
    Search DuckDuckGo's HTML results page and return website URLs.
    """

    query = f"{keyword} {location}"

    url = (
        "https://html.duckduckgo.com/html/?q="
        + quote(query)
    )

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=TIMEOUT,
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    websites = []

    for result in soup.select(".result"):
        link = result.select_one(".result__a")

        if not link:
            continue

        website = link.get("href")

        if website:
            websites.append(website)

    return websites[:10]


def get_page(url):
    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=TIMEOUT,
        )

        response.raise_for_status()

        return response.text

    except requests.RequestException:
        return ""


def extract_email(text):
    emails = re.findall(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text,
    )

    # Remove common fake/example emails.
    for email in emails:
        if "example.com" not in email.lower():
            return email

    return ""


def extract_phone(text):
    # This intentionally uses a simple pattern.
    # Phone formats vary greatly between countries.
    matches = re.findall(
        r"(?:\+92|0092|0)\s?\d{3}[\s-]?\d{3}[\s-]?\d{4}",
        text,
    )

    if matches:
        return matches[0]

    return ""


def get_business_name(soup, url):
    title = soup.title

    if title and title.string:
        return title.string.strip()

    hostname = urlparse(url).netloc
    return hostname.replace("www.", "")


def find_contact_page(soup, base_url):
    """
    Look for a normal contact/about page.
    """
    for link in soup.find_all("a", href=True):
        text = link.get_text(" ", strip=True).lower()
        href = link["href"].lower()

        if (
            "contact" in text
            or "contact" in href
            or "about" in text
            or "about" in href
        ):
            return urljoin(base_url, link["href"])

    return ""


def scrape_website(url):
    html = get_page(url)

    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")

    page_text = soup.get_text(" ", strip=True)

    name = get_business_name(soup, url)
    email = extract_email(page_text)
    phone = extract_phone(page_text)

    # If the homepage has no contact information,
    # try one contact/about page.
    if not email or not phone:
        contact_url = find_contact_page(soup, url)

        if contact_url and contact_url != url:
            contact_html = get_page(contact_url)

            if contact_html:
                contact_soup = BeautifulSoup(
                    contact_html,
                    "html.parser"
                )

                contact_text = contact_soup.get_text(
                    " ",
                    strip=True
                )

                if not email:
                    email = extract_email(contact_text)

                if not phone:
                    phone = extract_phone(contact_text)

    return {
        "name": name,
        "website": url,
        "email": email,
        "phone": phone,
        "source": "DuckDuckGo search",
    }


def find_leads(keyword, location):
    websites = search_web(keyword, location)

    leads = []

    for website in websites:
        # Ignore obvious social/search websites.
        domain = urlparse(website).netloc.lower()

        blocked_domains = [
            "duckduckgo.com",
            "google.com",
            "facebook.com",
            "instagram.com",
            "youtube.com",
            "linkedin.com",
        ]

        if any(blocked in domain for blocked in blocked_domains):
            continue

        lead = scrape_website(website)

        if lead:
            leads.append(lead)

    return leads

