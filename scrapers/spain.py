"""
Web scraper for Spain universities.
"""

import re
import unicodedata
from typing import Dict, List
from urllib.parse import urlparse

import requests
import xlrd
from bs4 import BeautifulSoup

SOURCE_URL = (
    "https://www.educacion.gob.es/ruct/listauniversidades.action?actual=universidades"
)

BASE_URL = "https://www.educacion.gob.es"
SEARCH_URL = (
    "https://www.educacion.gob.es/ruct/consultauniversidades?actual=universidades"
)


def _normalize_url(raw: str) -> str:
    url = (raw or "").strip()
    if not url:
        return ""

    if not url.lower().startswith(("http://", "https://")):
        url = "http://" + url

    parsed = urlparse(url)
    if not parsed.netloc:
        return ""

    host = parsed.netloc
    if "." not in host:
        return ""

    # Drop obvious garbage like purely numeric values.
    if not re.search(r"[a-zA-Z]", host):
        return ""

    return url


def _find_excel_export_url(session: requests.Session) -> str:
    headers = {"User-Agent": "Mozilla/5.0", "Referer": SEARCH_URL}
    html = session.get(SEARCH_URL, headers=headers, timeout=45).text
    soup = BeautifulSoup(html, "html.parser")
    form = soup.find("form")
    if not form or not form.get("action"):
        return ""

    post_url = BASE_URL + form.get("action")
    data = {"consulta": "1", "cccaa": "", "codigoUniversidad": "", "tipo_univ": ""}
    results_html = session.post(post_url, data=data, headers=headers, timeout=45).text
    soup2 = BeautifulSoup(results_html, "html.parser")

    href = ""
    for link in soup2.find_all("a", href=True):
        span = link.find("span", class_=re.compile(r"\bexcel\b", re.I))
        if span is not None:
            href = link["href"]
            break

    if not href:
        return ""

    if href.startswith("http://") or href.startswith("https://"):
        return href

    # The export link is usually like: listauniversidades?... (relative to /ruct/)
    if href.startswith("listauniversidades"):
        return BASE_URL + "/ruct/" + href

    if href.startswith("/"):
        return BASE_URL + href

    return BASE_URL + "/ruct/" + href


def _norm_text(value: str) -> str:
    text = (value or "").strip().casefold()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = " ".join(text.split())
    return text


def _parse_xls(content: bytes) -> List[Dict[str, str]]:
    wb = xlrd.open_workbook(file_contents=content)
    sh = wb.sheet_by_index(0)

    if sh.nrows <= 1:
        return []

    headers_row = [str(sh.cell_value(0, c)).strip() for c in range(sh.ncols)]
    try:
        name_col = headers_row.index("Universidad")
        url_col = headers_row.index("URL")
        acronym_col = headers_row.index("Acrónimo")
        modality_col = headers_row.index("Modalidad")
        profit_col = headers_row.index("Con ánimo de lucro")
    except ValueError:
        return []

    universities: List[Dict[str, str]] = []
    seen = set()

    for r in range(1, sh.nrows):
        name = str(sh.cell_value(r, name_col)).strip()
        website = _normalize_url(str(sh.cell_value(r, url_col)).strip())
        acronym = str(sh.cell_value(r, acronym_col)).strip()
        modality = _norm_text(str(sh.cell_value(r, modality_col)))
        profit = _norm_text(str(sh.cell_value(r, profit_col)))

        # Filters requested by user:
        # 1) Acrónimo blank => drop
        if not acronym:
            continue
        # 2) Modalidad == No Presencial => drop
        if modality == _norm_text("No Presencial"):
            continue
        # 3) Con ánimo de lucro == Si => drop
        if profit == "si":
            continue

        if not name:
            continue

        key = (name.casefold(), website.casefold() if website else "")
        if key in seen:
            continue
        seen.add(key)

        universities.append({"name": name, "website": website})

    return universities


def scrape_universities() -> List[Dict[str, str]]:
    session = requests.Session()
    excel_url = _find_excel_export_url(session)
    if not excel_url:
        return []

    headers = {"User-Agent": "Mozilla/5.0", "Referer": SEARCH_URL}
    try:
        resp = session.get(excel_url, headers=headers, timeout=60)
    except requests.RequestException:
        return []

    if resp.status_code >= 400 or not resp.content:
        return []

    # Basic signature check for legacy XLS OLE container.
    if not resp.content.startswith(bytes.fromhex("D0CF11E0A1B11AE1")):
        return []

    return _parse_xls(resp.content)
