# chatbot.py
# This file handles all the AI chat logic
# It talks to Groq AI and remembers the conversation!

import os
from groq import Groq
from dotenv import load_dotenv

# Load our API key from .env file
load_dotenv()

# Connect to Groq AI
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# SYSTEM PROMPT
# This tells the AI WHO it is
# Like giving it a job description!

SYSTEM_PROMPT = """
You are FitBot - a friendly and motivating gym buddy AI assistant.

Your personality:
- Energetic and encouraging
- You talk like a supportive friend, not a robot
- You use simple language
- You give practical fitness advice
- You celebrate the user's progress
- You motivate them when they feel lazy or sad

You can help with:
- Workout tips and exercise advice
- Motivation and encouragement  
- Answering fitness questions
- Suggesting exercises for specific goals
- Giving rest day advice
- Nutrition tips (basic ones)

Important rules:
- Keep responses short and friendly (3-5 lines max)
- Always end with an encouraging line
- If user seems sad or tired, be extra supportive
- Use simple Indian English that everyone understands
"""

# FUNCTION 1: Detect User's Mood
# We check if the user seems sad/tired/happy
# So our AI can respond appropriately

def detect_mood(user_message):
    # Convert to lowercase so comparison works
    message = user_message.lower()

    # Check for sad/negative words
    sad_words = ["tired", "lazy", "sad", "demotivated", "give up",
                 "cant", "can't", "hate", "bored", "skip", "miss"]

    # Check for happy/positive words
    happy_words = ["great", "amazing", "awesome", "did it", "completed",
                   "finished", "proud", "motivated", "strong", "best"]

    # Check which mood matches
    for word in sad_words:
        if word in message:
            return "sad"

    for word in happy_words:
        if word in message:
            return "happy"

    # Default mood if no keywords found
    return "neutral"

# FUNCTION 2: Get AI Response
# This sends the full conversation to AI
# AI reads everything and replies smartly

def get_ai_response(chat_history):
    # chat_history is a list of all messages so far
    # Example:
    # [
    #   {"role": "user", "content": "I feel lazy today"},
    #   {"role": "assistant", "content": "Hey! That's okay..."},
    #   {"role": "user", "content": "I want to skip gym"}
    # ]

    # We add the system prompt at the very beginning
    # This tells AI to act as FitBot
    messages_to_send = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ] + chat_history
    # The + joins the system prompt with the actual chat

    # Send everything to Groq AI
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages_to_send,
        temperature=0.8,   # slightly creative for personality
        max_tokens=300,    # keep responses short
    )

    # Extract just the text reply
    reply = response.choices[0].message.content
    return reply

# FUNCTION 3: Build First Message
def get_welcome_message():
    return "Hey! I'm FitBot 💪 Your personal gym buddy! Ask me anything about workouts, fitness tips, or just tell me how you're feeling today. Let's crush those goals together! 🔥"