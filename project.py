import streamlit as st
import google.generativeai as genai
import pandas as pd
import matplotlib.pyplot as plt

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="AI Fitness Assistant", layout="wide", page_icon="💪")
st.title("🏋️‍♂️ AI Fitness & Diet Assistant")

# --- 2. AUTHENTICATION ---
API_KEY = "AIzaSyC4kNFbAK-etaTLWKikvE4NG6OU4TRSGvM"  # Replace with your actual key

def get_working_model(api_key):
    """Dynamically finds a working model to avoid 404 errors."""
    try:
        genai.configure(api_key=api_key, transport='rest')
        available_models = [m.name for m in genai.list_models() 
                           if 'generateContent' in m.supported_generation_methods]
        priority = ["models/gemini-1.5-flash", "models/gemini-1.5-pro", "models/gemini-pro"]
        for p in priority:
            if p in available_models:
                return p
        return available_models[0] if available_models else None
    except Exception as e:
        st.error(f"Failed to fetch models: {e}")
        return None

# --- 3. SIDEBAR ---
with st.sidebar:
    st.header("📋 User Profile")
    weight = st.number_input("Weight (kg)", value=75.0)
    height = st.number_input("Height (cm)", value=170.0)
    age = st.number_input("Age", value=25)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    activity = st.selectbox("Activity", ["sedentary", "lightly active", "moderately active", "very active"])
    goal = st.radio("Goal", ["Weight Loss", "Weight Gain"])
    diet_pref = st.selectbox("Diet", ["Non-Vegetarian", "Vegetarian", "Vegan"])
    medical = st.text_input("Medical/Allergies", "None")
    
    submit_button = st.button("Generate Plan")

# --- 4. GENERATION ---
if submit_button:
    if API_KEY == "YOUR_API_KEY_HERE":
        st.error("Please paste your API key in the code.")
    else:
        with st.spinner("Finding active AI model..."):
            working_model_name = get_working_model(API_KEY)
        
        if working_model_name:
            with st.status(f"🚀 Using {working_model_name}...") as status:
                model = genai.GenerativeModel(model_name=working_model_name)
                
                prompt = f"""
                Act as an Expert Fitness Trainer. 
                User: {gender}, {age}yrs, {weight}kg, {height}cm.
                Goal: {goal}. Diet: {diet_pref}. Activity: {activity}.
                
                Provide output in this format:
                1. Quick calculations (BMI, BMR, TDEE, Macros).
                2. Exercise Plans (bullet points):
                   - 🟢 Beginner
                   - 🟡 Intermediate
                   - 🔴 Advanced
                3. Diet Schedule (Markdown table):
                   - Breakfast, Lunch, Dinner, Snacks
                   - Tailored to {diet_pref} and {goal}
                4. Safety Tips (short bullet points).
                
                Keep everything concise, structured, and easy to read.
                Also provide the numeric values of BMI, BMR, TDEE, and Macros clearly so they can be plotted.
                """
                
                try:
                    response = model.generate_content(prompt)
                    status.update(label="✅ Success!", state="complete")
                    st.markdown(response.text)

                    # --- 5. Add Attractive Images ---
                    st.subheader("🔥 Motivation & Inspiration")
                    st.image("https://images.unsplash.com/photo-1599058917212-d750089bc07d", 
                             caption="Strength Training", use_column_width=True)
                    st.image("https://images.unsplash.com/photo-1605296867304-46d5465a13f1", 
                             caption="Healthy Diet", use_column_width=True)
                    st.image("https://images.unsplash.com/photo-1594737625785-c0f3f0b3fc1d", 
                             caption="Yoga & Flexibility", use_column_width=True)

                except Exception as e:
                    status.update(label="❌ Generation Failed", state="error")
                    st.error(f"Error: {e}")
        else:
            st.error("Could not find a valid Gemini model for this API key.")

# --- 6. Q&A Section ---
st.header("❓ Ask the AI Assistant")
user_question = st.text_input("Type your question about fitness/diet here:")
if user_question:
    try:
        model = genai.GenerativeModel(model_name=get_working_model(API_KEY))
        q_response = model.generate_content(f"Answer concisely: {user_question}")
        st.markdown(q_response.text)
    except Exception as e:
        st.error(f"Error answering question: {e}")
