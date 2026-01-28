import pandas as pd

class MovieAnalyzer:
    def __init__(self, df):
        self.df = df

    def get_ranked_movies(self, metric, ascending=False, top_n=5, filter_condition=None):
        data = self.df.copy()
        if filter_condition is not None:
            data = data[filter_condition]
        
        data = data.sort_values(by=metric, ascending=ascending).reset_index(drop=True)
        data['rank'] = data[metric].rank(method='min', ascending=ascending).astype('Int64')
        return data[['id', 'title', metric, 'rank']].head(top_n)

    def print_kpis(self):
        print("\n--- KPI Analysis ---")
        
        kpis = [
            ("Highest Revenue", 'revenue_musd', False, None),
            ("Highest Budget", 'budget_musd', False, None),
            ("Highest Profit", 'profit_musd', False, None),
            ("Lowest Profit", 'profit_musd', True, None),
            ("Highest ROI (Budget >= 10M)", 'roi', False, self.df['budget_musd'] >= 10),
            ("Lowest ROI (Budget >= 10M)", 'roi', True, self.df['budget_musd'] >= 10),
            ("Most Voted", 'vote_count', False, None),
            ("Highest Rated (Votes >= 10)", 'vote_average', False, self.df['vote_count'] >= 10),
        ]

        for title, metric, asc, cond in kpis:
            print(f"\n{title}:")
            print(self.get_ranked_movies(metric, ascending=asc, top_n=5, filter_condition=cond))

    def get_custom_search_results(self):
        """Returns a dictionary of DataFrames for specific search queries."""
        results = {}
        
        # Search 1
        mask_genre = self.df['genres'].str.contains('Science Fiction', na=False) | self.df['genres'].str.contains('Action', na=False)
        mask_actor = self.df['cast'].str.contains('Bruce Willis', na=False)
        results['bruce_willis_scifi'] = self.df[mask_genre & mask_actor].sort_values('vote_average', ascending=False)

        # Search 2
        mask_actor_2 = self.df['cast'].str.contains('Uma Thurman', na=False)
        mask_director = self.df['director'] == 'Quentin Tarantino'
        results['uma_thurman_tarantino'] = self.df[mask_actor_2 & mask_director].sort_values('runtime', ascending=True)
        
        return results

    def analyze_franchise_vs_standalone(self):
        self.df['is_franchise'] = self.df['collection_name'].notna()
        
        comparison = self.df.groupby('is_franchise').agg({
            'revenue_musd': 'mean',
            'roi': 'median',
            'budget_musd': 'mean',
            'popularity': 'mean',
            'vote_average': 'mean'
        }).rename(index={True: 'Franchise', False: 'Standalone'})
        
        return comparison

    def get_top_directors(self):
        director_stats = self.df.dropna(subset=['director']).groupby('director').agg({
            'title': 'count',
            'revenue_musd': 'sum',
            'vote_average': 'mean'
        }).rename(columns={'title': 'movie_count', 'revenue_musd': 'total_revenue', 'vote_average': 'mean_rating'})
        
        return director_stats.sort_values('total_revenue', ascending=False).head(5)

    def run(self):
        self.print_kpis()
        self.get_custom_search_results()
        self.analyze_franchise_vs_standalone()
        self.get_top_directors()
