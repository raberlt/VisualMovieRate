# Movie Review & Rating API

## Giới thiệu
Dự án này cung cấp một website trực quan phân tích dữ liệu đánh giá phim, sử dụng **Python**, **Flask** và **MongoDB**. Dữ liệu được lấy từ gần 100.000 bộ phim phổ biến 
trong 10 năm trở lại đây (từ 2015-2025) từ web [TMDB](https://www.themoviedb.org/).

## Hướng Dẫn Cài Đặt và Chạy Dự Án

### 1. Clone Dự Án
```sh
git clone https://github.com/raberlt/VisualMovieRate
cd VisualMovieRate
```

### 2. Tạo và Kích Hoạt Môi Trường Ảo
```sh
python -m venv myenv
source myenv/bin/activate  # Trên macOS/Linux
myenv\\Scripts\\activate  # Trên Windows
```

### 3. Cài Đặt Thư Viện Cần Thiết
```sh
pip install -r requirements.txt
```

### 4. Cấu Hình Biến Môi Trường
```sh
cp .env_example .env  # Trên macOS/Linux
copy .env_example .env  # Trên Windows
```

### 5. Chạy Ứng Dụng
```sh
python app.py
```

### 6. Truy Cập Ứng Dụng
Mở trình duyệt và truy cập:
```
http://127.0.0.1:5000
```

## Ghi chú
- Đảm bảo **MongoDB** đang chạy trên máy hoặc kết nối đúng URI.
- Nếu gặp lỗi, kiểm tra lại **biến môi trường** trong file `.env`.
- Tìm hiểu thêm [TMDB_API_DOCUMENT](https://developer.themoviedb.org/docs/getting-started)
  

## Liên hệ
Nếu có vấn đề, vui lòng mở issue hoặc liên hệ qua email [Nguyễn Đại Phát](mailto:21010625@st.phenikaa-uni.edu.vn)

