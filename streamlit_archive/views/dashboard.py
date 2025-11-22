import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.mock_data import get_dashboard_metrics

def app():
    # Fetch Data
    data = get_dashboard_metrics()
    metrics = data["metrics"]
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.title("📊 Executive Dashboard")
    st.markdown("Real-time overview of insurance fraud detection activities.")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- Top Metrics Row ---
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown(f'''
        <div class="glass-card" style="text-align: center;">
            <h4 style="margin:0; color: #94a3b8;">Total Claims</h4>
            <h1 style="margin:0; font-size: 2.5rem;">{metrics['total']:,}</h1>
        </div>
        ''', unsafe_allow_html=True)
        
    with c2:
        st.markdown(f'''
        <div class="glass-card" style="text-align: center;">
            <h4 style="margin:0; color: #94a3b8;">Fraud Detected</h4>
            <h1 style="margin:0; font-size: 2.5rem; color: #ef4444;">{metrics['fraud_count']}</h1>
        </div>
        ''', unsafe_allow_html=True)

    with c3:
        st.markdown(f'''
        <div class="glass-card" style="text-align: center;">
            <h4 style="margin:0; color: #94a3b8;">Est. Fraud Value</h4>
            <h1 style="margin:0; font-size: 2.5rem; color: #f59e0b;">${metrics['fraud_val']/1000:.0f}k</h1>
        </div>
        ''', unsafe_allow_html=True)

    with c4:
        st.markdown(f'''
        <div class="glass-card" style="text-align: center;">
            <h4 style="margin:0; color: #94a3b8;">Avg Process Time</h4>
            <h1 style="margin:0; font-size: 2.5rem; color: #38bdf8;">{metrics['proc_time']}s</h1>
        </div>
        ''', unsafe_allow_html=True)

    # --- Charts Row ---
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("📈 Claims Timeline")
        
        # Plotly Line Chart
        df_timeline = data["timeline"]
        fig_line = px.area(
            df_timeline, 
            x="Date", 
            y=["Legitimate", "Fraudulent"],
            color_discrete_map={"Legitimate": "#38bdf8", "Fraudulent": "#ef4444"},
            template="plotly_dark"
        )
        fig_line.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=0, b=0),
            legend=dict(orientation="h", y=1.1)
        )
        st.plotly_chart(fig_line, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("🍩 Claim Types")
        
        # Plotly Donut Chart
        df_types = data["types"]
        fig_donut = px.pie(
            df_types, 
            values="Count", 
            names="Type", 
            hole=0.6,
            color_discrete_sequence=px.colors.sequential.Plasma,
            template="plotly_dark"
        )
        fig_donut.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=0, b=0),
            showlegend=False
        )
        st.plotly_chart(fig_donut, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Recent Alerts Table ---
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🚨 High Risk Alerts")
    
    alerts = data["alerts"]
    # Custom HTML Table for better styling than st.dataframe
    table_html = """
    <table style="width:100%; border-collapse: collapse; color: white;">
        <thead>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.1); text-align: left;">
                <th style="padding: 10px;">Claim ID</th>
                <th style="padding: 10px;">Type</th>
                <th style="padding: 10px;">Risk Level</th>
                <th style="padding: 10px;">Score</th>
                <th style="padding: 10px;">Date</th>
                <th style="padding: 10px;">Action</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for row in alerts:
        risk_color = "#ef4444" if row["Risk"] == "High" else "#f59e0b" if row["Risk"] == "Medium" else "#22c55e"
        table_html += f"""
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                <td style="padding: 10px; font-family: monospace;">{row['ID']}</td>
                <td style="padding: 10px;">{row['Type']}</td>
                <td style="padding: 10px;"><span style="color: {risk_color}; font-weight: bold;">{row['Risk']}</span></td>
                <td style="padding: 10px;">{row['Score']}</td>
                <td style="padding: 10px;">{row['Date']}</td>
                <td style="padding: 10px;"><button style="background: rgba(255,255,255,0.1); border: none; color: white; padding: 4px 8px; border-radius: 4px; cursor: pointer;">View</button></td>
            </tr>
        """
    
    table_html += "</tbody></table>"
    st.markdown(table_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
