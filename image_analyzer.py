import base64
import os
import json
from io import BytesIO
from typing import List, Dict, Any
from PIL import Image, ImageEnhance, ImageFilter
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv('key.env')

# Initialize Gemini Vision API
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

def analyze_with_gemini_vision(image_data: str) -> List[Dict[str, Any]]:
    """Use Gemini Vision API to detect and analyze food ingredients in the image."""
    try:
        # Create comprehensive prompt for Gemini Vision
        prompt = """
You are a professional food recognition expert and nutritionist. Analyze this image and identify all food ingredients present.

INSTRUCTIONS:
1. Identify ALL food ingredients visible in the image
2. Provide accurate quantities and units for each ingredient
3. Categorize each ingredient properly
4. Be specific about ingredient names (e.g., "chicken breast" not just "chicken")
5. Estimate quantities based on what you can see
6. Only include ingredients you are confident about
7. Consider cooking state (raw, cooked, chopped, etc.)

Return ONLY a valid JSON array of ingredients (no additional text or explanations):

[
    {
        "name": "specific ingredient name",
        "quantity": "estimated quantity (e.g., 2, 500g, 1 cup, 3 slices)",
        "unit": "unit of measurement (e.g., pieces, grams, cups, slices, whole)",
        "category": "fruit/vegetable/meat/dairy/grain/nuts_seeds/herbs_spices/other",
        "confidence": "high/medium/low",
        "notes": "brief description of state or preparation (e.g., raw, cooked, chopped, fresh)"
    }
]

IMPORTANT GUIDELINES:
- Be conservative and accurate - only include ingredients you're confident about
- Use specific ingredient names (e.g., "bell pepper" not just "pepper")
- Provide realistic quantity estimates
- Consider the context and cooking state
- Focus on ingredients that could be used in cooking
- Return ONLY the JSON array, no other text
"""
        
        # Convert base64 to image for Gemini
        if image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]
        image_bytes = base64.b64decode(image_data)
        
        # Generate response from Gemini Vision
        response = gemini_model.generate_content([prompt, {"mime_type": "image/jpeg", "data": image_bytes}])
        
        if response and response.text:
            # Clean response text
            cleaned_text = response.text.strip()
            
            # Remove markdown formatting if present
            if cleaned_text.startswith('```json'):
                cleaned_text = cleaned_text[7:]
            if cleaned_text.endswith('```'):
                cleaned_text = cleaned_text[:-3]
            
            # Remove any leading/trailing text that might be before/after JSON
            start_idx = cleaned_text.find('[')
            end_idx = cleaned_text.rfind(']') + 1
            if start_idx != -1 and end_idx != 0:
                cleaned_text = cleaned_text[start_idx:end_idx]
            
            gemini_results = json.loads(cleaned_text.strip())
            
            # Validate and clean results
            validated_results = []
            for result in gemini_results:
                if isinstance(result, dict) and 'name' in result:
                    # Ensure required fields exist
                    validated_result = {
                        'name': result.get('name', '').strip(),
                        'quantity': result.get('quantity', '1-2'),
                        'unit': result.get('unit', 'pieces'),
                        'category': result.get('category', determine_food_category(result.get('name', ''))),
                        'confidence': result.get('confidence', 'medium'),
                        'notes': result.get('notes', '')
                    }
                    
                    # Only include ingredients with valid names
                    if validated_result['name']:
                        validated_results.append(validated_result)
            
            return validated_results
        
    except json.JSONDecodeError as e:
        print(f"JSON parsing error in Gemini response: {e}")
        print(f"Response text: {response.text if response else 'No response'}")
        return []
    except Exception as e:
        print(f"Gemini Vision analysis error: {e}")
        return []

def analyze_food_image(image_data: str) -> List[Dict[str, Any]]:
    """
    Analyze food image using Gemini Vision API for accurate ingredient detection.
    """
    print("Starting Gemini Vision food analysis...")
    try:
        # 1. Decode base64 image
        if image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]
        image_bytes = base64.b64decode(image_data)
        original_image = Image.open(BytesIO(image_bytes))

        # 2. Preprocess image with multiple techniques for better detection
        processed_images = preprocess_image(original_image)
        
        # 3. Analyze with Gemini Vision using the original image
        print("Analyzing image with Gemini Vision...")
        gemini_results = analyze_with_gemini_vision(image_data)
        
        if gemini_results:
            print(f"Gemini Vision detected {len(gemini_results)} ingredients:")
            for result in gemini_results:
                print(f" - {result['name']}: {result['quantity']} {result['unit']} ({result['category']}) - {result['confidence']} confidence")
            
            # Filter results to only include high and medium confidence ingredients
            final_results = []
            for result in gemini_results:
                if result['confidence'] in ['high', 'medium']:
                    final_results.append({
                        'name': result['name'],
                        'quantity': result['quantity'],
                        'unit': result['unit'],
                        'category': result['category']
                    })
            
            print(f"Final results: {len(final_results)} ingredients after confidence filtering")
            return final_results
        else:
            print("No ingredients detected by Gemini Vision")
            return []

    except Exception as e:
        print(f"An unexpected error occurred during Gemini Vision analysis: {e}")
        import traceback
        print(traceback.format_exc())
        return [] 
