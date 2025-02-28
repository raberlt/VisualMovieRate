import os
import requests
import json
import time
from dotenv import load_dotenv

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {TMDB_API_KEY}"
}

file_path = "data/raw/2025.json"

# Đọc dữ liệu hiện có
if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        try:
            existing_movies = json.load(f)
        except json.JSONDecodeError:
            existing_movies = []
else:
    existing_movies = []

# Tạo dictionary để dễ cập nhật
existing_movie_dict = {movie["id"]: movie for movie in existing_movies}

years_to_fetch = [2025]  # Các năm cần cập nhật

for year in years_to_fetch:
    print(f"\n🔍 Đang cập nhật dữ liệu năm {year}...")
    page = 1

    while page <= 1:
        url = (f"https://api.themoviedb.org/3/discover/movie?include_adult=false"
               f"&include_video=false&language=en-US&page={page}"
               f"&primary_release_year={year}&sort_by=popularity.desc")
        
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"❌ Lỗi API ({response.status_code}) năm {year} tại trang {page}")
            break

        data = response.json()
        movies = data.get("results", [])

        updated_movies_list = []
        new_movies_list = []

        for movie in movies:
            movie_id = movie["id"]
            movie_title = movie["title"]

            if movie_id in existing_movie_dict:
                # Cập nhật thông tin phim đã có
                existing_movie_dict[movie_id].update(movie)
                updated_movies_list.append(movie_title)
            else:
                # Thêm phim mới nếu chưa có
                existing_movie_dict[movie_id] = movie
                new_movies_list.append(movie_title)

        total_pages = min(data.get("total_pages", 1), 500)  
        progress = (page / total_pages) * 100

        print(f"\n📄 Trang {page}/{total_pages} ({progress:.2f}%)")
        if updated_movies_list:
            print(f"🔄 Cập nhật: {len(updated_movies_list)} phim")
            for title in updated_movies_list:
                print(f"  - {title}")
        
        if new_movies_list:
            print(f"➕ Thêm mới: {len(new_movies_list)} phim")
            for title in new_movies_list:
                print(f"  - {title}")

        if page >= total_pages:
            break

        page += 1
        time.sleep(0.5)  # Tránh spam API

    print(f"\n✅ Hoàn thành cập nhật năm {year}")

# Ghi lại dữ liệu đã cập nhật
updated_movies = list(existing_movie_dict.values())

with open(file_path, "w", encoding="utf-8") as f:
    json.dump(updated_movies, f, ensure_ascii=False, indent=4)

print(f"\n🎬 Đã cập nhật thông tin của {len(updated_movies)} phim trong {file_path}")
