# -*- coding: utf-8 -*-
# Bao bá»c model embedding (Sentence-Transformers)
from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from dupliapp.config import settings

_model = None

def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(settings.MODEL_NAME)
    return _model

def embed_texts(texts: List[str]) -> np.ndarray:
    model = get_model()
    embs = model.encode(texts, normalize_embeddings=True)
    return np.array(embs, dtype=np.float32)
