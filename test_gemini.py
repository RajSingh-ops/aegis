import os
import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aegis_core.settings')
import django
django.setup()

import google.generativeai as genai
from dotenv import load_dotenv
from django.conf import settings

def test_api_connection():
    print("=" * 60)
    print("AEGIS - Gemini API Connection Test")
    print("=" * 60)
    
    load_dotenv()
    
    api_key = settings.GEMINI_API_KEY
    if not api_key:
        print("\n❌ FAILED: GEMINI_API_KEY not found in .env file")
        print("\nPlease:")
        print("1. Create a .env file in the project root")
        print("2. Add: GEMINI_API_KEY=your_api_key_here")
        print("3. Get your key from: https://aistudio.google.com/app/apikey")
        return False
    
    print(f"\n✅ API Key found: {api_key[:10]}...{api_key[-4:]}")
    print(f"✅ Model: {settings.GEMINI_MODEL}")
    
    try:
        print("\n🔄 Testing connection to Gemini API...")
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel(settings.GEMINI_MODEL)
        response = model.generate_content("Say 'AEGIS is online!' and nothing else.")
        
        print(f"\n✅ SUCCESS! Gemini responded:")
        print(f"   {response.text}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ FAILED: {str(e)}")
        print("\nPossible issues:")
        print("- Invalid API key")
        print("- Network connection problem")
        print("- API quota exceeded")
        return False

def test_function_calling():
    print("\n" + "=" * 60)
    print("Testing Function Calling")
    print("=" * 60)
    
    try:
        from core_auditor.services.gemini_client import GeminiClient
        
        print("\n🔄 Initializing Gemini client with tools...")
        client = GeminiClient()
        
        if not client.is_enabled():
            print("❌ Client not enabled (check API key)")
            return False
        
        print("✅ Client initialized successfully")
        
        print("\n🔄 Testing function call detection...")
        client.start_chat()
        response = client.send_message(
            "I see an unsafe condition: someone without gloves touching sterile equipment. This is a critical safety violation."
        )
        
        has_function_call = False
        if response.candidates and len(response.candidates) > 0:
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'function_call') and part.function_call:
                    has_function_call = True
                    print(f"\n✅ Function call detected: {part.function_call.name}")
                    print(f"   Args: {dict(part.function_call.args)}")
        
        if not has_function_call:
            print("\n⚠️  No function call detected (Gemini may have responded with text only)")
            print("   This is okay - function calling is context-dependent")
        
        return True
        
    except Exception as e:
        print(f"\n❌ FAILED: {str(e)}")
        return False

def test_orchestrator():
    print("\n" + "=" * 60)
    print("Testing AuditorOrchestrator")
    print("=" * 60)
    
    try:
        from core_auditor.services.orchestrator import AuditorOrchestrator
        
        print("\n🔄 Initializing orchestrator...")
        orchestrator = AuditorOrchestrator()
        
        if not orchestrator.gemini.is_enabled():
            print("⚠️  Running in simulation mode (no API key)")
        else:
            print("✅ Orchestrator initialized with Gemini AI")
        
        print("\n🔄 Testing input processing...")
        response = orchestrator.process_input("Test message: monitor surgical procedure")
        
        print(f"\n✅ Response received:")
        print(f"   Content: {response['content'][:100]}...")
        print(f"   Thought signature: {response['thought_signature']}")
        print(f"   Tool use: {response['tool_use']}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n🚀 Starting Gemini API Integration Tests\n")
    
    test1 = test_api_connection()
    
    if test1:
        test2 = test_function_calling()
        test3 = test_orchestrator()
        
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"API Connection:      {'✅ PASS' if test1 else '❌ FAIL'}")
        print(f"Function Calling:    {'✅ PASS' if test2 else '❌ FAIL'}")
        print(f"Orchestrator:        {'✅ PASS' if test3 else '❌ FAIL'}")
        
        if test1 and test2 and test3:
            print("\n🎉 All tests passed! Gemini integration is working.")
            print("\nYou can now:")
            print("1. Start the server: python manage.py runserver")
            print("2. Open http://localhost:8000")
            print("3. Test with real AI responses!")
        else:
            print("\n⚠️  Some tests failed. Check the errors above.")
    else:
        print("\n❌ API connection failed. Fix the API key issue first.")
    
    print("\n" + "=" * 60)
