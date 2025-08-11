# -*- coding: utf-8 -*-
# Äá»c cáº¥u hÃ¬nh tá»« .env vÃ  biáº¿n mÃ´i trÆ°á»ng
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Settings:
    SQLSERVER_CONN: str = os.getenv("SQLSERVER_CONN", "")
    CHROMA_DIR: str = os.getenv("CHROMA_DIR", "./chroma_data")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8008"))
    THRESHOLD: float = float(os.getenv("THRESHOLD", "0.7"))
    TOPK: int = int(os.getenv("TOPK", "3"))

settings = Settings()
