# -*- coding: utf-8 -*-
# Unit tests for topics routes
import pytest
import json
from unittest.mock import patch, MagicMock

class TestTopicsRoutes:
    """Test cases for topic management endpoints."""
    
    def test_upsert_single_topic_success(self, client, mock_topic_service, sample_topic_data):
        """Test successful upsert of a single topic."""
        response = client.post('/topics/upsert', 
                             data=json.dumps(sample_topic_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['upserted'] == 1
        mock_topic_service.upsert_one.assert_called_once_with(sample_topic_data)
    
    def test_upsert_single_topic_missing_required_fields(self, client, mock_topic_service):
        """Test upsert with missing required fields."""
        incomplete_data = {
            "title": "Đề tài test",
            "description": "Mô tả test"
            # Missing topicId and topicVersionId
        }
        
        # Mock the service to raise ValueError
        mock_topic_service.upsert_one.side_effect = ValueError("Missing field: topicId")
        
        response = client.post('/topics/upsert',
                             data=json.dumps(incomplete_data),
                             content_type='application/json')
        
        assert response.status_code == 200  # Flask doesn't automatically handle exceptions
        # The error would be handled by the service layer
    
    def test_upsert_single_topic_invalid_json(self, client):
        """Test upsert with invalid JSON."""
        response = client.post('/topics/upsert',
                             data="invalid json",
                             content_type='application/json')
        
        assert response.status_code == 400
    
    def test_bulk_upsert_success(self, client, mock_topic_service, sample_bulk_data):
        """Test successful bulk upsert of multiple topics."""
        mock_topic_service.upsert_many.return_value = 2
        
        response = client.post('/topics/bulk-upsert',
                             data=json.dumps(sample_bulk_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['upserted'] == 2
        mock_topic_service.upsert_many.assert_called_once_with(sample_bulk_data['items'])
    
    def test_bulk_upsert_empty_items(self, client, mock_topic_service):
        """Test bulk upsert with empty items array."""
        empty_data = {"items": []}
        mock_topic_service.upsert_many.side_effect = ValueError("Provide a non-empty 'items' array")
        
        response = client.post('/topics/bulk-upsert',
                             data=json.dumps(empty_data),
                             content_type='application/json')
        
        assert response.status_code == 200  # Error handled by service layer
    
    def test_bulk_upsert_direct_array(self, client, mock_topic_service):
        """Test bulk upsert with direct array instead of object with items."""
        direct_array = [
            {
                "topicId": "T001",
                "topicVersionId": "TV001",
                "title": "Đề tài 1"
            }
        ]
        mock_topic_service.upsert_many.return_value = 1
        
        response = client.post('/topics/bulk-upsert',
                             data=json.dumps(direct_array),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['upserted'] == 1
        mock_topic_service.upsert_many.assert_called_once_with(direct_array)
    
    def test_search_topics_success(self, client, mock_topic_service, sample_search_data):
        """Test successful topic search."""
        expected_response = {
            "passed": True,
            "hits": [
                {
                    "topicId": "T001",
                    "topicVersionId": "TV001", 
                    "title": "Đề tài tương tự",
                    "similarity": 0.65
                }
            ],
            "suggestions": [
                {
                    "topicId": "T001",
                    "topicVersionId": "TV001",
                    "title": "Đề tài tương tự",
                    "similarity": 0.65
                }
            ],
            "threshold": 0.8
        }
        
        mock_topic_service.search.return_value = expected_response
        
        response = client.post('/topics/search',
                             data=json.dumps(sample_search_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data == expected_response
        mock_topic_service.search.assert_called_once()
    
    def test_search_topics_with_text_only(self, client, mock_topic_service):
        """Test search with text field only."""
        search_data = {
            "text": "Ứng Dụng Machine Learning Trong Y Tế",
            "topK": 3,
            "threshold": 0.7
        }
        
        expected_response = {
            "passed": False,
            "hits": [],
            "suggestions": [],
            "threshold": 0.7
        }
        
        mock_topic_service.search.return_value = expected_response
        
        response = client.post('/topics/search',
                             data=json.dumps(search_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data == expected_response
    
    def test_search_topics_with_metadata_filter(self, client, mock_topic_service):
        """Test search with metadata filter."""
        search_data = {
            "title": "Đề tài test",
            "metadataFilter": {"category": "AI"},
            "topK": 5,
            "threshold": 0.8
        }
        
        expected_response = {
            "passed": True,
            "hits": [],
            "suggestions": [],
            "threshold": 0.8
        }
        
        mock_topic_service.search.return_value = expected_response
        
        response = client.post('/topics/search',
                             data=json.dumps(search_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data == expected_response
    
    def test_search_topics_no_content(self, client, mock_topic_service):
        """Test search with no content provided."""
        search_data = {}
        
        expected_response = {"error": "Provide either 'text' or the content fields"}
        mock_topic_service.search.return_value = expected_response
        
        response = client.post('/topics/search',
                             data=json.dumps(search_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data == expected_response
    
    def test_search_topics_duplicate_found(self, client, mock_topic_service):
        """Test search when duplicate is found (passed=False)."""
        search_data = {
            "title": "Đề tài test",
            "topK": 3,
            "threshold": 0.7
        }
        
        expected_response = {
            "passed": False,
            "hits": [
                {
                    "topicId": "T001",
                    "topicVersionId": "TV001",
                    "title": "Đề tài trùng lặp",
                    "similarity": 0.85
                }
            ],
            "suggestions": [
                {
                    "topicId": "T001", 
                    "topicVersionId": "TV001",
                    "title": "Đề tài trùng lặp",
                    "similarity": 0.85
                }
            ],
            "threshold": 0.7
        }
        
        mock_topic_service.search.return_value = expected_response
        
        response = client.post('/topics/search',
                             data=json.dumps(search_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['passed'] == False
        assert len(data['hits']) > 0
        assert data['hits'][0]['similarity'] >= data['threshold'] 