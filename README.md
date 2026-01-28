# TMDB Movie Data Analysis

A comprehensive data engineering and analysis pipeline for movie data fetched from the [The Movie Database (TMDB) API](https://www.themoviedb.org/). This project mimics a real-world ETL process: extracting raw data, cleaning complex JSON structures, performing financial analysis, and generating professional visualizations to uncover trends in the film industry.

## 🚀 Key Features

### [1. Data Extraction](`models/extraction.py`)
- **Robust API Handling**: Fetches movie metadata with built-in retry logic for network stability.
- **Batch Processing**: Handles bulk movie IDs efficiently.

### [2. Advanced Data Cleaning](`models/cleaning.py`)
- **JSON Flattening**: Parses nested JSON fields (Genres, Production Companies, Cast/Crew) into usable formats.
- **Schema Standardization**: Converts data types, handles missing values, and ensures consistent schema.
- **Deduplication**: Smart handling of duplicate records and unhashable structures.

### [3. Financial Analysis](`models/analysis.py`)
- **KPI Calculation**: Computes ROI, Profit, and multi-currency adjustments.
- **Comparative Analysis**: Franchise vs. Standalone movies.
- **Director Metrics**: Aggregates performance metrics for top directors.

### [4. Visualization](`models/visualization.py`)
Generates high-quality charts using **Seaborn** and **Matplotlib**:
- **Revenue trends**: Budget vs. Revenue correlations.
- **Genre Insights**: ROI distribution and average returns by genre.
- **Time Analysis**: Yearly box office evolution.
- **Audience Metrics**: Popularity vs. Ratings correlations.

---

## 📂 Project Structure

```text
DEM02/
├── data/
│   ├── raw/                 # Valid raw CSVs from extraction
│   └── cleaned/             # Production-ready datasets
├── models/
│   ├── extraction.py        # API extraction module
│   ├── cleaning.py          # Data cleaning & transformation
│   ├── analysis.py          # Business logic & KPIs
│   └── visualization.py     # Plotting engine
├── plots/                   # Generated visual reports
├── main.py                  # Pipeline entry point
├── .env                     # API Configuration
└── requirements.txt         # Python dependencies
```

---

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.8+
- TMDB API Key from [TMDB](https://www.themoviedb.org/settings/api)

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/DE-E-K/tmdb-movie-analysis.git
    cd DEM02
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure API Key**:
    Create a `.env` file in the root directory:
    ```env
    api_key=YOUR_TMDB_API_KEY
    ```

---

## ⚡ Usage

Run the full pipeline (Extract → Clean → Analyze → Visualize):

```bash
python main.py
```

### Generated Visualizations (in `plots/`)
*   **`Revenue_vs_Budget.png`**: Scatter plot showing the correlation between investment and return.
*   **`ROI_Distribution_by_Genre.png`**: Financial risk/reward profiles for major genres.
*   **`ROI_by_Genre.png`**: Ranked bar chart of most profitable genres.
*   **`Revenue_vs_Budget_Yearly.png`**: Comparative bar chart of total industry spend vs. earning per year.
*   **`Popularity_vs_Rating.png`**: How audience buzz correlates with critical score.
*   **`Yearly_Box_Office_Trends.png`**: The growth of the movie industry over time.
*   **`Franchise_vs_Standalone.png`**: Performance comparison of IP-driven content vs. original films.

---

## Future Improvements
- **Database Integration**: Load cleaned data into PostgreSQL/Snowflake.
- **Orchestration**: Schedule daily updates using Apache Airflow.
