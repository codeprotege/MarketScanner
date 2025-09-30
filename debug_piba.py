import requests
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def scrape_piba_debug():
    """
    Scrapes CPD courses from the PIBA website for debugging purposes.
    """
    url = "https://www.piba.org.hk/cpd-course"
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url, timeout=60000)
            page.wait_for_selector("div.card-body")
            content = page.content()
            with open('piba.html', 'w', encoding='utf-8') as f:
                f.write(content)
            browser.close()
            print("Successfully saved piba.html")

    except Exception as e:
        print(f"An error occurred while scraping PIBA: {e}")

if __name__ == "__main__":
    scrape_piba_debug()