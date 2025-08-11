# -*- coding: utf-8 -*-
# Các route thao tác Topic trong Chroma: upsert/bulk-upsert/search
from flask import Blueprint, request, jsonify
from flasgger import swag_from
from dupliapp.config import settings
from dupliapp.services.topic_service import TopicsService

# Tạo blueprint cho routes quản lý đề tài
bp = Blueprint("topics", __name__, url_prefix="/topics")

@bp.post("/upsert")
@swag_from({
    'tags': ['Đề Tài'],
    'summary': 'Thêm hoặc cập nhật một đề tài',
    'description': 'Thêm hoặc cập nhật một đề tài nghiên cứu với vector embeddings',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['topicId', 'topicVersionId'],
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
                        'description': 'Mô tả đề tài',
                        'example': 'Nghiên cứu về việc áp dụng kỹ thuật ML để cải thiện kết quả y tế'
                    },
                    'objectives': {
                        'type': 'string',
                        'description': 'Mục tiêu nghiên cứu',
                        'example': 'Phát triển các mô hình ML để dự đoán bệnh tật'
                    },
                    'methodology': {
                        'type': 'string',
                        'description': 'Phương pháp nghiên cứu',
                        'example': 'Học có giám sát với dữ liệu y tế'
                    },
                    'expectedOutcomes': {
                        'type': 'string',
                        'description': 'Kết quả nghiên cứu mong đợi',
                        'example': 'Cải thiện độ chính xác dự đoán bệnh tật'
                    },
                    'requirements': {
                        'type': 'string',
                        'description': 'Yêu cầu nghiên cứu',
                        'example': 'Python, TensorFlow, dữ liệu y tế'
                    },
                    'metadata': {
                        'type': 'object',
                        'description': 'Siêu dữ liệu bổ sung',
                        'example': {'category': 'AI', 'difficulty': 'Nâng cao'}
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Đề tài được thêm/cập nhật thành công',
            'schema': {
                'type': 'object',
                'properties': {
                    'upserted': {'type': 'integer', 'example': 1}
                }
            }
        },
        400: {
            'description': 'Yêu cầu không hợp lệ - thiếu trường bắt buộc',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'Thiếu trường: topicId'}
                }
            }
        }
    }
})
def upsert():
    # Thêm hoặc cập nhật một đề tài với vector embedding
    data = request.get_json(force=True)
    svc = TopicsService()
    svc.upsert_one(data)
    return jsonify({"upserted": 1})

@bp.post("/bulk-upsert")
@swag_from({
    'tags': ['Đề Tài'],
    'summary': 'Thêm hoặc cập nhật nhiều đề tài',
    'description': 'Thêm hoặc cập nhật nhiều đề tài nghiên cứu với vector embeddings trong một thao tác',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'items': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'required': ['topicId', 'topicVersionId'],
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
                                    'description': 'Mô tả đề tài',
                                    'example': 'Nghiên cứu về việc áp dụng kỹ thuật ML để cải thiện kết quả y tế'
                                },
                                'objectives': {
                                    'type': 'string',
                                    'description': 'Mục tiêu nghiên cứu',
                                    'example': 'Phát triển các mô hình ML để dự đoán bệnh tật'
                                },
                                'methodology': {
                                    'type': 'string',
                                    'description': 'Phương pháp nghiên cứu',
                                    'example': 'Học có giám sát với dữ liệu y tế'
                                },
                                'expectedOutcomes': {
                                    'type': 'string',
                                    'description': 'Kết quả nghiên cứu mong đợi',
                                    'example': 'Cải thiện độ chính xác dự đoán bệnh tật'
                                },
                                'requirements': {
                                    'type': 'string',
                                    'description': 'Yêu cầu nghiên cứu',
                                    'example': 'Python, TensorFlow, dữ liệu y tế'
                                },
                                'metadata': {
                                    'type': 'object',
                                    'description': 'Siêu dữ liệu bổ sung',
                                    'example': {'category': 'AI', 'difficulty': 'Nâng cao'}
                                }
                            }
                        },
                        'description': 'Mảng các đối tượng đề tài cần thêm/cập nhật'
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Các đề tài được thêm/cập nhật thành công',
            'schema': {
                'type': 'object',
                'properties': {
                    'upserted': {'type': 'integer', 'example': 5}
                }
            }
        },
        400: {
            'description': 'Yêu cầu không hợp lệ - dữ liệu không hợp lệ',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'Cung cấp mảng items không rỗng'}
                }
            }
        }
    }
})
def bulk_upsert():
    # Thêm hoặc cập nhật nhiều đề tài cùng lúc (hiệu quả hơn)
    data = request.get_json(force=True)
    items = data.get("items") if isinstance(data, dict) else data
    svc = TopicsService()
    n = svc.upsert_many(items)
    return jsonify({"upserted": n})

@bp.post("/search")
@swag_from({
    'tags': ['Đề Tài'],
    'summary': 'Tìm kiếm đề tài trùng lặp',
    'description': 'Tìm kiếm các đề tài tương tự sử dụng độ tương tự ngữ nghĩa. Nếu độ tương tự >= ngưỡng, đề tài được coi là trùng lặp.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'text': {
                        'type': 'string',
                        'description': 'Văn bản trực tiếp để tìm kiếm (thay thế cho các trường riêng lẻ)',
                        'example': 'Ứng Dụng Machine Learning Trong Y Tế'
                    },
                    'title': {
                        'type': 'string',
                        'description': 'Tiêu đề đề tài',
                        'example': 'Ứng Dụng Machine Learning Trong Y Tế'
                    },
                    'description': {
                        'type': 'string',
                        'description': 'Mô tả đề tài',
                        'example': 'Nghiên cứu về việc áp dụng kỹ thuật ML để cải thiện kết quả y tế'
                    },
                    'objectives': {
                        'type': 'string',
                        'description': 'Mục tiêu nghiên cứu',
                        'example': 'Phát triển các mô hình ML để dự đoán bệnh tật'
                    },
                    'methodology': {
                        'type': 'string',
                        'description': 'Phương pháp nghiên cứu',
                        'example': 'Học có giám sát với dữ liệu y tế'
                    },
                    'expectedOutcomes': {
                        'type': 'string',
                        'description': 'Kết quả nghiên cứu mong đợi',
                        'example': 'Cải thiện độ chính xác dự đoán bệnh tật'
                    },
                    'requirements': {
                        'type': 'string',
                        'description': 'Yêu cầu nghiên cứu',
                        'example': 'Python, TensorFlow, dữ liệu y tế'
                    },
                    'topK': {
                        'type': 'integer',
                        'description': 'Số lượng kết quả tương tự hàng đầu để trả về',
                        'default': 3,
                        'example': 5
                    },
                    'threshold': {
                        'type': 'number',
                        'format': 'float',
                        'description': 'Ngưỡng độ tương tự (0.0 đến 1.0). Các đề tài có độ tương tự >= ngưỡng được coi là trùng lặp.',
                        'default': 0.7,
                        'example': 0.8
                    },
                    'metadataFilter': {
                        'type': 'object',
                        'description': 'Lọc kết quả theo siêu dữ liệu',
                        'example': {'category': 'AI'}
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Tìm kiếm hoàn thành thành công',
            'schema': {
                'type': 'object',
                'properties': {
                    'passed': {
                        'type': 'boolean',
                        'description': 'True nếu không tìm thấy trùng lặp trên ngưỡng',
                        'example': True
                    },
                    'hits': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'topicId': {'type': 'string', 'example': 'T001'},
                                'topicVersionId': {'type': 'string', 'example': 'TV001'},
                                'title': {'type': 'string', 'example': 'Machine Learning Trong Y Tế'},
                                'similarity': {'type': 'number', 'format': 'float', 'example': 0.85}
                            }
                        }
                    },
                    'suggestions': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'topicId': {'type': 'string', 'example': 'T001'},
                                'topicVersionId': {'type': 'string', 'example': 'TV001'},
                                'title': {'type': 'string', 'example': 'Machine Learning Trong Y Tế'},
                                'similarity': {'type': 'number', 'format': 'float', 'example': 0.85}
                            }
                        }
                    },
                    'threshold': {
                        'type': 'number',
                        'format': 'float',
                        'example': 0.7
                    }
                }
            }
        },
        400: {
            'description': 'Yêu cầu không hợp lệ - thiếu nội dung tìm kiếm',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'Cung cấp text hoặc các trường nội dung'}
                }
            }
        }
    }
})
def search():
    # Tìm kiếm đề tài trùng lặp dựa trên độ tương tự ngữ nghĩa
    # Nếu có kết quả >= threshold -> passed=false -> Frontend chặn submit
    data = request.get_json(force=True)
    svc = TopicsService()
    res = svc.search(
        data,
        top_k=data.get("topK") or settings.TOPK,
        threshold=data.get("threshold") or settings.THRESHOLD,
    )
    return jsonify(res)
