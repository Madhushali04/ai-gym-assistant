# 🏋️ AI Gym & Fitness Assistant

A complete AI-powered fitness application built as a Major Project
for the Artificial Intelligence Program at Unlox Academy.
## 🚀 Live App
👉 https://nexfit-ai.streamlit.app,to access camera ,kindy run locally using [streamlit run Home.py]
---

## 👩‍💻 Developer
- **Name:** Madhumitha
- **College:** Brindavan College of Engineering
- **Specialization:** IoT, Cybersecurity and Blockchain Technology
- **Internship:** Unlox Academy — AI Program
- **Batch:** February 2026

---

## 📌 Project Overview
The AI Gym & Fitness Assistant is a unified system that helps users
manage their fitness journey using Artificial Intelligence.
It includes 3 core AI modules built with Python and Streamlit,
connected to MongoDB Atlas cloud database and powered by
Groq LLaMA 3.3 70B language model.

---

## 🧩 Modules Built

### Module 1 — AI Gym Trainer (Pose Detection)
- Real-time pose detection using MediaPipe
- Supports 6 exercises: Bicep Curl, Squat, Shoulder Press,
  Lateral Raise, Lunge, Tricep Extension
- Automatic rep counter
- Live skeleton drawing on webcam feed
- Form feedback messages
- Workout history saved to MongoDB

### Module 2 — AI Dietician & Calorie Coach
- BMI calculator with category detection
- Daily calorie calculator using Mifflin-St Jeor formula
- Macro targets (Protein, Carbs, Fat)
- AI-generated personalized Indian meal plan using Groq LLaMA 3.3
- Weekly grocery list generator
- Visual analytics using Plotly charts (BMI gauge, macro pie, calorie bar)
- Diet plans saved to MongoDB Atlas
- Download plan as text file

### Module 5 — Virtual Gym Buddy Chatbot
- AI fitness coach powered by Groq LLaMA 3.3 70B
- Mood detection (happy / sad / neutral) using TextBlob
- Remembers full conversation history
- Motivational responses based on mood
- Chat history saved to MongoDB
- Quick question suggestions in sidebar

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| Backend | Python 3.13 |
| AI / LLM | Groq API (LLaMA 3.3 70B) |
| Pose Detection | MediaPipe 0.10.33 |
| Computer Vision | OpenCV |
| Sentiment Analysis | TextBlob + NLTK |
| Database | MongoDB Atlas (Cloud) |
| Analytics | Plotly |
| Storage | Local file system + MongoDB |
| Environment | python-dotenv |

> Note: Firebase Storage was evaluated but requires a paid Blaze plan.
> As an alternative, files are saved locally and metadata stored in MongoDB Atlas.

---
---

## ⚙️ How to Run

### Step 1 — Clone or download the project

### Step 2 — Create virtual environment
```bash
python -m venv venv --without-pip
venv\Scripts\Activate.ps1
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```

### Step 3 — Install packages
```bash
pip install -r requirements.txt
```

### Step 4 — Add your API keys
Create a `.env` file:
GROQ_API_KEY=your_groq_key_here
MONGO_URI=your_mongodb_atlas_uri_here
Get free Groq key at: https://console.groq.com

### Step 5 — Run the app
```bash
streamlit run Home.py
```

Open browser at: http://localhost:8501
## 📊 Features Summary

| Module | Feature | Status |
|--------|---------|--------|
| Dietician | BMI Calculator | ✅ Working |
| Dietician | AI Diet Plan | ✅ Working |
| Dietician | Grocery List | ✅ Working |
| Dietician | Download Plan | ✅ Working |
| Dietician | Plotly Charts | ✅ Working |
| Dietician | MongoDB Save | ✅ Working |
| Gym Buddy | AI Chat | ✅ Working |
| Gym Buddy | Mood Detection | ✅ Working |
| Gym Buddy | MongoDB Save | ✅ Working |
| Pose Trainer | Webcam Feed | ✅ Working |
| Pose Trainer | Rep Counter | ✅ Working |
| Pose Trainer | 6 Exercises | ✅ Working |
| Pose Trainer | MongoDB Save | ✅ Working |

---

## 🔗 Links
- Groq API: https://console.groq.com
- MongoDB Atlas: https://mongodb.com/atlas
- MediaPipe: https://mediapipe.dev
- Streamlit: https://streamlit.io