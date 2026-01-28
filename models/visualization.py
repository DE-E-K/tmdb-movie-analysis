import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import logging

logger = logging.getLogger(__name__)
# Suppress matplotlib category info logs when plotting numeric-like strings
logging.getLogger('matplotlib.category').setLevel(logging.WARNING)

class DataVisualizer:
    def __init__(self, df, output_dir):
        self.df = df
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Prepare data
        self.df['year'] = self.df['release_date'].dt.year
        self.df['primary_genre'] = self.df['genres'].apply(lambda x: x.split('|')[0] if isinstance(x, str) and '|' in x else x)

    def save_plot(self, filename):
        path = os.path.join(self.output_dir, filename)
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()
        logger.info(f"Saved plot: {path}")
        return path

    def plot_revenue_vs_budget(self):
        plt.figure(figsize=(10,6))
        sns.scatterplot(data=self.df, x='budget_musd', y='revenue_musd', hue='primary_genre', alpha=0.6, legend=False)
        plt.title('Revenue vs. Budget Trends')
        plt.xlabel('Budget (Million USD)')
        plt.ylabel('Revenue (Million USD)')
        plt.grid(True, alpha=0.3)
        return self.save_plot("Revenue_vs_Budget.png")

    def plot_roi_distribution(self):
        plt.figure(figsize=(12,6))
        top_genres = self.df['primary_genre'].value_counts().head(10).index
        sns.boxplot(data=self.df[self.df['primary_genre'].isin(top_genres)], x='primary_genre', y='roi')
        plt.title('ROI Distribution by Top 10 Genres')
        plt.xticks(rotation=45)
        plt.ylim(-1, 10)
        return self.save_plot("ROI_Distribution_by_Genre.png")

    def plot_popularity_vs_rating(self):
        plt.figure(figsize=(10,6))
        sns.scatterplot(data=self.df, x='vote_average', y='popularity', alpha=0.6)
        plt.title('Popularity vs. Rating')
        plt.xlabel('Vote Average')
        plt.ylabel('Popularity')
        plt.grid(True, alpha=0.3)
        return self.save_plot("Popularity_vs_Rating.png")

    def plot_yearly_trends(self):
        plt.figure(figsize=(12,6))
        yearly_rev = self.df.groupby('year')['revenue_musd'].sum().reset_index()
        sns.lineplot(data=yearly_rev, x='year', y='revenue_musd', marker='o')
        plt.title('Yearly Trends in Box Office Revenue')
        plt.xlabel('Year')
        plt.ylabel('Total Revenue (Million USD)')
        plt.grid(True, alpha=0.3)
        return self.save_plot("Yearly_Box_Office_Trends.png")

    def plot_franchise_comparison(self):
        self.df['is_franchise'] = self.df['collection_name'].notna()
        comp = self.df.groupby('is_franchise')['revenue_musd'].mean().reset_index()
        comp['Type'] = comp['is_franchise'].map({True: 'Franchise', False: 'Standalone'})
        
        plt.figure(figsize=(8,6))
        sns.barplot(data=comp, x='Type', y='revenue_musd', hue='Type', palette='viridis', legend=False)
        plt.title('Average Revenue: Franchise vs Standalone')
        plt.ylabel('Average Revenue (Million USD)')
        plt.xlabel('')
        return self.save_plot("Franchise_vs_Standalone.png")

    def plot_roi_by_genre(self):
        plt.figure(figsize=(12, 6))
        
        # Calculate ROI if not present
        if 'roi' not in self.df.columns:
            self.df['roi'] = self.df['revenue_musd'] / self.df['budget_musd']
            
        # Group by genre (using the string column as requested by user snippet)
        # Note: This groups by the full genre string. If distinct genres are needed, use explode.
        # User snippet: df_clean.groupBy("genres").agg(F.mean("roi").alias("mean_roi"))
        roi_genre = self.df.groupby("genres")['roi'].mean().reset_index(name="mean_roi").sort_values('mean_roi', ascending=False)
        
        # Using seaborn barplot for consistent coloring
        ax = sns.barplot(x=roi_genre['mean_roi'], 
                        y=roi_genre['genres'], color='#eb5d19',
                        orient='h')

        for container in ax.containers:
            ax.bar_label(container, fmt='%.2f', padding=3, rotation=0, fontsize=9)
            
        plt.title('Total ROI by Genre', fontsize=30, pad=20)
        plt.xlabel('Mean ROI') 
        plt.tight_layout()
        return self.save_plot("ROI_by_Genre.png")

    def plot_revenue_vs_budget_yearly(self):
        # Aggregate Revenue and Budget by Year
        pdf_rev_bud = self.df.groupby('year')[['revenue_musd', 'budget_musd']].sum().rename(
            columns={'revenue_musd': 'Total Revenue', 'budget_musd': 'Total Budget'}).reset_index()

        # Ensure year is integer for cleaner plotting
        pdf_rev_bud['year'] = pdf_rev_bud['year'].astype(int)

        pdf_melted = pdf_rev_bud.melt(id_vars='year', value_vars=['Total Revenue', 'Total Budget'], 
                                                     var_name='Type', value_name='Amount')
                
        # Renaissance mapping for legend to match Pandas "Revenue" and "Budget"
        pdf_melted['Type'] = pdf_melted['Type'].replace({'Total Revenue': 'Revenue', 'Total Budget': 'Budget'})

        plt.figure(figsize=(12, 6))
        ax = sns.barplot(data=pdf_melted, x='year', y='Amount', hue='Type', palette=['#eb5d19', 'darkgray'])

        for container in ax.containers:
            ax.bar_label(container, fmt='%.1f', padding=3, rotation=0, fontsize=9)
            
        plt.title('Revenue vs Budget Over Years', fontsize=30, pad=20)
        plt.xlabel('Year')
        plt.ylabel('Amount (Million USD)')
        plt.legend(title='Type')
        plt.tight_layout()
        return self.save_plot("Revenue_vs_Budget_Yearly.png")

    def run(self):
        logger.info("\n--- Generating Visualizations ---")
        self.plot_revenue_vs_budget()
        self.plot_roi_distribution()
        self.plot_popularity_vs_rating()
        self.plot_yearly_trends()
        self.plot_franchise_comparison()
        self.plot_roi_by_genre()
        self.plot_revenue_vs_budget_yearly()
