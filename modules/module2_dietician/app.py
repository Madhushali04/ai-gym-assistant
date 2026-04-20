# app.py
# This is the MAIN FILE that runs our Streamlit app
# It's like the face of our dietician - what the user sees!

import streamlit as st          # for building the webpage
from diet_utils import (        # our math functions
    calculate_bmi,
    calculate_calories,
    get_calorie_goal,
    get_macros
)
from llm_utils import (         # our AI functions
    generate_diet_plan,
    generate_grocery_list
)

# ══════════════════════════════════════
# PAGE SETUP
# This runs first - sets up the webpage
# ══════════════════════════════════════
st.set_page_config(
    page_title="AI Dietician",  # browser tab title
    page_icon="🥗",             # browser tab icon
    layout="wide"               # use full screen width
)

# Big title at the top of the page
st.title("🥗 AI Dietician & Calorie Coach")
st.write("Fill in your details and get a personalized diet plan powered by AI!")

# ══════════════════════════════════════
# SIDEBAR - where user fills in details
# This appears on the LEFT side
# ══════════════════════════════════════
st.sidebar.header("Enter Your Details")

# Each of these creates an input widget in the sidebar
age = st.sidebar.number_input(
    "Your Age",           # label shown to user
    min_value=10,         # minimum allowed value
    max_value=100,        # maximum allowed value
    value=21              # default value
)

gender = st.sidebar.selectbox(
    "Your Gender",
    ["Female", "Male"]    # dropdown options
)

weight = st.sidebar.number_input(
    "Your Weight (kg)",
    min_value=30.0,
    max_value=200.0,
    value=60.0
)

height = st.sidebar.number_input(
    "Your Height (cm)",
    min_value=100.0,
    max_value=250.0,
    value=165.0
)

activity = st.sidebar.selectbox(
    "How Active Are You?",
    [
        "Sedentary (little/no exercise)",
        "Lightly active (1-3 days/week)",
        "Moderately active (3-5 days/week)",
        "Very active (6-7 days/week)",
        "Super active (athlete/physical job)"
    ]
)

goal = st.sidebar.selectbox(
    "Your Goal",
    [
        "Lose weight",
        "Maintain weight",
        "Gain muscle"
    ]
)

diet_type = st.sidebar.selectbox(
    "Your Diet Type",
    [
        "Non-vegetarian",
        "Vegetarian",
        "Vegan",
        "Eggetarian"
    ]
)

# Text box for allergies
allergies = st.sidebar.text_input(
    "Any allergies or foods to avoid?",
    placeholder="Example: nuts, dairy, gluten"
)

# Big green button at bottom of sidebar
generate = st.sidebar.button(
    "Generate My Diet Plan",
    type="primary"          # makes it green/highlighted
)

# ══════════════════════════════════════
# MAIN AREA - calculations shown always
# These update automatically when inputs change
# ══════════════════════════════════════

# Run all our math functions with the user's inputs
bmi, bmi_category          = calculate_bmi(weight, height)
tdee                       = calculate_calories(weight, height, age, gender, activity)
calorie_goal               = get_calorie_goal(tdee, goal)
protein_g, carbs_g, fat_g  = get_macros(calorie_goal, goal)

# Show 3 metric cards side by side
st.subheader("Your Daily Stats")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Your BMI",
        value=bmi,
        delta=bmi_category    # shown in small text below
    )

with col2:
    st.metric(
        label="Calories to Maintain",
        value=f"{tdee} kcal"
    )

with col3:
    st.metric(
        label="Your Daily Calorie Goal",
        value=f"{calorie_goal} kcal",
        delta=goal
    )

# Show macros in another row
st.subheader("Your Daily Macro Targets")
m1, m2, m3 = st.columns(3)

with m1:
    st.metric("Protein", f"{protein_g}g")
with m2:
    st.metric("Carbohydrates", f"{carbs_g}g")
with m3:
    st.metric("Fat", f"{fat_g}g")

# A horizontal line to separate sections
st.divider()

# ══════════════════════════════════════
# AI DIET PLAN SECTION
# Only runs when user clicks the button
# ══════════════════════════════════════

if generate:
    # Show a loading spinner while AI is thinking
    with st.spinner("AI is creating your diet plan... please wait!"):
        diet_plan = generate_diet_plan(
            age, gender, weight, height,
            goal, diet_type,
            allergies if allergies else "None",
            calorie_goal, protein_g, carbs_g, fat_g
        )

    # Show the diet plan
    st.subheader("Your Personalized Diet Plan")
    st.markdown(diet_plan)   # markdown makes it look nice
    st.divider()
    # Now generate grocery list from the diet plan
    with st.spinner("Creating your grocery list..."):
        grocery_list = generate_grocery_list(diet_plan)

    st.subheader("Your Weekly Grocery List")
    st.markdown(grocery_list)
    # Download button so user can save their plan
    st.divider()
    full_plan = f"MY DIET PLAN\n\n{diet_plan}\n\nMY GROCERY LIST\n\n{grocery_list}"
    st.download_button(
        label="Download My Plan as Text File",
        data=full_plan,
        file_name="my_diet_plan.txt",
        mime="text/plain"
    )
else:
    # Show this message before button is clicked
    st.info("Fill in your details on the left sidebar and click Generate My Diet Plan!")