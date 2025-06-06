from datetime import date
from health import (
    calculate_bmi,
    bmi_category,
    recommend_plan,
    total_daily_calories,
    save_log,
    load_logs,
    age_recommendation,
    suggest_foods,
    estimate_burned_calories,
    lookup_calories,
    smart_calorie_goal,
    calculate_points,
    set_language,
    _,
)

def prompt_calorie_entries():
    entries = []
    print(_("Enter calories or scan product barcodes. Type 'done' when finished."))
    while True:
        value = input(_("Calories or barcode: "))
        if value.lower() == "done":
            break
        if value.isdigit() and len(value) >= 6:
            cal = lookup_calories(value)
            if cal is None:
                print(_("Product not found. Please enter calories manually."))
                continue
            print(_("Added {cal} kcal from barcode {code}.").format(cal=cal, code=value))
            entries.append(cal)
            continue
        try:
            entries.append(float(value))
        except ValueError:
            print(_("Please enter a number or 'done'."))
    return entries


def prompt_steps():
    try:
        return int(input(_("Enter daily steps (optional, 0 if none): ")))
    except ValueError:
        return 0


def prompt_meal_plan():
    plan = []
    while True:
        desc = input(_("Meal description (or 'done'): "))
        if desc.lower() == "done":
            break
        try:
            cals = float(input(_("Calories: ")))
        except ValueError:
            print(_("Please enter a number or 'done'."))
            continue
        plan.append({"meal": desc, "calories": cals})
    return plan


def main():
    lang = input("Select language (en/es/de): ").lower()
    if lang not in ("en", "es", "de"):
        lang = "en"
    set_language(lang)

    calories = prompt_calorie_entries()
    meal_plan = prompt_meal_plan()
    total = total_daily_calories(calories)
    print(_("Total calories consumed today: {total}").format(total=total))
    steps = prompt_steps()
    burned = estimate_burned_calories(steps)
    print(_("Estimated calories burned: {burned}").format(burned=burned))

    try:
        age = int(input(_("Enter your age: ")))
        weight = float(input(_("Enter your weight in kg: ")))
        height = float(input(_("Enter your height in meters: ")))
    except ValueError:
        print(_("Please enter a number or 'done'."))
        return

    country = input(_("Enter your country or region: "))

    bmi = calculate_bmi(weight, height)
    category = bmi_category(bmi)
    plan = recommend_plan(bmi)
    advice = age_recommendation(age)
    foods = ", ".join(suggest_foods(country))

    print(_("Your BMI is {value:.2f} ({category}).").format(value=bmi, category=category))
    print(_("Recommendation: {plan}").format(plan=plan))
    print(_("Age advice: {text}").format(text=advice))
    if foods:
        print(_("Food suggestions for {place}: {items}").format(place=country, items=foods))

    history = load_logs()
    goal = smart_calorie_goal(history, bmi)
    print(_("Adjusted calorie goal: {goal}").format(goal=goal))
    points = calculate_points(total - burned, goal)
    print(_("Total points earned: {pts}").format(pts=points))

    log_entry = {
        "date": date.today().isoformat(),
        "age": age,
        "country": country,
        "meals": meal_plan,
        "calories": calories,
        "total_calories": total,
        "steps": steps,
        "burned_calories": burned,
        "calorie_goal": goal,
        "points": points,
        "weight": weight,
        "height": height,
        "bmi": bmi,
    }
    save_log(log_entry)


if __name__ == "__main__":
    main()
 
