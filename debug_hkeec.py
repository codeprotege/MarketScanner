import requests
from playwright.sync_api import sync_playwright

def scrape_hkeec_debug():
    """
    Scrapes CPD courses from the HKEEC website using Playwright.
    """
    url = "https://www.hkeec.com/cpd-courses-insurance"
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url, timeout=60000)
            page.wait_for_load_state('networkidle', timeout=30000)
            content = page.content()
            with open('hkeec.html', 'w', encoding='utf-8') as f:
                f.write(content)
            browser.close()
            print("Successfully saved hkeec.html")

    except Exception as e:
        print(f"An error occurred while scraping HKEEC: {e}")

if __name__ == "__main__":
    scrape_hkeec_debug()