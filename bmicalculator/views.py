from django.shortcuts import render
import joblib

model = joblib.load('bmi_model.pkl')

def bmi_view(request):
    bmi = None
    message = None
    if request.method == "POST":
        weight = request.POST.get('weight')
        height = request.POST.get('height')
        try:
            weight = float(weight)
            height = float(height) / 100  # cm to meters
            bmi = round(weight / (height ** 2), 2)

            if bmi < 18.5:
                message = "You are underweight."
            elif bmi < 25:
                message = "You have a normal weight."
            elif bmi < 30:
                message = "You are overweight."
            else:
                message = "You are obese."
        except (TypeError, ValueError):
            message = "Please enter valid numbers."

    return render(request, 'bmicalculator/home.html', {'bmi': bmi, 'message': message})
