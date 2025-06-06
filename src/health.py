import math
import json
import os
from datetime import date
import gettext

LOCALE_DIR = os.path.join(os.path.dirname(__file__), "locales")
translation = gettext.translation("messages", localedir=LOCALE_DIR, fallback=True)
_ = translation.gettext


def set_language(lang):
    """Load translations for the given language code."""
    global translation, _
    translation = gettext.translation(
        "messages", localedir=LOCALE_DIR, languages=[lang], fallback=True
    )
    _ = translation.gettext

# BMI Calculation

def calculate_bmi(weight, height):
    """Return Body Mass Index (BMI) given weight in kg and height in meters."""
    if height <= 0:
        raise ValueError("Height must be greater than zero")
    return weight / (height ** 2)


def bmi_category(bmi):
    """Return BMI category based on WHO classifications."""
    if bmi < 18.5:
        return _("Underweight")
    elif bmi < 25:
        return _("Normal weight")
    elif bmi < 30:
        return _("Overweight")
    else:
        return _("Obesity")


def recommend_plan(bmi):
    """Provide a simple calorie adjustment recommendation based on BMI."""
    if bmi < 18.5:
        return _(
            "Your BMI indicates you're underweight. Increase calorie intake by 300-500 kcal/day and focus on nutrient-dense foods."
        )
    elif bmi < 25:
        return _(
            "Your BMI is in the normal range. Maintain a balanced diet to keep your current weight."
        )
    elif bmi < 30:
        return _(
            "Your BMI indicates overweight. Reduce daily calories by 300-500 kcal and increase physical activity."
        )
    else:
        return _(
            "Your BMI is in the obese range. Consult a healthcare provider for a personalized plan and aim to reduce calories by 500-700 kcal/day."
        )


def total_daily_calories(calorie_entries):
    """Return the sum of calorie entries for the day."""
    return sum(calorie_entries)


HEALTH_LOG = "health_history.json"


def load_logs():
    if not os.path.exists(HEALTH_LOG):
        return []
    with open(HEALTH_LOG, "r") as f:
        return json.load(f)


def save_log(entry):
    history = load_logs()
    history.append(entry)
    with open(HEALTH_LOG, "w") as f:
        json.dump(history, f, indent=2)


FOOD_SUGGESTIONS = {
    "mexico": ["tacos de pollo", "frijoles", "ensalada"],
    "spain": ["paella", "gazpacho", "ensalada"],
    "usa": ["chicken salad", "oatmeal", "grilled salmon"],
}


def suggest_foods(country):
    """Return a list of regional food suggestions for the given country."""
    return FOOD_SUGGESTIONS.get(country.lower(), [])


def age_recommendation(age):
    """Return a simple health recommendation based on age."""
    if age < 18:
        return _("Consult a pediatric specialist for personalized advice.")
    elif age < 65:
        return _("Maintain regular exercise and balanced nutrition.")
    else:
        return _("Include flexibility and strength exercises to stay active.")


# Device & AI utilities

STEP_CAL_FACTOR = 0.04  # calories burned per step (rough estimate)

PRODUCT_DB = {
    "0123456789": 150,
    "9876543210": 250,
}


def estimate_burned_calories(steps):
    """Estimate calories burned based on step count."""
    return steps * STEP_CAL_FACTOR


def lookup_calories(barcode):
    """Return calories for a given product barcode from a small sample DB."""
    return PRODUCT_DB.get(barcode)


def smart_calorie_goal(history, bmi):
    """Adjust daily calorie goal based on recent history and BMI."""
    if history:
        recent = history[-7:]
        avg = sum(e.get("total_calories", 0) for e in recent) / len(recent)
    else:
        avg = 2000
    if bmi < 18.5:
        return avg + 300
    elif bmi < 25:
        return avg
    elif bmi < 30:
        return max(1200, avg - 300)
    else:
        return max(1000, avg - 500)


def calculate_points(total, goal):
    """Simple gamification: award points based on meeting the goal."""
    return 10 if total <= goal else 5
