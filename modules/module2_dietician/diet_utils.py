# diet_utils.py
# This file does all the MATH for our dietician app
# No AI here - just simple calculations!

# ══════════════════════════════════════
# WHAT IS BMI?
# BMI tells us if your weight is healthy
# Formula: weight divided by height squared
# ══════════════════════════════════════

def calculate_bmi(weight, height):
    # Step 1: convert height from cm to meters
    # Example: 165 cm becomes 1.65 m
    height_in_meters = height / 100

    # Step 2: apply the BMI formula
    # Example: 60 / (1.65 x 1.65) = 22.03
    bmi = weight / (height_in_meters * height_in_meters)

    # Step 3: round to 2 decimal places
    bmi = round(bmi, 2)

    # Step 4: find the category
    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal weight"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    # Send back both values
    return bmi, category
# ══════════════════════════════════════
# WHAT IS TDEE?
# TDEE = how many calories YOU need per day
# It depends on your body size AND how active you are
# ══════════════════════════════════════

def calculate_calories(weight, height, age, gender, activity):

    # Step 1: calculate BMR (calories just to stay alive)
    # BMR = what your body burns even if you sleep all day
    if gender == "Female":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5

    # Step 2: multiply by activity level
    # The more you move, the more calories you burn
    if activity == "Sedentary (little/no exercise)":
        tdee = bmr * 1.2
    elif activity == "Lightly active (1-3 days/week)":
        tdee = bmr * 1.375
    elif activity == "Moderately active (3-5 days/week)":
        tdee = bmr * 1.55
    elif activity == "Very active (6-7 days/week)":
        tdee = bmr * 1.725
    else:
        tdee = bmr * 1.9
    # Round to a whole number
    return round(tdee)


# ══════════════════════════════════════
# ADJUST CALORIES BASED ON GOAL
# Lose weight = eat less than you burn
# Gain muscle = eat more than you burn
# Maintain    = eat exactly what you burn
# ══════════════════════════════════════

def get_calorie_goal(tdee, goal):

    if goal == "Lose weight":
        # Eat 500 less per day = lose ~0.5 kg per week
        return tdee - 500

    elif goal == "Gain muscle":
        # Eat 300 more per day = enough energy to build muscle
        return tdee + 300

    else:
        # Maintain = no change needed
        return tdee

# ══════════════════════════════════════
# CALCULATE MACROS
# Macros = Protein, Carbs, Fat
# These 3 nutrients make up all your calories
# ══════════════════════════════════════

def get_macros(calorie_goal, goal):

    if goal == "Lose weight":
        # More protein = keeps you full + protects muscle
        protein_calories = calorie_goal * 0.40  # 40% protein
        carb_calories    = calorie_goal * 0.35  # 35% carbs
        fat_calories     = calorie_goal * 0.25  # 25% fat

    elif goal == "Gain muscle":
        # More carbs = fuel for heavy workouts
        protein_calories = calorie_goal * 0.35
        carb_calories    = calorie_goal * 0.45
        fat_calories     = calorie_goal * 0.20

    else:
        # Balanced split for maintaining
        protein_calories = calorie_goal * 0.30
        carb_calories    = calorie_goal * 0.40
        fat_calories     = calorie_goal * 0.30

    # Convert calories to GRAMS
    # 1g protein = 4 calories
    # 1g carbs   = 4 calories
    # 1g fat     = 9 calories
    protein_g = round(protein_calories / 4)
    carbs_g   = round(carb_calories / 4)
    fat_g     = round(fat_calories / 9)
    return protein_g, carbs_g, fat_g