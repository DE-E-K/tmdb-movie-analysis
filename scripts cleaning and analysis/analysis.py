#!/usr/bin/env python
# coding: utf-8

# import necessary libraries
import pandas as pd
from IPython.display import display
from datetime import datetime as dt
import seaborn as sns
import matplotlib.pyplot as plt
import re


# load the cleaned dataset
df = pd.read_csv(r'../data/cleaned/movies_data_cleaned.csv',parse_dates=True)
df.shape


# ## KPI Implementation & Analysis
# Identify the Best/Worst Performing Movies based Highest Revenue Budget and Profit

# for revenue
df['revenue_rank'] = df['revenue_musd'].rank(ascending=False)
df = df.sort_values(by='revenue_musd', ascending=False)

print(f"""Top 3 movies with highest revenue 
      \n{df[['id','title', 'revenue_musd', 'revenue_rank']].head(3)} 
      \n\n bottom 2 lowest revenue movies:
      \n{df[['id','title', 'revenue_musd', 'revenue_rank']].tail(2)}""")

#  bugdet
df['budget_rank'] = df.budget_musd.rank(ascending=False)
df = df.sort_values(by='budget_musd', ascending=False)

print(f"""Top 3 movies with highest budget:
      \n{df[['id','title', 'budget_musd', 'budget_rank']].head(3)} 
      \n\n bottom 2 lowest budget movies:
      \n{df[['id','title', 'budget_musd', 'budget_rank']].tail(2)}""")

# for profit
df['profit_rank'] = df['profit_musd'].rank(ascending=False)
df = df.sort_values(by='profit_musd', ascending=False)
print(f"""Top 3 movies that generate highest profit:
      \n{df[['id','title', 'profit_musd', 'profit_rank']].head(3)} 
      \n\n bottom 2 lowest profit:
      \n{df[['id','title', 'profit_musd', 'profit_rank']].tail(2)}""")


# for return on investement
df['roi'] = df['revenue_musd'] / df['budget_musd']
roi = df[df['budget_musd']>10].sort_values(by='roi', ascending=False)
roi['roi_rank'] = roi['roi'].rank(ascending=False)
print(f"""Top 3 highest performining movies by return on invest and bugdet great than 10M:
      \n{roi[['id','title', 'budget_musd', 'revenue_musd', 'profit_musd', 'roi_rank']].head(3)} 
      \n\n least 2 movies:
      \n{roi[['id','title', 'budget_musd', 'revenue_musd', 'profit_musd', 'roi_rank']].tail(2)}""")


# Based on voting
df['vote_rank'] = df['vote_count'].rank(ascending=False)
df = df.sort_values('vote_count', ascending=False)
print(f"""Top voted movies: 
      \n{df[['id', 'title', 'vote_count', 'vote_rank']].head(3)}""")


# Ratings filters: only movies with >= 10 votes
rated = df[df['vote_count'] >= 10].sort_values('vote_average', ascending=False)
print(f"""Top 3 highest performing movies  by voting more than 10k votes:
      \n{rated[['id', 'title', 'vote_average']].head(3)} 
      \nLeast 2 movies  with lowest rated with vote >= 10M):
      \n{rated[['id', 'title', 'vote_average']].tail(2)}""")


# Popularity
df['pop_rank'] = df['popularity'].rank(ascending=False)
df = df.sort_values('popularity', ascending=False)
print(f"""Top 3 popularity movies:
      \n{df[['id', 'title', 'popularity', 'pop_rank']].head(3)} 
      \nLeast 2 performing movies by popularity:
      \n{df[['id', 'title', 'popularity', 'pop_rank']].tail(2)}""")


# # Franchise vs. Standalone Movie Performance
def analyze_franchises_vs_standalone(data):
        """Compare franchise vs standalone movie performance"""
        print("\n--- Franchise vs Standalone Analysis ---")

        # Identify franchise movies
        data['is_franchise'] = data['belongs_to_collection'].notna()

        comparison = {}
        metrics = ['revenue_musd', 'roi', 'budget_musd', 'popularity', 'vote_average']

        for metric in metrics:
            if metric in data.columns:
                franchise_mean = data[data['is_franchise']][metric].mean()
                standalone_mean = data[~data['is_franchise']][metric].mean()
                comparison[metric] = {
                    'franchise': franchise_mean,
                    'standalone': standalone_mean,
                    'difference': franchise_mean - standalone_mean
                }

        # Display results
        for metric, values in comparison.items():
            print(f"\n{metric.upper()}:")
            print(f"  Franchise Mean: {values['franchise']:.2f}")
            print(f"  Standalone Mean: {values['standalone']:.2f}")
            print(f"  Difference: {values['difference']:.2f}")

        return comparison


comparison = analyze_franchises_vs_standalone(df)


def successful_franchises(data):
    """Find the most successful movie franchises"""
    if 'belongs_to_collection' not in data.columns:
        return pd.DataFrame()

    franchise_data = []
    franchises = data['belongs_to_collection'].dropna().unique()

    for franchise in franchises:
        franchise_movies = data[data['belongs_to_collection'] == franchise]

        franchise_data.append({
            'franchise': franchise,
            'movie_count': len(franchise_movies),
            'total_budget': franchise_movies['budget_musd'].sum(),
            'mean_budget': franchise_movies['budget_musd'].mean(),
            'total_revenue': franchise_movies['revenue_musd'].sum(),
            'mean_revenue': franchise_movies['revenue_musd'].mean(),
            'mean_rating': franchise_movies['vote_average'].mean(),
        })

    franchise_df = pd.DataFrame(franchise_data)

    if not franchise_df.empty:
        print("\n--- Most Successful Franchises ---")
        franchise_df.sort_values('total_revenue', ascending=False).head()
    return franchise_df


# **5. Find the Most Successful Movie Franchises based on:** 
# * Total number of movies in franchise
# * Total & Mean Budget
# * Total & Mean Revenue
# * Mean Rating

successful_franchises(df)

# most Success full franchise movies and directors
succuss = df[['id', 'title', 'collection_name','director', 'budget_musd', 
              'revenue_musd', 'vote_count', 'roi', 'popularity']].\
                  dropna().reset_index()
succuss[['id', 'title', 'collection_name','director']]

# Find the Most Successful Directors based on:
# - Total Number of Movies Directed
# - Total Revenue
# - Mean Rating

#  BY REVENUE GENERATED
dir = df.groupby("director").agg(
    total_revenue=("revenue_musd", "sum"),
    movie_count=("revenue_musd", "count"),
    average_rating = ("vote_count", "mean")
).sort_values("total_revenue", ascending=False).head(20)
print(f"""\nDirectors performance based on:
      \n -Total Number of Movies Directed,
      \n -Total Revenue
      \n -Mean Rating""")
print(dir)

df.isna().sum()

# ## Data Visualization
# Use Pandas, Matplotlib to visualize:
# - Revenue vs. Budget Trends
# - ROI Distribution by Genre
# - Popularity vs. Rating
# - Yearly Trends in Box Office Performance

# - Comparison of Franchise vs. Standalone Success
# ensure datetime and year column
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
df['year'] = df['release_date'].dt.year

# helper to extract primary genre name from the stored string
def _primary_genre(genre_str):
    if pd.isna(genre_str):
        return np.nan
    m = re.search(r"'name':\s*'([^']+)'", str(genre_str))
    if m:
        return m.group(1)
    parts = str(genre_str).split('|')
    return parts[0].strip() if parts else np.nan

if 'primary_genre' not in df.columns:
    df['primary_genre'] = df['genres'].apply(_primary_genre)


# 1) Revenue vs Budget Trends (log-log scatter)
plt.figure(figsize=(9,6))
plot1 = df[(df['budget_musd'] > 0) & (df['revenue_musd'] > 0)]
sns.scatterplot(
    data=plot1,
    x='budget_musd',
    y='revenue_musd',
    hue='collection_name',
    alpha=0.7,
    edgecolor=None,
    legend='brief'
)
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Budget (M USD) [log scale]')
plt.ylabel('Revenue (M USD) [log scale]')
plt.title('Revenue vs Budget (log-log) colored by primary genre')
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
plt.tight_layout()
plt.show()


# 2) ROI Distribution by Genre (boxplot for top genres)
# top_genres = df['primary_genre'].value_counts()
plt.figure(figsize=(10,6))
sns.barplot(
    data  = pd.DataFrame(df.groupby('primary_genre')['roi'].sum()),
    x='primary_genre',
    y='roi'
)
plt.xticks(rotation=45)
plt.ylabel('ROI (revenue/budget)')
plt.title('ROI distribution for top 10 primary genres')
plt.tight_layout()
plt.show()

# 3) Popularity vs Rating (bubble with vote_count size, color by ROI)
plt.figure(figsize=(8,6))
sizes = (df['vote_count'].fillna(0) / (df['vote_count'].max() or 1)) * 250
sc = plt.scatter(
    df['vote_average'],
    df['popularity'],
    s=sizes,
    c=df['roi'],
    cmap='viridis',
    alpha=0.7,
    edgecolors='w',
    linewidth=0.3
)
cbar = plt.colorbar(sc)
cbar.set_label('ROI')
plt.xlabel('Vote Average (Rating)')
plt.ylabel('Popularity')
plt.title('Popularity vs Rating (bubble size ~ vote count, color ~ ROI)')
plt.tight_layout()
plt.show()

# 4) Yearly Trends in Box Office Performance
yearly = df.dropna(subset=['year']).groupby('year').agg(
    total_revenue=('revenue_musd', 'sum'),
    mean_revenue=('revenue_musd', 'mean'),
    movies_count=('id', 'count')
).sort_index()

plt.figure(figsize=(10,6))
plt.plot(yearly.index, yearly['total_revenue'], marker='o', label='Total Revenue (M USD)')
plt.plot(yearly.index, yearly['mean_revenue'], marker='o', label='Mean Revenue (M USD)')
plt.bar(yearly.index, yearly['movies_count'], alpha=0.15, label='Number of Movies')
plt.xlabel('Year')
plt.ylabel('Revenue (M USD)')
plt.title('Yearly Box Office Trends')
plt.legend()
plt.tight_layout()
plt.show()

# 5) Comparison of Franchise vs Standalone Success
df['is_franchise'] = df['belongs_to_collection'].notna()

fig, axes = plt.subplots(1, 2, figsize=(12,5))
sns.barplot(data=df, x='is_franchise', y='revenue_musd', ax=axes[0])
axes[0].set_xticklabels(['Standalone', 'Franchise'])
axes[0].set_title('Revenue: Franchise vs Standalone')
axes[0].set_ylabel('Revenue (M USD)')

sns.barplot(data=df[df['budget_musd'] > 0], x='is_franchise', y='roi', ax=axes[1])
axes[1].set_xticklabels(['Standalone', 'Franchise'])
axes[1].set_title('ROI: Franchise vs Standalone')
axes[1].set_ylabel('ROI (revenue/budget)')
plt.tight_layout()
plt.show()