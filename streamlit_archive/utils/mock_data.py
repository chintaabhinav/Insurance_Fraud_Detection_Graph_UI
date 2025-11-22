import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def get_dashboard_metrics():
    """
    Generates mock data for the dashboard.
    In production, this would query the FastAPI backend or Neo4j directly.
    """
    # Top Level Metrics
    total_claims = 1245
    fraud_claims = 84
    fraud_value = 450000  # $450k
    avg_processing_time = 1.2  # seconds

    # Timeseries Data (Last 30 days)
    dates = [datetime.today() - timedelta(days=i) for i in range(29, -1, -1)]
    
    data = []
    for date in dates:
        daily_claims = random.randint(30, 60)
        daily_fraud = random.randint(0, 5)
        data.append({
            "Date": date.strftime("%Y-%m-%d"),
            "Legitimate": daily_claims - daily_fraud,
            "Fraudulent": daily_fraud
        })
    
    df_timeline = pd.DataFrame(data)

    # Claim Types Distribution
    claim_types = {
        "Auto Accident": 450,
        "Theft": 120,
        "Medical": 300,
        "Property Damage": 250,
        "Life": 125
    }
    df_types = pd.DataFrame(list(claim_types.items()), columns=["Type", "Count"])

    # Recent Alerts
    recent_alerts = [
        {"ID": "CLM-9921", "Type": "Auto", "Risk": "High", "Score": 0.92, "Date": "2025-11-22"},
        {"ID": "CLM-9920", "Type": "Medical", "Risk": "Medium", "Score": 0.65, "Date": "2025-11-22"},
        {"ID": "CLM-9918", "Type": "Theft", "Risk": "High", "Score": 0.88, "Date": "2025-11-21"},
        {"ID": "CLM-9915", "Type": "Property", "Risk": "Low", "Score": 0.12, "Date": "2025-11-21"},
        {"ID": "CLM-9902", "Type": "Auto", "Risk": "High", "Score": 0.95, "Date": "2025-11-20"},
    ]

    return {
        "metrics": {
            "total": total_claims,
            "fraud_count": fraud_claims,
            "fraud_val": fraud_value,
            "proc_time": avg_processing_time
        },
        "timeline": df_timeline,
        "types": df_types,
        "alerts": recent_alerts
    }
