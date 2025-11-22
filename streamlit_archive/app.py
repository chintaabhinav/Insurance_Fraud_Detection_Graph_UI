import streamlit as st
import os

# Page Configuration
st.set_page_config(
    page_title="FraudGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

css_path = os.path.join("assets", "style.css")
if os.path.exists(css_path):
    load_css(css_path)

# Sidebar Navigation
st.sidebar.title("🛡️ FraudGuard AI")
st.sidebar.markdown("---")

pages = {
    "Dashboard": "views/dashboard.py",
    "Upload & Detect": "views/upload.py",
    "Graph Chatbot": "views/chatbot.py",
    "System Monitoring": "views/monitoring.py",
    "Evaluation": "views/evaluation.py"
}

selection = st.sidebar.radio("Navigation", list(pages.keys()))

st.sidebar.markdown("---")
st.sidebar.info("Connected to **Neo4j** & **FastAPI**")

# Routing Logic (Simple import and run for now, or just use st.switch_page if using multipage app structure, 
# but for custom control I'll import the module)

import importlib.util
import sys

def load_view(view_name):
    # For now, we will just display a placeholder. 
    # In a real app, we would dynamically import the module.
    # But since I haven't created the files yet, I'll handle the logic here or create the files.
    
    # Dynamic import approach
    module_path = pages[view_name]
    spec_name = view_name.replace(" ", "_").replace("&", "and")
    spec = importlib.util.spec_from_file_location(spec_name, module_path)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        sys.modules[view_name] = module
        spec.loader.exec_module(module)
        if hasattr(module, "app"):
            module.app()
    else:
        st.error(f"Could not load view: {view_name}")

# Create the view files if they don't exist (I will do this in the next step, but for now app.py expects them)
if os.path.exists(pages[selection]):
    load_view(selection)
else:
    st.title(f"{selection}")
    st.write("Page under construction.")
