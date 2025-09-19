import re
import json

def parse_hkex_html(html_content):
    """
    Parses the HTML content of the HKEX stock list page to extract company data.
    """
    # This regex is designed to find the 'stockData' assignment and capture the JSON-like array.
    match = re.search(r'stockData\s*:\s*(\[.*?\])', html_content, re.DOTALL)
    if not match:
        print("Could not find the stockData array in the HTML content.")
        return []

    # Extract the JSON-like string
    json_like_data = match.group(1)

    # The data is a JavaScript array of objects, but the keys are not quoted, which is invalid in standard JSON.
    # We need to add quotes to the keys to make it parsable.
    # The keys are: no, s, n, marketCap, price, change, revenue
    # A simple regex replacement can achieve this.

    # Let's use a more robust method to extract the data by finding all company objects
    # and then extracting the name and symbol from each.

    companies = []
    # Regex to find each object within the stockData array
    stock_objects = re.findall(r'{\s*no:\s*\d+,\s*s:\s*"(.*?)",\s*n:\s*"(.*?)",.*?}', json_like_data)

    for stock_object in stock_objects:
        symbol_full, name = stock_object
        # The symbol is in the format "hkg/0700", we only need "0700"
        symbol = symbol_full.split('/')[-1]
        companies.append(f"{symbol}|{name}")

    return companies

if __name__ == "__main__":
    try:
        with open("hkex.html", "r", encoding="utf-8") as f:
            html_content = f.read()
    except FileNotFoundError:
        print("Error: hkex.html not found. Please download it first.")
        exit()

    companies = parse_hkex_html(html_content)

    if companies:
        with open("hkex_companies.txt", "w", encoding="utf-8") as f:
            for company in companies:
                f.write(company + "\n")
        print(f"Successfully extracted {len(companies)} companies to hkex_companies.txt")
    else:
        print("Failed to extract any company data from hkex.html.")
