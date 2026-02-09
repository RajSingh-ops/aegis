import google.generativeai as genai
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class GeminiClient:
    
    def __init__(self):
        if not settings.GEMINI_API_KEY:
            logger.warning("GEMINI_API_KEY not set. Using simulation mode.")
            self.enabled = False
            return
        
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(
                model_name=settings.GEMINI_MODEL,
                tools=self._get_tools(),
                system_instruction=self._get_system_instruction()
            )
            self.chat = None
            self.enabled = True
            logger.info(f"Gemini client initialized with model: {settings.GEMINI_MODEL}")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")
            self.enabled = False
    
    def _get_system_instruction(self):
        return """You are AEGIS (Advanced Evaluation and Governance Intelligence System), an AI safety auditor monitoring high-stakes operations in real-time.

Your role and responsibilities:
- Analyze video, audio, and text inputs for safety violations and regulatory non-compliance
- Cross-reference observed actions against established safety protocols and regulations
- Log deviations with appropriate severity ratings (LOW, MEDIUM, HIGH, CRITICAL)
- Provide clear, actionable recommendations for corrective actions
- Maintain professional, precise communication focused on safety

You have access to specialized tools:
- log_deviation: Record safety violations to the analytics database with severity and recommendations
- search_knowledge_vault: Query the regulatory protocols and safety standards database

Guidelines:
- Prioritize safety above all else
- Be specific and factual in your assessments
- Use tools proactively when you detect issues or need protocol information
- Provide context and reasoning for your decisions
- Maintain a professional, authoritative tone

Remember: Lives may depend on your accurate and timely analysis."""
    
    def _get_tools(self):
        from .tools import AEGIS_TOOLS
        return AEGIS_TOOLS
    
    def start_chat(self, history=None):
        if not self.enabled:
            return None
        
        self.chat = self.model.start_chat(history=history or [])
        logger.debug("Chat session started")
        return self.chat
    
    def send_message(self, message, stream=False):
        if not self.enabled:
            raise Exception("Gemini client not enabled. Check API key configuration.")
        
        if not self.chat:
            self.start_chat()
        
        try:
            response = self.chat.send_message(message, stream=stream)
            logger.debug(f"Received response from Gemini")
            return response
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise
    
    def get_history(self):
        return self.chat.history if self.chat else []
    
    def is_enabled(self):
        return self.enabled
