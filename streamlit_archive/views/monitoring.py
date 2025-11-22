import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.monitoring_utils import get_system_metrics
import time

def app():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.title("📈 System Monitoring")
    st.markdown("Track LLM usage, backend performance, and system health.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Auto-refresh mechanism (simulated with a rerun button for now to avoid infinite loops in dev)
    if st.button("🔄 Refresh Metrics"):
        st.rerun()

    data = get_system_metrics()
    sys_stats = data["system"]

    # --- System Health Row ---
    st.markdown("### 🖥️ System Health")
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown(f'''
        <div class="glass-card" style="text-align: center;">
            <h4 style="margin:0; color: #94a3b8;">CPU Usage</h4>
            <h1 style="margin:0; font-size: 2.5rem; color: {'#ef4444' if sys_stats['cpu'] > 80 else '#38bdf8'}">{sys_stats['cpu']}%</h1>
        </div>
        ''', unsafe_allow_html=True)
    with c2:
        st.markdown(f'''
        <div class="glass-card" style="text-align: center;">
            <h4 style="margin:0; color: #94a3b8;">Memory</h4>
            <h1 style="margin:0; font-size: 2.5rem; color: {'#ef4444' if sys_stats['memory'] > 85 else '#a855f7'}">{sys_stats['memory']}%</h1>
        </div>
        ''', unsafe_allow_html=True)
    with c3:
        st.markdown(f'''
        <div class="glass-card" style="text-align: center;">
            <h4 style="margin:0; color: #94a3b8;">API Latency</h4>
            <h1 style="margin:0; font-size: 2.5rem; color: {'#f59e0b' if sys_stats['latency'] > 500 else '#22c55e'}">{sys_stats['latency']}ms</h1>
        </div>
        ''', unsafe_allow_html=True)
    with c4:
        st.markdown(f'''
        <div class="glass-card" style="text-align: center;">
            <h4 style="margin:0; color: #94a3b8;">Active Threads</h4>
            <h1 style="margin:0; font-size: 2.5rem;">{sys_stats['threads']}</h1>
        </div>
        ''', unsafe_allow_html=True)

    # --- LLM Analytics ---
    st.markdown("### 🧠 LLM Analytics (24h)")
    col_llm1, col_llm2 = st.columns([2, 1])

    with col_llm1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Token Usage & Cost")
        df_llm = data["llm_stats"]
        
        # Dual axis chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_llm["Time"], y=df_llm["Tokens"], name="Tokens", line=dict(color="#38bdf8", width=3)))
        fig.add_trace(go.Scatter(x=df_llm["Time"], y=df_llm["Cost ($)"], name="Cost ($)", yaxis="y2", line=dict(color="#f59e0b", width=3, dash="dot")))
        
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(title="Tokens"),
            yaxis2=dict(title="Cost ($)", overlaying="y", side="right"),
            legend=dict(orientation="h", y=1.1),
            margin=dict(l=0, r=0, t=20, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_llm2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Request Volume")
        fig_bar = px.bar(df_llm, x="Time", y="Requests", template="plotly_dark", color_discrete_sequence=["#a855f7"])
        fig_bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=20, b=0)
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Live Logs ---
    st.markdown("### 📜 Backend Logs")
    logs_html = '<div style="background: #0f172a; border: 1px solid #334155; border-radius: 8px; padding: 15px; font-family: monospace; height: 300px; overflow-y: scroll;">'
    for log in data["logs"]:
        color = "#ef4444" if "ERROR" in log else "#f59e0b" if "WARNING" in log else "#22c55e"
        logs_html += f'<div style="margin-bottom: 5px;"><span style="color: {color};">{log}</span></div>'
    logs_html += '</div>'
    
    st.markdown(logs_html, unsafe_allow_html=True)
