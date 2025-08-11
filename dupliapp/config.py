# -*- coding: utf-8 -*-
"""
Module cấu hình ứng dụng
Đọc cấu hình từ biến môi trường và cung cấp giá trị mặc định
"""
import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Tải biến môi trường từ file .env
load_dotenv()

@dataclass
class Settings:
    """
    Class chứa tất cả cấu hình của ứng dụng
    
    Sử dụng dataclass để tự động tạo __init__, __repr__, etc.
    Tất cả giá trị được đọc từ biến môi trường với fallback values
    """
    
    # Chuỗi kết nối SQL Server (bắt buộc cho việc đồng bộ dữ liệu)
    SQLSERVER_CONN: str = os.getenv("SQLSERVER_CONN", "")
    
    # Cấu hình ChromaDB - Local hoặc Cloud
    CHROMA_MODE: str = os.getenv("CHROMA_MODE", "local")  # "local" hoặc "cloud"
    
    # Thư mục lưu trữ dữ liệu ChromaDB local (vector database)
    CHROMA_DIR: str = os.getenv("CHROMA_DIR", "./chroma_data")
    
    # Cấu hình ChromaDB Cloud
    CHROMA_CLOUD_HOST: str = os.getenv("CHROMA_CLOUD_HOST", "")
    CHROMA_CLOUD_PORT: int = int(os.getenv("CHROMA_CLOUD_PORT", "443"))
    CHROMA_CLOUD_SSL: bool = os.getenv("CHROMA_CLOUD_SSL", "true").lower() == "true"
    CHROMA_CLOUD_API_KEY: str = os.getenv("CHROMA_CLOUD_API_KEY", "")
    CHROMA_CLOUD_TENANT: str = os.getenv("CHROMA_CLOUD_TENANT", "")
    CHROMA_CLOUD_DATABASE: str = os.getenv("CHROMA_CLOUD_DATABASE", "")
    
    # Tên model embedding để chuyển đổi text thành vector
    # all-MiniLM-L6-v2 là model nhỏ gọn, nhanh và hiệu quả cho tiếng Việt
    MODEL_NAME: str = os.getenv("MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
    
    # Host và port để chạy Flask server
    HOST: str = os.getenv("HOST", "0.0.0.0")  # 0.0.0.0 = lắng nghe tất cả interfaces
    PORT: int = int(os.getenv("PORT", "8008"))
    
    # Ngưỡng độ tương tự để xác định trùng lặp (0.0 - 1.0)
    # Giá trị càng cao thì càng nghiêm ngặt trong việc phát hiện trùng lặp
    THRESHOLD: float = float(os.getenv("THRESHOLD", "0.7"))
    
    # Số lượng kết quả tương tự tối đa trả về khi tìm kiếm
    TOPK: int = int(os.getenv("TOPK", "3"))

# Tạo instance settings để sử dụng trong toàn bộ ứng dụng
settings = Settings()
