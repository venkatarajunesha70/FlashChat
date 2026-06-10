import streamlit as st
from groq import Groq

# 1. Page Configuration
st.set_page_config(page_title="Groq Chat", page_icon="💬", layout="centered")
st.title("FlashChat - Fastest Chatbot")
st.write("A lightning-fast chat interface powered by Groq.")

# 2. Initialize Groq Client
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    import os
    client = Groq(api_key=os.environ.get("GROQ_API_KEY", "api-key"))

# 3. Initialize Chat History (Session State)
# Streamlit re-runs the whole script on every interaction; session_state keeps the memory alive.
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful, concise AI assistant."},
        {"role": "assistant", "content": "Hello! How can I help you today?"}
    ]

# 4. Display Past Chat Messages
# We skip displaying the system prompt (index 0) so the user doesn't see it
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 5. Handle New User Input
if user_input := st.chat_input("Type your message here..."):
    
    # Append user message to history and instantly display it
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Generate response from Groq
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Call Groq API with the entire conversation history for context
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile", # Fast and reliable model
                    messages=st.session_state.messages,
                    temperature=0.7,
                )
                
                response_text = completion.choices[0].message.content
                
                # Display the response and save it to history
                st.write(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                
            except Exception as e:
                st.error(f"Groq API Error: {e}")