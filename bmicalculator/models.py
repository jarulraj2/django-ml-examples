# bmi_model.py
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib

# Sample training data: [weight (kg), height (cm)]
X = np.array([
    [50, 160],
    [60, 165],
    [70, 170],
    [80, 175],
    [90, 180],
    [100, 185]
])
# BMI values corresponding to the above samples
y = np.array([19.5, 22.0, 24.2, 26.1, 27.8, 29.2])

model = LinearRegression()
model.fit(X, y)

# Save model for use in Django app
joblib.dump(model, 'bmi_model.pkl')
print("Model saved as bmi_model.pkl")
