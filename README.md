# Duplicate Check Service

Dịch vụ kiểm tra trùng lặp đề tài nghiên cứu sử dụng vector embeddings và tìm kiếm tương tự.

## Tính Năng

- **Quản Lý Đề Tài**: Thêm và cập nhật đề tài nghiên cứu với vector embeddings
- **Phát Hiện Trùng Lặp**: Tìm kiếm đề tài tương tự sử dụng độ tương tự ngữ nghĩa
- **Thao Tác Hàng Loạt**: Xử lý nhiều đề tài một cách hiệu quả
- **Cơ Sở Dữ Liệu Vector**: Được hỗ trợ bởi cơ sở dữ liệu vector Chroma
- **API Documentation**: Swagger UI tích hợp

## Cài Đặt

1. **Clone repository:**
```bash
git clone <repository-url>
cd duplicate-service
```

2. **Tạo virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# hoặc
.venv\Scripts\activate  # Windows
```

3. **Cài đặt dependencies:**
```bash
pip install -r requirements.txt
```

4. **Cấu hình environment variables:**
```bash
cp .env.example .env
# Chỉnh sửa file .env với các giá trị phù hợp
```

5. **Chạy ứng dụng:**
```bash
python run.py
```

## API Documentation

Truy cập Swagger UI tại: `http://localhost:8008/apidocs/`

### Các Endpoint Chính

- `GET /` - Thông tin dịch vụ
- `GET /health` - Kiểm tra sức khỏe
- `POST /topics/upsert` - Thêm/cập nhật đề tài
- `POST /topics/bulk-upsert` - Thêm/cập nhật nhiều đề tài
- `POST /topics/search` - Tìm kiếm trùng lặp
- `GET /chroma/stats` - Thống kê cơ sở dữ liệu
- `POST /index/topics` - Xây dựng lại chỉ mục

## Testing

```bash
# Cài đặt test dependencies
pip install -r requirements-test.txt

# Chạy tests
pytest tests/ -v

# Chạy tests với coverage
pytest tests/ -v --cov=dupliapp --cov-report=html
```

## Cấu Trúc Dự Án

```
duplicate-service/
├── dupliapp/
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── routes/
│   │   ├── health.py
│   │   ├── topics.py
│   │   ├── chroma.py
│   │   └── index.py
│   ├── services/
│   │   ├── topic_service.py
│   │   └── index_service.py
│   ├── repositories/
│   │   ├── chroma_repository.py
│   │   └── topic_repository.py
│   └─
```