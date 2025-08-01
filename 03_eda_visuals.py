import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load merged dataset
df = pd.read_csv("merged_games_sales.csv")

# Clean genre field for grouping
df['genres'] = df['genres'].fillna('unknown')

# 1. Ratings vs Global Sales
sns.scatterplot(x='rating', y='global_sales', data=df)
plt.title("User Rating vs Global Sales")
plt.xlabel("Rating")
plt.ylabel("Global Sales (millions)")
plt.grid(True)
plt.show()

# 2. Top Genres by Global Sales
top_genres = df.groupby('genres')['global_sales'].sum().sort_values(ascending=False).head(10)
top_genres.plot(kind='bar', color='teal', title='Top Genres by Global Sales')
plt.xlabel("Genre")
plt.ylabel("Total Sales (millions)")
plt.xticks(rotation=45)
plt.grid(True)
plt.show()

# 3. Wishlist vs Global Sales
sns.regplot(x='wishlist', y='global_sales', data=df)
plt.title("Wishlist vs Global Sales")
plt.xlabel("Wishlist Count")
plt.ylabel("Global Sales (millions)")
plt.grid(True)
plt.show()

# 4. Plays per Genre
plays_genre = df.groupby('genres')['plays'].mean().sort_values(ascending=False).head(10)
plays_genre.plot(kind='bar', color='coral', title='Average Plays per Genre')
plt.ylabel("Average Plays")
plt.xlabel("Genre")
plt.xticks(rotation=45)
plt.grid(True)
plt.show()
