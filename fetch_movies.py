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

all_movies = []

for year in range(2025, 2026):
    print(f"🔍 Đang lấy dữ liệu năm {year}...")
    page = 1

    while page <= 500:
        url = (f"https://api.themoviedb.org/3/discover/movie?include_adult=false"
               f"&include_video=false&language=en-US&page={page}"
               f"&primary_release_year={year}&sort_by=popularity.desc")
        
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"❌ Lỗi API ({response.status_code}) năm {year} tại trang {page}")
            break

        data = response.json()
        movies = data.get("results", [])
        all_movies.extend(movies)
        total_pages = min(data.get("total_pages", 1), 500)  # Giới hạn tối đa 500 trang
        
        print(f"📄 Trang {page} / {total_pages} | {len(movies)} phim")

        if page >= total_pages:
            break

        page += 1
        time.sleep(0.5)  # Tránh spam API

    print(f"✅ Hoàn thành năm {year}, tổng {len(all_movies)} phim đã thu thập\n")

# Lưu 
with open("data/raw/all_movies.json", "w", encoding="utf-8") as f:
    json.dump(all_movies, f, ensure_ascii=False, indent=4)

print(f"🎬 Tổng số phim thu thập được: {len(all_movies)}")
print("✅ Dữ liệu đã được lưu vào all_movies.json")
