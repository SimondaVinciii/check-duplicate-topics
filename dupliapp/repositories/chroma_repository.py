# -*- coding: utf-8 -*-
# Repository lÃ m viá»‡c vá»›i ChromaDB
from typing import List, Dict, Any, Optional
import os
import chromadb
from dupliapp.config import settings

class ChromaTopicsRepository:
    COLLECTION = "topics_v1"

    def __init__(self):
        os.makedirs(settings.CHROMA_DIR, exist_ok=True)
        self.client = chromadb.PersistentClient(path=settings.CHROMA_DIR)
        try:
            self.col = self.client.get_collection(self.COLLECTION)
        except Exception:
            self.col = self.client.create_collection(name=self.COLLECTION, metadata={"hnsw:space": "cosine"})

    def upsert(self, ids: List[str], embeddings: List[List[float]], metadatas: List[Dict[str, Any]], documents: List[str]):
        self.col.upsert(ids=ids, embeddings=embeddings, metadatas=metadatas, documents=documents)

    def query(self, query_embedding: List[float], n_results: int, where: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        res = self.col.query(query_embeddings=[query_embedding], n_results=n_results, where=where)
        # Chroma tráº£ vá» nested list, ta flatten Ä‘á»ƒ dá»… dÃ¹ng
        out = {"metadatas": [], "distances": []}
        if res and res.get("metadatas"):
            metas = res["metadatas"][0]
            dists = res.get("distances", [[0]*len(metas)])[0]
            for m, d in zip(metas, dists):
                out["metadatas"].append(m)
                out["distances"].append(d)
        return out

    def count(self) -> int:
        try:
            return int(self.col.count())
        except Exception:
            return 0

    def stats(self) -> Dict[str, Any]:
        try:
            collections = []
            for c in self.client.list_collections():
                try:
                    col = self.client.get_collection(c.name)
                    cnt = int(col.count())
                except Exception:
                    cnt = 0
                collections.append({"name": c.name, "count": cnt})
            return {
                "path": settings.CHROMA_DIR,
                "activeCollection": self.COLLECTION,
                "activeCount": self.count(),
                "collections": collections
            }
        except Exception as e:
            return {"error": str(e)}
