import requests
from playwright.sync_api import sync_playwright

def scrape_cpduk_debug():
    """
    Scrapes CPD courses from the cpduk.co.uk website using Playwright for analysis.
    """
    url = "https://cpduk.co.uk/providers/ehp-hong-kong-ltd"
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url, timeout=60000)
            page.wait_for_load_state('networkidle', timeout=30000)
            content = page.content()
            with open('cpduk.html', 'w', encoding='utf-8') as f:
                f.write(content)
            browser.close()
            print("Successfully saved cpduk.html")

    except Exception as e:
        print(f"An error occurred while scraping cpduk.co.uk: {e}")

if __name__ == "__main__":
    scrape_cpduk_debug()