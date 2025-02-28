import json
import os

data_dir = "data"
raw_dir = os.path.join(data_dir, "raw")
processed_dir = os.path.join(data_dir, "processed")

os.makedirs(raw_dir, exist_ok=True)
os.makedirs(processed_dir, exist_ok=True)

genre_dict = {
    28: "Action", 12: "Adventure", 16: "Animation", 35: "Comedy", 80: "Crime",
    99: "Documentary", 18: "Drama", 10751: "Family", 14: "Fantasy", 36: "History",
    27: "Horror", 10402: "Music", 9648: "Mystery", 10749: "Romance",
    878: "Science Fiction", 10770: "TV Movie", 53: "Thriller", 10752: "War", 37: "Western"
}

years = range(2015, 2026)

for year in years:
    input_file = os.path.join(raw_dir, f"{year}.json")
    output_file = os.path.join(processed_dir, f"filtered_{year}.json")

    if not os.path.exists(input_file):
        print(f"⚠️ Không tìm thấy {input_file}, bỏ qua.")
        continue

    with open(input_file, "r", encoding="utf-8") as f:
        movies = json.load(f)
# lọc 
    filtered_movies = []
    for movie in movies:
        filtered_movies.append({
            "title": movie.get("title"),
            "overview": movie.get("overview"),
            "release_date": movie.get("release_date"),
            "popularity": movie.get("popularity"),
            "vote_average": movie.get("vote_average"),
            "vote_count": movie.get("vote_count"),
            "genres": [genre_dict.get(gid, "Unknown") for gid in movie.get("genre_ids", [])]
        })

    # lưu folder processed
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(filtered_movies, f, ensure_ascii=False, indent=4)

    print(f" Đã xử lý {len(filtered_movies)} phim từ {year} và lưu vào {output_file}")
