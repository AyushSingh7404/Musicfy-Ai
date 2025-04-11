import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
import psycopg2
import webbrowser
from urllib.request import urlopen
from PIL import Image, ImageTk
from io import BytesIO
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Database Connection
DB_CONFIG = {
    "dbname": "musicfy_db",
    "user": "your_username",
    "password": "your_password",
    "host": "localhost",
    "port": "5432"
}

def connect_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
        return None

# Load Artists Dataset
artists_df = pd.read_csv("artists.csv")

# Feature Extraction from Artists Data
def extract_artist_features():
    artists_df['followers'] = artists_df['followers'].fillna(0)
    artists_df['popularity'] = artists_df['popularity'].fillna(0)
    artists_df['genre_count'] = artists_df['genres'].apply(lambda x: len(eval(x)) if x != "[]" else 0)
    return artists_df[['name', 'followers', 'popularity', 'genre_count']]

artist_features = extract_artist_features()

# Sentiment Analysis for Mood Detection
analyzer = SentimentIntensityAnalyzer()
def detect_mood(text):
    sentiment = analyzer.polarity_scores(text)
    if sentiment['compound'] >= 0.05:
        return "Happy"
    elif sentiment['compound'] <= -0.05:
        return "Sad"
    else:
        return "Neutral"

# Recommendation System using KNN
scaler = StandardScaler()
feature_columns = ['followers', 'popularity', 'genre_count']
artist_scaled = scaler.fit_transform(artist_features[feature_columns])
knn = NearestNeighbors(n_neighbors=10, metric='euclidean')  # Recommend 10 songs
knn.fit(artist_scaled)

def recommend_songs(mood):
    if mood == "Happy":
        target_features = [500000, 80, 3]
    elif mood == "Sad":
        target_features = [20000, 40, 1]
    else:
        target_features = [100000, 60, 2]
    
    distances, indices = knn.kneighbors([target_features])
    return artist_features.iloc[indices[0]][['name', 'followers', 'popularity']]

# Generate YouTube Search Links
def get_youtube_link(song, artist):
    return f"https://www.youtube.com/results?search_query={song.replace(' ', '+')}+-+{artist.replace(' ', '+')}"

def get_preview_image(song, artist):
    search_url = f"https://img.youtube.com/vi/{song.replace(' ', '+')}_{artist.replace(' ', '+')}/hqdefault.jpg"
    try:
        img_data = urlopen(search_url).read()
        img = Image.open(BytesIO(img_data))
        return ImageTk.PhotoImage(img)
    except:
        return None

# Tkinter UI Setup
root = tk.Tk()
root.title("Musicfy AI - Mood-Based Song Recommendation")
root.geometry("800x600")
root.configure(bg="#1E1E1E")

# UI Elements
label = tk.Label(root, text="Enter your mood (e.g., 'I feel happy today!')", font=("Arial", 12), fg="white", bg="#1E1E1E")
label.pack(pady=10)

entry = tk.Entry(root, width=50, bg="#333", fg="white", font=("Arial", 12))
entry.pack(pady=10)
entry.bind("<Return>", lambda event: on_recommend())

def on_recommend():
    user_mood_text = entry.get()
    detected_mood = detect_mood(user_mood_text)
    recommendations = recommend_songs(detected_mood)
    
    for widget in link_frame.winfo_children():
        widget.destroy()
    
    for _, row in recommendations.iterrows():
        song_name = f"Song {row.name + 1}"
        artist_name = row['name']
        link = get_youtube_link(song_name, artist_name)
        img = get_preview_image(song_name, artist_name)
        
        song_button = tk.Button(link_frame, text=f"{song_name} - {artist_name}", fg="blue", cursor="hand2", font=("Arial", 12), command=lambda l=link: webbrowser.open(l))
        song_button.pack(pady=5)
        
        if img:
            img_label = tk.Label(link_frame, image=img, bg="#1E1E1E")
            img_label.image = img
            img_label.pack(pady=5)

button = ttk.Button(root, text="Recommend Songs", command=on_recommend)
button.pack(pady=10)

link_frame = tk.Frame(root, bg="#1E1E1E")
link_frame.pack()

root.mainloop()
