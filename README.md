# Movie Review & Rating API

## Giới thiệu
Dự án này cung cấp một website trực quan quản lý và phân tích dữ liệu đánh giá phim, sử dụng **Python**, **Flask** và **MongoDB** ...

## Hướng Dẫn Cài Đặt và Chạy Dự Án

### 1. Clone Dự Án
```sh
git clone <repository-url>
cd <project-folder>
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
Mở file `.env` và cập nhật giá trị phù hợp.

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

## Liên hệ
Nếu có vấn đề, vui lòng mở **issue** hoặc liên hệ qua email.

