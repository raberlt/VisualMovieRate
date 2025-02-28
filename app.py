from flask import Flask, render_template, jsonify
from datetime import datetime
from collections import Counter

import os
import json
import threading
import time

app = Flask(__name__)

DATA_FOLDER = "data/processed"
current_year = datetime.now().year

# Biến lưu cache dữ liệu
cached_data = {
    "top_movies": [],
    "ratings": [],
    "rating_trend": {},
    "scatter_data": [],
    "genre_count": {},
    "genre_ratings": {}
}

# Hàm tải dữ liệu (cập nhật lại dữ liệu trong cache)
def update_data():
    global cached_data
    while True:
        print("🔄 Cập nhật dữ liệu mới...")
        cached_data["top_movies"] = load_top_movies()
        cached_data["ratings"] = load_ratings()
        cached_data["rating_trend"] = load_rating_trend()
        cached_data["scatter_data"] = load_scatter_data()
        cached_data["genre_count"] = count_movies_by_genre()
        cached_data["genre_ratings"] = load_genre_ratings()
        print("✅ Dữ liệu đã cập nhật!")
        time.sleep(30)  # Cập nhật lại sau 30 giây

# Chạy cập nhật dữ liệu trong background
update_thread = threading.Thread(target=update_data, daemon=True)
update_thread.start()

# Các hàm load dữ liệu
def load_top_movies():
    all_movies = []
    for year in range(2015, current_year + 1):
        file_path = os.path.join(DATA_FOLDER, f"filtered_{year}.json")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                all_movies.extend(json.load(f))
    
    top_movies = sorted(all_movies, key=lambda x: x.get("popularity", 0), reverse=True)[:10]
    return top_movies

def load_ratings():
    all_ratings = []
    for year in range(2015, current_year + 1):
        file_path = os.path.join(DATA_FOLDER, f"filtered_{year}.json")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                all_ratings.extend([movie["vote_average"] for movie in json.load(f) if "vote_average" in movie])
    return all_ratings

def load_rating_trend():
    rating_trend = {}
    for year in range(2015, current_year + 1):
        file_path = os.path.join(DATA_FOLDER, f"filtered_{year}.json")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                ratings = [movie["vote_average"] for movie in json.load(f) if "vote_average" in movie]
                if ratings:
                    rating_trend[year] = sum(ratings) / len(ratings)
    return rating_trend

def load_scatter_data():
    scatter_data = []
    for year in range(2015, current_year + 1):
        file_path = os.path.join(DATA_FOLDER, f"filtered_{year}.json")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                scatter_data.extend([
                    {"popularity": movie["popularity"], "vote_average": movie["vote_average"]}
                    for movie in json.load(f) if "popularity" in movie and "vote_average" in movie
                ])
    return scatter_data

def count_movies_by_genre():
    genre_count = Counter()
    for year in range(2015, current_year + 1):
        file_path = os.path.join(DATA_FOLDER, f"filtered_{year}.json")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                movies = json.load(f)
                for movie in movies:
                    for genre in set(movie.get("genres", [])):  # Dùng set để tránh trùng lặp trong cùng 1 phim
                        genre_count[genre] += 1
    print(dict(genre_count))
    return dict(genre_count)

def load_genre_ratings():
    genre_ratings = {}
    for year in range(2015, current_year + 1):
        file_path = os.path.join(DATA_FOLDER, f"filtered_{year}.json")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                movies = json.load(f)
                for movie in movies:
                    rating = movie.get("vote_average")
                    if rating is not None:
                        for genre in set(movie.get("genres", [])):
                            if genre not in genre_ratings:
                                genre_ratings[genre] = []
                            genre_ratings[genre].append(rating)
    return genre_ratings

@app.route("/")
def index():
    return render_template("index.html", 
        movies=cached_data["top_movies"],
        ratings=cached_data["ratings"],
        rating_trend=cached_data["rating_trend"],
        scatter_data=cached_data["scatter_data"],
        count_movies_by_genre=cached_data["genre_count"],
        genre_ratings=cached_data["genre_ratings"]       
    )

@app.route("/api/movies")
def api_movies():
    return jsonify(cached_data["top_movies"])

@app.route("/api/ratings")
def api_ratings():
    return jsonify(cached_data["ratings"])

@app.route("/api/rating-trend")
def api_rating_trend():
    return jsonify(cached_data["rating_trend"])

@app.route("/api/scatter")
def api_scatter():
    return jsonify(cached_data["scatter_data"])

@app.route("/api/genre-count")
def api_genre_count():
    return jsonify(cached_data["genre_count"])

@app.route("/api/genre-ratings")
def api_genre_ratings():
    return jsonify(cached_data["genre_ratings"])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
