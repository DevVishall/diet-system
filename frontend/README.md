# Diet Recommendation System

A simple web application that provides personalized diet recommendations based on user inputs such as age, weight, height, gender, activity level, and goals.

## Features

- Calculates daily caloric needs using the Harris-Benedict equation
- Provides meal plan distribution
- Recommends foods based on nutritional requirements
- Modern and responsive user interface

## Project Structure

```
.
├── backend/
│   └── main.py
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── script.js
└── requirements.txt
```

## Setup Instructions

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Start the backend server:
```bash
cd backend
uvicorn main:app --reload
```

3. Open the frontend:
- Navigate to the `frontend` directory
- Open `index.html` in your web browser

## Usage

1. Fill out the form with your personal information:
   - Age
   - Weight (in kg)
   - Height (in cm)
   - Gender
   - Activity Level
   - Goal (weight loss, maintenance, or weight gain)

2. Click "Get Recommendations" to receive your personalized diet plan

3. View your results:
   - Daily caloric needs
   - Meal plan distribution
   - Recommended foods with nutritional information

## Technical Details

- Backend: Python with FastAPI
- Frontend: HTML, CSS, and JavaScript
- API Endpoint: http://localhost:8000/recommend

## Notes

- The food database is currently a simple example dataset
- Calculations are based on the Harris-Benedict equation for BMR
- The system provides basic recommendations and should not replace professional medical advice 