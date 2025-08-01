import pandas as pd
import pymysql
from sqlalchemy import create_engine, text

# Step 1: Ensure database exists
temp_engine = create_engine("mysql+pymysql://root:Maha2301##@localhost/")
with temp_engine.connect() as conn:
    conn.execute(text("CREATE DATABASE IF NOT EXISTS video_game_db;"))
    print("✅ Database 'video_game_db' ensured.")

# Step 2: Load CSVs
games_df = pd.read_csv("cleaned_games.csv")
sales_df = pd.read_csv("cleaned_vgsales.csv")

# Step 3: Normalize titles (important for joining)
games_df["game_title"] = games_df["game_title"].str.strip().str.lower()
sales_df["title"] = sales_df["title"].str.strip().str.lower()

# Step 4: Create game_id using merged dataframe
merged_df = pd.merge(games_df, sales_df, left_on="game_title", right_on="title", how="inner")
merged_df.reset_index(drop=True, inplace=True)
merged_df["game_id"] = merged_df.index + 1  # start IDs from 1

# Step 5: Add game_id back to original dataframes
games_df = pd.merge(games_df, merged_df[["game_title", "game_id"]], on="game_title", how="left")
sales_df = pd.merge(sales_df, merged_df[["title", "game_id"]], on="title", how="left")

# Step 6: Upload to MySQL
engine = create_engine("mysql+pymysql://root:Maha2301##@localhost/video_game_db")

games_df.to_sql("games", con=engine, if_exists="replace", index=False)
sales_df.to_sql("sales", con=engine, if_exists="replace", index=False)
merged_df.to_sql("merged_data", con=engine, if_exists="replace", index=False)

print("✅ Tables 'games', 'sales', and 'merged_data' uploaded successfully.")

# Step 7: Create merged SQL view using game_id
create_view_sql = """
CREATE OR REPLACE VIEW merged_view AS
SELECT 
    g.game_id,
    g.game_title,
    g.genre,
    g.platform,
    g.publisher,
    g.developer,
    g.release_date,
    g.rating,
    g.wishlist,
    g.number_of_reviews,
    g.average_playtime,
    s.global_sales,
    s.na_sales,
    s.eu_sales,
    s.jp_sales,
    s.other_sales
FROM games g
JOIN sales s ON g.game_id = s.game_id;
"""

with engine.connect() as conn:
    conn.execute(text(create_view_sql))
    print("✅ SQL view 'merged_view' created successfully.")
