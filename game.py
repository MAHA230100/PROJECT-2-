import pandas as pd
import mysql.connector

try:
    # Connect to MySQL
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Maha2301##',
        database='game_db'
    )
    cursor = conn.cursor()

    # Load and clean the CSV
    games = pd.read_csv('games.csv')
    if 'Unnamed: 0' in games.columns:
        games = games.drop(columns=['Unnamed: 0'])
    if 'game_id' in games.columns:
        games = games.drop(columns=['game_id'])
        

    # Build INSERT SQL
    cols = ", ".join(f"`{col}`" for col in games.columns)
    placeholders = ", ".join(["%s"] * len(games.columns))
    sql = f"INSERT INTO Game ({cols}) VALUES ({placeholders})"

    for row in games.itertuples(index=False, name=None):
        cursor.execute(sql, row)

    conn.commit()
    print("✅ Game data inserted successfully.")

except mysql.connector.Error as err:
    print(f"❌ MySQL Error: {err}")
except FileNotFoundError as fnf:
    print(f"❌ File not found: {fnf}")
except Exception as e:
    print(f"❌ General Error: {e}")
finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
