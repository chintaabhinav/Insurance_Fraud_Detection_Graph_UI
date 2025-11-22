import os
import requests
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8080")

def extract_claim_data(file, doc_type=None, classify_if_missing=True):
    """
    Sends the file to the backend for extraction and classification.
    """
    url = f"{BACKEND_URL}/v1/extract"
    
    # Prepare params
    params = {
        "classify_if_missing": str(classify_if_missing).lower()
    }
    if doc_type:
        params["doc_type"] = doc_type

    # Prepare file
    file.seek(0)
    files = {"file": (file.name, file, "application/pdf")}

    try:
        response = requests.post(url, params=params, files=files, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def chat_with_graph(message: str):
    """
    Sends a natural language query to the backend to be processed by the Graph LLM.
    """
    url = f"{BACKEND_URL}/v1/chat"
    
    # Mocking the response for now as the backend endpoint might not exist or be ready
    # In real implementation:
    # try:
    #     resp = requests.post(url, json={"query": message}, timeout=30)
    #     resp.raise_for_status()
    #     return resp.json()["response"]
    # except Exception as e:
    #     return f"Error: {str(e)}"

    # Mock Logic
    msg = message.lower()
    if "fraud" in msg and "ring" in msg:
        return "I found a potential fraud ring involving **3 claims** and **2 medical providers** in the *North District*. They share the same phone number `(555) 019-2834`."
    elif "claim" in msg and "123" in msg:
        return "Claim **#123** is marked as **High Risk** (Score: 0.89). The claimant has submitted 4 claims in the last 2 months."
    elif "summary" in msg:
        return "The current dataset contains **1,245 claims**. The overall fraud rate is **6.7%**. The most common fraud type is *Staged Accidents*."
    else:
        return "I can help you analyze the graph. Try asking about specific claims, fraud rings, or general statistics."
