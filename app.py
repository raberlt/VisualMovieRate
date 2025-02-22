from flask import Flask, render_template, jsonify
import os
import json

app = Flask(__name__)

# Thư mục chứa dữ liệu đã xử lý
DATA_FOLDER = "data/processed"


def load_top_movies(year=2015):
    """Tải top 10 phim có độ phổ biến cao nhất trong năm chỉ định."""
    file_path = os.path.join(DATA_FOLDER, f"filtered_{year}.json")
    print(f"Đang kiểm tra tệp: {file_path}")  # In đường dẫn tệp để kiểm tra

    if not os.path.exists(file_path):
        print("❌ Tệp không tồn tại!")
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        movies = json.load(f)

    if not movies:
        print("❌ Dữ liệu trong tệp JSON rỗng!")
        return []

    # Sắp xếp theo độ phổ biến và lấy 10 phim đầu
    top_movies = sorted(movies, key=lambda x: x.get("popularity", 0), reverse=True)[:10]
    
    print(f"✅ Tải thành công {len(top_movies)} phim!")
    return top_movies


@app.route("/")
def index():
    top_movies_2015 = load_top_movies(2015)
    print(top_movies_2015)  # Kiểm tra dữ liệu trong terminal
    return render_template("index.html", movies=top_movies_2015)


@app.route("/api/movies/2015")
def api_movies_2015():
    """API trả về danh sách top 10 phim phổ biến năm 2015."""
    return jsonify(load_top_movies(2015))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
