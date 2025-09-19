import re
import subprocess
import os
import time

def find_investor_relations_url(company_name, company_symbol):
    """
    Finds the investor relations URL for a given company.
    """
    query = f'"{company_name}" "{company_symbol}" investor relations'
    print(f"Searching for IR URL: {query}")
    try:
        search_results = google_search(query)
        if search_results:
            # Look for a URL that contains "investor" or "ir"
            for result in search_results:
                if "investor" in result['url'] or "ir" in result['url']:
                    return result['url']
            # If no specific IR link is found, return the first result
            return search_results[0]['url']
    except Exception as e:
        print(f"An error occurred during IR URL search: {e}")
    return None

def find_annual_report_link(ir_url):
    """
    Scrapes an investor relations page to find a link to the annual report.
    """
    print(f"Scraping for annual report link on: {ir_url}")
    try:
        # Use curl to get the page content
        html_content = subprocess.check_output(["curl", "-A", "Lynx", "-L", "-s", ir_url]).decode('utf-8')

        # Look for links containing "annual report" or "10-K"
        # This is a simple heuristic and may need to be improved
        for line in html_content.splitlines():
            if "annual report" in line.lower() or "10-k" in line.lower():
                match = re.search(r'href\s*=\s*["\'](.*?)["\']', line)
                if match:
                    link = match.group(1)
                    if link.endswith('.pdf'):
                        # Make the link absolute if it's relative
                        if not link.startswith('http'):
                            from urllib.parse import urljoin
                            link = urljoin(ir_url, link)
                        return link
    except Exception as e:
        print(f"An error occurred while scraping for annual report link: {e}")
    return None

def download_report(url, company_symbol, output_dir):
    """
    Downloads a report from a given URL to a specified directory.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    year_match = re.search(r'(20\d{2})', url)
    year = year_match.group(1) if year_match else "latest"

    filename = f"{company_symbol}_{year}_annual_report.pdf"
    filepath = os.path.join(output_dir, filename)

    print(f"Downloading report from {url} to {filepath}")
    try:
        subprocess.run(["curl", "-L", "-s", "-o", filepath, url], check=True)
        print(f"Download complete: {filepath}")
        return filepath
    except Exception as e:
        print(f"Error downloading report for {company_symbol}: {e}")
    return None

def process_company(company_name, company_symbol, output_dir):
    """
    Processes a single company: finds and downloads its annual report.
    """
    print(f"\nProcessing: {company_name} ({company_symbol})")

    # First, try to find a direct PDF link
    pdf_url = find_annual_report_url(f'{company_name} {company_symbol} annual report', 'filetype:pdf')
    if pdf_url and pdf_url.endswith('.pdf'):
        download_report(pdf_url, company_symbol, output_dir)
        return

    # If no direct PDF is found, try to find the IR page
    ir_url = find_investor_relations_url(company_name, company_symbol)
    if ir_url:
        report_url = find_annual_report_link(ir_url)
        if report_url:
            download_report(report_url, company_symbol, output_dir)
        else:
            print(f"Could not find an annual report link on the IR page for {company_name}")
    else:
        print(f"Could not find an investor relations page for {company_name}")
