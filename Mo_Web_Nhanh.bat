@echo off
chcp 65001 >nul
title Khởi động Website NutriSnack
echo ===============================================================
echo   🌿 ĐANG KHỞI ĐỘNG HỆ THỐNG NUTRISNACK (DJANGO + MYSQL)
echo ===============================================================
echo.

cd /d "%~dp0"

if not exist "venv\Scripts\python.exe" (
    echo [LỖI] Không tìm thấy môi trường ảo Python (venv)!
    echo Vui lòng đảm bảo đã tạo venv và cài đặt requirements.txt.
    pause
    exit /b
)

echo [1/2] Đang mở trình duyệt tại: http://127.0.0.1:8000 ...
timeout /t 1 /nobreak >nul
start "" http://127.0.0.1:8000

echo [2/2] Đang chạy máy chủ Django trên cổng 8000...
echo.
echo ===============================================================
echo   ✅ MÁY CHỦ ĐANG HOẠT ĐỘNG!
echo   👉 Địa chỉ truy cập: http://127.0.0.1:8000
echo   ⚠️  GIỮ NGUYÊN CỬA SỔ NÀY KHI SỬ DỤNG WEB (TẮT LÀ TẮT WEB).
echo ===============================================================
echo.

venv\Scripts\python.exe manage.py runserver 0.0.0.0:8000

pause
