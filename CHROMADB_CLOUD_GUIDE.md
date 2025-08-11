# Hướng Dẫn Sử Dụng ChromaDB Cloud

## Tổng Quan

Dự án hỗ trợ 2 chế độ ChromaDB:
- **Local Mode**: Lưu trữ dữ liệu locally (mặc định)
- **Cloud Mode**: Sử dụng ChromaDB Cloud service (v2 API)

## ⚠️ Lưu Ý Quan Trọng

**ChromaDB Cloud đã deprecated v1 API và yêu cầu sử dụng v2 API.** 
Dự án này đã được cập nhật để sử dụng v2 API.

## Cấu Hình ChromaDB

### 1. ChromaDB Local (Mặc định)

**Ưu điểm:**
- Không cần internet
- Không có chi phí
- Dữ liệu lưu trữ locally
- Phù hợp cho development và testing

**Cấu hình:**
```env
CHROMA_MODE=local
CHROMA_DIR=./chroma_data
```

### 2. ChromaDB Cloud (v2 API)

**Ưu điểm:**
- Không cần quản lý server
- Backup tự động
- Scalable
- Có thể truy cập từ nhiều nơi
- Phù hợp cho production

**Cấu hình:**
```env
CHROMA_MODE=cloud
CHROMA_CLOUD_HOST=your-host.chromadb.com
CHROMA_CLOUD_PORT=443
CHROMA_CLOUD_SSL=true
CHROMA_CLOUD_API_KEY=your-api-key
CHROMA_CLOUD_TENANT=your-tenant-id
CHROMA_CLOUD_DATABASE=your-database-name
```

## Cách Lấy Thông Tin ChromaDB Cloud

### Bước 1: Đăng ký tài khoản
1. Truy cập: https://cloud.chromadb.com
2. Đăng ký tài khoản mới
3. Xác thực email

### Bước 2: Tạo Database
1. Đăng nhập vào dashboard
2. Click "Create Database"
3. Đặt tên database
4. Lưu lại Database ID

### Bước 3: Lấy API Key
1. Vào Settings → API Keys
2. Click "Create API Key"
3. Đặt tên cho API key
4. Copy và lưu API key

### Bước 4: Lấy Tenant ID
1. Vào Settings → General
2. Copy Tenant ID

### Bước 5: Lấy Host
1. Vào Settings → General
2. Copy Host URL

## Cấu Hình File .env

### Local Mode
```env
# ChromaDB Local
CHROMA_MODE=local
CHROMA_DIR=./chroma_data

# Các cấu hình khác
SQLSERVER_CONN=your-sql-connection-string
MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
HOST=0.0.0.0
PORT=8008
THRESHOLD=0.7
TOPK=3
```

### Cloud Mode
```env
# ChromaDB Cloud (v2 API)
CHROMA_MODE=cloud
CHROMA_CLOUD_HOST=your-host.chromadb.com
CHROMA_CLOUD_PORT=443
CHROMA_CLOUD_SSL=true
CHROMA_CLOUD_API_KEY=your-api-key-here
CHROMA_CLOUD_TENANT=your-tenant-id
CHROMA_CLOUD_DATABASE=your-database-name

# Các cấu hình khác
SQLSERVER_CONN=your-sql-connection-string
MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2
HOST=0.0.0.0
PORT=8008
THRESHOLD=0.7
TOPK=3
```

## Chuyển Đổi Từ Local Sang Cloud

### Bước 1: Backup dữ liệu local
```bash
# Dữ liệu local được lưu trong thư mục CHROMA_DIR
cp -r ./chroma_data ./chroma_data_backup
```

### Bước 2: Cấu hình cloud
Cập nhật file `.env` với thông tin ChromaDB Cloud

### Bước 3: Rebuild index
```bash
# Gọi API để rebuild index từ SQL Server
curl -X POST http://localhost:8008/index/topics
```

## Kiểm Tra Trạng Thái

### Health Check
```bash
curl http://localhost:8008/health
```

### ChromaDB Stats
```bash
curl http://localhost:8008/chroma/stats
```

**Response cho Local Mode:**
```json
{
  "mode": "local",
  "path": "./chroma_data",
  "activeCollection": "topics_v1",
  "activeCount": 1500,
  "collections": [
    {
      "name": "topics_v1",
      "count": 1500
    }
  ]
}
```

**Response cho Cloud Mode:**
```json
{
  "mode": "cloud",
  "host": "your-host.chromadb.com",
  "database": "your-database-name",
  "tenant": "your-tenant-id",
  "activeCollection": "topics_v1",
  "activeCount": 1500,
  "collections": [
    {
      "name": "topics_v1",
      "count": 1500
    }
  ]
}
```

## Troubleshooting

### Lỗi v1 API Deprecated
**Triệu chứng:** `"The v1 API is deprecated. Please use /v2 apis"`

**Giải pháp:**
- ✅ **Đã được sửa** trong phiên bản hiện tại
- Sử dụng `tenant` và `database` parameters trong HttpClient
- Đảm bảo sử dụng ChromaDB client version mới nhất

### Lỗi kết nối Cloud
**Triệu chứng:** `ValueError: CHROMA_CLOUD_HOST is required for cloud mode`

**Giải pháp:**
- Kiểm tra API key có đúng không
- Kiểm tra host có đúng không
- Kiểm tra internet connection
- Đảm bảo tất cả thông tin cloud được cấu hình

### Lỗi Tenant không tồn tại
**Triệu chứng:** `Could not connect to tenant default_tenant. Are you sure it exists?`

**Giải pháp:**
- Kiểm tra `CHROMA_CLOUD_TENANT` có đúng không
- Đảm bảo tenant ID được copy chính xác từ dashboard
- Tạo tenant mới nếu cần

### Lỗi SSL
**Triệu chứng:** SSL connection errors

**Giải pháp:**
- Đảm bảo `CHROMA_CLOUD_SSL=true`
- Kiểm tra certificate
- Thử với `CHROMA_CLOUD_SSL=false` (nếu được hỗ trợ)

### Lỗi Authentication
**Triệu chứng:** 401 Unauthorized

**Giải pháp:**
- Kiểm tra API key có quyền truy cập database
- Kiểm tra tenant ID có đúng không
- Tạo API key mới nếu cần

### Lỗi Database không tồn tại
**Triệu chứng:** Database not found

**Giải pháp:**
- Kiểm tra database name có đúng không
- Tạo database mới trong ChromaDB Cloud
- Đảm bảo API key có quyền truy cập database

## So Sánh Local vs Cloud

| Tính năng | Local | Cloud |
|-----------|-------|-------|
| **Chi phí** | Miễn phí | Có phí |
| **Internet** | Không cần | Cần |
| **Backup** | Manual | Tự động |
| **Scalability** | Giới hạn | Không giới hạn |
| **Maintenance** | Tự quản lý | Không cần |
| **Performance** | Phụ thuộc hardware | Tối ưu |
| **Security** | Tự bảo vệ | Enterprise grade |
| **API Version** | Local | v2 API |

## Best Practices

### Development
- Sử dụng **Local mode** cho development
- Test với dữ liệu nhỏ
- Backup thường xuyên

### Production
- Sử dụng **Cloud mode** cho production
- Monitor usage và costs
- Set up alerts cho errors
- Regular backup verification

### Migration
- Test migration với dữ liệu nhỏ trước
- Backup trước khi migrate
- Verify data integrity sau migration
- Monitor performance sau migration

## Kiểm Tra Version

### ChromaDB Client Version
```bash
pip show chromadb
```

**Khuyến nghị:** Sử dụng ChromaDB version 0.4.24 hoặc mới hơn để hỗ trợ v2 API.

### Test Connection
```bash
# Test local mode
python test_chroma_modes.py

# Test cloud mode (nếu có credentials)
CHROMA_MODE=cloud python test_chroma_modes.py
```
