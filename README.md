# TMDB Movie Data Analysis: Documentation

## Project Overview

This project implements a complete movie data analysis workflow using
Python, Pandas, and the TMDb API. It demonstrates API extraction in `fetchData.py`, data
cleaning in `cleaning.py/.ipynb`, KPIs, advanced filtering, franchise analysis, and visual
insights. in `analysis.py/.ipynb`

## Objectives

-   Extract movie metadata from the [TMDb API](https://www.themoviedb.org/settings/api).
-   Clean and transform the dataset into usable analytical form.
-   Conduct exploratory data analysis (EDA).
-   Compute KPIs such as revenue, profit, ROI, popularity, and ratings.
-   Analyze franchises and directors.
-   Visualize trends and insights using Matplotlib.

## API Data Extraction

A list of movie IDs is used to fetch metadata via TMDb API. Results are
stored in Pandas DataFrames and saved to `data/raw/`.

## Data Cleaning & Transformation in `cleaning.ipynb`

Key tasks include: 
- Removing irrelevant columns. 
- Parsing JSON-likefields (genres, companies, languages, etc.). 
- Converting budget andrevenue to million USD. 
- Handling missing values, invalid dates, and placeholders. 
- Filtering only "Released" movies. 
- Reordering columnsinto a standardized final schema.

## KPI Analysis in `analysis.ipynb`

KPIs include: 
- Highest/Lowest Revenue 
- Highest/Lowest Profit
- Highest/Lowest ROI 
- Most Voted Movies 
- Highest/Lowest Rated Movies 
- Most Popular Movies

User-defined functions streamline ranking operations.

## Advanced Filtering
Examples: - Best-rated Sci-Fi Action movies starring Bruce Willis. -
Movies starring Uma Thurman directed by Quentin Tarantino.

## Franchise & Director Analysis

-   Compare standalone vs franchise movies using financial and popularity metrics.
-   Identify top-performing franchises.
-   Rank directors by revenue and ratings.

## Visualizations in `analysis.ipynb`

Charts include: - Budget vs Revenue - ROI distribution by genre -
Popularity vs Rating - Box office trends by year - Franchise vs
standalone comparison

## Folder Structure

```
    tmdb-movie-da/
    ├── data/
    │   ├── raw/            # raw fetched dat in scv format
    │   ├── cleaned/        # cleaned, and preprocessedd data
    ├── models/
    │   └── getAPI_Data.py  # script helps me to fetch data
    ├── scripts cleaning and analysis/ 
    │   ├── cleaning.*      # data preprocessing logic
    │   ├── analysis.*      # EDA, KPIs, and Insights 
    │   └── fetchData.py    # Helper extraction script
    ├── plots/              # keeps the image from analysis
    ├── requirements.txt    # dependencies used
    ├── Summary.txt         # Summary of key findings 
    ├── README.md          
    └── LICENSE

```
## Deliverables

-   Full ETL-style workflow using Python.
-   Cleaned dataset ready for analytics.
-   KPI tables and detailed insights.
-   Visual plots for financial and performance analysis.

## Technologies Used

-   Python
-   Pandas
-   Matplotlib
-   TMDb API
-   JSON parsing