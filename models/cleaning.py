import pandas as pd
import numpy as np
from ast import literal_eval
import os
import logging

logger = logging.getLogger(__name__)

class DataCleaner:
    def __init__(self):
        pass

    def load_data(self, filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        return pd.read_csv(filepath)

    def safe_parse(self, x):
        # If it's already a list or dict, return it directly
        if isinstance(x, (list, dict)):
            return x
            
        # Handle null/empty values for scalars
        if x is None or (isinstance(x, str) and x == ''):
            return []
            
        # Check for NaN (only if it's a number/float/scalar that pandas considers NA)
        try:
            if pd.isna(x):
                return []
        except (ValueError, TypeError):
            # Fallback if pd.isna fails on complex objects
            pass

        try:
            return literal_eval(str(x))
        except (ValueError, SyntaxError, TypeError):
            return []

    def flatten_column(self, df, col_name, key='name', separator='|'):
        def _extract(x):
            parsed = self.safe_parse(x)
            if isinstance(parsed, dict):
                # Handle single dict (like belongs_to_collection)
                return parsed.get(key, np.nan)
            elif isinstance(parsed, list):
                # Handle list of dicts
                values = [item.get(key, '') for item in parsed if isinstance(item, dict) and key in item]
                return separator.join(values) if values else np.nan
            return np.nan
        
        return df[col_name].apply(_extract)

    def parse_credits_cast(self, x):
        parsed = self.safe_parse(x)
        if not isinstance(parsed, dict):
            return [], 0
        cast_list = parsed.get('cast', [])
        if not isinstance(cast_list, list):
            return [], 0
        cast_names = [p.get('name') for p in cast_list]
        return cast_names, len(cast_list)

    def parse_credits_director(self, x):
        parsed = self.safe_parse(x)
        if not isinstance(parsed, dict):
            return np.nan, 0
        crew_list = parsed.get('crew', [])
        if not isinstance(crew_list, list):
            return np.nan, 0
        
        directors = [p.get('name') for p in crew_list if p.get('job') == 'Director']
        director = directors[0] if directors else np.nan
        return director, len(crew_list)

    def drop_irrelevant_columns(self, df):
        """Step 1: Removal of irrelevant columns."""
        logger.info("Dropping irrelevant columns...")
        irrelevant_cols = ['adult', 'imdb_id', 'original_title', 'video', 'homepage']
        initial_cols = len(df.columns)
        df = df.drop(columns=[c for c in irrelevant_cols if c in df.columns])
        logger.debug(f"Dropped {initial_cols - len(df.columns)} columns.")
        return df

    def flatten_json_columns(self, df):
        """Step 2: Parse and flatten JSON-like columns."""
        logger.info("Flattening JSON columns...")
        # Collection
        df['collection_name'] = self.flatten_column(df, 'belongs_to_collection')
        
        # Others
        for col in ['genres', 'production_countries', 'production_companies', 'spoken_languages']:
            df[col] = self.flatten_column(df, col)
            df[col] = df[col].replace('', np.nan)
        return df

    def convert_datatypes(self, df):
        """Step 3: Convert types and handle basic filtering."""
        logger.info("Converting datatypes and filtering status...")
        df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
        
        if 'status' in df.columns:
            initial_rows = len(df)
            df = df[df['status'] == 'Released'].copy()
            df = df.drop(columns=['status'])
            dropped = initial_rows - len(df)
            if dropped > 0:
                logger.info(f"Filtered out {dropped} non-released movies.")
        
        numeric_cols = ['budget', 'id', 'popularity', 'revenue', 'vote_count', 'vote_average', 'runtime']
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Handle Zeros -> NaN
        for col in ['budget', 'revenue', 'runtime']:
            df[col] = df[col].replace(0, np.nan)
            
        return df

    def calculate_financials(self, df):
        """Step 4: Calculate derived financial metrics."""
        logger.info("Calculating financial metrics...")
        df['budget_musd'] = df['budget'] / 1e6
        df['revenue_musd'] = df['revenue'] / 1e6
        df['profit_musd'] = df['revenue_musd'] - df['budget_musd']
        df['roi'] = df['revenue_musd'] / df['budget_musd']
        return df

    def process_credits(self, df):
        """Step 5: Extract Cast and Crew information."""
        logger.info("Processing credits...")
        cast_data = df['credits'].apply(self.parse_credits_cast)
        df['cast'] = cast_data.apply(lambda x: "|".join(x[0]))
        df['cast_size'] = cast_data.apply(lambda x: x[1])
        
        crew_data = df['credits'].apply(self.parse_credits_director)
        df['director'] = crew_data.apply(lambda x: x[0])
        df['crew_size'] = crew_data.apply(lambda x: x[1])
        return df

    def handle_missing_and_duplicates(self, df):
        """Step 6: Handle missing text and remove duplicates."""
        logger.info("Handling missing values and duplicates...")
        for col in ['overview', 'tagline']:
            df[col] = df[col].replace(['No Data', ''], np.nan)
        
        # df = df.drop_duplicates()
        initial_rows = len(df)
        df = df.dropna(subset=['id', 'title'])
        df = df.dropna(thresh=10)
        dropped = initial_rows - len(df)
        if dropped > 0:
            logger.info(f"Dropped {dropped} rows due to missing critical data.")
        return df

    def finalize_schema(self, df):
        """Step 7: Reorder columns to final schema."""
        logger.info("Finalizing schema...")
        target_order = [
            'id', 'title', 'tagline', 'release_date', 'genres', 'belongs_to_collection',
            'original_language', 'budget_musd', 'revenue_musd', 'production_companies',
            'production_countries', 'vote_count', 'vote_average', 'popularity',
            'runtime', 'overview', 'spoken_languages', 'poster_path', 'cast',
            'cast_size', 'director', 'crew_size', 'profit_musd', 'roi', 'collection_name'
        ]
        
        for col in target_order:
            if col not in df.columns:
                df[col] = np.nan
        
        # Ensure we return a dataframe with only the target columns
        return df[target_order]

    def clean(self, df):
        """Orchestrate the full cleaning pipeline."""
        logger.info(f"Starting full data cleaning pipeline on {len(df)} records...")
        df = self.drop_irrelevant_columns(df)
        df = self.flatten_json_columns(df)
        df = self.convert_datatypes(df)
        df = self.calculate_financials(df)
        df = self.process_credits(df)
        df = self.handle_missing_and_duplicates(df)
        df = self.finalize_schema(df)
        logger.info(f"Cleaning complete. Final dataset has {len(df)} records.")
        return df

    def run(self, input_path, output_path):
        df = self.load_data(input_path)
        df_cleaned = self.clean(df)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df_cleaned.to_csv(output_path, index=False)
        logger.info(f"Cleaned data saved to {output_path}")
        return df_cleaned
