# -*- coding: utf-8 -*-
# Use-case build láº¡i index tá»« SQL Server (tuá»³ chá»n)
from typing import Optional
from dupliapp.repositories.topic_repository import MsSqlTopicRepository
from dupliapp.services.topic_service import TopicsService

class IndexService:
    def build_from_sql(self, limit: Optional[int] = None) -> int:
        repo = MsSqlTopicRepository()
        rows = repo.fetch_latest(limit=limit)
        svc = TopicsService()
        items = []
        for r in rows:
            items.append({
                "topicId": r["TopicId"],
                "topicVersionId": r["TopicVersionId"],
                "title": r.get("Title", ""),
                "description": r.get("Description", ""),
                "objectives": r.get("Objectives", ""),
                "methodology": r.get("Methodology", ""),
                "expectedOutcomes": r.get("ExpectedOutcomes", ""),
                "requirements": r.get("Requirements", ""),
            })
        return svc.upsert_many(items)
