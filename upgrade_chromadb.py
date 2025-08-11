#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script upgrade ChromaDB và test kết nối
Sử dụng: python upgrade_chromadb.py
"""

import os
import sys
import subprocess
from dotenv import load_dotenv

def upgrade_chromadb():
    """Upgrade ChromaDB lên version mới nhất"""
    print("🔄 Upgrading ChromaDB...")
    
    try:
        # Upgrade ChromaDB
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "--upgrade", "chromadb"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ ChromaDB upgraded successfully")
            print(result.stdout)
        else:
            print("❌ Failed to upgrade ChromaDB")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error upgrading ChromaDB: {e}")
        return False
    
    return True

def check_chromadb_version():
    """Kiểm tra ChromaDB version"""
    print("\n📋 Checking ChromaDB version...")
    
    try:
        import chromadb
        print(f"✅ ChromaDB version: {chromadb.__version__}")
        
        # Kiểm tra version có hỗ trợ v2 API không
        version_parts = chromadb.__version__.split('.')
        major = int(version_parts[0])
        minor = int(version_parts[1])
        
        if major > 0 or (major == 0 and minor >= 4):
            print("✅ ChromaDB version hỗ trợ v2 API")
            return True
        else:
            print("⚠️ ChromaDB version cũ, cần upgrade")
            return False
            
    except Exception as e:
        print(f"❌ Không thể kiểm tra ChromaDB version: {e}")
        return False

def test_connection():
    """Test kết nối ChromaDB"""
    print("\n🔌 Testing ChromaDB connection...")
    
    load_dotenv()
    
    try:
        from dupliapp.repositories.chroma_repository import ChromaTopicsRepository
        
        # Test initialization
        repo = ChromaTopicsRepository()
        print("✅ ChromaDB connection successful")
        
        # Test stats
        stats = repo.stats()
        print(f"✅ Stats: {stats}")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def show_troubleshooting():
    """Hiển thị hướng dẫn troubleshooting"""
    print("\n🔧 Troubleshooting Guide:")
    print("1. Nếu lỗi v1 API deprecated:")
    print("   - Đã được sửa trong code mới")
    print("   - Sử dụng fallback connection method")
    print()
    print("2. Nếu lỗi tenant validation:")
    print("   - Kiểm tra tenant ID có đúng không")
    print("   - Đảm bảo API key có quyền truy cập")
    print()
    print("3. Nếu lỗi SSL:")
    print("   - Thử CHROMA_CLOUD_SSL=false")
    print("   - Kiểm tra certificate")
    print()
    print("4. Nếu vẫn lỗi:")
    print("   - Sử dụng local mode: CHROMA_MODE=local")
    print("   - Hoặc liên hệ ChromaDB support")

def main():
    """Main function"""
    print("🚀 ChromaDB Upgrade & Test")
    print("=" * 50)
    
    # Upgrade ChromaDB
    upgrade_ok = upgrade_chromadb()
    
    # Check version
    version_ok = check_chromadb_version()
    
    # Test connection
    connection_ok = test_connection()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Results:")
    print(f"   Upgrade: {'✅ OK' if upgrade_ok else '❌ FAIL'}")
    print(f"   Version: {'✅ OK' if version_ok else '❌ FAIL'}")
    print(f"   Connection: {'✅ OK' if connection_ok else '❌ FAIL'}")
    
    if connection_ok:
        print("\n🎉 ChromaDB is working correctly!")
    else:
        print("\n⚠️ ChromaDB has issues")
        show_troubleshooting()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
