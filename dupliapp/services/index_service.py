# -*- coding: utf-8 -*-
# Service xây dựng lại index từ SQL Server (tùy chọn)
from typing import Optional, Dict, Any, List
from dupliapp.repositories.topic_repository import MsSqlTopicRepository
from dupliapp.services.topic_service import TopicsService

class IndexService:
    def build_from_sql(self, limit: Optional[int] = None) -> Dict[str, Any]:
        # Xây dựng lại chỉ mục vector từ dữ liệu SQL Server
        # Hữu ích cho thiết lập ban đầu hoặc đồng bộ hóa dữ liệu
        
        # Lấy dữ liệu từ SQL Server
        repo = MsSqlTopicRepository()
        rows = repo.fetch_latest(limit=limit)
        
        # Chuyển đổi sang format phù hợp cho vector database
        svc = TopicsService()
        items = []
        topics_added = []  # Danh sách topics được thêm vào
        
        for r in rows:
            topic_info = {
                "topicId": r["TopicId"],
                "topicVersionId": r["TopicVersionId"],
                "title": r.get("Title", ""),
                "description": r.get("Description", ""),
                "objectives": r.get("Objectives", ""),
                "methodology": r.get("Methodology", ""),
                "expectedOutcomes": r.get("ExpectedOutcomes", ""),
                "requirements": r.get("Requirements", ""),
            }
            items.append(topic_info)
            
            # Thêm thông tin topic vào danh sách trả về
            topics_added.append({
                "topicId": r["TopicId"],
                "topicVersionId": r["TopicVersionId"],
                "title": r.get("Title", ""),
                "description": r.get("Description", "")[:100] + "..." if len(r.get("Description", "")) > 100 else r.get("Description", ""),  # Cắt ngắn description
            })
            
        # Thêm tất cả vào vector database
        indexed_count = svc.upsert_many(items)
        
        return {
            "indexed": indexed_count,
            "topics": topics_added,
            "total_topics": len(topics_added)
        }
