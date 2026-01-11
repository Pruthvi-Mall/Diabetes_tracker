def lifestyle_advice(risk, bmi, glucose, age):
    tips = []

    if risk == 1:
        tips.append("Avoid sugary and processed foods")
        tips.append("Drink 3–4 liters of water daily")
        tips.append("Walk at least 30 minutes per day")
    else:
        tips.append("Maintain balanced diet")
        tips.append("Drink at least 2.5 liters of water daily")
        tips.append("Exercise 20 minutes daily")

    if bmi > 30:
        tips.append("Reduce calorie intake and avoid oily foods")
    if age > 45:
        tips.append("Monitor blood sugar weekly")

    return tips[:3]


def diet_plan(risk):
    if risk == 1:
        return ["Brown rice", "Green vegetables", "Low sugar fruits"]
    else:
        return ["Balanced meals", "Fresh fruits", "Adequate protein"]


def emergency_alert(glucose):
    if glucose > 180:
        return "⚠ HIGH BLOOD SUGAR – Immediate medical consultation recommended"
    return "No emergency"
