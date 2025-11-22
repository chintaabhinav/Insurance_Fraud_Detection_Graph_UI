import os
import json
import requests
from typing import Any, Dict, Optional
from dotenv import load_dotenv

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8080")

def extract_fields_from_pdf(file, doc_type: Optional[str] = None, classify_if_missing: bool = True) -> Dict[str, Any]:
    """
    Send the uploaded PDF to FastAPI /v1/extract and return the parsed JSON.
    `file` is a Streamlit UploadedFile.
    """
    if file is None:
        return {"error": "no file provided"}

    # Build URL with query params
    url = f"{BACKEND_URL}/v1/extract"
    params = {}
    if doc_type:
        params["doc_type"] = doc_type
    params["classify_if_missing"] = "true" if classify_if_missing else "false"

    # Reset pointer (Streamlit may have read this already)
    file.seek(0)

    files = {
        "file": (file.name or "document.pdf", file, "application/pdf")
    }

    try:
        resp = requests.post(url, params=params, files=files, timeout=60)
    except requests.RequestException as e:
        return {"error": f"request_failed: {e}"}

    # Normalize response
    try:
        data = resp.json()
    except json.JSONDecodeError:
        return {"error": f"invalid_json_from_backend (status={resp.status_code})", "text": resp.text}

    if resp.status_code != 200:
        # pass backend detail up to UI
        return {"error": f"backend_{resp.status_code}", "detail": data.get("detail", data)}

    return data  # expected schema: {doc_type, model, result, usage, cost_estimate}

def explain_fraud(claim_data: dict, user_question: str) -> str:
    # unchanged dummy
    import textwrap
    base_reason = textwrap.dedent(f"""
    Based on the graph analysis and claim details:

    - The claimant **{claim_data.get('Policy Holder', 'N/A')}** is linked to multiple high-value claims.
    - The claim amount **{claim_data.get('Claim Amount', 'N/A')}** is unusual for similar incidents.
    - Connections between claimant, agent, and service providers match known fraud patterns.
    """)
    if "why" in user_question.lower():
        return base_reason + "\nOverall, these patterns increase the fraud likelihood for this claim."
    else:
        return "I analyze historical links, unusual patterns, amounts, and relationships in the Neo4j graph to justify the decision."

def chatbot_answer(user_message: str) -> str:
    # unchanged dummy
    msg = user_message.lower()
    if "fraud" in msg and "how" in msg:
        return (
            "Our system detects fraud by combining:\n"
            "- Document analysis using LLMs\n"
            "- Relationship graphs in Neo4j\n"
            "- Historical patterns of suspicious activity."
        )
    if "summary" in msg:
        return "Upload a document on the Upload & Detect page, and I’ll summarize key claim details for you."
    if "neo4j" in msg:
        return "Neo4j stores entities (claimants, agents, providers, policies) and their relationships to spot hidden fraud rings."
    if "hi" in msg or "hello" in msg:
        return "Hello 👋 I’m your Fraud Assistant. Ask me about claims, fraud logic, or how the system works."
    return (
        "Great question. Right now I’m a demo bot. In the full version, I’ll use your documentation and graph data "
        "to give precise, explainable answers. 🧠"
    )