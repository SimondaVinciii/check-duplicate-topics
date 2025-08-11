# -*- coding: utf-8 -*-
# Repository Ä‘á»c dá»¯ liá»‡u topic tá»« SQL Server báº±ng pyodbc
from typing import List, Dict, Any, Optional
import pyodbc
from dupliapp.config import settings

SQL = r"""
WITH latest AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY TopicId ORDER BY VersionNumber DESC) AS rn
    FROM dbo.topic_versions WITH (NOLOCK)
    WHERE IsActive = 1
)
SELECT {top_clause}
    t.Id AS TopicId,
    l.Id AS TopicVersionId, 
    l.Title, l.Description, l.Objectives, l.Methodology, l.ExpectedOutcomes, l.Requirements
FROM dbo.topics t WITH (NOLOCK)
JOIN latest l ON l.TopicId = t.Id AND l.rn = 1
ORDER BY t.Id ASC
"""

class MsSqlTopicRepository:
    def __init__(self):
        if not settings.SQLSERVER_CONN:
            raise RuntimeError("SQLSERVER_CONN env var is not set")
        self.conn = pyodbc.connect(settings.SQLSERVER_CONN)

    def fetch_latest(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        cur = self.conn.cursor()
        top_clause = "TOP (?)" if limit else ""
        cur.execute(SQL.format(top_clause=top_clause), (limit,) if limit else ())
        rows = cur.fetchall()
        out: List[Dict[str, Any]] = []            
        for r in rows:
            out.append({
                "TopicId": r.TopicId,
                "TopicVersionId": r.TopicVersionId,
                "Title": r.Title,
                "Description": r.Description,
                "Objectives": r.Objectives,
                "Methodology": r.Methodology,
                "ExpectedOutcomes": r.ExpectedOutcomes,
                "Requirements": r.Requirements,
            })
        return out
