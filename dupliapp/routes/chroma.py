# -*- coding: utf-8 -*-
# Route thống kê ChromaDB - cung cấp thông tin về vector database
from flask import Blueprint, jsonify
from flasgger import swag_from
from dupliapp.services.topic_service import TopicsService

# Tạo blueprint cho routes quản lý ChromaDB
bp = Blueprint("chroma", __name__, url_prefix="/chroma")

@bp.get("/stats")
@swag_from({
    'tags': ['Chroma'],
    'summary': 'Lấy thống kê cơ sở dữ liệu ChromaDB',
    'description': 'Trả về thống kê chi tiết về cơ sở dữ liệu vector ChromaDB bao gồm thông tin collection và số lượng vector',
    'responses': {
        200: {
            'description': 'Lấy thống kê cơ sở dữ liệu thành công',
            'schema': {
                'type': 'object',
                'properties': {
                    'path': {
                        'type': 'string',
                        'description': 'Đường dẫn lưu trữ ChromaDB',
                        'example': './chroma_data'
                    },
                    'activeCollection': {
                        'type': 'string',
                        'description': 'Tên collection đang hoạt động',
                        'example': 'topics_v1'
                    },
                    'activeCount': {
                        'type': 'integer',
                        'description': 'Số lượng vector trong collection hiện tại',
                        'example': 1500
                    },
                    'collections': {
                        'type': 'array',
                        'description': 'Danh sách tất cả collections và số vector',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'name': {
                                    'type': 'string',
                                    'description': 'Tên collection',
                                    'example': 'topics_v1'
                                },
                                'count': {
                                    'type': 'integer',
                                    'description': 'Số lượng vector trong collection',
                                    'example': 1500
                                }
                            }
                        },
                        'example': [
                            {
                                'name': 'topics_v1',
                                'count': 1500
                            }
                        ]
                    }
                }
            }
        },
        500: {
            'description': 'Lỗi máy chủ nội bộ khi truy cập ChromaDB',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'description': 'Thông báo lỗi chi tiết',
                        'example': 'Không thể kết nối đến ChromaDB'
                    }
                }
            }
        }
    }
})
def stats():
    # Lấy thống kê chi tiết về cơ sở dữ liệu vector ChromaDB
    svc = TopicsService()
    return jsonify(svc.chroma_stats())
