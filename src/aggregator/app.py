"""Module application to collect data from Spotify."""
from loguru import logger
from loguru_config import LoguruConfig

from src.aggregator.aggregator import aggregate
from src.aggregator.artist_aggregate import artist_aggregate_main
from src.aggregator.auth_credentials import access_token, token_type

LoguruConfig.load("loguru-config.yaml")


def main():
    """Main function for application entrypoint."""
    logger.info("Starting general aggregator")
    low, high = 1, 2
    logger.debug(f"Low: {low}, High: {high}")
    aggregate(low=low, high=high)
    logger.info("General aggregator finished")

    logger.info("Starting artist aggregator")
    artist_aggregate_main(
        source_file_path='src/aggregator/resources/spotify-followed-artists-low.json',
        id_file_path='src/aggregator/resources/artists-ids-list-low.json',
        headers={'Authorization': f'{token_type}  {access_token}'}
    )
    logger.info("Artist aggregator finished")


if __name__ == '__main__':
    main()
