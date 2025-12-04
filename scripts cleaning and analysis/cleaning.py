#!/usr/bin/env python
# coding: utf-8

# Load necessary modules and libraries
import pandas as pd
import numpy as np
from ast import literal_eval
import os 

# ## DATA PREPARATION AND CLEANING
# ### Load dataset and interaction with them

df = pd.read_csv(r'..\data\raw\movies_data.csv')

# Display basic information about the DataFrame
df.info()

# Descriptive statistics of numerical columns
df.describe().T

# descriptive statistics of categorical and string columns
df.describe(include=['O']).T

# Removing the irrelevant columns

irrelevant_cols = ['adult', 'imdb_id', 'original_title', 'video', 'homepage']

# function to drop columns if exist in df
def drop_irrelevant_columns(dataframe, columns):
    for col in columns:
        if col in dataframe.columns:
            dataframe = dataframe.drop(columns=col)
        else: 
            print(f"Column with name '{col}' does not exist in the DataFrame.")
    return dataframe

#  before removing irrelevant columns
print(f"Before removing irrelevant columns df has {df.shape[1]} columns.")

# removing irrelevant columns
df = drop_irrelevant_columns(df, irrelevant_cols)

print(f"After removing irrelevant columns df has {df.shape[1]} columns.")

# # Evaluating the columns look like json
# json like columns to be parsed
json_like_cols = ['belongs_to_collection', 'genres', 'production_countries', 
                  'production_companies', 'spoken_languages']
df[json_like_cols].head()

# ### Extracting the columns in `belongs_to_colection` column which looks like dictionary or json

df['belongs_to_collection'].head()

# Extracting the column 'collecitionname', and other from belongs_to_collection
def safe_expand_dict(x):
    if pd.isna(x) or x is None or x == '':
        return np.nan
    elif isinstance(x, str):
        try:
            import ast
            return ast.literal_eval(x)
        except:
            return np.nan
    elif isinstance(x, dict):
        return x
    else:
        return np.nan

# Apply safe conversion
clean_series = df['belongs_to_collection'].apply(safe_expand_dict)
clean_series.head()

# Expand and maintain original index
df_cleaned_series = pd.json_normalize(clean_series)
df_exp = pd.concat([df, df_cleaned_series['name']], axis=1)
df_exp.rename(columns={'name': 'collection_name'}, inplace=True)


# ## Separate columns with | for remaing columns 
# - Genre names (genres → separate multiple genres with "|").
# - Spoken languages (spoken_languages → separate with "|").
# - Production countries (production_countries → separate with "|").
# - Production companies (production_companies → separate with "|").
#  columns to separate it's values by |

json_cols_tosep = json_like_cols[1:]
df_exp[json_cols_tosep].head()

# Remove square brackets and separate dictionaries by ' | ' as identified pattern
df_exp[json_cols_tosep] = df_exp[json_cols_tosep].apply(
    lambda x: x.str.replace(r'[\[\]]', '', regex=True)
    .str.replace(r'(?<=\}),\s*', ' | ', regex=True))

# clean original by repacing ['']
df_exp['origin_country'] = df_exp['origin_country'].replace(r"[\[''\]]","", regex=True)

df_exp[json_cols_tosep].head(2)

# change release_date to datetime format
df_exp['release_date'] = pd.to_datetime(df_exp['release_date'], errors='coerce')

# Final DataFrame info after making same cleaning steps
df_exp.info()

# express budget anda revenue to millions of 
df_exp['budget_musd'] = df_exp['budget'] / 1000000
df_exp['revenue_musd'] = df_exp['revenue'] / 1000000
df_exp['profit_musd'] = df_exp['revenue_musd'] - df_exp['budget_musd'] # profit in million usd
df_exp['roi'] = df_exp['revenue_musd'] / df_exp['budget_musd'] # return on investment

# remove origingal_language and status columns
df_exp.drop(columns=['status', 'status', 'budget', 'revenue'], inplace=True)

# check missing values in the final cleaned DataFrame
df_exp.isna().sum().sort_values(ascending=False)

# deep dive into credits column
df_exp[['cast', 'crew']] = pd.json_normalize(df_exp['credits'].apply(literal_eval))

# get cast crew data separately from credits_data and save to csv files
cast = pd.json_normalize(df_exp['cast'].explode())
crew = pd.json_normalize(df_exp['crew'].explode())

# save to csv files  
cast.to_csv('../data/raw/cast_data.csv', index=False)
crew.to_csv('../data/raw/crew_data.csv', index=False)

cast.shape, crew.shape

def add_size(df, col):
    parsed = df[col]

    # Count items and store in new column
    df[col + '_size'] = parsed.apply(len)
    return df

cols = ['cast', 'crew']
for col in cols:
    df_exp = add_size(df_exp, col)

# define a function to get the director for credits columm
def extract_director(credits_data):
    # handle missing values
    if pd.isna(credits_data) or credits_data in (None, ''):
        return np.nan

    # if it's a string representation, try to parse it to a dict/list
    if isinstance(credits_data, str):
        try:
            credits_data = literal_eval(credits_data)
        except Exception:
            return np.nan

    # now ensure we have a dict with 'crew'
    if not isinstance(credits_data, dict) or 'crew' not in credits_data:
        return np.nan

    crew = credits_data.get('crew') or []
    # crew should be a list of dicts; extract director name(s)
    directors = [person.get('name') for person in crew if person.get('job') == 'Director']
    return directors[0] if directors else np.nan

df_exp['director'] = df_exp['credits'].apply(extract_director)

# compare df_exp.columns with the target order and reorder if possible
target_order = [
    'id', 'title', 'tagline', 'release_date', 'genres', 'belongs_to_collection',
    'original_language', 'budget_musd', 'revenue_musd', 'production_companies',
    'production_countries', 'vote_count', 'vote_average', 'popularity',
    'runtime', 'overview', 'spoken_languages', 'poster_path', 'cast',
    'cast_size', 'director', 'crew_size', 'profit_musd', 'collection_name'
]

existing_cols = list(df_exp.columns)
missing = [c for c in target_order if c not in existing_cols]
missing

# drop all columns whose name ends with '.1'
cols_to_drop = [col for col in df.columns if col.endswith('.1')]

if cols_to_drop:
    df.drop(columns=cols_to_drop, inplace=True)
    print(f"Dropped columns: {cols_to_drop}")
else:
    print("No columns ending with '.1' found.")


final = df_exp[target_order]
final.to_csv('../data/cleaned/movies_data_cleaned.csv', index=False)

"""======= Data cleaning process complete 🍵======"""