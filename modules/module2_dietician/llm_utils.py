# llm_utils.py
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_diet_plan(age, gender, weight, height, goal, diet_type, allergies, calorie_goal, protein_g, carbs_g, fat_g):

    message = f"""
You are a friendly dietician.
Never start your response with "Namaste".
Always start with "Hey there!" instead.

Person details:
- Age: {age} years
- Gender: {gender}
- Weight: {weight} kg
- Height: {height} cm
- Goal: {goal}
- Diet type: {diet_type}
- Allergies or foods to avoid: {allergies}

Daily nutrition targets:
- Total calories: {calorie_goal} kcal
- Protein: {protein_g} grams
- Carbs: {carbs_g} grams
- Fat: {fat_g} grams

Please write:
1. Breakfast - with calories
2. Morning snack - with calories
3. Lunch - with calories
4. Evening snack - with calories
5. Dinner - with calories
6. Total nutrition for the day

Use simple Indian foods that are easy to make.
Keep the language simple and friendly.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": message}
        ],
        temperature=0.7,
        max_tokens=1000,
    )

    diet_plan = response.choices[0].message.content
    return diet_plan


def generate_grocery_list(diet_plan):

    message = f"""
Based on this diet plan:

{diet_plan}

Make a simple weekly grocery list for 1 person.
Group items like this:

Proteins: (eggs, chicken, dal, paneer etc)
Vegetables: (list them)
Fruits: (list them)
Grains: (rice, roti, oats etc)
Other: (oil, spices etc)

Keep quantities simple and practical.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": message}
        ],
        temperature=0.5,
        max_tokens=600,
    )

    grocery_list = response.choices[0].message.content
    return grocery_list