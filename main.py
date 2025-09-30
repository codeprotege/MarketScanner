import pandas as pd
from cpd_scrapers import (
    scrape_ia,
    scrape_hkcaavq,
    scrape_piba,
    scrape_hkcii,
    scrape_peak,
    scrape_cpduk,
)

def main():
    """
    Main function to run all scrapers and save the results.
    """
    all_courses = []

    # List of all scraper functions to run
    scrapers = [
        scrape_ia,
        scrape_hkcaavq,
        scrape_piba,
        scrape_hkcii,
        scrape_peak,
        scrape_cpduk,
    ]

    for scraper in scrapers:
        try:
            print(f"Running scraper: {scraper.__name__}")
            courses = scraper()
            if courses:
                all_courses.extend(courses)
                print(f"Found {len(courses)} courses from {scraper.__name__}")
            else:
                print(f"No courses found from {scraper.__name__}")
        except Exception as e:
            print(f"An error occurred in {scraper.__name__}: {e}")

    df = pd.DataFrame(all_courses)
    if not df.empty:
        df.to_csv("cpd_courses_final.csv", index=False)
        print("Scraped data saved to cpd_courses_final.csv")
    else:
        print("No courses were found from any scraper.")

if __name__ == "__main__":
    main()