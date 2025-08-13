# Hướng dẫn sử dụng Embedding Models

## Tổng quan

Ứng dụng hỗ trợ 2 loại embedding models:

1. **Sentence Transformers** (mặc định): Sử dụng các model local như `all-mpnet-base-v2`
2. **Gemini Embeddings**: Sử dụng Google Gemini API với model `gemini-embedding-001`

## Cấu hình

### 1. Sentence Transformers (Mặc định)

```bash
# Trong file .env
EMBEDDING_TYPE=sentence_transformers
MODEL_NAME=sentence-transformers/all-mpnet-base-v2
```

**Ưu điểm:**
- Chạy offline, không cần API key
- Nhanh và ổn định
- Miễn phí

**Nhược điểm:**
- Chất lượng embedding có thể thấp hơn so với cloud models
- Cần tải model về máy

### 2. Gemini Embeddings

```bash
# Trong file .env
EMBEDDING_TYPE=gemini
GEMINI_API_KEY=your-gemini-api-key-here
```

**Ưu điểm:**
- Chất lượng embedding cao
- Không cần tải model về máy
- Hỗ trợ đa ngôn ngữ tốt

**Nhược điểm:**
- Cần API key và có thể tính phí
- Phụ thuộc vào kết nối internet
- Có thể có độ trễ

## Cách lấy Gemini API Key

1. Truy cập [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Đăng nhập bằng Google account
3. Tạo API key mới
4. Copy API key vào file `.env`

## Chuyển đổi giữa các models

### Từ Sentence Transformers sang Gemini

1. Cập nhật file `.env`:
```bash
EMBEDDING_TYPE=gemini
GEMINI_API_KEY=your-api-key
```

2. Khởi động lại ứng dụng

### Từ Gemini sang Sentence Transformers

1. Cập nhật file `.env`:
```bash
EMBEDDING_TYPE=sentence_transformers
MODEL_NAME=sentence-transformers/all-mpnet-base-v2
```

2. Khởi động lại ứng dụng

## Lưu ý quan trọng

- Khi chuyển đổi giữa các embedding models, các vector đã lưu trong ChromaDB sẽ không tương thích
- Cần xóa và tạo lại collection nếu muốn sử dụng model khác
- Model `all-mpnet-base-v2` có kích thước vector là 768 chiều
- Model `gemini-embedding-001` có kích thước vector là 768 chiều

## Troubleshooting

### Lỗi "GEMINI_API_KEY is required"
- Kiểm tra xem đã set `GEMINI_API_KEY` trong file `.env` chưa
- Đảm bảo API key hợp lệ

### Lỗi "Unsupported embedding type"
- Kiểm tra giá trị `EMBEDDING_TYPE` phải là `sentence_transformers` hoặc `gemini`

### Lỗi kết nối Gemini API
- Kiểm tra kết nối internet
- Kiểm tra API key có đúng không
- Kiểm tra quota của Gemini API
