# -*- coding: utf-8 -*-
# Service xử lý business logic cho đề tài - phát hiện trùng lặp và quản lý vector
from typing import List, Dict, Any
from dupliapp.utils.embeddings import embed_texts
from dupliapp.repositories.chroma_repository import ChromaTopicsRepository

class TopicsService:
    def __init__(self):
        # Khởi tạo repository để tương tác với ChromaDB
        self.repo = ChromaTopicsRepository()

    @staticmethod
    def compose_topic_text(row: Dict[str, Any]) -> str:
        # Ghép nội dung các trường thành 1 text để tạo embedding
        # Bao gồm: title, description, objectives, methodology, expectedOutcomes, requirements
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
        # Thêm hoặc cập nhật một đề tài với vector embedding
        # Kiểm tra các trường bắt buộc: topicId, topicVersionId
        required = ["topicId", "topicVersionId"]
        for k in required:
            if k not in data:
                raise ValueError(f"Missing field: {k}")
        
        # Tạo text và embedding
        text = self.compose_topic_text(data)
        emb = embed_texts([text])[0].tolist()
        
        # Chuẩn bị metadata cho ChromaDB
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
        # Thêm metadata bổ sung nếu có
        extra = data.get("metadata") or {}
        if isinstance(extra, dict):
            meta.update(extra)
            
        # Lưu vào ChromaDB
        self.repo.upsert(
            ids=[f"tv:{meta['TopicVersionId']}"],
            embeddings=[emb],
            metadatas=[meta],
            documents=[text],
        )

    def upsert_many(self, items: List[Dict[str, Any]]) -> int:
        # Thêm hoặc cập nhật nhiều đề tài cùng lúc (hiệu quả hơn)
        if not isinstance(items, list) or not items:
            raise ValueError("Provide a non-empty 'items' array")
            
        ids, texts, metas = [], [], []
        for it in items:
            # Kiểm tra trường bắt buộc cho mỗi item
            if "topicId" not in it or "topicVersionId" not in it:
                raise ValueError("Each item must include topicId and topicVersionId")
                
            # Tạo text và metadata cho mỗi item
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
            
        # Tạo embeddings cho tất cả texts cùng lúc
        embs = embed_texts(texts).tolist()
        self.repo.upsert(ids=ids, embeddings=embs, metadatas=metas, documents=texts)
        return len(ids)

    def search(self, data: Dict[str, Any], top_k: int, threshold: float) -> Dict[str, Any]:
        # Tìm kiếm đề tài trùng lặp dựa trên độ tương tự ngữ nghĩa
        # Cho phép truyền 'text' trực tiếp hoặc ghép từ các field
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
            
        # Tạo embedding cho query text
        query_emb = embed_texts([text])[0].tolist()
        
        # Lọc theo metadata nếu có
        where = data.get("metadataFilter") if isinstance(data.get("metadataFilter"), dict) else None
        
        # Tìm kiếm trong ChromaDB
        res = self.repo.query(query_emb, n_results=top_k, where=where)
        
        # Xử lý kết quả và tính similarity score
        hits = []
        for meta, dist in zip(res.get("metadatas", []), res.get("distances", [])):
            m = meta or {}
            # Chuyển đổi từ cosine distance sang similarity score [0..1]
            sim = 1.0 - (float(dist) / 2.0)
            hits.append({
                "topicId": m.get("TopicId"),
                "topicVersionId": m.get("TopicVersionId"),
                "title": m.get("Title", ""),
                "similarity": round(sim, 4)
            })
            
        # Sắp xếp theo similarity giảm dần
        hits.sort(key=lambda h: h.get("similarity", 0), reverse=True)
        
        # Kiểm tra xem có trùng lặp không (passed = True nếu không có hit >= threshold)
        passed = all(h["similarity"] < threshold for h in hits)
        suggestions = hits[:3]  # Top 3 gợi ý
        
        return {"passed": passed, "hits": hits, "suggestions": suggestions, "threshold": threshold}

    @staticmethod
    def count_vectors() -> int:
        # Đếm số vector trong ChromaDB (dùng cho health check)
        return ChromaTopicsRepository().count()

    def chroma_stats(self) -> Dict[str, Any]:
        # Lấy thống kê chi tiết về ChromaDB
        return ChromaTopicsRepository().stats()
