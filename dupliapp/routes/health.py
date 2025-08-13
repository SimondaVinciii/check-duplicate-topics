# -*- coding: utf-8 -*-
# Route kiểm tra sức khỏe dịch vụ và thông tin cơ bản
from flask import Blueprint, jsonify
from flasgger import swag_from
from dupliapp.services.topic_service import TopicsService
from dupliapp.config import settings

# Tạo blueprint cho routes kiểm tra sức khỏe
bp = Blueprint("health", __name__)

@bp.get("/")
@swag_from({
	'tags': ['Sức Khỏe'],
	'summary': 'Lấy thông tin dịch vụ',
	'description': 'Trả về thông tin cơ bản về dịch vụ và các endpoint có sẵn',
	'responses': {
		200: {
			'description': 'Lấy thông tin dịch vụ thành công',
			'schema': {
				'type': 'object',
				'properties': {
					'service': {'type': 'string', 'example': 'duplicate-service-flask'},
					'version': {'type': 'string', 'example': '2.0.0'},
					'docs': {
						'type': 'array',
						'items': {'type': 'string'},
						'example': ['/apidocs', '/health', '/chroma/stats', '/topics/search']
					}
				}
			}
		}
	}
})
def root():
	# Trang chủ đơn giản và danh sách các route hữu ích
	embedding_type = settings.EMBEDDING_TYPE
	embedding_model = settings.MODEL_NAME if embedding_type == "sentence_transformers" else "gemini-embedding-001"
	return jsonify({
		"service": "duplicate-service-flask",
		"version": "2.0.0",
		"docs": ["/apidocs", "/health", "/chroma/stats", "/topics/search", "/topics/upsert", "/topics/bulk-upsert", "/index/topics"],
		"embeddingType": embedding_type,
		"embeddingModel": embedding_model,
	})

@bp.get("/health")
@swag_from({
	'tags': ['Sức Khỏe'],
	'summary': 'Kiểm tra sức khỏe',
	'description': 'Thực hiện kiểm tra sức khỏe và trả về số lượng vector trong cơ sở dữ liệu',
	'responses': {
		200: {
			'description': 'Kiểm tra sức khỏe thành công',
			'schema': {
				'type': 'object',
				'properties': {
					'status': {'type': 'string', 'example': 'ok'},
					'vectors': {'type': 'integer', 'example': 1500},
					'embeddingType': {'type': 'string', 'example': 'sentence_transformers'},
					'embeddingModel': {'type': 'string', 'example': 'sentence-transformers/all-mpnet-base-v2'}
				}
			}
		}
	}
})
def health():
	# Kiểm tra sức khỏe dịch vụ + số lượng vector đang có trong database
	vectors = TopicsService.count_vectors()
	embedding_type = settings.EMBEDDING_TYPE
	embedding_model = settings.MODEL_NAME if embedding_type == "sentence_transformers" else "gemini-embedding-001"
	return jsonify({
		"status": "ok",
		"vectors": vectors,
		"embeddingType": embedding_type,
		"embeddingModel": embedding_model,
	})
