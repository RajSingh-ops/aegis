from datetime import datetime

# Mock function for now, will connect to Analytics app later
def log_deviation(severity, description, recommended_action):
    """
    Logs a safety deviation to the operational analytics pipeline.
    """
    print(f"[ANALYTICS] Deviation Logged: [{severity}] {description} -> {recommended_action}")
    return {"status": "success", "id": "dev_123456", "timestamp": datetime.now().isoformat()}

# Mock function for Knowledge Vault retrieval
def search_knowledge_vault(query):
    """
    Searches the 2M token Knowledge Vault for relevant safety protocols.
    """
    print(f"[KNOWLEDGE VAULT] Searching for: {query}")
    return {
        "results": [
            "Standard Operating Procedure 4.2.1: Always wear protective eyewear.",
            "IEC 60601-1: Medical electrical equipment safety standards."
        ]
    }

AEGIS_TOOLS = [
    {
        "function_declarations": [
            {
                "name": "log_deviation",
                "description": "Logs a detected safety deviation or regulatory non-conformance.",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "severity": {"type": "STRING", "description": "Low, Medium, High, or Critical"},
                        "description": {"type": "STRING", "description": "Detailed description of the event"},
                        "recommended_action": {"type": "STRING", "description": "Immediate corrective action required"}
                    },
                    "required": ["severity", "description", "recommended_action"]
                }
            },
            {
                "name": "search_knowledge_vault",
                "description": "Queries the safety protocols and legal regulations database.",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "query": {"type": "STRING", "description": "The specific safety topic or procedure to look up"}
                    },
                    "required": ["query"]
                }
            }
        ]
    }
]
