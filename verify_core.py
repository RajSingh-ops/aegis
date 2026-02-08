import os
import django
import json
import asyncio

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aegis_core.settings')
django.setup()

from core_auditor.orchestrator import AuditorOrchestrator

def test_orchestrator_flow():
    print("--- Starting Orchestrator Verification ---")
    
    orchestrator = AuditorOrchestrator()
    
    # Test 1: Normal Operation
    print("\nTest 1: Normal Input")
    response1 = orchestrator.process_input("Surgeon is proceeding with the incision.")
    print(f"Response: {response1['content']}")
    print(f"Thought Signature: {response1['thought_signature']}")
    assert response1['thought_signature'] is not None, "Thought Signature missing!"

    # Test 2: Safety Violation (Trigger Tool)
    print("\nTest 2: Safety Violation Input")
    response2 = orchestrator.process_input("The surgeon is using an unsafe scalpel technique.")
    print(f"Response: {response2['content']}")
    
    if response2['tool_use']:
        print(f"Tool Triggered: {response2['tool_use']['name']}")
        result = orchestrator.execute_tool(response2['tool_use']['name'], response2['tool_use']['args'])
        print(f"Tool Result: {result}")
        assert response2['tool_use']['name'] == "log_deviation", "Wrong tool triggered!"
    else:
        print("FAIL: Tool not triggered for safety violation.")

    print("\n--- Verification Complete ---")

if __name__ == "__main__":
    test_orchestrator_flow()
