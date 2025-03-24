document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('dietForm');
    const resultsDiv = document.getElementById('results');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = {
            age: parseInt(document.getElementById('age').value),
            weight: parseFloat(document.getElementById('weight').value),
            height: parseFloat(document.getElementById('height').value),
            gender: document.getElementById('gender').value,
            activity_level: document.getElementById('activity').value,
            goal: document.getElementById('goal').value
        };

        try {
            const response = await fetch('http://localhost:8000/recommend', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            displayResults(data);
        } catch (error) {
            console.error('Error:', error);
            alert('There was an error getting your recommendations. Please try again.');
        }
    });

    function displayResults(data) {
        // Display daily calories
        document.getElementById('dailyCalories').textContent = 
            `${Math.round(data.daily_calories)} calories per day`;

        // Display meal plan
        const mealPlanHtml = Object.entries(data.meal_plan)
            .map(([meal, calories]) => `
                <div class="meal-item">
                    <h4>${meal.charAt(0).toUpperCase() + meal.slice(1)}</h4>
                    <p>${Math.round(calories)} calories</p>
                </div>
            `).join('');
        document.getElementById('mealPlan').innerHTML = mealPlanHtml;

        // Display food recommendations
        const foodRecsHtml = data.food_recommendations
            .map(food => `
                <div class="food-item">
                    <h4>${food.name}</h4>
                    <p>Calories: ${food.calories}</p>
                    <p>Protein: ${food.protein}g</p>
                    <p>Carbs: ${food.carbs}g</p>
                    <p>Fats: ${food.fats}g</p>
                </div>
            `).join('');
        document.getElementById('foodRecommendations').innerHTML = foodRecsHtml;

        // Show results
        resultsDiv.classList.remove('hidden');
    }
}); 