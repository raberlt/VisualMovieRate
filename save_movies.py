import os
import json
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["moviemanagement"]
collection = db["movies"]

DATA_FOLDER = "data/processed"

start_year = 2021
end_year = 2025

def save_movies(year):
    """Lưu dữ liệu từ file filtered_{year}.json vào MongoDB với tiến trình phần trăm"""
    filename = f"filtered_{year}.json"
    file_path = os.path.join(DATA_FOLDER, filename)

    if not os.path.exists(file_path):
        print(f"⚠️ Không tìm thấy file dữ liệu: {filename}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        movies = json.load(f)

    total_movies = len(movies)
    if total_movies == 0:
        print(f"⚠️ Không có phim nào để lưu cho năm {year}!")
        return

    print(f"📥 Bắt đầu lưu {total_movies} phim từ {filename} vào MongoDB...\n")

    updated_count = 0
    inserted_count = 0

    for index, movie in enumerate(movies, start=1):
        movie["year"] = year  
        
        result = collection.update_one(
            {"title": movie["title"], "year": movie["year"]},
            {"$set": movie},
            upsert=True  # Tránh trùng lặp dữ liệu
        )

        if result.matched_count > 0:
            updated_count += 1
            status = "Cập nhật"
        else:
            inserted_count += 1
            status = "Thêm mới"

        # Tính phần trăm tiến trình
        percent = (index / total_movies) * 100
        print(f"🔄 {index}/{total_movies} ({percent:.2f}%) - {status}: {movie['title']}")

    print(f"\n✅ Năm {year}: Đã lưu {total_movies} phim (Cập nhật: {updated_count}, Thêm mới: {inserted_count})!\n")


if __name__ == "__main__":
    for year in range(start_year, end_year + 1):
        save_movies(year)

    print("🎬 Hoàn thành lưu dữ liệu!")
