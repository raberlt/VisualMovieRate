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

def save_movies_to_mongo():
    """Lưu dữ liệu từ các file JSON filtered_xxxx vào MongoDB"""
    for filename in os.listdir(DATA_FOLDER):
        if filename.startswith("filtered_") and filename.endswith(".json"):
            year = filename.replace("filtered_", "").replace(".json", "")
            print(year)
            file_path = os.path.join(DATA_FOLDER, filename)

            with open(file_path, "r", encoding="utf-8") as f:
                movies = json.load(f)
                for movie in movies:
                    movie["year"] = int(year)  # Thêm thông tin năm vào dữ liệu
                    collection.update_one(
                        {"title": movie["title"], "year": movie["year"]},
                        {"$set": movie},
                        upsert=True  # Tránh trùng lặp dữ liệu
                    )
            
            print(f"✅ Đã lưu {len(movies)} phim từ {filename} vào MongoDB")

if __name__ == "__main__":
    save_movies_to_mongo()
    print("🎬 Hoàn thành lưu dữ liệu vào MongoDB!")
