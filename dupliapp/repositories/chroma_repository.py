# -*- coding: utf-8 -*-
"""
Repository để tương tác với cơ sở dữ liệu vector ChromaDB
ChromaDB là một cơ sở dữ liệu vector mã nguồn mở, được sử dụng để lưu trữ và tìm kiếm
các vector embeddings của đề tài nghiên cứu.
Hỗ trợ cả ChromaDB local và ChromaDB cloud.
"""
from typing import List, Dict, Any, Optional
import os
import chromadb
from dupliapp.config import settings

class ChromaTopicsRepository:
    """
    Repository class để quản lý dữ liệu đề tài trong ChromaDB
    
    Chức năng chính:
    - Khởi tạo kết nối với ChromaDB (local hoặc cloud)
    - Thêm/cập nhật vector embeddings của đề tài
    - Tìm kiếm đề tài tương tự dựa trên vector similarity
    - Đếm số lượng vector và lấy thống kê database
    """
    
    # Tên collection trong ChromaDB để lưu trữ đề tài
    COLLECTION = "topics_v1"

    def __init__(self):
        """
        Khởi tạo repository và kết nối với ChromaDB
        
        Quy trình:
        1. Kiểm tra mode (local/cloud)
        2. Tạo thư mục lưu trữ ChromaDB nếu chưa tồn tại (local mode)
        3. Kết nối với ChromaDB (local hoặc cloud)
        4. Lấy collection hiện có hoặc tạo mới nếu chưa có
        5. Cấu hình collection với cosine similarity space
        """
        
        # Khởi tạo client dựa trên mode
        if settings.CHROMA_MODE.lower() == "cloud":
            self._init_cloud_client()
        else:
            self._init_local_client()
            
        # Lấy hoặc tạo collection
        self._get_or_create_collection()

    def _init_local_client(self):
        """Khởi tạo ChromaDB local client"""
        # Tạo thư mục lưu trữ ChromaDB nếu chưa tồn tại
        os.makedirs(settings.CHROMA_DIR, exist_ok=True)
        
        # Khởi tạo client kết nối với ChromaDB (persistent storage)
        self.client = chromadb.PersistentClient(path=settings.CHROMA_DIR)
        self.mode = "local"

    def _init_cloud_client(self):
        """Khởi tạo ChromaDB cloud client"""
        # Kiểm tra các thông tin cần thiết cho cloud
        if not settings.CHROMA_CLOUD_HOST:
            raise ValueError("CHROMA_CLOUD_HOST is required for cloud mode")
        if not settings.CHROMA_CLOUD_API_KEY:
            raise ValueError("CHROMA_CLOUD_API_KEY is required for cloud mode")
        if not settings.CHROMA_CLOUD_TENANT:
            raise ValueError("CHROMA_CLOUD_TENANT is required for cloud mode")
        if not settings.CHROMA_CLOUD_DATABASE:
            raise ValueError("CHROMA_CLOUD_DATABASE is required for cloud mode")
        
        # Khởi tạo cloud client với v2 API
        # Sử dụng tenant và database parameters thay vì headers
        # Bỏ qua validation để tránh lỗi v1 API deprecated
        try:
            self.client = chromadb.HttpClient(
                host=settings.CHROMA_CLOUD_HOST,
                port=settings.CHROMA_CLOUD_PORT,
                ssl=settings.CHROMA_CLOUD_SSL,
                headers={
                    "X-Chroma-Token": settings.CHROMA_CLOUD_API_KEY
                },
                tenant=settings.CHROMA_CLOUD_TENANT,
                database=settings.CHROMA_CLOUD_DATABASE
            )
        except Exception as e:
            # Nếu lỗi validation, thử cách khác - bỏ qua tenant validation
            print(f"⚠️ Warning: Tenant validation failed, trying direct connection: {e}")
            self.client = chromadb.HttpClient(
                host=settings.CHROMA_CLOUD_HOST,
                port=settings.CHROMA_CLOUD_PORT,
                ssl=settings.CHROMA_CLOUD_SSL,
                headers={
                    "X-Chroma-Token": settings.CHROMA_CLOUD_API_KEY,
                    "X-Chroma-Tenant": settings.CHROMA_CLOUD_TENANT,
                    "X-Chroma-Database": settings.CHROMA_CLOUD_DATABASE
                }
            )
        
        self.mode = "cloud"

    def _get_or_create_collection(self):
        """Lấy collection hiện có hoặc tạo mới"""
        try:
            # Thử lấy collection hiện có
            self.col = self.client.get_collection(self.COLLECTION)
        except Exception:
            # Nếu collection chưa tồn tại, tạo mới với cấu hình cosine similarity
            # hnsw:space="cosine" sử dụng thuật toán HNSW với cosine distance
            self.col = self.client.create_collection(
                name=self.COLLECTION, 
                metadata={"hnsw:space": "cosine"}
            )

    def upsert(self, ids: List[str], embeddings: List[List[float]], 
               metadatas: List[Dict[str, Any]], documents: List[str]):
        """
        Thêm hoặc cập nhật vector embeddings vào ChromaDB
        
        Args:
            ids: Danh sách ID duy nhất cho mỗi vector (format: "tv:TopicVersionId")
            embeddings: Danh sách vector embeddings (numpy arrays)
            metadatas: Danh sách metadata cho mỗi vector (thông tin đề tài)
            documents: Danh sách text gốc được sử dụng để tạo embeddings
            
        Chức năng:
        - Nếu ID đã tồn tại: cập nhật vector và metadata
        - Nếu ID chưa tồn tại: thêm mới vector
        - Hỗ trợ batch operations để tối ưu hiệu suất
        """
        self.col.upsert(
            ids=ids, 
            embeddings=embeddings, 
            metadatas=metadatas, 
            documents=documents
        )

    def query(self, query_embedding: List[float], n_results: int, 
              where: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Tìm kiếm vector tương tự dựa trên query embedding
        
        Args:
            query_embedding: Vector embedding của query cần tìm kiếm
            n_results: Số lượng kết quả tương tự nhất cần trả về
            where: Điều kiện lọc kết quả theo metadata (tùy chọn)
            
        Returns:
            Dict chứa:
            - metadatas: Danh sách metadata của các vector tương tự
            - distances: Danh sách khoảng cách (distance) tương ứng
            
        Chức năng:
        - Sử dụng cosine similarity để tìm vector gần nhất
        - Trả về kết quả được sắp xếp theo độ tương tự giảm dần
        - Hỗ trợ lọc kết quả theo metadata
        """
        # Thực hiện query tìm kiếm vector tương tự
        res = self.col.query(
            query_embeddings=[query_embedding], 
            n_results=n_results, 
            where=where
        )
        
        # Chroma trả về nested list, ta flatten để dễ sử dụng
        # Ví dụ: res["metadatas"] = [[meta1, meta2, meta3]] -> [meta1, meta2, meta3]
        out = {"metadatas": [], "distances": []}
        
        if res and res.get("metadatas"):
            # Lấy metadata và distances từ kết quả nested
            metas = res["metadatas"][0]  # Lấy list đầu tiên
            dists = res.get("distances", [[0]*len(metas)])[0]  # Lấy list đầu tiên của distances
            
            # Ghép metadata và distance tương ứng
            for m, d in zip(metas, dists):
                out["metadatas"].append(m)
                out["distances"].append(d)
                
        return out

    def count(self) -> int:
        """
        Đếm tổng số vector trong collection hiện tại
        
        Returns:
            Số lượng vector trong collection
            Trả về 0 nếu có lỗi xảy ra
            
        Chức năng:
        - Kiểm tra sức khỏe database
        - Cung cấp thông tin cho monitoring
        """
        try:
            return int(self.col.count())
        except Exception:
            # Trả về 0 nếu không thể đếm (collection rỗng hoặc lỗi)
            return 0

    def stats(self) -> Dict[str, Any]:
        """
        Lấy thống kê chi tiết về ChromaDB và tất cả collections
        
        Returns:
            Dict chứa thông tin:
            - mode: "local" hoặc "cloud"
            - path: Đường dẫn lưu trữ ChromaDB (local mode)
            - host: Host ChromaDB (cloud mode)
            - activeCollection: Tên collection đang sử dụng
            - activeCount: Số vector trong collection hiện tại
            - collections: Danh sách tất cả collections và số vector
            
        Chức năng:
        - Monitoring và debugging
        - Kiểm tra trạng thái database
        - Cung cấp thông tin cho admin dashboard
        """
        try:
            collections = []
            
            # Duyệt qua tất cả collections trong database
            for c in self.client.list_collections():
                try:
                    # Lấy collection và đếm số vector
                    col = self.client.get_collection(c.name)
                    cnt = int(col.count())
                except Exception:
                    # Nếu không thể đếm, gán 0
                    cnt = 0
                    
                collections.append({
                    "name": c.name, 
                    "count": cnt
                })
                
            # Thông tin cơ bản
            base_info = {
                "mode": self.mode,
                "activeCollection": self.COLLECTION,
                "activeCount": self.count(),
                "collections": collections
            }
            
            # Thêm thông tin cụ thể cho từng mode
            if self.mode == "local":
                base_info["path"] = settings.CHROMA_DIR
            else:
                base_info["host"] = settings.CHROMA_CLOUD_HOST
                base_info["database"] = settings.CHROMA_CLOUD_DATABASE
                base_info["tenant"] = settings.CHROMA_CLOUD_TENANT
                
            return base_info
            
        except Exception as e:
            # Trả về thông báo lỗi nếu có vấn đề
            return {"error": str(e), "mode": self.mode}
