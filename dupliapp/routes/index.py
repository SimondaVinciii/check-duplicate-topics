# -*- coding: utf-8 -*-
# Route xây dựng lại index từ SQL Server (tùy chọn)
from flask import Blueprint, request, jsonify
from flasgger import swag_from
from dupliapp.services.index_service import IndexService

# Tạo blueprint cho routes xây dựng chỉ mục
bp = Blueprint("index", __name__, url_prefix="/index")

@bp.post("/topics")
@swag_from({
    'tags': ['Chỉ Mục'],
    'summary': 'Xây dựng lại chỉ mục đề tài từ SQL Server',
    'description': 'Xây dựng lại chỉ mục vector bằng cách lấy đề tài từ SQL Server và tạo embeddings. Hữu ích cho thiết lập ban đầu hoặc đồng bộ hóa dữ liệu.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': False,
            'schema': {
                'type': 'object',
                'properties': {
                    'limit': {
                        'type': 'integer',
                        'description': 'Số lượng đề tài tối đa để lập chỉ mục (tùy chọn, lập chỉ mục tất cả nếu không được chỉ định)',
                        'example': 1000
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Xây dựng lại chỉ mục hoàn thành thành công',
            'schema': {
                'type': 'object',
                'properties': {
                    'indexed': {
                        'type': 'integer',
                        'description': 'Số lượng đề tài được lập chỉ mục thành công',
                        'example': 1500
                    },
                    'total_topics': {
                        'type': 'integer',
                        'description': 'Tổng số đề tài được xử lý',
                        'example': 1500
                    },
                    'topics': {
                        'type': 'array',
                        'description': 'Danh sách các đề tài đã được thêm vào ChromaDB',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'topicId': {
                                    'type': 'string',
                                    'description': 'Định danh duy nhất cho đề tài',
                                    'example': 'T001'
                                },
                                'topicVersionId': {
                                    'type': 'string',
                                    'description': 'Định danh duy nhất cho phiên bản đề tài',
                                    'example': 'TV001'
                                },
                                'title': {
                                    'type': 'string',
                                    'description': 'Tiêu đề đề tài',
                                    'example': 'Ứng Dụng Machine Learning Trong Y Tế'
                                },
                                'description': {
                                    'type': 'string',
                                    'description': 'Mô tả đề tài (đã cắt ngắn nếu quá dài)',
                                    'example': 'Nghiên cứu về việc áp dụng kỹ thuật ML để cải thiện kết quả y tế...'
                                }
                            }
                        },
                        'example': [
                            {
                                'topicId': 'T001',
                                'topicVersionId': 'TV001',
                                'title': 'Ứng Dụng Machine Learning Trong Y Tế',
                                'description': 'Nghiên cứu về việc áp dụng kỹ thuật ML để cải thiện kết quả y tế...'
                            },
                            {
                                'topicId': 'T002',
                                'topicVersionId': 'TV002',
                                'title': 'Phát Triển Hệ Thống Quản Lý Sinh Viên',
                                'description': 'Xây dựng hệ thống quản lý thông tin sinh viên sử dụng công nghệ web...'
                            }
                        ]
                    }
                }
            }
        },
        500: {
            'description': 'Lỗi máy chủ nội bộ trong quá trình lập chỉ mục',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'Kết nối cơ sở dữ liệu thất bại'}
                }
            }
        }
    }
})
def index_topics():
    # Xây dựng lại chỉ mục vector bằng cách lấy đề tài từ SQL Server
    # Hữu ích cho thiết lập ban đầu hoặc đồng bộ hóa dữ liệu
    body = request.get_json(silent=True) or {}
    limit = body.get("limit")
    svc = IndexService()
    result = svc.build_from_sql(limit=limit)
    return jsonify(result)
