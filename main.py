import streamlit as st
import google.generativeai as genai
import time

# ✅ Set Page Config FIRST (Fixes Streamlit error)
st.set_page_config(page_title="CHATALI", layout="wide", page_icon="🤖")

# ✅ Load API Key from Streamlit Secrets
try:
    GENAI_API_KEY = st.secrets["GEMINI"]["API_KEY"]  # Fetch API key from secrets.toml
except FileNotFoundError:
    st.error("❌ Secrets file not found! Ensure `.streamlit/secrets.toml` exists.")
    st.stop()
except KeyError:
    st.error("❌ API Key missing in `secrets.toml`. Add `[GEMINI] API_KEY = 'your_key'`")
    st.stop()

# ✅ Configure Gemini API
genai.configure(api_key=GENAI_API_KEY)

# 🔹 Function to interact with Gemini
def get_gemini_response(prompt):
    try:
        model = genai.GenerativeModel("gemini-2.5-pro-latest")  # Ensure this model exists
        response = model.generate_content(prompt)
        return response.text if response else "⚠️ Sorry, I couldn't process that."
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# 🔹 Chatbot UI
st.title("🤖 CHATALI AI Chatbot")
st.write("Welcome to your AI-powered assistant! Ask me anything.")

# ✅ Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# ✅ Sidebar for Clearing Chat
with st.sidebar:
    if st.button("🗑️ Clear Chat", key="clear_chat"):
        st.session_state.messages = []
        st.rerun()

    st.header("ℹ️ About")
    st.write("This chatbot can help you with a wide range of tasks!")

# ✅ Display Chat History
for role, text in st.session_state.messages:
    with st.chat_message(role, avatar="👤" if role == "user" else "🤖"):
        st.write(text)

# ✅ User Input
user_input = st.chat_input("Type your message...")

# ✅ When user sends a message
if user_input:
    st.session_state.messages.append(("user", user_input))

    with st.chat_message("user", avatar="👤"):
        st.write(user_input)

    with st.spinner("Thinking..."):
        response = get_gemini_response(user_input)
        time.sleep(1)

    st.session_state.messages.append(("assistant", response))

    with st.chat_message("assistant", avatar="🤖"):
        st.write(response)
