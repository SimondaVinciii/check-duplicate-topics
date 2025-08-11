# -*- coding: utf-8 -*-
# Route thống kê Chroma: /chroma/stats
from flask import Blueprint, jsonify
from flasgger import swag_from
from dupliapp.services.topic_service import TopicsService

bp = Blueprint("chroma", __name__, url_prefix="/chroma")

@bp.get("/stats")
@swag_from({
    'tags': ['Chroma'],
    'summary': 'Lấy thống kê cơ sở dữ liệu Chroma',
    'description': 'Trả về thống kê chi tiết về cơ sở dữ liệu vector Chroma bao gồm thông tin collection và số lượng vector',
    'responses': {
        200: {
            'description': 'Lấy thống kê cơ sở dữ liệu thành công',
            'schema': {
                'type': 'object',
                'properties': {
                    'collection_count': {
                        'type': 'integer',
                        'description': 'Số lượng collections trong cơ sở dữ liệu',
                        'example': 1
                    },
                    'total_vectors': {
                        'type': 'integer',
                        'description': 'Tổng số vector được lưu trữ',
                        'example': 1500
                    },
                    'collections': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'name': {'type': 'string', 'example': 'topics'},
                                'count': {'type': 'integer', 'example': 1500},
                                'metadata': {'type': 'object'}
                            }
                        }
                    }
                }
            }
        }
    }
})
def stats():
    svc = TopicsService()
    return jsonify(svc.chroma_stats())
