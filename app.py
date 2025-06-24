from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from dotenv import load_dotenv
from authlib.integrations.flask_client import OAuth
from urllib.parse import urlencode
import psycopg2
from psycopg2.extras import DictCursor
import json
from sample_data import SAMPLE_RECIPES
from sqlalchemy import text
import random
import cv2
import numpy as np
from PIL import Image
import io
import base64
from collections import defaultdict
from typing import List, Dict, Any
from collections import Counter
import google.generativeai as genai
from image_analyzer import analyze_food_image

# Load environment variables
load_dotenv('key.env')

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug = True  # Enable debug mode

# Initialize Gemini API
GEMINI_API_KEY = "AIzaSyD92SHG5VmVHdUiQAtHVtXnS7_z6mWDKq4"
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

# Initialize database
db = SQLAlchemy(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize OAuth
oauth = OAuth(app)

# Google OAuth setup
google = oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'},
)

# GitHub OAuth setup
github = oauth.register(
    name='github',
    client_id=os.getenv('GITHUB_CLIENT_ID'),
    client_secret=os.getenv('GITHUB_CLIENT_SECRET'),
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100))
    password_hash = db.Column(db.String(200))
    preferences = db.relationship('UserPreferences', backref='user', uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# User preferences model
class UserPreferences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    calorie_goal = db.Column(db.Integer, default=2000)
    protein_goal = db.Column(db.Integer, default=150)
    carbs_goal = db.Column(db.Integer, default=250)
    fat_goal = db.Column(db.Integer, default=65)
    budget = db.Column(db.String(20))
    preferred_cuisines = db.Column(db.JSON)
    taste_preferences = db.Column(db.JSON)
    dietary_restrictions = db.Column(db.JSON)

# Recipe model
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    meal_type = db.Column(db.String(20), nullable=False)  # breakfast, lunch, dinner, snack, drink
    cuisine = db.Column(db.String(50))
    calories = db.Column(db.Integer)
    protein = db.Column(db.Float)
    carbs = db.Column(db.Float)
    fat = db.Column(db.Float)
    prep_time = db.Column(db.Integer)  # in minutes
    cook_time = db.Column(db.Integer)  # in minutes
    servings = db.Column(db.Integer)
    difficulty = db.Column(db.String(20))  # easy, medium, hard
    ingredients = db.Column(db.JSON)  # List of ingredients with quantities
    instructions = db.Column(db.JSON)  # List of step-by-step instructions
    image_url = db.Column(db.String(200))
    tags = db.Column(db.JSON)  # List of tags like vegetarian, gluten-free, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'meal_type': self.meal_type,
            'cuisine': self.cuisine,
            'calories': self.calories,
            'protein': self.protein,
            'carbs': self.carbs,
            'fat': self.fat,
            'prep_time': self.prep_time,
            'cook_time': self.cook_time,
            'servings': self.servings,
            'difficulty': self.difficulty,
            'ingredients': self.ingredients,
            'instructions': self.instructions,
            'image_url': self.image_url,
            'tags': self.tags
        }

# ScannedIngredient model
class ScannedIngredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.String(50))
    unit = db.Column(db.String(20))
    category = db.Column(db.String(50))
    expiry_date = db.Column(db.DateTime)
    scanned_at = db.Column(db.DateTime, default=datetime.utcnow)
    image_url = db.Column(db.String(200))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create database tables and add sample data
def init_db():
    with app.app_context():
        try:
            # Create tables with new schema
            db.create_all()
            
            # Check if we already have sample recipes
            if Recipe.query.count() == 0:
                # Add sample recipes from external file
                for recipe_data in SAMPLE_RECIPES:
                    recipe = Recipe(**recipe_data)
                    db.session.add(recipe)
                db.session.commit()
                print("Database initialized with sample recipes!")
            else:
                print("Database already contains recipes, skipping initialization.")
                
        except Exception as e:
            print(f"Error initializing database: {str(e)}")
            raise

# Initialize the database when the app starts
init_db()

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        
        flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return redirect(url_for('register'))
        
        user = User(email=email, name=name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        return redirect(url_for('dashboard'))
    
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/update_macros', methods=['POST'])
@login_required
def update_macros():
    if not current_user.preferences:
        current_user.preferences = UserPreferences(user_id=current_user.id)
    
    current_user.preferences.calorie_goal = request.form.get('calories', type=int)
    current_user.preferences.protein_goal = request.form.get('protein', type=int)
    current_user.preferences.carbs_goal = request.form.get('carbs', type=int)
    current_user.preferences.fat_goal = request.form.get('fat', type=int)
    
    db.session.commit()
    flash('Macronutrient goals updated successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/update_preferences', methods=['POST'])
@login_required
def update_preferences():
    if not current_user.preferences:
        current_user.preferences = UserPreferences(user_id=current_user.id)
    
    current_user.preferences.budget = request.form.get('budget')
    current_user.preferences.preferred_cuisines = request.form.getlist('cuisines')
    current_user.preferences.taste_preferences = request.form.getlist('tastes')
    current_user.preferences.dietary_restrictions = request.form.getlist('restrictions')
    
    db.session.commit()
    flash('Preferences updated successfully!', 'success')
    return redirect(url_for('dashboard'))

# Recipe routes
@app.route('/recipes')
@login_required
def list_recipes():
    recipes = Recipe.query.all()
    return render_template('recipes.html', recipes=recipes)

@app.route('/recipes/<int:recipe_id>')
@login_required
def view_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('recipe_detail.html', recipe=recipe)

@app.route('/recipes/search')
@login_required
def search_recipes():
    query = request.args.get('q', '')
    meal_type = request.args.get('meal_type', '')
    cuisine_filter = request.args.get('cuisine', '')
    
    recipes = Recipe.query
    
    if query:
        recipes = recipes.filter(Recipe.name.ilike(f'%{query}%'))
    if meal_type:
        recipes = recipes.filter(Recipe.meal_type == meal_type)
    if cuisine_filter:
        recipes = recipes.filter(Recipe.cuisine == cuisine_filter)
    
    recipes = recipes.all()
    return render_template('recipes.html', recipes=recipes)

@app.route('/recipes/filter')
@login_required
def filter_recipes():
    calories_max = request.args.get('calories_max', type=int)
    protein_min = request.args.get('protein_min', type=float)
    prep_time_max = request.args.get('prep_time_max', type=int)
    difficulty = request.args.get('difficulty')
    meal_type = request.args.get('meal_type')
    tags = request.args.getlist('tags')
    
    recipes = Recipe.query
    
    if calories_max:
        recipes = recipes.filter(Recipe.calories <= calories_max)
    if protein_min:
        recipes = recipes.filter(Recipe.protein >= protein_min)
    if prep_time_max:
        recipes = recipes.filter(Recipe.prep_time <= prep_time_max)
    if difficulty:
        recipes = recipes.filter(Recipe.difficulty == difficulty)
    if meal_type:
        recipes = recipes.filter(Recipe.meal_type == meal_type)
    if tags:
        for tag in tags:
            recipes = recipes.filter(Recipe.tags.cast(db.JSON).contains([tag]))
    
    recipes = recipes.all()
    return render_template('recipes.html', recipes=recipes)

# OAuth routes
@app.route('/login/google')
def google_login():
    try:
        redirect_uri = url_for('google_authorize', _external=True)
        print(f"Google OAuth redirect URI: {redirect_uri}")  # Debug log
        return google.authorize_redirect(redirect_uri)
    except Exception as e:
        print(f"Google login error: {str(e)}")  # Debug log
        flash('Error connecting to Google. Please try again.', 'error')
        return redirect(url_for('login'))

@app.route('/login/google/authorize')
def google_authorize():
    try:
        token = google.authorize_access_token()
        resp = google.get('userinfo')
        user_info = resp.json()
        
        # Check if user exists
        user = User.query.filter_by(email=user_info['email']).first()
        if not user:
            # Create new user
            user = User(
                email=user_info['email'],
                name=user_info.get('name', user_info['email'].split('@')[0])
            )
            db.session.add(user)
            db.session.commit()
        
        login_user(user)
        return redirect(url_for('dashboard'))
    except Exception as e:
        print(f"Google authorize error: {str(e)}")  # Debug log
        flash('Error authenticating with Google. Please try again.', 'error')
        return redirect(url_for('login'))

@app.route('/login/github')
def github_login():
    try:
        redirect_uri = url_for('github_authorize', _external=True)
        print(f"GitHub OAuth redirect URI: {redirect_uri}")  # Debug log
        return github.authorize_redirect(redirect_uri)
    except Exception as e:
        print(f"GitHub login error: {str(e)}")  # Debug log
        flash('Error connecting to GitHub. Please try again.', 'error')
        return redirect(url_for('login'))

@app.route('/login/github/authorize')
def github_authorize():
    try:
        token = github.authorize_access_token()
        resp = github.get('user')
        user_info = resp.json()
        
        # Get primary email
        emails = github.get('user/emails').json()
        primary_email = next((email['email'] for email in emails if email['primary']), None)
        
        if not primary_email:
            flash('Could not get email from GitHub', 'error')
            return redirect(url_for('login'))
        
        # Check if user exists
        user = User.query.filter_by(email=primary_email).first()
        if not user:
            # Create new user
            user = User(
                email=primary_email,
                name=user_info.get('name', user_info['login'])
            )
            db.session.add(user)
            db.session.commit()
        
        login_user(user)
        return redirect(url_for('dashboard'))
    except Exception as e:
        print(f"GitHub authorize error: {str(e)}")  # Debug log
        flash('Error authenticating with GitHub. Please try again.', 'error')
        return redirect(url_for('login'))

@app.route('/recommendations')
@login_required
def recommendations():
    """Show recommended recipes based on user preferences and nutritional goals."""
    # Get query parameters
    meal_type = request.args.get('meal_type')
    calories = request.args.get('calories', type=int)
    protein = request.args.get('protein', type=float)
    carbs = request.args.get('carbs', type=float)
    fat = request.args.get('fat', type=float)
    cuisines = request.args.get('cuisines', '').split(',')
    tastes = request.args.get('tastes', '').split(',')
    restrictions = request.args.get('restrictions', '').split(',')
    budget = request.args.get('budget')

    # Start with all recipes
    recipes = Recipe.query

    # Filter by meal type
    if meal_type:
        recipes = recipes.filter(Recipe.meal_type == meal_type)

    # Filter by cuisine preferences
    if cuisines and cuisines[0]:
        recipes = recipes.filter(Recipe.cuisine.in_(cuisines))

    # Filter by dietary restrictions
    if restrictions and restrictions[0]:
        for restriction in restrictions:
            recipes = recipes.filter(Recipe.tags.cast(db.JSON).contains([restriction]))

    # Get all matching recipes
    matching_recipes = recipes.all()

    # Score each recipe based on nutritional goals and preferences
    scored_recipes = []
    for recipe in matching_recipes:
        score = 0

        # Score based on calorie match (within 20% of target)
        calorie_diff = abs(recipe.calories - calories)
        if calorie_diff <= calories * 0.2:  # Within 20% of target
            score += 100 - (calorie_diff / calories * 100)

        # Score based on protein match (within 20% of target)
        protein_diff = abs(recipe.protein - protein)
        if protein_diff <= protein * 0.2:
            score += 100 - (protein_diff / protein * 100)

        # Score based on carbs match (within 20% of target)
        carbs_diff = abs(recipe.carbs - carbs)
        if carbs_diff <= carbs * 0.2:
            score += 100 - (carbs_diff / carbs * 100)

        # Score based on fat match (within 20% of target)
        fat_diff = abs(recipe.fat - fat)
        if fat_diff <= fat * 0.2:
            score += 100 - (fat_diff / fat * 100)

        # Add bonus points for matching taste preferences
        if tastes and tastes[0]:
            for taste in tastes:
                if taste in recipe.tags:
                    score += 25

        # Add bonus points for matching budget
        if budget:
            recipe_budget = recipe.tags.get('budget', 'moderate')
            if recipe_budget == budget:
                score += 50

        scored_recipes.append((recipe, score))

    # Sort by score and get top 6 recipes
    scored_recipes.sort(key=lambda x: x[1], reverse=True)
    top_recipes = [recipe.to_dict() for recipe, _ in scored_recipes[:1]]

    return jsonify(top_recipes)

@app.route('/compare_preferences', methods=['POST'])
def compare_preferences():
    user_preferences = request.get_json()
    
    # Score each recipe based on how well it matches user preferences
    scored_recipes = []
    for recipe in SAMPLE_RECIPES:
        score = 0
        total_criteria = 0
        
        # Compare nutritional values (40% of total score)
        if abs(recipe['calories'] - user_preferences['calories']) <= 200:
            score += 0.4
        if abs(recipe['protein'] - user_preferences['protein']) <= 10:
            score += 0.4
        if abs(recipe['carbs'] - user_preferences['carbs']) <= 20:
            score += 0.4
        if abs(recipe['fat'] - user_preferences['fat']) <= 5:
            score += 0.4
        total_criteria += 1.6
        
        # Compare meal type (20% of total score)
        if recipe['meal_type'] in user_preferences['meal_types']:
            score += 0.2
        total_criteria += 0.2
        
        # Compare cuisine (20% of total score)
        if recipe['cuisine'].lower() in [c.lower() for c in user_preferences['cuisine_preferences']]:
            score += 0.2
        total_criteria += 0.2
        
        # Compare dietary preferences (20% of total score)
        dietary_matches = sum(1 for tag in recipe['tags'] if tag in user_preferences['dietary_preferences'])
        if dietary_matches > 0:
            score += 0.2
        total_criteria += 0.2
        
        # Calculate final match score
        match_score = score / total_criteria
        
        # Add recipe with match score
        recipe_with_score = recipe.copy()
        recipe_with_score['match_score'] = match_score
        scored_recipes.append(recipe_with_score)
    
    # Sort recipes by match score
    scored_recipes.sort(key=lambda x: x['match_score'], reverse=True)
    
    # Return top 3 matches
    return jsonify({
        'matched_recipes': scored_recipes[:3]
    })

@app.route('/generate_meal_plan', methods=['POST'])
def generate_meal_plan():
    """Generate a custom recipe using Gemini API based on user preferences and available ingredients."""
    try:
        # Get and log the raw request data
        print("\n=== Received Request Data ===")
        print(f"Request Method: {request.method}")
        print(f"Content Type: {request.content_type}")
        print(f"Raw Data: {request.get_data()}")
        
        # Parse JSON data from request
        user_preferences = request.get_json()
        print("\n=== Parsed User Preferences ===")
        print(f"User Preferences: {json.dumps(user_preferences, indent=2)}")
        
        if not user_preferences:
            print("Error: No user preferences received")
            return jsonify({
                'error': 'No user preferences received',
                'details': 'Please provide your preferences'
            }), 400

        # Validate required fields
        required_fields = ['calories', 'protein', 'carbs', 'fat', 'meal_type']
        missing_fields = [field for field in required_fields if field not in user_preferences]
        
        if missing_fields:
            print(f"Error: Missing required fields: {missing_fields}")
            return jsonify({
                'error': 'Missing required fields',
                'details': f'Please provide values for: {", ".join(missing_fields)}'
            }), 400

        # Get available ingredients from the request. This is now a mandatory field.
        available_ingredients = user_preferences.get('available_ingredients', [])

        # Strict check: If no ingredients were scanned and passed, do not proceed.
        if not available_ingredients:
            print("Error: No scanned ingredients provided.")
            return jsonify({
                'error': 'No ingredients provided',
                'details': 'Please scan your food before generating a meal plan.'
            }), 400

        print(f"Using ONLY scanned ingredients for recipe generation: {available_ingredients}")

        # Create prompt for Gemini API
        prompt = create_recipe_prompt(user_preferences, available_ingredients)
        
        print("\n=== Sending to Gemini API ===")
        print(f"Prompt: {prompt}")
        
        # Generate recipe using Gemini API
        response = gemini_model.generate_content(prompt)
        
        if not response or not response.text:
            raise Exception("No response from Gemini API")
        
        print(f"\n=== Gemini API Response ===")
        print(response.text)
        
        # Parse the response to extract recipe data
        recipe_data = parse_recipe_response(response.text)
        
        if not recipe_data:
            raise Exception("Failed to parse recipe from Gemini API response")
        
        # Add user goals to response
        response_data = {
            'recipe': recipe_data,
            'user_goals': {
                'calories': user_preferences['calories'],
                'protein': user_preferences['protein'],
                'carbs': user_preferences['carbs'],
                'fat': user_preferences['fat']
            }
        }
        
        print("\n=== Sending Response ===")
        print(json.dumps(response_data, indent=2))
        
        return jsonify(response_data)
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"\n=== Error Generating Meal Plan ===")
        print(f"Error: {str(e)}")
        print(f"Error details:\n{error_details}")
        return jsonify({
            'error': 'Failed to generate meal recommendation',
            'details': str(e),
            'traceback': error_details
        }), 500

def create_recipe_prompt(user_preferences: Dict[str, Any], available_ingredients: List[str]) -> str:
    """Create a detailed prompt for the Gemini API to generate a custom recipe."""
    
    meal_type = user_preferences['meal_type']
    calories = user_preferences['calories']
    protein = user_preferences['protein']
    carbs = user_preferences['carbs']
    fat = user_preferences['fat']
    
    # Build dietary restrictions text
    dietary_restrictions = user_preferences.get('dietary_restrictions', [])
    dietary_text = ""
    if dietary_restrictions and 'anything' not in dietary_restrictions:
        dietary_text = f"Dietary restrictions: {', '.join(dietary_restrictions)}. "
    
    # Build cuisine preferences text
    preferred_cuisines = user_preferences.get('preferred_cuisines', [])
    cuisine_text = ""
    if preferred_cuisines:
        cuisine_text = f"Preferred cuisines: {', '.join(preferred_cuisines)}. "
    
    # Build taste preferences text
    taste_preferences = user_preferences.get('taste_preferences', [])
    taste_text = ""
    if taste_preferences:
        taste_text = f"Taste preferences: {', '.join(taste_preferences)}. "
    
    # Build cooking constraints text
    cooking_time = user_preferences.get('cooking_time', '30')
    difficulty = user_preferences.get('difficulty', 'medium')
    cooking_text = f"Cooking time: {cooking_time} minutes. Difficulty level: {difficulty}. "
    
    prompt = f"""
You are a professional chef and nutritionist. Create a custom recipe for a {meal_type} meal that meets the following requirements:

NUTRITIONAL TARGETS:
- Calories: {calories} kcal
- Protein: {protein}g
- Carbohydrates: {carbs}g
- Fat: {fat}g

{dietary_text}{cuisine_text}{taste_text}{cooking_text}

AVAILABLE INGREDIENTS:
{', '.join(available_ingredients)}

INSTRUCTIONS:
1. Create a recipe that uses primarily the available ingredients listed above
2. You may suggest 2-3 additional common ingredients if needed for the recipe
3. Ensure the recipe meets the nutritional targets as closely as possible
4. Make the recipe appropriate for the specified meal type
5. Consider the dietary restrictions, cuisine preferences, and taste preferences
6. Keep the cooking time and difficulty level appropriate

RESPONSE FORMAT:
Return ONLY a valid JSON object with the following structure (no additional text):

{{
    "name": "Recipe Name",
    "meal_type": "{meal_type}",
    "cuisine": "Cuisine Type",
    "calories": {calories},
    "protein": {protein},
    "carbs": {carbs},
    "fat": {fat},
    "prep_time": 15,
    "cook_time": 20,
    "servings": 1,
    "difficulty": "{difficulty}",
    "ingredients": [
        {{"name": "ingredient name", "amount": "quantity with unit"}}
    ],
    "instructions": [
        "Step 1 instruction",
        "Step 2 instruction",
        "Step 3 instruction"
    ],
    "tags": ["tag1", "tag2", "tag3"]
}}

IMPORTANT: Return ONLY the JSON object, no additional text or explanations.
"""
    
    return prompt

def parse_recipe_response(response_text: str) -> Dict[str, Any]:
    """Parse the Gemini API response to extract recipe data."""
    try:
        # Clean the response text
        cleaned_text = response_text.strip()
        
        # Remove any markdown formatting if present
        if cleaned_text.startswith('```json'):
            cleaned_text = cleaned_text[7:]
        if cleaned_text.endswith('```'):
            cleaned_text = cleaned_text[:-3]
        
        cleaned_text = cleaned_text.strip()
        
        # Parse JSON
        recipe_data = json.loads(cleaned_text)
        
        # Validate required fields
        required_fields = ['name', 'meal_type', 'calories', 'protein', 'carbs', 'fat', 'ingredients', 'instructions']
        for field in required_fields:
            if field not in recipe_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Ensure ingredients and instructions are lists
        if not isinstance(recipe_data['ingredients'], list):
            recipe_data['ingredients'] = []
        if not isinstance(recipe_data['instructions'], list):
            recipe_data['instructions'] = []
        
        # Set default values for optional fields
        recipe_data.setdefault('cuisine', 'International')
        recipe_data.setdefault('prep_time', 15)
        recipe_data.setdefault('cook_time', 20)
        recipe_data.setdefault('servings', 1)
        recipe_data.setdefault('difficulty', 'medium')
        recipe_data.setdefault('tags', [])
        
        return recipe_data
        
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Response text: {response_text}")
        return None
    except Exception as e:
        print(f"Error parsing recipe response: {e}")
        return None

@app.route('/meal_plan_results')
def meal_plan_results():
    """Display the generated meal plan results."""
    return render_template('meal_plan_results.html')

# Camera routes
@app.route('/scan')
@login_required
def scan_page():
    """Render the camera scanning page."""
    return render_template('scan.html')

@app.route('/scan/process', methods=['POST'])
def process_scan():
    """Process the scanned image and return detected ingredients."""
    print("\n=== Processing Scan ===")
    try:
        # Ensure request is JSON
        if not request.is_json:
            print("Request is not JSON")
            return jsonify({
                'success': False,
                'error': 'Invalid request format',
                'details': 'Request must be JSON'
            }), 400

        data = request.get_json()
        print("Received JSON data")

        # Validate image data
        if not data or 'image' not in data:
            print("No image data in request")
            return jsonify({
                'success': False,
                'error': 'Missing image data',
                'details': 'No image data provided in request'
            }), 400

        # Process the image
        print("Processing image...")
        ingredients = analyze_food_image(data['image'])
        
        if not ingredients:
            print("No ingredients detected")
            return jsonify({
                'success': False,
                'error': 'No ingredients detected',
                'details': 'Please try taking a clearer picture with better lighting'
            }), 200

        print(f"Successfully detected {len(ingredients)} ingredients")
        return jsonify({
            'success': True,
            'ingredients': ingredients
        }), 200

    except Exception as e:
        print(f"Error processing scan: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': 'Failed to process image',
            'details': str(e)
        }), 500

@app.route('/scan/ingredients')
@login_required
def get_scanned_ingredients():
    """Get all scanned ingredients for the current user."""
    ingredients = ScannedIngredient.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': ing.id,
        'name': ing.name,
        'quantity': ing.quantity,
        'unit': ing.unit,
        'category': ing.category,
        'expiry_date': ing.expiry_date.isoformat() if ing.expiry_date else None,
        'scanned_at': ing.scanned_at.isoformat()
    } for ing in ingredients])

@app.route('/scan/recipes', methods=['GET', 'POST'])
@login_required
def get_recipes_from_ingredients():
    """Get recipe recommendations based on scanned or manual ingredients using Gemini API."""
    try:
        ingredient_names = []
        
        if request.method == 'POST':
            # Handle manual ingredients from POST request
            data = request.get_json()
            if data and 'ingredients' in data:
                manual_ingredients = data['ingredients']
                ingredient_names = [ing.get('name', '') for ing in manual_ingredients if ing.get('name')]
            else:
                return jsonify({
                    'recipes': [],
                    'available_ingredients': [],
                    'error': 'No ingredients provided in request'
                }), 400
        else:
            # Handle scanned ingredients from GET request
            user_ingredients = ScannedIngredient.query.filter_by(user_id=current_user.id).all()
            ingredient_names = [ing.name for ing in user_ingredients]
        
        if not ingredient_names:
            return jsonify({
                'recipes': [],
                'available_ingredients': [],
                'message': 'No ingredients available. Please scan or add some ingredients first.'
            })
        
        # Create prompt for Gemini API
        prompt = f"""
You are a professional chef. Create 3 different recipe suggestions based on the following available ingredients:

AVAILABLE INGREDIENTS:
{', '.join(ingredient_names)}

INSTRUCTIONS:
1. Create 3 diverse recipes that use primarily the available ingredients
2. You may suggest 2-3 additional common pantry ingredients per recipe if needed
3. Make the recipes suitable for different meal types (breakfast, lunch, dinner)
4. Ensure the recipes are practical and easy to follow
5. Include nutritional information for each recipe

RESPONSE FORMAT:
Return ONLY a valid JSON array with 3 recipe objects (no additional text):

[
    {{
        "name": "Recipe Name 1",
        "meal_type": "breakfast/lunch/dinner",
        "cuisine": "Cuisine Type",
        "calories": 400,
        "protein": 25,
        "carbs": 45,
        "fat": 15,
        "prep_time": 15,
        "cook_time": 20,
        "servings": 1,
        "difficulty": "easy/medium/hard",
        "ingredients": [
            {{"name": "ingredient name", "amount": "quantity with unit"}}
        ],
        "instructions": [
            "Step 1 instruction",
            "Step 2 instruction",
            "Step 3 instruction"
        ],
        "tags": ["tag1", "tag2"]
    }},
    {{
        "name": "Recipe Name 2",
        "meal_type": "breakfast/lunch/dinner",
        "cuisine": "Cuisine Type",
        "calories": 500,
        "protein": 30,
        "carbs": 50,
        "fat": 20,
        "prep_time": 20,
        "cook_time": 25,
        "servings": 1,
        "difficulty": "easy/medium/hard",
        "ingredients": [
            {{"name": "ingredient name", "amount": "quantity with unit"}}
        ],
        "instructions": [
            "Step 1 instruction",
            "Step 2 instruction",
            "Step 3 instruction"
        ],
        "tags": ["tag1", "tag2"]
    }},
    {{
        "name": "Recipe Name 3",
        "meal_type": "breakfast/lunch/dinner",
        "cuisine": "Cuisine Type",
        "calories": 450,
        "protein": 28,
        "carbs": 48,
        "fat": 18,
        "prep_time": 18,
        "cook_time": 22,
        "servings": 1,
        "difficulty": "easy/medium/hard",
        "ingredients": [
            {{"name": "ingredient name", "amount": "quantity with unit"}}
        ],
        "instructions": [
            "Step 1 instruction",
            "Step 2 instruction",
            "Step 3 instruction"
        ],
        "tags": ["tag1", "tag2"]
    }}
]

IMPORTANT: Return ONLY the JSON array, no additional text or explanations.
"""
        
        # Generate recipes using Gemini API
        response = gemini_model.generate_content(prompt)
        
        if not response or not response.text:
            raise Exception("No response from Gemini API")
        
        # Parse the response to extract recipe data
        recipes_data = parse_recipes_response(response.text)
        
        if not recipes_data:
            raise Exception("Failed to parse recipes from Gemini API response")
        
        return jsonify({
            'recipes': recipes_data,
            'available_ingredients': ingredient_names
        })
        
    except Exception as e:
        print(f"Error generating recipes from ingredients: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return jsonify({
            'recipes': [],
            'available_ingredients': ingredient_names if 'ingredient_names' in locals() else [],
            'error': 'Failed to generate recipes',
            'details': str(e)
        }), 500

def parse_recipes_response(response_text: str) -> List[Dict[str, Any]]:
    """Parse the Gemini API response to extract multiple recipe data."""
    try:
        # Clean the response text
        cleaned_text = response_text.strip()
        
        # Remove any markdown formatting if present
        if cleaned_text.startswith('```json'):
            cleaned_text = cleaned_text[7:]
        if cleaned_text.endswith('```'):
            cleaned_text = cleaned_text[:-3]
        
        cleaned_text = cleaned_text.strip()
        
        # Parse JSON
        recipes_data = json.loads(cleaned_text)
        
        # Ensure it's a list
        if not isinstance(recipes_data, list):
            recipes_data = [recipes_data]
        
        # Validate and clean each recipe
        cleaned_recipes = []
        for recipe in recipes_data:
            if not isinstance(recipe, dict):
                continue
                
            # Validate required fields
            required_fields = ['name', 'meal_type', 'calories', 'protein', 'carbs', 'fat', 'ingredients', 'instructions']
            if all(field in recipe for field in required_fields):
                # Ensure ingredients and instructions are lists
                if not isinstance(recipe['ingredients'], list):
                    recipe['ingredients'] = []
                if not isinstance(recipe['instructions'], list):
                    recipe['instructions'] = []
                
                # Set default values for optional fields
                recipe.setdefault('cuisine', 'International')
                recipe.setdefault('prep_time', 15)
                recipe.setdefault('cook_time', 20)
                recipe.setdefault('servings', 1)
                recipe.setdefault('difficulty', 'medium')
                recipe.setdefault('tags', [])
                
                cleaned_recipes.append(recipe)
        
        return cleaned_recipes
        
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Response text: {response_text}")
        return []
    except Exception as e:
        print(f"Error parsing recipes response: {e}")
        return []

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 
