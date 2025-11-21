# Ứng dụng Tự Động Đăng Ký - Python Selenium

Ứng dụng Python sử dụng Selenium để tự động đăng ký tài khoản trên trang web https://python1.pyan.vn/

## Yêu Cầu

- Python 3.7 trở lên
- Google Chrome đã được cài đặt
- ChromeDriver (sẽ được tự động tải nếu sử dụng webdriver-manager)

## Cài Đặt

1. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

## Sử Dụng

### Chạy nhanh với cấu hình mặc định:
```bash
python register.py
```

Chương trình sẽ tự động:
- Đọc cấu hình từ `config.json` (tự động tạo nếu chưa có)
- Tạo tên và email ngẫu nhiên nếu chưa có trong config
- Lưu thông tin đăng ký vào `registration_history.json`

### Cấu hình qua file config.json

File `config.json` sẽ được tự động tạo khi chạy lần đầu. Bạn có thể chỉnh sửa:

```json
{
  "coupon": "damuatdh",
  "name": null,
  "email": null,
  "wait_timeout": 10,
  "fast_mode": true
}
```

- `coupon`: Mã coupon mặc định
- `name`: Tên cố định (để `null` để tự động tạo)
- `email`: Email cố định (để `null` để tự động tạo)
- `wait_timeout`: Thời gian chờ tối đa (giây)
- `fast_mode`: Chế độ nhanh (giảm thời gian chờ, tắt hình ảnh)

### Xem lịch sử đăng ký

Tất cả thông tin đăng ký được lưu trong file `registration_history.json`:

```json
[
  {
    "timestamp": "2025-01-XX XX:XX:XX",
    "name": "User_xxxxxx",
    "email": "test_xxxxxx@example.com",
    "coupon": "damuatdh",
    "status": "success"
  }
]
```

## Tính Năng

### Tính năng chính:
- ✅ Tự động truy cập trang web
- ✅ Tự động click vào nút "Đăng Ký Ngay"
- ✅ Tự động điền form đăng ký (tên, email, coupon)
- ✅ Tự động click nút "Apply" để áp dụng coupon
- ✅ Tự động click nút "Complete my purchase"
- ✅ Tự động tạo tên và email ngẫu nhiên nếu không chỉ định
- ✅ Xử lý lỗi và chụp màn hình khi có lỗi
- ✅ Hiển thị kết quả đăng ký

### Tính năng mới (cải tiến):
- 🚀 **Chế độ nhanh (Fast Mode)**: Giảm thời gian chờ, tắt hình ảnh để tải nhanh hơn
- 💾 **Lưu cấu hình**: Tự động lưu và đọc cấu hình từ `config.json`
- 📝 **Lưu lịch sử**: Tự động lưu tất cả thông tin đăng ký vào `registration_history.json`
- ⚡ **Tối ưu hóa**: Sử dụng explicit waits thay vì sleep cố định
- 🔄 **Tái sử dụng**: Đọc thông tin từ config để không phải nhập lại

## Cấu Trúc File

```
.
├── register.py                    # Script chính
├── config.json                    # File cấu hình (tự động tạo)
├── registration_history.json      # Lịch sử đăng ký (tự động tạo)
├── error_screenshot.png           # Screenshot khi có lỗi (nếu có)
├── requirements.txt               # Danh sách thư viện
└── README.md                      # File hướng dẫn này
```

## Lưu Ý

- Đảm bảo bạn có kết nối internet
- Trình duyệt Chrome sẽ tự động mở trong quá trình chạy
- Nếu trang web có CAPTCHA, bạn cần giải quyết thủ công
- Tuân thủ điều khoản sử dụng của trang web
- File `config.json` và `registration_history.json` sẽ được tạo tự động

## Xử Lý Lỗi

Nếu gặp lỗi:
1. Kiểm tra kết nối internet
2. Đảm bảo Chrome đã được cài đặt
3. Kiểm tra file `error_screenshot.png` nếu có lỗi xảy ra
4. Kiểm tra cấu trúc HTML của trang web có thay đổi không
5. Xem file `registration_history.json` để kiểm tra các lần đăng ký trước

## Tối Ưu Hóa

Chương trình đã được tối ưu để chạy nhanh hơn:
- Sử dụng explicit waits thay vì sleep cố định
- Tắt hình ảnh trong chế độ fast mode
- Page load strategy = 'eager' (không chờ tất cả resources)
- Giảm thời gian chờ giữa các bước

