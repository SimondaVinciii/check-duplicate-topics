#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script kiểm tra và sửa lỗi cấu hình ChromaDB
Sử dụng: python fix_chroma_config.py
"""

import os
import sys
from dotenv import load_dotenv

def check_environment():
    """Kiểm tra biến môi trường"""
    print("🔍 Kiểm tra cấu hình môi trường...")
    
    load_dotenv()
    
    # Kiểm tra mode
    mode = os.getenv("CHROMA_MODE", "local").lower()
    print(f"✅ CHROMA_MODE: {mode}")
    
    if mode == "local":
        chroma_dir = os.getenv("CHROMA_DIR", "./chroma_data")
        print(f"✅ CHROMA_DIR: {chroma_dir}")
        
        # Kiểm tra thư mục
        if not os.path.exists(chroma_dir):
            print(f"📁 Tạo thư mục: {chroma_dir}")
            os.makedirs(chroma_dir, exist_ok=True)
        else:
            print(f"✅ Thư mục đã tồn tại: {chroma_dir}")
            
    elif mode == "cloud":
        required_vars = [
            "CHROMA_CLOUD_HOST",
            "CHROMA_CLOUD_API_KEY", 
            "CHROMA_CLOUD_TENANT",
            "CHROMA_CLOUD_DATABASE"
        ]
        
        missing_vars = []
        for var in required_vars:
            value = os.getenv(var)
            if not value:
                missing_vars.append(var)
            else:
                # Ẩn API key vì lý do bảo mật
                if var == "CHROMA_CLOUD_API_KEY":
                    print(f"✅ {var}: {'*' * 10}{value[-4:] if len(value) > 4 else '*' * len(value)}")
                else:
                    print(f"✅ {var}: {value}")
        
        if missing_vars:
            print(f"❌ Thiếu biến môi trường: {missing_vars}")
            return False
        else:
            print("✅ Tất cả biến cloud đã được cấu hình")
            
    return True

def test_chroma_connection():
    """Test kết nối ChromaDB"""
    print("\n🔌 Test kết nối ChromaDB...")
    
    try:
        from dupliapp.repositories.chroma_repository import ChromaTopicsRepository
        
        # Test initialization
        repo = ChromaTopicsRepository()
        print("✅ Kết nối ChromaDB thành công")
        
        # Test stats
        stats = repo.stats()
        print(f"✅ Stats: {stats}")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi kết nối: {e}")
        return False

def fix_common_issues():
    """Sửa các lỗi thường gặp"""
    print("\n🔧 Sửa lỗi thường gặp...")
    
    # Kiểm tra ChromaDB version
    try:
        import chromadb
        print(f"✅ ChromaDB version: {chromadb.__version__}")
        
        # Kiểm tra version có hỗ trợ v2 API không
        version_parts = chromadb.__version__.split('.')
        major = int(version_parts[0])
        minor = int(version_parts[1])
        
        if major > 0 or (major == 0 and minor >= 4):
            print("✅ ChromaDB version hỗ trợ v2 API")
        else:
            print("⚠️ ChromaDB version cũ, khuyến nghị upgrade")
            
    except Exception as e:
        print(f"❌ Không thể kiểm tra ChromaDB version: {e}")
    
    # Kiểm tra file .env
    env_file = ".env"
    if not os.path.exists(env_file):
        print(f"📝 Tạo file {env_file}...")
        with open(env_file, "w", encoding="utf-8") as f:
            f.write("# ChromaDB Configuration\n")
            f.write("CHROMA_MODE=local\n")
            f.write("CHROMA_DIR=./chroma_data\n")
            f.write("\n# Other configurations\n")
            f.write("HOST=0.0.0.0\n")
            f.write("PORT=8008\n")
            f.write("THRESHOLD=0.7\n")
            f.write("TOPK=3\n")
        print(f"✅ Đã tạo file {env_file}")
    else:
        print(f"✅ File {env_file} đã tồn tại")

def show_help():
    """Hiển thị hướng dẫn"""
    print("\n📖 Hướng dẫn sử dụng:")
    print("1. Local Mode (mặc định):")
    print("   CHROMA_MODE=local")
    print("   CHROMA_DIR=./chroma_data")
    print()
    print("2. Cloud Mode:")
    print("   CHROMA_MODE=cloud")
    print("   CHROMA_CLOUD_HOST=your-host.chromadb.com")
    print("   CHROMA_CLOUD_API_KEY=your-api-key")
    print("   CHROMA_CLOUD_TENANT=your-tenant-id")
    print("   CHROMA_CLOUD_DATABASE=your-database-name")
    print()
    print("3. Test kết nối:")
    print("   python test_chroma_modes.py")
    print()
    print("4. Chạy ứng dụng:")
    print("   python run.py")

def main():
    """Main function"""
    print("🚀 ChromaDB Configuration Fixer")
    print("=" * 50)
    
    # Kiểm tra môi trường
    env_ok = check_environment()
    
    # Sửa lỗi thường gặp
    fix_common_issues()
    
    # Test kết nối
    if env_ok:
        connection_ok = test_chroma_connection()
    else:
        connection_ok = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Kết quả:")
    print(f"   Environment: {'✅ OK' if env_ok else '❌ FAIL'}")
    print(f"   Connection: {'✅ OK' if connection_ok else '❌ FAIL'}")
    
    if env_ok and connection_ok:
        print("\n🎉 ChromaDB đã được cấu hình thành công!")
    else:
        print("\n⚠️ Có vấn đề với cấu hình ChromaDB")
        show_help()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
