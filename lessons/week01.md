# Week 01 - Cài đặt và chạy

Bài học dùng OpenCV và NumPy để đọc ảnh, chuyển ảnh sang grayscale, cắt ROI
và lưu kết quả.

## 1. Tạo môi trường Python

Chạy các lệnh sau từ thư mục gốc của dự án:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

Trên Windows PowerShell, kích hoạt môi trường bằng:

```powershell
.\.venv\Scripts\Activate.ps1
```

## 2. Cài thư viện

Cài OpenCV và NumPy:

```bash
python -m pip install opencv-python numpy
```

Nếu chạy trên Linux và gặp lỗi `ImportError: libGL.so.1: cannot open shared
object file`, cài thư viện hệ thống còn thiếu:

```bash
sudo apt-get update
sudo apt-get install -y libgl1
```

Nếu không cần mở cửa sổ ảnh bằng các hàm như `cv2.imshow`, có thể dùng bản
headless thay cho `opencv-python`. Không cài đồng thời hai bản OpenCV:

```bash
python -m pip uninstall -y opencv-python
python -m pip install opencv-python-headless numpy
```

## 3. Chạy bài học

Từ thư mục gốc dự án, khi môi trường `.venv` đã được kích hoạt:

```bash
python lessons/week01.py
```

Ảnh dữ liệu mẫu sẽ được tạo trong `data/raw/` nếu chưa có. Kết quả được lưu
trong `outputs/week01/`. Hai thư mục này được `.gitignore` bỏ qua vì chứa dữ
liệu và ảnh sinh ra khi chạy bài.
