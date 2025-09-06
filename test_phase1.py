#!/usr/bin/env python3
"""
Phase 1 Integration Test

This script tests all Phase 1 components to ensure they work together properly.
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test that all modules can be imported."""
    print("🧪 Testing imports...")
    
    try:
        # Core AI Assistant
        from ai_assistant import AIAssistantMagics, ModelPlayground, setup_assistant
        print("  ✅ AI Assistant core modules")
        
        from ai_assistant.magic_commands import AIAssistantMagics
        print("  ✅ Magic commands module")
        
        from ai_assistant.model_playground import ModelPlayground, create_playground
        print("  ✅ Model playground module")
        
        from ai_assistant.utils import setup_assistant, check_api_keys
        print("  ✅ Utility functions")
        
        # Web interface
        import flask
        import flask_socketio
        print("  ✅ Web framework dependencies")
        
        from web_interface.app import app, setup_ai_clients
        print("  ✅ Web application")
        
        # AI dependencies
        import openai
        import anthropic
        import google.generativeai as genai
        print("  ✅ AI service clients")
        
        return True
        
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
        return False


def test_magic_commands():
    """Test magic commands functionality."""
    print("\n🧪 Testing magic commands...")
    
    try:
        from ai_assistant.magic_commands import AIAssistantMagics
        
        # Create magic commands instance
        magics = AIAssistantMagics()
        print("  ✅ Magic commands instance created")
        
        # Test help functionality
        magics._show_help()
        print("  ✅ Help system works")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Magic commands error: {e}")
        return False


def test_model_playground():
    """Test model playground functionality."""
    print("\n🧪 Testing model playground...")
    
    try:
        from ai_assistant.model_playground import ModelPlayground, create_playground
        
        # Create playground instance
        playground = create_playground()
        print("  ✅ Model playground instance created")
        
        # Test usage stats (should work even without responses)
        stats = playground.get_usage_stats()
        print("  ✅ Usage statistics work")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Model playground error: {e}")
        return False


def test_web_interface():
    """Test web interface functionality."""
    print("\n🧪 Testing web interface...")
    
    try:
        from web_interface.app import app, setup_ai_clients
        
        # Test app creation
        with app.app_context():
            print("  ✅ Flask app context works")
        
        # Test AI clients setup
        setup_ai_clients()
        print("  ✅ AI clients setup works")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Web interface error: {e}")
        return False


def test_demo_notebook():
    """Test that demo notebook exists and is valid."""
    print("\n🧪 Testing demo notebook...")
    
    try:
        import nbformat
        
        demo_path = project_root / 'notebooks' / 'ai_assistant_demo.ipynb'
        if not demo_path.exists():
            print("  ❌ Demo notebook not found")
            return False
        
        # Load and validate notebook
        with open(demo_path, 'r') as f:
            nb = nbformat.read(f, as_version=4)
        
        print(f"  ✅ Demo notebook loaded ({len(nb.cells)} cells)")
        
        # Check for key cells
        markdown_cells = [cell for cell in nb.cells if cell.cell_type == 'markdown']
        code_cells = [cell for cell in nb.cells if cell.cell_type == 'code']
        
        print(f"  ✅ Notebook structure: {len(markdown_cells)} markdown, {len(code_cells)} code cells")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Demo notebook error: {e}")
        return False


def test_documentation():
    """Test that documentation files exist."""
    print("\n🧪 Testing documentation...")
    
    docs_to_check = [
        'README.md',
        'docs/PHASE1_SUMMARY.md',
        'setup_phase1.py',
        'Makefile'
    ]
    
    all_exist = True
    for doc in docs_to_check:
        doc_path = project_root / doc
        if doc_path.exists():
            print(f"  ✅ {doc}")
        else:
            print(f"  ❌ {doc} missing")
            all_exist = False
    
    return all_exist


def main():
    """Run all tests."""
    print("🚀 Phase 1 Integration Test")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Magic Commands", test_magic_commands),
        ("Model Playground", test_model_playground),
        ("Web Interface", test_web_interface),
        ("Demo Notebook", test_demo_notebook),
        ("Documentation", test_documentation)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  ❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Phase 1 is ready for use.")
        print("\n📋 Next Steps:")
        print("1. Configure API keys in .env file")
        print("2. Try the demo: jupyter lab notebooks/ai_assistant_demo.ipynb")
        print("3. Start web interface: cd web_interface && python app.py")
        print("4. Use %ai_help in any notebook for available commands")
        return 0
    else:
        print(f"\n⚠️  {total - passed} tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())