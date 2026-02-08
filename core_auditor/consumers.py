import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .orchestrator import AuditorOrchestrator

class AuditorConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orchestrator = AuditorOrchestrator()

    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'Aegis Core Auditor Connected'
        }))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')

        # Pass input to Orchestrator
        response = self.orchestrator.process_input(message)
        
        # Handle Tool Execution
        if response.get("tool_use"):
            tool_result = self.orchestrator.execute_tool(
                response["tool_use"]["name"], 
                response["tool_use"]["args"]
            )
            final_message = f"{response['content']} \nTool Result: {tool_result}"
        else:
            final_message = response['content']

        await self.send(text_data=json.dumps({
            'type': 'audit_response',
            'message': final_message,
            'thought_signature': response.get('thought_signature')
        }))
