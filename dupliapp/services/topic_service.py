# -*- coding: utf-8 -*-
# Use-case xá»­ lÃ½ duplicate, upsert vector vÃ o Chroma
from typing import List, Dict, Any
from dupliapp.utils.embeddings import embed_texts
from dupliapp.repositories.chroma_repository import ChromaTopicsRepository

class TopicsService:
    def __init__(self):
        self.repo = ChromaTopicsRepository()

    @staticmethod
    def compose_topic_text(row: Dict[str, Any]) -> str:
        # GhÃ©p ná»™i dung cÃ¡c trÆ°á»ng thÃ nh 1 text Ä‘á»ƒ embedding
        parts = [
            str(row.get("title") or row.get("Title") or ""),
            str(row.get("description") or row.get("Description") or ""),
            str(row.get("objectives") or row.get("Objectives") or ""),
            str(row.get("methodology") or row.get("Methodology") or ""),
            str(row.get("expectedOutcomes") or row.get("ExpectedOutcomes") or ""),
            str(row.get("requirements") or row.get("Requirements") or ""),
        ]
        return "\n\n".join([p for p in parts if p and p.strip()])

    def upsert_one(self, data: Dict[str, Any]) -> None:
        required = ["topicId", "topicVersionId"]
        for k in required:
            if k not in data:
                raise ValueError(f"Missing field: {k}")
        text = self.compose_topic_text(data)
        emb = embed_texts([text])[0].tolist()
        meta = {
            "TopicId": data.get("topicId"),
            "TopicVersionId": data.get("topicVersionId"),
            "Title": data.get("title", ""),
            "Description": data.get("description", ""),
            "Objectives": data.get("objectives", ""),
            "Methodology": data.get("methodology", ""),
            "ExpectedOutcomes": data.get("expectedOutcomes", ""),
            "Requirements": data.get("requirements", ""),
        }
        extra = data.get("metadata") or {}
        if isinstance(extra, dict):
            meta.update(extra)
        self.repo.upsert(
            ids=[f"tv:{meta['TopicVersionId']}"],
            embeddings=[emb],
            metadatas=[meta],
            documents=[text],
        )

    def upsert_many(self, items: List[Dict[str, Any]]) -> int:
        if not isinstance(items, list) or not items:
            raise ValueError("Provide a non-empty 'items' array")
        ids, texts, metas = [], [], []
        for it in items:
            if "topicId" not in it or "topicVersionId" not in it:
                raise ValueError("Each item must include topicId and topicVersionId")
            text = self.compose_topic_text(it)
            meta = {
                "TopicId": it.get("topicId"),
                "TopicVersionId": it.get("topicVersionId"),
                "Title": it.get("title", ""),
                "Description": it.get("description", ""),
                "Objectives": it.get("objectives", ""),
                "Methodology": it.get("methodology", ""),
                "ExpectedOutcomes": it.get("expectedOutcomes", ""),
                "Requirements": it.get("requirements", ""),
            }
            extra = it.get("metadata") or {}
            if isinstance(extra, dict):
                meta.update(extra)
            ids.append(f"tv:{meta['TopicVersionId']}")
            texts.append(text)
            metas.append(meta)
        embs = embed_texts(texts).tolist()
        self.repo.upsert(ids=ids, embeddings=embs, metadatas=metas, documents=texts)
        return len(ids)

    def search(self, data: Dict[str, Any], top_k: int, threshold: float) -> Dict[str, Any]:
        # Cho phÃ©p truyá»n 'text' trá»±c tiáº¿p hoáº·c ghÃ©p tá»« cÃ¡c field
        text = data.get("text") or "\n\n".join([
            data.get("title", ""),
            data.get("description", ""),
            data.get("objectives", ""),
            data.get("methodology", ""),
            data.get("expectedOutcomes", ""),
            data.get("requirements", ""),
        ]).strip()
        if not text:
            return {"error": "Provide either 'text' or the content fields"}
        query_emb = embed_texts([text])[0].tolist()
        where = data.get("metadataFilter") if isinstance(data.get("metadataFilter"), dict) else None
        res = self.repo.query(query_emb, n_results=top_k, where=where)
        hits = []
        for meta, dist in zip(res.get("metadatas", []), res.get("distances", [])):
            m = meta or {}
            sim = 1.0 - (float(dist) / 2.0)  # Ä‘á»•i tá»« cosine distance sang similarity ~ [0..1]
            hits.append({
                "topicId": m.get("TopicId"),
                "topicVersionId": m.get("TopicVersionId"),
                "title": m.get("Title", ""),
                "similarity": round(sim, 4)
            })
        hits.sort(key=lambda h: h.get("similarity", 0), reverse=True)
        passed = all(h["similarity"] < threshold for h in hits)
        suggestions = hits[:3]
        return {"passed": passed, "hits": hits, "suggestions": suggestions, "threshold": threshold}

    @staticmethod
    def count_vectors() -> int:
        return ChromaTopicsRepository().count()

    def chroma_stats(self) -> Dict[str, Any]:
        return ChromaTopicsRepository().stats()
