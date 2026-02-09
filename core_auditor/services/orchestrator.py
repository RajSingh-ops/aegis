import json
import logging
from .gemini_client import GeminiClient
from .tools import log_deviation, search_knowledge_vault

logger = logging.getLogger(__name__)

class AuditorOrchestrator:
    
    def __init__(self):
        self.gemini = GeminiClient()
        self.history = []
        self.thought_signature = None
        
        if self.gemini.is_enabled():
            self.gemini.start_chat()
            logger.info("AuditorOrchestrator initialized with Gemini AI")
        else:
            logger.warning("AuditorOrchestrator running in simulation mode (no API key)")
    
    def process_input(self, input_text, modality="text"):
        if not self.gemini.is_enabled():
            return self._simulate_response(input_text)
        
        try:
            response = self.gemini.send_message(input_text)
            
            result = {
                "content": "",
                "thought_signature": self._extract_thought_signature(response),
                "tool_use": None
            }
            
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                
                if hasattr(candidate, 'content') and candidate.content:
                    if hasattr(candidate.content, 'parts'):
                        for part in candidate.content.parts:
                            if hasattr(part, 'function_call') and part.function_call:
                                func_call = part.function_call
                                result["tool_use"] = {
                                    "name": func_call.name,
                                    "args": dict(func_call.args) if hasattr(func_call, 'args') else {}
                                }
                                logger.info(f"Function call requested: {func_call.name}")
                                continue
                            
                            if hasattr(part, 'text'):
                                result["content"] += part.text
            
            if not result["content"] and not result["tool_use"]:
                try:
                    if hasattr(response, 'text'):
                        result["content"] = response.text
                except ValueError as e:
                    logger.debug(f"No text content in response (function call only): {e}")
                    if not result["tool_use"]:
                        result["content"] = "Processing your request..."
            
            self.thought_signature = result["thought_signature"]
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing input with Gemini: {e}")
            import traceback
            traceback.print_exc()
            return {
                "content": f"Error communicating with AI: {str(e)}",
                "thought_signature": None,
                "tool_use": None
            }
    
    def execute_tool(self, tool_name, args):
        try:
            if tool_name == "log_deviation":
                tool_result = log_deviation(**args)
                severity = args.get('severity', 'UNKNOWN').upper()
                description = args.get('description', 'No description')
                action = args.get('recommended_action', 'No action specified')
                
                severity_emoji = {
                    'LOW': '⚠️',
                    'MEDIUM': '⚠️',
                    'HIGH': '🚨',
                    'CRITICAL': '🔴'
                }.get(severity, '⚠️')
                
                return f"""
{severity_emoji} **SAFETY DEVIATION LOGGED**

**Severity:** {severity}
**Issue:** {description}
**Action Required:** {action}

**Record ID:** #{tool_result.get('id')}
**Logged at:** {tool_result.get('timestamp', 'N/A')[:19].replace('T', ' ')}
"""
            
            elif tool_name == "search_knowledge_vault":
                tool_result = search_knowledge_vault(**args)
                query = args.get('query', 'Unknown query')
                results = tool_result.get('results', [])
                
                formatted_results = "\\n".join([f"  • {r}" for r in results])
                
                return f"""
📚 **KNOWLEDGE VAULT SEARCH**

**Query:** {query}

**Relevant Protocols:**
{formatted_results}
"""
            
            else:
                tool_result = {"error": f"Unknown tool: {tool_name}"}
                logger.error(f"Unknown tool requested: {tool_name}")
                return f"❌ Error: Unknown tool '{tool_name}'"
            
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {e}")
            return f"❌ Tool execution error: {str(e)}"
    
    def _extract_thought_signature(self, response):
        try:
            response_hash = hash(str(response))
            return f"gemini_{abs(response_hash) % 1000000}"
        except Exception as e:
            logger.debug(f"Could not extract thought signature: {e}")
            return "gemini_response"
    
    def _simulate_response(self, input_text):
        self.history.append({"role": "user", "parts": [input_text]})
        
        response = {
            "content": "",
            "thought_signature": "sim_" + str(abs(hash(input_text)) % 1000000),
            "tool_use": None
        }

        if "unsafe" in input_text.lower() or "violation" in input_text.lower():
            response["tool_use"] = {
                "name": "log_deviation",
                "args": {
                    "severity": "High",
                    "description": f"Detected potential safety violation in: {input_text}",
                    "recommended_action": "Halt procedure immediately and inspect."
                }
            }
            response["content"] = "⚠️ I have detected a critical safety risk and will log a deviation."
        
        elif "protocol" in input_text.lower():
            response["tool_use"] = {
                "name": "search_knowledge_vault",
                "args": {"query": input_text}
            }
            response["content"] = "🔍 Consulting the Knowledge Vault for relevant protocols..."
        
        else:
            response["content"] = f"✅ Acknowledged. Monitoring stream: {input_text[:50]}..."

        self.thought_signature = response["thought_signature"]
        self.history.append({"role": "model", "parts": [response["content"]]})
        
        return response
