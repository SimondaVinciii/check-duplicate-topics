# -*- coding: utf-8 -*-
# Module xử lý vector embeddings sử dụng Sentence Transformers
from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from dupliapp.config import settings

# Biến global để lưu model (singleton pattern)
_model = None

def get_model() -> SentenceTransformer:
    # Lazy loading model embedding - chỉ load khi cần thiết
    global _model
    if _model is None:
        _model = SentenceTransformer(settings.MODEL_NAME)
    return _model

def embed_texts(texts: List[str]) -> np.ndarray:
    # Chuyển đổi danh sách text thành vector embeddings
    model = get_model()
    # normalize_embeddings=True để chuẩn hóa vector về unit length
    embs = model.encode(texts, normalize_embeddings=True)
    return np.array(embs, dtype=np.float32)
