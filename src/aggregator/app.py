"""Module application to collect data from Spotify."""
from loguru import logger
from loguru_config import LoguruConfig
from scalene import scalene_profiler

from src.aggregator.aggregator import aggregate
from src.aggregator.artist_aggregate import artist_aggregate_main
from src.aggregator.auth_credentials import (
    access_token, token_type, client_headers,
    get_artist_stats_extensions, get_tracks_extensions
)
from src.aggregator.stats_from_files import stats_from_files_main
from src.aggregator.stats_update import stats_update_main
from src.aggregator.tracks_count import tracks_count

LoguruConfig.load("loguru-config.yaml")


def main():
    """Main function for application entrypoint."""
    scalene_profiler.start()
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

    logger.info("Starting stats from files aggregator")
    stats_from_files_main(
        timeout=1,
        request_count=0,
        file_path="src/aggregator/resources/artists",
        artist_count=0,
        albums_path="src/aggregator/resources/albums",
        headers=client_headers,
        extensions=get_artist_stats_extensions
    )
    logger.info("Stats from files aggregator finished")

    logger.info("Starting stats update aggregator")
    stats_update_main(
        artist_ids=[
            '0M2HHtY3OOQzIZxrHkbJLT', '4tZwfgrHOc3mvqYlEYSvVi', '00FQb4jTyendYWaN8pK0wa'
        ],
        timeout=1,
        request_count=0,
        file_path='src/aggregator/resources/artists',
        headers=client_headers,
        tracks_extensions=get_tracks_extensions,
        artist_extensions=get_artist_stats_extensions
    )
    logger.info("Stats update aggregator finished")

    logger.info("Starting tracks count")
    tracks_count()
    logger.info("Tracks count finished")
    scalene_profiler.stop()


if __name__ == '__main__':
    main()
