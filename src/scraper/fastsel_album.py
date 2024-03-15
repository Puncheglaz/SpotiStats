"""Module for fast selenium album scrapping."""
from fastsel_utils import data_scraping


def main():
    """Main function for data scraping."""
    data_scraping(
        request_mode='album',
        request_id='3VOqo81Nwyx8rcZEc2l379',
        operation_name='getAlbum',
        processed_file_name='albums',
        seltest_mode=False
    )


if __name__ == '__main__':
    main()
