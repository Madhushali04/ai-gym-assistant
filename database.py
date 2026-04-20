# database.py
# This file handles all MongoDB connections
# We save diet plans, workouts and chat history here!

import os
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

# Load .env file to get MONGO_URI
load_dotenv()

# ══════════════════════════════════════
# CONNECT TO MONGODB
# ══════════════════════════════════════

def get_database():
    # Read connection string from .env file
    uri = os.getenv("MONGO_URI")

    # Connect to MongoDB Atlas
    client = MongoClient(uri)

    # Our database name
    db = client["ai_gym_assistant"]

    return db


# ══════════════════════════════════════
# DIET PLAN FUNCTIONS
# ══════════════════════════════════════

def save_diet_plan(age, gender, weight, height, goal, diet_type, calorie_goal, diet_plan, grocery_list):
    db = get_database()

    # diet_plans is our collection (like a table)
    collection = db["diet_plans"]

    # Document to save
    document = {
        "timestamp":    datetime.now(),
        "age":          age,
        "gender":       gender,
        "weight":       weight,
        "height":       height,
        "goal":         goal,
        "diet_type":    diet_type,
        "calorie_goal": calorie_goal,
        "diet_plan":    diet_plan,
        "grocery_list": grocery_list
    }

    # Save to MongoDB
    result = collection.insert_one(document)
    return str(result.inserted_id)


def get_recent_diet_plans(limit=5):
    db = get_database()
    collection = db["diet_plans"]

    # Get newest plans first
    plans = list(collection.find().sort("timestamp", -1).limit(limit))

    # Convert ObjectId to string
    for plan in plans:
        plan["_id"] = str(plan["_id"])

    return plans


# ══════════════════════════════════════
# WORKOUT HISTORY FUNCTIONS
# ══════════════════════════════════════

def save_workout(exercise, reps):
    db = get_database()
    collection = db["workout_history"]

    document = {
        "timestamp": datetime.now(),
        "exercise":  exercise,
        "reps":      reps
    }

    result = collection.insert_one(document)
    return str(result.inserted_id)


def get_workout_history(limit=10):
    db = get_database()
    collection = db["workout_history"]

    history = list(collection.find().sort("timestamp", -1).limit(limit))

    for item in history:
        item["_id"] = str(item["_id"])

    return history


# ══════════════════════════════════════
# CHAT HISTORY FUNCTIONS
# ══════════════════════════════════════

def save_chat_message(role, content, mood=None):
    db = get_database()
    collection = db["chat_history"]

    document = {
        "timestamp": datetime.now(),
        "role":      role,
        "content":   content,
        "mood":      mood
    }

    result = collection.insert_one(document)
    return str(result.inserted_id)


def get_chat_history(limit=20):
    db = get_database()
    collection = db["chat_history"]

    history = list(collection.find().sort("timestamp", -1).limit(limit))

    for item in history:
        item["_id"] = str(item["_id"])

    return history


# ══════════════════════════════════════
# TEST CONNECTION
# Run this file directly to test
# ══════════════════════════════════════

if __name__ == "__main__":
    try:
        db = get_database()
        print("MongoDB connected successfully!")
        print(f"Database: {db.name}")
        print(f"Collections: {db.list_collection_names()}")
    except Exception as e:
        print(f"Connection failed: {e}")