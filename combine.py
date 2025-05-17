import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns


house_csv = "house.csv"
gold_csv = "gold.csv"

# Load the CSVs
house_df = pd.read_csv(house_csv)
gold_df = pd.read_csv(gold_csv)


house_df[house_df.columns[0]]  =   pd.to_datetime(house_df[house_df.columns[0]]).dt.to_period('M')
gold_df[house_df.columns[0]]   =   pd.to_datetime(gold_df[gold_df.columns[0]]).dt.to_period('M')

# Merge on Date
common_column = house_df.columns[0]
merged_df = pd.merge(house_df, gold_df, on=common_column , how='inner')

# Get column names by position
house_price_col = merged_df.columns[1]  # This gives "house_price"
gold_per_oz_col = merged_df.columns[2]  # This gives "gold_per_oz"

# Now use these column names to reference the actual data columns
merged_df['house_per_oz'] = merged_df[house_price_col] / merged_df[gold_per_oz_col]

# Plot
sns.set_theme(style="darkgrid")
plt.figure(figsize=(14, 6))
merged_df['Date'] = merged_df['Date'].dt.to_timestamp()
sns.lineplot(data=merged_df, x='Date', y='house_per_oz', color='gold', 
             label='House Price in Gold (oz)')
# Format title and labels
plt.title('US Median House Price in Ounces of Gold (1963–2025)', fontsize=16)
plt.xlabel('Year', fontsize=12)
plt.ylabel('House Price (oz of Gold)', fontsize=12)

# Format x-axis to show only the year, every N years
ax = plt.gca()
ax.xaxis.set_major_locator(mdates.YearLocator(base=5))  # one tick every 5 years
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))  # show only the year
plt.xticks(rotation=45)

# Add source note
plt.text(
    x=1, y=0,
    s="Source: St Louis Federal Reserve - Median House Price data",
    ha='right', va='bottom',
    transform=ax.transAxes,
    fontsize=9, color='gray'
)

plt.tight_layout()
plt.grid(True)
plt.legend()
plt.show()