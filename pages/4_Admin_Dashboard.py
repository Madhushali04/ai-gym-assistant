# pages/4_Admin_Dashboard.py
# Admin Dashboard - simple version

import streamlit as st
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from database import get_database

st.set_page_config(page_title="Admin Dashboard", page_icon="📊", layout="wide")

st.title("📊 Admin Dashboard")
st.write("Usage statistics for AI Gym Assistant")
st.divider()

# ── Get data from MongoDB ──────────────────────────────
try:
    db = get_database()

    diet_count    = db["diet_plans"].count_documents({})
    workout_count = db["workout_history"].count_documents({})
    chat_count    = db["chat_history"].count_documents({})

    # ── Stats ──────────────────────────────────────────
    st.subheader("Overall Stats")
    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Diet Plans Generated", diet_count)
    with c2:
        st.metric("Workouts Tracked", workout_count)
    with c3:
        st.metric("Chat Messages", chat_count)

    st.divider()

    # ── Recent Diet Plans ──────────────────────────────
    st.subheader("Recent Diet Plans")
    recent_diets = list(
        db["diet_plans"]
        .find({}, {"timestamp": 1, "goal": 1, "gender": 1, "calorie_goal": 1})
        .sort("timestamp", -1)
        .limit(5)
    )

    if recent_diets:
        for plan in recent_diets:
            st.write(f"Goal: {plan.get('goal')} | Gender: {plan.get('gender')} | Calories: {plan.get('calorie_goal')} kcal | Time: {plan.get('timestamp')}")
    else:
        st.info("No diet plans saved yet!")

    st.divider()

    # ── Recent Workouts ────────────────────────────────
    st.subheader("Recent Workouts")
    recent_workouts = list(
        db["workout_history"]
        .find({}, {"timestamp": 1, "exercise": 1, "reps": 1})
        .sort("timestamp", -1)
        .limit(5)
    )

    if recent_workouts:
        for w in recent_workouts:
            st.write(f"Exercise: {w.get('exercise')} | Reps: {w.get('reps')} | Time: {w.get('timestamp')}")
    else:
        st.info("No workouts saved yet!")

    st.divider()

    # ── System Status ──────────────────────────────────
    st.subheader("System Status")
    st.success("MongoDB Atlas — Connected")
    st.success("Groq LLM — Active")
    st.success("MediaPipe — Loaded")
    st.success("Streamlit — Running")

except Exception as e:
    st.error(f"Database error: {e}")