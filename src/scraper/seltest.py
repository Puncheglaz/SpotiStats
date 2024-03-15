"""Module for fast selenium scraping."""
from fastsel_utils import setup_driver, data_scraping

driver = setup_driver()


def main():
    """Main function for data scraping."""
    data_scraping(seltest_mode=True)


main()
