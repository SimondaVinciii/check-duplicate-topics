# -*- coding: utf-8 -*-
# Build lại index từ SQL Server (tùy chọn): /index/topics
from flask import Blueprint, request, jsonify
from flasgger import swag_from
from dupliapp.services.index_service import IndexService

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
    body = request.get_json(silent=True) or {}
    limit = body.get("limit")
    svc = IndexService()
    n = svc.build_from_sql(limit=limit)
    return jsonify({"indexed": n})
