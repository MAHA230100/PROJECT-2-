import pandas as pd
import numpy as np

# === Load raw data ===
try:
    games = pd.read_csv("games.csv")
    vgsales = pd.read_csv("vgsales.csv")
except FileNotFoundError as e:
    print(f"❌ File not found: {e}")
    exit(1)

print(f"📥 Loaded games.csv: {games.shape}")
print(f"📥 Loaded vgsales.csv: {vgsales.shape}")

# === Clean games.csv ===
if "Platform(s)" in games.columns:
    games.rename(columns={"Platform(s)": "Platform"}, inplace=True)

games = games.loc[:, ~games.columns.str.contains("^Unnamed")]
games.drop_duplicates(subset="Title", inplace=True)
games = games[games["Title"].notnull()]

# Fill missing numeric columns
for col in ["Rating", "Plays", "Backlogs", "Wishlist"]:
    if col in games.columns:
        games[col] = games[col].fillna(0)
    else:
        games[col] = 0

# Fill missing categorical columns
for col in ["Genres", "Platform", "Team"]:
    if col in games.columns:
        games[col] = games[col].fillna("Unknown")
    else:
        games[col] = "Unknown"

# Format text columns
games["Genres"] = games["Genres"].str.lower().str.strip()
games["Platform"] = games["Platform"].str.upper().str.strip()
games["Team"] = games["Team"].str.title().str.strip()

# Convert dates
if "Release Date" in games.columns:
    games["Release Date"] = pd.to_datetime(games["Release Date"], errors="coerce")

# === Clean vgsales.csv ===
vgsales = vgsales.loc[:, ~vgsales.columns.str.contains("^Unnamed")]
vgsales.drop_duplicates(subset="Name", inplace=True)

# Fill numeric columns
for col in ["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales", "Global_Sales"]:
    if col in vgsales.columns:
        vgsales[col] = vgsales[col].fillna(0)
    else:
        vgsales[col] = 0

# Fill Publisher
if "Publisher" in vgsales.columns:
    vgsales["Publisher"] = vgsales["Publisher"].fillna("Unknown")
else:
    vgsales["Publisher"] = "Unknown"

# Format text columns
if "Genre" in vgsales.columns:
    vgsales["Genre"] = vgsales["Genre"].str.lower().str.strip()

if "Platform" in vgsales.columns:
    vgsales["Platform"] = vgsales["Platform"].str.upper().str.strip()

# Convert Year to numeric
if "Year" in vgsales.columns:
    vgsales["Year"] = pd.to_numeric(vgsales["Year"], errors="coerce")

# === Merge cleaned datasets ===
games["Title"] = games["Title"].str.strip().str.lower()
vgsales["Name"] = vgsales["Name"].str.strip().str.lower()

merged_df = pd.merge(
    games, vgsales,
    left_on=["Title", "Platform"],
    right_on=["Name", "Platform"],
    how="inner"
)

merged_df.drop(columns=["Name"], inplace=True)

print(f"🔗 Merged dataset created: {merged_df.shape[0]} records")

# === Save cleaned outputs ===
games.to_csv("cleaned_games.csv", index=False)
vgsales.to_csv("cleaned_vgsales.csv", index=False)
merged_df.to_csv("merged_games_sales.csv", index=False)

print("✅ Cleaning complete. Files saved:")
print(" - cleaned_games.csv")
print(" - cleaned_vgsales.csv")
print(" - merged_games_sales.csv")
