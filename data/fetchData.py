# Load necessary modules
import os
import sys

# Add the project root to sys.path to enable importing modules from sibling directories
script_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(script_dir, os.pardir))
sys.path.insert(0, project_root)

from models.getAPI_Data import fetch_all_movies
from dotenv import load_dotenv
import pandas as pd


def main():
    """
    Fetches movie data from The Movie Database (TMDB) API for a predefined
    list of movie IDs and saves the data to a CSV file.
    """
    load_dotenv()  # Load environment variables from .env file

    api_key = os.getenv("api_key")
    if not api_key:
        print("Error: API key 'api_key' not found in .env file.", file=sys.stderr)
        sys.exit(1)

    # A list of valid movie IDs.
    movie_ids = [0, 299534, 19995, 140607, 299536, 597, 135397, 420818, 24428,
                 168259, 99861, 284054, 12445, 181808, 330457, 351286, 109445,
                 321612, 260513]

    print(f"Fetching data for {len(movie_ids)} movie...")
    movies_data = fetch_all_movies(movie_ids, api_key)

    if not movies_data:
        print("No movie data was fetched. Exiting.")
        return

    df = pd.DataFrame(movies_data)

    print(f"Successfully fetched data for {len(df)} movies.")
    print(f"Missing data for {len(movie_ids) - len(df)} movies.")

    # Create a more robust path to the output file
    output_dir = os.path.join(os.path.dirname(__file__), 'raw')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'movies_data.csv')
    df.to_csv(output_path, index=False)
    print(f"Data saved to {output_path}")

if __name__ == "__main__":
    main()
