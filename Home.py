# Home.py
import streamlit as st

st.set_page_config(
    page_title="AI Gym Assistant",
    page_icon="🏋️",
    layout="wide"
)

# ══════════════════════════════════════
# CUSTOM CSS - makes everything look good
# ══════════════════════════════════════
st.markdown("""
<style>

/* Main background */
.main {
    background-color: #0e0e0e;
}

/* Big hero title */
.hero-title {
    font-size: 58px;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(90deg, #00c9ff, #92fe9d);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0px;
    line-height: 1.2;
}

/* Subtitle under title */
.hero-subtitle {
    font-size: 20px;
    text-align: center;
    color: #aaaaaa;
    margin-top: 10px;
    margin-bottom: 40px;
}

/* Module cards */
.card {
    background: linear-gradient(145deg, #1a1a2e, #16213e);
    border-radius: 20px;
    padding: 30px;
    text-align: center;
    border: 1px solid #00c9ff33;
    transition: transform 0.3s;
    height: 100%;
}

.card:hover {
    transform: translateY(-5px);
    border: 1px solid #00c9ff;
}

.card-icon {
    font-size: 50px;
    margin-bottom: 15px;
}

.card-title {
    font-size: 22px;
    font-weight: 700;
    color: #00c9ff;
    margin-bottom: 10px;
}

.card-desc {
    font-size: 14px;
    color: #cccccc;
    line-height: 1.8;
}

/* Stats bar */
.stat-box {
    background: linear-gradient(145deg, #1a1a2e, #16213e);
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    border: 1px solid #92fe9d33;
}

.stat-number {
    font-size: 36px;
    font-weight: 800;
    color: #92fe9d;
}

.stat-label {
    font-size: 14px;
    color: #aaaaaa;
}

/* Tech badge */
.badge {
    display: inline-block;
    background: #00c9ff22;
    color: #00c9ff;
    border: 1px solid #00c9ff55;
    border-radius: 20px;
    padding: 5px 15px;
    font-size: 13px;
    margin: 4px;
}

/* Section title */
.section-title {
    font-size: 28px;
    font-weight: 700;
    color: white;
    text-align: center;
    margin: 40px 0 20px 0;
}

/* Divider line */
.custom-divider {
    height: 2px;
    background: linear-gradient(90deg, transparent, #00c9ff, transparent);
    margin: 40px 0;
    border: none;
}

/* Footer */
.footer {
    text-align: center;
    color: #555555;
    font-size: 13px;
    margin-top: 60px;
    padding: 20px;
}

</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════
# HERO SECTION
# ══════════════════════════════════════
st.markdown("""
<div style='padding: 60px 20px 20px 20px;'>
    <div class='hero-title'>🏋️ AI Gym & Fitness Assistant</div>
    <div class='hero-subtitle'>
        Your complete AI-powered fitness companion — diet planning, 
        pose detection & motivational coaching, all in one place.
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════
# STATS ROW
# ══════════════════════════════════════
st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)

s1, s2, s3, s4 = st.columns(4)

with s1:
    st.markdown("""
    <div class='stat-box'>
        <div class='stat-number'>3</div>
        <div class='stat-label'>AI Modules</div>
    </div>
    """, unsafe_allow_html=True)

with s2:
    st.markdown("""
    <div class='stat-box'>
        <div class='stat-number'>6</div>
        <div class='stat-label'>Exercises Tracked</div>
    </div>
    """, unsafe_allow_html=True)

with s3:
    st.markdown("""
    <div class='stat-box'>
        <div class='stat-number'>33</div>
        <div class='stat-label'>Body Landmarks</div>
    </div>
    """, unsafe_allow_html=True)

with s4:
    st.markdown("""
    <div class='stat-box'>
        <div class='stat-number'>70B</div>
        <div class='stat-label'>LLM Parameters</div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════
# MODULE CARDS
# ══════════════════════════════════════
st.markdown("<div class='section-title'>Choose Your Module</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class='card'>
        <div class='card-icon'>🥗</div>
        <div class='card-title'>AI Dietician</div>
        <div class='card-desc'>
            ✦ BMI Calculator<br>
            ✦ Daily calorie targets<br>
            ✦ AI-powered Indian meal plan<br>
            ✦ Macro breakdown<br>
            ✦ Weekly grocery list<br>
            ✦ Download your plan<br><br>
            <b style='color:#00c9ff'>← Click Dietician in sidebar</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='card'>
        <div class='card-icon'>💪</div>
        <div class='card-title'>Gym Buddy Chatbot</div>
        <div class='card-desc'>
            ✦ AI fitness coach<br>
            ✦ Real-time mood detection<br>
            ✦ Personalized workout advice<br>
            ✦ Motivational support<br>
            ✦ Full conversation memory<br>
            ✦ Powered by LLaMA 3.3 70B<br><br>
            <b style='color:#00c9ff'>← Click Gym Buddy in sidebar</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='card'>
        <div class='card-icon'>🏋️</div>
        <div class='card-title'>Pose Trainer</div>
        <div class='card-desc'>
            ✦ Real-time pose detection<br>
            ✦ Automatic rep counter<br>
            ✦ 6 exercises supported<br>
            ✦ Live skeleton on webcam<br>
            ✦ Form feedback<br>
            ✦ Powered by MediaPipe<br><br>
            <b style='color:#00c9ff'>← Click Pose Trainer in sidebar</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════
# HOW IT WORKS
# ══════════════════════════════════════
st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>How It Works</div>", unsafe_allow_html=True)

h1, h2, h3, h4 = st.columns(4)

with h1:
    st.markdown("""
    <div style='text-align:center; padding: 20px;'>
        <div style='font-size:40px'>1️⃣</div>
        <div style='color:#00c9ff; font-weight:700; margin:10px 0'>Open a Module</div>
        <div style='color:#aaaaaa; font-size:14px'>
            Choose Dietician, Gym Buddy or Pose Trainer from the sidebar
        </div>
    </div>
    """, unsafe_allow_html=True)

with h2:
    st.markdown("""
    <div style='text-align:center; padding: 20px;'>
        <div style='font-size:40px'>2️⃣</div>
        <div style='color:#00c9ff; font-weight:700; margin:10px 0'>Enter Your Details</div>
        <div style='color:#aaaaaa; font-size:14px'>
            Fill in your age, weight, height, goal and preferences
        </div>
    </div>
    """, unsafe_allow_html=True)

with h3:
    st.markdown("""
    <div style='text-align:center; padding: 20px;'>
        <div style='font-size:40px'>3️⃣</div>
        <div style='color:#00c9ff; font-weight:700; margin:10px 0'>AI Does the Work</div>
        <div style='color:#aaaaaa; font-size:14px'>
            Our AI generates your plan or detects your pose in real time
        </div>
    </div>
    """, unsafe_allow_html=True)

with h4:
    st.markdown("""
    <div style='text-align:center; padding: 20px;'>
        <div style='font-size:40px'>4️⃣</div>
        <div style='color:#00c9ff; font-weight:700; margin:10px 0'>Crush Your Goals</div>
        <div style='color:#aaaaaa; font-size:14px'>
            Follow your plan, chat with FitBot and track your reps!
        </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════
# TECH STACK
# ══════════════════════════════════════
st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Built With</div>", unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center; padding: 20px;'>
    <span class='badge'>🐍 Python 3.13</span>
    <span class='badge'>⚡ Streamlit</span>
    <span class='badge'>🤖 Groq LLaMA 3.3 70B</span>
    <span class='badge'>🎯 MediaPipe</span>
    <span class='badge'>👁️ OpenCV</span>
    <span class='badge'>💬 TextBlob NLP</span>
    <span class='badge'>🔐 python-dotenv</span>
    <span class='badge'>🔢 NumPy</span>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════
# FOOTER
# ══════════════════════════════════════
st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)
st.markdown("""
<div class='footer'>
    Unlox Academy AI Program &nbsp;|&nbsp;
    February 2026 Batch &nbsp;|&nbsp;
</div>
""", unsafe_allow_html=True)