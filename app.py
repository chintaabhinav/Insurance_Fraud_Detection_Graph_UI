import streamlit as st
import plotly.express as px

from utils.llm_utils import extract_fields_from_pdf, explain_fraud, chatbot_answer
from utils.neo4j_utils import check_fraud_with_graph, get_dashboard_data

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Insurance Fraud Intelligence",
    page_icon="🕵️‍♀️",
    layout="wide"
)

# ---------- CUSTOM STYLES ----------
st.markdown("""
    <style>
        /* Global */
        body {
            background-color: #0f172a;
        }
        .main {
            background: linear-gradient(135deg, #020817 0%, #0f172a 40%, #111827 100%);
            color: #e5e7eb;
        }
        /* Sidebar */
        [data-testid="stSidebar"] {
            background: #020817;
            border-right: 1px solid #111827;
        }
         [data-testid="stSidebar"] * {
             color: #e5e7eb !important;
         }
        /* Cards */
        .metric-card {
            padding: 14px 16px;
            border-radius: 14px;
            background: rgba(15,23,42,0.98);
            border: 1px solid #1f2937;
            box-shadow: 0 10px 25px rgba(15,23,42,0.9);
        }
        .tag {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 999px;
            font-size: 11px;
            margin-right: 6px;
            background: rgba(56,189,248,0.1);
            color: #38bdf8;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR NAV ----------
st.sidebar.title("🕵️ Fraud Intelligence")
# ---------- CUSTOM NAVBAR ----------
st.sidebar.markdown("### 🧭 Navigation")
st.sidebar.markdown('<hr style="margin-top:-10px;margin-bottom:10px;border-color:#334155;">', unsafe_allow_html=True)

# Define pages
pages = {
    "Upload & Detect": "📄 Upload & Detect",
    "Dashboard": "📊 Dashboard",
    "Chatbot": "💬 Chatbot"
}

# Style for active/inactive tabs

tab_style = """
<style>
/* --- AGGRESSIVE BLACK TEXT FIX FOR NAV BUTTONS --- */

/* Target the button itself */
div[data-testid="stSidebar"] button[kind="secondary"] {
    background-color: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 10px !important;
    padding: 12px 20px !important;
    margin-bottom: 10px !important;
    width: 100% !important;
    text-align: left !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
}

/* FORCE BLACK TEXT - Multiple selectors for maximum specificity */
div[data-testid="stSidebar"] button[kind="secondary"],
div[data-testid="stSidebar"] button[kind="secondary"] *,
div[data-testid="stSidebar"] button[kind="secondary"] span,
div[data-testid="stSidebar"] button[kind="secondary"] div,
div[data-testid="stSidebar"] button[kind="secondary"] p,
.stButton button[kind="secondary"],
.stButton button[kind="secondary"] *,
section[data-testid="stSidebar"] button,
section[data-testid="stSidebar"] button * {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    opacity: 1 !important;
}

/* Target Streamlit's internal button text spans with attribute selectors */
[data-testid="stSidebar"] button > div,
[data-testid="stSidebar"] button > div > span,
[data-testid="stSidebar"] button span[data-testid*="text"],
[data-testid="stSidebar"] button div[data-testid*="text"] {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}

/* Use pseudo-elements to override any inherited opacity or color filters */
div[data-testid="stSidebar"] button[kind="secondary"]::before {
    content: none !important;
}

# /* Hover state - no change, stays the same as idle */
# div[data-testid="stSidebar"] button[kind="secondary"]:hover {
#     background-color: #ffffff !important;
#     border: 1px solid #cbd5e1 !important;
#     box-shadow: none !important;
#     transform: none !important;
# }

div[data-testid="stSidebar"] button[kind="secondary"]:hover *,
div[data-testid="stSidebar"] button[kind="secondary"]:hover {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    background-color: transparent !important;
}

/* Active/Selected state */
div[data-testid="stSidebar"] button[kind="secondary"][aria-pressed="true"] {
    background-color: #e2e8f0 !important;
    border: 2px solid #38bdf8 !important;
    box-shadow: 0 0 6px rgba(56,189,248,0.4) !important;
}

div[data-testid="stSidebar"] button[kind="secondary"][aria-pressed="true"] *,
div[data-testid="stSidebar"] button[kind="secondary"][aria-pressed="true"] {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}

/* Nuclear option - override EVERYTHING in the sidebar buttons */
[data-testid="stSidebar"] button {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}

[data-testid="stSidebar"] button * {
    color: inherit !important;
    -webkit-text-fill-color: inherit !important;
}
</style>
"""

st.markdown(tab_style, unsafe_allow_html=True)



st.markdown(tab_style, unsafe_allow_html=True)

# Get current page
if "current_page" not in st.session_state:
    st.session_state.current_page = "Upload & Detect"

# Display styled tabs
for key, label in pages.items():
    if st.sidebar.button(label, key=key, use_container_width=True):
        st.session_state.current_page = key
        st.rerun()



# Set current page
page = st.session_state.current_page



# Use session state to carry last claim info
if "last_claim" not in st.session_state:
    st.session_state["last_claim"] = None
if "last_result" not in st.session_state:
    st.session_state["last_result"] = None


# ---------- PAGE 1: UPLOAD & DETECT ----------
if page == "Upload & Detect":
    st.markdown("## 🧾 Upload & Detect")
    st.markdown(
        "Upload a claim PDF to analyze it with an LLM, check hidden links in Neo4j, "
        "and get an **instant fraud risk decision**."
    )

    col_left, col_right = st.columns([2, 1])

    with col_left:
        uploaded_file = st.file_uploader(
            "📂 Upload Claim Document (PDF)",
            type=["pdf"],
            help="The system will extract key fields, query the fraud graph, and return a decision."
        )

        if uploaded_file:
            with st.spinner("Reading document & extracting claim fields using LLM..."):
                extracted = extract_fields_from_pdf(uploaded_file)

            st.markdown("### 📑 Extracted Claim Details")
            st.json(extracted)

            with st.spinner("Running graph-based fraud detection via Neo4j..."):
                result = check_fraud_with_graph(extracted)

            st.session_state["last_claim"] = extracted
            st.session_state["last_result"] = result

            is_fraud = result["is_fraudulent"]
            score = result["fraud_score"]

            st.markdown("### 🧠 Decision")
            if is_fraud:
                st.error(f"🚨 This claim is flagged as **FRAUDULENT** (Risk Score: {score})")
            else:
                st.success(f"✅ This claim appears **LEGITIMATE** (Risk Score: {score})")

            st.caption("Risk score is a confidence indicator derived from graph + LLM signals.")

            # Rules / Signals
            st.markdown("#### 🔎 Key Signals")
            for r in result["rules_triggered"]:
                st.markdown(f"- {r}")

    
    st.sidebar.markdown('<hr style="margin:15px 0;border-color:#1e293b;">', unsafe_allow_html=True)
    st.sidebar.caption("🧠 Powered by LLM + Neo4j Graph Intelligence")
    st.markdown("---")

    # 🔥 Q&A for this specific claim (on same page)
    st.markdown("### 💬 Ask about this claim")

    if st.session_state["last_claim"] is None:
        st.info("Upload a document first to ask why it is flagged or how the decision was made.")
    else:
        user_q = st.text_input(
            "Example: *Why is this claim fraudulent?*  |  *Which fields look suspicious?*",
            key="claim_qa_box"
        )
        if user_q:
            with st.spinner("Generating explanation from LLM using claim + graph context..."):
                answer = explain_fraud(st.session_state["last_claim"], user_q)
            st.markdown("#### 🔍 Explanation")
            st.write(answer)


# ---------- PAGE 2: DASHBOARD ----------
elif page == "Dashboard":
    st.markdown("## 📊 Fraud Analytics Dashboard")
    st.markdown(
        "Monitor how many claims are processed, how many are flagged as fraud, and patterns over time. "
        "In the real system, this will be powered directly from Neo4j events."
    )

    data = get_dashboard_data()
    df = data["timeseries"]

    k1, k2, k3 = st.columns(3)
    with k1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Frauds Detected", data["total_frauds"])
        st.markdown("</div>", unsafe_allow_html=True)
    with k2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Legitimate Claims", data["total_legit"])
        st.markdown("</div>", unsafe_allow_html=True)
    with k3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Fraud Rate (%)", data["fraud_rate"])
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("### 📈 Fraud vs Legit Over Time")
    fig = px.line(
        df,
        x="date",
        y=["frauds", "legit"],
        labels={"value": "Number of Claims", "date": "Date", "variable": "Type"},
        markers=True,
        title="Daily Claims Overview (Demo Data)"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 🧩 Data Snapshot")
    st.dataframe(df.tail(10), use_container_width=True)


# ---------- PAGE 3: CHATBOT ----------
elif page == "Chatbot":
    st.markdown("## 💬 Fraud Assistant Chatbot")
    st.markdown(
        "Ask questions about how the system works, fraud logic, Neo4j graph usage, or document summaries.\n"
        "_(Currently using a mock brain — plug in your LLM later.)_"
    )

    # Simple chat-style UI
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    user_msg = st.text_input("Type your question here:", key="chat_input")

    if user_msg:
        reply = chatbot_answer(user_msg)
        st.session_state["chat_history"].append(("You", user_msg))
        st.session_state["chat_history"].append(("Assistant", reply))

    for sender, msg in st.session_state["chat_history"]:
        if sender == "You":
            st.markdown(f"**🧑 You:** {msg}")
        else:
            st.markdown(f"**🤖 Assistant:** {msg}")
