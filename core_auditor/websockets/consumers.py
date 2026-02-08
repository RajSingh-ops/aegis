import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from ..services.orchestrator import AuditorOrchestrator
import logging

logger = logging.getLogger(__name__)

class AuditorConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orchestrator = None

    async def connect(self):
        try:
            # Initialize orchestrator here to avoid blocking constructor
            if self.orchestrator is None:
                self.orchestrator = await sync_to_async(AuditorOrchestrator)()
            
            await self.accept()
            
            # Check if Gemini is enabled
            gemini_status = "Gemini AI Active" if self.orchestrator.gemini.is_enabled() else "Simulation Mode"
            
            await self.send(text_data=json.dumps({
                'type': 'connection_established',
                'message': f'Aegis Core Auditor Connected - {gemini_status}'
            }))
            logger.info(f"WebSocket connected: {gemini_status}")
        except Exception as e:
            logger.error(f"Error during WebSocket connection: {e}")
            import traceback
            traceback.print_exc()
            await self.accept()
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': f'Connection error: {str(e)}'
            }))

    async def disconnect(self, close_code):
        logger.info(f"WebSocket disconnected: {close_code}")

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json.get('message')
            
            if not message:
                return

            logger.info(f"Received message: {message}")

            # Process with orchestrator (run in thread pool to avoid blocking)
            response = await sync_to_async(self.orchestrator.process_input)(message)
            
            logger.info(f"Response from orchestrator: content={bool(response.get('content'))}, tool_use={bool(response.get('tool_use'))}")
            
            # Handle Tool Execution
            if response.get("tool_use"):
                tool_name = response["tool_use"]["name"]
                tool_args = response["tool_use"]["args"]
                logger.info(f"Executing tool: {tool_name} with args: {tool_args}")
                
                tool_result = await sync_to_async(self.orchestrator.execute_tool)(
                    tool_name,
                    tool_args
                )
                final_message = f"{response['content']}\n\n{tool_result}"
                logger.info(f"Tool {tool_name} executed successfully")
            else:
                final_message = response['content']

            await self.send(text_data=json.dumps({
                'type': 'audit_response',
                'message': final_message,
                'thought_signature': response.get('thought_signature')
            }))
            
            logger.info(f"Sent response to client ({len(final_message)} chars)")
            
        except Exception as e:
            logger.error(f"Error in WebSocket receive: {e}")
            import traceback
            traceback.print_exc()
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': f'❌ Error: {str(e)}'
            }))
