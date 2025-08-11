# -*- coding: utf-8 -*-
"""
Factory function để khởi tạo Flask application
File này tạo và cấu hình ứng dụng Flask với tất cả các thành phần cần thiết
"""
from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from dupliapp.routes.health import bp as health_bp
from dupliapp.routes.chroma import bp as chroma_bp
from dupliapp.routes.topics import bp as topics_bp
from dupliapp.routes.index import bp as index_bp

def create_app() -> Flask:
    """
    Factory function để tạo và cấu hình Flask application
    
    Returns:
        Flask app đã được cấu hình đầy đủ với:
        - CORS support
        - Swagger UI documentation
        - Tất cả API routes đã đăng ký
    """
    # Tạo Flask app instance
    app = Flask(__name__)
    
    # Cấu hình CORS để cho phép frontend gọi API
    # supports_credentials=True cho phép gửi cookies/headers xác thực
    CORS(app, supports_credentials=True)
    
    # Cấu hình Swagger với tài liệu chi tiết
    # Swagger UI sẽ có sẵn tại /apidocs/
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec_1',
                "route": '/apispec_1.json',
                "rule_filter": lambda rule: True,  # Bao gồm tất cả routes
                "model_filter": lambda tag: True,  # Bao gồm tất cả models
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }
    
    # Template cho Swagger documentation
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "API Dịch Vụ Kiểm Tra Trùng Lặp",
            "description": """
            ## Tài Liệu API Dịch Vụ Kiểm Tra Trùng Lặp
            
            Dịch vụ này cung cấp chức năng phát hiện trùng lặp cho các đề tài nghiên cứu 
            sử dụng vector embeddings và tìm kiếm tương tự.
            
            ### Tính Năng Chính:
            - **Quản Lý Đề Tài**: Thêm và cập nhật đề tài nghiên cứu với vector embeddings
            - **Phát Hiện Trùng Lặp**: Tìm kiếm đề tài tương tự sử dụng độ tương tự ngữ nghĩa
            - **Thao Tác Hàng Loạt**: Xử lý nhiều đề tài một cách hiệu quả
            - **Cơ Sở Dữ Liệu Vector**: Được hỗ trợ bởi cơ sở dữ liệu vector Chroma
            - **Giám Sát Sức Khỏe**: Kiểm tra sức khỏe dịch vụ và thống kê
            
            ### Xác Thực:
            Hiện tại không yêu cầu xác thực cho các endpoint API.
            
            ### Giới Hạn Tốc Độ:
            Hiện tại chưa triển khai giới hạn tốc độ.
            
            ### Xử Lý Lỗi:
            Tất cả các endpoint trả về mã trạng thái HTTP phù hợp và thông báo lỗi ở định dạng JSON.
            """,
            "version": "2.0.0",
            "contact": {
                "name": "Hỗ Trợ API",
                "email": "support@example.com"
            },
            "license": {
                "name": "MIT",
                "url": "https://opensource.org/licenses/MIT"
            }
        },
        "host": "localhost:8008",
        "basePath": "/",
        "schemes": ["http", "https"],
        "consumes": ["application/json"],
        "produces": ["application/json"],
        "tags": [
            {
                "name": "Sức Khỏe",
                "description": "Các endpoint kiểm tra sức khỏe và thông tin dịch vụ"
            },
            {
                "name": "Đề Tài",
                "description": "Các endpoint quản lý đề tài và phát hiện trùng lặp"
            },
            {
                "name": "Chroma",
                "description": "Thống kê và quản lý cơ sở dữ liệu vector"
            },
            {
                "name": "Chỉ Mục",
                "description": "Quản lý chỉ mục và đồng bộ hóa dữ liệu"
            }
        ]
    }
    
    # Khởi tạo Swagger với cấu hình và template
    Swagger(app, config=swagger_config, template=swagger_template)
    
    # Đăng ký các blueprint (modules) cho ứng dụng
    # Mỗi blueprint chứa một nhóm routes liên quan
    app.register_blueprint(health_bp)    # Routes kiểm tra sức khỏe
    app.register_blueprint(chroma_bp)    # Routes thống kê ChromaDB
    app.register_blueprint(topics_bp)    # Routes quản lý đề tài
    app.register_blueprint(index_bp)     # Routes xây dựng chỉ mục
    
    return app
