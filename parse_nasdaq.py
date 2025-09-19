import csv

def parse_nasdaq_listed():
    """
    Parses the nasdaqlisted.txt file and returns a list of dictionaries,
    each containing the symbol and name of a company.
    It filters out ETFs and test securities.
    """
    companies = []
    try:
        with open('nasdaqlisted.txt', 'r') as f:
            # The first line is a header, so we skip it.
            # The last line is a footer.
            lines = f.read().splitlines()[1:-1]
            reader = csv.reader(lines, delimiter='|')

            for row in reader:
                # The format is: Symbol|Company Name|...
                # We only need the first two columns.
                if len(row) >= 2:
                    symbol = row[0].strip()
                    name = row[1].strip()

                    # Filter out ETFs and test securities
                    if not name.endswith(('ETF', 'ETN')) and not symbol.endswith('$'):
                         companies.append({'symbol': symbol, 'name': name})

    except FileNotFoundError:
        print("Error: nasdaqlisted.txt not found. Please download it first.")
        return []

    return companies

if __name__ == "__main__":
    companies = parse_nasdaq_listed()

    if companies:
        with open('nasdaq_companies.txt', 'w', encoding='utf-8') as f:
            for company in companies:
                f.write(f"{company['symbol']}|{company['name']}\n")
        print(f"Total non-ETF, non-test companies: {len(companies)}")
        print("Written to nasdaq_companies.txt")
    else:
        print("No companies found or file could not be read.")
