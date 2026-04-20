# app.py
# AI Gym Trainer - Pose Detection
# Supports 6 exercises!

import streamlit as st
import cv2
from pose_utils import RepCounter, process_frame

# ══════════════════════════════════════
# PAGE SETUP
# ══════════════════════════════════════
st.set_page_config(
    page_title="AI Gym Trainer",
    page_icon="🏋️",
    layout="wide"
)

st.title("🏋️ AI Gym Trainer — Pose Detection")
st.write("Real-time exercise tracking using your webcam!")

# ══════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════
st.sidebar.header("Exercise Settings")

exercise = st.sidebar.selectbox(
    "Choose Exercise",
    [
        "Bicep Curl",
        "Squat",
        "Shoulder Press",
        "Lateral Raise",
        "Lunge",
        "Tricep Extension"
    ]
)

st.sidebar.write("---")
st.sidebar.write("**How to do each exercise:**")
st.sidebar.write("💪 **Bicep Curl** — face sideways, curl right arm up and down")
st.sidebar.write("🦵 **Squat** — face sideways, bend knees and stand back up")
st.sidebar.write("🙌 **Shoulder Press** — face sideways, push right arm up overhead")
st.sidebar.write("🦾 **Lateral Raise** — face camera, raise right arm out to side")
st.sidebar.write("🏃 **Lunge** — face sideways, step forward and bend knee")
st.sidebar.write("💪 **Tricep Extension** — face sideways, extend arm straight up")
st.sidebar.write("---")
st.sidebar.write("**Tips:**")
st.sidebar.write("- Good lighting helps detection")
st.sidebar.write("- Keep your full body in frame")
st.sidebar.write("- Move slowly and steadily")

# ══════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════
if "rep_counter" not in st.session_state:
    st.session_state.rep_counter = RepCounter()

if "camera_on" not in st.session_state:
    st.session_state.camera_on = False

# Reset reps when exercise changes
if "current_exercise" not in st.session_state:
    st.session_state.current_exercise = exercise

if st.session_state.current_exercise != exercise:
    st.session_state.rep_counter.reset()
    st.session_state.current_exercise = exercise

# ══════════════════════════════════════
# BUTTONS
# ══════════════════════════════════════
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("▶ Start Camera", type="primary"):
        st.session_state.camera_on = True
        st.session_state.rep_counter.reset()

with col2:
    if st.button("⏹ Stop Camera"):
        st.session_state.camera_on = False

with col3:
    if st.button("🔄 Reset Reps"):
        st.session_state.rep_counter.reset()

# ══════════════════════════════════════
# STATS ROW
# ══════════════════════════════════════
st.write("---")
stat1, stat2, stat3 = st.columns(3)

with stat1:
    st.metric("Exercise", exercise)

with stat2:
    st.metric("Reps", st.session_state.rep_counter.count)

with stat3:
    st.metric(
        "Stage",
        st.session_state.rep_counter.stage or "Not started"
    )

# Feedback message
st.info(f"💬 {st.session_state.rep_counter.feedback}")

# ══════════════════════════════════════
# WEBCAM FEED
# ══════════════════════════════════════
st.write("---")

frame_placeholder = st.empty()

if st.session_state.camera_on:

    st.write("📷 Camera is ON — do your exercise!")

    cap = cv2.VideoCapture(0)

    while st.session_state.camera_on:

        success, frame = cap.read()

        if not success:
            st.error("Cannot access camera! Make sure webcam is connected.")
            break

        # Mirror effect
        frame = cv2.flip(frame, 1)

        # Process frame for pose + rep counting
        processed_frame, count, stage, feedback = process_frame(
            frame,
            st.session_state.rep_counter,
            exercise
        )

        # Update session state
        st.session_state.rep_counter.count    = count
        st.session_state.rep_counter.stage    = stage
        st.session_state.rep_counter.feedback = feedback

        # Convert BGR to RGB for display
        display_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)

        # Show frame in browser
        frame_placeholder.image(
            display_frame,
            channels="RGB",
            use_container_width=True
        )

    cap.release()

else:
    frame_placeholder.markdown(
        """
        <div style='text-align:center; padding:80px;
        border: 2px dashed gray; border-radius:10px;'>
        <h2>📷 Camera is OFF</h2>
        <p>Select your exercise from the sidebar</p>
        <p>then click <b>▶ Start Camera</b> to begin!</p>
        </div>
        """,
        unsafe_allow_html=True
    )