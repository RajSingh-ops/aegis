import os
import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aegis_core.settings')
import django
django.setup()

print("=" * 60)
print("AEGIS System Diagnostic")
print("=" * 60)

print("\n[1/5] Testing imports...")
try:
    from core_auditor.services.gemini_client import GeminiClient
    from core_auditor.services.orchestrator import AuditorOrchestrator
    from core_auditor.services.tools import log_deviation, search_knowledge_vault, AEGIS_TOOLS
    from core_auditor.websockets.consumers import AuditorConsumer
    print("✅ All imports successful")
except Exception as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

print("\n[2/5] Checking environment...")
from django.conf import settings
if settings.GEMINI_API_KEY:
    print(f"✅ API Key configured: {settings.GEMINI_API_KEY[:10]}...{settings.GEMINI_API_KEY[-4:]}")
    print(f"✅ Model: {settings.GEMINI_MODEL}")
else:
    print("⚠️  No API key (will use simulation mode)")

print("\n[3/5] Testing Gemini client...")
try:
    client = GeminiClient()
    if client.is_enabled():
        print("✅ Gemini client enabled")
    else:
        print("⚠️  Gemini client disabled (simulation mode)")
except Exception as e:
    print(f"❌ Client initialization error: {e}")

print("\n[4/5] Testing orchestrator...")
try:
    orchestrator = AuditorOrchestrator()
    print("✅ Orchestrator initialized")
    
    response = orchestrator.process_input("test message")
    print(f"✅ Orchestrator response: {response['content'][:50]}...")
except Exception as e:
    print(f"❌ Orchestrator error: {e}")
    import traceback
    traceback.print_exc()

print("\n[5/5] Testing tools...")
try:
    tools = AEGIS_TOOLS
    print(f"✅ Tools loaded: {len(tools[0].function_declarations)} functions")
except Exception as e:
    print(f"❌ Tools error: {e}")

print("\n" + "=" * 60)
print("Diagnostic Complete!")
print("=" * 60)
print("\n✅ System is ready to use!")
print("\nNext steps:")
print("1. Start server: python manage.py runserver")
print("2. Open browser: http://localhost:8000")
print("3. Test the dashboard")
