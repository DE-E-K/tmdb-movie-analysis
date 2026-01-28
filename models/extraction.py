import os
import requests
import time
import pandas as pd
from dotenv import load_dotenv

class MovieExtractor:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.themoviedb.org/3'

    def fetch_movie_data(self, movie_id):
        """Fetch movie data from TMDb API with retry logic"""
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
                # User requested 5 second retry delay
                if attempt == 0:
                    print(f"Error fetching movie {movie_id}: {e}. Retrying in 5 seconds...")
                    time.sleep(5)
                else:
                    print(f"Failed to fetch movie {movie_id} after retry: {e}")
                    return None

    def fetch_all_movies(self, movie_ids):
        print(f"Fetching data for {len(movie_ids)} movies...")
        movie_ids = sorted(movie_ids)
        movies_data = []
        
        for movie_id in movie_ids:
            print(f"Fetching data for movie ID: {movie_id}")
            movie_data = self.fetch_movie_data(movie_id)
            
            if movie_data and 'id' in movie_data:
                movies_data.append(movie_data)
            else:
                print(f"Failed to fetch data for movie with ID: {movie_id}")
        
        return movies_data

    def run(self, movie_ids, output_path):
        data = self.fetch_all_movies(movie_ids)
        if not data:
            print("No data fetched.")
            return None
        
        df = pd.DataFrame(data)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"Data saved to {output_path}")
        return df
