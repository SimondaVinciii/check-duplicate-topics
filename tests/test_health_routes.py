# -*- coding: utf-8 -*-
# Unit tests for health routes
import pytest
import json
from unittest.mock import patch

class TestHealthRoutes:
    """Test cases for health check endpoints."""
    
    def test_root_endpoint(self, client):
        """Test the root endpoint returns service information."""
        response = client.get('/')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert 'service' in data
        assert 'version' in data
        assert 'docs' in data
        assert data['service'] == 'duplicate-service-flask'
        assert data['version'] == '2.0.0'
        assert isinstance(data['docs'], list)
        assert '/apidocs' in data['docs']
        assert '/health' in data['docs']
    
    def test_health_endpoint_success(self, client, mock_topic_service):
        """Test health endpoint returns correct status and vector count."""
        # Mock the count_vectors method
        mock_topic_service.count_vectors.return_value = 1500
        
        response = client.get('/health')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['status'] == 'ok'
        assert data['vectors'] == 1500
    
    def test_health_endpoint_zero_vectors(self, client, mock_topic_service):
        """Test health endpoint with zero vectors."""
        mock_topic_service.count_vectors.return_value = 0
        
        response = client.get('/health')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['status'] == 'ok'
        assert data['vectors'] == 0
    
    def test_health_endpoint_large_vector_count(self, client, mock_topic_service):
        """Test health endpoint with large vector count."""
        mock_topic_service.count_vectors.return_value = 100000
        
        response = client.get('/health')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['status'] == 'ok'
        assert data['vectors'] == 100000 