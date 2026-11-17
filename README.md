# 🌿 NutriSnack - Siêu Thị Trái Cây Sấy & Hạt Dinh Dưỡng Cao Cấp
> **Đồ án môn học Thương mại điện tử (TMĐT) - Hệ thống thông tin quản lý (MIS)**  
> Nền tảng: **Python 3.13 + Django 5.2 + MySQL 8.0 + VietQR Realtime**

---

## 📌 1. Giới thiệu tổng quan
NutriSnack là website thương mại điện tử chuyên cung cấp các dòng sản phẩm nông sản chế biến sâu, trái cây sấy thăng hoa âm sâu `-40°C` và hạt dinh dưỡng cao cấp.

### Các tính năng cốt lõi:
* 🛒 **Mua hàng & Giỏ hàng trực tuyến:** Quản lý giỏ hàng qua Session, tính phí ship thông minh theo khu vực (Nội thành / Tỉnh khác), miễn phí vận chuyển cho đơn từ 500.000đ.
* 📦 **Quản lý kho theo tiêu chuẩn FEFO (First-Expired, First-Out):** Tự động xuất kho từ các lô hàng có hạn dùng gần nhất trước; tự động khóa không bán các lô cận hạn dưới 30 ngày.
* 🔍 **Truy xuất nguồn gốc theo Lô hàng (Traceability):** Khách hàng nhập mã lô in trên bao bì để kiểm tra vùng trồng VietGAP, ngày đóng gói và tiêu chuẩn kiểm định.
* ⚡ **Cổng thanh toán VietQR Napas 24/7 (Vietcombank):** Tự động sinh mã VietQR chứa đúng số tiền và mã đơn hàng; hỗ trợ cơ chế nhận diện thanh toán Realtime tự động.
* 👥 **Phân quyền người dùng (Role-Based Access Control):** Admin (Toàn quyền), Sales (Quản lý đơn hàng), Warehouse (Quản lý nhập xuất lô hàng).

---

## 🚀 2. Hướng dẫn cài đặt & Chạy cho thành viên

### CÁCH 1: Chạy trực tiếp bằng Python (Khuyên dùng khi lập trình)

#### Bước 1: Sao chép mã nguồn & mở Terminal
Mở thư mục dự án trong **VS Code** (hoặc PowerShell/Terminal).

#### Bước 2: Tạo môi trường ảo & Cài đặt thư viện
```powershell
# Tạo môi trường ảo Python
python -m venv venv

# Kích hoạt môi trường ảo
.\venv\Scripts\Activate.ps1       # Trên Windows PowerShell
# (Hoặc: source venv/bin/activate  # Trên macOS / Linux)

# Cài đặt tất cả thư viện cần thiết
pip install -r requirements.txt
```

#### Bước 3: Cấu hình biến môi trường (.env)
Sao chép file mẫu `.env.example` thành `.env`:
```powershell
copy .env.example .env            # Trên Windows
# (Hoặc: cp .env.example .env      # Trên macOS / Linux)
```
> *Lưu ý: Đảm bảo dịch vụ MySQL trên máy đang chạy và kiểm tra mật khẩu MySQL trong file `.env` (mặc định user: `root`, pass: `Tun13@vn`, database: `nutrisnack_db`).*

#### Bước 4: Khởi tạo Cơ sở dữ liệu & Nạp dữ liệu mẫu
```powershell
# Chạy migration để tạo bảng
python manage.py migrate

# Nạp 18 sản phẩm chuẩn TMĐT, danh mục, lô hàng và các tài khoản mẫu
python manage.py seed_data --admin-password admin --demo-password demo1234
```

#### Bước 5: Chạy máy chủ Web
```powershell
python manage.py runserver
```
Truy cập trình duyệt tại:
* 🌐 **Cửa hàng:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
* ⚙️ **Trang Quản trị Admin:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

### CÁCH 2: Chạy 1 bước bằng Docker (Không cần cài Python hay MySQL)
Nếu máy bạn đã cài sẵn **Docker Desktop**:

1. Mở Terminal tại thư mục dự án và chạy:
   ```bash
   docker compose up -d --build
   ```
2. Docker sẽ tự động:
   - Kéo và khởi chạy container **MySQL 8.0**.
   - Build ứng dụng Django, tự động chạy migrate và nạp sẵn toàn bộ dữ liệu mẫu.
3. Mở trình duyệt tại [http://127.0.0.1:8000](http://127.0.0.1:8000).
4. Khi muốn dừng:
   ```bash
   docker compose down
   ```

---

## 🔑 3. Danh sách tài khoản mẫu để kiểm thử

| Tên đăng nhập | Mật khẩu | Vai trò | Mục đích thử nghiệm |
| :--- | :--- | :--- | :--- |
| **admin** | `DatMatKhauManh1!` | **Superuser (Quản trị viên)** | Xem toàn bộ báo cáo dashboard, điều chỉnh tồn kho, sửa thông tin sản phẩm, quản lý tài khoản. |
| *(Khách vãng lai)* | *(Không cần)* | **Khách hàng** | Đặt hàng nhanh không cần tài khoản, tra cứu đơn qua Mã đơn + SĐT. |

---

## 💳 4. Thông tin Cổng thanh toán VietQR
Hệ thống kết nối trực tiếp cổng **VietQR Napas 24/7**:
* **Ngân hàng:** Vietcombank (VCB)
* **Số tài khoản:** `1019462183`
* **Chủ tài khoản:** `PHAM THI MY TIEN`
* Khi khách đặt hàng, website tự sinh mã QR động chứa đúng số tiền và cú pháp `NS...`. Trên màn hình chi tiết đơn hàng có sẵn **Bộ lắng nghe Realtime** và nút **`⚡ Giả lập quét mã thanh toán`** phục vụ thuyết minh đồ án.

---

## 🛠️ 5. Xử lý một số lỗi thường gặp (Troubleshooting)

1. **Lỗi `Port 8000 is already in use`:**
   - Cổng 8000 đang bị ứng dụng khác chiếm. Chạy sang cổng khác:
     ```powershell
     python manage.py runserver 8080
     ```
2. **Lỗi `Can't connect to MySQL server`:**
   - Dịch vụ MySQL chưa được bật. Mở PowerShell với quyền Admin và gõ:
     ```powershell
     net start MySQL80
     ```
3. **Chạy kiểm thử tự động (Unit Tests):**
   - Đảm bảo toàn bộ hệ thống hoạt động ổn định 100%:
     ```powershell
     python manage.py test
     ```
