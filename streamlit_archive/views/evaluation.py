import streamlit as st
import pandas as pd
import plotly.express as px
import time

def app():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.title("✅ Model Evaluation")
    st.markdown("Run evaluation pipelines to assess classification accuracy and fraud detection performance.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Control Panel
    col_ctrl, col_stats = st.columns([1, 2])
    
    with col_ctrl:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("⚙️ Configuration")
        dataset = st.selectbox("Select Dataset", ["Validation Set A (100 samples)", "Test Set B (500 samples)", "Golden Set (50 samples)"])
        model_ver = st.selectbox("Model Version", ["v1.2.0 (Current)", "v1.1.5 (Stable)", "v1.3.0-beta"])
        
        if st.button("▶️ Run Evaluation", use_container_width=True):
            st.session_state.eval_running = True
            st.session_state.eval_progress = 0
            st.session_state.eval_done = False
        st.markdown('</div>', unsafe_allow_html=True)

    # Simulation Logic
    if st.session_state.get("eval_running"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(100):
            time.sleep(0.02) # Simulate work
            progress_bar.progress(i + 1)
            status_text.text(f"Processing sample {i+1}/100...")
        
        st.session_state.eval_running = False
        st.session_state.eval_done = True
        st.rerun()

    # Results Display
    if st.session_state.get("eval_done"):
        with col_stats:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("🏆 Evaluation Results")
            
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Accuracy", "94.2%", "+1.2%")
            with m2:
                st.metric("Precision", "91.5%", "+0.5%")
            with m3:
                st.metric("Recall", "88.9%", "-0.2%")
            
            st.markdown('</div>', unsafe_allow_html=True)

        # Confusion Matrix & Details
        c1, c2 = st.columns([1, 1])
        
        with c1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### Confusion Matrix")
            
            # Mock Confusion Matrix Data
            cm_data = [[45, 5], [8, 42]]
            fig_cm = px.imshow(cm_data, 
                               labels=dict(x="Predicted", y="Actual", color="Count"),
                               x=['Legit', 'Fraud'],
                               y=['Legit', 'Fraud'],
                               text_auto=True,
                               color_continuous_scale='Blues',
                               template="plotly_dark")
            fig_cm.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_cm, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with c2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### ⚠️ Misclassified Samples")
            
            misclassified = [
                {"ID": "CLM-102", "Actual": "Fraud", "Pred": "Legit", "Conf": 0.45},
                {"ID": "CLM-156", "Actual": "Legit", "Pred": "Fraud", "Conf": 0.62},
                {"ID": "CLM-189", "Actual": "Fraud", "Pred": "Legit", "Conf": 0.38},
                {"ID": "CLM-201", "Actual": "Legit", "Pred": "Fraud", "Conf": 0.55},
            ]
            df_miss = pd.DataFrame(misclassified)
            st.dataframe(df_miss, use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)
