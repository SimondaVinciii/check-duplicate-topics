"""
Entry point chính để khởi chạy ứng dụng Flask
File này là điểm bắt đầu khi chạy dịch vụ kiểm tra trùng lặp
"""
from dupliapp.main import create_app
from dupliapp.config import settings

# Tạo Flask application từ factory function
app = create_app()

if __name__ == "__main__":
    # Chạy Flask development server
    # Sử dụng host và port từ cấu hình settings
    app.run(host=settings.HOST, port=settings.PORT)