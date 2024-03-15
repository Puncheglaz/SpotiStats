"""Module for fast selenium artist scrapping."""
from fastsel_utils import data_scraping


def main():
    """Main function for data scraping."""
    data_scraping(
        request_mode='artist',
        request_id='4iHNK0tOyZPYnBU7nGAgpQ',
        operation_name='queryArtistOverview',
        processed_file_name='artist_stats',
        seltest_mode=False
    )


if __name__ == '__main__':
    main()
