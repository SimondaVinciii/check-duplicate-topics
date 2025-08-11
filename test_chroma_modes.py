#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script test để kiểm tra ChromaDB Local và Cloud modes
Sử dụng: python test_chroma_modes.py
"""

import os
import sys
import json
from dotenv import load_dotenv

# Thêm thư mục gốc vào path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_local_mode():
    """Test ChromaDB local mode"""
    print("🔧 Testing ChromaDB Local Mode...")
    
    # Set environment variables for local mode
    os.environ["CHROMA_MODE"] = "local"
    os.environ["CHROMA_DIR"] = "./chroma_data_test"
    
    try:
        from dupliapp.repositories.chroma_repository import ChromaTopicsRepository
        
        # Test initialization
        repo = ChromaTopicsRepository()
        print("✅ Local mode initialization successful")
        
        # Test stats
        stats = repo.stats()
        print(f"✅ Local stats: {json.dumps(stats, indent=2)}")
        
        # Test count
        count = repo.count()
        print(f"✅ Local count: {count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Local mode test failed: {e}")
        return False

def test_cloud_mode():
    """Test ChromaDB cloud mode"""
    print("\n☁️ Testing ChromaDB Cloud Mode...")
    
    # Check if cloud credentials are available
    required_vars = [
        "CHROMA_CLOUD_HOST",
        "CHROMA_CLOUD_API_KEY", 
        "CHROMA_CLOUD_TENANT",
        "CHROMA_CLOUD_DATABASE"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️ Cloud mode test skipped - missing variables: {missing_vars}")
        print("💡 Set these environment variables to test cloud mode:")
        for var in missing_vars:
            print(f"   {var}=your-value")
        return False
    
    # Set environment variables for cloud mode
    os.environ["CHROMA_MODE"] = "cloud"
    
    try:
        from dupliapp.repositories.chroma_repository import ChromaTopicsRepository
        
        # Test initialization
        repo = ChromaTopicsRepository()
        print("✅ Cloud mode initialization successful")
        
        # Test stats
        stats = repo.stats()
        print(f"✅ Cloud stats: {json.dumps(stats, indent=2)}")
        
        # Test count
        count = repo.count()
        print(f"✅ Cloud count: {count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Cloud mode test failed: {e}")
        return False

def test_config():
    """Test configuration loading"""
    print("\n⚙️ Testing Configuration...")
    
    try:
        from dupliapp.config import settings
        
        print(f"✅ CHROMA_MODE: {settings.CHROMA_MODE}")
        print(f"✅ CHROMA_DIR: {settings.CHROMA_DIR}")
        
        if settings.CHROMA_MODE == "cloud":
            print(f"✅ CHROMA_CLOUD_HOST: {settings.CHROMA_CLOUD_HOST}")
            print(f"✅ CHROMA_CLOUD_PORT: {settings.CHROMA_CLOUD_PORT}")
            print(f"✅ CHROMA_CLOUD_SSL: {settings.CHROMA_CLOUD_SSL}")
            print(f"✅ CHROMA_CLOUD_TENANT: {settings.CHROMA_CLOUD_TENANT}")
            print(f"✅ CHROMA_CLOUD_DATABASE: {settings.CHROMA_CLOUD_DATABASE}")
            # Don't print API key for security
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 ChromaDB Mode Testing")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Test configuration
    config_ok = test_config()
    
    # Test local mode
    local_ok = test_local_mode()
    
    # Test cloud mode
    cloud_ok = test_cloud_mode()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"   Configuration: {'✅ PASS' if config_ok else '❌ FAIL'}")
    print(f"   Local Mode: {'✅ PASS' if local_ok else '❌ FAIL'}")
    print(f"   Cloud Mode: {'✅ PASS' if cloud_ok else '⚠️ SKIP' if not cloud_ok else '❌ FAIL'}")
    
    if local_ok:
        print("\n💡 Local mode is working correctly!")
    if cloud_ok:
        print("💡 Cloud mode is working correctly!")
    
    if not local_ok and not cloud_ok:
        print("\n❌ Both modes failed. Please check your configuration.")
        return 1
    
    print("\n✅ Testing completed successfully!")
    return 0

if __name__ == "__main__":
    exit(main())
