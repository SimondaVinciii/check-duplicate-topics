# -*- coding: utf-8 -*-
# Test configuration and fixtures
import pytest
import tempfile
import os
from unittest.mock import patch, MagicMock
from dupliapp.main import create_app
from dupliapp.config import settings

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Create a temporary directory for test data
    with tempfile.TemporaryDirectory() as temp_dir:
        # Mock environment variables for testing
        with patch.dict(os.environ, {
            'CHROMA_DIR': temp_dir,
            'MODEL_NAME': 'sentence-transformers/all-MiniLM-L6-v2',
            'THRESHOLD': '0.7',
            'TOPK': '3'
        }):
            app = create_app()
            app.config['TESTING'] = True
            app.config['WTF_CSRF_ENABLED'] = False
            
            yield app

@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create a test runner for the app's Click commands."""
    return app.test_cli_runner()

@pytest.fixture
def mock_topic_service():
    """Mock TopicsService for testing."""
    with patch('dupliapp.services.topic_service.TopicsService') as mock:
        service_instance = MagicMock()
        mock.return_value = service_instance
        yield service_instance

@pytest.fixture
def mock_index_service():
    """Mock IndexService for testing."""
    with patch('dupliapp.services.index_service.IndexService') as mock:
        service_instance = MagicMock()
        mock.return_value = service_instance
        yield service_instance

@pytest.fixture
def sample_topic_data():
    """Sample topic data for testing."""
    return {
        "topicId": "T001",
        "topicVersionId": "TV001",
        "title": "Ứng Dụng Machine Learning Trong Y Tế",
        "description": "Nghiên cứu về việc áp dụng kỹ thuật ML để cải thiện kết quả y tế",
        "objectives": "Phát triển các mô hình ML để dự đoán bệnh tật",
        "methodology": "Học có giám sát với dữ liệu y tế",
        "expectedOutcomes": "Cải thiện độ chính xác dự đoán bệnh tật",
        "requirements": "Python, TensorFlow, dữ liệu y tế",
        "metadata": {"category": "AI", "difficulty": "Nâng cao"}
    }

@pytest.fixture
def sample_search_data():
    """Sample search data for testing."""
    return {
        "title": "Ứng Dụng Machine Learning Trong Y Tế",
        "description": "Nghiên cứu về việc áp dụng kỹ thuật ML để cải thiện kết quả y tế",
        "topK": 5,
        "threshold": 0.8
    }

@pytest.fixture
def sample_bulk_data():
    """Sample bulk upsert data for testing."""
    return {
        "items": [
            {
                "topicId": "T001",
                "topicVersionId": "TV001",
                "title": "Đề tài 1",
                "description": "Mô tả đề tài 1"
            },
            {
                "topicId": "T002", 
                "topicVersionId": "TV002",
                "title": "Đề tài 2",
                "description": "Mô tả đề tài 2"
            }
        ]
    } 