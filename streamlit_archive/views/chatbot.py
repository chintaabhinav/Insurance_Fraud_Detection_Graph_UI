import streamlit as st
from utils.api_client import chat_with_graph
import time

def app():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.title("💬 Graph Chatbot")
    st.markdown("Ask questions to the knowledge graph using natural language.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Initialize Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your Fraud Detection Assistant. Ask me about suspicious claims, fraud rings, or graph patterns."}
        ]

    # Display Chat History
    for msg in st.session_state.messages:
        role_class = "user" if msg["role"] == "user" else "bot"
        avatar = "🧑‍💻" if msg["role"] == "user" else "🤖"
        
        st.markdown(f"""
        <div class="chat-message {role_class}">
            <div class="chat-avatar">{avatar}</div>
            <div class="chat-content">{msg['content']}</div>
        </div>
        """, unsafe_allow_html=True)

    # Chat Input
    if prompt := st.chat_input("Ask about fraud patterns..."):
        # Add User Message
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

    # Handle Response Generation (after rerun to show user message first)
    if st.session_state.messages[-1]["role"] == "user":
        with st.spinner("Thinking..."):
            # Simulate delay for realism
            time.sleep(0.5)
            response = chat_with_graph(st.session_state.messages[-1]["content"])
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

    # Suggested Queries
    st.markdown("### 💡 Suggested Queries")
    suggestions = [
        "Show me all high-risk claims",
        "Identify potential fraud rings",
        "Summarize the fraud statistics",
        "Check Claim #123 for fraud",
        "List top 5 suspicious providers"
    ]
    
    # Create a container for chips
    cols = st.columns(len(suggestions))
    for i, suggestion in enumerate(suggestions):
        # We use a button that updates the chat input (conceptually, but Streamlit buttons can't directly type into chat_input)
        # So we'll just make them append to history directly for now as a shortcut
        if st.button(suggestion, key=f"sugg_{i}", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": suggestion})
            st.rerun()
