import base64
import os
from io import BytesIO
from collections import defaultdict
from typing import List, Dict, Any
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from clarifai.client.model import Model
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv('key.env')

# Initialize Gemini for additional analysis
GEMINI_API_KEY = "AIzaSyD92SHG5VmVHdUiQAtHVtXnS7_z6mWDKq4"
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

def preprocess_image(image: Image.Image) -> List[Image.Image]:
    """Apply multiple preprocessing techniques to improve detection accuracy."""
    processed_images = []
    
    # Original image
    processed_images.append(image)
    
    # Enhanced contrast
    enhancer = ImageEnhance.Contrast(image)
    enhanced = enhancer.enhance(1.5)
    processed_images.append(enhanced)
    
    # Enhanced brightness
    enhancer = ImageEnhance.Brightness(image)
    brightened = enhancer.enhance(1.2)
    processed_images.append(brightened)
    
    # Sharpened
    sharpened = image.filter(ImageFilter.SHARPEN)
    processed_images.append(sharpened)
    
    # Convert to different color spaces for better detection
    # Convert PIL to OpenCV format
    cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    lab = cv2.cvtColor(cv_image, cv2.COLOR_BGR2LAB)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    lab[:,:,0] = clahe.apply(lab[:,:,0])
    enhanced_cv = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    enhanced_pil = Image.fromarray(cv2.cvtColor(enhanced_cv, cv2.COLOR_BGR2RGB))
    processed_images.append(enhanced_pil)
    
    return processed_images

def determine_food_category(ingredient_name: str) -> str:
    """Enhanced food category determination with more comprehensive ingredient lists."""
    ingredient_lower = ingredient_name.lower()
    
    # Expanded ingredient categories
    fruits = ['apple', 'banana', 'orange', 'grape', 'strawberry', 'blueberry', 'raspberry', 
              'blackberry', 'pineapple', 'mango', 'peach', 'pear', 'plum', 'cherry', 'lemon', 'lime',
              'kiwi', 'avocado', 'coconut', 'pomegranate', 'fig', 'date', 'raisin', 'cranberry',
              'apricot', 'nectarine', 'tangerine', 'clementine', 'mandarin', 'grapefruit']
    
    vegetables = ['carrot', 'broccoli', 'spinach', 'lettuce', 'tomato', 'onion', 'garlic', 
                  'potato', 'sweet potato', 'corn', 'pepper', 'bell pepper', 'cucumber', 
                  'zucchini', 'eggplant', 'mushroom', 'cauliflower', 'cabbage', 'kale',
                  'celery', 'radish', 'beet', 'turnip', 'parsnip', 'rutabaga', 'jicama',
                  'artichoke', 'asparagus', 'brussels sprout', 'bok choy', 'chard', 'collard',
                  'arugula', 'watercress', 'endive', 'escarole', 'frisée', 'mizuna']
    
    meats = ['chicken', 'beef', 'pork', 'lamb', 'turkey', 'duck', 'fish', 'salmon', 'tuna', 
             'shrimp', 'bacon', 'sausage', 'ham', 'steak', 'burger', 'meatball', 'sirloin',
             'ribeye', 'tenderloin', 'brisket', 'chuck', 'flank', 'skirt', 'tri-tip',
             'cod', 'halibut', 'mackerel', 'sardine', 'anchovy', 'tilapia', 'catfish',
             'lobster', 'crab', 'clam', 'mussel', 'oyster', 'scallop', 'squid', 'octopus']
    
    dairy = ['milk', 'cheese', 'yogurt', 'butter', 'cream', 'sour cream', 'cottage cheese', 
             'cream cheese', 'mozzarella', 'cheddar', 'parmesan', 'gouda', 'brie', 'feta',
             'blue cheese', 'swiss', 'provolone', 'ricotta', 'mascarpone', 'halloumi',
             'kefir', 'buttermilk', 'half and half', 'heavy cream', 'whipping cream']
    
    grains = ['bread', 'rice', 'pasta', 'noodle', 'quinoa', 'oat', 'wheat', 'flour', 'cereal', 
              'toast', 'sandwich', 'burger bun', 'tortilla', 'wrap', 'bagel', 'croissant',
              'muffin', 'biscuit', 'roll', 'bun', 'pita', 'naan', 'focaccia', 'sourdough',
              'rye', 'whole wheat', 'multigrain', 'brown rice', 'wild rice', 'basmati',
              'jasmine', 'arborio', 'couscous', 'bulgur', 'farro', 'barley', 'millet',
              'spelt', 'kamut', 'amaranth', 'teff', 'sorghum']
    
    nuts_seeds = ['almond', 'walnut', 'pecan', 'cashew', 'pistachio', 'macadamia', 'hazelnut',
                  'pine nut', 'peanut', 'sunflower seed', 'pumpkin seed', 'chia seed',
                  'flax seed', 'sesame seed', 'hemp seed', 'poppy seed', 'pomegranate seed']
    
    herbs_spices = ['basil', 'oregano', 'thyme', 'rosemary', 'sage', 'mint', 'parsley',
                    'cilantro', 'dill', 'chive', 'tarragon', 'marjoram', 'bay leaf',
                    'black pepper', 'white pepper', 'salt', 'garlic powder', 'onion powder',
                    'paprika', 'cayenne', 'chili powder', 'cumin', 'coriander', 'turmeric',
                    'ginger', 'cinnamon', 'nutmeg', 'clove', 'allspice', 'cardamom']
    
    # Check categories with improved matching
    if any(fruit in ingredient_lower for fruit in fruits):
        return 'fruit'
    elif any(veg in ingredient_lower for veg in vegetables):
        return 'vegetable'
    elif any(meat in ingredient_lower for meat in meats):
        return 'meat'
    elif any(dairy_item in ingredient_lower for dairy_item in dairy):
        return 'dairy'
    elif any(grain in ingredient_lower for grain in grains):
        return 'grain'
    elif any(nut in ingredient_lower for nut in nuts_seeds):
        return 'nuts_seeds'
    elif any(herb in ingredient_lower for herb in herbs_spices):
        return 'herbs_spices'
    else:
        return 'other'

def analyze_with_gemini(image_data: str, clarifai_results: List[str]) -> List[Dict[str, Any]]:
    """Use Gemini to validate and enhance Clarifai results."""
    try:
        # Create prompt for Gemini
        prompt = f"""
You are a food recognition expert. Analyze this image and validate the following detected ingredients from an AI model:

DETECTED INGREDIENTS: {', '.join(clarifai_results)}

Please:
1. Validate if these ingredients are actually present in the image
2. Add any missing ingredients you can clearly see
3. Remove any false positives
4. Provide accurate quantities and units for each ingredient
5. Categorize each ingredient properly

Return ONLY a valid JSON array of ingredients (no additional text):
[
    {{
        "name": "ingredient name",
        "quantity": "estimated quantity",
        "unit": "unit of measurement",
        "category": "fruit/vegetable/meat/dairy/grain/nuts_seeds/herbs_spices/other",
        "confidence": "high/medium/low"
    }}
]

Focus on accuracy and be conservative - only include ingredients you're confident about.
"""
        
        # Convert base64 to image for Gemini
        if image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]
        image_bytes = base64.b64decode(image_data)
        
        # Generate response from Gemini
        response = gemini_model.generate_content([prompt, {"mime_type": "image/jpeg", "data": image_bytes}])
        
        if response and response.text:
            import json
            # Clean response text
            cleaned_text = response.text.strip()
            if cleaned_text.startswith('```json'):
                cleaned_text = cleaned_text[7:]
            if cleaned_text.endswith('```'):
                cleaned_text = cleaned_text[:-3]
            
            gemini_results = json.loads(cleaned_text.strip())
            return gemini_results
        
    except Exception as e:
        print(f"Gemini analysis error: {e}")
    
    return []

def analyze_food_image(image_data: str) -> List[Dict[str, Any]]:
    """
    Enhanced food image analysis using multiple AI models and preprocessing techniques.
    """
    print("Starting enhanced image analysis...")
    try:
        # 1. Decode base64 image
        if image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]
        image_bytes = base64.b64decode(image_data)
        original_image = Image.open(BytesIO(image_bytes))

        # 2. Preprocess image with multiple techniques
        processed_images = preprocess_image(original_image)
        
        # 3. Clarifai configuration
        model_url = "https://clarifai.com/clarifai/main/models/food-item-recognition"
        pat_token = os.getenv('CLARIFAI_PAT_TOKEN')
        cols, rows = 6, 6  # Increased grid density
        confidence_threshold = 0.08  # Lowered threshold for more inclusivity
        top_n = 8  # Increased top predictions
        ignore_labels = {"food", "meal", "dessert", "snack", "dish", "cuisine", "cooking"}
        
        # Load model
        model = Model(url=model_url, pat=pat_token)

        # 4. Multi-image analysis
        all_ingredient_scores = defaultdict(float)
        all_ingredient_counts = defaultdict(int)
        all_ingredient_confidence = defaultdict(list)

        for img_idx, image in enumerate(processed_images):
            print(f"Analyzing preprocessed image {img_idx + 1}/{len(processed_images)}...")
            
            width, height = image.size
            crop_width = width // cols
            crop_height = height // rows
            overlap_x = crop_width // 4  # Increased overlap
            overlap_y = crop_height // 4
            
            for row in range(rows):
                for col in range(cols):
                    left = max(0, col * crop_width - overlap_x)
                    upper = max(0, row * crop_height - overlap_y)
                    right = min(width, (col + 1) * crop_width + overlap_x)
                    lower = min(height, (row + 1) * crop_height + overlap_y)

                    crop = image.crop((left, upper, right, lower))
                    if crop.mode == 'RGBA':
                        crop = crop.convert('RGB')

                    buffered = BytesIO()
                    crop.save(buffered, format="JPEG")
                    
                    try:
                        prediction = model.predict_by_bytes(buffered.getvalue())
                        concepts = prediction.outputs[0].data.concepts

                        filtered_concepts = [
                            c for c in concepts[:top_n]
                            if c.value >= confidence_threshold and c.name.lower() not in ignore_labels
                        ]
                        
                        for concept in filtered_concepts:
                            all_ingredient_scores[concept.name] += concept.value
                            all_ingredient_counts[concept.name] += 1
                            all_ingredient_confidence[concept.name].append(concept.value)
                            
                    except Exception as e:
                        print(f"Error processing grid cell ({row+1},{col+1}) in image {img_idx+1}: {e}")
                        continue

        # 5. Advanced aggregation with confidence weighting
        if not all_ingredient_scores:
            print("No ingredients detected from Clarifai analysis.")
            return []

        # Calculate weighted scores based on consistency across images
        final_ingredients = []
        for name, total_score in all_ingredient_scores.items():
            count = all_ingredient_counts[name]
            avg_confidence = sum(all_ingredient_confidence[name]) / len(all_ingredient_confidence[name])
            
            # Weight by consistency (higher weight for ingredients detected across multiple images)
            consistency_weight = min(count / len(processed_images), 1.0)
            weighted_score = total_score * consistency_weight * avg_confidence
            
            if count >= 2:  # Only include ingredients detected in at least 2 grid cells
                final_ingredients.append((name, weighted_score, count, avg_confidence))

        # Sort by weighted score
        final_ingredients.sort(key=lambda x: x[1], reverse=True)
        
        # Get top ingredients
        top_ingredients = [name for name, _, _, _ in final_ingredients[:15]]
        
        print(f"Clarifai detected: {', '.join(top_ingredients)}")
        
        # 6. Validate with Gemini
        print("Validating results with Gemini...")
        gemini_results = analyze_with_gemini(image_data, top_ingredients)
        
        # 7. Combine and finalize results
        final_results = []
        
        # Use Gemini results as primary if available
        if gemini_results:
            for result in gemini_results:
                if result.get('confidence') in ['high', 'medium']:
                    final_results.append({
                        'name': result['name'],
                        'quantity': result.get('quantity', '1-2'),
                        'unit': result.get('unit', 'pieces'),
                        'category': result.get('category', determine_food_category(result['name']))
                    })
        
        # Fallback to Clarifai results if Gemini fails
        if not final_results:
            for name, _, count, _ in final_ingredients[:10]:
                if count >= 3:
                    quantity, unit = "3-5", "pieces"
                elif count >= 2:
                    quantity, unit = "2-3", "pieces"
                else:
                    quantity, unit = "1-2", "pieces"

                category = determine_food_category(name)
                
                final_results.append({
                    'name': name,
                    'quantity': quantity,
                    'unit': unit,
                    'category': category
                })
        
        print(f"Final results: {len(final_results)} ingredients detected")
        for result in final_results:
            print(f" - {result['name']}: {result['quantity']} {result['unit']} ({result['category']})")
        
        return final_results

    except Exception as e:
        print(f"An unexpected error occurred during enhanced image analysis: {e}")
        import traceback
        print(traceback.format_exc())
        return [] 
