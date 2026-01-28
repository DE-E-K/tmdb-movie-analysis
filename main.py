import os
import sys
from dotenv import load_dotenv
from models.extraction import MovieExtractor
from models.cleaning import DataCleaner
from models.analysis import MovieAnalyzer
from models.visualization import DataVisualizer

def main():
    # Setup paths
    project_root = os.path.dirname(os.path.abspath(__file__))
    raw_data_path = os.path.join(project_root, 'data', 'raw', 'movies_data.csv')
    cleaned_data_path = os.path.join(project_root, 'data', 'cleaned', 'movies_data_cleaned.csv')
    plots_dir = os.path.join(project_root, 'plots')

    # Load environment variables
    load_dotenv()
    api_key = os.getenv("api_key")
    if not api_key:
        print("Error: API key not found in .env")
        sys.exit(1)

    print("=== TMDB Data Pipeline Starting ===")

    # 1. Extraction
    print("\n--- Step 1: Data Extraction ---")
    movie_ids = [0, 299534, 19995, 140607, 299536, 597, 135397, 420818, 24428,
                 168259, 99861, 284054, 12445, 181808, 330457, 351286, 109445,
                 321612, 260513]
    extractor = MovieExtractor(api_key)
    extractor.run(movie_ids, raw_data_path)

    # 2. Cleaning
    print("\n--- Step 2: Data Cleaning ---")
    cleaner = DataCleaner()
    df_cleaned = cleaner.run(raw_data_path, cleaned_data_path)

    # 3. Analysis
    print("\n--- Step 3: Analysis ---")
    analyzer = MovieAnalyzer(df_cleaned)
    analyzer.run()

    # 4. Visualization
    print("\n--- Step 4: Visualization ---")
    visualizer = DataVisualizer(df_cleaned, plots_dir)
    visualizer.run()

    print("\n=== Pipeline Complete ===")

if __name__ == "__main__":
    main()
