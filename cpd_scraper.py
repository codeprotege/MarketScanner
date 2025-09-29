import requests
from bs4 import BeautifulSoup
import pandas as pd
from playwright.sync_api import sync_playwright

def scrape_pcpd():
    """
    Scrapes CPD courses from the PCPD website.
    """
    url = "https://www.pcpd.org.hk/english/education_training/organisations/workshops/workshop.php"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    courses = []

    # Find the table containing the courses
    table = soup.find("table")
    if not table:
        return courses

    # Iterate over the rows of the table
    for row in table.find_all("tr")[1:]:  # Skip the header row
        cols = row.find_all("td")
        if len(cols) >= 5:
            date = cols[1].text.strip()
            course_name = cols[3].text.strip()

            # The URL is in the <a> tag within the course name cell
            course_link = cols[3].find("a")
            if course_link:
                course_url = f"https://www.pcpd.org.hk{course_link['href']}"
            else:
                course_url = url  # Fallback to the main page

            courses.append({
                "course_name": course_name,
                "related_url": course_url,
                "application_link": url,  # The main page is the application form
                "detail": f"Date: {date}"
            })

    return courses

def scrape_hkiod():
    """
    Scrapes CPD courses from the HKIoD website using Playwright to handle dynamic content.
    """
    url = "https://www.hkiod.com/open-classes/"
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        content = page.content()
        browser.close()

    soup = BeautifulSoup(content, "html.parser")
    courses = []

    tables = soup.find_all("table")
    target_table = None
    for table in tables:
        if "Subject and Speaker" in str(table):
            target_table = table
            break

    if not target_table:
        return courses

    for row in target_table.find_all("tr")[1:]:  # Skip header
        cols = row.find_all("td")
        if len(cols) >= 3:
            # The course name and link are in the second column
            course_cell = cols[1]
            course_link = course_cell.find("a")
            if course_link:
                course_name = course_link.text.strip()
                course_url = course_link['href']
            else:
                course_name = course_cell.text.strip()
                course_url = url  # Fallback to the main page

            # The application link is on the page
            application_link = "https://hkiod.wufoo.com/forms/training-programmes-registration-form/"

            courses.append({
                "course_name": course_name,
                "related_url": course_url,
                "application_link": application_link,
                "detail": f"Date: {cols[0].text.strip()}"
            })

    return courses

def scrape_compliance_plus():
    """
    Scrapes CPD courses from the CompliancePlus (Thinkific) website.
    """
    url = "https://complianceplus.thinkific.com/"
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_load_state('networkidle', timeout=30000)
        content = page.content()
        browser.close()

    soup = BeautifulSoup(content, "html.parser")
    courses = []

    # Find all course cards
    course_cards = soup.find_all("li", class_="products__list-item")

    for card in course_cards:
        course_link = card.find("a", class_="course-card")
        if course_link:
            course_name = course_link.find("h3").text.strip()
            course_url = f"{url.rstrip('/')}{course_link['href']}"
            price_span = card.find("span", class_="course-card__price")
            price = price_span.text.strip() if price_span else "N/A"

            courses.append({
                "course_name": course_name,
                "related_url": course_url,
                "application_link": course_url,
                "detail": f"Price: {price}"
            })

    return courses

def main():
    """
    Main function to scrape all CPD course websites.
    """
    all_courses = []
    all_courses.extend(scrape_pcpd())
    all_courses.extend(scrape_hkiod())
    all_courses.extend(scrape_compliance_plus())

    df = pd.DataFrame(all_courses)
    df.to_csv("cpd_courses.csv", index=False)
    print("Scraped data saved to cpd_courses.csv")

if __name__ == "__main__":
    main()