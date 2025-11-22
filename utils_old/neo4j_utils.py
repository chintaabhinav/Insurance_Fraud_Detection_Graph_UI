import random
import pandas as pd
from datetime import datetime, timedelta

def check_fraud_with_graph(extracted_fields: dict) -> dict:
    """
    TEMP: Mock graph-based fraud decision.
    Later: replace with real Neo4j queries.
    """
    score = round(random.uniform(0.2, 0.98), 2)
    is_fraud = score > 0.7

    return {
        "is_fraudulent": is_fraud,
        "fraud_score": score,
        "rules_triggered": [
            "Shared contact between claimant & service provider",
            "Unusual claim frequency in last 6 months",
            "High amount vs peer claims in same region"
        ] if is_fraud else [
            "No suspicious relationships detected",
            "Claim profile matches historical legitimate patterns"
        ]
    }

def get_dashboard_data():
    """
    TEMP: Generate fake timeseries + summary stats.
    Later: pull from Neo4j.
    """
    today = datetime.today()
    dates = [today - timedelta(days=i) for i in range(29, -1, -1)]

    records = []
    total_frauds = 0
    total_legit = 0

    for d in dates:
        frauds = random.randint(1, 8)
        legit = random.randint(10, 40)
        total_frauds += frauds
        total_legit += legit
        records.append({
            "date": d.date().isoformat(),
            "frauds": frauds,
            "legit": legit
        })

    df = pd.DataFrame(records)

    return {
        "timeseries": df,
        "total_frauds": total_frauds,
        "total_legit": total_legit,
        "fraud_rate": round(total_frauds / (total_frauds + total_legit) * 100, 2),
    }
