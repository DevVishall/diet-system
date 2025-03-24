from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import json

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load food database
food_db = pd.DataFrame({
    'name': ['Chicken Breast', 'Brown Rice', 'Broccoli', 'Salmon', 'Sweet Potato', 
            'Quinoa', 'Spinach', 'Greek Yogurt', 'Eggs', 'Oatmeal'],
    'calories': [165, 216, 55, 208, 103, 120, 23, 130, 155, 307],
    'protein': [31, 5, 3.7, 22, 2, 4.4, 2.9, 17, 13, 11],
    'carbs': [0, 45, 11.2, 0, 24, 21.3, 3.6, 9, 1, 55],
    'fats': [3.6, 1.8, 0.6, 13, 0.2, 1.9, 0.4, 0.7, 11, 5],
    'category': ['protein', 'carbs', 'vegetable', 'protein', 'carbs', 
                'carbs', 'vegetable', 'protein', 'protein', 'carbs']
})

class UserInput(BaseModel):
    age: int
    weight: float
    height: float
    gender: str
    activity_level: str
    goal: str

class DietRecommendation(BaseModel):
    daily_calories: float
    meal_plan: dict
    food_recommendations: List[dict]

@app.get("/")
async def root():
    return {"message": "Welcome to Diet Recommendation System"}

@app.post("/recommend", response_model=DietRecommendation)
async def get_diet_recommendation(user_input: UserInput):
    try:
        # Calculate BMR using Harris-Benedict equation
        if user_input.gender.lower() == "male":
            bmr = 88.362 + (13.397 * user_input.weight) + (4.799 * user_input.height) - (5.677 * user_input.age)
        else:
            bmr = 447.593 + (9.247 * user_input.weight) + (3.098 * user_input.height) - (4.330 * user_input.age)

        # Activity level multiplier
        activity_multipliers = {
            "sedentary": 1.2,
            "light": 1.375,
            "moderate": 1.55,
            "active": 1.725,
            "very_active": 1.9
        }
        
        tdee = bmr * activity_multipliers.get(user_input.activity_level.lower(), 1.2)

        # Adjust calories based on goal
        if user_input.goal.lower() == "weight_loss":
            daily_calories = tdee - 500
        elif user_input.goal.lower() == "weight_gain":
            daily_calories = tdee + 500
        else:  # maintenance
            daily_calories = tdee

        # Create meal plan
        meal_plan = {
            "breakfast": 0.3 * daily_calories,
            "lunch": 0.35 * daily_calories,
            "dinner": 0.25 * daily_calories,
            "snacks": 0.1 * daily_calories
        }

        # Generate food recommendations
        recommendations = []
        for category in ['protein', 'carbs', 'vegetable']:
            category_foods = food_db[food_db['category'] == category].to_dict('records')
            if category_foods:
                recommendations.extend(category_foods)

        return DietRecommendation(
            daily_calories=round(daily_calories, 2),
            meal_plan={k: round(v, 2) for k, v in meal_plan.items()},
            food_recommendations=recommendations
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 