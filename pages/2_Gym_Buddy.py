# pages/2_Gym_Buddy.py
# Module 5 - Virtual Gym Buddy Chatbot

import streamlit as st
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'modules', 'module5_gym_buddy'))

from chatbot import get_ai_response, detect_mood, get_welcome_message

st.set_page_config(
    page_title="Gym Buddy Chatbot",
    page_icon="💪",
    layout="centered"
)

st.title("💪 FitBot - Your AI Gym Buddy")
st.write("Chat with your personal fitness coach!")

# ── Session state ──────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": get_welcome_message()
    })

# ── Sidebar ────────────────────────────────────────────
st.sidebar.header("FitBot Menu")
st.sidebar.write("**Quick Questions:**")
st.sidebar.write("- What workout should I do today?")
st.sidebar.write("- I feel tired, should I skip gym?")
st.sidebar.write("- Give me a 10 minute home workout")
st.sidebar.write("- How many calories does running burn?")
st.sidebar.write("- I completed my workout today!")

if st.sidebar.button("Start New Chat"):
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": get_welcome_message()
    })
    st.rerun()

# ── Display messages ───────────────────────────────────
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "mood" in message:
            if message["mood"] == "sad":
                st.caption("Mood detected: feeling low 😔")
            elif message["mood"] == "happy":
                st.caption("Mood detected: feeling great 😄")
        st.write(message["content"])

# ── Chat input ─────────────────────────────────────────
user_input = st.chat_input("Type your message here...")

if user_input:
    mood = detect_mood(user_input)
    st.session_state.messages.append({
        "role": "user", "content": user_input, "mood": mood
    })

    with st.chat_message("user"):
        if mood == "sad":
            st.caption("Mood detected: feeling low 😔")
        elif mood == "happy":
            st.caption("Mood detected: feeling great 😄")
        st.write(user_input)

    chat_for_ai = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
    ]

    with st.chat_message("assistant"):
        with st.spinner("FitBot is thinking..."):
            reply = get_ai_response(chat_for_ai)
        st.write(reply)

    st.session_state.messages.append({
        "role": "assistant", "content": reply
    })
     # ── Save to MongoDB ────────────────────────────────
    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
        from database import save_chat_message
        save_chat_message("user", user_input, mood)
        save_chat_message("assistant", reply)
    except Exception as e:
        pass  # silently continue if save fails