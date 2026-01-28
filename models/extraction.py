import os
import requests
import time
import pandas as pd
import logging
from concurrent.futures import ProcessPoolExecutor, as_completed

logger = logging.getLogger(__name__)

class MovieExtractor:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.themoviedb.org/3'

    def fetch_movie_data(self, movie_id):
        """Fetch movie data from TMDb API with retry logic"""
        logger.debug(f"Fetching movie ID {movie_id}...")
        url = f"{self.base_url}/movie/{movie_id}"
        params = {
            'api_key': self.api_key,
            'append_to_response': 'credits'
        }
        
        # Retry mechanism: 2 attempts (1st try + 1 retry)
        for attempt in range(2):
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                if attempt == 0:
                    logger.warning(f"Request failed for movie {movie_id}: {e}. Retrying in 5 seconds...")
                    time.sleep(5)
                else:
                    logger.error(f"Permanent failure for movie {movie_id} after retry: {e}")
                    return None

    def fetch_all_movies(self, movie_ids, max_workers=10):
        logger.info(f"Starting batch fetch for {len(movie_ids)} movies with {max_workers} workers.")
        movie_ids = sorted(movie_ids)
        movies_data = []
        failed_ids = []
        
        # Using ProcessPoolExecutor for Multiprocessing as requested
        # Note: For strict I/O bound tasks like API requests, Threads are usually preferred,
        # but ProcessPoolExecutor fulfills the explicit requirement for "multiprocessing".
        
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            # Map future to movie_id
            future_to_id = {executor.submit(self.fetch_movie_data, mid): mid for mid in movie_ids}
            
            success_count = 0
            
            for future in as_completed(future_to_id):
                movie_id = future_to_id[future]
                try:
                    data = future.result()
                    if data and 'id' in data:
                        movies_data.append(data)
                        success_count += 1
                    else:
                        failed_ids.append(movie_id)
                        logger.warning(f"Failed to fetch valid data for movie ID: {movie_id}")
                except Exception as exc:
                    failed_ids.append(movie_id)
                    logger.error(f"Movie ID {movie_id} generated an exception: {exc}")

        logger.info(f"Batch fetch complete. Successful: {success_count}, Failed: {len(failed_ids)}.")
        if failed_ids:
            logger.info(f"List of failed/invalid Movie IDs: {failed_ids}")
        
        return movies_data

    def run(self, movie_ids, output_path):
        data = self.fetch_all_movies(movie_ids)
        if not data:
            logger.error("No data fetched.")
            return None
        
        df = pd.DataFrame(data)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        logger.info(f"Data saved to {output_path}")
        return df
