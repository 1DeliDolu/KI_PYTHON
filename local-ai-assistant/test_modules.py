#!/usr/bin/env python3
"""
Test script for Multi-Task AI Assistant
Tests all core modules individually
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_config():
    """Test configuration module"""
    try:
        from config import Config
        config = Config()
        print("✓ Config module loaded successfully")
        print(f"  - App name: {config.APP_NAME}")
        print(f"  - Version: {config.VERSION}")
        return True
    except Exception as e:
        print(f"✗ Config module failed: {e}")
        return False

def test_wikipedia():
    """Test Wikipedia module"""
    try:
        from scripts.wikipedia_query import WikipediaQuery
        wiki = WikipediaQuery()
        result = wiki.search("Python programming", max_results=1)
        if result["success"]:
            print("✓ Wikipedia module working")
            print(f"  - Found {result['total_results']} results")
        else:
            print(f"✗ Wikipedia search failed: {result['message']}")
        return result["success"]
    except Exception as e:
        print(f"✗ Wikipedia module failed: {e}")
        return False

def test_translator():
    """Test Translation module"""
    try:
        from scripts.translator import Translator
        translator = Translator()
        result = translator.translate("Hello world", "tr")
        if result["success"]:
            print("✓ Translation module working")
            print(f"  - Translation: {result['translated_text']}")
        else:
            print(f"✗ Translation failed: {result['message']}")
        return result["success"]
    except Exception as e:
        print(f"✗ Translation module failed: {e}")
        return False

def test_document_reader():
    """Test Document Reader module"""
    try:
        from scripts.document_reader import DocumentReader
        reader = DocumentReader()
        print("✓ Document Reader module loaded successfully")
        return True
    except Exception as e:
        print(f"✗ Document Reader module failed: {e}")
        return False

def test_image_analysis():
    """Test Image Analysis module"""
    try:
        from scripts.image_analysis import ImageAnalysis
        analyzer = ImageAnalysis()
        print("✓ Image Analysis module loaded successfully")
        return True
    except Exception as e:
        print(f"✗ Image Analysis module failed: {e}")
        return False

def test_video_analysis():
    """Test Video Analysis module"""
    try:
        from scripts.video_analysis import VideoAnalysis
        analyzer = VideoAnalysis()
        print("✓ Video Analysis module loaded successfully")
        return True
    except Exception as e:
        print(f"✗ Video Analysis module failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("Multi-Task AI Assistant - Module Tests")
    print("=" * 50)
    
    tests = [
        ("Configuration", test_config),
        ("Wikipedia Query", test_wikipedia),
        ("Translation", test_translator),
        ("Document Reader", test_document_reader),
        ("Image Analysis", test_image_analysis),
        ("Video Analysis", test_video_analysis)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nTesting {test_name}...")
        if test_func():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} modules working")
    print("=" * 50)
    
    if passed == total:
        print("🎉 All modules are working correctly!")
        print("\nYou can now run the main application:")
        print("  python main.py --interactive")
    else:
        print("⚠️  Some modules have issues. Check the errors above.")
        print("\nYou can still try running the main application:")
        print("  python main.py --interactive")

if __name__ == "__main__":
    main()