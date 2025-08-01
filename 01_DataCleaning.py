# video_game_cleaning.py

import pandas as pd
import numpy as np

# ========== PART 1: Load Data ========== #
games = pd.read_csv("games.csv")
vgsales = pd.read_csv("vgsales.csv")

# ========== PART 2: Initial Inspection ========== #
print("Games dataset shape:", games.shape)
print("Sales dataset shape:", vgsales.shape)

# ========== PART 3: Clean games.csv ========== #

# Rename 'Platform(s)' to 'Platform' if needed
if 'Platform(s)' in games.columns:
    games.rename(columns={'Platform(s)': 'Platform'}, inplace=True)

# Drop unnecessary columns if any exist (e.g., unnamed index columns)
games = games.loc[:, ~games.columns.str.contains('^Unnamed')]

# Drop duplicates
games.drop_duplicates(subset="Title", inplace=True)

# Remove rows where Title is missing
games = games[games['Title'].notnull()]

# Handle null values in numerical columns
num_cols = ['Rating', 'Plays', 'Backlogs', 'Wishlist']
for col in num_cols:
    if col in games.columns:
        games[col] = games[col].fillna(0)
    else:
        games[col] = 0  # Add column if missing

# Fill missing categorical values
cat_cols = ['Genres', 'Platform', 'Team']
for col in cat_cols:
    if col in games.columns:
        games[col] = games[col].fillna("Unknown")
    else:
        games[col] = "Unknown"  # Add column if missing

# Standardize text fields
games['Genres'] = games['Genres'].str.lower().str.strip()
games['Platform'] = games['Platform'].str.upper().str.strip()
games['Team'] = games['Team'].str.title().str.strip()

# Format release date
if 'Release Date' in games.columns:
    games['Release Date'] = pd.to_datetime(games['Release Date'], errors='coerce')

# ========== PART 4: Clean vgsales.csv ========== #

# Drop unnecessary columns
vgsales = vgsales.loc[:, ~vgsales.columns.str.contains('^Unnamed')]

# Drop duplicates
vgsales.drop_duplicates(subset="Name", inplace=True)

# Fill missing values for numeric columns
sales_cols = ['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']
for col in sales_cols:
    if col in vgsales.columns:
        vgsales[col] = vgsales[col].fillna(0)
    else:
        vgsales[col] = 0

# Fill missing categorical columns
if 'Publisher' in vgsales.columns:
    vgsales['Publisher'] = vgsales['Publisher'].fillna("Unknown")
if 'Genre' in vgsales.columns:
    vgsales['Genre'] = vgsales['Genre'].str.lower().str.strip()
if 'Platform' in vgsales.columns:
    vgsales['Platform'] = vgsales['Platform'].str.upper().str.strip()

# Convert Year to numeric
if 'Year' in vgsales.columns:
    vgsales['Year'] = pd.to_numeric(vgsales['Year'], errors='coerce')

# ========== PART 5: Merge Datasets ========== #

# Standardize merge keys
games['Title'] = games['Title'].str.strip().str.lower()
vgsales['Name'] = vgsales['Name'].str.strip().str.lower()

# Merge on game title and platform
merged_df = pd.merge(games, vgsales, left_on=['Title', 'Platform'], right_on=['Name', 'Platform'], how='inner')

# Drop unnecessary duplicate column
merged_df.drop(columns=["Name"], inplace=True)

# ========== PART 6: Save Cleaned Data ========== #

games.to_csv("cleaned_games.csv", index=False)
vgsales.to_csv("cleaned_vgsales.csv", index=False)
merged_df.to_csv("merged_games_sales.csv", index=False)

print("✅ Data cleaning completed. Cleaned files saved as:")
print(" - cleaned_games.csv")
print(" - cleaned_vgsales.csv")
print(" - merged_games_sales.csv")
