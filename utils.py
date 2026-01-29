def calculate_bmi(weight, height):
    height_m = height / 100
    return round(weight / (height_m ** 2), 2)

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 24.9:
        return "Normal"
    elif bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

def fitness_level(bmi, fat):
    if bmi > 30 or fat > 30:
        return "Beginner"
    elif bmi > 25 or fat > 22:
        return "Intermediate"
    else:
        return "Advanced"

def muscle_health(fat):
    if fat > 30:
        return "Low muscle density ❌"
    elif fat > 20:
        return "Average muscle density ⚠️"
    else:
        return "Good muscle density ✅"
