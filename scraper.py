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
