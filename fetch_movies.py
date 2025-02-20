import os
import requests
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Load biến môi trường từ .env
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")
MONGO_URI = os.getenv("MONGO_URI")

# Kết nối MongoDB
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
db = client["moviemanagement"]
collection = db["airing_today"]
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

url = "https://api.themoviedb.org/3/tv/airing_today?language=en-US&page=1"
response = requests.get(url, headers=headers)
data = response.json()
# print(data)

if "results" in data:
    collection.insert_many(data["results"])
    print("Dữ liệu đã được lưu vào MongoDB.")
else:
    print("Không có dữ liệu để lưu.")

# # Hàm lấy danh sách phim phổ biến
# def fetch_popular_movies(page=1):
#     url = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=en-US&page={page}"
#     response = requests.get(url)
#     if response.status_code == 200:
#         return response.json().get("results", [])
#     return "sao"

# # Lưu dữ liệu vào MongoDB (tránh lưu trùng)
# def save_to_mongo(movies):
#     for movie in movies:
#         if not collection.find_one({"id": movie["id"]}):  # Kiểm tra phim đã tồn tại chưa
#             collection.insert_one(movie)
#     print(f"✅ Đã lưu {len(movies)} phim vào MongoDB.")

# Chạy chương trình
# if __name__ == "__main__":
    # movies = fetch_popular_movies(page=1)  # Lấy danh sách phim trang 1
    # save_to_mongo(movies)
