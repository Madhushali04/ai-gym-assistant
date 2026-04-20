# pages/3_Pose_Trainer.py
import streamlit as st
import cv2
import sys
import os

# ── Fix paths ──────────────────────────────────────────
current_dir  = os.path.dirname(os.path.abspath(__file__))
root_dir     = os.path.join(current_dir, '..')
module_path  = os.path.join(root_dir, 'modules', 'module1_pose_trainer')
model_file   = os.path.join(module_path, 'pose_landmarker.task')

sys.path.insert(0, module_path)

st.set_page_config(
    page_title="AI Gym Trainer",
    page_icon="🏋️",
    layout="wide"
)

st.title("🏋️ AI Gym Trainer — Pose Detection")
st.write("Real-time exercise tracking using your webcam!")

# ── Check model file exists before doing anything ──────
if not os.path.exists(model_file):
    st.error(f"Model file not found at: {model_file}")
    st.info("Run this in terminal to fix it:")
    st.code(f'python -c "import urllib.request; urllib.request.urlretrieve(\'https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task\', r\'{model_file}\')"')
    st.stop()

# ── Import after path is set ───────────────────────────
try:
    from pose_utils import RepCounter, process_frame
    st.success("Pose detection loaded successfully!")
except Exception as e:
    st.error(f"Import error: {e}")
    st.stop()

# ── Sidebar ────────────────────────────────────────────
st.sidebar.header("Exercise Settings")

exercise = st.sidebar.selectbox("Choose Exercise", [
    "Bicep Curl",
    "Squat",
    "Shoulder Press",
    "Lateral Raise",
    "Lunge",
    "Tricep Extension"
])

st.sidebar.write("---")
st.sidebar.write("**Tips:**")
st.sidebar.write("- Good lighting helps detection")
st.sidebar.write("- Keep full body in frame")
st.sidebar.write("- Move slowly and steadily")

# ── Session state ──────────────────────────────────────
if "rep_counter" not in st.session_state:
    st.session_state.rep_counter = RepCounter()

if "camera_on" not in st.session_state:
    st.session_state.camera_on = False

if "current_exercise" not in st.session_state:
    st.session_state.current_exercise = exercise

if st.session_state.current_exercise != exercise:
    st.session_state.rep_counter.reset()
    st.session_state.current_exercise = exercise

# ── Buttons ────────────────────────────────────────────
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

# ── Stats ──────────────────────────────────────────────
st.write("---")
s1, s2, s3 = st.columns(3)
with s1:
    st.metric("Exercise", exercise)
with s2:
    st.metric("Reps", st.session_state.rep_counter.count)
with s3:
    st.metric("Stage", st.session_state.rep_counter.stage or "Not started")

st.info(f"💬 {st.session_state.rep_counter.feedback}")
st.write("---")

# ── Webcam ─────────────────────────────────────────────
frame_placeholder = st.empty()

if st.session_state.camera_on:
    st.write("📷 Camera is ON — do your exercise!")
    cap = cv2.VideoCapture(0)

    while st.session_state.camera_on:
        success, frame = cap.read()
        if not success:
            st.error("Cannot access camera!")
            break

        frame = cv2.flip(frame, 1)

        try:
            processed_frame, count, stage, feedback = process_frame(
                frame, st.session_state.rep_counter, exercise
            )
            st.session_state.rep_counter.count    = count
            st.session_state.rep_counter.stage    = stage
            st.session_state.rep_counter.feedback = feedback
            display_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            frame_placeholder.image(display_frame, channels="RGB", use_container_width=True)

        except Exception as e:
            st.error(f"Processing error: {e}")
            break
     # ── Save workout to MongoDB when camera stops ──────
    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
        from database import save_workout
        if st.session_state.rep_counter.count > 0:
            save_workout(exercise, st.session_state.rep_counter.count)
            st.success(f"Workout saved! {exercise}: {st.session_state.rep_counter.count} reps")
    except Exception as e:
        pass   

    cap.release()
else:
    frame_placeholder.markdown("""
        <div style='text-align:center; padding:80px;
        border: 2px dashed gray; border-radius:10px;'>
        <h2>📷 Camera is OFF</h2>
        <p>Select exercise from sidebar</p>
        <p>then click <b>▶ Start Camera</b></p>
        </div>""", unsafe_allow_html=True)