import pandas as pd
from sqlalchemy import create_engine, text
import pymysql

# DB credentials
DB_USER = "root"
DB_PASS = "Maha2301##"
DB_HOST = "localhost"
DB_NAME = "video_game_db"

# Create DB if not exists
engine_temp = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/")
with engine_temp.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};"))
print("✅ Database ready.")

# Load CSVs
try:
    games_df = pd.read_csv("cleaned_games.csv")
    sales_df = pd.read_csv("cleaned_vgsales.csv")
except Exception as e:
    print("❌ Error loading CSVs:", e)
    exit(1)

# Rename title columns
game_col = next((col for col in ["name", "title", "Title"] if col in games_df.columns), None)
sales_col = next((col for col in ["title", "Name"] if col in sales_df.columns), None)

if not game_col or not sales_col:
    print("❌ Required title columns not found.")
    print("📌 Games cols:", games_df.columns.tolist())
    print("📌 Sales cols:", sales_df.columns.tolist())
    exit(1)

games_df.rename(columns={game_col: "game_title"}, inplace=True)
sales_df.rename(columns={sales_col: "game_title"}, inplace=True)

# Normalize titles
games_df["game_title"] = games_df["game_title"].str.strip().str.lower()
sales_df["game_title"] = sales_df["game_title"].str.strip().str.lower()

# Merge data
merged_df = pd.merge(games_df, sales_df, on="game_title", how="inner")
print(f"✅ Merged rows: {len(merged_df)}")

# Upload to MySQL
engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}")
try:
    games_df.to_sql("games", con=engine, if_exists="replace", index=False)
    sales_df.to_sql("sales", con=engine, if_exists="replace", index=False)
    merged_df.to_sql("merged_data", con=engine, if_exists="replace", index=False)
    print("✅ Tables uploaded.")
except Exception as e:
    print("❌ Upload failed:", e)
    exit(1)

# Create view
view_sql = """
CREATE OR REPLACE VIEW merged_view AS
SELECT
    g.*,
    s.global_sales,
    s.na_sales,
    s.eu_sales,
    s.jp_sales,
    s.other_sales
FROM games g
JOIN sales s ON g.game_title = s.game_title;
"""

try:
    with engine.connect() as conn:
        conn.execute(text(view_sql))
    print("✅ View created.")
except Exception as e:
    print("❌ View creation failed:", e)
