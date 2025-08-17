from flask import Flask, render_template, request, jsonify
import random
import pandas as pd
import os
import PyPDF2
from docx import Document
from werkzeug.utils import secure_filename
import tempfile
import requests
import json

app = Flask(__name__)

# Configuration for file uploads
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max file size
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

# Medical Certificate Processing Functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_file(file):
    """Extract text from uploaded file based on its type."""
    try:
        filename = secure_filename(file.filename)
        file_extension = filename.rsplit('.', 1)[1].lower()
        
        if file_extension == 'pdf':
            return extract_text_from_pdf(file)
        elif file_extension == 'docx':
            return extract_text_from_docx(file)
        elif file_extension == 'txt':
            return file.read().decode('utf-8')
        else:
            return None
    except Exception as e:
        print(f"Error extracting text: {str(e)}")
        return None

def extract_text_from_pdf(file):
    """Extract text from PDF file."""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        print(f"Error reading PDF: {str(e)}")
        return None

def extract_text_from_docx(file):
    """Extract text from DOCX file."""
    try:
        doc = Document(file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        print(f"Error reading DOCX: {str(e)}")
        return None

def detect_health_conditions(text):
    """Detect health conditions from extracted text."""
    if not text:
        return []
    
    text_lower = text.lower()
    detected_conditions = []
    
    # Medical condition keywords mapping
    conditions = {
        "diabetes": "Diabetes",
        "diabetic": "Diabetes",
        "blood sugar": "Diabetes",
        "glucose": "Diabetes",
        "high blood pressure": "High Blood Pressure",
        "hypertension": "High Blood Pressure",
        "bp": "High Blood Pressure",
        "heart disease": "Heart Disease",
        "cardiac": "Heart Disease",
        "coronary": "Heart Disease",
        "asthma": "Asthma",
        "respiratory": "Respiratory Issues",
        "cancer": "Cancer",
        "tumor": "Cancer",
        "malignant": "Cancer",
        "kidney disease": "Kidney Disease",
        "renal": "Kidney Disease",
        "lung disease": "Lung Disease",
        "pulmonary": "Lung Disease",
        "arthritis": "Arthritis",
        "thyroid": "Thyroid Disorder",
        "cholesterol": "High Cholesterol",
        "migraine": "Migraine",
        "depression": "Depression",
        "anxiety": "Anxiety"
    }
    
    # Check for each condition
    for keyword, condition in conditions.items():
        if keyword in text_lower and condition not in detected_conditions:
            detected_conditions.append(condition)
    
    return detected_conditions


# Rule-based fitness chatbot for Vercel compatibility
def chat_with_fitness_ai(message, context=""):
    """
    Rule-based fitness AI response system that works in Vercel
    """
    message_lower = message.lower()
    
    # Fitness advice patterns
    if any(word in message_lower for word in ['workout', 'exercise', 'training']):
        if 'beginner' in message_lower:
            return "For beginners, start with 20-30 minutes of cardio 3 times a week. Focus on form over intensity. Try walking, cycling, or swimming to build endurance safely."
        elif 'strength' in message_lower:
            return "Start with bodyweight exercises: push-ups, squats, lunges, and planks. Do 2-3 sets of 10-15 reps. Rest 1-2 minutes between sets."
        else:
            return "A good workout routine includes: 1) 5-10 min warm-up, 2) 20-40 min main exercise, 3) 5-10 min cool-down. Aim for 150 minutes of moderate activity weekly."
    
    elif any(word in message_lower for word in ['diet', 'nutrition', 'food', 'eat']):
        if 'weight loss' in message_lower:
            return "For weight loss: Create a 500-calorie daily deficit, eat protein-rich foods, include vegetables, and stay hydrated. Track your meals and be consistent."
        elif 'muscle' in message_lower:
            return "For muscle building: Eat 1.6-2.2g protein per kg body weight daily. Include complex carbs, healthy fats, and eat in a slight calorie surplus."
        else:
            return "A balanced diet includes: lean proteins, whole grains, fruits, vegetables, and healthy fats. Stay hydrated with 8-10 glasses of water daily."
    
    elif any(word in message_lower for word in ['motivation', 'motivated', 'tired']):
        return "Remember why you started! Set small, achievable goals. Celebrate progress, not perfection. Find a workout buddy or join a fitness community for support."
    
    elif any(word in message_lower for word in ['injury', 'pain', 'hurt']):
        return "If you're experiencing pain, stop exercising immediately. Rest, ice, compress, and elevate (RICE). Consult a healthcare professional for persistent pain."
    
    elif any(word in message_lower for word in ['goal', 'target', 'aim']):
        return "Set SMART goals: Specific, Measurable, Achievable, Relevant, and Time-bound. Break big goals into smaller milestones. Track your progress regularly."
    
    elif any(word in message_lower for word in ['form', 'technique', 'proper']):
        return "Proper form is crucial! Start with lighter weights, focus on controlled movements, and consider working with a certified trainer. Quality over quantity always."
    
    elif any(word in message_lower for word in ['rest', 'recovery', 'sleep']):
        return "Rest days are essential! Aim for 7-9 hours of sleep, take 1-2 rest days per week, and listen to your body. Recovery is when your body gets stronger."
    
    elif any(word in message_lower for word in ['cardio', 'aerobic', 'endurance']):
        return "Cardio improves heart health and burns calories. Start with 20-30 minutes of moderate activity like brisk walking, cycling, or swimming. Gradually increase duration and intensity."
    
    elif any(word in message_lower for word in ['hiit', 'interval', 'intense']):
        return "HIIT workouts are great for burning fat and improving fitness. Try 30 seconds of high-intensity exercise followed by 30 seconds of rest. Repeat for 10-20 minutes."
    
    else:
        return "I'm FitAI, your fitness coach! I can help with workout routines, nutrition advice, motivation, injury prevention, and fitness goals. What specific fitness topic would you like to discuss?"

def get_fitness_context(user_data=None):
    """
    Generate context based on user's fitness data
    """
    if user_data:
        return f"User context: Weight: {user_data.get('weight', 'N/A')}kg, Height: {user_data.get('height', 'N/A')}cm, Goal: {user_data.get('goal', 'general fitness')}"
    return ""
