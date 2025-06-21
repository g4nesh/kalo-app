import base64
import os
from io import BytesIO
from collections import defaultdict
from typing import List, Dict, Any

from PIL import Image
from clarifai.client.model import Model
from dotenv import load_dotenv

# Load environment variables
load_dotenv('key.env')

def determine_food_category(ingredient_name: str) -> str:
    """Determine the food category based on ingredient name."""
    ingredient_lower = ingredient_name.lower()
    
    # Fruits
    fruits = ['apple', 'banana', 'orange', 'grape', 'strawberry', 'blueberry', 'raspberry', 
              'blackberry', 'pineapple', 'mango', 'peach', 'pear', 'plum', 'cherry', 'lemon', 'lime']
    
    # Vegetables
    vegetables = ['carrot', 'broccoli', 'spinach', 'lettuce', 'tomato', 'onion', 'garlic', 
                  'potato', 'sweet potato', 'corn', 'pepper', 'bell pepper', 'cucumber', 
                  'zucchini', 'eggplant', 'mushroom', 'cauliflower', 'cabbage', 'kale']
    
    # Meats
    meats = ['chicken', 'beef', 'pork', 'lamb', 'turkey', 'duck', 'fish', 'salmon', 'tuna', 
             'shrimp', 'bacon', 'sausage', 'ham', 'steak', 'burger', 'meatball']
    
    # Dairy
    dairy = ['milk', 'cheese', 'yogurt', 'butter', 'cream', 'sour cream', 'cottage cheese', 
             'cream cheese', 'mozzarella', 'cheddar', 'parmesan']
    
    # Grains
    grains = ['bread', 'rice', 'pasta', 'noodle', 'quinoa', 'oat', 'wheat', 'flour', 'cereal', 
              'toast', 'sandwich', 'burger bun', 'tortilla', 'wrap']
    
    # Check categories
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
    else:
        return 'other'

def analyze_food_image(image_data: str) -> List[Dict[str, Any]]:
    """
    Analyzes a food image using Clarifai's food recognition model with grid-based analysis,
    based on the user's validated test script.
    """
    print("Starting image analysis with dedicated analyzer module...")
    try:
        # 1. Decode base64 image
        if image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]
        image_bytes = base64.b64decode(image_data)
        image = Image.open(BytesIO(image_bytes))

        # 2. Configs from the working test script
        model_url = "https://clarifai.com/clarifai/main/models/food-item-recognition"
        pat_token = os.getenv('CLARIFAI_PAT_TOKEN')
        cols, rows = 4, 4
        confidence_threshold = 0.10
        top_n = 5
        ignore_labels = {"food", "meal", "dessert", "snack", "dish"}
        
        # Load model
        model = Model(url=model_url, pat=pat_token)

        # 3. Grid processing logic from the test script
        width, height = image.size
        crop_width = width // cols
        crop_height = height // rows
        overlap_x = crop_width // 3
        overlap_y = crop_height // 3
        
        ingredient_scores = defaultdict(float)
        ingredient_counts = defaultdict(int)

        print(f"Analyzing image with {cols}x{rows} grid...")
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
                    
                    if filtered_concepts:
                        preds_str = ", ".join(f"{c.name} ({c.value:.2f})" for c in filtered_concepts)
                        print(f"Grid cell ({row+1},{col+1}): {preds_str}")
                        for concept in filtered_concepts:
                            ingredient_scores[concept.name] += concept.value
                            ingredient_counts[concept.name] += 1
                except Exception as e:
                    print(f"Error processing grid cell ({row+1},{col+1}): {e}")
                    continue

        # 4. Final aggregation from the test script
        if not ingredient_scores:
             print("Clarifai analysis returned no ingredients.")
             return []

        print("\nAggregated detected ingredients:")
        final_ingredients = sorted(
            ingredient_scores.items(),
            key=lambda x: (x[1], ingredient_counts[x[0]]),
            reverse=True
        )

        # 5. Format output
        cleaned_ingredients = []
        for name, score in final_ingredients[:10]:
            count = ingredient_counts[name]
            print(f" - {name}: total score {score:.2f} over {count} cells")
            
            if count >= 3: quantity, unit = "3-5", "pieces"
            elif count >= 2: quantity, unit = "2-3", "pieces"
            else: quantity, unit = "1-2", "pieces"

            category = determine_food_category(name)
            
            cleaned_ingredients.append({
                'name': name, 'quantity': quantity,
                'unit': unit, 'category': category
            })
        
        print(f"Returning {len(cleaned_ingredients)} detected ingredients from Clarifai.")
        return cleaned_ingredients

    except Exception as e:
        print(f"An unexpected error occurred during image analysis: {e}")
        import traceback
        print(traceback.format_exc())
        return [] 