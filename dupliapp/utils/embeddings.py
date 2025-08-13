# -*- coding: utf-8 -*-
# Module xử lý vector embeddings sử dụng Sentence Transformers hoặc Gemini
from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from dupliapp.config import settings

# Biến global để lưu model (singleton pattern)
_sentence_model = None
_gemini_configured = False


def get_sentence_model() -> SentenceTransformer:
    # Lazy loading sentence transformer model - chỉ load khi cần thiết
    global _sentence_model
    if _sentence_model is None:
        _sentence_model = SentenceTransformer(settings.MODEL_NAME)
    return _sentence_model


def _ensure_gemini_configured() -> None:
    global _gemini_configured
    if not _gemini_configured:
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is required when using Gemini embeddings")
        genai.configure(api_key=settings.GEMINI_API_KEY)
        _gemini_configured = True


def _resolve_gemini_model_name() -> str:
    # Cho phép override qua biến cấu hình nếu có
    raw_name = getattr(settings, "GEMINI_EMBEDDING_MODEL", None)
    if not raw_name:
        # Nếu không khai báo, ưu tiên tên mà người dùng mong muốn, và map về tên chuẩn của API
        # 'gemini-embedding-001' (alias) -> 'models/embedding-001' (tên chuẩn API)
        return "models/embedding-001"
    # Chuẩn hóa một số alias phổ biến
    name = raw_name.strip()
    if name == "gemini-embedding-001":
        return "models/embedding-001"
    return name


def embed_texts(texts: List[str]) -> np.ndarray:
    # Chuyển đổi danh sách text thành vector embeddings
    embedding_type = (settings.EMBEDDING_TYPE or "sentence_transformers").strip().lower()

    if embedding_type == "sentence_transformers":
        model = get_sentence_model()
        # normalize_embeddings=True để chuẩn hóa vector về unit length
        embs = model.encode(texts, normalize_embeddings=True)
        return np.array(embs, dtype=np.float32)

    # Hỗ trợ alias: google, gemini, google_gemini
    elif embedding_type in ("gemini", "google", "google_gemini"):
        _ensure_gemini_configured()
        model_name = _resolve_gemini_model_name()
        embeddings = []
        for text in texts:
            result = genai.embed_content(model=model_name, content=text)
            embedding = result["embedding"]
            embeddings.append(embedding)
        # Chuẩn hóa embeddings về unit length
        embeddings = np.array(embeddings, dtype=np.float32)
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        # Tránh chia cho 0
        norms[norms == 0] = 1.0
        normalized_embeddings = embeddings / norms
        return normalized_embeddings

    else:
        raise ValueError(f"Unsupported embedding type: {settings.EMBEDDING_TYPE}")
