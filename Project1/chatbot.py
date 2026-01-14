import streamlit as st
import google.generativeai as genai
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="Gemini Chatbot",
    page_icon="💬",
    layout="wide"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history_file" not in st.session_state:
    st.session_state.chat_history_file = "chat_history.json"

# Load chat history from file
def load_chat_history():
    """Load chat history from JSON file"""
    if os.path.exists(st.session_state.chat_history_file):
        try:
            with open(st.session_state.chat_history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error loading chat history: {e}")
            return []
    return []

# Save chat history to file
def save_chat_history():
    """Save chat history to JSON file"""
    try:
        with open(st.session_state.chat_history_file, 'w', encoding='utf-8') as f:
            json.dump(st.session_state.messages, f, indent=2, ensure_ascii=False)
    except Exception as e:
        st.error(f"Error saving chat history: {e}")

# Initialize Gemini API
def initialize_gemini():
    """Initialize Gemini API with API key"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        api_key = st.sidebar.text_input(
            "Enter your Gemini API Key",
            type="password",
            help="Get your free API key from https://makersuite.google.com/app/apikey"
        )
        if api_key:
            st.session_state.api_key = api_key
            genai.configure(api_key=api_key)
            return True
        else:
            st.warning("⚠️ Please enter your Gemini API key in the sidebar to start chatting.")
            return False
    else:
        genai.configure(api_key=api_key)
        return True

# Load existing chat history on startup
if not st.session_state.messages:
    loaded_history = load_chat_history()
    if loaded_history:
        st.session_state.messages = loaded_history

# Sidebar for API key and controls
with st.sidebar:
    st.title("⚙️ Settings")
    
    # API Key input
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            help="Get your free API key from https://makersuite.google.com/app/apikey"
        )
        if api_key:
            os.environ["GEMINI_API_KEY"] = api_key
            genai.configure(api_key=api_key)
    
    st.divider()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        if os.path.exists(st.session_state.chat_history_file):
            os.remove(st.session_state.chat_history_file)
        st.rerun()
    
    # Download chat history
    if st.session_state.messages:
        chat_json = json.dumps(st.session_state.messages, indent=2, ensure_ascii=False)
        st.download_button(
            label="📥 Download Chat History",
            data=chat_json,
            file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    st.divider()
    st.info("💡 This chatbot uses Google's Gemini Pro API. All conversations are saved locally.")

# Main chat interface
st.title("💬 Gemini Chatbot")
st.caption("Powered by Google Gemini Pro - Your conversations are automatically saved!")

# Initialize Gemini
if not initialize_gemini():
    st.stop()

# Initialize the model
try:
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    st.error(f"Error initializing model: {e}")
    st.stop()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "timestamp" in message:
            st.caption(f"🕒 {message['timestamp']}")

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message to chat history
    user_message = {
        "role": "user",
        "content": prompt,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.messages.append(user_message)
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
        st.caption(f"🕒 {user_message['timestamp']}")
    
    # Get response from Gemini
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Prepare conversation history for the model
                conversation_history = []
                for msg in st.session_state.messages[:-1]:  # Exclude the current prompt
                    conversation_history.append({
                        "role": msg["role"],
                        "parts": [msg["content"]]
                    })
                
                # Generate response
                response = model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.7,
                        top_p=0.8,
                        top_k=40,
                    )
                )
                
                assistant_response = response.text
                
                # Display assistant response
                st.markdown(assistant_response)
                
                # Add assistant message to chat history
                assistant_message = {
                    "role": "assistant",
                    "content": assistant_response,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state.messages.append(assistant_message)
                
                # Save chat history to file
                save_chat_history()
                
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
