import random
import pandas as pd
from datetime import datetime, timedelta

def get_system_metrics():
    """
    Generates mock system monitoring data.
    """
    # Real-time System Stats
    cpu_usage = random.randint(20, 65)
    memory_usage = random.randint(40, 80)
    api_latency = random.randint(150, 800)  # ms
    active_threads = random.randint(4, 12)

    # LLM Usage (Last 24 Hours)
    hours = [datetime.now() - timedelta(hours=i) for i in range(23, -1, -1)]
    llm_data = []
    for h in hours:
        tokens = random.randint(1000, 5000)
        cost = (tokens / 1000) * 0.03  # Mock cost calculation
        llm_data.append({
            "Time": h.strftime("%H:00"),
            "Tokens": tokens,
            "Cost ($)": round(cost, 4),
            "Requests": random.randint(10, 50)
        })
    df_llm = pd.DataFrame(llm_data)

    # Mock Logs
    log_levels = ["INFO", "INFO", "INFO", "WARNING", "ERROR"]
    endpoints = ["/v1/extract", "/v1/chat", "/v1/graph/query", "/health"]
    logs = []
    for _ in range(10):
        timestamp = datetime.now().strftime("%H:%M:%S")
        level = random.choice(log_levels)
        endpoint = random.choice(endpoints)
        msg = f"Request processed for {endpoint}" if level == "INFO" else f"High latency detected on {endpoint}" if level == "WARNING" else f"Connection timeout on {endpoint}"
        logs.append(f"[{timestamp}] [{level}] {msg}")

    return {
        "system": {
            "cpu": cpu_usage,
            "memory": memory_usage,
            "latency": api_latency,
            "threads": active_threads
        },
        "llm_stats": df_llm,
        "logs": logs
    }
