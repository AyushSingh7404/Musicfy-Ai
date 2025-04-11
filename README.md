# Musicfy-Ai
🎧 Project Title: Musicfy AI - Mood-Based Music Recommendation System
🔍 Overview:
Musicfy AI is an end-to-end machine learning project that recommends songs based on a user's mood detected from free-text input (e.g., “I feel sad today”). The system uses sentiment analysis, feature-based artist similarity, and live song link generation via YouTube/DuckDuckGo to provide personalized song suggestions.

🛠️ Key Components:
🧠 Mood Detection (NLP):

Used VADER Sentiment Analyzer to interpret user mood from input text.

Classified mood into Happy, Sad, and Neutral.

📊 Feature Engineering & Model Building:

Extracted features like popularity, followers, and genre count from an artists.csv dataset.

Scaled the data using StandardScaler.

Built a K-Nearest Neighbors (KNN) model to recommend similar artists.

🔗 Song Link Generation:

Dynamically generated YouTube search links based on song and artist names using string formatting and DuckDuckGo scraping.

🖥️ GUI with Tkinter:

Developed a desktop interface using Python’s tkinter library.

Allowed user interaction, dynamic updates, clickable links, and image previews.

Handled events like Enter key press for smoother UX.

🎯 Deployment:

Uploaded the entire project with documentation to GitHub.

Included requirements.txt, usage instructions, and demo screenshots.

🚀 Tech Stack:
Language: Python

Libraries: Tkinter, Pandas, Scikit-learn, VaderSentiment, PIL

ML Model: K-Nearest Neighbors (KNN)

Deployment: GitHub Repository with local execution instructions

Recommendation Links: YouTube via DuckDuckGo search

Database (Optional): PostgreSQL for storing artist data
