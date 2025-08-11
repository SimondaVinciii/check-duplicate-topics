# -*- coding: utf-8 -*-
# Unit tests for index routes
import pytest
import json
from unittest.mock import patch, MagicMock

class TestIndexRoutes:
    """Test cases for index management endpoints."""
    
    def test_index_topics_success(self, client, mock_index_service):
        """Test successful topic indexing."""
        mock_index_service.build_from_sql.return_value = 1500
        
        request_data = {"limit": 1000}
        
        response = client.post('/index/topics',
                             data=json.dumps(request_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['indexed'] == 1500
        mock_index_service.build_from_sql.assert_called_once_with(limit=1000)
    
    def test_index_topics_no_limit(self, client, mock_index_service):
        """Test topic indexing without limit parameter."""
        mock_index_service.build_from_sql.return_value = 2000
        
        response = client.post('/index/topics',
                             data=json.dumps({}),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['indexed'] == 2000
        mock_index_service.build_from_sql.assert_called_once_with(limit=None)
    
    def test_index_topics_empty_request(self, client, mock_index_service):
        """Test topic indexing with empty request body."""
        mock_index_service.build_from_sql.return_value = 500
        
        response = client.post('/index/topics',
                             data='',
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['indexed'] == 500
        mock_index_service.build_from_sql.assert_called_once_with(limit=None)
    
    def test_index_topics_invalid_json(self, client):
        """Test topic indexing with invalid JSON."""
        response = client.post('/index/topics',
                             data="invalid json",
                             content_type='application/json')
        
        assert response.status_code == 400
    
    def test_index_topics_zero_indexed(self, client, mock_index_service):
        """Test topic indexing when no topics are indexed."""
        mock_index_service.build_from_sql.return_value = 0
        
        response = client.post('/index/topics',
                             data=json.dumps({"limit": 100}),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['indexed'] == 0
    
    def test_index_topics_large_limit(self, client, mock_index_service):
        """Test topic indexing with large limit."""
        mock_index_service.build_from_sql.return_value = 10000
        
        request_data = {"limit": 10000}
        
        response = client.post('/index/topics',
                             data=json.dumps(request_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['indexed'] == 10000
        mock_index_service.build_from_sql.assert_called_once_with(limit=10000)
    
    def test_index_topics_with_additional_fields(self, client, mock_index_service):
        """Test topic indexing with additional fields in request (should be ignored)."""
        mock_index_service.build_from_sql.return_value = 100
        
        request_data = {
            "limit": 100,
            "additional_field": "should_be_ignored",
            "another_field": 123
        }
        
        response = client.post('/index/topics',
                             data=json.dumps(request_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['indexed'] == 100
        # Only limit should be passed to the service
        mock_index_service.build_from_sql.assert_called_once_with(limit=100) 