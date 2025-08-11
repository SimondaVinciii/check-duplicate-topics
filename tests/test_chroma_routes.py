# -*- coding: utf-8 -*-
# Unit tests for chroma routes
import pytest
import json
from unittest.mock import patch, MagicMock

class TestChromaRoutes:
    """Test cases for Chroma database statistics endpoints."""
    
    def test_chroma_stats_success(self, client, mock_topic_service):
        """Test successful retrieval of Chroma statistics."""
        expected_stats = {
            "collection_count": 1,
            "total_vectors": 1500,
            "collections": [
                {
                    "name": "topics",
                    "count": 1500,
                    "metadata": {}
                }
            ]
        }
        
        mock_topic_service.chroma_stats.return_value = expected_stats
        
        response = client.get('/chroma/stats')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data == expected_stats
        mock_topic_service.chroma_stats.assert_called_once()
    
    def test_chroma_stats_empty_database(self, client, mock_topic_service):
        """Test Chroma stats with empty database."""
        expected_stats = {
            "collection_count": 0,
            "total_vectors": 0,
            "collections": []
        }
        
        mock_topic_service.chroma_stats.return_value = expected_stats
        
        response = client.get('/chroma/stats')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['collection_count'] == 0
        assert data['total_vectors'] == 0
        assert len(data['collections']) == 0
    
    def test_chroma_stats_multiple_collections(self, client, mock_topic_service):
        """Test Chroma stats with multiple collections."""
        expected_stats = {
            "collection_count": 2,
            "total_vectors": 2500,
            "collections": [
                {
                    "name": "topics",
                    "count": 1500,
                    "metadata": {"description": "Research topics"}
                },
                {
                    "name": "documents", 
                    "count": 1000,
                    "metadata": {"description": "Research documents"}
                }
            ]
        }
        
        mock_topic_service.chroma_stats.return_value = expected_stats
        
        response = client.get('/chroma/stats')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['collection_count'] == 2
        assert data['total_vectors'] == 2500
        assert len(data['collections']) == 2
        assert data['collections'][0]['name'] == 'topics'
        assert data['collections'][1]['name'] == 'documents'
    
    def test_chroma_stats_large_database(self, client, mock_topic_service):
        """Test Chroma stats with large database."""
        expected_stats = {
            "collection_count": 1,
            "total_vectors": 100000,
            "collections": [
                {
                    "name": "topics",
                    "count": 100000,
                    "metadata": {}
                }
            ]
        }
        
        mock_topic_service.chroma_stats.return_value = expected_stats
        
        response = client.get('/chroma/stats')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['total_vectors'] == 100000
        assert data['collections'][0]['count'] == 100000 