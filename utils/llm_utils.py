import random
import textwrap

def extract_fields_from_pdf(file) -> dict:
    """
    TEMP: Mock LLM extraction.
    Replace this with real PDF → LLM extraction later.
    """
    # In real logic: read PDF, send to LLM, parse fields
    return {
        "Claim ID": "C" + str(random.randint(1000, 9999)),
        "Policy Holder": "John Doe",
        "Policy ID": "P-789456",
        "Claim Amount": "$12,500",
        "Incident Type": "Vehicle Accident",
        "Region": "California",
    }

def explain_fraud(claim_data: dict, user_question: str) -> str:
    """
    TEMP: Mock explanation using claim_data.
    Later: call LLM with graph evidence + claim details.
    """
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
    """
    TEMP: Simple rule-based chatbot.
    Later: plug in LLM or RAG.
    """
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
