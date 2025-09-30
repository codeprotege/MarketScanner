import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
from playwright.sync_api import sync_playwright
import openpyxl
import io
import re

def scrape_ia():
    """
    Scrapes CPD courses from the IA website by downloading and parsing an Excel file.
    """
    url = "https://www.ia.org.hk/en/supervision/reg_ins_intermediaries/files/T1_VC_List_for_Public.xlsx"
    courses = []
    try:
        response = requests.get(url)
        response.raise_for_status()

        workbook = openpyxl.load_workbook(io.BytesIO(response.content))
        sheet = workbook.active

        # Data starts from row 7
        for row in sheet.iter_rows(min_row=7, values_only=True):
            if len(row) > 5 and row[3]:
                provider = row[2]
                course_name = row[3]
                hours = row[5]
                if isinstance(hours, str):
                    hours = hours.replace('\n', ' ').strip()

                details = f"Provider: {provider}, Hours: {hours}"

                courses.append({
                    "course_name": course_name,
                    "related_url": "N/A",
                    "application_link": "N/A",
                    "detail": details
                })
    except requests.exceptions.RequestException as e:
        print(f"Error downloading or processing file from IA: {e}")
    except Exception as e:
        print(f"An error occurred while scraping IA: {e}")

    return courses

def scrape_hkcaavq():
    """
    Scrapes CPD courses from the HKCAAVQ website by downloading and parsing Excel/PDF files.
    """
    url = "https://www.hkcaavq.edu.hk/en/assessment/CPD_IA_prog/"
    courses = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url, timeout=60000)

            # Click the collapsible section to reveal the link
            page.locator('a.row_head:has-text("Information of Approved CPD Activities")').click()

            # Wait for the specific link to appear and get its href
            excel_link_locator = page.locator('a:has-text("EXCEL")[href$=".xls"]')
            excel_link_locator.wait_for(timeout=15000)
            excel_url = excel_link_locator.get_attribute('href')

            if not excel_url.startswith('http'):
                excel_url = f"https://www.hkcaavq.edu.hk{excel_url}"

            browser.close()

            excel_response = requests.get(excel_url)
            excel_response.raise_for_status()

            # Skip the header rows, data starts from row 8 (index 7)
            df = pd.read_excel(io.BytesIO(excel_response.content), engine='xlrd', header=None, skiprows=7)

            for index, row in df.iterrows():
                # Using column 3 (course name) to check for valid rows
                if len(row) >= 6 and pd.notna(row.iloc[3]):
                    provider = row.iloc[2]
                    course_name = row.iloc[3]
                    hours = row.iloc[5]

                    courses.append({
                        "course_name": str(course_name),
                        "related_url": "N/A",
                        "application_link": "N/A",
                        "detail": f"Provider: {provider}, Hours: {hours}"
                    })
    except Exception as e:
        print(f"An error occurred while scraping HKCAAVQ: {e}")

    return courses

def scrape_piba():
    """
    Scrapes CPD courses from the PIBA website.
    """
    url = "https://www.piba.org.hk/cpd-course"
    courses = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url, timeout=60000)
            page.wait_for_selector("div.card")

            script_tag = page.locator('script#__NEXT_DATA__').inner_text()
            json_data = json.loads(script_tag)
            course_list = json_data.get('props', {}).get('pageProps', {}).get('initialProgramList', [])

            for course_data in course_list:
                course_name = course_data.get('title')
                application_link = course_data.get('otherPlatformLink', 'N/A')

                pdf_document = course_data.get('pdfDocument')
                related_url = 'N/A'
                if pdf_document:
                    related_url = f"https://www.piba.org.hk/download/{pdf_document}"

                details = []
                if course_data.get('courseCode'):
                    details.append(f"Memo: {course_data.get('courseCode')}")

                start_date = course_data.get('activityStartDateTime')
                if start_date:
                    details.append(f"Start Date: {start_date.split('T')[0]}")

                end_date = course_data.get('activityEndDateTime')
                if end_date:
                    details.append(f"End Date: {end_date.split('T')[0]}")

                if course_data.get('physicalVenue'):
                    details.append(f"Venue: {course_data.get('physicalVenue')}")

                if course_data.get('facilitator'):
                    details.append(f"Facilitator: {course_data.get('facilitator')}")

                if course_data.get('activityContent'):
                    soup_content = BeautifulSoup(course_data.get('activityContent'), 'html.parser')
                    details.append(f"Content: {soup_content.get_text(separator=' ', strip=True)}")

                courses.append({
                    "course_name": course_name,
                    "related_url": related_url,
                    "application_link": application_link,
                    "detail": ", ".join(details)
                })

            browser.close()

    except Exception as e:
        print(f"An error occurred while scraping PIBA: {e}")

    return courses

def scrape_hkcii():
    """
    Scrapes CPD courses from the HKCII website.
    """
    url = "https://www.hkcii.org/index.php?page=cpd"
    base_url = "https://www.hkcii.org/"
    courses = []
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        links = soup.select("a[href*='continuing-professional-development-cpd']")
        for link in links:
            course_name = link.text.strip()
            course_url = link['href']
            if not course_url.startswith('http'):
                course_url = f"{base_url}{course_url}"

            related_url = course_url
            application_link = course_url
            detail = ""

            try:
                detail_response = requests.get(course_url)
                detail_soup = BeautifulSoup(detail_response.content, 'html.parser')

                main_content = detail_soup.find('div', id='main')
                if main_content:
                    detail = main_content.get_text(separator=' ', strip=True)

                    # Find PDF link
                    embed_tag = main_content.find('embed')
                    if embed_tag and embed_tag.get('src'):
                        related_url = embed_tag.get('src')
                        if not related_url.startswith('http'):
                            related_url = f"{base_url}{related_url}"

                    # Find Google Form link
                    gform_link = main_content.find('a', href=re.compile(r'docs\.google\.com/forms'))
                    if gform_link:
                        application_link = gform_link['href']

            except requests.exceptions.RequestException as e:
                print(f"Could not fetch details for {course_url}: {e}")

            courses.append({
                "course_name": course_name,
                "related_url": related_url,
                "application_link": application_link,
                "detail": detail
            })

    except requests.exceptions.RequestException as e:
        print(f"Error downloading or processing file from HKCII: {e}")
    except Exception as e:
        print(f"An error occurred while scraping HKCII: {e}")

    return courses

def scrape_peak():
    """
    Scrapes CPD courses from the PEAK website using Playwright.
    """
    url = "https://www.peak.edu.hk/exam/ia-cpd"
    courses = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url, timeout=120000) # Increased timeout
            page.wait_for_selector("div.course-item", timeout=30000)
            content = page.content()
            browser.close()

        soup = BeautifulSoup(content, "html.parser")

        course_items = soup.select("div.course-item")

        for item in course_items:
            title_tag = item.find("h3")
            if title_tag:
                course_name = title_tag.text.strip()

                link_tag = item.find("a", text=re.compile("Details", re.IGNORECASE))
                related_url = "N/A"
                if link_tag and link_tag.has_attr('href'):
                    related_url = link_tag['href']
                    if not related_url.startswith('http'):
                        related_url = f"https://www.peak.edu.hk{related_url}"

                application_link = related_url # Assume the detail page has application info

                details = item.find("div", class_="course-info").get_text(separator=' ', strip=True)

                courses.append({
                    "course_name": course_name,
                    "related_url": related_url,
                    "application_link": application_link,
                    "detail": details
                })
    except Exception as e:
        print(f"An error occurred while scraping PEAK, site may be unresponsive: {e}")

    return courses

def scrape_cpduk():
    """
    Scrapes CPD courses from the cpduk.co.uk website using Playwright.
    """
    url = "https://cpduk.co.uk/providers/ehp-hong-kong-ltd"
    courses = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url, timeout=60000)
            page.wait_for_selector("div.course-teaser")
            content = page.content()
            browser.close()

        soup = BeautifulSoup(content, "html.parser")

        course_cards = soup.select("div.course-teaser")

        for card in course_cards:
            title_tag = card.find("h3", class_="title")
            if title_tag:
                course_name = title_tag.text.strip()
                course_link = card.find("a")
                course_url = "N/A"
                if course_link:
                    course_url = course_link['href']
                    if not course_url.startswith('http'):
                        course_url = f"https://cpduk.co.uk{course_url}"

                details = card.find("div", class_="leading-snug")
                detail_text = details.text.strip() if details else "N/A"

                courses.append({
                    "course_name": course_name,
                    "related_url": course_url,
                    "application_link": course_url,
                    "detail": detail_text
                })

    except Exception as e:
        print(f"An error occurred while scraping cpduk.co.uk: {e}")

    return courses