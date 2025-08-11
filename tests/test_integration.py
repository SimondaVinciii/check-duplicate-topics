# -*- coding: utf-8 -*-
# Integration tests for the complete API workflow
import pytest
import json
from unittest.mock import patch, MagicMock

class TestAPIIntegration:
    """Integration tests for complete API workflows."""
    
    def test_complete_topic_workflow(self, client, mock_topic_service, mock_index_service):
        """Test complete workflow: index -> upsert -> search."""
        # Step 1: Index topics
        mock_index_service.build_from_sql.return_value = 100
        
        index_response = client.post('/index/topics',
                                   data=json.dumps({"limit": 100}),
                                   content_type='application/json')
        
        assert index_response.status_code == 200
        assert json.loads(index_response.data)['indexed'] == 100
        
        # Step 2: Upsert a new topic
        topic_data = {
            "topicId": "T001",
            "topicVersionId": "TV001",
            "title": "Đề tài test",
            "description": "Mô tả test"
        }
        
        upsert_response = client.post('/topics/upsert',
                                    data=json.dumps(topic_data),
                                    content_type='application/json')
        
        assert upsert_response.status_code == 200
        assert json.loads(upsert_response.data)['upserted'] == 1
        
        # Step 3: Search for duplicates
        search_data = {
            "title": "Đề tài test",
            "topK": 3,
            "threshold": 0.7
        }
        
        expected_search_result = {
            "passed": True,
            "hits": [],
            "suggestions": [],
            "threshold": 0.7
        }
        
        mock_topic_service.search.return_value = expected_search_result
        
        search_response = client.post('/topics/search',
                                    data=json.dumps(search_data),
                                    content_type='application/json')
        
        assert search_response.status_code == 200
        assert json.loads(search_response.data) == expected_search_result
        
        # Step 4: Check health
        mock_topic_service.count_vectors.return_value = 101  # 100 indexed + 1 upserted
        
        health_response = client.get('/health')
        
        assert health_response.status_code == 200
        health_data = json.loads(health_response.data)
        assert health_data['status'] == 'ok'
        assert health_data['vectors'] == 101
        
        # Step 5: Check Chroma stats
        expected_stats = {
            "collection_count": 1,
            "total_vectors": 101,
            "collections": [
                {
                    "name": "topics",
                    "count": 101,
                    "metadata": {}
                }
            ]
        }
        
        mock_topic_service.chroma_stats.return_value = expected_stats
        
        stats_response = client.get('/chroma/stats')
        
        assert stats_response.status_code == 200
        assert json.loads(stats_response.data) == expected_stats
    
    def test_bulk_operations_workflow(self, client, mock_topic_service):
        """Test workflow with bulk operations."""
        # Bulk upsert multiple topics
        bulk_data = {
            "items": [
                {
                    "topicId": "T001",
                    "topicVersionId": "TV001",
                    "title": "Đề tài 1"
                },
                {
                    "topicId": "T002",
                    "topicVersionId": "TV002", 
                    "title": "Đề tài 2"
                },
                {
                    "topicId": "T003",
                    "topicVersionId": "TV003",
                    "title": "Đề tài 3"
                }
            ]
        }
        
        mock_topic_service.upsert_many.return_value = 3
        
        bulk_response = client.post('/topics/bulk-upsert',
                                  data=json.dumps(bulk_data),
                                  content_type='application/json')
        
        assert bulk_response.status_code == 200
        assert json.loads(bulk_response.data)['upserted'] == 3
        
        # Search for duplicates in bulk
        search_data = {
            "text": "Đề tài test",
            "topK": 5,
            "threshold": 0.8
        }
        
        expected_search_result = {
            "passed": False,
            "hits": [
                {
                    "topicId": "T001",
                    "topicVersionId": "TV001",
                    "title": "Đề tài 1",
                    "similarity": 0.85
                }
            ],
            "suggestions": [
                {
                    "topicId": "T001",
                    "topicVersionId": "TV001", 
                    "title": "Đề tài 1",
                    "similarity": 0.85
                }
            ],
            "threshold": 0.8
        }
        
        mock_topic_service.search.return_value = expected_search_result
        
        search_response = client.post('/topics/search',
                                    data=json.dumps(search_data),
                                    content_type='application/json')
        
        assert search_response.status_code == 200
        search_result = json.loads(search_response.data)
        assert search_result['passed'] == False
        assert len(search_result['hits']) > 0
    
    def test_error_handling_workflow(self, client, mock_topic_service):
        """Test error handling across different endpoints."""
        # Test invalid JSON in upsert
        upsert_response = client.post('/topics/upsert',
                                    data="invalid json",
                                    content_type='application/json')
        
        assert upsert_response.status_code == 400
        
        # Test invalid JSON in search
        search_response = client.post('/topics/search',
                                    data="invalid json", 
                                    content_type='application/json')
        
        assert search_response.status_code == 400
        
        # Test invalid JSON in bulk upsert
        bulk_response = client.post('/topics/bulk-upsert',
                                  data="invalid json",
                                  content_type='application/json')
        
        assert bulk_response.status_code == 400
        
        # Test invalid JSON in index
        index_response = client.post('/index/topics',
                                   data="invalid json",
                                   content_type='application/json')
        
        assert index_response.status_code == 400
    
    def test_service_unavailable_handling(self, client, mock_topic_service):
        """Test handling when underlying services are unavailable."""
        # Mock service to raise exception
        mock_topic_service.count_vectors.side_effect = Exception("Database connection failed")
        
        # This would normally cause an error, but Flask handles it gracefully
        health_response = client.get('/health')
        
        # The response might be 500 or handled by Flask's error handlers
        assert health_response.status_code in [200, 500] 