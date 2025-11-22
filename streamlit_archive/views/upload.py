import streamlit as st
from utils.api_client import extract_claim_data
import json

def app():
    # Header
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.title("🧾 Upload & Detect")
    st.markdown("Upload a claim document (PDF) to automatically classify it, extract data, and detect fraud.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Main Layout
    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📂 Document Upload")
        uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'])
        
        # Options
        with st.expander("⚙️ Advanced Options"):
            doc_type = st.selectbox("Force Document Type (Optional)", ["Auto-Detect", "Claim Form", "Police Report", "Medical Bill", "Repair Estimate"])
            if doc_type == "Auto-Detect":
                doc_type = None
            
            auto_classify = st.toggle("Auto-classify if missing", value=True)
        
        process_btn = st.button("🚀 Analyze Document", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        if uploaded_file and process_btn:
            with st.spinner("🔍 Analyzing document... This may take a moment."):
                # Call Backend
                result = extract_claim_data(uploaded_file, doc_type, auto_classify)
                
                if "error" in result:
                    st.error(f"❌ Error processing document: {result['error']}")
                else:
                    # Success Display
                    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                    st.subheader("✅ Analysis Results")
                    
                    # Top Level Metrics
                    m1, m2 = st.columns(2)
                    with m1:
                        st.metric("Document Type", result.get("doc_type", "Unknown"))
                    with m2:
                        fraud_score = result.get("result", {}).get("fraud_score", 0)
                        st.metric("Fraud Risk Score", f"{fraud_score * 100:.1f}%", delta_color="inverse")

                    st.divider()
                    
                    # Extracted Fields
                    st.markdown("#### 📝 Extracted Data")
                    st.json(result.get("result", {}), expanded=False)
                    
                    # Fraud Analysis (Mocked or from backend)
                    if "fraud_analysis" in result:
                        st.markdown("#### 🕵️ Fraud Analysis")
                        st.write(result["fraud_analysis"])
                    
                    st.markdown('</div>', unsafe_allow_html=True)

        elif not uploaded_file:
            # Placeholder when no file is uploaded
            st.markdown('<div class="glass-card" style="text-align: center; opacity: 0.7;">', unsafe_allow_html=True)
            st.markdown("### 👈 Upload a file to get started")
            st.markdown("The system will analyze the document structure and content.")
            st.markdown('</div>', unsafe_allow_html=True)
