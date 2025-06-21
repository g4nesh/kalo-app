SAMPLE_RECIPES = [
    # Original recipes
    {
        'name': 'Grilled Chicken Salad',
        'meal_type': 'lunch',
        'cuisine': 'American',
        'calories': 350,
        'protein': 35,
        'carbs': 15,
        'fat': 18,
        'prep_time': 15,
        'cook_time': 20,
        'servings': 2,
        'difficulty': 'easy',
        'ingredients': [
            {'name': 'chicken breast', 'amount': '200g'},
            {'name': 'mixed greens', 'amount': '4 cups'},
            {'name': 'cherry tomatoes', 'amount': '1 cup'},
            {'name': 'cucumber', 'amount': '1'},
            {'name': 'olive oil', 'amount': '2 tbsp'},
            {'name': 'balsamic vinegar', 'amount': '1 tbsp'}
        ],
        'instructions': [
            'Season chicken with salt and pepper',
            'Grill chicken for 6-8 minutes per side',
            'Let chicken rest for 5 minutes',
            'Slice chicken into strips',
            'Combine all ingredients in a bowl',
            'Drizzle with olive oil and balsamic vinegar'
        ],
        'tags': ['healthy', 'high-protein', 'low-carb', 'gluten-free']
    },
    {
        'name': 'Vegetable Stir Fry',
        'meal_type': 'dinner',
        'cuisine': 'Asian',
        'calories': 400,
        'protein': 15,
        'carbs': 45,
        'fat': 20,
        'prep_time': 20,
        'cook_time': 15,
        'servings': 4,
        'difficulty': 'medium',
        'ingredients': [
            {'name': 'tofu', 'amount': '400g'},
            {'name': 'broccoli', 'amount': '2 cups'},
            {'name': 'bell peppers', 'amount': '2'},
            {'name': 'carrots', 'amount': '2'},
            {'name': 'soy sauce', 'amount': '3 tbsp'},
            {'name': 'sesame oil', 'amount': '1 tbsp'}
        ],
        'instructions': [
            'Cut tofu into cubes',
            'Chop all vegetables',
            'Heat sesame oil in a wok',
            'Stir fry tofu until golden',
            'Add vegetables and stir fry for 5 minutes',
            'Add soy sauce and cook for 2 more minutes'
        ],
        'tags': ['vegetarian', 'vegan', 'healthy', 'quick']
    },
    {
        'name': 'Overnight Oats',
        'meal_type': 'breakfast',
        'cuisine': 'International',
        'calories': 300,
        'protein': 12,
        'carbs': 45,
        'fat': 10,
        'prep_time': 5,
        'cook_time': 0,
        'servings': 1,
        'difficulty': 'easy',
        'ingredients': [
            {'name': 'oats', 'amount': '1/2 cup'},
            {'name': 'milk', 'amount': '1 cup'},
            {'name': 'honey', 'amount': '1 tbsp'},
            {'name': 'berries', 'amount': '1/2 cup'},
            {'name': 'chia seeds', 'amount': '1 tbsp'}
        ],
        'instructions': [
            'Combine oats and milk in a jar',
            'Add honey and chia seeds',
            'Stir well and refrigerate overnight',
            'Top with berries in the morning'
        ],
        'tags': ['vegetarian', 'make-ahead', 'healthy', 'quick']
    },
    {
        'name': 'Green Smoothie',
        'meal_type': 'drink',
        'cuisine': 'International',
        'calories': 200,
        'protein': 5,
        'carbs': 30,
        'fat': 8,
        'prep_time': 5,
        'cook_time': 0,
        'servings': 1,
        'difficulty': 'easy',
        'ingredients': [
            {'name': 'spinach', 'amount': '2 cups'},
            {'name': 'banana', 'amount': '1'},
            {'name': 'apple', 'amount': '1'},
            {'name': 'almond milk', 'amount': '1 cup'},
            {'name': 'honey', 'amount': '1 tbsp'}
        ],
        'instructions': [
            'Wash all fruits and vegetables',
            'Add all ingredients to blender',
            'Blend until smooth',
            'Serve immediately'
        ],
        'tags': ['vegetarian', 'vegan', 'healthy', 'quick']
    },
    {
        'name': 'Trail Mix',
        'meal_type': 'snack',
        'cuisine': 'International',
        'calories': 150,
        'protein': 5,
        'carbs': 15,
        'fat': 10,
        'prep_time': 5,
        'cook_time': 0,
        'servings': 1,
        'difficulty': 'easy',
        'ingredients': [
            {'name': 'almonds', 'amount': '1/4 cup'},
            {'name': 'dried cranberries', 'amount': '1/4 cup'},
            {'name': 'dark chocolate chips', 'amount': '2 tbsp'},
            {'name': 'pumpkin seeds', 'amount': '2 tbsp'}
        ],
        'instructions': [
            'Combine all ingredients in a bowl',
            'Mix well',
            'Store in an airtight container'
        ],
        'tags': ['vegetarian', 'vegan', 'healthy', 'quick', 'portable']
    },
    
    # New breakfast recipes
    {
        'name': 'Protein Pancakes',
        'meal_type': 'breakfast',
        'cuisine': 'American',
        'calories': 380,
        'protein': 25,
        'carbs': 35,
        'fat': 15,
        'prep_time': 10,
        'cook_time': 15,
        'servings': 2,
        'difficulty': 'easy',
        'ingredients': [
            {'name': 'eggs', 'amount': '3'},
            {'name': 'banana', 'amount': '1'},
            {'name': 'protein powder', 'amount': '30g'},
            {'name': 'oats', 'amount': '1/4 cup'},
            {'name': 'coconut oil', 'amount': '1 tbsp'},
            {'name': 'maple syrup', 'amount': '2 tbsp'}
        ],
        'instructions': [
            'Blend eggs, banana, protein powder, and oats',
            'Heat coconut oil in a non-stick pan',
            'Pour batter to form pancakes',
            'Cook 2-3 minutes per side until golden',
            'Serve with maple syrup'
        ],
        'tags': ['high-protein', 'gluten-free', 'quick', 'fitness']
    },
    {
        'name': 'Avocado Toast',
        'meal_type': 'breakfast',
        'cuisine': 'International',
        'calories': 320,
        'protein': 12,
        'carbs': 25,
        'fat': 22,
        'prep_time': 8,
        'cook_time': 5,
        'servings': 1,
        'difficulty': 'easy',
        'ingredients': [
            {'name': 'whole wheat bread', 'amount': '2 slices'},
            {'name': 'avocado', 'amount': '1'},
            {'name': 'egg', 'amount': '1'},
            {'name': 'lime juice', 'amount': '1 tsp'},
            {'name': 'red pepper flakes', 'amount': '1/4 tsp'},
            {'name': 'salt', 'amount': 'to taste'}
        ],
        'instructions': [
            'Toast bread slices',
            'Mash avocado with lime juice and salt',
            'Fry or poach egg to preference',
            'Spread avocado on toast',
            'Top with egg and red pepper flakes'
        ],
        'tags': ['vegetarian', 'healthy', 'trendy', 'quick']
    },
    {
        'name': 'Greek Yogurt Parfait',
        'meal_type': 'breakfast',
        'cuisine': 'Mediterranean',
        'calories': 280,
        'protein': 20,
        'carbs': 35,
        'fat': 8,
        'prep_time': 5,
        'cook_time': 0,
        'servings': 1,
        'difficulty': 'easy',
        'ingredients': [
            {'name': 'Greek yogurt', 'amount': '1 cup'},
            {'name': 'granola', 'amount': '1/4 cup'},
            {'name': 'mixed berries', 'amount': '1/2 cup'},
            {'name': 'honey', 'amount': '1 tbsp'},
            {'name': 'walnuts', 'amount': '2 tbsp'}
        ],
        'instructions': [
            'Layer half the yogurt in a glass',
            'Add half the berries and granola',
            'Repeat layers',
            'Top with walnuts and drizzle with honey'
        ],
        'tags': ['vegetarian', 'high-protein', 'healthy', 'no-cook']
    },
    
    # New lunch recipes
    {
        'name': 'Quinoa Buddha Bowl',
        'meal_type': 'lunch',
        'cuisine': 'International',
        'calories': 450,
        'protein': 18,
        'carbs': 55,
        'fat': 18,
        'prep_time': 20,
        'cook_time': 25,
        'servings': 2,
        'difficulty': 'medium',
        'ingredients': [
            {'name': 'quinoa', 'amount': '1 cup'},
            {'name': 'sweet potato', 'amount': '1 large'},
            {'name': 'chickpeas', 'amount': '1 can'},
            {'name': 'kale', 'amount': '2 cups'},
            {'name': 'tahini', 'amount': '3 tbsp'},
            {'name': 'lemon juice', 'amount': '2 tbsp'}
        ],
        'instructions': [
            'Cook quinoa according to package directions',
            'Roast diced sweet potato for 25 minutes',
            'Rinse and drain chickpeas',
            'Massage kale with lemon juice',
            'Mix tahini with water for dressing',
            'Arrange all ingredients in bowls and drizzle with dressing'
        ],
        'tags': ['vegan', 'healthy', 'complete-protein', 'meal-prep']
    },
    {
        'name': 'Turkey Club Wrap',
        'meal_type': 'lunch',
        'cuisine': 'American',
        'calories': 420,
        'protein': 28,
        'carbs': 32,
        'fat': 22,
        'prep_time': 10,
        'cook_time': 0,
        'servings': 1,
        'difficulty': 'easy',
        'ingredients': [
            {'name': 'whole wheat tortilla', 'amount': '1 large'},
            {'name': 'turkey breast', 'amount': '100g'},
            {'name': 'bacon', 'amount': '2 strips'},
            {'name': 'lettuce', 'amount': '3 leaves'},
            {'name': 'tomato', 'amount': '1/2'},
            {'name': 'mayonnaise', 'amount': '1 tbsp'}
        ],
        'instructions': [
            'Cook bacon until crispy',
            'Spread mayo on tortilla',
            'Layer turkey, bacon, lettuce, and tomato',
            'Roll tightly and slice in half'
        ],
        'tags': ['high-protein', 'portable', 'quick', 'comfort-food']
    },
    {
        'name': 'Asian Lettuce Wraps',
        'meal_type': 'lunch',
        'cuisine': 'Asian',
        'calories': 290,
        'protein': 22,
        'carbs': 18,
        'fat': 15,
        'prep_time': 15,
        'cook_time': 12,
        'servings': 3,
        'difficulty': 'medium',
        'ingredients': [
            {'name': 'ground chicken', 'amount': '300g'},
            {'name': 'butter lettuce', 'amount': '1 head'},
            {'name': 'mushrooms', 'amount': '200g'},
            {'name': 'green onions', 'amount': '3'},
            {'name': 'ginger', 'amount': '1 tbsp'},
            {'name': 'soy sauce', 'amount': '2 tbsp'}
        ],
        'instructions': [
            'Cook ground chicken in a large pan',
            'Add diced mushrooms and cook until soft',
            'Stir in ginger, soy sauce, and green onions',
            'Separate lettuce leaves',
            'Serve chicken mixture in lettuce cups'
        ],
        'tags': ['low-carb', 'high-protein', 'gluten-free', 'light']
    },
    
    # New dinner recipes
    {
        'name': 'Salmon with Roasted Vegetables',
        'meal_type': 'dinner',
        'cuisine': 'Mediterranean',
        'calories': 520,
        'protein': 35,
        'carbs': 25,
        'fat': 32,
        'prep_time': 15,
        'cook_time': 30,
        'servings': 2,
        'difficulty': 'medium',
        'ingredients': [
            {'name': 'salmon fillet', 'amount': '300g'},
            {'name': 'zucchini', 'amount': '2'},
            {'name': 'bell peppers', 'amount': '2'},
            {'name': 'olive oil', 'amount': '3 tbsp'},
            {'name': 'lemon', 'amount': '1'},
            {'name': 'herbs de provence', 'amount': '1 tsp'}
        ],
        'instructions': [
            'Preheat oven to 400°F',
            'Cut vegetables into chunks',
            'Toss vegetables with olive oil and herbs',
            'Roast vegetables for 20 minutes',
            'Add seasoned salmon to pan',
            'Bake for 12-15 minutes until fish flakes easily'
        ],
        'tags': ['healthy', 'omega-3', 'low-carb', 'one-pan']
    },
    {
        'name': 'Beef Stir Fry with Brown Rice',
        'meal_type': 'dinner',
        'cuisine': 'Asian',
        'calories': 480,
        'protein': 30,
        'carbs': 45,
        'fat': 20,
        'prep_time': 20,
        'cook_time': 25,
        'servings': 3,
        'difficulty': 'medium',
        'ingredients': [
            {'name': 'beef sirloin', 'amount': '250g'},
            {'name': 'brown rice', 'amount': '1 cup'},
            {'name': 'snap peas', 'amount': '200g'},
            {'name': 'garlic', 'amount': '3 cloves'},
            {'name': 'oyster sauce', 'amount': '2 tbsp'},
            {'name': 'vegetable oil', 'amount': '2 tbsp'}
        ],
        'instructions': [
            'Cook brown rice according to package directions',
            'Slice beef into thin strips',
            'Heat oil in wok over high heat',
            'Stir fry beef for 3-4 minutes',
            'Add garlic and snap peas',
            'Add oyster sauce and cook 2 more minutes'
        ],
        'tags': ['high-protein', 'whole-grains', 'quick', 'balanced']
    },
    {
        'name': 'Vegetarian Lentil Curry',
        'meal_type': 'dinner',
        'cuisine': 'Indian',
        'calories': 380,
        'protein': 20,
        'carbs': 50,
        'fat': 12,
        'prep_time': 15,
        'cook_time': 35,
        'servings': 4,
        'difficulty': 'medium',
        'ingredients': [
            {'name': 'red lentils', 'amount': '1.5 cups'},
            {'name': 'coconut milk', 'amount': '400ml'},
            {'name': 'onion', 'amount': '1'},
            {'name': 'curry powder', 'amount': '2 tbsp'},
            {'name': 'tomatoes', 'amount': '2'},
            {'name': 'spinach', 'amount': '2 cups'}
        ],
        'instructions': [
            'Sauté diced onion until soft',
            'Add curry powder and cook for 1 minute',
            'Add lentils, coconut milk, and diced tomatoes',
            'Simmer for 25 minutes until lentils are tender',
            'Stir in spinach until wilted',
            'Season with salt and pepper'
        ],
        'tags': ['vegan', 'high-fiber', 'protein-rich', 'comfort-food']
    },
    
    # New snack recipes
    {
        'name': 'Protein Energy Balls',
        'meal_type': 'snack',
        'cuisine': 'International',
        'calories': 180,
        'protein': 8,
        'carbs': 20,
        'fat': 9,
        'prep_time': 15,
        'cook_time': 0,
        'servings': 4,
        'difficulty': 'easy',
        'ingredients': [
            {'name': 'dates', 'amount': '12'},
            {'name': 'almond butter', 'amount': '3 tbsp'},
            {'name': 'protein powder', 'amount': '30g'},
            {'name': 'coconut flakes', 'amount': '2 tbsp'},
            {'name': 'chia seeds', 'amount': '1 tbsp'}
        ],
        'instructions': [
            'Remove pits from dates',
            'Blend dates until they form a paste',
            'Mix in almond butter and protein powder',
            'Roll mixture into 12 balls',
            'Roll balls in coconut flakes and chia seeds'
        ],
        'tags': ['no-bake', 'portable', 'energy', 'make-ahead']
    },
    {
        'name': 'Hummus and Veggie Plate',
        'meal_type': 'snack',
        'cuisine': 'Mediterranean',
        'calories': 220,
        'protein': 10,
        'carbs': 25,
        'fat': 12,
        'prep_time': 10,
        'cook_time': 0,
        'servings': 1,
        'difficulty': 'easy',
        'ingredients': [
            {'name': 'hummus', 'amount': '1/3 cup'},
            {'name': 'carrots', 'amount': '1 large'},
            {'name': 'cucumber', 'amount': '1/2'},
            {'name': 'bell pepper', 'amount': '1/2'},
            {'name': 'pita bread', 'amount': '1 small'}
        ],
        'instructions': [
            'Cut vegetables into sticks',
            'Arrange vegetables on plate',
            'Serve with hummus and pita bread'
        ],
        'tags': ['vegetarian', 'fiber-rich', 'fresh', 'mediterranean']
    },
    {
        'name': 'Apple Slices with Almond Butter',
        'meal_type': 'snack',
        'cuisine': 'American',
        'calories': 190,
        'protein': 6,
        'carbs': 20,
        'fat': 12,
        'prep_time': 3,
        'cook_time': 0,
        'servings': 1,
        'difficulty': 'easy',
        'ingredients': [
            {'name': 'apple', 'amount': '1 medium'},
            {'name': 'almond butter', 'amount': '2 tbsp'},
            {'name': 'cinnamon', 'amount': 'pinch'}
        ],
        'instructions': [
            'Slice apple into wedges',
            'Serve with almond butter for dipping',
            'Sprinkle with cinnamon'
        ],
        'tags': ['natural', 'quick', 'satisfying', 'kid-friendly']
    },
    
    # New drink recipes
    {
        'name': 'Protein Smoothie Bowl',
        'meal_type': 'drink',
        'cuisine': 'International',
        'calories': 340,
        'protein': 25,
        'carbs': 40,
        'fat': 12,
        'prep_time': 10,
        'cook_time': 0,
        'servings': 1,
        'difficulty': 'easy',
        'ingredients': [
            {'name': 'frozen berries', 'amount': '1 cup'},
            {'name': 'protein powder', 'amount': '30g'},
            {'name': 'Greek yogurt', 'amount': '1/2 cup'},
            {'name': 'banana', 'amount': '1/2'},
            {'name': 'granola', 'amount': '2 tbsp'},
            {'name': 'coconut flakes', 'amount': '1 tbsp'}
        ],
        'instructions': [
            'Blend berries, protein powder, yogurt, and banana',
            'Pour into bowl',
            'Top with granola and coconut flakes'
        ],
        'tags': ['high-protein', 'antioxidants', 'post-workout', 'filling']
    },
    {
        'name': 'Golden Turmeric Latte',
        'meal_type': 'drink',
        'cuisine': 'Indian',
        'calories': 120,
        'protein': 4,
        'carbs': 15,
        'fat': 6,
        'prep_time': 5,
        'cook_time': 5,
        'servings': 1,
        'difficulty': 'easy',
        'ingredients': [
            {'name': 'coconut milk', 'amount': '1 cup'},
            {'name': 'turmeric', 'amount': '1 tsp'},
            {'name': 'ginger', 'amount': '1/2 tsp'},
            {'name': 'honey', 'amount': '1 tbsp'},
            {'name': 'cinnamon', 'amount': '1/4 tsp'},
            {'name': 'black pepper', 'amount': 'pinch'}
        ],
        'instructions': [
            'Heat coconut milk in a saucepan',
            'Whisk in turmeric, ginger, and cinnamon',
            'Simmer for 3 minutes',
            'Strain and sweeten with honey',
            'Add pinch of black pepper'
        ],
        'tags': ['anti-inflammatory', 'warming', 'vegan', 'wellness']
    },
    {
        'name': 'Iced Matcha Latte',
        'meal_type': 'drink',
        'cuisine': 'Japanese',
        'calories': 110,
        'protein': 6,
        'carbs': 12,
        'fat': 4,
        'prep_time': 5,
        'cook_time': 0,
        'servings': 1,
        'difficulty': 'easy',
        'ingredients': [
            {'name': 'matcha powder', 'amount': '1 tsp'},
            {'name': 'oat milk', 'amount': '1 cup'},
            {'name': 'maple syrup', 'amount': '1 tbsp'},
            {'name': 'ice cubes', 'amount': '1 cup'},
            {'name': 'vanilla extract', 'amount': '1/4 tsp'}
        ],
        'instructions': [
            'Whisk matcha with 2 tbsp hot water',
            'Add maple syrup and vanilla',
            'Fill glass with ice',
            'Pour in oat milk and matcha mixture',
            'Stir well before drinking'
        ],
        'tags': ['caffeinated', 'antioxidants', 'refreshing', 'energizing']
    },
    
    # Additional diverse recipes
    {
        'name': 'Mediterranean Chickpea Salad',
        'meal_type': 'lunch',
        'cuisine': 'Mediterranean',
        'calories': 360,
        'protein': 16,
        'carbs': 45,
        'fat': 14,
        'prep_time': 15,
        'cook_time': 0,
        'servings': 2,
        'difficulty': 'easy',
        'ingredients': [
            {'name': 'chickpeas', 'amount': '2 cans'},
            {'name': 'feta cheese', 'amount': '100g'},
            {'name': 'olives', 'amount': '1/2 cup'},
            {'name': 'red onion', 'amount': '1/4 cup'},
            {'name': 'parsley', 'amount': '1/4 cup'},
            {'name': 'lemon juice', 'amount': '3 tbsp'}
        ],
        'instructions': [
            'Drain and rinse chickpeas',
            'Dice red onion and crumble feta',
            'Combine all ingredients in a bowl',
            'Dress with lemon juice and olive oil',
            'Let marinate for 30 minutes before serving'
        ],
        'tags': ['vegetarian', 'protein-rich', 'mediterranean', 'meal-prep']
    },
    {
        'name': 'Stuffed Bell Peppers',
        'meal_type': 'dinner',
        'cuisine': 'American',
        'calories': 420,
        'protein': 25,
        'carbs': 35,
        'fat': 20,
        'prep_time': 25,
        'cook_time': 45,
        'servings': 4,
        'difficulty': 'medium',
        'ingredients': [
            {'name': 'bell peppers', 'amount': '4 large'},
            {'name': 'ground turkey', 'amount': '400g'},
            {'name': 'brown rice', 'amount': '1 cup cooked'},
            {'name': 'diced tomatoes', 'amount': '1 can'},
            {'name': 'mozzarella cheese', 'amount': '1 cup'},
            {'name': 'Italian seasoning', 'amount': '1 tbsp'}
        ],
        'instructions': [
            'Cut tops off peppers and remove seeds',
            'Cook ground turkey with Italian seasoning',
            'Mix turkey with rice and diced tomatoes',
            'Stuff peppers with mixture',
            'Top with cheese and bake at 375°F for 35 minutes'
        ],
        'tags': ['comfort-food', 'balanced', 'family-friendly', 'meal-prep']
    },
    {
        'name': 'Chocolate Chia Pudding',
        'meal_type': 'snack',
        'cuisine': 'International',
        'calories': 250,
        'protein': 8,
        'carbs': 25,
        'fat': 15,
        'prep_time': 10,
        'cook_time': 0,
        'servings': 2,
        'difficulty': 'easy',
        'ingredients': [
            {'name': 'chia seeds', 'amount': '1/4 cup'},
            {'name': 'almond milk', 'amount': '1 cup'},
            {'name': 'cocoa powder', 'amount': '2 tbsp'},
            {'name': 'maple syrup', 'amount': '2 tbsp'},
            {'name': 'vanilla extract', 'amount': '1/2 tsp'},
            {'name': 'berries', 'amount': '1/4 cup'}
        ],
        'instructions': [
            'Whisk together all ingredients except berries',
            'Refrigerate for at least 2 hours or overnight',
            'Stir before serving',
            'Top with fresh berries'
        ],
        'tags': ['healthy-dessert', 'make-ahead', 'vegan', 'omega-3']
    },
    {
        'name': 'Cauliflower Rice Bowl',
        'meal_type': 'dinner',
        'cuisine': 'Asian',
        'calories': 280,
        'protein': 12,
        'carbs': 20,
        'fat': 18,
        'prep_time': 15,
        'cook_time': 15,
        'servings': 2,
        'difficulty': 'medium',
        'ingredients': [
            {'name': 'cauliflower', 'amount': '1 head'},
            {'name': 'edamame', 'amount': '1 cup'},
            {'name': 'avocado', 'amount': '1'},
            {'name': 'sesame seeds', 'amount': '2 tbsp'},
            {'name': 'tamari', 'amount': '2 tbsp'},
            {'name': 'rice vinegar', 'amount': '1 tbsp'}
        ],
        'instructions': [
            'Pulse cauliflower in food processor to rice-like consistency',
            'Sauté cauliflower rice for 5-7 minutes',
            'Steam edamame according to package directions',
            'Slice avocado',
            'Combine all ingredients in bowls',
            'Drizzle with tamari and rice vinegar'
        ],
        'tags': ['low-carb', 'plant-based', 'light', 'nutrient-dense']
    },
    {
    'name': 'Sweet Plantain Black Bean Tacos',
    'meal_type': 'dinner',
    'cuisine': 'Mexican',
    'calories': 420,
    'protein': 14,
    'carbs': 52,
    'fat': 18,
    'prep_time': 10,
    'cook_time': 20,
    'servings': 2,
    'difficulty': 'easy',
    'ingredients': [
        {'name': 'ripe plantains', 'amount': '2'},
        {'name': 'black beans', 'amount': '1 can'},
        {'name': 'corn tortillas', 'amount': '6 small'},
        {'name': 'red onion', 'amount': '1/2, sliced'},
        {'name': 'cilantro', 'amount': '1/4 cup, chopped'},
        {'name': 'lime', 'amount': '1'},
        {'name': 'olive oil', 'amount': '1 tbsp'}
    ],
    'instructions': [
        'Slice plantains and pan-fry in olive oil until golden brown',
        'Warm black beans with a pinch of salt',
        'Heat tortillas until pliable',
        'Assemble tacos with beans, plantains, onion, and cilantro',
        'Squeeze lime juice over the top before serving'
    ],
    'tags': ['vegan', 'sweet', 'mexican', 'easy', 'high-fiber']
},
{
    'name': 'Mango Chickpea Quinoa Bowl',
    'meal_type': 'dinner',
    'cuisine': 'Mexican',
    'calories': 510,
    'protein': 17,
    'carbs': 60,
    'fat': 22,
    'prep_time': 15,
    'cook_time': 15,
    'servings': 2,
    'difficulty': 'medium',
    'ingredients': [
        {'name': 'quinoa', 'amount': '1 cup uncooked'},
        {'name': 'chickpeas', 'amount': '1 can'},
        {'name': 'mango', 'amount': '1, diced'},
        {'name': 'avocado', 'amount': '1, sliced'},
        {'name': 'red bell pepper', 'amount': '1, diced'},
        {'name': 'lime', 'amount': '1, juiced'},
        {'name': 'cumin', 'amount': '1 tsp'}
    ],
    'instructions': [
        'Cook quinoa according to package instructions',
        'Sauté chickpeas with cumin for 5-7 minutes',
        'Prepare all other ingredients',
        'Assemble quinoa bowls with mango, chickpeas, avocado, and bell pepper',
        'Drizzle lime juice over the top before serving'
    ],
    'tags': ['vegan', 'sweet', 'protein-rich', 'fiber-packed']
},
{
    'name': 'Sweet Potato Enchiladas',
    'meal_type': 'dinner',
    'cuisine': 'Mexican',
    'calories': 470,
    'protein': 15,
    'carbs': 55,
    'fat': 20,
    'prep_time': 20,
    'cook_time': 25,
    'servings': 2,
    'difficulty': 'hard',
    'ingredients': [
        {'name': 'sweet potatoes', 'amount': '2, peeled and cubed'},
        {'name': 'black beans', 'amount': '1 can'},
        {'name': 'corn tortillas', 'amount': '6'},
        {'name': 'enchilada sauce', 'amount': '1 cup'},
        {'name': 'red onion', 'amount': '1/2, diced'},
        {'name': 'olive oil', 'amount': '1 tbsp'}
    ],
    'instructions': [
        'Boil or roast sweet potatoes until soft',
        'Mash sweet potatoes and mix with black beans and onion',
        'Fill tortillas with mixture, roll, and place in baking dish',
        'Pour enchilada sauce over top',
        'Bake at 375°F for 20 minutes'
    ],
    'tags': ['vegan', 'sweet', 'hearty', 'comfort-food']
},
{
    'name': 'Grilled Corn & Pineapple Salad',
    'meal_type': 'dinner',
    'cuisine': 'Mexican',
    'calories': 350,
    'protein': 10,
    'carbs': 45,
    'fat': 14,
    'prep_time': 10,
    'cook_time': 15,
    'servings': 2,
    'difficulty': 'easy',
    'ingredients': [
        {'name': 'corn cobs', 'amount': '2'},
        {'name': 'pineapple rings', 'amount': '4'},
        {'name': 'avocado', 'amount': '1'},
        {'name': 'cilantro', 'amount': '1/4 cup'},
        {'name': 'lime', 'amount': '1'},
        {'name': 'olive oil', 'amount': '1 tbsp'}
    ],
    'instructions': [
        'Grill corn and pineapple until slightly charred',
        'Cut kernels off corn and dice pineapple',
        'Mix in diced avocado and chopped cilantro',
        'Drizzle with lime juice and olive oil',
        'Toss gently and serve warm or chilled'
    ],
    'tags': ['vegan', 'sweet', 'fresh', 'gluten-free']
}, 
{
    'name': 'Chipotle-Lime Sweet Potato Bowl',
    'meal_type': 'dinner',
    'cuisine': 'Mexican',
    'calories': 390,
    'protein': 11,
    'carbs': 48,
    'fat': 17,
    'prep_time': 15,
    'cook_time': 25,
    'servings': 2,
    'difficulty': 'medium',
    'ingredients': [
        {'name': 'sweet potatoes', 'amount': '2, cubed'},
        {'name': 'black beans', 'amount': '1 can'},
        {'name': 'quinoa', 'amount': '1/2 cup uncooked'},
        {'name': 'lime', 'amount': '1, juiced'},
        {'name': 'chipotle powder', 'amount': '1/2 tsp'},
        {'name': 'olive oil', 'amount': '1 tbsp'},
        {'name': 'maple syrup', 'amount': '1 tbsp'}
    ],
    'instructions': [
        'Roast sweet potatoes with olive oil, maple syrup, and chipotle powder for 25 minutes at 400°F',
        'Cook quinoa according to package directions',
        'Warm black beans',
        'Assemble bowls with quinoa, sweet potatoes, and beans',
        'Drizzle with fresh lime juice'
    ],
    'tags': ['vegan', 'gluten-free', 'dairy-free', 'sweet', 'spicy', 'balanced']
},
{
    'name': 'Coconut-Lime Lentil Tacos',
    'meal_type': 'dinner',
    'cuisine': 'Mexican',
    'calories': 420,
    'protein': 18,
    'carbs': 50,
    'fat': 16,
    'prep_time': 10,
    'cook_time': 20,
    'servings': 2,
    'difficulty': 'medium',
    'ingredients': [
        {'name': 'brown lentils', 'amount': '1 cup cooked'},
        {'name': 'coconut milk', 'amount': '1/2 cup'},
        {'name': 'lime', 'amount': '1, juiced'},
        {'name': 'corn tortillas', 'amount': '6'},
        {'name': 'cilantro', 'amount': '1/4 cup chopped'},
        {'name': 'red cabbage', 'amount': '1 cup shredded'}
    ],
    'instructions': [
        'Simmer lentils in coconut milk for 10 minutes until creamy',
        'Add lime juice and salt to taste',
        'Warm tortillas',
        'Fill with lentils and top with cabbage and cilantro'
    ],
    'tags': ['vegan', 'vegetarian', 'gluten-free', 'dairy-free', 'sweet-savory']
},
{
    'name': 'Butternut Squash & Black Bean Chili',
    'meal_type': 'dinner',
    'cuisine': 'Mexican',
    'calories': 380,
    'protein': 14,
    'carbs': 46,
    'fat': 14,
    'prep_time': 15,
    'cook_time': 30,
    'servings': 2,
    'difficulty': 'medium',
    'ingredients': [
        {'name': 'butternut squash', 'amount': '2 cups, cubed'},
        {'name': 'black beans', 'amount': '1 can'},
        {'name': 'tomatoes', 'amount': '1 can diced'},
        {'name': 'onion', 'amount': '1, chopped'},
        {'name': 'garlic', 'amount': '2 cloves, minced'},
        {'name': 'chili powder', 'amount': '1 tbsp'},
        {'name': 'olive oil', 'amount': '1 tbsp'}
    ],
    'instructions': [
        'Sauté onion and garlic in olive oil until translucent',
        'Add squash and cook for 5 minutes',
        'Add beans, tomatoes, and chili powder',
        'Simmer for 25 minutes until squash is soft',
        'Adjust seasoning and serve hot'
    ],
    'tags': ['vegan', 'dairy-free', 'gluten-free', 'vegetarian', 'hearty', 'warming']
},
{
    'name': 'Mexican-Spiced Roasted Chickpeas & Avocado Salad',
    'meal_type': 'dinner',
    'cuisine': 'Mexican',
    'calories': 350,
    'protein': 13,
    'carbs': 28,
    'fat': 20,
    'prep_time': 10,
    'cook_time': 25,
    'servings': 2,
    'difficulty': 'easy',
    'ingredients': [
        {'name': 'chickpeas', 'amount': '1 can, drained'},
        {'name': 'avocado', 'amount': '1, sliced'},
        {'name': 'lettuce or mixed greens', 'amount': '2 cups'},
        {'name': 'lime', 'amount': '1, juiced'},
        {'name': 'cumin', 'amount': '1 tsp'},
        {'name': 'paprika', 'amount': '1 tsp'},
        {'name': 'olive oil', 'amount': '1 tbsp'}
    ],
    'instructions': [
        'Toss chickpeas with olive oil, cumin, and paprika',
        'Roast at 400°F for 25 minutes until crispy',
        'Prepare greens and avocado in a bowl',
        'Add roasted chickpeas and drizzle with lime juice'
    ],
    'tags': ['vegan', 'gluten-free', 'dairy-free', 'light', 'crunchy', 'sweet-savory']
},
{
    'name': 'Chicken Parmesan with Zucchini Noodles',
    'meal_type': 'dinner',
    'cuisine': 'Italian',
    'calories': 480,
    'protein': 45,
    'carbs': 25,
    'fat': 22,
    'prep_time': 20,
    'cook_time': 30,
    'servings': 2,
    'difficulty': 'medium',
    'ingredients': [
        {'name': 'chicken breast', 'amount': '2 (150g each)'},
        {'name': 'zucchini', 'amount': '2 medium'},
        {'name': 'marinara sauce', 'amount': '1 cup'},
        {'name': 'mozzarella cheese', 'amount': '1/2 cup shredded'},
        {'name': 'Parmesan cheese', 'amount': '1/4 cup grated'},
        {'name': 'egg', 'amount': '1'},
        {'name': 'almond flour', 'amount': '1/2 cup'},
        {'name': 'olive oil', 'amount': '2 tbsp'}
    ],
    'instructions': [
        'Slice chicken breasts horizontally to thin them, dip in egg, then dredge in almond flour mixed with Parmesan.',
        'Pan-fry chicken in olive oil until golden brown on both sides, then transfer to a baking dish.',
        'Top chicken with marinara sauce and mozzarella cheese.',
        'Bake at 400°F (200°C) for 15-20 minutes, or until cheese is bubbly and chicken is cooked through.',
        'Meanwhile, spiralize zucchini into noodles. Sauté briefly in a pan with a little olive oil until tender-crisp.',
        'Serve chicken Parmesan over zucchini noodles.'
    ],
    'tags': ['high-protein', 'low-carb', 'comfort-food', 'gluten-free']
},
{
    'name': 'Caprese Salad Skewers',
    'meal_type': 'snack',
    'cuisine': 'Italian',
    'calories': 180,
    'protein': 8,
    'carbs': 10,
    'fat': 12,
    'prep_time': 10,
    'cook_time': 0,
    'servings': 1,
    'difficulty': 'easy',
    'ingredients': [
        {'name': 'cherry tomatoes', 'amount': '1 cup'},
        {'name': 'fresh mozzarella balls (bocconcini)', 'amount': '1 cup'},
        {'name': 'fresh basil leaves', 'amount': '1/2 cup'},
        {'name': 'balsamic glaze', 'amount': '2 tbsp'}
    ],
    'instructions': [
        'Thread cherry tomatoes, mozzarella balls, and basil leaves onto small skewers.',
        'Arrange skewers on a platter.',
        'Drizzle generously with balsamic glaze just before serving.'
    ],
    'tags': ['vegetarian', 'quick', 'fresh', 'mediterranean']
},
{
    'name': 'Vegetable Minestrone Soup',
    'meal_type': 'dinner',
    'cuisine': 'Italian',
    'calories': 320,
    'protein': 15,
    'carbs': 45,
    'fat': 10,
    'prep_time': 20,
    'cook_time': 40,
    'servings': 4,
    'difficulty': 'medium',
    'ingredients': [
        {'name': 'vegetable broth', 'amount': '6 cups'},
        {'name': 'diced tomatoes', 'amount': '1 can (14.5 oz)'},
        {'name': 'cannellini beans', 'amount': '1 can (15 oz), rinsed'},
        {'name': 'small pasta (ditalini)', 'amount': '1/2 cup'},
        {'name': 'carrots', 'amount': '2, diced'},
        {'name': 'celery stalks', 'amount': '2, diced'},
        {'name': 'zucchini', 'amount': '1 medium, diced'},
        {'name': 'spinach', 'amount': '2 cups fresh'},
        {'name': 'Parmesan cheese', 'amount': 'for serving (optional)'},
        {'name': 'olive oil', 'amount': '1 tbsp'}
    ],
    'instructions': [
        'Heat olive oil in a large pot over medium heat. Add diced carrots and celery; cook until softened, about 5-7 minutes.',
        'Stir in vegetable broth, diced tomatoes, and cannellini beans. Bring to a simmer.',
        'Add small pasta and diced zucchini. Cook for 10-12 minutes, or until pasta is al dente and zucchini is tender.',
        'Stir in fresh spinach until wilted.',
        'Season with salt and pepper to taste.',
        'Ladle into bowls and serve hot, optionally topped with grated Parmesan cheese.'
    ],
    'tags': ['vegetarian', 'hearty', 'comfort-food', 'one-pot']
}
]