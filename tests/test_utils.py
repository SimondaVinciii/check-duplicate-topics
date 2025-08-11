# -*- coding: utf-8 -*-
# Unit tests for utility functions
import pytest
from unittest.mock import patch, MagicMock
from dupliapp.services.topic_service import TopicsService

class TestTopicServiceUtils:
    """Test cases for utility functions in TopicService."""
    
    def test_compose_topic_text_with_all_fields(self):
        """Test composing topic text with all fields present."""
        topic_data = {
            "title": "Đề tài test",
            "description": "Mô tả test",
            "objectives": "Mục tiêu test",
            "methodology": "Phương pháp test",
            "expectedOutcomes": "Kết quả mong đợi",
            "requirements": "Yêu cầu test"
        }
        
        expected_text = "Đề tài test\n\nMô tả test\n\nMục tiêu test\n\nPhương pháp test\n\nKết quả mong đợi\n\nYêu cầu test"
        
        result = TopicsService.compose_topic_text(topic_data)
        
        assert result == expected_text
    
    def test_compose_topic_text_with_mixed_case_fields(self):
        """Test composing topic text with mixed case field names."""
        topic_data = {
            "Title": "Đề tài test",
            "Description": "Mô tả test",
            "objectives": "Mục tiêu test",
            "Methodology": "Phương pháp test",
            "expectedOutcomes": "Kết quả mong đợi",
            "Requirements": "Yêu cầu test"
        }
        
        expected_text = "Đề tài test\n\nMô tả test\n\nMục tiêu test\n\nPhương pháp test\n\nKết quả mong đợi\n\nYêu cầu test"
        
        result = TopicsService.compose_topic_text(topic_data)
        
        assert result == expected_text
    
    def test_compose_topic_text_with_empty_fields(self):
        """Test composing topic text with empty fields."""
        topic_data = {
            "title": "Đề tài test",
            "description": "",
            "objectives": None,
            "methodology": "   ",
            "expectedOutcomes": "Kết quả mong đợi",
            "requirements": ""
        }
        
        expected_text = "Đề tài test\n\nKết quả mong đợi"
        
        result = TopicsService.compose_topic_text(topic_data)
        
        assert result == expected_text
    
    def test_compose_topic_text_with_only_title(self):
        """Test composing topic text with only title field."""
        topic_data = {
            "title": "Đề tài test"
        }
        
        expected_text = "Đề tài test"
        
        result = TopicsService.compose_topic_text(topic_data)
        
        assert result == expected_text
    
    def test_compose_topic_text_with_no_content(self):
        """Test composing topic text with no content."""
        topic_data = {
            "title": "",
            "description": None,
            "objectives": "",
            "methodology": "   ",
            "expectedOutcomes": "",
            "requirements": ""
        }
        
        result = TopicsService.compose_topic_text(topic_data)
        
        assert result == "" 