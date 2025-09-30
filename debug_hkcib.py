import requests
from playwright.sync_api import sync_playwright

def scrape_hkcib_debug():
    """
    Scrapes CPD courses from the HKCIB website using Playwright for analysis.
    """
    url = "https://www.hkcib.org.hk/cpd-courses"
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url, timeout=60000)
            page.wait_for_load_state('networkidle', timeout=30000)
            content = page.content()
            with open('hkcib.html', 'w', encoding='utf-8') as f:
                f.write(content)
            browser.close()
            print("Successfully saved hkcib.html")

    except Exception as e:
        print(f"An error occurred while scraping hkcib.org.hk: {e}")

if __name__ == "__main__":
    scrape_hkcib_debug()