from datetime import datetime
from analytics.models import Deviation
import google.generativeai as genai

def log_deviation(severity, description, recommended_action):
    deviation = Deviation.objects.create(
        severity=severity.upper(),
        description=description,
        recommended_action=recommended_action
    )
    print(f"[ANALYTICS] Deviation Logged: [{severity}] {description} -> {recommended_action}")
    return {"status": "success", "id": str(deviation.id), "timestamp": deviation.timestamp.isoformat()}

def search_knowledge_vault(query):
    print(f"[KNOWLEDGE VAULT] Searching for: {query}")
    return {
        "results": [
            "Standard Operating Procedure 4.2.1: Always wear protective eyewear.",
            "IEC 60601-1: Medical electrical equipment safety standards."
        ]
    }

AEGIS_TOOLS = [
    genai.protos.Tool(
        function_declarations=[
            genai.protos.FunctionDeclaration(
                name="log_deviation",
                description="Logs a detected safety deviation or regulatory non-conformance to the database. Use this when you detect unsafe conditions, protocol violations, or regulatory non-compliance.",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "severity": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Severity level of the deviation. Must be one of: LOW, MEDIUM, HIGH, or CRITICAL"
                        ),
                        "description": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Detailed description of the safety deviation, including what was observed and why it's a concern"
                        ),
                        "recommended_action": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="Immediate corrective action required to address the deviation"
                        )
                    },
                    required=["severity", "description", "recommended_action"]
                )
            ),
            genai.protos.FunctionDeclaration(
                name="search_knowledge_vault",
                description="Queries the safety protocols and legal regulations database. Use this to look up specific procedures, standards, or regulatory requirements.",
                parameters=genai.protos.Schema(
                    type=genai.protos.Type.OBJECT,
                    properties={
                        "query": genai.protos.Schema(
                            type=genai.protos.Type.STRING,
                            description="The specific safety topic, procedure, or regulation to look up"
                        )
                    },
                    required=["query"]
                )
            )
        ]
    )
]
