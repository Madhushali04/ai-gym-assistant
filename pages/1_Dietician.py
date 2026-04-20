# pages/1_Dietician.py
# Module 2 - AI Dietician & Calorie Coach

import streamlit as st
import sys
import os
import plotly.graph_objects as go

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'modules', 'module2_dietician'))

from diet_utils import calculate_bmi, calculate_calories, get_calorie_goal, get_macros
from llm_utils import generate_diet_plan, generate_grocery_list

st.set_page_config(
    page_title="AI Dietician",
    page_icon="🥗",
    layout="wide"
)

st.title("🥗 AI Dietician & Calorie Coach")
st.write("Fill in your details and get a personalized diet plan powered by AI!")

# ── Sidebar inputs ─────────────────────────────────────
st.sidebar.header("Enter Your Details")

age       = st.sidebar.number_input("Your Age", min_value=10, max_value=100, value=21)
gender    = st.sidebar.selectbox("Your Gender", ["Female", "Male"])
weight    = st.sidebar.number_input("Your Weight (kg)", min_value=30.0, max_value=200.0, value=60.0)
height    = st.sidebar.number_input("Your Height (cm)", min_value=100.0, max_value=250.0, value=165.0)

activity  = st.sidebar.selectbox("How Active Are You?", [
    "Sedentary (little/no exercise)",
    "Lightly active (1-3 days/week)",
    "Moderately active (3-5 days/week)",
    "Very active (6-7 days/week)",
    "Super active (athlete/physical job)"
])

goal      = st.sidebar.selectbox("Your Goal", ["Lose weight", "Maintain weight", "Gain muscle"])
diet_type = st.sidebar.selectbox("Your Diet Type", ["Non-vegetarian", "Vegetarian", "Vegan", "Eggetarian"])
allergies = st.sidebar.text_input("Any allergies or foods to avoid?", placeholder="Example: nuts, dairy")
generate  = st.sidebar.button("Generate My Diet Plan", type="primary")

# ── Calculations ───────────────────────────────────────
bmi, bmi_category         = calculate_bmi(weight, height)
tdee                      = calculate_calories(weight, height, age, gender, activity)
calorie_goal              = get_calorie_goal(tdee, goal)
protein_g, carbs_g, fat_g = get_macros(calorie_goal, goal)

# ── Stats Metrics ──────────────────────────────────────
st.subheader("Your Daily Stats")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Your BMI", bmi, bmi_category)
with col2:
    st.metric("Calories to Maintain", f"{tdee} kcal")
with col3:
    st.metric("Your Calorie Goal", f"{calorie_goal} kcal", goal)

# ── Macro Metrics ──────────────────────────────────────
st.subheader("Your Daily Macro Targets")
m1, m2, m3 = st.columns(3)
with m1:
    st.metric("Protein", f"{protein_g}g")
with m2:
    st.metric("Carbohydrates", f"{carbs_g}g")
with m3:
    st.metric("Fat", f"{fat_g}g")

# ── Charts ─────────────────────────────────────────────
st.subheader("Your Stats Visualized")
chart1, chart2, chart3 = st.columns(3)

# Chart 1: Macro Pie Chart
with chart1:
    fig_pie = go.Figure(data=[go.Pie(
        labels=["Protein", "Carbs", "Fat"],
        values=[protein_g, carbs_g, fat_g],
        hole=0.4,
        marker=dict(colors=["#00c9ff", "#92fe9d", "#f7971e"])
    )])
    fig_pie.update_layout(
        title="Macro Split",
        showlegend=True,
        height=300,
        margin=dict(t=40, b=0, l=0, r=0),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# Chart 2: BMI Gauge
with chart2:
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=bmi,
        title={"text": "BMI Gauge", "font": {"color": "white"}},
        gauge={
            "axis": {"range": [10, 40]},
            "bar":  {"color": "#00c9ff"},
            "steps": [
                {"range": [10, 18.5], "color": "#3498db"},
                {"range": [18.5, 25], "color": "#2ecc71"},
                {"range": [25, 30],   "color": "#f39c12"},
                {"range": [30, 40],   "color": "#e74c3c"},
            ],
            "threshold": {
                "line":      {"color": "white", "width": 4},
                "thickness": 0.75,
                "value":     bmi
            }
        },
        number={"font": {"color": "white"}}
    ))
    fig_gauge.update_layout(
        height=300,
        margin=dict(t=40, b=0, l=20, r=20),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

# Chart 3: Calorie Bar Chart
with chart3:
    fig_bar = go.Figure(data=[
        go.Bar(
            x=["Maintenance", "Your Goal"],
            y=[tdee, calorie_goal],
            marker_color=["#92fe9d", "#00c9ff"],
            text=[f"{tdee} kcal", f"{calorie_goal} kcal"],
            textposition="auto"
        )
    ])
    fig_bar.update_layout(
        title="Calorie Comparison",
        height=300,
        margin=dict(t=40, b=0, l=0, r=0),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        yaxis=dict(gridcolor="#333333")
    )
    st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# ── AI Diet Plan ───────────────────────────────────────
if generate:
    with st.spinner("AI is creating your diet plan..."):
        diet_plan = generate_diet_plan(
            age, gender, weight, height, goal, diet_type,
            allergies if allergies else "None",
            calorie_goal, protein_g, carbs_g, fat_g
        )
    st.subheader("Your Personalized Diet Plan")
    st.markdown(diet_plan)
    st.divider()

    with st.spinner("Creating your grocery list..."):
        grocery_list = generate_grocery_list(diet_plan)
    st.subheader("Your Weekly Grocery List")
    st.markdown(grocery_list)
    st.divider()

    # ── Save to MongoDB ────────────────────────────────
    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
        from database import save_diet_plan
        save_diet_plan(
            age, gender, weight, height,
            goal, diet_type, calorie_goal,
            diet_plan, grocery_list
        )
        st.success("Diet plan saved to database!")
    except Exception as e:
        st.warning(f"Could not save to database: {e}")

    # ── Download button ────────────────────────────────
    full_plan = f"MY DIET PLAN\n\n{diet_plan}\n\nMY GROCERY LIST\n\n{grocery_list}"
    st.download_button(
        "Download My Plan",
        data=full_plan,
        file_name="my_diet_plan.txt",
        mime="text/plain"
    )

else:
    st.info("Fill in your details on the left and click Generate My Diet Plan!")