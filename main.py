import os
import time
from report_finder import process_company

def read_company_list(filename):
    """
    Reads a company list from a file.
    Each line should be in the format: SYMBOL|Company Name
    """
    companies = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or '|' not in line:
                    continue

                parts = line.split('|', 1)
                symbol = parts[0].strip()
                name = parts[1].strip()
                companies.append({'symbol': symbol, 'name': name})
    except FileNotFoundError:
        print(f"Warning: Company list file not found: {filename}")
    return companies

def main():
    """
    Main function to process US and HK company lists.
    """
    # Define output directories
    us_output_dir = "reports/us"
    hk_output_dir = "reports/hk"

    # Create directories if they don't exist
    os.makedirs(us_output_dir, exist_ok=True)
    os.makedirs(hk_output_dir, exist_ok=True)

    # Process a small number of US companies for testing
    print("--- Processing US Companies (Sample) ---")
    us_companies = read_company_list('nasdaq_companies.txt')
    if us_companies:
        for company in us_companies[:2]: # Process only the first 2 for testing
            # This is where the agent would call the tool
            # I am simulating this by calling the function directly
            # This will fail in the current environment, but it shows the intended logic
            try:
                process_company(company['name'], company['symbol'], us_output_dir)
            except NameError:
                print("Skipping company due to missing 'google_search' tool.")
            time.sleep(2)
    else:
        print("No US companies to process.")

    # Process a small number of HK companies for testing
    print("\n--- Processing HK Companies (Sample)---")
    hk_companies = read_company_list('hkex_companies.txt')
    if hk_companies:
        for company in hk_companies[:2]: # Process only the first 2 for testing
            try:
                process_company(company['name'], company['symbol'], hk_output_dir)
            except NameError:
                print("Skipping company due to missing 'google_search' tool.")
            time.sleep(2)
    else:
        print("No HK companies to process.")

    print("\n--- Sample processing complete. ---")

if __name__ == "__main__":
    main()
