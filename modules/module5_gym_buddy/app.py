# app.py
# This is the chat interface for our Gym Buddy
# It looks and works like WhatsApp - you type, AI replies!

import streamlit as st
from chatbot import get_ai_response, detect_mood, get_welcome_message

# ══════════════════════════════════════
# PAGE SETUP
# ══════════════════════════════════════
st.set_page_config(
    page_title="FitBot - Gym Buddy",
    page_icon="💪",
    layout="centered"    # centered looks better for chat
)

st.title("💪 FitBot - Your AI Gym Buddy")
st.write("Chat with your personal fitness coach! Ask anything about workouts or fitness.")

# ══════════════════════════════════════
# CHAT HISTORY
# st.session_state remembers things
# even when Streamlit reruns the page
# Without this, chat would reset every time!
# ══════════════════════════════════════

# First time opening app - set up empty chat
if "messages" not in st.session_state:
    st.session_state.messages = []  # empty list to store chat

    # Add FitBot's welcome message as first message
    welcome = get_welcome_message()
    st.session_state.messages.append({
        "role": "assistant",    # assistant = FitBot
        "content": welcome
    })

# ══════════════════════════════════════
# SIDEBAR - user info and tips
# ══════════════════════════════════════
st.sidebar.header("FitBot Menu")
st.sidebar.write("**Quick Questions to Ask:**")
st.sidebar.write("- What workout should I do today?")
st.sidebar.write("- I feel tired, should I skip gym?")
st.sidebar.write("- Give me a 10 minute home workout")
st.sidebar.write("- How many calories does running burn?")
st.sidebar.write("- I completed my workout today!")

# Clear chat button in sidebar
if st.sidebar.button("Start New Chat"):
    # Reset everything
    st.session_state.messages = []
    welcome = get_welcome_message()
    st.session_state.messages.append({
        "role": "assistant",
        "content": welcome
    })
    st.rerun()   # refresh the page

# ══════════════════════════════════════
# DISPLAY ALL CHAT MESSAGES
# Loop through history and show each message
# ══════════════════════════════════════

for message in st.session_state.messages:
    # message["role"] is either "user" or "assistant"
    with st.chat_message(message["role"]):
        # Show mood emoji if it exists
        if "mood" in message:
            if message["mood"] == "sad":
                st.caption("Mood detected: feeling low 😔")
            elif message["mood"] == "happy":
                st.caption("Mood detected: feeling great 😄")

        # Show the actual message text
        st.write(message["content"])

# ══════════════════════════════════════
# CHAT INPUT BOX
# This is the text box at the bottom
# Streamlit shows it automatically at bottom
# ══════════════════════════════════════

user_input = st.chat_input("Type your message here...")

# This runs only when user sends a message
if user_input:

    # Step 1: Detect the mood
    mood = detect_mood(user_input)

    # Step 2: Save user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "mood": mood
    })

    # Step 3: Show user message on screen
    with st.chat_message("user"):
        if mood == "sad":
            st.caption("Mood detected: feeling low 😔")
        elif mood == "happy":
            st.caption("Mood detected: feeling great 😄")
        st.write(user_input)

    # Step 4: Get AI reply
    # We only send role+content to AI (not mood)
    chat_for_ai = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
    ]

    # Show loading spinner while AI thinks
    with st.chat_message("assistant"):
        with st.spinner("FitBot is thinking..."):
            reply = get_ai_response(chat_for_ai)
        st.write(reply)

    # Step 5: Save AI reply to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": reply
    })