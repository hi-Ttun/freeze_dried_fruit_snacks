# NutriSnack: đặc tả dự án (để agent đọc ở đầu mỗi tác vụ)

Website thương mại điện tử bán trái cây sấy thăng hoa và hạt dinh dưỡng (bài tập lớn TMĐT, nhóm 6).
Kênh lõi là website riêng (D2C). Giao diện tiếng Việt, mã lệnh và tên biến tiếng Anh.

## Công nghệ
Django 5 + PostgreSQL (SQLite khi dev nhanh) + template Django + CSS thuần (static/css/site.css). Không dùng framework JS.
Cấu hình đọc từ biến môi trường (.env). Không đưa bí mật vào mã nguồn.

## Cấu trúc
- `config/`: settings, urls, wsgi
- `shop/`: Category, Product, Variant, Lot (lô hàng, hạn dùng), trang cửa hàng, truy xuất theo lô, trang chính sách
- `orders/`: giỏ hàng (session), Order, OrderItem, OrderItemAllocation, Payment, Shipment, StatusHistory, services.place_order (FEFO), báo cáo
- `accounts/`: đăng ký, đăng nhập, đăng xuất
- `templates/`, `static/`

## Quy tắc nghiệp vụ
- Giá lưu số nguyên VNĐ. Hiển thị bằng filter `vnd`.
- Chỉ bán lô còn >= MIN_SHELF_DAYS ngày hạn dùng. Xuất kho theo FEFO (hạn gần nhất trước). Đặt hàng chạy trong một transaction, khóa dòng lô.
- Phí vận chuyển: theo khu vực (nội thành / khác), miễn phí từ FREE_SHIPPING_THRESHOLD.
- Thanh toán: COD và chuyển khoản (VietQR). Cổng thanh toán sandbox, tích hợp hãng vận chuyển, song ngữ nằm ngoài phạm vi (hướng phát triển).
- Trạng thái đơn: pending -> confirmed -> (paid) -> packing -> shipping -> delivered -> completed; nhánh cancelled (chỉ trước khi giao, trả hàng về đúng lô), returned (không tự nhập lại kho vì là thực phẩm).
- Chỉ đổi trạng thái qua `Order.change_status` (ghi StatusHistory, xử lý kho, thanh toán, vận chuyển).
- Khách vãng lai xem đơn bằng mã đơn + số điện thoại (lưu trong session).
- Phân quyền: Admin (superuser), Sales, Warehouse (tạo bằng `seed_data`).

## Việc chưa làm (theo lịch)
Mã giảm giá, đánh giá sản phẩm, quên mật khẩu, giới hạn số lần đăng nhập/tra cứu, /health, Nginx + HTTPS, sao lưu, đo tải, ảnh sản phẩm thật.

## Quy ước
Mỗi thay đổi nhỏ, chạy `python manage.py test` trước khi commit. Không đổi tên model/field khi chưa tạo migration.
