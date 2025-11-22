from flask import Flask, render_template, request, jsonify
import os
import requests
from dotenv import load_dotenv
import random
from datetime import datetime, timedelta

load_dotenv()

app = Flask(__name__)
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8080")

# --- Mock Data Helpers (Keep for Dashboard for now) ---
def get_dashboard_data():
    return {
        "total_claims": 1245,
        "fraud_claims": 84,
        "fraud_value": 450000,
        "proc_time": 1.2,
        "timeline": {
            "labels": [(datetime.today() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(29, -1, -1)],
            "legit": [random.randint(30, 60) for _ in range(30)],
            "fraud": [random.randint(0, 5) for _ in range(30)]
        }
    }

# --- Routes ---

@app.route('/')
def dashboard():
    data = get_dashboard_data()
    return render_template('dashboard.html', page='dashboard', data=data)

@app.route('/upload')
def upload():
    return render_template('upload.html', page='upload')

@app.route('/chat')
def chat():
    return render_template('chat.html', page='chat')

@app.route('/monitoring')
def monitoring():
    return render_template('monitoring.html', page='monitoring')

@app.route('/evaluation')
def evaluation():
    return render_template('evaluation.html', page='evaluation')

# --- API Endpoints ---

@app.route('/api/upload', methods=['POST'])
def api_upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    doc_type = request.form.get('doc_type')
    classify_if_missing = request.form.get('classify_if_missing', 'true')

    # Prepare request to FastAPI backend
    url = f"{BACKEND_URL}/v1/extract"
    params = {"classify_if_missing": classify_if_missing}
    if doc_type and doc_type != "Auto-Detect":
        params["doc_type"] = doc_type

    files = {'file': (file.filename, file.stream, file.content_type)}

    try:
        # Forward to backend
        resp = requests.post(url, params=params, files=files, timeout=60)
        resp.raise_for_status()
        return jsonify(resp.json())
    except requests.exceptions.RequestException as e:
        # Fallback for demo if backend is offline
        print(f"Backend connection failed: {e}")
        return jsonify({
            "error": "Backend connection failed", 
            "details": str(e),
            # Mock response for UI testing if backend is down
            "mock_fallback": True,
            "doc_type": "Medical Bill",
            "result": {
                "fraud_score": 0.85,
                "summary": "High mismatch in service codes vs diagnosis.",
                "extracted_fields": {
                    "Patient": "John Doe",
                    "Amount": "$45,000",
                    "Date": "2025-10-12"
                },
                "fraud_analysis": [
                    "Provider is flagged in 3 other fraud cases.",
                    "Service date overlaps with another claim in a different state."
                ]
            }
        }), 503

@app.route('/api/chat', methods=['POST'])
def api_chat():
    msg = request.json.get('message', '')
    url = f"{BACKEND_URL}/v1/chat"
    
    try:
        resp = requests.post(url, json={"query": msg}, timeout=30)
        resp.raise_for_status()
        return jsonify(resp.json())
    except requests.exceptions.RequestException as e:
        print(f"Chat backend failed: {e}")
        # Fallback Mock
        return jsonify({
            "response": "I'm having trouble connecting to the brain (Backend). <br><i>Error: Connection refused</i>"
        })

if __name__ == '__main__':
    app.run(debug=True, port=5001)
