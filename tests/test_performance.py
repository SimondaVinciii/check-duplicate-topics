# -*- coding: utf-8 -*-
# Performance tests for API endpoints
import pytest
import time
import json
from unittest.mock import patch, MagicMock

class TestAPIPerformance:
    """Performance tests for API endpoints."""
    
    def test_health_endpoint_performance(self, client, mock_topic_service):
        """Test health endpoint response time."""
        mock_topic_service.count_vectors.return_value = 1000
        
        start_time = time.time()
        response = client.get('/health')
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200
        assert response_time < 1.0  # Should respond within 1 second
    
    def test_search_endpoint_performance(self, client, mock_topic_service):
        """Test search endpoint response time."""
        search_data = {
            "title": "Đề tài test",
            "topK": 10,
            "threshold": 0.7
        }
        
        expected_response = {
            "passed": True,
            "hits": [],
            "suggestions": [],
            "threshold": 0.7
        }
        
        mock_topic_service.search.return_value = expected_response
        
        start_time = time.time()
        response = client.post('/topics/search',
                             data=json.dumps(search_data),
                             content_type='application/json')
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200
        assert response_time < 2.0  # Should respond within 2 seconds
    
    def test_bulk_upsert_performance(self, client, mock_topic_service):
        """Test bulk upsert endpoint performance with large dataset."""
        # Create large dataset
        large_dataset = {
            "items": [
                {
                    "topicId": f"T{i:03d}",
                    "topicVersionId": f"TV{i:03d}",
                    "title": f"Đề tài {i}",
                    "description": f"Mô tả đề tài {i}"
                }
                for i in range(100)  # 100 topics
            ]
        }
        
        mock_topic_service.upsert_many.return_value = 100
        
        start_time = time.time()
        response = client.post('/topics/bulk-upsert',
                             data=json.dumps(large_dataset),
                             content_type='application/json')
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200
        assert json.loads(response.data)['upserted'] == 100
        assert response_time < 5.0  # Should handle 100 topics within 5 seconds
    
    def test_concurrent_requests(self, client, mock_topic_service):
        """Test handling of concurrent requests."""
        import threading
        import queue
        
        mock_topic_service.count_vectors.return_value = 100
        mock_topic_service.search.return_value = {
            "passed": True,
            "hits": [],
            "suggestions": [],
            "threshold": 0.7
        }
        
        results = queue.Queue()
        
        def make_request(request_type):
            try:
                if request_type == 'health':
                    response = client.get('/health')
                elif request_type == 'search':
                    response = client.post('/topics/search',
                                         data=json.dumps({"title": "test"}),
                                         content_type='application/json')
                
                results.put((request_type, response.status_code))
            except Exception as e:
                results.put((request_type, f"Error: {e}"))
        
        # Start multiple concurrent requests
        threads = []
        for i in range(10):
            thread = threading.Thread(target=make_request, args=('health' if i % 2 == 0 else 'search',))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Check results
        success_count = 0
        while not results.empty():
            request_type, status_code = results.get()
            if status_code == 200:
                success_count += 1
        
        assert success_count == 10  # All requests should succeed 